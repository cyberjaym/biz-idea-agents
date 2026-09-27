"""
Ingestion pipeline: pull newly-issued certificate domains and match them
against registered brand keywords using permutations.py.

Two source modes:

  - "crtsh":   real, live query against crt.sh's free public JSON search API
               (https://crt.sh/?q=...&output=json), one query per registered
               brand keyword per cycle. This is REAL data when it runs
               somewhere with outbound internet access. crt.sh has no
               "firehose of every cert issued" endpoint for the public tier,
               so this only surfaces certs whose identity string loosely
               contains the keyword (crt.sh does a SQL LIKE match) -- see
               README for what this does and doesn't catch.

  - "sample":  reads sample_data/sample_certs.jsonl, a small hand-built batch
               of domains (mix of real-looking benign domains and invented
               lookalike domains covering every permutation type). This
               simulates a firehose of "newly observed" certificate domains
               so the full permutation engine (including character
               substitution / homoglyph / omission typosquats that don't
               contain the brand keyword as a substring) can be demonstrated
               end-to-end without live network access. It is synthetic
               demo data and is always labeled with source="sample".
"""
from __future__ import annotations

import json
import os
import time

import requests

import db
from permutations import generate_label_permutations, classify_domain

CRTSH_URL = "https://crt.sh/"
CRTSH_TIMEOUT_SECONDS = 20
SAMPLE_FILE = os.path.join(os.path.dirname(__file__), "sample_data", "sample_certs.jsonl")

_permutation_cache: dict[str, dict] = {}


def _permutations_for(keyword: str) -> dict:
    if keyword not in _permutation_cache:
        _permutation_cache[keyword] = generate_label_permutations(keyword)
    return _permutation_cache[keyword]


def fetch_from_crtsh(keyword: str) -> list[dict]:
    """Query crt.sh for certificate identities loosely matching `keyword`.

    Returns a list of {"domain", "issuer", "cert_seen_at"} dicts, deduped by
    domain. Raises requests.RequestException on network/HTTP failure -- the
    caller is expected to surface this rather than silently returning [].
    """
    params = {"q": f"%{keyword}%", "output": "json"}
    headers = {"User-Agent": "ct-phish-api-mvp/0.1 (+https://github.com/)"}
    resp = requests.get(CRTSH_URL, params=params, headers=headers, timeout=CRTSH_TIMEOUT_SECONDS)
    resp.raise_for_status()
    entries = resp.json()

    seen: dict[str, dict] = {}
    for entry in entries:
        raw_names = entry.get("name_value", "") or ""
        issuer = entry.get("issuer_name")
        seen_at = entry.get("entry_timestamp")
        for name in raw_names.split("\n"):
            name = name.strip().lower()
            if not name or name in seen:
                continue
            seen[name] = {"domain": name, "issuer": issuer, "cert_seen_at": seen_at}
    return list(seen.values())


def fetch_from_sample() -> list[dict]:
    records = []
    with open(SAMPLE_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def _process_domain_against_brand(domain_record: dict, brand: dict, source: str) -> dict | None:
    domain = domain_record["domain"]
    keyword = brand["keyword"]

    if domain in brand.get("legit_domains", []):
        return None  # the brand's own known-good domain, not an alert

    perm_set = _permutations_for(keyword)
    result = classify_domain(domain, keyword, perm_set)
    if not result:
        return None
    match_type, confidence, matched_label = result

    inserted = db.insert_alert(
        brand_id=brand["id"],
        brand_keyword=keyword,
        domain=domain,
        match_type=match_type,
        confidence=confidence,
        source=source,
        issuer=domain_record.get("issuer"),
        cert_seen_at=domain_record.get("cert_seen_at"),
    )
    return {
        "domain": domain,
        "brand": keyword,
        "match_type": match_type,
        "confidence": confidence,
        "new": inserted,
    }


def run_ingest_cycle(mode: str = "sample") -> dict:
    """Run one ingestion + matching pass. Returns a summary dict.

    mode="sample" -> full permutation engine against the bundled sample batch,
                      checked against every registered brand.
    mode="crtsh"  -> one live crt.sh substring query per registered brand.
    """
    brands = db.list_brands()
    if not brands:
        return {"mode": mode, "brands_checked": 0, "domains_checked": 0, "new_alerts": 0, "matches": []}

    matches = []
    domains_checked = 0

    if mode == "sample":
        records = fetch_from_sample()
        domains_checked = len(records)
        for record in records:
            for brand in brands:
                m = _process_domain_against_brand(record, brand, source="sample")
                if m:
                    matches.append(m)

    elif mode == "crtsh":
        for brand in brands:
            try:
                records = fetch_from_crtsh(brand["keyword"])
            except requests.RequestException as exc:
                matches.append({"brand": brand["keyword"], "error": f"crt.sh request failed: {exc}"})
                continue
            domains_checked += len(records)
            for record in records:
                m = _process_domain_against_brand(record, brand, source="crtsh")
                if m:
                    matches.append(m)
            time.sleep(1)  # be polite to the free public endpoint

    else:
        raise ValueError(f"unknown mode: {mode}")

    new_alerts = sum(1 for m in matches if m.get("new"))
    return {
        "mode": mode,
        "brands_checked": len(brands),
        "domains_checked": domains_checked,
        "new_alerts": new_alerts,
        "matches": matches,
    }
