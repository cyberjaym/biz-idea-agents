# Gap Scout — run 13: fresh 2027 rule changes (2026-10-27k)

**Status: HARD STOP.** MODE=manual. $0 spent. Domains unchecked.

Method: only changes **announced in Aug–Oct 2026** with **2027 effective dates**, before the copycat wave arrives.

| # | Name | Total | D | W | G | B | Dist | One line |
|---|------|------:|--:|--:|--:|--:|--:|---|
| 1 | **FCCReady** | 6.6 | 6 | 7 | **8** | 7 | 5 | Find, verify and attach FCC IDs for electronics listings before the 2027 marketplace deadlines |
| 2 | EWS Rescue | 6.0 | 7 | 8 | 5 | 4 | 6 | Keep old Outlook-connected business apps working after Microsoft switches off Exchange Web Services on Apr 1, 2027 |

## 1. FCCReady — the highest gap score of any run
- **The rule:** FCC order 26-50 (Sept 2026; [FCC](https://docs.fcc.gov/public/attachments/FCC-26-50A1.pdf), [Wiley](https://www.wiley.law/alert-FCC-Expands-Covered-List-Prohibitions-to-Devices-with-Certain-Logic-Bearing-Hardware-Components-Imposes-Compliance-Obligations-on-Online-Marketplaces)). Online marketplaces must show a device's FCC ID at the point of sale:
  - **Mar 1, 2027** for devices they sell from their own inventory.
  - **Jun 1, 2027** for third-party listings, where the marketplace verifies the ID is validly issued and the **seller certifies** it is accurate.
  - Exempt: low-volume sellers (under about 200 sales / $5k) and used devices. Listings made before Oct 13, 2026 are exempt until edited ([Seller Essentials](https://selleressentials.com/ebay-fcc-id-requirement/)).
  - Sellers are already confused ([eBay Community thread](https://community.ebay.com/forum/selling-57920/topic/fcc-id-clarification-for-used-listings-485019/)).
- **Gap:** searches found **no compliance tool**. Verification runs against the FCC's public equipment-authorization database and the Covered List (banned equipment makers, now extended to components).
- **Product, two sides:**
  - **Sellers** (high-volume electronics sellers on eBay, Amazon, Walmart, Reverb, TikTok Shop, Newegg): upload a catalog CSV. AI matches each brand and model to its FCC ID, checks it against the FCC database and the Covered List, and outputs listing-ready IDs plus a certification record. $49–199/mo by number of products.
  - **Mid-size marketplaces** (Reverb, Bonanza, Mercari, regional platforms): a verification API called at listing time, priced per check.
- **Build:** 6 days. The FCC database is public; the AI does the brand/model-to-ID matching.
- **Domains (unchecked):** fccready.com · fccidcheck.com · fccready.app
- **Risks:** narrow audience. Amazon and eBay may build verification in, which would leave sellers needing only the lookup. Matching accuracy on generic or unbranded imports. Rules could be amended.

## 2. EWS Rescue
- **Problem:** Microsoft began disabling Exchange Web Services Oct 1, 2026; it is permanently off **Apr 1, 2027, with no exceptions** ([4sysops](https://4sysops.com/archives/exchange-web-services-retirement-in-exchange-online-timeline-and-migration-to-microsoft-graph-api/)). Older business apps that read or send Outlook mail through it will break.
- **Competition:** [EWS Bridge](https://ewsbridge.com/) already sells a translation layer that converts EWS calls to Microsoft's newer API. Migration consultants.
- **Angle:** an MSP inventory and risk report across client tenants, plus a done-for-you migration service. Building a full bridge is hard (B=4).

## Excluded / rejected
- **California sales tax on software subscriptions (Jan 2027):** big, fresh demand, but the **tax category is excluded** per your instruction. Say the word if you want it back in.
- **Rejected:** the FCC rule on revoking consent for texts and calls (messaging platforms handle it), California's new privacy-deletion law SB 923 (privacy tools crowded), Android developer verification, OpenAI model retirements, California 2027 employment laws.
