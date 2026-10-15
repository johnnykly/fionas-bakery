#!/usr/bin/env python3
"""Build the static site from src/ into docs/ (served by GitHub Pages).

Each page in src/pages/ starts with a JSON header in an HTML comment:
    <!--{"path": "/priser/", "title": "...", "description": "...", ...}-->
Placeholders in page bodies:
    {{root}}                     relative path to the site root
    {{icon:name}}                inline Phosphor icon from src/assets/icons
    {{img:name|alt|sizes|class|eager}}  responsive <img> for src/assets/img/name-{640,1200}.webp
    {{cta}}                      the shared "Begär offert" button
Usage: python3 tools/build.py
"""
import html
import json
import re
import shutil
from datetime import date
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "docs"
SITE_URL = "https://fionasbakery.se"

NAV = [
    ("brollop", "/brollopstartor/", "Bröllop"),
    ("fest", "/tartor-till-fest/", "Fest & kalas"),
    ("foretag", "/foretag-och-catering/", "Företag"),
    ("priser", "/priser/", "Priser & smaker"),
    ("om", "/om-fiona/", "Om Fiona"),
]

BUSINESS = {
    "@type": "Bakery",
    "@id": SITE_URL + "/#bakery",
    "name": "Fiona's Bakery",
    "description": "Beställningstårtor och bakelser i Malmö: bröllopstårtor med handgjorda sockerblommor, tårtor till barnkalas, dop, babyshower, möhippa och företagsevent.",
    "url": SITE_URL + "/",
    "logo": SITE_URL + "/assets/favicon.svg",
    "image": SITE_URL + "/assets/img/brollop-sockerrosor-1200.webp",
    "telephone": "+46738740378",
    "email": "kontakt@fionasbakery.se",
    "priceRange": "$$",
    "currenciesAccepted": "SEK",
    "paymentAccepted": "Swish",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Trossgatan 25",
        "postalCode": "232 36",
        "addressLocality": "Arlöv",
        "addressRegion": "Skåne län",
        "addressCountry": "SE",
    },
    "areaServed": [{"@type": "City", "name": n} for n in
                   ["Malmö", "Arlöv", "Burlöv", "Lund", "Lomma", "Staffanstorp", "Vellinge"]],
    "sameAs": ["https://www.instagram.com/fionasbakery/"],
}

LOGO_MARK = (
    '<svg class="logo__mark" viewBox="0 0 32 34" aria-hidden="true" focusable="false">'
    '<circle cx="16" cy="3.6" r="2.4" fill="var(--accent)"/>'
    '<path d="M5 32V19a11 11 0 0 1 22 0v13z" fill="currentColor"/>'
    '<path d="M19.6 15.4a3.3 3.3 0 0 0-4.1 3.2V29M12.4 21.2h6.2" fill="none" stroke="var(--bg)" '
    'stroke-width="2.5" stroke-linecap="round"/></svg>'
)


def rel_root(path: str) -> str:
    depth = len([p for p in path.strip("/").split("/") if p])
    return "../" * depth if depth else "./"


def icon(name: str) -> str:
    svg = (SRC / "assets/icons" / f"{name}.svg").read_text()
    svg = re.sub(r"<svg[^>]*>", '<svg class="icon" viewBox="0 0 256 256" aria-hidden="true" focusable="false">', svg, count=1)
    return svg.replace(' fill="currentColor"', "")


_dims = {}


def img(spec: str, root: str) -> str:
    parts = spec.split("|") + [""] * 5
    name, alt, sizes, cls, eager = parts[:5]
    if name not in _dims:
        with Image.open(SRC / "assets/img" / f"{name}-1200.webp") as im:
            _dims[name] = im.size
    w, h = _dims[name]
    base = f"{root}assets/img/{name}"
    attrs = [
        f'src="{base}-1200.webp"',
        f'srcset="{base}-640.webp 640w, {base}-1200.webp 1200w"',
        f'sizes="{sizes or "(max-width: 860px) 100vw, 50vw"}"',
        f'width="{w}" height="{h}"',
        f'alt="{html.escape(alt, quote=True)}"',
        'fetchpriority="high"' if eager == "eager" else 'loading="lazy"',
        'decoding="async"',
    ]
    if cls:
        attrs.insert(0, f'class="{cls}"')
    return "<img " + " ".join(attrs) + ">"


def cta(root: str, small: bool = False) -> str:
    size = " btn--small" if small else ""
    return f'<a class="btn btn--primary{size}" href="{root}bestall/"><span>Begär offert</span>{icon("arrow-right")}</a>'


def render(body: str, root: str) -> str:
    body = body.replace("{{cta}}", cta(root))
    body = re.sub(r"\{\{icon:([\w-]+)\}\}", lambda m: icon(m.group(1)), body)
    body = re.sub(r"\{\{img:([^}]+)\}\}", lambda m: img(m.group(1), root), body)
    return body.replace("{{root}}", root)


def breadcrumbs(meta: dict, root: str) -> tuple[str, dict | None]:
    if meta["path"] == "/" or not meta.get("crumb"):
        return "", None
    visible = (
        f'<nav class="crumbs" aria-label="Brödsmulor"><ol><li><a href="{root}">Hem</a></li>'
        f'<li aria-current="page">{html.escape(meta["crumb"])}</li></ol></nav>'
    )
    data = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Hem", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": meta["crumb"], "item": SITE_URL + meta["path"]},
        ],
    }
    return visible, data


def layout(meta: dict, body: str) -> str:
    root = meta.get("root") or rel_root(meta["path"])
    crumbs_html, crumbs_data = breadcrumbs(meta, root)
    body = body.replace("{{crumbs}}", crumbs_html)
    body = render(body, root)

    graph = [BUSINESS]
    if crumbs_data:
        graph.append(crumbs_data)
    graph.extend(meta.get("schema", []))
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    current = ' aria-current="page"'
    nav_items = "".join(
        f'<a href="{root}{href.lstrip("/")}"{current if meta.get("nav") == key else ""}>{label}</a>'
        for key, href, label in NAV
    )
    canonical = SITE_URL + meta["path"]
    og_image = f'{SITE_URL}/assets/img/{meta.get("image", "brollop-sockerrosor")}-1200.webp'
    title = meta["title"]
    desc = meta["description"]
    robots = '<meta name="robots" content="noindex">' if meta.get("noindex") else ""
    year = date.today().year

    return f"""<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="sv_SE">
<meta property="og:site_name" content="Fiona's Bakery">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#fbf7f0">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{root}assets/fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/hanken-grotesk.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/css/site.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<div id="top"></div>
<a class="skip" href="#innehall">Hoppa till innehållet</a>
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="logo" href="{root}" aria-label="Fiona's Bakery, till startsidan">{LOGO_MARK}<span class="logo__word">Fiona's Bakery</span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="huvudmeny" aria-label="Öppna meny">
      <span class="icon-open">{icon("list")}</span><span class="icon-close">{icon("x")}</span>
    </button>
    <nav class="nav" id="huvudmeny" aria-label="Huvudmeny">
      {nav_items}
      {cta(root, small=True)}
    </nav>
  </div>
</header>
<main id="innehall">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="logo" href="{root}">{LOGO_MARK}<span class="logo__word">Fiona's Bakery</span></a>
        <p class="muted" style="margin-top:1rem;max-width:34ch">Beställningstårtor och bakelser, handgjorda i Arlöv. Leverans i Malmö med omnejd.</p>
      </div>
      <div>
        <h2>Tårtor</h2>
        <ul>
          <li><a href="{root}brollopstartor/">Bröllopstårtor</a></li>
          <li><a href="{root}tartor-till-fest/">Barnkalas, dop & fest</a></li>
          <li><a href="{root}foretag-och-catering/">Företag & catering</a></li>
          <li><a href="{root}priser/">Priser & smaker</a></li>
          <li><a href="{root}om-fiona/">Om Fiona</a></li>
        </ul>
      </div>
      <div class="footer-contact">
        <h2>Kontakt</h2>
        <ul>
          <li><a href="tel:+46738740378">{icon("phone")}073-874 03 78</a></li>
          <li><a href="mailto:kontakt@fionasbakery.se">{icon("envelope-simple")}kontakt@fionasbakery.se</a></li>
          <li><a href="https://www.instagram.com/fionasbakery/" rel="noopener">{icon("instagram-logo")}@fionasbakery</a></li>
          <li><span class="muted">Trossgatan 25, 232 36 Arlöv<br>Hämtning enligt överenskommelse</span></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© {year} Fiona's Bakery. Godkänd för F-skatt.</span>
      <a href="{root}integritet/">Integritetspolicy</a>
    </div>
  </div>
</footer>
<script src="{root}assets/js/site.js" defer></script>
</body>
</html>
"""


def parse(page: Path) -> tuple[dict, str]:
    text = page.read_text()
    m = re.match(r"\s*<!--(.*?)-->\s*", text, re.S)
    if not m:
        raise SystemExit(f"{page}: missing JSON header")
    return json.loads(m.group(1)), text[m.end():]


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC / "assets", OUT / "assets", ignore=shutil.ignore_patterns("icons"))
    urls = []
    for page in sorted((SRC / "pages").glob("*.html")):
        meta, body = parse(page)
        target = OUT / ("404.html" if meta["path"] == "/404" else (meta["path"].strip("/") + "/index.html").lstrip("/"))
        if meta["path"] == "/404":
            meta["path"] = "/"
            meta["root"] = "/"  # absolute: GitHub Pages serves 404.html at any depth
            meta["noindex"] = True
        target.parent.mkdir(parents=True, exist_ok=True)
        html_out = layout(meta, body)
        if "—" in html_out or "–" in html_out:
            raise SystemExit(f"{page.name}: contains an em/en dash")
        target.write_text(html_out)
        if not meta.get("noindex"):
            urls.append((meta["path"], meta.get("priority", "0.7")))
    today = date.today().isoformat()
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE_URL}{p}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n" for p, pr in urls)
        + "</urlset>\n"
    )
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    (OUT / ".nojekyll").write_text("")
    print(f"Built {len(urls)} indexed pages into {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
