import os
import csv
import time
import glob
import hashlib
import requests
import trafilatura
from bs4 import BeautifulSoup
from datetime import datetime

DATA_DIR = os.path.join(os.getcwd(), "data")
OUT_DIR = os.path.join(DATA_DIR, "scraping", "search")
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/127.0.0.1 Safari/537.36"
}

def sanitize_filename(name: str, maxlen: int = 120) -> str:
    safe = "".join(ch if ch.isalnum() or ch in " ._-–—()" else "_" for ch in name).strip()
    if len(safe) > maxlen:
        safe = safe[:maxlen].rstrip("_ .-")
    return safe or "sem_titulo"

def fetch_html(url: str) -> str:
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        return r.text
    except requests.exceptions.RequestException as e:
        print(f"erro ao baixar {url}: {e}")
        return ""

def extract_title(html: str) -> str:
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    og = soup.find("meta", property="og:title") or soup.find("meta", attrs={"name": "title"})
    if og and og.get("content"):
        return og["content"].strip()
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else ""

def extract_text(html: str) -> str:
    if not html:
        return ""
    try:
        text = trafilatura.extract(html, include_comments=False, include_tables=False)
        return (text or "").strip()
    except Exception as e:
        print(f"erro ao extrair texto: {e}")
        return ""

def save_single_csv(title: str, url: str, content: str):
    base = sanitize_filename(title)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base}_{ts}.csv"
    path = os.path.join(OUT_DIR, filename)
    try:
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "url", "content"])
            writer.writeheader()
            writer.writerow({"title": title, "url": url, "content": content.replace("\n", " ").strip()})
        print(f"✅ salvo: {path}")
    except OSError as e:
        print(f"erro ao salvar {path}: {e}")

def process_link(url: str, seen_titles: set):
    try:
        html = fetch_html(url)
        if not html:
            return
        title = extract_title(html) or f"artigo_{hashlib.sha1(url.encode('utf-8')).hexdigest()[:10]}"
        key = title.lower().strip()
        if key in seen_titles:
            return
        content = extract_text(html)
        if not content:
            return
        save_single_csv(title, url, content)
        seen_titles.add(key)
    except Exception as e:
        print(f"erro inesperado em {url}: {e}")

def etl_one_file(input_file: str):
    try:
        with open(input_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            links = [row["link"] for row in reader if row.get("link")]
    except Exception as e:
        print(f"erro ao ler {input_file}: {e}")
        return
    seen = set()
    for i, url in enumerate(links, 1):
        print(f"[{i}/{len(links)}] {url}")
        process_link(url, seen)
        time.sleep(0.2)

def main():
    pattern = os.path.join(DATA_DIR, "links_clima_aracaju_p*.csv")
    inputs = sorted(glob.glob(pattern))
    if not inputs:
        print("⚠️ Nenhum CSV de links encontrado.")
        return
    for path in inputs:
        print(f"🔎 Processando: {path}")
        etl_one_file(path)

if __name__ == "__main__":
    main()
