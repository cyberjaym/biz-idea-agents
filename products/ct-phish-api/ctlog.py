"""
Real RFC 6962 Certificate Transparency log tailer.

Unlike crt.sh (a third-party aggregator with its own uptime/coverage), this
module talks directly to a CT log's own public HTTP API -- the standing
infrastructure every CT log is required to expose per RFC 6962 -- to pull
newly-appended entries and extract the domains from their certificates.

Two HTTP calls are used:

  - GET {base}/ct/v1/get-sth
      Returns the log's current "signed tree head", including `tree_size`
      (how many entries the log currently has). Used to find out how much
      new data is available.

  - GET {base}/ct/v1/get-entries?start=X&end=Y
      Returns raw log entries in the range [X, Y] (inclusive). Each entry is
      a base64-encoded `MerkleTreeLeaf` (`leaf_input`) plus `extra_data`
      (chain material). This is NOT pre-parsed JSON of the certificate --
      it's the raw TLS-encoded structure defined in RFC 6962 SS3.4, which this
      module unwraps by hand before handing bytes to a real X.509 parser.

Target log: this defaults to a single currently-qualified CT log (Sectigo's
"Sabre" log, chosen because unlike Let's Encrypt's Oak/temporal-shard logs it
is not year-sharded and so doesn't need a URL change every deployment). CT
logs do get decommissioned/replaced over time, so the base URL is fully
configurable via the CT_LOG_BASE_URL env var -- **before running this in
production, verify the target log is still listed as qualified/usable in
Google's canonical log list** (https://www.gstatic.com/ct/log_list/v3/log_list.json)
and point CT_LOG_BASE_URL at whichever log you choose. This code was written
and unit-tested against the RFC 6962 wire format in a sandbox with no
outbound access to any CT log host, so the live get-sth/get-entries calls
below have NOT been exercised against a real log -- see README for exactly
what was and wasn't verified.
"""
from __future__ import annotations

import base64
from datetime import datetime, timezone

import requests
from cryptography import x509

DEFAULT_BASE_URL = "https://sabre.ct.comodo.com"
GET_STH_PATH = "/ct/v1/get-sth"
GET_ENTRIES_PATH = "/ct/v1/get-entries"
REQUEST_TIMEOUT_SECONDS = 20

# RFC 6962 SS3.4 constants
_VERSION_V1 = 0
_LEAF_TYPE_TIMESTAMPED_ENTRY = 0
_ENTRY_TYPE_X509 = 0
_ENTRY_TYPE_PRECERT = 1


class MerkleLeafParseError(ValueError):
    """A get-entries item didn't parse as a well-formed RFC 6962 MerkleTreeLeaf."""


# ---------------------------------------------------------------------------
# Low-level TLS presentation-language helpers (RFC 5246 SS4 vector encoding:
# a fixed-width big-endian length prefix followed by that many content bytes)
# ---------------------------------------------------------------------------

def _read_uint(data: bytes, offset: int, length: int) -> tuple[int, int]:
    if offset + length > len(data):
        raise MerkleLeafParseError(f"truncated data reading {length}-byte uint at offset {offset}")
    value = int.from_bytes(data[offset:offset + length], "big")
    return value, offset + length


def _read_fixed(data: bytes, offset: int, length: int) -> tuple[bytes, int]:
    if offset + length > len(data):
        raise MerkleLeafParseError(f"truncated data reading {length} fixed bytes at offset {offset}")
    return data[offset:offset + length], offset + length


def _read_opaque(data: bytes, offset: int, len_bytes: int) -> tuple[bytes, int]:
    """Read a TLS `opaque vector<...>`: an N-byte big-endian length prefix
    followed by that many bytes of content."""
    length, offset = _read_uint(data, offset, len_bytes)
    return _read_fixed(data, offset, length)


# ---------------------------------------------------------------------------
# RFC 6962 SS3.4 MerkleTreeLeaf parsing
# ---------------------------------------------------------------------------

def parse_merkle_tree_leaf(leaf_input: bytes) -> dict:
    """Parse the raw bytes of a `leaf_input` field (already base64-decoded)
    into its RFC 6962 SS3.4 MerkleTreeLeaf / TimestampedEntry fields.

    struct {
        Version version;                    // 1 byte, v1 = 0
        MerkleLeafType leaf_type;           // 1 byte, timestamped_entry = 0
        select(leaf_type) {
            case timestamped_entry: TimestampedEntry;
        } leaf;
    } MerkleTreeLeaf;

    struct {
        uint64 timestamp;                   // 8 bytes, ms since epoch
        LogEntryType entry_type;            // 2 bytes, x509_entry=0 / precert_entry=1
        select(entry_type) {
            case x509_entry:   ASN1Cert;               // opaque<1..2^24-1>
            case precert_entry: PreCert;                // issuer_key_hash[32] + opaque tbs<1..2^24-1>
        } signed_entry;
        CtExtensions extensions;            // opaque<0..2^16-1>
    } TimestampedEntry;

    Returns a dict with: version, leaf_type, timestamp (int, ms), entry_type,
    and either "x509_cert" (DER bytes) or ("issuer_key_hash", "tbs_certificate").
    Raises MerkleLeafParseError on any structural mismatch (wrong version/type,
    truncated buffer, trailing bytes left over).
    """
    offset = 0
    version, offset = _read_uint(leaf_input, offset, 1)
    if version != _VERSION_V1:
        raise MerkleLeafParseError(f"unsupported MerkleTreeLeaf version {version} (expected v1=0)")

    leaf_type, offset = _read_uint(leaf_input, offset, 1)
    if leaf_type != _LEAF_TYPE_TIMESTAMPED_ENTRY:
        raise MerkleLeafParseError(f"unsupported MerkleLeafType {leaf_type} (expected timestamped_entry=0)")

    timestamp, offset = _read_uint(leaf_input, offset, 8)
    entry_type, offset = _read_uint(leaf_input, offset, 2)

    result = {"version": version, "leaf_type": leaf_type, "timestamp": timestamp, "entry_type": entry_type}

    if entry_type == _ENTRY_TYPE_X509:
        cert_der, offset = _read_opaque(leaf_input, offset, 3)  # ASN1Cert<1..2^24-1>
        result["x509_cert"] = cert_der
    elif entry_type == _ENTRY_TYPE_PRECERT:
        issuer_key_hash, offset = _read_fixed(leaf_input, offset, 32)
        tbs_cert, offset = _read_opaque(leaf_input, offset, 3)  # opaque TBSCertificate<1..2^24-1>
        result["issuer_key_hash"] = issuer_key_hash
        result["tbs_certificate"] = tbs_cert
    else:
        raise MerkleLeafParseError(f"unknown LogEntryType {entry_type} (expected 0=x509 or 1=precert)")

    # CtExtensions extensions<0..2^16-1> -- unused here, but consumed so we
    # can verify the buffer is fully and correctly framed (no trailing bytes).
    extensions, offset = _read_opaque(leaf_input, offset, 2)
    result["extensions"] = extensions

    if offset != len(leaf_input):
        raise MerkleLeafParseError(
            f"{len(leaf_input) - offset} trailing bytes left over after parsing MerkleTreeLeaf"
        )
    return result


def parse_precert_chain_entry(extra_data: bytes) -> bytes:
    """Parse the `extra_data` of a precert get-entries item:

    struct {
        ASN1Cert pre_certificate;              // opaque<1..2^24-1>
        ASN1Cert certificate_chain<0..2^24-1>; // vector of opaque<1..2^24-1>, overall<0..2^24-1>
    } PrecertChainEntry;

    Returns the DER bytes of `pre_certificate` -- the actual certificate
    structure (poison extension included) that was submitted to get the SCT.
    This is a real, fully-parseable X.509 Certificate (unlike the bare
    TBSCertificate bytes embedded in the MerkleTreeLeaf itself, which lack
    the outer SEQUENCE/signature and so are not independently parseable as a
    Certificate) -- so it's what we hand to the X.509 parser for precerts.
    """
    pre_certificate, _offset = _read_opaque(extra_data, 0, 3)
    return pre_certificate


# ---------------------------------------------------------------------------
# X.509 -> domain extraction (real cryptography library, no hand-rolled ASN.1)
# ---------------------------------------------------------------------------

def extract_domains_from_der(der_bytes: bytes) -> list[str]:
    """Load a DER-encoded X.509 certificate and return every domain name it
    asserts (Subject Alternative Name DNSNames, plus Subject Common Name if
    it looks like a hostname), lowercased and deduplicated."""
    cert = x509.load_der_x509_certificate(der_bytes)
    domains: set[str] = set()

    try:
        for attr in cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME):
            value = str(attr.value).strip().lower()
            if value and "." in value:
                domains.add(value)
    except Exception:
        pass

    try:
        san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        for name in san.value.get_values_for_type(x509.DNSName):
            name = name.strip().lower()
            if name:
                domains.add(name)
    except x509.ExtensionNotFound:
        pass

    return sorted(domains)


def domains_from_get_entries_item(entry: dict) -> tuple[list[str], str | None, str | None]:
    """Given one raw item from a get-entries response ({"leaf_input": b64,
    "extra_data": b64}), return (domains, issuer_name, cert_seen_at_iso).

    Unwraps the MerkleTreeLeaf per RFC 6962 SS3.4, then for x509 entries parses
    the embedded certificate directly, and for precert entries parses the
    pre_certificate out of extra_data's PrecertChainEntry (see
    parse_precert_chain_entry for why).
    """
    leaf_input = base64.b64decode(entry["leaf_input"])
    leaf = parse_merkle_tree_leaf(leaf_input)
    cert_seen_at = datetime.fromtimestamp(leaf["timestamp"] / 1000.0, tz=timezone.utc).isoformat()

    if leaf["entry_type"] == _ENTRY_TYPE_X509:
        der = leaf["x509_cert"]
    else:
        extra_data = base64.b64decode(entry.get("extra_data") or "")
        der = parse_precert_chain_entry(extra_data)

    cert = x509.load_der_x509_certificate(der)
    domains = extract_domains_from_der(der)
    try:
        issuer = cert.issuer.rfc4514_string()
    except Exception:
        issuer = None
    return domains, issuer, cert_seen_at


# ---------------------------------------------------------------------------
# RFC 6962 HTTP client (get-sth / get-entries)
# ---------------------------------------------------------------------------

def fetch_sth(base_url: str) -> dict:
    """GET {base_url}/ct/v1/get-sth -- the log's current signed tree head.
    Raises requests.RequestException on network/HTTP failure (not caught
    here -- same "surface the real error" contract as fetch_from_crtsh)."""
    resp = requests.get(base_url.rstrip("/") + GET_STH_PATH, timeout=REQUEST_TIMEOUT_SECONDS)
    resp.raise_for_status()
    return resp.json()


def fetch_entries(base_url: str, start: int, end: int) -> list[dict]:
    """GET {base_url}/ct/v1/get-entries?start=X&end=Y (inclusive range).
    Logs may return fewer entries than requested (their own batch cap) --
    caller should use the actual returned count, not assume end-start+1."""
    resp = requests.get(
        base_url.rstrip("/") + GET_ENTRIES_PATH,
        params={"start": start, "end": end},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    resp.raise_for_status()
    return resp.json().get("entries", [])
