import csv
import hashlib
import os
import re
import time
from datetime import datetime
from typing import Dict, List, Optional

import requests
import trafilatura
from bs4 import BeautifulSoup
from fastapi import HTTPException

from src.config import settings
from src.lib.clients.serpapi import SerpAPIClient
from src.schemas.scraping_schema import (
    DeleteFileResponse,
    EtlResponse,
    FileItem,
    ListFilesResponse,
    SearchLinksResponse,
)


class ScrapingService:
    def __init__(self):
        self.client = SerpAPIClient(api_key=settings.serp_api_key)
        self.data_dir = os.path.join(os.getcwd(), "data")
        self.out_dir = os.path.join(self.data_dir, "scraping", "search")
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.out_dir, exist_ok=True)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/127.0.0.1 Safari/537.36"
        }

    def _slug(self, text: str) -> str:
        value = re.sub(r"[^\w\s-]", "", text, flags=re.U).strip().lower()
        return re.sub(r"[\s_-]+", "_", value)

    def _extract_links(self, news_results: List[dict]) -> List[Dict[str, str]]:
        links: List[Dict[str, str]] = []
        for item in news_results:
            if item.get("link"):
                links.append({"link": item["link"]})
        return links

    def _save_links_csv(self, records: List[Dict[str, str]], filename: str) -> str:
        if not records:
            raise HTTPException(status_code=404, detail="sem registros para salvar")
        file_path = os.path.join(self.data_dir, filename)
        with open(file_path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["link"])
            writer.writeheader()
            writer.writerows(records)
        return file_path

    def _fetch_html(self, url: str) -> str:
        try:
            r = requests.get(url, headers=self.headers, timeout=20)
            r.raise_for_status()
            return r.text
        except requests.exceptions.RequestException:
            return ""

    def _extract_title(self, html: str) -> str:
        if not html:
            return ""
        soup = BeautifulSoup(html, "html.parser")
        og = soup.find("meta", property="og:title") or soup.find(
            "meta", attrs={"name": "title"}
        )
        if og and og.get("content"):
            return str(og["content"]).strip()
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        h1 = soup.find("h1")
        return h1.get_text(strip=True) if h1 else ""

    def _extract_text(self, html: str) -> str:
        if not html:
            return ""
        try:
            text = trafilatura.extract(
                html, include_comments=False, include_tables=False
            )
            return str(text or "").strip()
        except Exception:
            return ""

    def _sanitize_filename(self, name: str, maxlen: int = 120) -> str:
        safe = "".join(
            ch if ch.isalnum() or ch in " ._-–—()" else "_" for ch in name
        ).strip()
        if len(safe) > maxlen:
            safe = safe[:maxlen].rstrip("_ .-")
        return safe or "sem_titulo"

    def _save_single_csv(self, title: str, url: str, content: str):
        base = self._sanitize_filename(title)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{base}_{ts}.csv"
        path = os.path.join(self.out_dir, filename)
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "url", "content"])
            writer.writeheader()
            writer.writerow(
                {
                    "title": title,
                    "url": url,
                    "content": content.replace("\n", " ").strip(),
                }
            )

    def _process_link(self, url: str, seen_titles: set):
        html = self._fetch_html(url)
        if not html:
            return
        title = (
            self._extract_title(html)
            or f"artigo_{hashlib.sha1(url.encode('utf-8')).hexdigest()[:10]}"
        )
        key = title.lower().strip()
        if key in seen_titles:
            return
        content = self._extract_text(html)
        if not content:
            return
        self._save_single_csv(title, url, content)
        seen_titles.add(key)

    def _etl_one_file(self, input_file: str):
        try:
            with open(input_file, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                links = [row["link"] for row in reader if row.get("link")]
        except Exception:
            return
        seen = set()
        for url in links:
            self._process_link(url, seen)
            time.sleep(0.2)

    def search_links(
        self,
        query: str,
        limit: int = 10,
        gl: str = "br",
        hl: str = "pt",
        engine: str = "google_news",
        when: Optional[str] = None,
        extra_params: Optional[Dict[str, str]] = None,
    ) -> SearchLinksResponse:
        if not query or not query.strip():
            raise HTTPException(status_code=400, detail="query inválida")
        if limit < 1:
            raise HTTPException(status_code=400, detail="limit inválido")
        limit = min(limit, 100)

        params: Dict[str, str | int] = {
            "engine": engine,
            "q": query,
            "gl": gl,
            "hl": hl,
            "num": min(10, limit),
            "start": 0,
        }
        if when:
            params["when"] = when
        if extra_params:
            params.update(extra_params)

        collected: List[Dict[str, str]] = []
        page = 1
        while len(collected) < limit:
            result = self.client.search(**params)
            news = result.get("news_results", []) if isinstance(result, dict) else []
            if not news:
                break
            links = self._extract_links(news)
            for item in links:
                if len(collected) >= limit:
                    break
                collected.append(item)
            if len(news) < int(params["num"]):
                break
            params["start"] = int(params.get("start", 0)) + int(params["num"])
            params["num"] = min(10, limit - len(collected))
            page += 1

        if not collected:
            raise HTTPException(status_code=404, detail="nenhum link encontrado")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"links_{self._slug(query)}_{timestamp}.csv"
        self._save_links_csv(collected, filename)

        return SearchLinksResponse(
            filename=filename,
            total_links=len(collected),
            path=os.path.join(self.data_dir, filename),
        )

    def etl(self, filename: str) -> EtlResponse:
        if not filename or "/" in filename or ".." in filename:
            raise HTTPException(status_code=400, detail="filename inválido")
        csv_path = os.path.join(self.data_dir, filename)
        if not os.path.exists(csv_path):
            raise HTTPException(status_code=404, detail="arquivo não encontrado")
        try:
            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                total = sum(1 for _ in reader)
        except Exception:
            total = 0

        self._etl_one_file(csv_path)

        return EtlResponse(
            filename=filename,
            processed=total,
            output_dir=self.out_dir,
        )

    def list_files(self, kind: str = "all") -> ListFilesResponse:
        kinds = {"links", "scraped", "all"}
        if kind not in kinds:
            raise HTTPException(status_code=400, detail="kind inválido")

        def file_info(path: str) -> FileItem:
            st = os.stat(path)
            return FileItem(
                name=os.path.basename(path),
                size=st.st_size,
                modified=datetime.fromtimestamp(st.st_mtime).isoformat(),
                path=path,
            )

        links_files = []
        scraped_files = []
        links_glob = os.path.join(self.data_dir, "links_*.csv")
        scraped_glob = os.path.join(self.out_dir, "*.csv")

        if kind in ("links", "all"):
            import glob

            for p in sorted(glob.glob(links_glob)):
                links_files.append(file_info(p))

        if kind in ("scraped", "all"):
            import glob

            for p in sorted(glob.glob(scraped_glob)):
                scraped_files.append(file_info(p))

        return ListFilesResponse(links=links_files, scraped=scraped_files)

    def delete_file(self, kind: str, filename: str) -> DeleteFileResponse:
        if kind not in {"links", "scraped"}:
            raise HTTPException(status_code=400, detail="kind inválido")
        if not filename or "/" in filename or ".." in filename:
            raise HTTPException(status_code=400, detail="filename inválido")
        base = self.data_dir if kind == "links" else self.out_dir
        path = os.path.join(base, filename)
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="arquivo não encontrado")
        os.remove(path)
        return DeleteFileResponse(deleted=filename, kind=kind)
