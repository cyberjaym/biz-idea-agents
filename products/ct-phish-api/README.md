# CT-Phish API

A brand-monitoring API that watches Certificate Transparency (CT) log data
for newly-issued certificates on domains that look like typosquats /
lookalikes of a customer's registered brand keywords (e.g. `paypa1.com`,
`secure-mycompany-login.net`), and surfaces those as alerts through a small
REST API.

This is an MVP: it proves the core mechanic end-to-end (register a brand
keyword -> detect lookalike domain -> query it back via API), not a
production SaaS.

Three ingestion modes exist: `sample` (synthetic demo batch), `crtsh` (live
query against crt.sh's public search API), and `ctlog` (a real RFC 6962
tailer against a live CT log's own `get-sth`/`get-entries` HTTP API, added
specifically to close the gap crt.sh's substring search can't: pure
character-substitution/homoglyph typosquats like `paypa1.com`). See "Data
sources" below for exactly what's real, what's synthetic, and what could and
couldn't be verified live in the sandbox this was built in.

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
- **`mode=ctlog` (real, live data, direct CT log protocol)** -- tails a
  single live Certificate Transparency log directly via its own public
  RFC 6962 HTTP API (`get-sth` + `get-entries`), the standing infrastructure
  every qualified CT log is required to expose, rather than depending on a
  third-party aggregator's uptime/coverage (crt.sh and certstream-style
  broadcasters are both single points of failure outside our control). This
  is the mode that can actually catch pure character-substitution/homoglyph
  typosquats crt.sh's substring search structurally cannot, because it
  inspects every certificate the log emits instead of searching for a
  keyword match. See "**mode=ctlog details**" below for exactly how it
  works, what was verified offline, and what could not be tested live in
  this sandbox.
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
`mode=ctlog` (below) is this MVP's answer to that gap: it inspects every
certificate a log emits rather than searching for a keyword substring, so it
would catch `paypa1.com` regardless of what string it contains.

## mode=ctlog details

`ctlog.py` implements a real RFC 6962 client and parser:

- **HTTP API**: `GET {base}/ct/v1/get-sth` returns the log's current tree
  size; `GET {base}/ct/v1/get-entries?start=X&end=Y` returns raw log entries
  in that range. No third-party aggregator sits in between -- this talks to
  the log itself.
- **Target log**: defaults to Sectigo's "Sabre" log
  (`https://sabre.ct.comodo.com`), chosen because (unlike Let's Encrypt's
  Oak/temporal-shard logs) it isn't year-sharded, so the default URL doesn't
  need updating every deployment. **CT logs do get decommissioned or
  replaced over time** -- before relying on this in production, check
  Google's canonical qualified-log list
  (`https://www.gstatic.com/ct/log_list/v3/log_list.json`) and point the
  `CT_LOG_BASE_URL` env var at whichever log(s) you choose. The base URL is
  never hardcoded into logic that assumes it won't change.
- **Parsing**: a `get-entries` item is `{"leaf_input": base64, "extra_data":
  base64}`. `leaf_input` is a TLS-encoded `MerkleTreeLeaf` (RFC 6962 SS3.4) --
  1-byte version, 1-byte leaf type, 8-byte timestamp, 2-byte entry type, then
  either a length-prefixed X.509 certificate (`x509_entry`) or a 32-byte
  issuer key hash + length-prefixed bare `TBSCertificate` (`precert_entry`),
  followed by a length-prefixed extensions field. `ctlog.py` unwraps this
  framing by hand (`parse_merkle_tree_leaf`) -- it is not "just call an X.509
  library on the raw bytes." For `x509_entry`, the embedded DER certificate
  is handed straight to `cryptography`'s `x509.load_der_x509_certificate`.
  For `precert_entry`, the bare `TBSCertificate` bytes in the leaf aren't
  independently parseable as a `Certificate` (no outer SEQUENCE/signature),
  so instead the actual submitted pre-certificate (a real, fully-parseable
  X.509 structure containing the CT poison extension) is recovered from
  `extra_data`'s `PrecertChainEntry.pre_certificate` field and parsed the
  same way. Domains are read from the parsed certificate's Subject
  Alternative Names (and Common Name as a fallback) and fed into the same
  `classify_domain` pipeline the other modes use.
- **Incremental polling**: `db.ctlog_state` stores `last_processed_index`
  per log URL. Each cycle calls `get-sth` for the current tree size, then
  fetches only entries after the last recorded index (`get-entries?start=
  last+1&end=...`), so repeated polls never re-fetch old data. First poll
  against a log starts at index 0.
- **Rate/volume handling (MVP limitation, stated plainly)**: each cycle
  fetches at most `CT_LOG_BATCH_SIZE` entries (default 500, env-configurable)
  from a single log. Real CT logs receive many entries per second across all
  qualified logs combined; a bounded, single-log, synchronous poll like this
  cannot keep up with full CT volume and will fall further behind the
  further it lags. This is fine for an MVP demo of the mechanic, not for a
  product promising real-time coverage -- see "what would need to change"
  below.
- **What was verified offline (this sandbox has no route to any real CT log
  host)**: `test_ctlog.py` builds real DER X.509 certificates locally with
  the `cryptography` library (self-signed, but genuine ASN.1 structures, not
  fabricated byte blobs), wraps them in hand-built, byte-correct
  `MerkleTreeLeaf`/`PrecertChainEntry` framing exactly as a real log's
  `get-entries` response would, and asserts: the leaf-framing parser
  recovers the exact original bytes/timestamp for both `x509_entry` and
  `precert_entry` leaves; domain extraction returns the exact SANs on the
  real certificate for both entry types (including the precert path that
  requires reading `extra_data`, not the bare `tbs_certificate`); and
  malformed input (bad version, truncated buffer, trailing bytes) is
  rejected with a clear error rather than silently misparsed. Also verified:
  `db.ctlog_state` correctly starts an unseen log at index -1, upserts
  (not duplicates) on repeated polls, and stores exactly one row per log
  URL. Run it yourself: `python3 test_ctlog.py` (19/19 checks passed as of
  this build).
- **What could NOT be verified live**: the actual `get-sth`/`get-entries`
  HTTP calls in `ctlog.py` against a real CT log host. Confirmed directly --
  `POST /ingest/run?mode=ctlog` returns a clean per-cycle error
  (`ctlog request failed (https://sabre.ct.comodo.com): ... Tunnel
  connection failed: 403 Forbidden`) with no fabricated fallback data,
  because this sandbox's egress proxy rejects the `CONNECT` to
  `sabre.ct.comodo.com:443` the same way it already rejected `crt.sh:443`
  for `mode=crtsh`. On a machine with normal internet access, this should
  work as written against whatever log `CT_LOG_BASE_URL` points at -- but
  that end-to-end path (real network response shape, real tree growth over
  time, log-specific quirks) has not actually been exercised.

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
- `POST /ingest/run?mode=sample|crtsh|ctlog` -- run one ingestion + matching
  cycle synchronously and return a summary (used for the demo; in a real
  deployment this would run on a schedule instead, see `poller.py`).

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

# try the live CT-log tailer (works on a machine with normal internet access;
# override CT_LOG_BASE_URL to point at a different qualified log)
curl -X POST "http://localhost:5000/ingest/run?mode=ctlog"
```

Run the offline parser fixture tests (no network required):

```bash
python3 test_ctlog.py
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
python3 poller.py --mode ctlog --interval 60
```

## What's deliberately left out of this MVP

- **No auth, billing, or admin UI** -- not needed to demonstrate the core
  mechanic; the brief explicitly scoped this out.
- **`mode=ctlog` only tails one CT log, in small bounded batches** -- no
  single CT log sees every certificate issued (each CA typically submits to
  several logs, and different CAs use different logs), and a real deployment
  needs a high-throughput consumer, not a bounded synchronous poll. See
  "mode=ctlog details" above and "what would need to change" below.
- **No public suffix list** -- TLD stripping in `permutations.py` is a
  small hardcoded heuristic (handles `.co.uk`-style two-label ccTLDs but not
  the full PSL). Fine at MVP scale, would misparse some edge-case domains.
- **No rate limiting / API keys** -- anyone who can reach the process can
  call every endpoint.
- **No dedup across brands beyond `(brand_id, domain)`** -- if two brands'
  keywords both flag the same domain, it's stored twice (once per brand),
  which is actually correct behavior, just noting it's not deduped further.

## What would need to change to run this as a paid product

- **Multi-log coverage**: run `mode=ctlog`-style tailing against every
  currently-qualified log in Google's log list in parallel (not just one),
  since no single log sees every certificate -- different CAs submit to
  different logs, and a domain's cert might only appear in one of them.
- **Real throughput, not a bounded synchronous poll**: replace the
  "fetch up to 500 entries per HTTP call" loop with a proper queue/worker
  setup (e.g. a dedicated consumer process per log pushing entries onto a
  queue, with worker processes doing the parse-and-classify step) that can
  sustain real CT log volume (many entries/second across all logs) without
  falling behind. `get-entries` should also be paginated continuously rather
  than run on a fixed interval.
- **Verify the target log(s) are still qualified**: CT logs get decommissioned
  over time; a production deployment needs to periodically re-check
  `log_list.json` and add/retire logs, not hardcode one log's URL forever.
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
