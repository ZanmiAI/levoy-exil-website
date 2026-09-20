# Levoy Exil — Official Website

Static replacement website for **levoyexil.com**, the online gallery of Haitian
master painter **Levoy Exil** (Saint Soleil movement).

Built on the **Zanmi Studio Artist Website Template** — see
[TEMPLATE-README.md](TEMPLATE-README.md) for how the shared engine works and
how to launch the next artist's site from this folder.

## Status (2026-09-20)

- ✅ Build complete: `python3 build.py` generates the full site into `public/`
- ✅ All 16 automated validation checks pass
- ⏳ Awaiting Daphnee's review of the local preview — **do not publish, do not
  touch DNS, do not cancel the current hosting** until she approves and the new
  site is verified live on the domain.

## Quick start

```bash
cd ~/workspace/levoy-exil-website
python3 build.py                                    # build into public/
python3 -m http.server 8000 --directory public      # preview at http://localhost:8000
```

## What gets generated

- `/` — hero, artist bio, selected originals, press, Gabriela Hearst feature,
  contact (Studio products section hidden — list is empty)
- `/gallery/` — all 42 originals with availability filtering
- `/artwork/{slug}/` — 42 artwork pages, each with VisualArtwork JSON-LD and
  WhatsApp + email enquiry buttons naming the painting
- `/exhibitions/` — 49 exhibitions, 1972–2023
- `/privacy/`, `/delivery-returns/` — adapted policy pages (enquiry-only wording)
- `/404.html`, `/sitemap.xml`, `/robots.txt`
- Optimized images (~1600px max side) + `assets/css/theme-vars.css` (brand tokens)

## Key business rules encoded in the build

- **Originals only, enquiry-first.** No cart, no checkout. Every artwork —
  including the 21 sold pieces — stays visible and offers WhatsApp
  (`https://api.whatsapp.com/send?phone=50934249786`, painting name prefilled)
  and email (`levoyexilgallery@gmail.com`, painting name in subject).
- `contact@levoyexil.com` does not exist and appears nowhere (build fails if found).
- Footer on every page: **Represented by [Zanmi Studio](https://zanmistudio.com)**.
- Hours: Monday–Saturday, 8 AM–8 PM EST.

## Editing content

Everything lives in **`site.json`** — branding, contact details, homepage
section order, artworks, exhibitions, press, policies. Edit it, rebuild, done.
See TEMPLATE-README.md for the full config reference.

## Project layout

```
site.json              # single source of truth (all content + branding)
build.py               # generator: images → pages → sitemap → validation
assets/css/styles.css  # shared stylesheet (semantic brand tokens)
assets/css/theme-vars.css  # generated from site.json (do not edit by hand)
assets/js/main.js      # nav toggle, gallery filters, products hiding
public/                # generated site — deploy this folder as-is
TEMPLATE-README.md     # template guide for the next artist site
```

## Source assets (never modified by the build)

- Migration archive: `~/workspace/levoy-exil-migration/assets/` (102 products, 31 site files)
- High-res scans: `~/workspace/levoy-exil-highres/extracted/LEVOY EXIL_FINAL JPG/` (38 files)

**Artwork imagery (2026-09-20):** all 6 plausible high-res candidate matches
were visually compared side-by-side and **rejected** — none of the 38 scans
depict any of the 42 listed paintings (confirmed by a perceptual-hash sweep of
all 42×38 pairs). Every artwork keeps its existing `*-primary.jpg` image.
