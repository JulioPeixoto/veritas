import os
import time
import csv
from datetime import datetime
from src.lib.clients.serpapi import SerpAPIClient
from src.config import settings

DATA_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_DIR, exist_ok=True)

client = SerpAPIClient(api_key=settings.serp_api_key)

def extract_links(news_results: list) -> list:
    links = []
    for item in news_results:
        if item.get("link"):
            links.append({"link": item["link"]})
    return links

def save_to_csv(records: list, filename: str):
    if not records:
        print("Nenhum registro para salvar.")
        return
    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["link"])
        writer.writeheader()
        writer.writerows(records)
    print(f"✅ {len(records)} links salvos em {file_path}")

def main():
    query = "clima Aracaju Sergipe"
    country = "br"
    language = "pt"
    engine = "google_news"
    params = {
        "engine": engine,
        "q": query,
        "gl": country,
        "hl": language,
        "num": 1,
        "start": 0
    }
    page = 1
    total_records = 0
    while True:
        print(f"\n🌎 Buscando página {page} (start={params['start']}) ...")
        result = client.search(**params)
        news = result.get("news_results", [])
        if not news:
            print("Sem mais resultados.")
            break
        links = extract_links(news)
        total_records += len(links)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"links_clima_aracaju_p{page}_{timestamp}.csv"
        save_to_csv(links, filename)
        if len(news) < params["num"]:
            break
        params["start"] += params["num"]
        page += 1
        time.sleep(1)
    print(f"\n✅ Total de links coletados: {total_records}")

if __name__ == "__main__":
    main()
