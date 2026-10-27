# Gap Scout — run 4 proposals (2026-10-27c) — no accounting/tax/payroll

**Status: HARD STOP.** MODE=manual. $0 spent. Domains unchecked. `config.json` now excludes accounting, bookkeeping, tax and payroll, so TagBack and OT Ledger are out.

**Bottom line:** no new idea beats the earlier non-accounting options. About 25 searches across consumer, creator, events, developer tools, trades, ecommerce, platform shutdowns and new regulations all ran into the same wall: **by late 2026, every gap visible in web search already has 3–8 small competitors**, usually launched within months of the triggering change.

## Combined non-accounting board

| # | Name | Total | D | W | G | B | Dist | From |
|---|------|------:|--:|--:|--:|--:|--:|---|
| 1 | AfterPub | 6.4 | 9 | 5 | 4 | 6 | 8 | run 2 |
| 2 | RenewDesk | 6.4 | 7 | 7 | 5 | 7 | 6 | run 1 |
| 3 | **InboxBridge** | 6.0 | 9 | 6 | 4 | 4 | 7 | **new** |
| 4 | MarginGuard | 6.0 | 7 | 7 | 5 | 5 | 6 | run 1 |
| 5 | RenewalProof | 6.0 | 5 | 6 | 6 | 8 | 5 | run 1 |
| 6 | **FeedReady** | 5.8 | 6 | 6 | 4 | 7 | 6 | **new** |
| 7 | ReviewVault | 5.8 | 7 | 5 | 4 | 7 | 6 | run 3 |
| 8 | **AgendaReady** | 5.4 | 6 | 6 | 5 | 6 | 4 | **new** |
| 9 | **FamilyFixtures** | 5.0 | 6 | 3 | 4 | 7 | 5 | **new** |

---

## 3. InboxBridge — keep pulling your other email into Gmail after January 2027

- **Pitch:** Gmail stops fetching external mailboxes over POP in January 2027, and new setups are already blocked. InboxBridge connects to the old mailbox (ISP, cPanel or domain email) and drops new mail into Gmail every few minutes, just like before.
- **Target customer:** Consumers on legacy ISP email, and small businesses whose domain email sits on cheap hosting with free Gmail as the front end.
- **Evidence:**
  - [Google: "Starting January 2027, Gmail will no longer support these features"](https://support.google.com/mail/answer/16604719?hl=en)
  - [Ask HN: How are you handling Gmail ending POP3 and Gmailify?](https://news.ycombinator.com/item?id=46763892)
  - [The Register, Jan 2026](https://www.theregister.com/2026/01/05/gmail_dropping_pop3/) · [TechRepublic](https://www.techrepublic.com/article/news-gmail-ends-gmailify-pop3/)
- **Competitors:** MailBridge (has a comparison page), MailPorter, Postdirect, ForwardMyInbox, imapsync (free, technical). Google recommends forwarding (free, but often breaks with ISP mailboxes and authentication checks).
- **Pricing model:** $3/mo or $29/yr per mailbox. $8/mo for businesses (5 mailboxes).
- **MVP:** IMAP/POP poller as a Vercel cron or worker. Gmail import via API (keeps headers and labels). Status dashboard. Failure alerts via Resend. Stripe.
- **Build:** 5 days of code, **but** the Gmail import scope is "restricted". That means Google verification (~6 weeks) plus a yearly CASA security assessment (about $675–5,400), so it likely misses the January 2027 rush. The workaround (an IMAP connection with a Gmail app password) avoids the review but means storing sensitive credentials.
- **Domains (unchecked):** inboxbridge.app · inboxbridge.io · fetchtogmail.com
- **Risks:** you'd be late to market with four or more competitors, Google approval sits on the critical path, and you'd be custodian of people's email credentials.

## 6. FeedReady — get WooCommerce, Squarespace and Wix stores into ChatGPT Shopping

- **Pitch:** ChatGPT Shopping now runs on merchant product feeds. Shopify and Etsy are enrolled automatically; everyone else must apply and maintain a spec-compliant feed. FeedReady generates, validates and refreshes it.
- **Evidence:**
  - [CoSpark: WooCommerce must register manually and submit a separate feed](https://cospark.com/blog/woocommerce-chatgpt/)
  - [Nightjar: stores lost visibility overnight in the July 2026 switch](https://nightjar.so/blog/how-to-get-your-products-on-chatgpt-and-google-ai-mode-shopping)
- **Competitors:** for WooCommerce, Product Feed PRO (free ChatGPT feed in its $199/yr plan), CTX Feed ($119/yr), RexTheme ($99.99/yr), FeedAgentX ($9/mo). Wix is building it natively. Squarespace has nothing obvious.
- **Pricing model:** $15/mo. **Build:** 4–5 days. **Domains (unchecked):** feedready.ai · feedready.app · aishopfeed.com
- **Risks:** OpenAI keeps changing the program (Instant Checkout was launched, then retired). Platforms will build this in. Merchant-program approval is required.

## 8. AgendaReady — accessible meeting agendas and minutes for small public bodies

- **Pitch:** Under the ADA Title II rule, public-body web documents must meet the WCAG 2.1 AA accessibility standard by April 2027 (large public bodies) and April 2028 (small towns and special districts). AgendaReady turns a board clerk's agenda and minutes into accessible web pages and PDFs, so each new monthly document is compliant.
- **Evidence:** [Duane Morris: DOJ extends deadlines one year](https://www.duanemorris.com/alerts/doj_extends_ada_title_ii_digital_accessibility_deadlines_one_year_0426.html) · [EqualWeb: recurring agendas are covered](https://www.equalweb.com/blog/ada-title-ii-pdf-documents-deadline/)
- **Competitors:** CivicPlus, Granicus, PDF-remediation services, EqualWeb, Siteimprove.
- **Pricing model:** $49/mo per public body. **Build:** 5–6 days. **Domains (unchecked):** agendaready.com · agendaready.app · accessibleagendas.com
- **Risks:** government buying is slow (distribution 4/10), and the deadline could slip again.

## 9. FamilyFixtures — one calendar for every kid's team apps

- **Pitch:** Merges schedules from TeamSnap, GameChanger, SportsEngine and school calendars into one family view, with carpool slots.
- **Evidence:** [Teach Hoops on Sammi](https://teachhoops.com/sammi-app-sports-parents/) · [CastApp: each TeamSnap team is a silo](https://www.castapp.info/best-youth-sports-apps/)
- **Competitors:** Sammi, Cozi, FamilyWall, Skylight. **Risks:** parents won't pay much (WTP 3/10).

---

## Rejected this run (each already has several low-cost competitors)
- **HVAC refrigerant rules (EPA, Jan 2026):** RefriTrak, RefriComply, RefrigerantTrack, FMHero, Field Ascend.
- **Florida 25-unit condo websites:** Mosaic HOA, Conduu, Urbi.
- **FDA food-traceability rule (FSMA 204):** deadline moved to 2028; several tools already.
- **Kajabi/Thinkific price-hike refugees:** Podia, Skool, Circle, Payhip.
- **Tenant deposit evidence:** door.lease, DepositProof, Evidence Vault.
- **Rover pet-sitter fees:** Time To Pet, Scritches, Pupline.
- **Eventbrite:** no 2026 fee hike found.
- **iOS 26 call screening:** Numeracle, Caller ID Reputation, Hiya.
- **Postman free-plan cut:** Bruno, Hoppscotch, Insomnia, Yaak.

## What I'd change about the search, not the ideas
1. **Get raw demand before vendors write about it.** Reddit and HN comments show pain weeks before "alternatives" blogs exist. That needs those hosts allowed and the Reddit keys added.
2. **Use an unfair advantage.** With gaps this crowded, the winner is whoever already has distribution or domain knowledge. If you know an industry, a community or a customer list, I can scout inside that niche specifically.
3. **Or pick on execution.** AfterPub and InboxBridge both have huge, deadline-driven search demand. A better product plus SEO can beat earlier entrants, but it's a race.
