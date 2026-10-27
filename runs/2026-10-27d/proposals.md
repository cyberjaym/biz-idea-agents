# Gap Scout — run 5: HR systems (2026-10-27d)

**Status: HARD STOP.** MODE=manual. $0 spent. Domains unchecked. Payroll calculation is still excluded; HRIS data, hiring, leave, compliance reporting and migrations are in scope.

**Why this run is different:** you work in HR systems. In a crowded market, the person who understands the buyer and the data wins. The scores below assume **no** insider advantage. Your background should raise Distribution and Buildability for whichever idea matches what you work on day to day.

| # | Name | Total | D | W | G | B | Dist |
|---|------|------:|--:|--:|--:|--:|--:|
| 1 | **HireNotice** | 6.6 | 7 | 7 | 6 | 7 | 6 |
| 2 | **HRIS Lint** | 6.4 | 6 | 7 | 6 | 7 | 6 |
| 3 | **HR Legacy Vault** | 6.0 | 6 | 7 | 6 | 6 | 5 |
| 4 | LeaveMap | 5.6 | 7 | 6 | 4 | 6 | 5 |
| 5 | EU PayReady | 5.4 | 7 | 7 | 4 | 5 | 4 |

---

## 1. HireNotice — AI-in-hiring compliance for employers too small for enterprise tools

- **Pitch:** If your recruiting tools use AI (resume screening, ranking, video scoring), several state laws now require notices, records and candidate rights. HireNotice inventories your AI use, generates the right notices for each candidate's location, handles candidate requests for an explanation, a correction or human review, and keeps the audit trail.
- **Target customer:** Employers with 10–500 staff hiring in IL, CA, CO or NYC, plus fractional HR consultants and staffing agencies.
- **Why now:**
  - **Illinois** HB 3773: in force since Jan 2026, covers employers with **1+ employees**. Notice duty applies, but the draft rules were withdrawn in June 2026, so employers are guessing.
  - **California** automated-decision rules: in force since Oct 2025 for employers with 5+ employees. 4-year recordkeeping, and liability reaches through vendors.
  - **Colorado** SB 26-189: starts **Jan 1, 2027** (notice, explanation of adverse decisions, human review, 3-year records, no small-employer exemption). Currently tied up in a court challenge.
  - **NYC** Local Law 144: annual bias audit.
- **Evidence:** [Manatt](https://www.manatt.com/insights/newsletters/employment-law/ai-assisted-hiring-faces-a-new-compliance-landscape-in-2026-california-and-illinois-put-discriminatory-impact-and-transparency-front-and-center) · [Crowell on SB 26-189](https://www.crowell.com/en/insights/client-alerts/colorado-hits-reset-on-ai-regulation-sb-26-189-repeals-and-reenacts-the-colorado-ai-act) · [Buchalter: legal challenge](https://www.buchalter.com/insights/colorado-rewrites-its-ai-law-what-employers-must-know-about-sb-26-189/) · [SiftFirst tracker](https://siftfirst.com/compliance/ai-hiring-laws-by-state) · [Ethena: laws for 2027](https://www.goethena.com/post/ai-in-hiring-5-employment-laws-every-hr-team-should-know-in-2027/)
- **Competitors:**
  - AI-governance platforms (FairNow, Warden AI, Holistic AI): roughly $15k–80k/yr mid-market estimate, aimed at mid-market companies and HR software vendors.
  - Law-firm memos and free trackers.
  - Broad labor-law libraries bundled into HRIS contracts.
  - I found nothing self-serve and sized for small employers.
- **Pricing model:** $99/mo (1 hiring state), $249/mo (multi-state), $499/mo for agencies and consultants (10 clients).
- **MVP features:**
  - Questionnaire mapping AI features across your hiring tools (Greenhouse, Lever, Ashby, Workable, LinkedIn, Indeed).
  - Rules for which law applies based on candidate and job location.
  - Attorney-reviewed notice templates, plus a careers-page widget and email snippets.
  - Candidate request portal (explanation, correction, human review) with deadline tracking.
  - Reviewer sign-off log. Record-retention export.
  - Integrations with the Greenhouse and Ashby APIs.
- **Build estimate:** 6–7 days. Paying a lawyer to review the templates is a cost and time item.
- **Domains (unchecked):** hirenotice.com · hirenotice.app · aihiringnotice.com
- **Risks:**
  - The laws are in flux: Colorado's is enjoined, Illinois has no final rules, and the federal government is pushing to preempt state AI laws.
  - The product can look like legal advice, so it needs attorney-reviewed content and disclaimers.
  - ATS vendors may add notice features.

## 2. HRIS Lint — a compliance and data-quality scan for your HR system

- **Pitch:** Upload an employee export, or connect BambooHR, Rippling, Gusto, ADP or Paylocity. HRIS Lint flags the errors that become lawsuits or failed audits:
  - exempt staff paid under the federal or state salary threshold (state thresholds change again Jan 1)
  - missing work locations
  - employees in states with new paid-leave programs who need notices
  - roles in pay-transparency states with no salary range
  - EEO-1 gaps and I-9 reverification dates due
  - duplicates, broken manager chains, ex-employees still active
- **Target customer:** HR generalists at 50–1,000 person companies, and **fractional HR and HRIS consultants who run audits for clients**. This is likely your network.
- **Evidence:**
  - Reporting is the most-cited HRIS gap ([Alpha Apex, citing the 2025-26 HR Systems Survey: 40%](https://www.alphaapexgroup.com/blog/hris-selection-guide)).
  - Integration and ID mismatches ([Bindbee](https://bindbee.dev/feeds/blog/challenges-hr-system-integration-enterprise-needs)).
  - Multi-state leave sprawl ([Pulpstream](https://pulpstream.com/resources/blog/multi-state-paid-leave-2026)).
  - No vendor advertises a cross-HRIS FLSA threshold scan; the search suggested a custom check.
- **Competitors:** built-in alerts (Rippling compliance alerts, BambooHR + VirgilHR), ADP SmartCompliance (enterprise), ComplianceHR, SalaryCube (comp). None is a neutral audit tool that works across HRIS products for consultants.
- **Pricing model:** $149 per audit report, or $79/mo for continuous monitoring. $299/mo for consultants (15 client orgs, white-label PDF).
- **MVP features:**
  - CSV/XLSX import with smart column mapping for the top 6 HRIS exports.
  - About 25 rules: federal and state salary thresholds, new paid-leave states, pay-transparency states, EEO-1 fields, I-9 dates, data hygiene.
  - Severity-ranked findings and a PDF audit report.
  - Phase 2: API sync via a unified HR API (Finch or Merge) or direct BambooHR/Rippling APIs.
- **Build estimate:** 5–6 days, CSV-first.
- **Domains (unchecked):** hrislint.com · hrislint.app · hrdatacheck.com
- **Risks:**
  - Rules need yearly upkeep; threshold tables change every January.
  - HRIS vendors keep adding native alerts.
  - Uploading employee PII brings security expectations; plan on SOC 2-lite controls and short retention.

## 3. HR Legacy Vault — read-only archive for decommissioned HR and timekeeping systems

- **Pitch:** When you leave Kronos Workforce Central (on-premise end of life **March 31, 2027**), Lattice HRIS (data deleted Aug 2026), or any old HRIS, you still have to keep timecards and personnel records for years. Keeping the old system running just to look things up is expensive. Vault imports the exports into a searchable, read-only archive with retention rules and an audit log.
- **Evidence:** [WorkAxle: WFC EOL Mar 31, 2027](https://www.workaxle.com/blog/kronos-workforce-central-end-of-life-migration) · [Settle Data: reimplementation, not upgrade](https://www.settledata.com/blog/ukg-migration-guide) · [ClonePartner: Lattice data deleted Aug 6](https://clonepartner.com/blog/lattice-hris-shutdown-the-2026-migration-data-export-guide/)
- **Competitors:** general enterprise archiving (Archive360 and similar), migration consultancies, keeping the legacy server alive.
- **Pricing model:** one-time import $1,500–5,000 plus $99–499/mo by record volume.
- **Build:** 6–7 days for a CSV/DB-export importer, search, per-employee record view, retention and legal hold.
- **Domains (unchecked):** hrlegacyvault.com · hrarchive.app · legacyhrvault.com
- **Risks:** enterprise sales cycle, sensitive data with security reviews, and every source system's export format is different. **Your HRIS knowledge is the moat here.**

## 4. LeaveMap — multi-state leave navigator (brief)
Minnesota, Delaware and Maine paid-leave programs went live in 2026, on top of FMLA and other state programs. LeaveMap generates notices, coordinates programs and tracks leave per employee. Competitors: Tilt, Sparrow, Pulpstream, plus built-ins in Rippling and Gusto. Crowded among funded startups.

## 5. EU PayReady — EU pay transparency for US companies with small EU teams (brief)
First reports are due June 2027 (150+ employees). Competitors: Figures, Ravio, Syndio, Sysarb, Axios Analytics and SAP all target this market. Low gap.

---

## Questions that would sharpen this
1. Which systems do you know best (Workday, UKG/Kronos, ADP, BambooHR/Rippling, an ATS)?
2. Implementer or consultant, in-house HRIS admin, or vendor side?
3. Company size you serve, and do you have a network (clients, a community, LinkedIn following) you could sell to?
