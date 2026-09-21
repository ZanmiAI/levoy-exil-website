#!/usr/bin/env python3
"""
Zanmi Studio — Artist Website Template · static site generator.

The single source of truth is site.json. EVERYTHING brand- and
content-related lives there — colors, fonts, logos, site title, contact
details, navigation, homepage section order, artworks, exhibitions,
press, policies — so launching the next artist's site means editing
the config, never this code.

    Build:    python3 build.py
    Preview:  python3 -m http.server 8000 --directory public
    Deploy:   upload the public/ folder to any static host.

See TEMPLATE-README.md for the full template guide.
"""
import json
import os
import re
import shutil
import html
from urllib.parse import quote
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(ROOT, "site.json"), encoding="utf-8"))

ARTIST = CFG["artist"]
SITE = CFG["site"]
THEME = CFG["theme"]
BRANDING = CFG.get("branding", {})
CONTACT = CFG["contact"]
STUDIO = CFG["studio"]
ASSETS = CFG.get("assets", {})
BASE = SITE["base_url"].rstrip("/")
# URL prefix for internal links/assets. The GitHub Pages preview lives under a
# subpath ("/levoy-exil-website"); production serves from the domain root, so
# at cutover set site.json "baseurl" to "" and rebuild.
BP = SITE.get("baseurl", "").rstrip("/")
BUILD_DATE = "2026-09-20"
YEAR = BUILD_DATE.split("-")[0]

# Generated, deployable site lives here (source files stay out of it).
OUT = os.path.join(ROOT, "public")

SRC_DIR = os.path.expanduser(ASSETS.get("source_dir", ""))
PRODUCTS_SRC = os.path.join(SRC_DIR, ASSETS.get("artworks_dir", "products"))
SITE_SRC = os.path.join(SRC_DIR, ASSETS.get("site_dir", "site"))
GALLERY_SRC = os.path.join(SRC_DIR, "old-site-photos", "files")


# ---------------------------------------------------------------- helpers ---
def esc(s):
    return html.escape(str(s), quote=True)


def money(p):
    return f"${p:,}"


def fmt_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November",
              "December"]
    return f"{months[m - 1]} {d}, {y}"


def wa_artwork(title, price):
    text = (f"Hello {ARTIST['name']} Gallery! I'm interested in the original "
            f"painting \u201c{title}\u201d by {ARTIST['name']} ({money(price)}). "
            f"Could you share more details?")
    return f"{CONTACT['whatsapp_base']}&text={quote(text)}"


def mail_artwork(title, price):
    subject = f"Enquiry about \u201c{title}\u201d by {ARTIST['name']}"
    body = (f"Hello,\n\nI'm interested in the original painting \u201c{title}\u201d "
            f"by {ARTIST['name']} ({money(price)}).\n\nCould you please share more details?\n\nThank you.")
    return f"mailto:{CONTACT['email']}?subject={quote(subject)}&body={quote(body)}"


def wa_general():
    text = (f"Hello {ARTIST['name']} Gallery! I'd like to enquire about an "
            f"original painting.")
    return f"{CONTACT['whatsapp_base']}&text={quote(text)}"


def art_alt(a):
    return (f"{a['title']} \u2014 original {a['medium'].lower()} painting by "
            f"{ARTIST['name']}, {a['dimensions']}")


def rel_art_img(a):
    return f"assets/img/artworks/{a['slug']}.jpg"


def rel_art_lifestyle(a):
    return f"assets/img/artworks/{a['slug']}-lifestyle.jpg"


def rel_art_gallery(a, i):
    return f"assets/img/artworks/gallery/{a['slug']}-{i}.jpg"


def rel_art_thumb(a):
    return f"assets/img/artworks/{a['slug']}-thumb.jpg"


def parse_dims(dimensions):
    m = re.search(r"(\d+)\s*x\s*(\d+)", dimensions)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None


def write_out(rel_path, content):
    dest = os.path.join(OUT, rel_path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(content)
    return dest


# ------------------------------------------------------------------ fonts ---
FONT_DEFAULT_WEIGHTS = {
    "headings": [400, 600, 700, 800],
    "body": [400, 500, 700],
    "display": [400],
}


def font_cfg(role):
    """Return (family, weights) for a font role.

    Config accepts either a plain string ("Raleway") or an explicit
    {"family": ..., "weights": [...]} object.
    """
    f = THEME["fonts"][role]
    if isinstance(f, dict):
        return f["family"], f.get("weights") or [400, 700]
    return f, FONT_DEFAULT_WEIGHTS.get(role, [400, 700])


def google_fonts_url():
    parts = []
    for role in ("display", "headings", "body"):
        fam, weights = font_cfg(role)
        fam_q = fam.replace(" ", "+")
        if weights:
            w = ";".join(str(int(x)) for x in weights)
            parts.append(f"family={fam_q}:wght@{w}")
        else:
            parts.append(f"family={fam_q}")
    return "https://fonts.googleapis.com/css2?" + "&".join(parts) + "&display=swap"


# ----------------------------------------------------------------- images ---
def save_jpg(im, dest, max_side, quality=82):
    im = im.convert("RGB")
    if max(im.size) > max_side:
        im.thumbnail((max_side, max_side), Image.LANCZOS)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    im.save(dest, "JPEG", quality=quality, progressive=True, optimize=True)


def process_images():
    print("Processing images...")
    a_max = ASSETS.get("artwork_max_side", 1600)
    a_q = ASSETS.get("artwork_quality", 82)
    t_max = ASSETS.get("thumb_max_side", 600)
    t_q = ASSETS.get("thumb_quality", 76)
    for a in CFG["artworks"]:
        src = os.path.join(PRODUCTS_SRC, a["source_image"])
        if not os.path.exists(src):
            raise SystemExit(f"MISSING artwork source image: {src}")
        im = Image.open(src)
        save_jpg(im, os.path.join(OUT, rel_art_img(a)), a_max, a_q)
        save_jpg(im, os.path.join(OUT, rel_art_thumb(a)), t_max, t_q)
        if a.get("lifestyle_image"):
            lsrc = os.path.join(PRODUCTS_SRC, a["lifestyle_image"])
            if not os.path.exists(lsrc):
                raise SystemExit(f"MISSING artwork lifestyle image: {lsrc}")
            save_jpg(Image.open(lsrc), os.path.join(OUT, rel_art_lifestyle(a)),
                     1200, a_q)
    n_life = sum(1 for a in CFG["artworks"] if a.get("lifestyle_image"))
    print(f"  {len(CFG['artworks'])} artworks x2 sizes + {n_life} lifestyle photos")
    n_gal = 0
    for a in CFG["artworks"]:
        for i, gfile in enumerate(a.get("gallery", [])):
            gsrc = os.path.join(GALLERY_SRC, gfile)
            if not os.path.exists(gsrc):
                raise SystemExit(f"MISSING artwork gallery image: {gsrc}")
            save_jpg(Image.open(gsrc), os.path.join(OUT, rel_art_gallery(a, i)),
                     1200, 80)
            n_gal += 1
    print(f"  {n_gal} old-site gallery photos")
    for job in ASSETS.get("site_images", []):
        src = os.path.join(SITE_SRC, job["src"])
        if not os.path.exists(src):
            raise SystemExit(f"MISSING site source image: {src}")
        save_jpg(Image.open(src), os.path.join(OUT, job["dest"]),
                 job.get("max_side", 1600), job.get("quality", 80))
    print(f"  {len(ASSETS.get('site_images', []))} site images")
    for job in ASSETS.get("copy_files", []):
        src = os.path.join(SITE_SRC, job["src"])
        if not os.path.exists(src):
            raise SystemExit(f"MISSING file to copy: {src}")
        dest = os.path.join(OUT, job["dest"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(src, dest)
    print(f"  {len(ASSETS.get('copy_files', []))} files copied as-is")
    os.makedirs(os.path.join(OUT, "assets/img/press"), exist_ok=True)
    n_press = 0
    seen_logos = set()
    press_logo_items = list(CFG["press"]["items"])
    for g in CFG.get("press_page", {}).get("groups", []):
        press_logo_items.extend(g.get("items", []))
    for item in press_logo_items:
        logo = item.get("logo")
        if not logo or logo in seen_logos:
            continue
        seen_logos.add(logo)
        src = os.path.join(SITE_SRC, os.path.basename(logo))
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(OUT, logo))
            n_press += 1
    print(f"  {n_press} press logos")
    for p in STUDIO.get("products", []):
        if p.get("source"):
            src = os.path.join(SITE_SRC, p["source"])
            if os.path.exists(src):
                save_jpg(Image.open(src), os.path.join(OUT, p["image"]), 900, 80)
    if STUDIO.get("products"):
        print(f"  {len(STUDIO['products'])} studio product images")


def write_theme_css():
    """Brand tokens -> CSS custom properties. All values come from config."""
    c = THEME["colors"]
    fams = {role: font_cfg(role)[0] for role in ("headings", "body", "display")}
    css = (":root {\n"
           f"  --color-primary: {c['primary']};\n"
           f"  --color-primary-deep: {c['primary_deep']};\n"
           f"  --color-sand: {c['sand']};\n"
           f"  --color-sand-light: {c['sand_light']};\n"
           f"  --color-accent: {c['accent']};\n"
           f"  --color-accent-deep: {c['accent_deep']};\n"
           f"  --color-ink: {c['ink']};\n"
           f"  --color-paper: {c['paper']};\n"
           f"  --color-white: {c['white']};\n"
           f"  --font-headings: '{fams['headings']}', sans-serif;\n"
           f"  --font-body: '{fams['body']}', sans-serif;\n"
           f"  --font-display: '{fams['display']}', cursive;\n"
           "}\n")
    write_out("assets/css/theme-vars.css", css)
    print("  theme-vars.css written")


# ------------------------------------------------------- shared chrome ---
def head(title, description, path="/", og_image=None, og_type="website",
         extra=""):
    canonical = BASE + path
    favicon = BRANDING.get("favicon", "")
    og_img = BASE + "/" + (og_image or CFG["hero"]["background"])
    return f"""<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0e3c79">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(ARTIST['name'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(og_img)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{google_fonts_url()}" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/theme-vars.css">
<link rel="stylesheet" href="/assets/css/styles.css">
<script src="/assets/js/main.js" defer></script>
{extra}</head>"""


def site_header(active="/"):
    logo = BRANDING.get("header_logo", "")
    logo_alt = BRANDING.get("header_logo_alt", f"{ARTIST['name']} logo")
    items = []
    for n in CFG["nav"]:
        if n.get("footer_only"):
            continue  # legal pages live in the footer only, not the header
        cur = ' aria-current="page"' if n["url"] == active else ""
        items.append(
            f'<li><a href="{esc(n["url"])}"{cur}>{esc(n["label"])}</a></li>')
    return f"""<header class="site-header">
<div class="wrap header-inner">
<a class="brand" href="/" aria-label="{esc(ARTIST['name'])} — home">
<img src="/{esc(logo)}" alt="{esc(logo_alt)}" width="44" height="44">
<span><span class="brand-name">{esc(ARTIST['name'])}</span><br><span class="brand-sub">{esc(ARTIST['tagline'])}</span></span>
</a>
<button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">\u2630</button>
<nav class="site-nav" id="site-nav" aria-label="Main navigation"><ul>{''.join(items)}</ul></nav>
</div>
</header>"""


def social_links():
    out = []
    for label, key in (("Facebook", "facebook"), ("Instagram", "instagram"),
                       ("YouTube", "youtube")):
        if CONTACT.get(key):
            out.append(f'<a href="{esc(CONTACT[key])}">{label}</a>')
    return "".join(out)


def site_footer():
    nav_items = "".join(
        f'<li><a href="{esc(n["url"])}">{esc(n["label"])}</a></li>'
        for n in CFG["nav"])
    return f"""<footer class="site-footer">
<div class="wrap footer-inner">
<div class="footer-brand">
<a class="footer-logo" href="/" aria-label="{esc(ARTIST['name'])} — home">
<img src="/{esc(BRANDING.get('footer_logo', ''))}" alt="{esc(BRANDING.get('footer_logo_alt', ARTIST['name'] + ' logo'))}" width="220" height="54">
</a>
<p class="brand-sub">{esc(ARTIST['tagline'])}</p>
<p>{esc(SITE['description'])}</p>
</div>
<nav class="footer-nav" aria-label="Footer navigation">
<h3>Explore</h3>
<ul>{nav_items}</ul>
</nav>
<div class="footer-contact">
<h3>Contact</h3>
<p>Email: <a href="mailto:{esc(CONTACT['email'])}">{esc(CONTACT['email'])}</a><br>
WhatsApp: <a href="{esc(wa_general())}">{esc(CONTACT['whatsapp_display'])}</a><br>
{esc(CONTACT['hours'])}</p>
<div class="social-row">{social_links()}</div>
</div>
</div>
<div class="wrap footer-bottom">
<span>\u00a9 {YEAR} {esc(ARTIST['name'])}. All rights reserved.</span>
<a class="studio-link" href="{esc(STUDIO['url'])}">{esc(STUDIO['footer_line'])}</a>
</div>
</footer>"""


def page_html(title, description, body, path="/", active="/", og_image=None,
              og_type="website", extra_head=""):
    html = f"""<!DOCTYPE html>
<html lang="{esc(SITE.get('lang', 'en'))}">
{head(title, description, path, og_image, og_type, extra_head)}
<body>
{site_header(active)}
<main>
{body}
</main>
{site_footer()}
</body>
</html>
"""
    if BP:
        # Prefix root-relative internal links so the site works under a
        # subpath (GitHub Pages preview). Absolute and protocol-relative
        # URLs are left untouched.
        html = re.sub(r'(href|src)="(?=/(?!/))', rf'\1="{BP}', html)
    return html


def write_page(path, *args, **kwargs):
    """Write a page; path like '/' or '/gallery/' becomes index.html."""
    rel = path.lstrip("/") + "index.html"
    write_out(rel, page_html(*args, path=path, **kwargs))
    return rel


# ------------------------------------------------- section renderers ---
def card_html(a):
    avail = a["availability"]
    badge = "Available" if avail == "in" else "Sold"
    return f"""<a class="card" href="/artwork/{a['slug']}/" data-availability="{avail}">
<div class="card-media"><img src="/{rel_art_thumb(a)}" alt="{esc(art_alt(a))}" loading="lazy"></div>
<div class="card-body">
<h3 class="card-title">{esc(a['title'])}</h3>
<p class="card-meta">{esc(a['medium'])} \u00b7 {esc(a['dimensions'])}</p>
<div class="card-foot"><span class="price">{money(a['price'])}</span><span class="badge badge--{avail}">{badge}</span></div>
</div></a>"""


def sec_hero(sec):
    h = CFG["hero"]
    return f"""<section class="hero">
<div class="hero-bg"><img src="/{esc(h['background'])}" alt="{esc(h.get('background_alt', ''))}" style="object-position: {esc(h.get('background_position', 'center'))}" fetchpriority="high"></div>
<div class="wrap hero-inner">
<img class="hero-logo" src="/{esc(BRANDING.get('hero_logo', ''))}" alt="{esc(BRANDING.get('hero_logo_alt', ARTIST['name']))}" width="92" height="92">
<p class="eyebrow">{esc(h['eyebrow'])}</p>
<h1>{esc(h['title'])}</h1>
<p class="tagline">{esc(h['subtitle'])}</p>
<div class="btn-row center">
<a class="btn btn--light" href="/gallery/">{esc(h['cta_gallery'])}</a>
<a class="btn btn--whatsapp" href="{esc(wa_general())}">{esc(h['cta_whatsapp'])}</a>
</div>
</div>
</section>"""


def sec_about(sec):
    a = ARTIST
    paras = "".join(f"<p>{esc(x)}</p>" for x in a["bio"])
    facts = "".join(
        f'<li><span class="k">{k}</span><span class="v">{esc(v)}</span></li>'
        for k, v in (("Born", a.get("born")),
                     ("Birthplace", a.get("birthplace")),
                     ("Movement", a.get("movement")))
        if v)
    return f"""<section class="section" id="about"><div class="wrap">
<div class="about-grid">
<figure class="about-portrait"><img src="/{esc(a['portrait'])}" alt="{esc(a['portrait_alt'])}" loading="lazy"><figcaption>{esc(a['name'])}</figcaption></figure>
<div><p class="eyebrow">The artist</p><h2>{esc(a['bio_heading'])}</h2>{paras}<ul class="fact-list">{facts}</ul></div>
</div>
</div></section>"""


def sec_featured(sec):
    f = CFG["featured"]
    by_slug = {x["slug"]: x for x in CFG["artworks"]}
    missing = [s for s in f["artworks"] if s not in by_slug]
    if missing:
        raise SystemExit(f"featured.artworks references unknown slugs: {missing}")
    cards = "".join(card_html(by_slug[s]) for s in f["artworks"])
    heading = sec.get("heading") or f["heading"]
    sub = sec.get("sub") or f.get("sub", "")
    n = len(CFG["artworks"])
    return f"""<section class="section"><div class="wrap">
<div class="center"><p class="eyebrow">Gallery</p><h2>{esc(heading)}</h2><p class="lead">{esc(sub)}</p></div>
<div class="grid grid--cards">{cards}</div>
<div class="btn-row center"><a class="btn btn--primary" href="/gallery/">View all {n} originals</a></div>
</div></section>"""


def sec_studio_products(sec):
    """Studio prints/merch showcase. Returns '' when the list is empty,
    so the section vanishes entirely for artists without products."""
    prods = STUDIO.get("products", [])
    if not prods:
        return ""
    base = STUDIO.get("shop_base_url", "").rstrip("/")
    cards = []
    for p in prods:
        url = p["url"]
        if not re.match(r"https?://", url):
            url = base + "/" + url.lstrip("/")
        cards.append(f"""<a class="card product-card" href="{esc(url)}">
<div class="card-media"><img src="/{esc(p['image'])}" alt="{esc(p.get('image_alt', p['name']))}" loading="lazy"></div>
<div class="card-body">
<h3 class="card-title">{esc(p['name'])}</h3>
<div class="card-foot"><span class="price">{money(p['price'])}</span><span class="shop-link">Shop at {esc(STUDIO['name'])} \u2192</span></div>
</div></a>""")
    return f"""<section class="section" data-products-showcase><div class="wrap">
<div class="center"><p class="eyebrow">{esc(STUDIO['name'])}</p><h2>{esc(STUDIO['products_heading'])}</h2>
<p class="lead">{esc(STUDIO['products_sub'])}</p>
<p class="products-note">Sold exclusively through the {esc(STUDIO['name'])} shop \u2014 links open the Studio store.</p></div>
<div class="grid grid--cards">{''.join(cards)}</div>
</div></section>"""


def sec_press(sec):
    pr = CFG["press"]
    items = []
    for it in pr["items"]:
        img = (f'<img src="/{esc(it["logo"])}" alt="{esc(it["logo_alt"])}" '
               f'loading="lazy">')
        cap = f"<span>{esc(it['caption'])}</span>"
        if it.get("url"):
            items.append(
                f'<a class="press-item" href="{esc(it["url"])}">{img}{cap}</a>')
        else:
            items.append(f'<div class="press-item">{img}{cap}</div>')
    return f"""<section class="section section--tint"><div class="wrap center">
<p class="eyebrow">Press</p><h2>{esc(pr['heading'])}</h2>
<div class="press-grid">{''.join(items)}</div>
</div></section>"""


def sec_contact(sec):
    c = CFG["contact_section"]
    return f"""<section class="section" id="contact"><div class="wrap">
<div class="contact-card">
<p class="eyebrow">Get in touch</p>
<h2>{esc(c['heading'])}</h2>
<p class="lead">{esc(c['text'])}</p>
<div class="btn-row center">
<a class="btn btn--whatsapp" href="{esc(wa_general())}">WhatsApp {esc(CONTACT['whatsapp_display'])}</a>
<a class="btn btn--light" href="mailto:{esc(CONTACT['email'])}">Email {esc(CONTACT['email'])}</a>
</div>
<ul class="contact-lines"><li>{esc(CONTACT['hours'])}</li></ul>
<div class="social-row">{social_links()}</div>
</div>
</div></section>"""


def sec_custom(sec):
    """Generic one-off section, fully described by config.

    Fields: heading (required), eyebrow, image, image_alt,
    image_position ("left"|"right"), paragraphs (list),
    cta_label + cta_url (optional),
    video_youtube_id + video_title (optional — renders the image as a
    click-to-play thumbnail that swaps in a YouTube embed).
    """
    heading = sec.get("heading") or sec.get("id", "Featured")
    eyebrow = (f'<p class="eyebrow">{esc(sec["eyebrow"])}</p>'
               if sec.get("eyebrow") else "")
    paras = "".join(f"<p>{esc(p)}</p>" for p in sec.get("paragraphs", []))
    cta = ""
    if sec.get("cta_label") and sec.get("cta_url"):
        cta = (f'<div class="btn-row"><a class="btn btn--primary" '
               f'href="{esc(sec["cta_url"])}" target="_blank" rel="noopener">'
               f'{esc(sec["cta_label"])}</a></div>')
    flip = " feature--img-right" if sec.get("image_position") == "right" else ""
    media = ""
    yt = (sec.get("video_youtube_id") or "").strip()
    if yt and sec.get("image"):
        label = sec.get("video_title") or sec.get("heading", "video")
        media = (
            f'<div class="feature-media">'
            f'<button type="button" class="video-facade" data-youtube-id="{esc(yt)}" '
            f'aria-label="Play video: {esc(label)}">'
            f'<img src="/{esc(sec["image"])}" '
            f'alt="{esc(sec.get("image_alt", ""))}" loading="lazy">'
            f'<span class="video-play" aria-hidden="true"></span>'
            f'</button></div>')
    elif sec.get("image"):
        media = (f'<div class="feature-media"><img src="/{esc(sec["image"])}" '
                 f'alt="{esc(sec.get("image_alt", ""))}" loading="lazy"></div>')
    return f"""<section class="section"><div class="wrap">
<div class="feature"><div class="feature-grid{flip}">
{media}
<div class="feature-body">{eyebrow}<h2>{esc(heading)}</h2>{paras}{cta}</div>
</div></div>
</div></section>"""


def sec_faq(sec):
    """FAQ section, driven by the top-level `faq` config block.

    Renders native <details>/<summary> accordions (no JS needed) and pairs
    with the FAQPage JSON-LD emitted on the homepage.
    """
    f = CFG.get("faq", {})
    items = f.get("items", [])
    if not items:
        return ""
    eyebrow = (f'<p class="eyebrow">{esc(f["eyebrow"])}</p>'
               if f.get("eyebrow") else "")
    lis = "".join(
        f'<details class="faq-item"><summary>{esc(i["q"])}</summary>'
        f'<div class="faq-a"><p>{esc(i["a"])}</p></div></details>'
        for i in items)
    return (f'<section class="section" id="faq"><div class="wrap"><div class="faq-wrap">'
            f'{eyebrow}<h2>{esc(f.get("heading", "Frequently Asked Questions"))}</h2>'
            f'<div class="faq-list">{lis}</div></div></div></section>')


def sec_news(sec):
    """News teaser section, driven by the top-level `news` config block."""
    n = CFG.get("news", {})
    articles = n.get("articles", [])
    if not articles:
        return ""
    eyebrow = (f'<p class="eyebrow">{esc(n["eyebrow"])}</p>'
               if n.get("eyebrow") else "")
    cards = "".join(
        f'<a class="news-card" href="/news/{esc(a["slug"])}/">'
        f'<p class="news-date">{esc(fmt_date(a["date"]))}</p>'
        f'<h3>{esc(a["title"])}</h3>'
        f'<p>{esc(a.get("teaser", ""))}</p>'
        f'<span class="news-more">Read more →</span></a>'
        for a in articles)
    return (f'<section class="section"><div class="wrap">'
            f'{eyebrow}<h2>{esc(n.get("heading", "News"))}</h2>'
            + (f'<p class="lead">{esc(n["sub"])}</p>' if n.get("sub") else "")
            + f'<div class="news-grid">{cards}</div>'
            f'<div class="btn-row center"><a class="btn btn--primary" '
            f'href="/news/">All stories</a></div>'
            f'</div></section>')


def sec_html(sec):
    """Raw HTML passthrough for true one-offs. Config is trusted."""
    return sec.get("html", "")


SECTION_RENDERERS = {
    "hero": sec_hero,
    "about": sec_about,
    "featured_artworks": sec_featured,
    "studio_products": sec_studio_products,
    "press": sec_press,
    "contact": sec_contact,
    "custom": sec_custom,
    "faq": sec_faq,
    "news": sec_news,
    "html": sec_html,
}


def render_sections(sections):
    out = []
    for i, sec in enumerate(sections or []):
        stype = sec.get("type")
        renderer = SECTION_RENDERERS.get(stype)
        if renderer is None:
            raise SystemExit(
                f"Unknown homepage section type {stype!r} (section #{i}). "
                f"Valid types: {', '.join(sorted(SECTION_RENDERERS))}. "
                "Use 'custom' or 'html' for one-off sections without touching code."
            )
        out.append(renderer(sec))
    return "\n".join(h for h in out if h)


# ------------------------------------------------------------ pages ---
def org_jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": f"{ARTIST['name']} Gallery",
        "url": BASE + "/",
        "logo": BASE + "/" + BRANDING.get("structured_data_logo", BRANDING.get("header_logo", "")),
        "sameAs": [CONTACT[k] for k in ("facebook", "instagram", "youtube")
                   if CONTACT.get(k)],
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, indent=2, ensure_ascii=False) + "\n</script>")


def person_jsonld():
    """Artist as a schema.org Person — identity signals for SEO/AEO."""
    same = [CONTACT[k] for k in ("facebook", "instagram", "youtube")
            if CONTACT.get(k)]
    same.append("https://art.state.gov/personnel/levoy_exil")
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": ARTIST["name"],
        "birthDate": "1944-10-19",
        "birthPlace": ARTIST["birthplace"],
        "nationality": "Haitian",
        "jobTitle": "Painter",
        "description": SITE["description"],
        "url": BASE + "/",
        "image": BASE + "/" + ARTIST["portrait"],
        "sameAs": same,
        "knowsAbout": ["Saint Soleil", "Haitian art", "Vodou art",
                        "Haitian painting"],
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, indent=2, ensure_ascii=False) + "\n</script>")


def faq_jsonld():
    """FAQPage schema — feeds Google rich results and answer engines."""
    items = CFG.get("faq", {}).get("items", [])
    if not items:
        return ""
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": i["q"],
             "acceptedAnswer": {"@type": "Answer", "text": i["a"]}}
            for i in items
        ],
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, indent=2, ensure_ascii=False) + "\n</script>")


def build_home():
    body = render_sections(CFG["homepage"]["sections"])
    write_page("/", SITE["title"], SITE["description"], body, active="/",
               extra_head=org_jsonld() + person_jsonld() + faq_jsonld())


def build_gallery():
    arts = CFG["artworks"]
    n_all = len(arts)
    n_in = sum(1 for a in arts if a["availability"] == "in")
    n_out = n_all - n_in
    cards = "".join(card_html(a) for a in arts)
    body = f"""<div class="wrap"><section class="section">
<p class="eyebrow">Original paintings</p>
<h1>The Gallery</h1>
<p class="lead">Browse all {n_all} original paintings by {esc(ARTIST['name'])}. Every piece is one of a kind \u2014 enquire directly via WhatsApp or email about any artwork, including sold pieces.</p>
<div class="filters" role="group" aria-label="Filter by availability">
<button class="filter-btn" data-filter="all" aria-pressed="true">All ({n_all})</button>
<button class="filter-btn" data-filter="in" aria-pressed="false">Available ({n_in})</button>
<button class="filter-btn" data-filter="out" aria-pressed="false">Sold ({n_out})</button>
</div>
<p class="gallery-count" aria-live="polite">{n_all} artworks</p>
<div class="grid grid--cards">{cards}</div>
</section></div>"""
    write_page("/gallery/",
               f"Gallery \u2014 {n_all} Original Paintings by {ARTIST['name']}",
               f"Browse all {n_all} original {ARTIST['name']} paintings "
               f"({n_in} available). Filter by availability and enquire "
               f"directly via WhatsApp or email.",
               body, active="/gallery/")


def build_exhibitions():
    exhs = CFG["exhibitions"]
    years = [e["year"] for e in exhs]
    items = []
    for e in exhs:
        title = (f'<span class="exhib-title">{esc(e["title"])}</span> '
                 if e.get("title") else "")
        bits = [b for b in (e.get("venue"), e.get("city"), e.get("country"))
                if b]
        venue = (f'<span class="exhib-venue">{esc(" \u2014 ".join(bits))}</span>'
                 if bits else "")
        sep = "<br>" if title and venue else ""
        items.append(
            f'<li><span class="exhib-year">{e["year"]}</span> '
            f'{title}{sep}{venue}</li>')
    body = f"""<div class="wrap"><section class="section">
<p class="eyebrow">{min(years)} \u2013 {max(years)}</p>
<h1>Exhibitions</h1>
<p class="lead">Five decades of exhibitions across Haiti, the Americas, and Europe \u2014 from the Saint Soleil workshops of the 1970s to the present day.</p>
<ol class="exhib-timeline">{''.join(items)}</ol>
</section></div>"""
    write_page("/exhibitions/",
               f"Exhibition History ({min(years)}\u2013{max(years)}) \u2014 {ARTIST['name']}",
               f"Exhibition history of {ARTIST['name']}, {min(years)} to "
               f"{max(years)}: {len(exhs)} shows in Haiti, the US, Canada, "
               f"Europe, and beyond.",
               body, active="/exhibitions/")


def article_jsonld(a, path):
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": a["title"],
        "description": a.get("teaser", ""),
        "datePublished": a["date"],
        "author": {"@type": "Person", "name": ARTIST["name"]},
        "publisher": {"@type": "Organization",
                      "name": f"{ARTIST['name']} Gallery"},
        "url": BASE + path,
        "mainEntityOfPage": BASE + path,
    }
    if a.get("image"):
        data["image"] = BASE + "/" + a["image"]["src"].lstrip("/")
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, indent=2, ensure_ascii=False) + "\n</script>")


def build_news_index():
    n = CFG.get("news", {})
    articles = n.get("articles", [])
    cards = "".join(
        f'<a class="news-card" href="/news/{esc(a["slug"])}/">'
        f'<p class="news-date">{esc(fmt_date(a["date"]))}</p>'
        f'<h3>{esc(a["title"])}</h3>'
        f'<p>{esc(a.get("teaser", ""))}</p>'
        f'<span class="news-more">Read more →</span></a>'
        for a in articles)
    body = (f'<div class="wrap"><section class="section">'
            f'<p class="eyebrow">{esc(n.get("eyebrow", "Stories"))}</p>'
            f'<h1>{esc(n.get("heading", "News"))}</h1>'
            + (f'<p class="lead">{esc(n["sub"])}</p>' if n.get("sub") else "")
            + f'<div class="news-grid">{cards}</div>'
            f'</section></div>')
    write_page("/news/", f"News — {ARTIST['name']}",
               f"News and stories from the life and work of {ARTIST['name']}.",
               body, active="/news/")


def _press_initials(publication):
    """Monogram fallback for press cards without a logo tile, e.g. 'GA'."""
    words = [w for w in publication.replace("&", " ").split()
             if w[0].isalnum()]
    return "".join(w[0] for w in words[:2]).upper()


def _press_card(it):
    pub = it["publication"]
    if it.get("logo"):
        logo = (f'<span class="press-logo">'
                f'<img src="/{esc(it["logo"])}" alt="{esc(pub)} logo" '
                f'loading="lazy"></span>')
    else:
        logo = (f'<span class="press-logo press-logo--mono" aria-hidden="true">'
                f'{esc(_press_initials(pub))}</span>')
    inner = (f'{logo}<span class="press-body">'
             f'<p class="press-pub">{esc(pub)}</p>'
             f'<h3>{esc(it["title"])}</h3>'
             + (f'<p>{esc(it["blurb"])}</p>' if it.get("blurb") else "")
             + (f'<span class="news-more">Read the article &#8599;</span>'
                if it.get("url") else "")
             + '</span>')
    if it.get("url"):
        return (f'<a class="press-card" href="{esc(it["url"])}" '
                f'target="_blank" rel="noopener">{inner}</a>')
    return f'<div class="press-card">{inner}</div>'


def _press_feature(it, pp):
    pub = it["publication"]
    logo = (f'<img src="/{esc(it["logo"])}" alt="{esc(pub)} logo">'
            if it.get("logo") else "")
    return (
        f'<a class="press-feature" href="{esc(it["url"])}" '
        f'target="_blank" rel="noopener">'
        f'<span class="press-feature-media">'
        f'<img src="/{esc(pp["feature_image"])}" '
        f'alt="{esc(pp.get("feature_image_alt", ""))}"></span>'
        f'<span class="press-feature-body">'
        f'<p class="press-pub">Featured story</p>'
        f'<h3>{esc(it["title"])}</h3>'
        + (f'<p>{esc(it["blurb"])}</p>' if it.get("blurb") else "")
        + (f'<span class="press-feature-logo">{logo}</span>' if logo else "")
        + f'<span class="news-more">Read the article &#8599;</span>'
        f'</span></a>')


def build_press_page():
    pp = CFG.get("press_page", {})
    sections = []
    for g in pp.get("groups", []):
        items = [it for it in g.get("items", []) if not it.get("featured")]
        feat = next((it for it in g.get("items", []) if it.get("featured")
                     and it.get("url")), None)
        cards = "".join(_press_card(it) for it in items)
        head = (
            f'<div class="press-group-head"><h2>{esc(g["heading"])}</h2>'
            f'<span class="press-count">{len(g.get("items", []))} '
            f'{"article" if len(g.get("items", [])) == 1 else "articles"}</span></div>'
            + (f'<p class="lead">{esc(g["sub"])}</p>' if g.get("sub") else ""))
        body = head
        if feat and pp.get("feature_image"):
            body += _press_feature(feat, pp)
        body += f'<div class="press-list">{cards}</div>'
        tone = " section--tint" if g.get("tone") == "tint" else ""
        sections.append(
            f'<section class="section{tone}"><div class="wrap">{body}</div>'
            f'</section>')
    hero = (
        f'<section class="press-hero"><div class="wrap">'
        f'<p class="eyebrow">{esc(pp.get("eyebrow", "Press"))}</p>'
        f'<h1>{esc(pp.get("heading", "Press"))}</h1>'
        + (f'<p class="lead">{esc(pp["sub"])}</p>' if pp.get("sub") else "")
        + f'</div></section>')
    write_page("/press/", f"Press — {ARTIST['name']}",
               f"Press coverage and recognition for {ARTIST['name']}: "
               f"Vogue, WWD, The New York Times, CNN, and more.",
               hero + "".join(sections), active="/press/")


def news_figure(img):
    """Render a <figure> for a news article image block."""
    inner = (f'<img src="/{esc(img["src"])}" alt="{esc(img.get("alt", ""))}"'
             f' loading="lazy">')
    if img.get("link"):
        inner = f'<a href="{esc(img["link"])}">{inner}</a>'
    caption = (f'<figcaption>{esc(img["caption"])}</figcaption>'
               if img.get("caption") else "")
    return f'<figure class="article-figure">{inner}{caption}</figure>'


def news_block(b):
    """Render one news article body block: paragraph string, {"h2": ...},
    {"img": ...}, or {"video": ...} (click-to-play YouTube facade)."""
    if isinstance(b, dict):
        if "h2" in b:
            return f'<h2>{esc(b["h2"])}</h2>'
        if "img" in b:
            return news_figure(b["img"])
        if "video" in b:
            v = b["video"]
            label = v.get("title") or "video"
            return (
                f'<button type="button" class="video-facade article-video" '
                f'data-youtube-id="{esc(v["youtube_id"])}" '
                f'aria-label="Play video: {esc(label)}">'
                f'<img src="/{esc(v["poster"])}" '
                f'alt="{esc(v.get("poster_alt", ""))}" loading="lazy">'
                f'<span class="video-play" aria-hidden="true"></span>'
                f'</button>')
        if "gallery" in b:
            g = b["gallery"]
            figs = "".join(
                f'<figure><img src="/{esc(i["src"])}" '
                f'alt="{esc(i.get("alt", ""))}" loading="lazy">'
                + (f'<figcaption>{esc(i["caption"])}</figcaption>'
                   if i.get("caption") else "")
                + '</figure>'
                for i in g.get("images", []))
            credit = (f'<p class="gallery-credit">{esc(g["credit"])}</p>'
                      if g.get("credit") else "")
            return f'<div class="article-gallery">{figs}</div>{credit}'
        return ""
    return f"<p>{esc(b)}</p>"


def build_article(a):
    path = f"/news/{a['slug']}/"
    paras = "".join(news_block(b) for b in a.get("body", []))
    if not paras:
        paras = ("<p><em>Full story coming soon — check back shortly.</em></p>")
    hero = news_figure(a["image"]) if a.get("image") else ""
    body = (f'<div class="wrap"><section class="section prose">'
            f'<p class="eyebrow">{esc(fmt_date(a["date"]))}</p>'
            f'<h1>{esc(a["title"])}</h1>'
            + (f'<p class="lead">{esc(a["teaser"])}</p>'
               if a.get("teaser") else "")
            + hero
            + paras
            + f'<p><a href="/news/">← All stories</a></p>'
            f'</section></div>')
    write_page(path, f"{a['title']} — {ARTIST['name']}",
               a.get("teaser") or f"{a['title']} — {ARTIST['name']}",
               body, active="/news/",
               extra_head=article_jsonld(a, path))


def build_prose(page_key, path, active):
    p = CFG["pages"][page_key]
    secs = "".join(
        f"<h2>{esc(s['heading'])}</h2>"
        + "".join(f"<p>{esc(x)}</p>" for x in s["body"])
        for s in p["sections"])
    body = (f'<div class="wrap"><section class="section prose">'
            f'<p class="eyebrow">{esc(ARTIST["name"])}</p>'
            f'<h1>{esc(p["title"])}</h1>'
            f'<p class="lead">{esc(p["intro"])}</p>{secs}'
            f"</section></div>")
    write_page(path, f"{p['title']} \u2014 {ARTIST['name']}",
               p["description"], body, active=active)


def artwork_jsonld(a, path):
    w, h = parse_dims(a["dimensions"])
    avail = ("https://schema.org/InStock"
             if a["availability"] == "in"
             else "https://schema.org/OutOfStock")
    data = {
        "@context": "https://schema.org",
        "@type": "VisualArtwork",
        "name": a["title"],
        "creator": {"@type": "Person", "name": ARTIST["name"]},
        "artMedium": a["medium"],
        "image": BASE + "/" + rel_art_img(a),
        "url": BASE + path,
        "offers": {
            "@type": "Offer",
            "price": a["price"],
            "priceCurrency": "USD",
            "availability": avail,
        },
    }
    if w and h:
        data["width"] = {"@type": "QuantitativeValue", "value": w,
                         "unitText": "inches"}
        data["height"] = {"@type": "QuantitativeValue", "value": h,
                          "unitText": "inches"}
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, indent=2, ensure_ascii=False) + "\n</script>")


def build_artwork(a, prev_a, next_a):
    path = f"/artwork/{a['slug']}/"
    avail = a["availability"]
    badge = "Available" if avail == "in" else "Sold"
    nav = []
    if prev_a:
        nav.append(f'<a class="btn btn--outline" href="/artwork/{prev_a["slug"]}/">\u2190 {esc(prev_a["title"])}</a>')
    if next_a:
        nav.append(f'<a class="btn btn--outline" href="/artwork/{next_a["slug"]}/">{esc(next_a["title"])} \u2192</a>')
    lifestyle = ""
    if a.get("lifestyle_image"):
        lifestyle = (f'<figure class="artwork-lifestyle">'
                     f'<img src="/{rel_art_lifestyle(a)}" loading="lazy" '
                     f'alt="{esc(a["title"])} by {esc(ARTIST["name"])}, shown framed in a home setting">'
                     f'<figcaption>In your home — a framed display of <em>{esc(a["title"])}</em></figcaption>'
                     f'</figure>')
    gallery = ""
    if a.get("gallery"):
        figs = []
        for i, _gfile in enumerate(a["gallery"]):
            if i == 0:
                alt = (f'{a["title"]} \u2014 photograph of the original '
                       f'{a["medium"].lower()} painting by {ARTIST["name"]}')
                cap = "Photograph of the original canvas"
            else:
                alt = (f'{a["title"]} by {ARTIST["name"]}, '
                       f'shown framed in a home interior')
                cap = "Styled in a home interior"
            figs.append(
                f'<figure><img src="/{rel_art_gallery(a, i)}" loading="lazy" '
                f'alt="{esc(alt)}"><figcaption>{cap}</figcaption></figure>')
        gallery = (
            f'<section class="artwork-gallery" aria-label="More photos">'
            f'<h2>More photos of <em>{esc(a["title"])}</em></h2>'
            f'<p class="gallery-sub">See how this painting could look on your '
            f'walls \u2014 photographs from the gallery.</p>'
            f'<div class="artwork-gallery-grid">{"".join(figs)}</div>'
            f'</section>')
    body = f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/gallery/">Gallery</a> \u00b7 {esc(a['title'])}</nav>
<section class="section"><div class="artwork-layout">
<div class="artwork-media"><img src="/{rel_art_img(a)}" alt="{esc(art_alt(a))}" fetchpriority="high">{lifestyle}</div>
<div class="artwork-info">
<p class="eyebrow">Original painting</p>
<h1>{esc(a['title'])}</h1>
<p class="lead">by {esc(ARTIST['name'])}</p>
<p class="price" style="font-size:1.6rem">{money(a['price'])}</p>
<div class="artwork-status"><span class="badge badge--{avail}">{badge}</span></div>
<table class="spec-table">
<tr><th>Medium</th><td>{esc(a['medium'])}</td></tr>
<tr><th>Dimensions</th><td>{esc(a['dimensions'])}</td></tr>
<tr><th>Artist</th><td>{esc(ARTIST['name'])}</td></tr>
<tr><th>Availability</th><td>{badge}</td></tr>
</table>
<div class="enquiry-box">
<h2>Enquire about this painting</h2>
<p>Every sale is arranged personally \u2014 message the gallery and we\u2019ll confirm availability, shipping, and payment.</p>
<div class="btn-row">
<a class="btn btn--whatsapp" href="{esc(wa_artwork(a['title'], a['price']))}">WhatsApp {esc(CONTACT['whatsapp_display'])}</a>
<a class="btn btn--outline" href="{esc(mail_artwork(a['title'], a['price']))}">Email the gallery</a>
</div>
</div>
</div>
</div>
{gallery}
<div class="artwork-nav">{''.join(nav)}</div>
</section></div>"""
    desc = (f"{a['title']}: an original {a['medium'].lower()} painting "
            f"({a['dimensions']}) by {ARTIST['name']}, {money(a['price'])}. "
            f"Enquire directly via WhatsApp or email.")
    write_page(path, f"{a['title']} \u2014 Original Painting by {ARTIST['name']}",
               desc, body, active="/gallery/", og_image=rel_art_img(a),
               extra_head=artwork_jsonld(a, path))


def build_404():
    body = """<div class="wrap"><section class="section notfound">
<h1>404</h1>
<p class="lead">This page doesn\u2019t exist \u2014 but the paintings do.</p>
<div class="btn-row center">
<a class="btn btn--primary" href="/">Back to home</a>
<a class="btn btn--outline" href="/gallery/">View the gallery</a>
</div>
</section></div>"""
    write_out("404.html", page_html(
        f"Page not found \u2014 {ARTIST['name']}",
        f"The page you\u2019re looking for doesn\u2019t exist on {ARTIST['name']}\u2019s website.",
        body, path="/404.html"))


def build_pages():
    print("Building pages...")
    build_home()
    build_gallery()
    build_exhibitions()
    build_news_index()
    for a in CFG.get("news", {}).get("articles", []):
        build_article(a)
    build_press_page()
    build_prose("privacy", "/privacy/", "/privacy/")
    build_prose("delivery", "/delivery-returns/", "/delivery-returns/")
    arts = CFG["artworks"]
    for i, a in enumerate(arts):
        prev_a = arts[i - 1] if i > 0 else None
        next_a = arts[i + 1] if i < len(arts) - 1 else None
        build_artwork(a, prev_a, next_a)
    build_404()
    print(f"  home + gallery + exhibitions + 2 policy pages + "
          f"{len(arts)} artworks + 404")


# ------------------------------------------------------ sitemap/robots ---
def write_sitemap():
    urls = ["/", "/gallery/", "/exhibitions/", "/news/", "/press/", "/privacy/",
            "/delivery-returns/"]
    urls += [f"/artwork/{a['slug']}/" for a in CFG["artworks"]]
    urls += [f"/news/{a['slug']}/"
             for a in CFG.get("news", {}).get("articles", [])]
    items = "\n".join(
        f"  <url><loc>{BASE}{u}</loc><lastmod>{BUILD_DATE}</lastmod></url>"
        for u in urls)
    write_out("sitemap.xml",
              '<?xml version="1.0" encoding="UTF-8"?>\n'
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
              f"{items}\n</urlset>\n")
    print(f"  sitemap.xml ({len(urls)} urls)")


def write_robots():
    write_out("robots.txt",
              f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    print("  robots.txt")


def write_llms_txt():
    """llms.txt — a plain-language brief of the site for AI crawlers (AEO)."""
    n = len(CFG["artworks"])
    n_in = sum(1 for a in CFG["artworks"] if a["availability"] == "in")
    lines = [
        f"# {ARTIST['name']}",
        "",
        f"> {SITE['description']}",
        "",
        "## Key facts",
        f"- Born {ARTIST['born']} in {ARTIST['birthplace']}.",
        "- Renowned Haitian painter; pivotal figure of the Saint Soleil "
        "art movement since 1973.",
        "- Paints Haitian spirituality in pointillism: Vodou spirits (loas), "
        "suns, dreams, and sacred geometry.",
        "- In 2023 his “Solrou: The Sun’s creates Unity” inspired Gabriela "
        "Hearst’s Spring Summer 2024 collection (New York Fashion Week).",
        f"- {len(CFG['exhibitions'])} exhibitions listed, 1972–2023.",
        "",
        "## The collection",
        f"- {n} original acrylic paintings on this site ({n_in} available, "
        "sold works remain visible).",
        "- Gallery (all works): " + BASE + "/gallery/",
        "- Exhibition history: " + BASE + "/exhibitions/",
        "- Frequently asked questions: " + BASE + "/#faq",
        "",
        "## Buying an original",
        "- There is no online checkout. Every piece is a one-of-a-kind "
        "original sold through direct enquiry.",
        f"- WhatsApp: {CONTACT['whatsapp_display']} "
        f"({CONTACT['whatsapp_base']})",
        f"- Email: {CONTACT['email']}",
        f"- Hours: {CONTACT['hours']}.",
        "",
        "## Official links",
        f"- Website: {BASE}/",
        f"- Instagram: {CONTACT['instagram']}",
        f"- Facebook: {CONTACT['facebook']}",
        f"- YouTube: {CONTACT['youtube']}",
        "- U.S. Department of State — Art in Embassies: "
        "https://art.state.gov/personnel/levoy_exil",
        "",
    ]
    write_out("llms.txt", "\n".join(lines))
    print("  llms.txt")


# ----------------------------------------------------------- validate ---
def validate():
    failures = []

    def check(name, cond, detail=""):
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}"
              + (f" \u2014 {detail}" if detail and not cond else ""))
        if not cond:
            failures.append(name)

    html_pages = {}
    for dirpath, _, filenames in os.walk(OUT):
        for fn in filenames:
            if fn.endswith(".html"):
                full = os.path.join(dirpath, fn)
                html_pages[os.path.relpath(full, OUT)] = open(
                    full, encoding="utf-8").read()
    combined = "\n".join(html_pages.values())

    art_pages = {k: v for k, v in html_pages.items()
                 if k.startswith("artwork/")}
    check("42 artwork pages generated", len(art_pages) == 42,
          f"found {len(art_pages)}")

    gal = html_pages.get(os.path.join("gallery", "index.html"), "")
    n_cards = gal.count('class="card"')
    check("42 cards on gallery page", n_cards == 42, f"found {n_cards}")

    exh = html_pages.get(os.path.join("exhibitions", "index.html"), "")
    n_exh = exh.count('class="exhib-year"')
    check("49 exhibitions listed", n_exh == 49, f"found {n_exh}")

    check("no contact@levoyexil.com anywhere",
          "contact@levoyexil.com" not in combined)

    text_no_neg = re.sub(
        r"(there is )?no (shopping |online )?carts?,?( and|,)? no checkout|"
        r"(there is )?no (shopping |online )?(cart|checkout)",
        "", combined, flags=re.IGNORECASE)
    m = re.search(
        r"\b(checkout|carts?)\b|add to cart|your cart|place order|"
        r"order now|payment gateway|stripe|paypal", text_no_neg,
        re.IGNORECASE)
    check("no cart/checkout wording", m is None,
          f"found {m.group(0)!r}" if m else "")

    bp_pat = re.escape(BP) if BP else ""
    refs = set(re.findall(r'''(?:src|href)="''' + bp_pat + r'''/(assets/[^"]+)"''',
                          combined))
    missing = sorted(r for r in refs
                     if not os.path.exists(os.path.join(OUT, r)))
    check("every referenced asset exists", not missing,
          f"missing: {missing[:6]}")
    if BP:
        bare = [m.group(1) for m in re.finditer(r'''(?:src|href)="(/[^"]*)"''',
                                                combined)
                if not m.group(1).startswith(BP + "/")]
        check("no bare root-relative URLs under subpath deploy", not bare,
              f"found {len(bare)} (assets would 404 on the preview): "
              f"{bare[:3]}")

    imgs = re.findall(r"<img\b[^>]*>", combined)
    bad = [t[:70] for t in imgs if "alt=" not in t]
    check("every image has an alt attribute", not bad,
          f"{len(bad)} without alt, e.g. {bad[:2]}")

    wa_base = CONTACT["whatsapp_base"]
    email = CONTACT["email"]
    bad_enq = []
    for a in CFG["artworks"]:
        key = os.path.join("artwork", a["slug"], "index.html")
        pg = html_pages.get(key, "")
        if wa_base not in pg or quote(a["title"]) not in pg:
            bad_enq.append(a["slug"] + ":whatsapp")
        subj = quote(f"Enquiry about \u201c{a['title']}\u201d")
        if f"mailto:{email}?subject=" not in pg or subj not in pg:
            bad_enq.append(a["slug"] + ":email")
    check("WhatsApp + email enquiry links name the artwork (all 42)",
          not bad_enq, f"bad: {bad_enq[:6]}")

    sold_pages = [v for v in art_pages.values() if "badge--out" in v]
    sold_ok = (len(sold_pages) == 21
               and all(wa_base in v and f"mailto:{email}" in v
                       for v in sold_pages))
    check("21 sold works visible and enquirable", sold_ok,
          f"found {len(sold_pages)} sold pages")

    check("studio products section absent (list empty)",
          "data-products-showcase" not in combined)

    bad_footer = [k for k, v in html_pages.items()
                  if STUDIO["url"] not in v or STUDIO["footer_line"] not in v]
    check("Zanmi Studio footer link on every page", not bad_footer,
          f"missing on: {bad_footer[:4]}")

    seen_titles, dup = {}, []
    for k, v in html_pages.items():
        mt = re.search(r"<title>(.*?)</title>", v, re.S)
        md = re.search(r'<meta name="description" content="(.*?)"', v, re.S)
        t = html.unescape(mt.group(1)).strip() if mt else ""
        d = html.unescape(md.group(1)).strip() if md else ""
        if not t or not d:
            dup.append(k + ":missing-meta")
        elif t in seen_titles:
            dup.append(k + ":dup-title")
        else:
            seen_titles[t] = k
    check("unique title + description on every page", not dup,
          f"{dup[:6]}")

    bad_ld = [k for k, v in art_pages.items()
              if '"@type": "VisualArtwork"' not in v]
    check("VisualArtwork JSON-LD on every artwork page", not bad_ld,
          f"{bad_ld[:4]}")

    sm_path = os.path.join(OUT, "sitemap.xml")
    n_expected = (7 + len(CFG["artworks"])
                  + len(CFG.get("news", {}).get("articles", [])))
    sm_ok = (os.path.exists(sm_path)
             and open(sm_path, encoding="utf-8").read().count("<loc>")
             == n_expected)
    check("sitemap.xml lists every page", sm_ok)
    check("robots.txt present",
          os.path.exists(os.path.join(OUT, "robots.txt")))
    check("llms.txt present",
          os.path.exists(os.path.join(OUT, "llms.txt")))

    home = html_pages.get("index.html", "")
    n_faq = len(CFG.get("faq", {}).get("items", []))
    check("FAQ section rendered on homepage",
          home.count('class="faq-item"') == n_faq and n_faq > 0,
          f"found {home.count('class=\"faq-item\"')} items")
    check("FAQPage JSON-LD on homepage", '"@type": "FAQPage"' in home)
    check("Person JSON-LD on homepage", '"@type": "Person"' in home
          and '"birthDate": "1944-10-19"' in home)

    news_pages = {k: v for k, v in html_pages.items()
                  if k.startswith("news/") and k != os.path.join("news", "index.html")}
    n_articles = len(CFG.get("news", {}).get("articles", []))
    check("news article pages generated", len(news_pages) == n_articles,
          f"found {len(news_pages)}")
    check("Article JSON-LD on every news page",
          all('"@type": "Article"' in v for v in news_pages.values()))
    check("news index page exists",
          os.path.join("news", "index.html") in html_pages)
    check("press page exists",
          os.path.join("press", "index.html") in html_pages)
    press_page = html_pages.get(os.path.join("press", "index.html"), "")
    check("press page lists Vogue and WWD",
          "Vogue" in press_page and "WWD" in press_page)

    print()
    if failures:
        raise SystemExit(
            f"VALIDATION FAILED ({len(failures)}): {', '.join(failures)}")
    print("All validation checks passed.")


# ---------------------------------------------------------------- main ---
def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)
    process_images()
    for rel in ("assets/css/styles.css", "assets/js/main.js"):
        dest = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(os.path.join(ROOT, rel), dest)
    print("  styles.css + main.js copied")
    write_theme_css()
    build_pages()
    write_sitemap()
    write_robots()
    write_llms_txt()
    print("\nValidating...")
    validate()
    print(f"\nDone. Deploy the '{os.path.basename(OUT)}/' folder as-is.")
    print(f"Preview locally: cd {ROOT} && "
          f"python3 -m http.server 8000 --directory public")


if __name__ == "__main__":
    main()
