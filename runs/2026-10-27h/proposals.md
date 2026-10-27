# Gap Scout — run 10: more AI-powered services (2026-10-27h)

**Status: HARD STOP.** MODE=manual. $0 spent. Domains unchecked.

| # | Name | Total | D | W | G | B | Dist | One line |
|---|------|------:|--:|--:|--:|--:|--:|---|
| 1 | **ConvertCheck** | 6.6 | 7 | 8 | 6 | 6 | 6 | Automated checks that data moved correctly between HR systems, for implementation teams. **Your field.** |
| 2 | **DescribeAI** | 6.4 | 8 | 8 | 5 | 6 | 5 | AI audio description for course and healthcare video at a fraction of $15–50/min |
| 3 | **ClaimKit** | 6.4 | 7 | 7 | 6 | 6 | 6 | Rebuild your lost-belongings inventory after a fire or hurricane from photos, order history and statements |
| 4 | CondoXray | 6.0 | 7 | 6 | 4 | 7 | 6 | Florida condo buyer risk report from association documents |
| 5 | TitleAI | 5.4 | 6 | 7 | 4 | 5 | 5 | AI title abstracting for title companies |

## 1. ConvertCheck — prove the HR data moved correctly
- **Problem:** data migration is reportedly about 40% of an HR-system implementation budget ([Workstream](https://www.workstream.us/blog/ukg-pricing)). Teams compare each test conversion against the source by hand, in spreadsheets: record counts, active/inactive workers, comp, managers, benefits, leave balances ([Workday plan](https://www.roadmap-creator.com/blog/workday-implementation-plan)). "A migration without a parallel-run validation period is a bet" ([HRTechSaaS](https://hrtechsaas.com/blog/hr-data-migration-guide/)). Deadlines are forcing migrations: Kronos Workforce Central on-premise support ends Mar 2027, and Lattice's HR product has shut down.
- **Product:** upload source and target extracts (or connect via a unified HR API). AI suggests field mappings. It then runs about 40 reconciliation checks (counts, salary totals by entity, manager loops, effective dates, leave balances) and produces a sign-off report for each test conversion. Pricing: $1,500 per project or $499/mo for implementation partners.
- **Competitors:** [Settle](https://www.settledata.com/migrate/ukg-to-workday) (AI-assisted migration *service*, enterprise), consultants with spreadsheets, vendor-specific load tools. I found no neutral validation tool that works across HR systems.
- **Why you:** you know the data models, the pain and the implementation partners. That's distribution and credibility none of the other ideas give you.
- **Risks:** small market of implementation partners and HRIS teams; sensitive employee data, so it needs strong security (consider a run-it-on-your-own-machine option).

## 2. DescribeAI — audio description at AI prices
- **Problem:** the accessibility standard requires narrated descriptions of what's on screen for prerecorded video. Manual work costs $15–30/min and AI services $5–15/min ([Visonic](https://visonicai.com/stories/true-cost-of-audio-description-ai-vs-manual/)). A mid-sized university has about 20,000 minutes ([Harmonize](https://harmonizelearning.com/blog/audio-descriptions-required-in-april-2026/)). Deadlines: Title II Apr 2027, HHS 504 May 2027.
- **Product:** connect YouTube, Vimeo or Kaltura. A vision model writes descriptions for the gaps in speech, a synthetic voice reads them, and a human spot-checks. Delivered as a described track or extended video. **$2–4/min.**
- **Competitors:** 3Play Media (AI audio description through Wistia and others), Verbit, Visonic AI, Captioning Star ($7.50/min).
- **Risks:** quality judgement on complex visuals; university purchasing cycles.

## 3. ClaimKit — rebuild your contents claim
- **Problem:** after a total loss, insurers need a room-by-room inventory, and "the burden of proving that loss falls on you" ([public adjuster guide](https://forthepublicadjusters.com/blog/fire-damage-contents-inventory-guide/)). People forget about a third of their items ([OneHomeAgent](https://onehomeagent.com/blog/ai-home-inventory-insurance-claims/)). Order history and photos are accepted proof ([JustClaims](https://justclaims.ai/blog/personal-property-inventory-for-insurance/)). Contents claims are often six figures.
- **Product:** upload phone photos (pre-loss photos of rooms), Amazon/Target order exports, card statements and email receipts. AI builds an itemised inventory with replacement-cost pricing and the export format adjusters want. **$299 flat**, or $799 with human review. Free for claims under $25k as a goodwill and SEO tool.
- **Competitors:** JustClaims.ai, OneHomeAgent, contents specialists and public adjusters (10–20% fees), Encircle (sold to contractors).
- **Risks:** stay a documentation tool. Negotiating with insurers needs a public-adjuster licence. Demand is disaster-driven and lumpy.

## 4–5 (brief)
- **CondoXray:** 56% of Miami-Dade buildings missed the deadline for their structural reserve study (SIRS) ([governingdocs](https://governingdocs.dev/blog/florida-condo-crisis-2026/)). AI reads the budgets, minutes, reserve study and milestone inspection to produce a $79 buyer report. Several tools already exist (governingdocs, assessment-risk checkers).
- **TitleAI:** manual title searches cost $150–400; Neuskale advertises $10/document. Professional-liability (E&O) insurance and underwriter disclosure are hurdles.

## Rejected
Freight carrier vetting: Highway, Carrier Assure, RMIS and MyCarrierPackets already cover it.
