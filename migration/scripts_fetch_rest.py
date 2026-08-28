"""
Haal de volledige inhoud van spirituelebetekenis.com op via de WP REST API.
Schrijft ruwe JSON per collectie naar migration/source/.
"""
import json, sys, time
from pathlib import Path
import requests

BASE = "https://spirituelebetekenis.com/wp-json/wp/v2"
OUT = Path(__file__).resolve().parent / "source"
OUT.mkdir(parents=True, exist_ok=True)
UA = "spirituelebetekenis-migration/1.0"
S = requests.Session()
S.headers.update({"User-Agent": UA})

def fetch_all(endpoint, per_page=100, extra=None):
    items, page = [], 1
    while True:
        params = {"per_page": per_page, "page": page, "orderby": "id", "order": "asc"}
        if extra:
            params.update(extra)
        for attempt in range(4):
            try:
                r = S.get(f"{BASE}/{endpoint}", params=params, timeout=60)
                break
            except requests.RequestException as e:
                if attempt == 3:
                    raise
                time.sleep(2 * (attempt + 1))
        if r.status_code == 400 and page > 1:
            break  # voorbij de laatste pagina
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        items.extend(batch)
        total = r.headers.get("X-WP-TotalPages")
        print(f"  {endpoint} p{page}/{total} -> {len(items)}", flush=True)
        if total and page >= int(total):
            break
        page += 1
        time.sleep(0.25)
    return items

def main():
    targets = sys.argv[1:] or ["categories", "tags", "users", "pages", "media", "posts"]
    for name in targets:
        print(f"== {name}", flush=True)
        data = fetch_all(name)
        (OUT / f"{name}.json").write_text(
            json.dumps(data, ensure_ascii=False), encoding="utf-8"
        )
        print(f"   {len(data)} -> {name}.json", flush=True)

if __name__ == "__main__":
    main()
