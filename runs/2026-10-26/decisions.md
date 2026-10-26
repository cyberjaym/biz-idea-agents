# Run log — 2026-10-26

## Config
- MODE=manual (user instruction: stay in manual for the first few weeks; revisit no earlier than ~2026-11-23).
- MAX_DOMAIN_PRICE=20, MAX_WEEKLY_SPEND=50, MIN_SCORE_TO_AUTOBUILD=8.
- Spend this run: $0. No domains registered. No Stripe objects created.

## Setup done
- `.gitignore` excludes `.env*` (keeps `.env.example`).
- `.claude/settings.json` denies `Read(./.env*)`.
- `config.json`, `.env.example`, `scripts/load_env.py`, `scripts/check_domains.py`, `scripts/scout_reddit.py`, `scripts/scout_hn.py`.

## Blockers (network policy of this cloud environment)
| Source | Result |
|---|---|
| oauth.reddit.com / www.reddit.com | CONNECT 403 (proxy refused); also blocked for WebSearch (`allowed_domains`) |
| hn.algolia.com | CONNECT 403 |
| api.porkbun.com | CONNECT 403 |
| WebFetch (any non-allowlisted host) | DNS failure (ENOTFOUND) |
| WebSearch (server-side) | works; used for this run |

Each failing call was tried once or twice and then stopped, per the "stop after two failures" rule.
Hosts to add under the environment's **Allowed domains**: `oauth.reddit.com`, `www.reddit.com`, `hn.algolia.com`,
`api.porkbun.com`, `api.vercel.com`, `api.supabase.com`, `api.resend.com`, `api.stripe.com`.

## Phase 1 — Scout (preliminary)
- About 35 web searches across SMB, MSP/sysadmin, accounting, real estate/STR, freelancers, ecommerce, consumer/club niches.
- 37 evidence items saved to `evidence.json`. Upvotes are null and quotes come from search snippets (pages could not be opened).
- Most surfaced sources are vendor or comparison blogs. First-person complaint data (Reddit, G2 and app-store reviews) is under-represented.

## Phase 2 — Analyze
- 6 clusters scored and 9 rejected (`scores.json`). Top total is 6.4, below the auto-build threshold of 8.
- Pattern: most 2026 "gaps" already have several fresh entrants. Competition-gap scores are the limiting factor.

## Phase 3 — Propose
- `proposals.md` lists 6 options. HARD STOP. Waiting for the user's selection.
- Domain availability is pending: run `python3 scripts/check_domains.py runs/2026-10-26/domains.json` once Porkbun is reachable.
