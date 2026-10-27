# Gap Scout — deep dive (2026-10-27f): trend-first options

**Status: HARD STOP.** MODE=manual. $0 spent. Domains unchecked. Accounting is still excluded.

**What changed:** earlier runs hunted for unmet compliance chores, which is why everything felt like a tax form. This run started from **where money and attention are moving in 2026**, then looked for the gap inside each trend:
- generative AI apps (consumer AI spending nearly tripled to $5B+)
- GLP-1 weight-loss drugs
- the in-person social-club boom
- AI-built ("vibe-coded") apps breaking
- household costs (electricity up 42% in 5 years; insurance at 9% of a mortgage payment)
- 59M family caregivers
- the phone-free childhood movement
- micro-dramas

Upside: **L** = could become a large business, **M** = solid niche business.

| # | Name | Total | Upside | Money model | One line |
|---|------|------:|:--:|---|---|
| 1 | **Offramp** | 6.8 | L | $19/mo consumer subscription | The plan for after you stop GLP-1s |
| 2 | **PremiumShield** | 6.8 | L | Free tool, paid leads to roofers and inspectors | Find every insurance discount and grant your house qualifies for |
| 3 | **ClubFuel** | 6.6 | L | 15–20% take on sponsorships | Brands book run clubs and social clubs like ad inventory |
| 4 | **SolarOrphan** | 6.6 | M | Repair leads ($50–250) plus $5/mo monitoring | Help for solar owners whose installer went bankrupt |
| 5 | **VibeRescue** | 6.6 | M | $199–499/mo care plan | Keeps AI-built apps secure, backed up and running |
| 6 | BillBack | 6.0 | M | 25–35% of refunds found | AI audits small-business utility bills for overcharges |
| 7 | PhonePact | 6.0 | M | Free, plus kid-phone affiliate revenue and PTA tier | School-level coordination for phone-free kids |
| 8 | ParentDesk | 5.8 | L | $15/mo per family | AI admin desk for your aging parent's mail, bills and appointments |
| 9 | ShortsStudio | 5.6 | L | Content/IP | AI-made micro-drama series, built on YouTube Shorts first |

Still on the table from earlier runs: HireNotice 6.6, AfterPub 6.4, HRIS Lint 6.4.

---

## 1. Offramp — the plan for after GLP-1s

- **Why now:** **50–65% of people stop GLP-1s within the first year** (cost is a major reason). Those who stop regain about two-thirds of the weight within a year, and research says evidence for maintenance strategies "remains limited". Incumbents (MyFitnessPal, Noom) are building features for people *on* the drug, not for leaving it.
- **Evidence:**
  - [Medscape: rapid regain when GLP-1s stopped](https://www.medscape.com/viewarticle/weight-regain-health-benefit-loss-rapid-when-glp-1s-stopped-2026a10000kr)
  - [Medscape: 50–65% discontinue in year 1](https://www.medscape.com/viewarticle/solutions-emerging-post-glp-1-weight-regain-2026a1000ine)
  - [eClinicalMedicine: maintenance evidence limited](https://www.thelancet.com/journals/eclinm/article/PIIS2589-5370(26)00240-3/fulltext)
  - [Protein Pal: most "protein trackers" are calorie counters](https://www.proteinpalapp.com/articles/best-protein-tracker-glp1)
- **Competitors:** Noom (GLP-1 companion), MyFitnessPal (GLP-1 mode, Aug 2026), WeightWatchers, human coaching ($149–200/mo: Trainwell, Future, Caliber). None is built around coming off the medication.
- **MVP:**
  - 16-week off-ramp program: protein targets, a strength plan, and appetite-return coaching.
  - Early-warning regain alerts (weight-trend bands), plus a log of any taper your doctor prescribes.
  - AI check-ins. Stripe subscription. Waitlist plus content SEO ("what happens when you stop Ozempic").
- **Build:** 6–7 days.
- **Domains (unchecked):** offramp.health · offrampapp.com · afterglp.com
- **Risks:** must stay wellness, not medical advice (no dosing guidance). Consumer acquisition costs. Big apps could copy it.

## 2. PremiumShield — every insurance discount and grant your house qualifies for

- **Why now:** insurance is a record **9% of the typical mortgage payment**, and carriers are dropping policies. Discount programs are scattered: Florida wind mitigation (up to ~40%), Alabama FORTIFIED-roof grants ($10k), Florida My Safe Florida Home ($10k), California Safer from Wildfires discounts plus a new Safe Homes grant program (Jan 2026). I found **no tool** that tells a homeowner which ones apply to their address.
- **Evidence:**
  - [ConsumerAffairs: insurance at 9% of mortgage payment](https://www.consumeraffairs.com/news/homeowners-insurance-rates-are-projected-to-rise-again-in-2026-031826.html)
  - [United Policyholders: quiet cancellations](https://uphelp.org/the-16-homeowner-trap-why-major-insurers-are-quietly-canceling-2026-policies-this-week/)
  - [Smart Home America: grants by state](https://www.smarthomeamerica.org/news/available-roofing-grants)
  - [Claims Journal: discounts not enough](https://www.claimsjournal.com/news/national/2026/07/09/338693.htm)
- **Money model:** free address check gives a personalised savings and grant plan. Revenue from sending qualified leads to wind-mitigation inspectors, FORTIFIED roofers and wildfire-hardening contractors ($50–200 per lead; roofing jobs are $15k+). Optional $29 "insurer letter" pack.
- **MVP:** address → state/county rules engine for FL, AL, CA, TX, LA, SC. Upgrade ROI calculator. Grant eligibility check. Lead routing to contractors. Programmatic SEO page for each county.
- **Build:** 6 days, plus a week of curating the program data.
- **Domains (unchecked):** premiumshield.app · lowermypremium.com · mitigationfinder.com
- **Risks:** must not quote or sell insurance (that needs a license), so stay informational. Grant funds open and close. You'd need to recruit contractors per state.

## 3. ClubFuel — brands book run clubs and social clubs like ad inventory

- **Why now:** run-club membership is reported up 59%, athletic singles events up 136%, and Gen Z is trading bars for clubs. Brands (On, HOKA, wearables, drinks) are paying to reach them, but deals are made directly and "there is no rate card". I found **no marketplace** that matches clubs with sponsors. Club tools (Heylo, SportLync, Strava) don't help clubs earn from sponsors.
- **Evidence:**
  - [Modern Retail: brands tapping run clubs](https://www.modernretail.co/marketing/as-running-clubs-explode-in-popularity-brands-are-tapping-these-groups-for-sampling-opportunities-and-sponsorships/)
  - [Diplo's Run Club: 7 national sponsors, 100k+ participants](https://www.endurancesportswire.com/diplos-run-club-announces-event-sponsors-ahead-of-2026-27-season/)
  - [Analog: "there is no rate card"](https://analog.directory/blog/posts/run-club-sponsorship-for-brands)
  - [Heylo pricing: club tools take payment fees, not sponsorship](https://wf.heylo.com/pricing)
- **Money model:** clubs list for free, with verified attendance, audience profile and a media kit. Brands book activations: a sampling run, a season sponsorship, or a 10-club city bundle. You take 15–20%. Typical deal sizes run from about $500 for a single run to five figures for a multi-club program.
- **MVP:** club profiles with attendance proof (photos and check-ins), brand search and filters, booking requests, Stripe Connect payouts, post-event recap report. Start by hand-signing 30 clubs in 2 cities and selling to brands yourself.
- **Build:** 7 days.
- **Domains (unchecked):** clubfuel.co · clubfuel.app · sponsormyclub.com
- **Risks:** a two-sided marketplace (it breaks the original "no large network effects" rule, but works city by city). Brand sales are a people business. Experiential agencies could compete.

## 4. SolarOrphan — help for solar owners whose installer went bankrupt

- **Why now:** SunPower, Sunnova, Mosaic and others went bust. Owners lost workmanship warranties and monitoring, and battery owners lost support. One estimate (unverified) puts it at **~1.3M households**. Repair shops are writing "orphan rescue" pages because the demand is there.
- **Evidence:**
  - [NRG Clean Power: your solar company went out of business](https://nrgcleanpower.com/learning-center/your-solar-company-went-out-of-business/)
  - [HomeSolarHub: SunPower workmanship warranty void](https://www.homesolarhub.com/guides/sunpower-bankruptcy-san-diego/)
  - [Elevarus: solar leads $25–250](https://elevarus.com/solar-lead-prices-four-products/)
- **Money model:** free "what do I do" wizard (installer, equipment, which warranty still applies, who services it). Sell repair leads to local certified installers. $5/mo monitoring through the Enphase and SolarEdge APIs, with alerts when production drops.
- **Build:** 6 days. **Domains (unchecked):** solarorphan.com · orphansolar.app · solarlifeline.com
- **Risks:** getting monitoring API access from Enphase and SolarEdge. Repair-lead prices are unproven. The demand shrinks over time.

## 5. VibeRescue — a care plan for AI-built apps

- **Why now:** millions of people are shipping apps with Lovable, Bolt and Cursor. One scan found **65% of 1,400 production vibe-coded apps had security issues**, typically a Supabase key in client JavaScript with row-level security off. Rescue agencies quote **$25–50k**. Scanners exist ($9–99/mo), but they only report problems; no one *keeps the app healthy*.
- **Evidence:**
  - [Forbes: vibe coding has a massive security problem](https://www.forbes.com/sites/jodiecook/2026/03/20/vibe-coding-has-a-massive-security-problem/)
  - [Prompts2Products: exposed key + RLS off](https://prompts2products.substack.com/p/safe)
  - [DEV: scanners "only checked for existence"](https://dev.to/solobillions/i-tested-every-vibe-coding-security-scanner-2026-heres-what-actually-works-p9k)
  - [Hatchworks: $25k–50k rescues](https://hatchworks.com/blog/gendd/cost-of-vibe-coding/)
- **Money model:** free scan, then $199/mo (monitoring, backups, dependency updates, fixes delivered as GitHub pull requests) or $499/mo with a monthly human review. AI agents do most of the work.
- **Build:** 6–7 days for the scanner, fix-PR bot and dashboard, all on your stack.
- **Domains (unchecked):** viberescue.dev · viberescue.com · keepmyappalive.com
- **Risks:** crowded scanner market. Lovable, Bolt and others are adding built-in checks. Liability if a breach happens anyway.

## 6–9 (brief)

- **BillBack (6.0):** electricity is up 42% in 5 years. Audit firms take 35–50% of refunds and work slowly by hand. Upload 12–36 months of bills; AI checks each bill against the utility's published rates (free data in the OpenEI Utility Rate Database) and finds wrong rate classes, demand-charge errors and taxes. Charge 25–35% of what's recovered. Tariff complexity is the hard part. ([Forbes](https://www.forbes.com/sites/daraabasiita/2026/07/30/how-ai-finds-the-money-hiding-in-company-utility-bills/), [Inertia](https://www.inertiaresourcesinc.com/blog/utility-bill-audit))
- **PhonePact (6.0):** the phone-free movement is spreading ([Axios](https://www.axios.com/2026/05/15/screen-free-childhood-parents-ditch-kids-phones)). Wait Until 8th already has 150k pledges and a 10-family threshold. The gap is after the pledge: group plans, kid-safe phone and watch picks (affiliate revenue), and a PTA dashboard. Low willingness to pay; mission-driven.
- **ParentDesk (5.8):** 59M family caregivers spend about $8.7k a year out of pocket ([CNBC/AARP](https://www.cnbc.com/2026/10/26/family-caregiving-costs-2026-midterm-elections.html)). Forward a parent's mail, bills and portal emails; AI sorts, flags scams and tracks due dates and appointments. Large market, but crowded with care apps and full of trust and privacy issues.
- **ShortsStudio (5.6):** micro-drama is a ~$8B format, and AI cuts production cost about 10x ([Outlierkit](https://outlierkit.com/resources/vertical-micro-drama-youtube-shorts/)). Rather than another tool, this is a content bet: produce AI series for YouTube Shorts and TikTok, then license or paywall the winners. Hits-driven; not software.

## Rejected this run
- **Car-deal checkers:** Vettor, Validate My Car Deal, Visor, CarEdge.
- **Cheaper NCSA (college recruiting):** NextCommit, Rosterhunter, SportsRecruits.
- **Vibe-app security scanners:** VAS, CheckVibe, VibeEval, Lovable's built-in check. Pivoted to the VibeRescue care plan instead.
- **AI local-government news:** Hamlet, Citizen Portal AI, Locunity.
- **Reshoring sourcing marketplace:** too heavy.
- **Trading-card and pet tech:** no gap evidence found.
