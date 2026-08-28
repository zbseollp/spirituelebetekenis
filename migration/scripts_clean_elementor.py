"""
De WordPress-pagina's (home, over, contact, trainingen) zijn met Elementor
gebouwd. Wat de REST API teruggeeft is dus een berg <div>'s die zonder de
Elementor-CSS nergens op lijkt.

Dit script haalt daar de semantische inhoud uit: koppen, alinea's, lijsten,
afbeeldingen en links, in dezelfde volgorde. Interne links en afbeeldings-URL's
worden relatief gemaakt zodat ze op de nieuwe site blijven werken.

Draait ná scripts_build_content.py en schrijft de opgeschoonde HTML terug naar
src/content/pages/*.json.
"""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

PAGES_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "pages"
DOMAIN = "https://spirituelebetekenis.com"

KEEP = {"h1","h2","h3","h4","h5","h6","p","ul","ol","li","strong","em","b","i",
        "br","a","img","blockquote","figure","figcaption","table","thead",
        "tbody","tr","th","td","hr"}
VOID = {"br", "img", "hr"}
KEEP_ATTRS = {"a": {"href", "rel", "target"}, "img": {"src", "alt", "width", "height", "loading"}}


class Cleaner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out = []
        self.skip_depth = 0
        self.skip_tag = None

    def handle_starttag(self, tag, attrs):
        # <script>/<style> en hun inhoud helemaal weglaten
        if tag in ("script", "style", "noscript", "svg"):
            self.skip_tag, self.skip_depth = tag, 1
            return
        if self.skip_tag:
            if tag == self.skip_tag:
                self.skip_depth += 1
            return
        if tag not in KEEP:
            return
        allowed = KEEP_ATTRS.get(tag, set())
        parts = []
        for k, v in attrs:
            if k not in allowed or v is None:
                continue
            if k in ("href", "src"):
                v = v.replace(DOMAIN, "")  # interne links relatief maken
            parts.append(f' {k}="{v}"')
        self.out.append(f"<{tag}{''.join(parts)}>")

    def handle_endtag(self, tag):
        if self.skip_tag:
            if tag == self.skip_tag:
                self.skip_depth -= 1
                if self.skip_depth == 0:
                    self.skip_tag = None
            return
        if tag in KEEP and tag not in VOID:
            self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skip_tag:
            self.out.append(data)

    def handle_entityref(self, name):
        if not self.skip_tag:
            self.out.append(f"&{name};")

    def handle_charref(self, name):
        if not self.skip_tag:
            self.out.append(f"&#{name};")


def tidy(html: str) -> str:
    c = Cleaner()
    c.feed(html)
    c.close()
    out = "".join(c.out)
    # lege elementen en overtollige witruimte opruimen
    for _ in range(4):
        out = re.sub(r"<(p|li|h[1-6]|ul|ol|strong|em)>\s*</\1>", "", out)
    out = re.sub(r"[ \t]+", " ", out)
    out = re.sub(r"(\s*\n\s*){2,}", "\n", out)
    return out.strip()


changed = []
for f in sorted(PAGES_DIR.glob("*.json")):
    rec = json.loads(f.read_text(encoding="utf-8"))
    before = rec["content"]
    if "data-elementor-type" not in before:
        continue
    after = tidy(before)
    rec["content"] = after
    f.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
    changed.append((rec["slug"], len(before), len(after)))

for slug, b, a in changed:
    print(f"{slug:<16} {b:>7} -> {a:>6} tekens")
if not changed:
    print("geen Elementor-pagina's gevonden (al opgeschoond?)")
