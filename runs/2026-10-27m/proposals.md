# Gap Scout — run 15 (2026-10-27m): platform deadlines for online sellers

**Status: HARD STOP.** MODE=manual. $0 spent. Domains unchecked.

**Pattern spotted:** online sellers face a **pile-up of platform deadlines** between Jan and Jun 2027, each covered only by scattered blog posts:

| Date | Platform | Change | Source |
|---|---|---|---|
| Jan 1, 2027 | Shopify (apps) | Public apps must switch to expiring access tokens | [Weaverse](https://weaverse.io/blogs/shopify-expiring-offline-access-tokens-january-2027-public-apps-migration) |
| **Jan 11, 2027** | **Amazon** | **Seller-built bundles deactivated** without brand permission | [PPC Land](https://ppc.land/amazon-gives-bundle-sellers-4-months-to-get-brand-approval-or-lose-listings/) |
| Jan 31, 2027 | Google Merchant Center | Minimum product image size 500×500 | [Google](https://support.google.com/merchants/answer/16989427?hl=en) |
| **Mar 1, 2027** | **Shopify (stores)** | **Script tags stop injecting** (reviews, chat, pop-ups, pixels break) | [learnshopify.dev](https://learnshopify.dev/blog/shopify-script-tags-deprecated) |
| Mar 1 / Jun 1, 2027 | FCC (eBay, Amazon, Walmart…) | FCC ID required on electronics listings | run 13 |
| Ongoing (Oct 2026) | Etsy | One unaltered photo per listing; new AI rules | [PPC Land](https://ppc.land/etsy-forces-sellers-to-show-one-unaltered-photo-in-every-listing/) |

| # | Name | Total | D | W | G | B | Dist |
|---|------|------:|--:|--:|--:|--:|--:|
| 1 | **SellerDeadline** | 7.0 | 8 | 7 | 7 | 6 | 7 |
| 2 | **ScriptScan** | 6.6 | 6 | 5 | 7 | 8 | 7 |
| – | BundleGuard (run 14) | 7.2 | | | | | |
| – | FCCReady (run 13) | 6.6 | | | | | |

## 1. SellerDeadline — one scan, every 2027 platform deadline
- **Pitch:** connect or upload your Amazon, Shopify, Google Merchant, eBay and Etsy data. You get one report covering every listing, bundle, image, app and FCC ID that breaks on each upcoming date, with how to fix it, plus a tracker that alerts you when new deadlines are announced.
- **Why it beats single-issue tools:** sellers run on several channels. One tool, one subscription, and it keeps working after each individual deadline passes (new platform changes are announced constantly). **Launch with BundleGuard as the first module** (Jan 11 is closest), then add ScriptScan, Google image checks and FCC IDs.
- **Money:** free scan, then $39–99/mo by channel count. Done-for-you fixes as an add-on. Affiliate revenue from replacement apps (Shopify Partner affiliate commissions).
- **Build:** 7 days for the core plus the bundle module; about 3 days for each further module.
- **Risks:** platforms may fix things or extend deadlines. It needs a steady feed of policy changes (an AI agent watching seller-news sources).

## 2. ScriptScan — will your Shopify store break on March 1?
- **Gap:** Shopify stops injecting script tags on Mar 1, 2027 (new ones already blocked since Oct 1, 2026). Today merchants must check apps one by one or hire an agency audit ([Insiteful](https://www.insiteful.com.au/shopify-storefront-script-audit/)). I found **no automated scanner**. A developer forum predicts "a lot of apps won't make it" ([Shopify Dev Community](https://community.shopify.dev/t/two-shopify-deadlines-land-9-weeks-apart-in-q1-2027-i-think-a-lot-of-apps-won-t-make-it-past-them/38711)).
- **Product:** enter a store URL, **no install needed**. It crawls the storefront, spots script-tag-injected app scripts, matches them to known apps, flags each as "will break / already migrated", and suggests replacement apps.
- **Money:** free (lead magnet), with revenue from Shopify app affiliate commissions plus a $149 "fix it for me" service. Agencies could white-label it.
- **Build:** 3–4 days. **Domains (unchecked):** scriptscan.app · shopify2027check.com · scripttagcheck.com

## Rejected
- Google 500px images: Google says it will auto-upscale many images.
- YouTube Partner Program thresholds: creator-growth tools are crowded.
- US customs postal filing (Type 13): needs a licensed customs filer.
- Walmart inactivity suspension: trivial.
