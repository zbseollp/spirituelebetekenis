"""
Zet de opgehaalde REST-data plus de gescrapete SEO-meta om naar de vorm die
Astro leest: één JSON per bericht/pagina in src/content/, plus een compacte
index met alleen de velden die de archieven nodig hebben.

De losse bestanden houden het geheugengebruik van de build laag; 6792 posts
met samen ~160 MB HTML passen niet comfortabel in één import.
"""
import json, re, html as H
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "source"
ROOT = HERE.parent
POSTS_DIR = ROOT / "src" / "content" / "posts"
PAGES_DIR = ROOT / "src" / "content" / "pages"
for d in (POSTS_DIR, PAGES_DIR):
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.json"):
        old.unlink()

meta = json.loads((SRC / "meta.json").read_text(encoding="utf-8"))
cats = {c["id"]: {"slug": c["slug"], "name": H.unescape(c["name"])}
        for c in json.loads((SRC / "categories.json").read_text(encoding="utf-8"))}

def unescape(s):
    return H.unescape(s or "").strip()

def plain(htm, limit=160):
    t = re.sub(r"<[^>]+>", " ", htm or "")
    t = re.sub(r"\s+", " ", H.unescape(t)).strip()
    return t if len(t) <= limit else t[: t.rfind(" ", 0, limit)] + "…"

def meta_for(link):
    return meta.get(link) or meta.get(link.rstrip("/") + "/") or {}

index = []

posts = json.loads((SRC / "posts.json").read_text(encoding="utf-8"))
for p in posts:
    m = meta_for(p["link"])
    cat_list = [cats[c] for c in p["categories"] if c in cats]
    body = p["content"]["rendered"]
    rec = {
        "slug": p["slug"],
        "title": unescape(p["title"]["rendered"]),
        "date": p["date"],
        "modified": p["modified"],
        "categories": cat_list,
        "content": body,
        "seoTitle": m.get("title", ""),
        "seoDescription": m.get("description", "") or plain(p["excerpt"]["rendered"] or body),
        "canonical": m.get("canonical", "") or p["link"],
        "ogImage": m.get("og_image", ""),
    }
    (POSTS_DIR / f"{p['slug']}.json").write_text(
        json.dumps(rec, ensure_ascii=False), encoding="utf-8")
    index.append({
        "slug": rec["slug"], "title": rec["title"], "date": rec["date"],
        "categories": [c["slug"] for c in cat_list],
        "excerpt": plain(p["excerpt"]["rendered"] or body, 150),
    })

pages = json.loads((SRC / "pages.json").read_text(encoding="utf-8"))
for p in pages:
    m = meta_for(p["link"])
    rec = {
        "slug": p["slug"],
        "title": unescape(p["title"]["rendered"]),
        "date": p["date"],
        "modified": p["modified"],
        "content": p["content"]["rendered"],
        "seoTitle": m.get("title", ""),
        "seoDescription": m.get("description", ""),
        "canonical": m.get("canonical", "") or p["link"],
        "ogImage": m.get("og_image", ""),
    }
    (PAGES_DIR / f"{p['slug']}.json").write_text(
        json.dumps(rec, ensure_ascii=False), encoding="utf-8")

index.sort(key=lambda r: r["date"], reverse=True)
(ROOT / "src" / "data").mkdir(parents=True, exist_ok=True)
(ROOT / "src" / "data" / "index.json").write_text(
    json.dumps(index, ensure_ascii=False), encoding="utf-8")
(ROOT / "src" / "data" / "categories.json").write_text(
    json.dumps(sorted(cats.values(), key=lambda c: c["name"]), ensure_ascii=False, indent=1),
    encoding="utf-8")

print(f"berichten: {len(posts)}   pagina's: {len(pages)}")
print(f"zonder seoTitle: {sum(1 for r in posts if not meta_for(r['link']).get('title'))}")
print(f"index.json: {(ROOT / 'src' / 'data' / 'index.json').stat().st_size / 1e6:.1f} MB")
