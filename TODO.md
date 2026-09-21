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
- [x] Production build prepared (2026-09-21 ~1 AM ET): built a production-ready
  copy with `"baseurl": ""` in /tmp/levoy-prod — all validation checks pass
  (42 artwork pages, 49 exhibitions, enquiry links, sitemap, JSON-LD).
  NOT pushed to GitHub; no custom domain configured; no DNS touched.
  Cutover checklist: PRODUCTION-CUTOVER-CHECKLIST.md (in repo root).
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
- [x] SEO/AEO foundation: unique titles/descriptions, canonicals, Open Graph/Twitter cards, VisualArtwork + Organization JSON-LD, alt text, sitemap — audited 2026-09-20 ~11:40 PM ET, all present; added theme-color #0e3c79 meta to every page head
- [x] Gabriela Hearst section with click-to-play official video + Rain Magazine article link
- [x] Homepage hero repositioned so Levoy's face is visible
- [x] FAQ section with FAQPage schema, Person entity, llms.txt
- [x] News section with two article title pages staged ("Still Painting at 81", Hearst collaboration)
- [x] Both news articles published in full with photos (2026-09-20)
- [x] Site pushed to GitHub (main + gh-pages preview)
- [x] All 17 press cards now show real publication logos (2026-09-20 ~11:45 PM ET): sourced + visually verified 10 missing logos (Fashionista, Grazia, Fashion Network, RAIN, Yahoo News, Kendam, Wikipedia, Nader Haitian Art, Google Arts & Culture, MutualArt); build.py press-logo copy loop now covers press_page groups; main 3140e74 + gh-pages df1217f — live on preview
- [x] Homepage feature video vertically centered in the blue block (2026-09-20 ~11:45 PM ET)

## 2026-09-20 ~11:05 PM ET — fixed unstyled preview (Daphnee reported "just writings")
- Root cause: all internal links used root-relative paths (/assets/...) which 404'd
  on the GitHub Pages project subpath, so no CSS/JS/images/nav loaded.
- Fix: site.json gained a Jekyll-style "baseurl" ("/levoy-exil-website"); page_html
  prefixes href/src when set. At production cutover set baseurl to "" and rebuild.
- Validation now fails the build if bare root-relative URLs remain (regression guard).
- Deployed main 60f4498 / gh-pages a4378b4; live-verified CSS, JS, hero, press, gallery all 200.

## 2026-09-20 ~11:15 PM ET — press page redesigned (Daphnee: "not on brand, just words")
- Was text-only cards with no visual identity. Redesigned in the site's design language:
  brand-blue hero band, logo tiles on every card (7 real logos; blue monogram
  tiles for the rest), featured-story card for the Vogue GH runway review with
  the Solrou image, group headers with article counts, alternating tinted bands.
- Deployed main d6ad3f0 / gh-pages 94dd2df; live-verified.

## 2026-09-20 ~11:25 PM ET — YouTube video added to Hearst article (Daphnee request)
- "Watch the film" click-to-play block (WUl9KtUQf38) added to the
  "From Fermathe to the Runway" news article; video already on homepage feature.
- Runway photos: Daphnee wants the 4 PDF runway shots big on the site. Found in
  PDF: 4 shots of the Solrou macrame look, credited "FILIPPO FIOR / GORUNWAY.COM"
  (Vogue screenshot p2). Copyright flag raised — awaiting her confirmation that
  she has permission/rights before publishing.

## 2026-09-20 ~11:24 PM ET — Awaiting Gabriela Hearst photo permission (Daphnee sent ask)
- Daphnee sent the permission request to Gabriela Hearst's team for the 4 runway
  photos (Solrou macrame look, Filippo Fior / GoRunway).
- PUBLISHED 2026-09-20 ~11:35 PM ET while permission is pending (Daphnee's
  explicit instruction after the rights flag): "On the runway" gallery with the
  4 Solrou macrame shots + credit "Runway photographs by Filippo Fior /
  GoRunway.com" on the Hearst news article. Rebuild-safe via site_images jobs.
- IF PERMISSION DENIED or takedown: remove the gallery immediately and rebuild.

## 2026-09-21 ~12:15 AM ET — real Vogue + WWD logos (Daphnee: placeholders "do not have logo")
- The Vogue and WWD press tiles were generated placeholder tiles (white text on
  brand blue), not the real mastheads. Replaced with the genuine logos, normalized
  as black-on-transparent 1200x630 tiles matching the other press tiles:
  Vogue = Didot serif masthead (vector source, re-fit after viewport clipping);
  WWD = bold sans wordmark (raster source, white knocked out).
- Same two files feed the press-page cards AND the homepage "As Seen On" section,
  so one replacement fixed both. No site.json changes needed.
- Rebuilt, validated, deployed main 9a36102 / gh-pages 45bb073; live-verified
  the new tiles on the preview URL.

## 2026-09-21 ~12:00 AM ET — old WordPress site archived (6 main pages; artwork pages NOT archived)
- Full-page desktop PDFs of the 6 main pages (Home, Gallery/Shop, Exhibitions,
  Privacy, Delivery/Returns, empty Cart) + INDEX.txt saved in Drive folder
  "Old site archive — WordPress (Sep 2026)" inside "Levoy Exil — Website".
- GAP: the 42 individual artwork/product pages were NOT separately archived.
  Decide with Daphnee whether to capture them before the domain cutover.
- Note: Drive archive currently lives under the hello@zanmibackyard.com Google
  account; per Daphnee's chat boundary, do not touch that account from the
  Levoy Exil chat — use the Studio/Levoy connection for any further Drive work.

## 2026-09-21 ~00:15 ET — Press logos backed up to Google Drive
- All 17 publication logo PNGs uploaded to Drive: "Levoy Exil — Website" >
  03_Assets > "Press logos" (new subfolder).
- Includes the corrected black Vogue and WWD mastheads.
- Skipped press-generic-225x225.png (retired placeholder, no longer used).

## 2026-09-21 ~01:15 AM ET — lifestyle "in a home" photos restored (Daphnee's catch)
- Daphnee noticed the old WordPress site showed framed "how it looks in a home"
  photos that hadn't been carried over. Confirmed: 9 such photos existed in the
  migration inventory (*-gallery-frame.png/jpg) but were wired into ZERO artwork
  pages on the new site.
- Added `lifestyle_image` to the 8 artworks that have one (alfasum, columbasol,
  desolfam, falcumda, fasolcum, kosollumba, solcuma, soldalum; solcuma had two
  variants — kept solcuma-gallery-frame.png). build.py now generates
  `<slug>-lifestyle.jpg` (max 1200px) and each artwork page renders it under the
  main photo with caption "In your home — a framed display of <Title>" and a
  descriptive alt attribute. New `.artwork-lifestyle` CSS in styles.css.
- Rebuilt, all validation checks passed, synced public/ -> preview_public/,
  pushed main 3bf341f / gh-pages 3b52e17; live-verified the Soldalum page +
  image URL on the preview site.
- NOTE for cutover: the production build in /tmp/levoy-prod predates this change
  and must be REGENERATED from the current build at cutover time (after DNS
  approval), so the lifestyle photos go live on levoyexil.com too.
