# Gap Scout — AI-powered services (2026-10-27g)

**Status: HARD STOP.** MODE=manual. $0 spent. Domains unchecked.

**Your answers:** you want to sell **software or an AI-powered service**, with no preference on industry or customer. So this run looked for **work businesses already pay people or outsourcers to do** that AI can now do about 90% of. The budget already exists, and you sell the outcome at a fraction of the price. Some call this "service-as-software" ([eGlobalis](https://www.eglobalis.com/services-as-software-what-happens-to-your-vendor-when-ai-eats-the-billable-hour/)).

## The big wave: accessibility deadlines in 2027–2028
- **ADA Title II:** public universities, cities and counties (50k+ population) must make websites and documents meet WCAG 2.1 AA by **Apr 26, 2027**; smaller ones by Apr 26, 2028 ([Duane Morris](https://www.duanemorris.com/alerts/doj_extends_ada_title_ii_digital_accessibility_deadlines_one_year_0426.html)).
- **HHS Section 504:** every healthcare provider receiving HHS funds (hospitals, clinics, nursing homes) with 15+ staff by **May 11, 2027**; smaller ones by May 2028 ([Deque](https://www.deque.com/blog/section-504-digital-accessibility-deadlines-what-every-hhs-funded-provider-must-know/), [accessibility.build](https://accessibility.build/blog/hhs-extends-section-504-healthcare-accessibility-deadline)).
- Universities now require software vendors to prove compliance before they buy ([University of Oklahoma](https://www.ou.edu/digital-accessibility/taskforce)). One vendor quoted Ohio State **$5/page, about $20M** for its library PDFs; an AI pipeline did it for about $0.06/page ([Venngage](https://venngage.com/blog/reduce-pdf-remediation-costs/)).

| # | Name | Total | D | W | G | B | Dist | Sells to |
|---|------|------:|--:|--:|--:|--:|--:|---|
| 1 | **ACR Express** | 6.8 | 8 | 8 | 5 | 7 | 6 | Software companies selling to universities, governments and hospitals |
| 2 | **QuestionnaireDone** | 6.6 | 7 | 8 | 5 | 7 | 6 | Small software companies selling to enterprises |
| 3 | DocReady | 6.4 | 9 | 8 | 4 | 6 | 5 | Universities, cities, school districts |
| 4 | FormReady | 6.2 | 8 | 7 | 5 | 6 | 5 | Clinics, practices, nursing homes |
| 5 | PolicyCheck AI | 6.2 | 7 | 8 | 6 | 5 | 5 | Independent insurance agencies |
| 6 | PermitReply | 6.0 | 7 | 7 | 6 | 5 | 5 | Contractors and architects |

AI-service options from earlier runs: VibeRescue 6.6, HireNotice 6.6, BillBack 6.0.

---

## 1. ACR Express — accessibility conformance report (VPAT) in 48 hours, for software sold to the public sector and healthcare

- **Problem:** before a university, city or hospital can buy your software, it now asks for an **Accessibility Conformance Report** (ACR; the industry template is called a VPAT). Consultants charge **$1,850–4,450**, sometimes $30–60k with remediation, and take weeks. Thousands of edtech, gov-tech and health-tech vendors need one before the 2027 deadlines.
- **What you sell:** a fixed price of **$790–1,290**, delivered in 48 hours. You enter your app URL and test login. Automated checks plus AI-driven walkthroughs test each of the 50 WCAG criteria. A human reviews the results. You receive a filled-in ACR on the current template (VPAT 2.5) and a prioritised fix list. Add-on: $199/mo to re-test every release and keep the ACR current.
- **Competitors:** [ACR Desk](https://acrdesk.com/) ($1,490 fixed), accessibility consultancies ($1.8–4.5k: [ADA Compliance Pros](https://www.adacompliancepros.com/blog/vpat-cost)), Deque, Level Access (enterprise). Do-it-yourself workbooks are about $79 plus 20–40 hours.
- **Day to day:** run the pipeline, review AI findings for about 2 hours per report, talk to software founders.
- **Build:** 7 days (Playwright crawler, axe-core, LLM checks, ACR document generator, Stripe, client portal).
- **Domains (unchecked):** acrexpress.com · acrexpress.app · vpatin48.com
- **Risks:** an ACR is only as good as its testing, so human review is essential. An overstated report creates liability. ACR Desk already proves the fixed-price model, so you'd compete on speed, price and continuous re-testing.

## 2. QuestionnaireDone — security questionnaires answered for you, priced per questionnaire

- **Problem:** small software companies trying to land enterprise deals get 100–400-question security questionnaires (the standard SIG and CAIQ templates, or custom ones). Outsourced filling costs a **median of $33k/yr**. Tools start at $3.6k–20k/yr (Loopio, Conveyor, Vanta add-on), which is too much for a 10-person startup that gets 10 questionnaires a year.
- **What you sell:** **$149 per questionnaire, back in 24 hours.** The customer uploads past answers, policies and SOC 2 documents once. AI drafts every answer with citations, a human checks the low-confidence ones, and you return the completed file. Subscription option: $299/mo for unlimited.
- **Competitors:** [ResponseHub](https://responsehub.ai/blog/7-best-security-questionnaire-automation-software-2026/) ($149/mo, self-serve), 1up, ComplyJet, Conveyor, Vanta. Most are self-serve software; "done for you, per questionnaire" is thinner.
- **Build:** 6 days. **Domains (unchecked):** questionnairedone.com · secqdone.com · answermyquestionnaire.com
- **Risks:** wrong answers carry contractual liability, so the customer signs off on each one. Customers' security documents are highly sensitive, which means strong security posture is needed from day one.

## 3. DocReady — AI-plus-human PDF remediation (brief)
The biggest demand, the most competition: CASO Comply and Accessibility on Demand from $0.30/page, ADAPT AI, Tabnav. Manual work runs $5–25/page. You'd win only on a niche (for example school-board packets, or course materials for one learning-management system) plus quality guarantees. Government purchasing is slow.

## 4. FormReady — accessible patient intake forms for clinics (brief)
HHS 504 applies to clinics with 15+ staff by May 2027. Their PDF intake forms must become accessible. Convert them to accessible web forms, with no patient data handled by you. Competitors: general remediation vendors, Phreesia and IntakeQ (full intake platforms). Clinics are slow buyers.

## 5. PolicyCheck AI (brief)
Independent insurance agencies (about 36k in the US) pay offshore teams to compare issued policies against what was quoted. Exdion has an AI version but sells to enterprises; 98% of agencies plan AI spending in 2026 ([ReSource Pro](https://www.resourcepro.com/blogs/why-ai-in-insurance-agencies-is-defining-2026)). Offer $8–15 per policy check for small agencies. Needs insurance domain knowledge.

## 6. PermitReply (brief)
Expediters charge $500–15k ([Permit Place](https://permitplace.com/permit-expediter-cost-guide/)), and responding to correction cycles is about half of the delay. AI reads the plan-check comments and drafts the response letter and checklist for the architect. Competitors: PermitFlow (VC-backed), expediters. Rules vary by city.

---

## Honest note
Every option here has competitors; that's 2026. What makes these better than earlier runs is that **the buyer already has a budget line** (consultants, outsourcers), and AI lets you deliver faster and cheaper while keeping most of the margin. The deadlines (2027–2028) bring buyers to you.
