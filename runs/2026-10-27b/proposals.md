# Gap Scout — run 3 proposals (2026-10-27b)

**Status: HARD STOP.** MODE=manual. $0 spent. Domains unchecked (Porkbun still blocked).

Angles this run:
- 1–3 star complaints about vertical SaaS: salons/studios, daycare, auto repair, nonprofits, therapists, property managers, churches.
- 2026 tax and payroll changes: "no tax on tips/overtime" W-2 boxes, and the IRS replacing FIRE with IRIS.
- Microsoft and Google retirements in 2026.
- Google review removals.

**Result:** one new idea ties for the top spot. The vertical-SaaS complaints are real, but every one of those markets already has a cheap challenger.

| # | Name | Total | D | W | G | B | Dist |
|---|------|------:|--:|--:|--:|--:|--:|
| 1 | **OT Ledger** (new) | 7.0 | 8 | 7 | 6 | 7 | 7 |
| 2 | TagBack (run 2) | 7.0 | 7 | 7 | 8 | 6 | 7 |
| 3 | ReviewVault (new) | 5.8 | 7 | 5 | 4 | 7 | 6 |

Earlier options (AfterPub, RenewDesk, MarginGuard, RenewalProof) are unchanged. ScanRelay is downgraded: one source says Microsoft pushed the basic-auth cutoff to the second half of 2027.

---

## 1. OT Ledger — get the new W-2 overtime (Code TT) and tips (Code TP) numbers right

- **Pitch:** Starting with 2026 W-2s (due **Feb 1, 2027**), employers must report "qualified overtime" in a new box, Box 12 code TT. It counts only the federal FLSA half-time premium. State daily overtime, 7th-day overtime and double time are excluded. Payroll software is getting this wrong. Upload your payroll and timesheet export, and OT Ledger computes the correct per-employee amount with an audit trail.
- **Target customer:** Bookkeepers and payroll accountants running QuickBooks Desktop or Online payroll for hourly-staff clients, especially in daily-overtime states (CA, AK, NV, CO). Also small restaurants for the tips side.
- **Evidence (first-hand):**
  - [QB Community: "New Qualified Overtime Compensation Tracking Not Working"](https://quickbooks.intuit.com/learn-support/en-us/other-questions/new-qualified-overtime-compensation-tracking-not-working/00/1593712): "when it does put a number on the paycheck, it is wrong"
  - [QB Community: California employers, QBO Core Payroll](https://quickbooks.intuit.com/learn-support/en-us/employees-and-payroll/qualified-overtime-tracking-for-california-employers-quickbooks/00/1597786): "we cannot accurately track Qualified OT using what QB has provided"
  - [QB Community: Desktop Enhanced Payroll](https://quickbooks.intuit.com/learn-support/en-us/employees-and-payroll/qualified-overtime-tracking-quickbooks-desktop-enhanced-payroll/00/1592816): wrong when daily overtime occurs without 40 weekly hours
  - [QB Community thread, 5+ pages](https://quickbooks.intuit.com/learn-support/en-us/employees-and-payroll/new-qualified-overtime-compensation-tracking/00/1593295/page/5): users entering amounts manually on each paycheck. Intuit staff said it will not issue a software fix for at least one mapping case.
  - [Ohio CPA: IRS updated W-2 guidance (Aug 2026)](https://ohiocpa.com/for-the-public/news/2026/08/20/irs-releases-updated-w-2-guidance-for-reporting-qualified-overtime) · [PayPro: CA daily OT doesn't qualify](https://paypronext.com/Blog/California-Overtime-in-2026-What-Employers-Need-to-Know-About-New-IRS-Reporting-Rules)
- **Competitors:** payroll providers' built-in tracking (QuickBooks: buggy per the threads; Gusto/ADP not checked). A Qualified Overtime module inside CFS Tax Tools, aimed at tax preparers (pricing not found). Employee-side calculators (free, wrong audience). No employer- or bookkeeper-focused calculator with CSV upload was found.
- **Pricing model:** $49 per employer per tax year, or $299/season for bookkeepers (up to 25 clients). Optional $19/mo to recheck every quarter.
- **MVP features:**
  - Import QuickBooks Desktop/Online payroll detail and timesheet CSVs, with column mapping.
  - Rules engine for the FLSA workweek. Regular rate includes nondiscretionary bonuses. Strips out CA daily, 7th-day and double-time premiums, and contractual overtime.
  - Per-employee and per-paycheck TT amounts. A correction schedule ("enter X on the QB tracking item for paycheck Y").
  - W-2 summary and PDF workpaper for each client.
  - Tips module: map each worker to a Treasury tipped-occupation code (TTOC), and separate qualified tips from service charges. Produces Code TP amounts.
  - Stripe one-time Checkout. Resend emails.
- **Build estimate:** 6–7 days. Messy export formats are the hard part; the rules are well defined. **It needs to launch by about Dec 1** to catch W-2 season.
- **Domains (unchecked):** otledger.com · otledger.app · qualifiedot.com
- **Risks:**
  - Tax-calculation liability: needs a "workpaper, not tax advice" disclaimer and a CPA review of the rules.
  - Intuit, Gusto or ADP may fix their tracking.
  - Seasonal (Nov–Feb). The provisions run only through tax year 2028, so it's a three-season product unless extended.

**Pairing note:** OT Ledger and TagBack sell to the **same buyer**: bookkeepers fixing gaps in QuickBooks. They could launch as one brand ("QuickBooks gap-fillers"). OT Ledger brings seasonal cash now; TagBack brings recurring revenue.

## 3. ReviewVault — archive your Google reviews and get alerted when they vanish

- **Pitch:** Google removed reviews in waves in 2026 (one business reportedly dropped from about 4,600 to 63 in a day) and doesn't notify owners. ReviewVault snapshots every review daily, alerts on removals, and keeps the evidence for an appeal.
- **Evidence:** [ALM Corp, July 2026](https://almcorp.com/news/google-business-profile-reviews-disappearing-investigation-july-2026/) · [Reviewflowz, June 2026](https://www.reviewflowz.com/blog/why-have-your-reviews-disappeared-from-google) · [Google: legitimate reviews sometimes removed by mistake](https://support.google.com/business/answer/10313341?hl=en)
- **Competitors:** BrightLocal, Local Viking, GatherUp, Reviewflowz, ReplyOnTheFly, plus Birdeye and Podium at the high end.
- **Pricing model:** $9/mo per location.
- **Build:** 4 days, but fetching reviews depends on the Google Business Profile API (needs access approval) or a scraper (against Google's terms).
- **Domains (unchecked):** reviewvault.app · reviewvault.io · savemyreviews.com
- **Risks:** crowded, API access is gated, and the urgency fades if Google stops the removal waves.

---

## Rejected this run
- **Vertical SaaS:** every niche already has a cheaper challenger. Salons/studios (GlossGenius $24–168), nonprofit fundraising (Givebutter and Zeffy are free; Little Green Light $45), landlords (Buildium $62, no minimum), churches (Breeze/Tithely $72 flat), auto repair (complaints are about $199–499 tools, but rivals are already pitching). Therapy EHRs add HIPAA burden.
- **FIRE → IRIS 1099 filing:** small filers already use filing services, and transmitting needs an IRS approval code.
- **Microsoft retirements** (Teams connectors, Outlook Lite, Lens) and the Tenor API shutdown: replacements are free and the wedge is tiny.
