# CT-Phish API

A brand-monitoring API that watches Certificate Transparency (CT) log data
for newly-issued certificates on domains that look like typosquats /
lookalikes of a customer's registered brand keywords (e.g. `paypa1.com`,
`secure-mycompany-login.net`), and surfaces those as alerts through a small
REST API.

This is an MVP: it proves the core mechanic end-to-end (register a brand
keyword -> detect lookalike domain -> query it back via API), not a
production SaaS.

## How it works

1. **Register a brand keyword** you want monitored, via `POST /brands`.
2. A **permutation engine** (`permutations.py`, same family of techniques as
   the open-source `dnstwist` tool, implemented from scratch) generates the
   set of lookalike labels for that keyword: character omission, insertion,
   repetition, transposition, QWERTY-adjacent substitution, homoglyph swaps
   (`o`->`0`, `l`->`1`, `rn`->`m`, ...), hyphenation, "combosquat" words
   (`login`, `secure`, `verify`, `account`, ...) glued to the keyword, and
   identical-keyword-different-TLD.
3. An **ingestion pipeline** (`ingest.py`) pulls in observed domains (see
   "data sources" below), classifies each one against every registered
   brand's permutation set (plus a Levenshtein-distance fallback for typos
   the fixed generators miss), and stores matches with a match type and
   confidence score.
4. **Alerts are queryable** via `GET /alerts?brand=...`.

## Data sources (what's real vs. simplified)

The task allowed either a live cert stream, crt.sh polling, or a documented
sample-data fallback. This MVP ships **both** a real crt.sh integration and
a sample-data mode, and is explicit about which is which:

- **`mode=crtsh` (real, live data)** -- queries crt.sh's free public JSON
  search API (`https://crt.sh/?q=%25<keyword>%25&output=json`) once per
  registered brand per cycle, parses the returned certificate identities,
  and runs them through the same classifier. This is real network code
  against a real public data source, not a mock.
  **However:** in the sandboxed environment this MVP was built in, outbound
  HTTPS to `crt.sh` is blocked by the environment's egress proxy policy
  (verified directly: `curl` to `crt.sh:443` returns `403 Forbidden` at the
  proxy's `CONNECT` step). So `mode=crtsh` could not be exercised against
  live internet data during this build -- when you run it yourself on a
  machine with normal internet access, it should work as written. If it
  fails, `POST /ingest/run?mode=crtsh` returns a clear per-brand error
  message rather than silently returning empty results.
- **`mode=sample` (synthetic demo data, clearly labeled)** -- reads
  `sample_data/sample_certs.jsonl`, a small hand-built batch of ~30 domain
  records in the same shape crt.sh/CT logs would produce (domain, issuer,
  timestamp). It mixes ordinary benign domains (`google.com`,
  `sunrise-bakery.com`, ...) with invented lookalike domains covering every
  match type (`paypa1.com`, `secure-paypal.net`, `chase-online.com`,
  `netf1ix.com`, ...). **This is synthetic data made up for this demo, not
  real phishing detections** -- it exists so the full permutation engine
  (including substitution/homoglyph/omission typos that don't contain the
  brand keyword as a literal substring, which crt.sh's substring search
  alone would miss) can be demonstrated end-to-end without live network
  access. Every alert stored from this mode has `source: "sample"` in the
  database and API response, so it's never confused with a live detection.

**Important limitation of crt.sh even when reachable:** crt.sh's public
search is a `LIKE %keyword%` match on certificate identity strings. It
reliably surfaces combosquats, hyphenated variants, prefix/suffix
variants, subdomains, and identical-keyword-different-TLD registrations
(anything that still contains the keyword as a literal substring). It will
**not** surface pure character-substitution or homoglyph typosquats like
`paypa1.com` unless crt.sh happens to also index it under a query that
matches (it won't, since `paypa1` doesn't contain the substring `paypal`).
A production version would need a live cert-stream firehose (e.g. a
certstream-style feed) checked against the full permutation set for that
class of typosquat -- see "what would change for production" below.

## API

- `GET /health` -- liveness check.
- `POST /brands` -- register a brand keyword.
  ```json
  {"keyword": "paypal", "owner": "jasonmitnick45@gmail.com", "legit_domains": ["paypal.com"]}
  ```
  `legit_domains` is optional: domains you already own that would otherwise
  trigger their own "identical keyword" alert are excluded.
- `GET /brands` -- list registered brands.
- `GET /alerts?brand=paypal&match_type=homoglyph&min_confidence=0.8` -- list
  stored alerts, all filters optional.
- `POST /ingest/run?mode=sample|crtsh` -- run one ingestion + matching cycle
  synchronously and return a summary (used for the demo; in a real deployment
  this would run on a schedule instead, see `poller.py`).

## Running it locally

Requires Python 3.9+.

```bash
cd products/ct-phish-api
pip install -r requirements.txt
python3 app.py
```

The API listens on `http://localhost:5000`. It creates a local SQLite file
`ct_phish.db` in this folder on first run (override path with the
`CT_PHISH_DB` env var).

### Demo walkthrough (verified working)

```bash
# register a brand
curl -X POST http://localhost:5000/brands \
  -H "Content-Type: application/json" \
  -d '{"keyword":"paypal","owner":"you@example.com","legit_domains":["paypal.com"]}'

curl -X POST http://localhost:5000/brands \
  -H "Content-Type: application/json" \
  -d '{"keyword":"chase","owner":"you@example.com","legit_domains":["chase.com"]}'

# run the sample-data ingestion pipeline (synthetic demo batch, see note above)
curl -X POST "http://localhost:5000/ingest/run?mode=sample"

# see what got flagged
curl "http://localhost:5000/alerts?brand=paypal"
curl "http://localhost:5000/alerts?min_confidence=0.9"

# try the live crt.sh path too (works on a machine with normal internet access)
curl -X POST "http://localhost:5000/ingest/run?mode=crtsh"
```

Running the sample cycle against `paypal` and `chase` (plus `netflix`)
produces 16 stored alerts spanning every match type (`homoglyph`,
`substitution`, `omission`, `insertion`, `transposition`, `hyphenation`,
`combosquat`, `identical`) and zero false positives on the benign domains
in the sample batch (`google.com`, `github.com`, `stripe.com`, etc.).

### Continuous polling

`poller.py` is a standalone loop for running ingestion on a timer instead of
triggering it by hand:

```bash
python3 poller.py --mode crtsh --interval 300
```

## What's deliberately left out of this MVP

- **No auth, billing, or admin UI** -- not needed to demonstrate the core
  mechanic; the brief explicitly scoped this out.
- **No live cert-stream firehose** -- crt.sh polling (or the sample batch)
  stands in for it; see limitations above.
- **No public suffix list** -- TLD stripping in `permutations.py` is a
  small hardcoded heuristic (handles `.co.uk`-style two-label ccTLDs but not
  the full PSL). Fine at MVP scale, would misparse some edge-case domains.
- **No rate limiting / API keys** -- anyone who can reach the process can
  call every endpoint.
- **No dedup across brands beyond `(brand_id, domain)`** -- if two brands'
  keywords both flag the same domain, it's stored twice (once per brand),
  which is actually correct behavior, just noting it's not deduped further.

## What would need to change to run this as a paid product

- **Live data**: replace/augment crt.sh polling with a real-time CT feed
  (e.g. running your own CT log tailer against the log list, or a
  certstream-style aggregator) so pure character-substitution/homoglyph
  typosquats are caught the moment a cert is issued, not just combosquats
  crt.sh's substring search happens to surface.
- **Rate limits & API keys**: per-customer API keys, request quotas, and
  usage-based or seat-based billing (Stripe) gating `/brands` and `/alerts`.
- **Alerting, not just polling**: webhooks/email/Slack push on new alerts
  instead of requiring the customer to poll `GET /alerts`.
- **Multi-tenant isolation**: brands/alerts scoped to an authenticated
  customer account rather than a single shared table.
- **Postgres instead of SQLite**: once you have concurrent writers (a
  scheduler process + an API process) and more than demo-scale data volume.
- **Public suffix list** (e.g. the `publicsuffix2` library) for correct
  registrable-domain extraction across all ccTLD shapes.
- **False-positive tuning**: confidence scores here are hand-assigned
  per match type; a real product would want feedback loops (customers
  marking alerts as false positives) to recalibrate.
