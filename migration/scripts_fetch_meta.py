"""
Haal per live-URL de SEO-meta uit de HTML-head (RankMath zit niet in de REST API).
Schrijft source/meta.json: {url: {title, description, canonical, robots, og_*}}.
Hervat automatisch: al opgehaalde URL's worden overgeslagen.
"""
import json, re, sys, threading, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests

SRC = Path(__file__).resolve().parent / "source"
OUT = SRC / "meta.json"
URLS = [u for u in (SRC / "sitemap-urls.txt").read_text(encoding="utf-8").split() if u]

done = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
todo = [u for u in URLS if u not in done]
print(f"{len(URLS)} URL's, {len(done)} al gedaan, {len(todo)} te doen", flush=True)

lock = threading.Lock()
S = requests.Session()
S.headers.update({"User-Agent": "spirituelebetekenis-migration/1.0"})

HEAD_END = re.compile(rb"</head>", re.I)

def pick(head, pattern):
    m = re.search(pattern, head, re.I | re.S)
    return m.group(1).strip() if m else ""

def scrape(url):
    for attempt in range(3):
        try:
            r = S.get(url, timeout=45, stream=True)
            chunks = []
            for chunk in r.iter_content(16384):
                chunks.append(chunk)
                if HEAD_END.search(b"".join(chunks[-2:])) or sum(map(len, chunks)) > 400_000:
                    break
            r.close()
            raw = b"".join(chunks).decode("utf-8", "replace")
            head = raw.split("</head>")[0]
            return {
                "status": r.status_code,
                "title": pick(head, r"<title[^>]*>(.*?)</title>"),
                "description": pick(head, r'<meta name="description" content="(.*?)"'),
                "canonical": pick(head, r'<link rel="canonical" href="(.*?)"'),
                "robots": pick(head, r'<meta name="robots" content="(.*?)"'),
                "og_title": pick(head, r'<meta property="og:title" content="(.*?)"'),
                "og_description": pick(head, r'<meta property="og:description" content="(.*?)"'),
                "og_image": pick(head, r'<meta property="og:image" content="(.*?)"'),
            }
        except Exception:
            if attempt == 2:
                return {"status": 0, "error": True}
            time.sleep(2 * (attempt + 1))

count = 0
def work(url):
    global count
    res = scrape(url)
    with lock:
        done[url] = res
        count += 1
        if count % 250 == 0:
            OUT.write_text(json.dumps(done, ensure_ascii=False), encoding="utf-8")
            print(f"  {count}/{len(todo)}", flush=True)

with ThreadPoolExecutor(max_workers=8) as ex:
    list(ex.map(work, todo))

OUT.write_text(json.dumps(done, ensure_ascii=False), encoding="utf-8")
bad = [u for u, v in done.items() if v.get("status") != 200 or not v.get("title")]
print(f"klaar: {len(done)} opgehaald, {len(bad)} zonder titel/niet-200", flush=True)
for u in bad[:20]:
    print("  !", u, done[u].get("status"), flush=True)
