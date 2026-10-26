# Gap Scout — Phase 3 proposals (2026-10-26)

**Status: HARD STOP — waiting for your pick.** MODE=manual. Nothing has been built, registered or spent.

> **Read this first: this is a preliminary run.** Reddit, the HN Algolia API, G2/Capterra page fetches and the Porkbun API were all
> blocked by this cloud environment's network policy (Reddit is also blocked for the web-search tool). Evidence comes from
> server-side web search only, so upvote counts are missing and most sources are vendor or comparison blogs, not first-person
> complaints. Domain availability is **unchecked**. No idea reaches the auto-build bar (8.0). The highest score is 6.4.
> My recommendation: re-run Phase 1 with the Reddit API before committing a week of build time.

Scores are 1–10 per criterion. Total = mean of Demand / WTP / Gap / Buildability / Distribution.

| # | Name | Total | D | W | G | B | Dist |
|---|------|------:|--:|--:|--:|--:|--:|
| 1 | RenewDesk | 6.4 | 7 | 7 | 5 | 7 | 6 |
| 2 | StayLegal | 6.0 | 7 | 6 | 4 | 6 | 7 |
| 3 | MarginGuard | 6.0 | 7 | 7 | 5 | 5 | 6 |
| 4 | RenewalProof | 6.0 | 5 | 6 | 6 | 8 | 5 |
| 5 | PerHead | 5.8 | 5 | 5 | 5 | 8 | 6 |
| 6 | TidySignup | 5.8 | 6 | 4 | 5 | 8 | 6 |

---

## 1. RenewDesk — renewal runbooks for the TLS certs MSPs *can't* automate

- **Pitch:** Since March 2026 every public cert dies within 200 days (100 days from March 2027). RenewDesk finds every client cert and turns the non-ACME ones (firewalls, VPNs, appliances) into scheduled, assigned renewal tickets with device-specific steps.
- **Target customer:** 2–20 person MSPs and IT consultants managing 10–100 client domains.
- **Evidence:**
  - [ZoneWatcher: "Your clients' certificates now expire twice a year"](https://zonewatcher.com/blog/2026-08-09-certificate-lifetime-crunch): 40 clients × 25 certs goes from ~1,000 to ~2,000 renewals a year (Aug 2026)
  - [Jimber: 47-day timeline](https://jimber.io/blog/47-day-tls-certificates-timeline/): firewalls, VPN gateways and load balancers "rarely can self-renew"
  - [SSL Insights: 200-day validity](https://sslinsights.com/200-day-ssl-certificate-validity/): limit drops to 100 days March 2027, 47 days March 2029
  - [HN: Let's Encrypt lifetime changes](https://news.ycombinator.com/item?id=46279241) (Dec 2025)
- **Competitors:** [CertKit](https://www.certkit.io/pricing) $99/mo (CT discovery only on $399 Business). [ZoneWatcher](https://zonewatcher.com/pricing) $1.40–4.00/domain/mo. [TrackSSL](https://trackssl.com/) $17–136/mo. KeyChest from ~$20/mo. Most are monitoring tools. None found centres on the manual-renewal workflow.
- **Pricing model:** $49/mo up to 15 clients, $99/mo up to 50, $199/mo unlimited. Flat per-MSP, not per-cert.
- **MVP features:** client → domain inventory. CT-log discovery of issued certs (can reuse `products/ct-phish-api/ctlog.py`). Live TLS probe for expiry and issuer. Device tagging (FortiGate, SonicWall, IIS, …) with a renewal-steps template. Renewal tasks with assignee and due date (expiry − N days). Email alerts via Resend. Per-client PDF/HTML report. Stripe subscription.
- **Build estimate:** 5–6 days (PSA integrations such as HaloPSA/ConnectWise are post-MVP).
- **Domains (unchecked):** renewdesk.io · renewdesk.app · certrenewdesk.com
- **Risks:** crowded adjacent market, so monitoring incumbents could add a task layer. MSPs often buy inside their RMM/PSA. The wedge (manual-renewal workflow) is my inference, not a quoted customer ask.

## 2. StayLegal — permit, renewal and night-cap tracker for multi-city STR hosts

- **Pitch:** One dashboard for every short-term-rental permit, renewal date, night cap and tax filing across cities, so a lapsed permit never costs $484–$2,000 a day.
- **Target customer:** Hosts and co-hosts with 2–15 listings across more than one city.
- **Evidence:**
  - [Beancount: STR registration 2026](https://beancount.io/blog/2026/07/13/short-term-rental-registration-licensing-compliance-guide): per-day fines up to $2,000 (LA) for lapsed certificates (Jul 2026)
  - [Civil Beat: hosts fined for illegal Airbnbs](https://www.civilbeat.org/2026/05/renovation-aloha-hosts-fined-for-illegal-airbnbs-in-latest-misstep/) (May 2026)
  - [RentCompliant: Airbnb fines by city](https://www.rentcompliant.com/blog/airbnb-fines-avoid-penalties/): "nearly every fine … is per day"
  - [Hostex: US STR regulations 2026](https://hostex.io/blog/short-term-rental-regulations-in-the-us/): ordinances spreading to small and mid-sized cities
- **Competitors:** STR Comply US $14.99–39.99/mo. RentPermit ~$19/mo (11 cities). RentCompliant $79 per city kit. HostShield, strrequirements, HostReady. **At least five new entrants, so the gap is narrowing.**
- **Pricing model:** $12/mo for 1–3 listings, $29/mo up to 15, $59/mo for co-hosts.
- **MVP features:** listing → jurisdiction mapping. Permit records with document vault (Supabase storage). Renewal and tax-deadline calendar with email reminders. iCal import from Airbnb/Vrbo to count nights against caps. Curated rules for the top 25 cities. Programmatic SEO pages per city.
- **Build estimate:** 6–7 days (the rules data is the slow part).
- **Domains (unchecked):** staylegal.app · staylegalhost.com · strpermitdesk.com
- **Risks:** stale rules create liability, so it needs a disclaimer and an update process. Crowded, SEO-led market. Airbnb could build it into the host dashboard.

## 3. MarginGuard — tariff-change alerts that show which SKUs just went unprofitable

- **Pitch:** Connect your Shopify store and supplier costs. When a tariff layer changes, MarginGuard shows which variants now lose money and what price restores your margin.
- **Target customer:** US Shopify brands importing 20–300 SKUs (mainly China/Vietnam origin).
- **Evidence:**
  - [LandedCostKit](https://landedcostkit.com/): "every new supplier quote or tariff announcement means redoing the numbers"
  - [DutyPilot: Shopify landed cost 2026](https://dutypilot.org/blog/shopify-landed-cost-calculator-tools-2026): Shopify doesn't natively calculate import costs
  - [Alibaba + Shopify landed cost](https://shopify.ecom-store.pro/blog/alibaba-shopify/): factory quote is 30–60% of true landed cost
  - Tariff stack changed again Feb 2026 (Section 122 replacing IEEPA duties, per the search summaries; verify with CBP)
- **Competitors:** [Landed Cost Receiving](https://apps.shopify.com/landed-cost-receiving) $29/mo. [Landed Cost Radar](https://landedcostradar.com/) (price not found). LandedCostKit (free tier: 10 SKUs per shipment). Plus many free HTS calculators.
- **Pricing model:** $39/mo up to 100 SKUs, $79/mo up to 500.
- **MVP features:** Shopify OAuth (or CSV import first). SKU → HTS code and origin. Cost stack (unit, freight, duty layers, fees). Margin dashboard. "What-if" tariff slider. Weekly email digest. Stripe billing. A custom app/CSV MVP avoids App Store review delays.
- **Build estimate:** 6–7 days for a CSV-first version. Shopify App Store listing adds 1–3 weeks of review.
- **Domains (unchecked):** marginguard.app · tariffmargin.com · landedmargin.com
- **Risks:** duty-rate accuracy and liability. Tariff policy could stabilise and the urgency fade. App Store distribution is gated.

## 4. RenewalProof — state auto-renewal-law kit for Stripe subscriptions

- **Pitch:** Drop-in consent capture, state-aware renewal reminders and a one-click cancel page for Stripe subscriptions, with an audit log you can show a regulator.
- **Target customer:** Indie SaaS, membership and box-subscription businesses on Stripe with US customers.
- **Evidence:**
  - [DTO Law: California ARL changes](https://dtolaw.com/news/californias-automatic-renewal-law-new-requirements-businesses-should-know-about/): separate express consent plus proof required
  - [Adaptiv: ARL by state 2026](https://adaptivpayments.com/blog/automatic-renewal-laws-by-state): MD (Jun 2026), CT/VA (Jul 2026), LA (Jan 2027) new rules
  - [TOS Lawyer: what SaaS must fix in 2026](https://toslawyer.com/auto-renewal-and-subscription-compliance-what-saas-and-e-commerce-companies-must-fix-in-2026/)
  - FTC restarted click-to-cancel rulemaking Jan 2026 (per search summary)
- **Competitors:** Stripe's native "upcoming renewal" emails (free, but not state-aware and no consent proof). Churnkey and ProsperStack cancel flows (pricing not found, aimed at retention). Law-firm audits.
- **Pricing model:** $29/mo up to 500 subscribers, $79/mo up to 5k.
- **MVP features:** Stripe Connect OAuth. Consent-capture widget plus timestamped log. Reminder scheduler (7/15/30-day rules by customer state). Hosted cancel page calling the Stripe API. Compliance report export.
- **Build estimate:** 4–5 days (best fit for your stack).
- **Domains (unchecked):** renewalproof.com · renewalproof.app · cancelcompliant.com
- **Risks:** this looks like legal advice, so it needs counsel-reviewed copy and disclaimers. Stripe could close the gap natively. Demand evidence is mostly law-firm content, not buyers asking.

## 5. PerHead — per-head catering quotes and event sheets for solo caterers

- **Pitch:** Build a menu proposal with per-head pricing and dietary notes in 3 minutes, get it e-signed with a deposit, and print the event sheet. $19/mo, not $69–300.
- **Target customer:** Solo caterers, personal chefs and food trucks doing 4–15 events a month.
- **Evidence:**
  - [Collaborative Kitchens: catering software 2026](https://collaborativekitchens.ai/blog/best-catering-software-2026): tools "priced for catering companies with staff, not solo operators"
  - [Univents: 12 tools compared](https://univents.app/en/knowledge/best-catering-software-2026): generic tools miss per-head pricing and dietary tracking
  - [MicroGaps: solo service software gaps](https://www.microgaps.com/blog/solo-service-software-gaps-2026): solo operators paying $60+/mo for software that barely fits
  - [QuoteIQ: catering software 2026](https://myquoteiq.com/top-8-softwares-for-catering-businesses-in-2026/)
- **Competitors:** Caterease ~$68–300+/mo. QuoteIQ $29.99/mo. Deelo $19–69/seat. Univents (free tier: 4 quotes/mo). HoneyBook $36+/mo.
- **Pricing model:** $19/mo flat. Stripe deposits with an optional 1% platform fee.
- **MVP features:** menu item library. Proposal builder (per-head and tiered pricing, dietary flags). Public proposal page with accept and Stripe deposit. Event sheet PDF. Client CRM-lite. Reminders.
- **Build estimate:** 4–5 days.
- **Domains (unchecked):** perhead.app · perheadquotes.com · caterquote.app
- **Risks:** low-ARPU, high-churn segment. Evidence is mostly vendor blogs. HoneyBook-style generalists are "good enough" for many caterers.

## 6. TidySignup — ad-free signup sheets and volunteer slots for PTAs and youth clubs

- **Pitch:** Signup sheets with no ads and no per-sheet upsells. $49/year per organizer.
- **Target customer:** PTA volunteers, youth sports team managers, church and club coordinators.
- **Evidence:**
  - [SignUpGenius on Capterra](https://www.capterra.com/p/135392/SignUpGenius/): reviewers say ads look unprofessional
  - [PaymentPop: TeamSnap 2026](https://paymentpop.com/merchant-accounts/teamsnap-reviews/): price increases, team limits, intrusive ads (Oct 2026)
  - [Trustpilot: TeamSnap](https://www.trustpilot.com/review/teamsnap.com): admin plus convenience fees on payments
  - [CheckThat: TeamSnap pricing](https://checkthat.ai/brands/teamsnap/pricing): non-refundable auto-renewing contracts
- **Competitors:** SignUpGenius $11.99–59.99/mo. TeamSnap $10.83–25.99/mo. Spond and TeamLinkt are free (they earn on payment fees).
- **Pricing model:** free for 1 active sheet, $49/yr unlimited.
- **MVP features:** sheet builder (slots, quantities, time windows). No-login participant signup. Reminders via Resend. Swap/cancel links. Organizer dashboard. CSV export.
- **Build estimate:** 3–4 days.
- **Domains (unchecked):** tidysignup.com · tidysignup.app · plainsignup.com
- **Risks:** volunteer buyers have low willingness to pay. Strong free competitors (Spond, Google Forms). Distribution relies on word of mouth.

---

## Rejected this run
Delighted replacement, Mailchimp alternative, HoneyBook alternative, pay-transparency checker, M365 license audit, self-managed HOA, status pages, bookkeeper document chasing (all now saturated). 1099 e-filing was rejected on regulatory grounds. See `scores.json`.

## What I need from you
Reply with one of:
1. **Pick #N** (optionally with changes). I'll check domains with Porkbun once the API is reachable, then start Phase 4.
2. **More options / re-run:** recommended. Allow the hosts listed in `decisions.md` and add the Reddit keys, and I'll rerun Phase 1 with real Reddit and HN data.
3. **Modify #N:** tell me what to change.
