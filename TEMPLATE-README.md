# Zanmi Studio — Artist Website Template

This folder is the **shared engine** behind every Zanmi Studio artist website.
Levoy Exil's site is the first one built on it; the next artist's site starts
as a copy of this folder with a different `site.json`.

## Template philosophy

**Shared engine, unique-feeling websites.** Every artist site runs the same
generator (`build.py`) and the same stylesheet, but no two sites should *feel*
templated:

1. **All branding is configuration.** Colors, fonts, logo files, and the site
   title live in `site.json`. Launching another artist must never require
   branding code changes — a new palette and typeface in config produces a
   visibly different site.
2. **Sections are modular and optional.** The homepage is an ordered list of
   sections in config. Levoy's Gabriela Hearst collaboration is a Levoy-only
   `custom` section; another artist simply omits it (or adds their own
   one-off sections) without touching shared code.
3. **Data-driven everything.** Artist name, bio, contact details, social links,
   artwork catalogue, exhibitions, press, and Studio products all live in
   `site.json`.

## Design system rule (decided 2026-09-20)

**Warm beige backgrounds are the constant; the accent color is the artist's.**

- The page background (`theme.colors.paper`, `#fbf7ef`) and tinted sections
  (`theme.colors.sand_light`, `#f6ead3`) stay beige on **every** artist site.
  This warm beige is the Zanmi Studio signature — visitors should feel the
  family resemblance across artists.
- Each artist chooses **one** accent color of their own to replace the deep
  blue (`theme.colors.primary`, currently `#0e3c79` for Levoy). Set it — and
  its darker hover shade (`primary_deep`) — in `site.json`; the header,
  buttons, links, and highlights follow automatically.
- Keep `accent`/`accent_deep` (terracotta) and `ink` as supporting tones
  unless the artist's palette demands otherwise.

## Launching a new artist site

```bash
# 1. Copy the whole folder
cp -r levoy-exil-website new-artist-website
cd new-artist-website

# 2. Replace the content config
#    Edit site.json (details below). Keep the same keys; change the values.

# 3. Point assets at the new artist's source images
#    Edit the "assets" block in site.json (source_dir, site_images, copy_files).

# 4. Build, validate, preview
python3 build.py
python3 -m http.server 8000 --directory public
```

`python3 build.py` wipes and regenerates `public/` from scratch, then runs
16 automated validation checks (page counts, enquiry links, alt text,
forbidden email, no cart/checkout, asset existence, unique metadata,
JSON-LD, sitemap coverage…). **If any check fails, the build exits non-zero —
fix the config, don't ship.**

Deploy by uploading the `public/` folder to any static host (GitHub Pages,
Netlify, Cloudflare Pages, plain nginx…). Never edit files inside `public/`
by hand; it's regenerated on every build.

## `site.json` reference

### `site` — identity & SEO

| Key | Meaning |
|---|---|
| `title` | Homepage `<title>` and default share title |
| `description` | Homepage meta description |
| `base_url` | Canonical production URL, e.g. `https://newartist.com` |
| `lang` | HTML lang attribute |

### `theme` — branding (this is what makes each site feel unique)

```json
"theme": {
  "colors": {
    "primary": "#0e3c79", "primary_deep": "#0a2c5c",
    "sand": "#e7ca9e",    "sand_light": "#f6ead3",
    "accent": "#b47b59",  "accent_deep": "#96593f",
    "ink": "#211c15", "paper": "#fbf7ef", "white": "#ffffff"
  },
  "fonts": {
    "headings": {"family": "Raleway", "weights": [400, 600, 700, 800]},
    "body":     {"family": "Roboto",   "weights": [400, 500, 700]},
    "display":  {"family": "Barriecito", "weights": [400]}
  }
}
```

- The nine color roles are semantic: `primary` (headers, buttons, feature
  backgrounds), `sand` (warm highlight surfaces), `accent` (prices, badges,
  links), `ink`/`paper`/`white` (text and page surfaces), plus `_deep`
  variants. The stylesheet only ever references these roles — there are no
  hardcoded brand hues anywhere.
- Fonts accept a plain string (`"Raleway"`, sensible default weights apply)
  or an explicit `{"family", "weights"}` object. Families are loaded from
  Google Fonts automatically.

`build.py` turns this block into `public/assets/css/theme-vars.css`. Changing
the palette + typefaces is the single biggest lever for making the next site
feel like its own website.

### `branding` — logo files

```json
"branding": {
  "header_logo": "assets/img/site/logo.png",
  "header_logo_alt": "Artist Name logo",
  "hero_logo": "assets/img/site/logo.png",
  "hero_logo_alt": "Artist Name logo",
  "favicon": "assets/img/site/favicon-32x32.png"
}
```

Paths are relative to `public/` and must exist after the asset pipeline runs
(see `assets.copy_files` / `assets.site_images` below). `header_logo` renders
at 44px in the nav, `hero_logo` at 92px in the hero.

### `contact` — details, socials, enquiry endpoints

```json
"contact": {
  "email": "artist@example.com",
  "whatsapp_base": "https://api.whatsapp.com/send?phone=50934249786",
  "whatsapp_display": "+509 3424-9786",
  "facebook": "https://www.facebook.com/...",
  "instagram": "https://www.instagram.com/...",
  "youtube": "https://www.youtube.com/...",
  "hours": "Monday\u2013Saturday, 8 AM\u20138 PM EST"
}
```

Social links with empty/missing URLs are simply not rendered. The WhatsApp
and email enquiry buttons on every artwork page prefill the painting's title
automatically — never hardcode artwork names into these URLs.

### `nav` — site navigation

```json
"nav": [
  {"label": "Home", "url": "/"},
  {"label": "Gallery", "url": "/gallery/"},
  {"label": "Exhibitions", "url": "/exhibitions/"},
  {"label": "Privacy", "url": "/privacy/"},
  {"label": "Delivery & Returns", "url": "/delivery-returns/"}
]
```

Used for the header, the mobile menu, and the footer. `url`s should be clean
paths ending in `/`.

### `hero` / `artist` — homepage intro content

- `hero`: `background` (path in `public/`), `eyebrow`, `title`, `subtitle`,
  CTA labels. The hero logo comes from `branding.hero_logo`.
- `artist`: `name`, `tagline`, `portrait` + `portrait_alt`, `bio_heading`,
  `bio` (list of paragraphs), `born`, `birthplace`, `movement`, `bio_years`.

### `homepage.sections` — the modular page builder

The homepage is exactly the ordered list in `homepage.sections`. Reorder,
add, or delete entries — no code changes.

```json
"homepage": {
  "sections": [
    {"type": "hero"},
    {"type": "about"},
    {"type": "featured_artworks"},
    {"type": "press"},
    {"type": "custom",
     "id": "gabriela-hearst",
     "eyebrow": "Fashion collaboration",
     "heading": "Gabriela Hearst \u00d7 Levoy Exil",
     "image": "assets/img/site/hearst.jpg",
     "image_alt": "...",
     "image_position": "left",
     "paragraphs": ["..."]},
    {"type": "studio_products"},
    {"type": "contact"}
  ]
}
```

Section types:

| Type | Renders |
|---|---|
| `hero` | Full-bleed hero from the `hero` block |
| `about` | Artist portrait + bio + fact list |
| `featured_artworks` | Cards for `featured.artworks` slugs + "view all" link |
| `press` | "As Seen On" logo grid from `press` |
| `studio_products` | Studio prints/merch showcase — **auto-hidden when `studio.products` is empty** |
| `contact` | Enquiry card from `contact_section` |
| `custom` | Generic one-off feature block (see fields above). `image_position`: `"left"` or `"right"`. Optional `cta_label` + `cta_url`. This is how Levoy's Gabriela Hearst section exists without any Levoy-specific code — copy the pattern for any artist-specific story. |
| `html` | Raw HTML passthrough (`{"type": "html", "html": "..."}`) for true one-offs. Config is trusted; keep it clean. |

Unknown `type` values fail the build with a message listing the valid types.

### `artworks` — the catalogue

```json
{
  "slug": "soltala",
  "title": "Soltala",
  "price": 1500,
  "availability": "in",
  "medium": "Acrylic on canvas",
  "dimensions": "16 x 12 inches",
  "source_image": "soltala-primary.jpg"
}
```

- `slug` → page URL `/artwork/{slug}/`. Must be unique and URL-safe.
- `availability`: `"in"` (Available) or `"out"` (Sold). **Sold works stay
  visible and enquirable** — this is a deliberate business rule, not a bug.
- `source_image`: filename inside `assets.artworks_dir` under
  `assets.source_dir`. The build fails loudly on a missing file.
- Titles are used verbatim in enquiry messages — never "fix" an artist's
  title in code; correct it in config if the artist approves.

Each artwork gets an SEO-unique title/description, descriptive alt text, and
`VisualArtwork` JSON-LD (creator, medium, dimensions, price, availability).
The builder optimizes each source into a ~1600px full image and a ~600px
card thumbnail.

### `exhibitions`, `press`

- `exhibitions`: `[{"year": 2023, "title": "...", "venue": "...",
  "city": "...", "country": "..."}]` — any field except `year` may be empty;
  empty fields are simply omitted from the timeline.
- `press.items`: `{"logo": "assets/img/press/x.png", "logo_alt": "...",
  "caption": "...", "url": "..."}`. **Only link a `url` you have verified.**
  Items without a URL render as plain (unlinked) press mentions.

### `studio` — representation + optional product showcase

```json
"studio": {
  "name": "Zanmi Studio",
  "url": "https://zanmistudio.com",
  "footer_line": "Represented by Zanmi Studio",
  "shop_base_url": "https://zanmistudio.com",
  "products_heading": "Studio Editions",
  "products_sub": "...",
  "products": []
}
```

- The footer representation link renders on **every** page — keep it.
- `products`: prints/merch the Studio sells for this artist. Each item:
  `{"name", "price", "image" (public/ path), "image_alt", "url"}`.
  `url` may be absolute, or relative to `shop_base_url`.
- These are **outbound links only** — artist sites sell originals, never
  merchandise. No cart, no checkout, no prices collected on-site.
- **Empty array = section hidden.** The `studio_products` homepage section,
  the defensive JS hiding, and the validator all agree: no products, no trace
  of the section in the output.

### `pages` — policy content

`pages.privacy` and `pages.delivery` each take `title`, `description`,
`intro`, and `sections: [{heading, body: [paragraphs]}]`. Write them for an
enquiry-only static site: no accounts, no checkout, no card details; shipping
and payment are arranged personally after enquiry. Keep the real contact
email — never invent a domain address.

### `assets` — the image pipeline

```json
"assets": {
  "source_dir": "~/workspace/artist-migration/assets",
  "artworks_dir": "products",
  "site_dir": "site",
  "artwork_max_side": 1600, "artwork_quality": 82,
  "thumb_max_side": 600,    "thumb_quality": 76,
  "site_images": [
    {"src": "hero-background.jpg", "dest": "assets/img/site/hero.jpg",
     "max_side": 1920, "quality": 80}
  ],
  "copy_files": [
    {"src": "logo.png", "dest": "assets/img/site/logo.png"}
  ]
}
```

- `site_images`: resized/optimized into place. `copy_files`: copied byte-for-byte
  (logos, favicons, press logos).
- Source files are **never modified** — optimized derivatives go only into
  `public/`.

### `featured`

`{"heading", "sub", "artworks": [slugs]}` — the homepage "Selected Originals"
row. Every slug must exist in `artworks` (build fails otherwise).

## Design system notes

- `assets/css/styles.css` is shared. It references only the semantic tokens
  from `theme-vars.css` (`--color-primary`, `--color-sand`, `--color-accent`,
  `--font-headings`, …) plus neutral ink/paper. To restyle a new artist,
  change `site.json` — not the CSS.
- `assets/js/main.js` is shared: mobile nav toggle, gallery availability
  filters with live counts, and defensive hiding of the Studio products
  section if it ever renders empty.
- Mobile-first, responsive, `prefers-reduced-motion` respected.

## New-artist checklist

1. Copy folder; update `site` (title, description, `base_url`).
2. Set `theme` colors + fonts — this is what makes it feel bespoke.
3. Add `branding` logo/favicon files; wire them through `assets.copy_files`.
4. Fill `contact` (real email, real WhatsApp number, verified social URLs).
5. Write `hero`, `artist`, `contact_section`; arrange `homepage.sections`
   (delete `custom` entries that don't apply; add the artist's own).
6. Fill `artworks` (unique slugs, real availability), `featured.artworks`.
7. Fill `exhibitions`, `press` (verified URLs only).
8. Set `studio.products` (or leave `[]` to hide the showcase).
9. Adapt `pages.privacy` / `pages.delivery` wording.
10. `python3 build.py` — all checks must pass.
11. Preview at `http://localhost:8000`; review every page type on mobile
    and desktop before any deployment conversation.

## Levoy Exil specifics (the first site on this template)

- Base URL: `https://levoyexil.com`
- 42 artworks (21 available / 21 sold), 49 exhibitions (1972–2023), 8 featured.
- The `custom` homepage section `"gabriela-hearst"` is Levoy-specific — it is
  the worked example of an optional one-off section.
- `studio.products` is empty → the Studio showcase is hidden on this site.
- Standing rules: **do not publish, do not create a repo, do not touch DNS**
  until Daphnee has reviewed the local preview and approved deployment; the
  existing hosting stays live until the new site is verified on the domain.
