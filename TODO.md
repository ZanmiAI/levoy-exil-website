# Levoy Exil Website — Task List

Living checklist for the levoyexil.com rebuild. Zanmi updates this file
every time something is finished or added — nothing falls through the cracks.

## Daphnee's tasks

- [ ] Google Business Profile for the gallery (after the domain goes live)
- [ ] Google Search Console + Bing Webmaster Tools verification (after the domain cutover)
- [ ] Backlink outreach — ask press outlets and institutions that mention Levoy to link to levoyexil.com
- [x] Reviewed and approved both news articles (2026-09-20) — full text published with chosen photos
- [ ] Approve the domain cutover (DNS switch from WordPress to the new static site)
- [ ] Send the original Levoy logo source files, if available

## Zanmi's tasks

- [x] Wrote the two news article drafts for Daphnee's review (approved 2026-09-20)
- [ ] Prepare the exact DNS records for the cutover (only after her approval)
- [ ] After cutover: verify SSL, levoyexil.com + www.levoyexil.com, redirects, mobile layout, assets, navigation, every enquiry link
- [ ] Upload the organized project backup to Google Drive + create the project index
- [x] Drive backup done: "Levoy Exil — Website" folder now holds 01_Code (site.json, build.py, TEMPLATE-README.md, TODO.md), 02_Docs (news article drafts), 03_Assets (asset inventory manifest), and "00 — Project Index" at the root. Single folder confirmed — no duplicate to consolidate.
- [x] Footer blue matched to header (2026-09-20): footer was using the darker `--color-primary-deep` (#0a2c5c) while the header uses the brand blue `--color-primary` (#0e3c79, from the real logo). Changed `.site-footer` to the brand blue. Rebuilt (all checks pass), pushed main fcd1bb3 + gh-pages 47234be.
- [x] Approved logo + favicon sets installed on the site (2026-09-20): new multi-size favicon.ico + apple-touch-icon.png in `<head>` (replacing the old 32px PNG); header/hero badge upgraded to the crisp new LE mark (1024px); footer brand lockup now shows the real serif wordmark (white); JSON-LD logo now points to the wordmark. All 14 brand files saved in repo `brand/` and Drive 03_Assets. Rebuilt (all checks pass), pushed main cd19d5b + gh-pages 02c6f45 — live on preview.
- [x] Hero "filter" removed per Daphnee's feedback (2026-09-20 ~10:40 PM ET): the hero photo was dimmed to 50% opacity over deep blue, which washed it out. Removed the dimming so the photo shows in full color; added a soft localized scrim behind the centered headline text only (photo edges untouched) plus stronger text shadows to keep "Levoy Exil" readable over the bright photo. Rebuilt (all checks pass), pushed main e3a9671 + gh-pages 561958a — live on preview.
- [ ] Full mobile + visual acceptance check of the new site (screenshot review running 2026-09-20 ~6:35 PM ET)
- [x] Official brand blue locked by Daphnee (2026-09-20): #0e3c79 — verified against the original website (theme-color meta + the original favicon file's actual blue). #283d75 (screenshot-sampling artifact) retired. Registered in brand/BRAND.md (GitHub) and the project summary branding document.

## Done

- [x] Static site built (home, gallery, 42 artwork pages, exhibitions, policies, 404, sitemap, robots)
- [x] Enquiry-first shop: WhatsApp + email on every artwork, sold works visible and enquirable
- [x] SEO/AEO foundation: unique titles/descriptions, canonicals, Open Graph/Twitter cards, VisualArtwork + Organization JSON-LD, alt text, sitemap
- [x] Gabriela Hearst section with click-to-play official video + Rain Magazine article link
- [x] Homepage hero repositioned so Levoy's face is visible
- [x] FAQ section with FAQPage schema, Person entity, llms.txt
- [x] News section with two article title pages staged ("Still Painting at 81", Hearst collaboration)
- [x] Both news articles published in full with photos (2026-09-20)
- [x] Site pushed to GitHub (main + gh-pages preview)

## 2026-09-20 ~11:05 PM ET — fixed unstyled preview (Daphnee reported "just writings")
- Root cause: all internal links used root-relative paths (/assets/...) which 404'd
  on the GitHub Pages project subpath, so no CSS/JS/images/nav loaded.
- Fix: site.json gained a Jekyll-style "baseurl" ("/levoy-exil-website"); page_html
  prefixes href/src when set. At production cutover set baseurl to "" and rebuild.
- Validation now fails the build if bare root-relative URLs remain (regression guard).
- Deployed main 60f4498 / gh-pages a4378b4; live-verified CSS, JS, hero, press, gallery all 200.
