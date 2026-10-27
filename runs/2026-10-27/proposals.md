# Gap Scout — Phase 3 proposals (2026-10-27, run 2)

**Status: HARD STOP — waiting for your pick.** MODE=manual. Nothing built, registered or spent.

**What changed from run 1:** Reddit, HN and Porkbun are still blocked. This run went straight to **first-hand complaint sources**:
Microsoft Q&A, the QuickBooks community, Shopify Community, the Airbnb Community Center, Trustpilot and Product Hunt. It
also looked for **products and features retired in 2026**. Those create demand with a deadline that competitors haven't
fully covered yet. Domain availability is still **unchecked**. No idea reaches 8. The top score is 7.0, up from 6.4.

| # | Name | Total | D | W | G | B | Dist | New? |
|---|------|------:|--:|--:|--:|--:|--:|---|
| 1 | **TagBack** | 7.0 | 7 | 7 | 8 | 6 | 7 | new |
| 2 | AfterPub | 6.4 | 9 | 5 | 4 | 6 | 8 | new |
| 3 | RenewDesk | 6.4 | 7 | 7 | 5 | 7 | 6 | from run 1 |
| 4 | MarginGuard | 6.0 | 7 | 7 | 5 | 5 | 6 | from run 1 |
| 5 | RenewalProof | 6.0 | 5 | 6 | 6 | 8 | 5 | from run 1 |
| 6 | ScanRelay | 5.4 | 8 | 6 | 3 | 4 | 6 | new |

Full write-ups for #3–5 are in `runs/2026-10-26/proposals.md`.

---

## 1. TagBack — bring back QuickBooks Online Tags (P&L by tag, bulk tagging, bank-feed tagging)

- **Pitch:** Intuit is removing Tags and pointing users to Custom Fields. Custom Fields can't be set on bank-feed transactions, can't produce a P&L, and can't be bulk-updated. TagBack connects to QBO and gives all three back.
- **Target customer:** Small businesses on QBO Simple Start or Essentials (no class tracking; 1–4 custom fields), and the bookkeepers who manage them, for job, event, property or grant tracking.
- **Evidence (first-hand):**
  - [QBO Community: "Anyone else suddenly lost Tags feature?"](https://quickbooks.intuit.com/community/reports-and-accounting-5/anyone-else-suddenly-lost-tags-feature-375321): "Custom fields does NOT have the same capability as tags." Access was cut in July 2026, before the promised 2028 date.
  - [QBO Community: tags migration, incomplete functionality](https://quickbooks.intuit.com/learn-support/en-us/reports-and-accounting/tags-migration-to-custom-fields-incomplete-functionality/00/1547324): "cannot run PnL report for custom fields"
  - [QBO Community: custom field in bank deposit](https://quickbooks.intuit.com/learn-support/en-us/banking/custom-field-in-bank-deposit/00/1536420): can't be assigned on the bank categorisation screen
  - [Intuit help: custom fields and tagging](https://quickbooks.intuit.com/learn-support/en-us/help-article/class-list/tag-transactions-quickbooks-online/L7x3G0aLv_US_en_US): Intuit confirms no P&L by custom field
  - [Gentle Frog Bookkeeping](https://gentlefrog.com/quickbooks-tags-are-being-discontinued/): Tags mattered most to Simple Start and Essentials users
- **Competitors:** none found that replaces Tags specifically. Workarounds are upgrading to QBO Plus for class tracking (about $45+/mo more) or exporting reports to Excel. Reporting add-ons (Fathom, Reach Reporting, Syft) are broader and cost more.
- **Pricing model:** $12/mo per QBO company. $79/mo for bookkeepers (up to 15 companies). 14-day trial.
- **MVP features:**
  - QBO OAuth on Intuit's free Builder tier (500k CorePlus credits/mo).
  - Sync transactions into Supabase. Tags live in TagBack; QBO data is never modified.
  - Rules that auto-tag by payee, memo, account or amount, plus bulk tagging.
  - P&L by tag or tag group, and transaction list by tag. CSV/Excel export.
  - Import exported legacy tag reports to restore history.
  - Stripe billing, Resend emails.
- **Build estimate:** 6–7 days of code. Intuit's production-key questionnaire runs in parallel (days to weeks). Intuit App Store listing comes later.
- **Domains (unchecked):** tagback.app · tagback.io · gettagback.com (avoids "QuickBooks"/"QBO" trademarks)
- **Risks:**
  - Single-platform dependency: Intuit could add bank-feed custom fields, or change API pricing. Above Builder credits the Silver tier is about $300/mo.
  - Production-key approval gates launch.
  - The size of the affected group is unknown; one source says ~3/4 of QBO users never used Tags.

## 2. AfterPub — open, convert and keep producing your Publisher files after the October 2026 retirement

- **Pitch:** Publisher left Microsoft 365 this month. Upload your .pub archive and AfterPub converts it to PDF, editable DOCX and web templates. Your weekly bulletin or newsletter keeps its layout, and you edit it in the browser from then on.
- **Target customer:** Church offices, schools/PTAs, clubs and small businesses with years of .pub bulletins, newsletters and flyers.
- **Evidence (first-hand):**
  - [MS Q&A: "We have thousands of Publisher files."](https://learn.microsoft.com/en-us/answers/questions/5773729/why-cant-microsoft-create-a-way-to-convert-from-pu)
  - [MS Q&A: "you will no longer be able to open or edit these files"](https://learn.microsoft.com/en-us/answers/questions/5852051/after-this-date-you-will-no-longer-be-able-to-open)
  - [MS Q&A: "using Publisher for more than 25 years"](https://learn.microsoft.com/en-us/answers/questions/5396035/ive-been-using-publisher-for-more-than-25-years-wh)
  - [MS Q&A: what happens to existing .PUB files](https://learn.microsoft.com/en-us/answers/questions/6000817/what-will-happen-to-existing-pub-files-after-micro)
  - [UMC: After Publisher, tools for every budget](https://www.resourceumc.org/en/content/after-publisher-bulletin-and-newsletter-tools-for-every-budget)
- **Competitors:**
  - Converters: Aspose (free, one file at a time), FreeConvert, PrivConvert (20 files per batch), Univik desktop (trial: 10 pages), Save Your PUB Files ($11, needs Publisher installed).
  - Bulletin tools: Publish Media ($9.99/mo or $99/yr), Bulletin Plus ($19.99/mo), bltn ($35/mo), Happy Bulletin ($49/mo).
  - Free alternatives: Canva and Word.
- **Pricing model:** $29 one-time "archive rescue" (up to 500 files) plus $8/mo for the web editor and templates.
- **MVP features:** bulk .pub upload. Conversion through a cloud API (ConvertAPI/Aspose Cloud; per-file cost). Searchable archive. Rebuild 5 common bulletin layouts as editable templates. Print-ready PDF export. SEO pages ("open .pub without Publisher").
- **Build estimate:** 5 days. Layout-preserving conversion depends on a third-party API.
- **Domains (unchecked):** afterpub.com · afterpub.app · afterpublisher.com
- **Risks:**
  - Strongest demand of any idea, but the gap is closing fast and conversion quality isn't in my control.
  - Buyers have low willingness to pay, and demand is a one-off spike that fades over 6–12 months.
  - Per-conversion API costs eat into margin.

## 6. ScanRelay — scan-to-email relay for MSPs before Exchange turns off basic-auth SMTP (Dec 2026)

- **Pitch:** Point every printer at ScanRelay. It delivers mail through each client's own Microsoft 365 tenant (Graph/OAuth), so nothing breaks when basic auth goes away.
- **Target customer:** MSPs with many clients that have older multifunction printers.
- **Evidence:**
  - [mySMTP: SMTP AUTH off by default late Dec 2026](https://mysmtp.com/blog/2026/01/28/microsoft-is-pulling-the-plug-on-smtp-auth-in-exchange-december-2026/)
  - [Just Tech: what it means for scan-to-email](https://justtech.com/microsoft-disabling-basic-authentication-for-smtp-auth-what-it-means-for-scan-to-email/)
  - [MS Q&A: MFPs and SMTP Auth deprecation](https://learn.microsoft.com/en-au/answers/questions/1879579/multi-function-printers-and-smtp-auth-deprecation)
- **Competitors:** SMTP2GO (free for 1,000 emails/mo; MSP sub-accounts), Mailgun, SendGrid, Microsoft's connector/relay (free), Microsoft HVE.
- **Pricing model:** $3 per device per month.
- **Build estimate:** 7+ days. **Doesn't fit your stack:** it needs a long-running SMTP listener, which Vercel can't host, so it would need a VPS or Fly.io.
- **Domains (unchecked):** scanrelay.app · scanrelay.io · relayforscanners.com
- **Risks:** crowded, there's spam/abuse liability, and Microsoft may extend the deadline again.

---

## Rejected this run
- Shopify Stocky replacement: 8+ apps already.
- SaaS auto-renewal tracker: Timemy, oboloo, Renewly, Contract Hound.
- Airbnb 15.5% fee repricing: free calculators plus direct-booking platforms.
- QuickBooks Desktop 2023 sunset: migration services already crowded.
- Relay.app and Arc shutdowns: absorbed by existing tools.

See `scores.json`.

## Recommendation
**TagBack** is the only idea this time with a clear, Intuit-confirmed gap, first-hand complaints, B2B buyers, and no direct competitor found. Its main risk is depending on Intuit. **AfterPub** is the fastest cash grab if you want a one-time-purchase SEO play. Pick one, ask for more, or modify.
