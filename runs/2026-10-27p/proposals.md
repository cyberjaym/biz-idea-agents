# Gap Scout — therapist practices, low competition, privacy-light (2026-10-27p)

**Status: HARD STOP.** MODE=manual. $0 spent. Domains unchecked.

**Constraint from user:** less competitive, mindful of privacy. Strategy: serve the *business* of the practice (licenses, continuity, space, rates) and **store no client health information**. That avoids HIPAA business-associate obligations and the crowded EHR, AI-notes and billing markets.

| # | Name | Total | D | W | G | B | Dist | Client data stored? |
|---|------|------:|--:|--:|--:|--:|--:|---|
| 1 | **Continuity** (professional will service) | 6.6 | 6 | 6 | 8 | 7 | 6 | None |
| 2 | CompactMap (multi-state license and compact tracker for group practices) | 6.0 | 6 | 7 | 5 | 7 | 5 | None (clinician data only) |
| 3 | RoomShare (rent out empty group-practice offices by the hour) | 5.8 | 6 | 6 | 5 | 7 | 5 | None |
| 4 | RateRaise (payer rate benchmarks and negotiation letters) | 5.8 | 6 | 7 | 4 | 6 | 6 | None |

## 1. Continuity — the professional will, as a living service
- **Requirement:** ethics codes expect a plan for clients and records if the clinician dies, becomes incapacitated or closes the practice: ACA C.2.h, APA 10.09, NASW 1.15, AAMFT 1.11 ([Wellness Collaborative](https://www.wellnesscollaborative.io/professional-will-for-therapists/), [Pepitone Law](https://www.pepitonelaw.com/legal-guides/therapist-professional-will)). Some states go further; for example, one summary says Oregon requires naming a records custodian to the board (unverified). "The most common failure is a practitioner dying or becoming incapacitated without a designated records custodian."
- **What exists:** static templates and books ([Guardian Clinical Essentials](https://www.guardianclinicalessentials.com/product/professional-will-for-therapists/), [psychotherapistsprofessionalwill.com](https://psychotherapistsprofessionalwill.com/the-professional-will/ethics-codes/)), and resource/consulting sites ([TheraClosure](https://www.theraclosure.com/resources)). **No ongoing service found.**
- **Product:**
  - Guided will builder by state and license type, with a retention schedule.
  - Invite and confirm a professional executor, with an executor dashboard and a signed custodian agreement.
  - Emergency instructions (where records live and which systems to access). **No passwords stored:** it points to password-manager emergency access instead.
  - Client-notification and referral letter templates for the executor.
  - **Annual check-in:** reminders to keep it current. An optional missed-check-in alert to the executor.
- **Money:** $79–129/yr per clinician. Group-practice plan. **Channel:** malpractice insurers, professional associations and supervisors, who could bundle it as risk reduction.
- **Privacy:** stores only the clinician's own information and instructions. No client data.
- **Domains (unchecked):** practicecontinuity.com · myprofessionalwill.com · theraexecutor.com
- **Risks:** low urgency (people procrastinate on wills), so it needs a channel such as insurers or associations. Content must be state-accurate and reviewed by a lawyer.

## 2. CompactMap
The Counseling Compact is live in 9 states with about 31 pending; PSYPACT is mature; the Social Work Compact is activated but not yet issuing ([compactstates.com](https://www.compactstates.com/counseling-compact-states), [telehealth.org](https://telehealth.org/news/cross-state-licensure-expands-but-not-all-compacts-are-ready-for-clinicians/)). Group telehealth practices need to know who can see a client in which state today, with expiry alerts. Competitors: [CompactRoute](https://compactroute.com/) (route planning), Medallion (enterprise credentialing), CE Broker (CE tracking).

## 3. RoomShare
Hourly therapy rooms run about $11–50/hr ([Khospace](https://khospace.com/), [SquareFoot NYC](https://www.squarefoot.com/blog/therapy-office-space-for-rent-nyc/)). Operators exist (TherapyHive, PractiSage, Olida, Peerspace). The narrower gap is host-side software for *group practices* renting idle rooms in the evenings and on weekends.

## 4. RateRaise
Payer rate data exists ([PayerPrice](https://payerprice.com/specialties/mental-health-therapy)); billing firms offer negotiation. Wedge: group-practice rate-increase letters built from public price-transparency files.

## Rejected
Supervision-hour trackers: Supervision Tracker, HourJourney, Miyndsett, HourPath, SparkHours and My LPC Hours. Also anything that stores client information (AI notes, intake, billing, superbills): crowded and HIPAA-heavy.
