# Gap Scout — therapist practices, round 2 (2026-10-27q)

**Status: HARD STOP.** MODE=manual. $0 spent. Domains unchecked.

**Context:** the user's wife is a therapist (insider access for validation). Continuity (6.6) is parked as a side option. The constraint is unchanged: no client health information stored.

| # | Name | Total | D | W | G | B | Dist | Client data? |
|---|------|------:|--:|--:|--:|--:|--:|---|
| 1 | ~~SuperviseMatch~~ (re-scored about 5.0 after competitor check: Motivo, The Supervision App, Guidara, directories) | 5.0 | 7 | 7 | 2 | 6 | 6 | None |
| 2 | **RiskCheck** (30-minute annual HIPAA risk analysis for solo therapists) | 6.2 | 6 | 6 | 5 | 8 | 6 | None (about systems, not clients) |
| 3 | PanelTrack (insurance-panel application tracker for 3–15 clinician groups) | 5.8 | 6 | 6 | 5 | 7 | 5 | None |
| 4 | Openings exchange (therapist-to-therapist "who has openings") | 5.6 | 7 | 4 | 4 | 7 | 6 | De-identified needs only |
| – | Continuity (parked) | 6.6 | | | | | | None |

## 1. SuperviseMatch
- **Money pool:** pre-licensed therapists need about 100–200 hours of direct supervision within 2,000–4,000 clinical hours ([counselingpsychology.org](https://www.counselingpsychology.org/articles/lmft-supervision-hours/)) and pay about **$75–150/hr individual, $40–75 group** ([Kate Walker Training](https://katewalkertraining.com/navigating-the-world-of-clinical-supervision-5-business-models-and-the-role-of-engagement-clinical-supervision-business-models/)). That's roughly **$7.5k–30k per associate** over licensure. Supervision cost is a known sore point ([Tamara Suttle on "money gouging"](https://tamarasuttle.com/clinical-supervision-and-money-gouging/)), and most states now allow tele-supervision.
- **Gap:** searches found hour-logging apps (crowded) but **no supervisor marketplace**. Associates find supervisors by word of mouth, state-association lists and Facebook groups.
- **Product:**
  - Supervisor profiles: state, license type, board-approved supervisor credential, modality, rate, openings, telehealth yes/no.
  - Associates filter, then book an intro call.
  - Supervision contract templates by state.
  - Recurring billing via Stripe Connect.
  - Hour sign-offs exportable to state board forms.
  - **No session video or case notes hosted** (sessions run on the supervisor's own HIPAA-compliant platform).
- **Money:** 10–12% of supervision fees, or a supervisor listing subscription ($29/mo).
- **Risks:** two-sided marketplace (start in your wife's state). Supervisors may take relationships off-platform after matching, so the value has to come from billing and sign-offs. Board rules differ by state.

## 2. RiskCheck
- **Requirement:** an annual written HIPAA security risk analysis applies to solo practices; there is **no size exemption** ([HIPAA Journal](https://www.hipaajournal.com/hipaa-for-solo-practitioners/), [Magister](https://www.magisterba.com/hipaa-risk-assessments-solo/)). The free HHS tool takes about 3–4 hours. A Security Rule overhaul was proposed in Jan 2025 (not final); if finalized, demand jumps.
- **Product:** a plain-language guided assessment pre-mapped to common therapist tools (SimplePractice, TherapyNotes, Google Workspace, Zoom). Produces a dated risk analysis, remediation list and policy pack, with an annual reminder. $79–99/yr.
- **Competitors:** Medcurity (behavioral health focus), Compliancy Group, consultants, the free HHS tool. Moderate.

## 3. PanelTrack
Small groups track insurance-panel applications on spreadsheets. Medallion is about $200–500 per provider per month ([GetPracticeHelp](https://www.getpracticehelp.com/blog/best-credentialing-software/)); Modio and PayerReady also exist. Wedge: a $15/provider/mo tracker for 3–15 clinician groups.

## 4. Openings exchange
NXTWK (free) and FeelGuide already exist ([NXTWK](https://nxtwk.com/), [FeelGuide](https://www.feelguide.network/)). Free incumbents mean therapists won't pay much.

## Earlier therapist ideas still available
CompactMap 6.0, RoomShare 5.8, RateRaise 5.8 (runs/2026-10-27p).
