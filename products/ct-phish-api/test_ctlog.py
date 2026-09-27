"""
Offline fixture tests for ctlog.py.

This sandbox's outbound network access is restricted to an allowlist (pypi
only) -- it cannot reach any real CT log host (confirmed: a live get-sth call
against oak.ct.letsencrypt.org fails at the egress proxy with a 403 CONNECT
rejection, the same failure mode already documented for crt.sh). So the
get-sth/get-entries HTTP calls in ctlog.py could NOT be exercised against a
real log during this build.

What CAN be verified without network access, and what this file verifies:
  1. The RFC 6962 SS3.4 MerkleTreeLeaf byte-framing parser (parse_merkle_tree_leaf)
     against a hand-built, byte-correct x509_entry leaf.
  2. The PrecertChainEntry extra_data parser (parse_precert_chain_entry)
     against a hand-built precert leaf + extra_data pair.
  3. Domain extraction (extract_domains_from_der / domains_from_get_entries_item)
     against REAL certificates generated locally with the `cryptography`
     library (self-signed, but real DER X.509 structures, not fabricated
     byte blobs) -- proving the parser correctly recovers SANs/CN through
     the full leaf_input -> DER -> x509.Certificate pipeline.
  4. Error handling: truncated/malformed input is rejected with
     MerkleLeafParseError, not silently misparsed.
  5. Incremental polling state (db.get_ctlog_state / set_ctlog_state).

Run with: python3 test_ctlog.py
"""
from __future__ import annotations

import base64
import datetime
import os
import sys
import tempfile

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

import ctlog

FAILURES = []


def check(label: str, condition: bool, detail: str = ""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}" + (f" -- {detail}" if detail and not condition else ""))
    if not condition:
        FAILURES.append(label)


# ---------------------------------------------------------------------------
# Fixture builders: real DER certs via `cryptography`, wrapped in hand-built,
# byte-correct RFC 6962 MerkleTreeLeaf / PrecertChainEntry framing.
# ---------------------------------------------------------------------------

def _build_self_signed_cert(common_name: str, san_dns_names: list[str], poison: bool = False) -> x509.Certificate:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])
    now = datetime.datetime.now(datetime.timezone.utc)
    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(days=1))
        .not_valid_after(now + datetime.timedelta(days=90))
        .add_extension(x509.SubjectAlternativeName([x509.DNSName(n) for n in san_dns_names]), critical=False)
    )
    if poison:
        # RFC 6962 SS3.1 CT poison extension OID, marked critical, so a real
        # verifier would reject this as a final cert -- exactly what marks a
        # "pre-certificate" submitted for an SCT before the real cert issues.
        builder = builder.add_extension(
            x509.UnrecognizedExtension(x509.ObjectIdentifier("1.3.6.1.4.1.11129.2.4.3"), b"\x05\x00"),
            critical=True,
        )
    return builder.sign(key, hashes.SHA256())


def _build_x509_leaf_input(cert_der: bytes, timestamp_ms: int) -> bytes:
    return (
        bytes([0])                                   # version = v1
        + bytes([0])                                 # leaf_type = timestamped_entry
        + timestamp_ms.to_bytes(8, "big")
        + (0).to_bytes(2, "big")                      # entry_type = x509_entry
        + len(cert_der).to_bytes(3, "big") + cert_der  # ASN1Cert<1..2^24-1>
        + (0).to_bytes(2, "big")                      # CtExtensions, empty
    )


def _build_precert_leaf_input(issuer_key_hash: bytes, tbs_der: bytes, timestamp_ms: int) -> bytes:
    assert len(issuer_key_hash) == 32
    return (
        bytes([0])
        + bytes([0])
        + timestamp_ms.to_bytes(8, "big")
        + (1).to_bytes(2, "big")                      # entry_type = precert_entry
        + issuer_key_hash
        + len(tbs_der).to_bytes(3, "big") + tbs_der    # opaque TBSCertificate<1..2^24-1>
        + (0).to_bytes(2, "big")
    )


def _build_precert_extra_data(pre_certificate_der: bytes, chain: list[bytes] | None = None) -> bytes:
    chain = chain or []
    chain_bytes = b"".join(len(c).to_bytes(3, "big") + c for c in chain)
    return (
        len(pre_certificate_der).to_bytes(3, "big") + pre_certificate_der
        + len(chain_bytes).to_bytes(3, "big") + chain_bytes
    )


def _b64_entry(leaf_input: bytes, extra_data: bytes = b"") -> dict:
    return {
        "leaf_input": base64.b64encode(leaf_input).decode(),
        "extra_data": base64.b64encode(extra_data).decode(),
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_x509_entry_roundtrip():
    cert = _build_self_signed_cert("paypa1.com", ["paypa1.com", "www.paypa1.com"])
    cert_der = cert.public_bytes(serialization.Encoding.DER)
    ts_ms = 1_700_000_000_000
    leaf_input = _build_x509_leaf_input(cert_der, ts_ms)
    entry = _b64_entry(leaf_input)

    leaf = ctlog.parse_merkle_tree_leaf(base64.b64decode(entry["leaf_input"]))
    check("x509 leaf: version parsed", leaf["version"] == 0)
    check("x509 leaf: entry_type parsed as x509 (0)", leaf["entry_type"] == 0)
    check("x509 leaf: timestamp round-trips exactly", leaf["timestamp"] == ts_ms)
    check("x509 leaf: embedded cert DER round-trips byte-for-byte", leaf["x509_cert"] == cert_der)

    domains, issuer, cert_seen_at = ctlog.domains_from_get_entries_item(entry)
    check(
        "x509 entry: extracted domains match real SANs",
        domains == sorted({"paypa1.com", "www.paypa1.com"}),
        detail=str(domains),
    )
    check("x509 entry: cert_seen_at derived from leaf timestamp", cert_seen_at.startswith("2023-11-14"))
    check("x509 entry: issuer extracted (self-signed, so == subject CN)", issuer is not None and "paypa1.com" in issuer)


def test_precert_entry_roundtrip():
    # The "pre_certificate" is a real, fully-formed X.509 structure (with the
    # CT poison extension) -- exactly what a log receives for a precert SCT
    # request and what extra_data.PrecertChainEntry.pre_certificate holds.
    precert = _build_self_signed_cert("secure-chase-login.net", ["secure-chase-login.net"], poison=True)
    precert_der = precert.public_bytes(serialization.Encoding.DER)
    tbs_der = precert.tbs_certificate_bytes  # bare TBSCertificate, as would sit in the leaf

    issuer_key_hash = b"\x11" * 32
    ts_ms = 1_700_000_005_000
    leaf_input = _build_precert_leaf_input(issuer_key_hash, tbs_der, ts_ms)
    extra_data = _build_precert_extra_data(precert_der)
    entry = _b64_entry(leaf_input, extra_data)

    leaf = ctlog.parse_merkle_tree_leaf(base64.b64decode(entry["leaf_input"]))
    check("precert leaf: entry_type parsed as precert (1)", leaf["entry_type"] == 1)
    check("precert leaf: issuer_key_hash round-trips", leaf["issuer_key_hash"] == issuer_key_hash)
    check("precert leaf: tbs_certificate bytes round-trip exactly", leaf["tbs_certificate"] == tbs_der)

    recovered_pre_cert = ctlog.parse_precert_chain_entry(base64.b64decode(entry["extra_data"]))
    check("precert extra_data: pre_certificate DER round-trips byte-for-byte", recovered_pre_cert == precert_der)

    domains, issuer, cert_seen_at = ctlog.domains_from_get_entries_item(entry)
    check(
        "precert entry: extracted domain matches real SAN (via extra_data, not bare tbs)",
        domains == ["secure-chase-login.net"],
        detail=str(domains),
    )


def test_malformed_input_rejected():
    try:
        ctlog.parse_merkle_tree_leaf(bytes([9, 0]) + b"\x00" * 10)  # bad version
        check("malformed: bad version rejected", False)
    except ctlog.MerkleLeafParseError:
        check("malformed: bad version rejected", True)

    try:
        ctlog.parse_merkle_tree_leaf(bytes([0, 0]))  # truncated, no timestamp
        check("malformed: truncated buffer rejected", False)
    except ctlog.MerkleLeafParseError:
        check("malformed: truncated buffer rejected", True)

    # trailing garbage after an otherwise-valid x509 leaf
    cert = _build_self_signed_cert("example.com", ["example.com"])
    cert_der = cert.public_bytes(serialization.Encoding.DER)
    leaf_input = _build_x509_leaf_input(cert_der, 1_700_000_000_000) + b"\xff\xff\xff"
    try:
        ctlog.parse_merkle_tree_leaf(leaf_input)
        check("malformed: trailing bytes rejected", False)
    except ctlog.MerkleLeafParseError:
        check("malformed: trailing bytes rejected", True)


def test_incremental_state_tracking():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.environ["CT_PHISH_DB"] = path
    try:
        import importlib
        import db as db_module
        importlib.reload(db_module)
        db_module.init_db()

        log_url = "https://example-log.test"
        check("ctlog_state: unseen log starts at -1", db_module.get_ctlog_state(log_url) == -1)

        db_module.set_ctlog_state(log_url, 499)
        check("ctlog_state: stores progress", db_module.get_ctlog_state(log_url) == 499)

        db_module.set_ctlog_state(log_url, 999)
        check("ctlog_state: advances on re-poll (upsert, not duplicate row)", db_module.get_ctlog_state(log_url) == 999)

        conn = db_module.get_conn()
        try:
            count = conn.execute(
                "SELECT COUNT(*) AS c FROM ctlog_state WHERE log_url = ?", (log_url,)
            ).fetchone()["c"]
        finally:
            conn.close()
        check("ctlog_state: exactly one row per log_url", count == 1)
    finally:
        os.remove(path)
        del os.environ["CT_PHISH_DB"]


if __name__ == "__main__":
    test_x509_entry_roundtrip()
    test_precert_entry_roundtrip()
    test_malformed_input_rejected()
    test_incremental_state_tracking()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S): {FAILURES}")
        sys.exit(1)
    print("All offline fixture tests passed.")
