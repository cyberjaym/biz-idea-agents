# biz-idea-agents

A small Claude Code multi-agent pipeline for going from "find a business idea" to "have a validated MVP with launch copy," using four subagents defined in `.claude/agents/`:

- **researcher** — scans for underserved, high-pain niches and returns 3-5 ranked ideas
- **validator** — stress-tests one idea (market size, competitors, feasibility, distribution) and returns a GO/NO-GO
- **builder** — scaffolds and builds a working MVP for a validated idea
- **copywriter** — writes a one-line pitch, landing page copy, and a cold outreach email

## Usage

In a Claude Code session opened on this repo:

1. Ask for ideas in a domain (or blank slate) — delegates to `researcher`.
2. Pick one idea from the results.
3. Ask to validate it — delegates to `validator` for a GO/NO-GO call.
4. On a GO, ask to build it — delegates to `builder` to scaffold an MVP.
5. Ask for launch copy — delegates to `copywriter` for pitch/landing page/outreach email.

## Gap Scout → Approve → Build → Deploy

A gated pipeline: **Scout** (Phase 1) → **Analyze** (2) → **Propose** (3, hard stop for approval) → **Build** (4) → **Domain + Deploy** (5).
Every run logs sources, scores and decisions to `runs/YYYY-MM-DD/`.

- `config.json`: MODE (`manual` | `auto`), spend caps, auto-build score threshold. Stripe stays in test mode in every mode.
- `.env.example`: every key the pipeline needs. Copy it to `.env.local` (git-ignored; Claude is denied read access via `.claude/settings.json`).
- `scripts/scout_reddit.py`, `scripts/scout_hn.py`: Phase 1 collectors (official Reddit API, HN Algolia).
- `scripts/check_domains.py`: Porkbun availability and price check. Read-only, never registers.
- `scripts/load_env.py`: loads `.env.local` at runtime without printing values.
