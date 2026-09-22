# Levoy Exil — Production Cutover Checklist

Prepared 2026-09-21 by Zanmi. **No DNS or hosting changes have been made.**
Production remains WordPress + WooCommerce/The7 on levoyexil.com.

## What Zanmi did (my part — done)

- [x] Built a production-ready copy of the site locally with `"baseurl": ""`
      (preview keeps `"/levoy-exil-website"`; production serves from domain root).
- [x] Ran the full build validation (42 artwork pages, 49 exhibitions,
      enquiry links, sitemap, JSON-LD, alt text, no cart/checkout wording).
- [x] Prepared the exact DNS records for GitHub Pages (see below).
- [x] Prepared the `CNAME` file content (`levoyexil.com`).

The production build output lives in `/tmp/levoy-prod/public/` for inspection —
it has NOT been pushed to GitHub and no custom domain has been configured.

## The DNS plan (for Daphnee's GoDaddy — do NOT apply until she approves)

GitHub Pages custom-domain records for `levoyexil.com`:

**Add / change only these web records:**

| Host | Type  | Value               |
|------|-------|---------------------|
| `@`  | A     | `185.199.108.153`   |
| `@`  | A     | `185.199.109.153`   |
| `@`  | A     | `185.199.110.153`   |
| `@`  | A     | `185.199.111.153`   |
| `www`| CNAME | `zanmiai.github.io` |

**Leave every other record untouched** — especially MX (email), TXT
(verification/SPF/DKIM), and any other hostnames. `levoyexilgallery@gmail.com`
is not affected by website-record changes.

## Daphnee's part (tomorrow)

1. **Export / screenshot the current GoDaddy DNS table** for levoyexil.com
   (so we can do a record-by-record comparison before anything changes).
2. **Decide on the 42 old artwork/product pages** — archive them or accept the
   current 6-page archive as sufficient. (Never call the 6-page set complete.)
3. **Approve the cutover explicitly** — say the word right before we apply
   the 5 web records above.
4. After DNS is applied (Zanmi's verification steps, only after approval):
   - GitHub repo → Settings → Pages → Custom domain: `levoyexil.com`
     → Enforce HTTPS (wait for certificate).
   - Verify `https://levoyexil.com` and `https://www.levoyexil.com`:
     pages, assets, navigation, responsive layout, WhatsApp + email links.
   - Keep WordPress hosting until BOTH domains pass.
5. After go-live:
   - Google Search Console + Bing Webmaster Tools verification.
   - Google Business Profile for the gallery.
   - Backlink outreach to press/institutions.

## Safety rules (standing)

- Never cancel WordPress hosting until the replacement is verified on both
  `levoyexil.com` and `www.levoyexil.com`.
- Preserve every unrelated DNS record during cutover.
- No production push without Daphnee's explicit approval immediately
  before applying changes.
