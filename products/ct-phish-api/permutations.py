"""
Typosquat / domain-permutation engine.

Implements the same family of techniques as the open-source `dnstwist` tool,
written from scratch (no dependency on dnstwist itself):

  - omission        drop one character                (paypal -> paypl)
  - insertion       insert one character               (paypal -> paypall)
  - repetition      double a character                 (paypal -> paypaal)
  - transposition   swap two adjacent characters        (paypal -> payapl)
  - substitution    swap a char for a QWERTY neighbor   (paypal -> paupal)
  - homoglyph       swap visually-similar chars/digits  (paypal -> paypa1)
  - hyphenation     insert a hyphen between letters      (paypal -> pay-pal)
  - combosquat      keyword + a suspicious trigger word (paypal-login, secure-paypal)
  - tld_swap        identical keyword, different TLD    (paypal.net instead of paypal.com)

`generate_label_permutations(keyword)` returns {candidate_label: match_type},
computed once per brand keyword and cached by the caller.

`classify_domain(domain, keyword, permutation_set)` decides whether an
*observed* registrable domain (e.g. from a certificate) is a lookalike for a
brand keyword, returning (match_type, confidence) or None.
"""
from __future__ import annotations

import re
import string

QWERTY_ADJACENT = {
    "a": "qwsz", "b": "vghn", "c": "xdfv", "d": "ersfcx", "e": "wsdr",
    "f": "drtgvc", "g": "ftyhbv", "h": "gyujnb", "i": "ujko", "j": "huikmn",
    "k": "jiolm", "l": "kop", "m": "njk", "n": "bhjm", "o": "iklp",
    "p": "ol", "q": "wa", "r": "edft", "s": "awedxz", "t": "rfgy",
    "u": "yhji", "v": "cfgb", "w": "qase", "x": "zsdc", "y": "tghu", "z": "asx",
}

# single-character (and a couple of 2-char) homoglyph swaps commonly seen in
# real-world phishing registrations
HOMOGLYPH_MAP = {
    "o": "0", "0": "o",
    "l": "1", "1": "l",
    "i": "1",
    "e": "3", "3": "e",
    "a": "4", "4": "a",
    "s": "5", "5": "s",
    "g": "9",
    "b": "8",
    "u": "v",
}
HOMOGLYPH_MULTICHAR = {
    "rn": "m",
    "vv": "w",
    "cl": "d",
    "m": "rn",
}

COMBOSQUAT_WORDS = [
    "secure", "login", "verify", "account", "support", "signin", "update",
    "service", "online", "mobile", "app", "id", "pay", "wallet", "confirm",
    "help", "portal", "my", "billing", "alert", "auth",
]

COMMON_TLDS = [
    "com", "net", "org", "info", "biz", "co", "cc", "top", "xyz",
    "online", "site", "shop", "live", "click", "vip",
]


def _omissions(kw: str):
    for i in range(len(kw)):
        yield kw[:i] + kw[i + 1:], "omission"


def _insertions(kw: str):
    for i in range(len(kw) + 1):
        for c in string.ascii_lowercase:
            yield kw[:i] + c + kw[i:], "insertion"


def _repetitions(kw: str):
    for i, ch in enumerate(kw):
        yield kw[:i] + ch + kw[i:], "repetition"


def _transpositions(kw: str):
    for i in range(len(kw) - 1):
        chars = list(kw)
        chars[i], chars[i + 1] = chars[i + 1], chars[i]
        yield "".join(chars), "transposition"


def _substitutions(kw: str):
    for i, ch in enumerate(kw):
        for c in QWERTY_ADJACENT.get(ch, ""):
            yield kw[:i] + c + kw[i + 1:], "substitution"


def _homoglyphs(kw: str):
    for i, ch in enumerate(kw):
        if ch in HOMOGLYPH_MAP:
            yield kw[:i] + HOMOGLYPH_MAP[ch] + kw[i + 1:], "homoglyph"
    for seq, repl in HOMOGLYPH_MULTICHAR.items():
        if seq in kw:
            yield kw.replace(seq, repl, 1), "homoglyph"


def _hyphenations(kw: str):
    for i in range(1, len(kw)):
        yield kw[:i] + "-" + kw[i:], "hyphenation"


def _combosquats(kw: str):
    for w in COMBOSQUAT_WORDS:
        yield f"{w}{kw}", "combosquat"
        yield f"{kw}{w}", "combosquat"
        yield f"{w}-{kw}", "combosquat"
        yield f"{kw}-{w}", "combosquat"


# priority order used when a candidate label is produced by more than one
# technique (keep the first / most specific classification found)
_GENERATORS = [
    _homoglyphs,
    _substitutions,
    _omissions,
    _insertions,
    _repetitions,
    _transpositions,
    _hyphenations,
    _combosquats,
]


def generate_label_permutations(keyword: str) -> dict:
    """Return {candidate_domain_label: match_type} for a brand keyword.

    Labels only (no TLD) -- the caller compares against the label of an
    observed domain, independent of which TLD it was registered under.
    """
    kw = keyword.strip().lower()
    kw = re.sub(r"[^a-z0-9-]", "", kw)
    results: dict = {}
    for gen in _GENERATORS:
        for label, match_type in gen(kw):
            if label and label != kw and label not in results:
                results[label] = match_type
    return results


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[-1]


# confidence assigned per match type -- higher means "more likely to be a
# deliberate lookalike registration rather than coincidence"
CONFIDENCE_BY_TYPE = {
    "identical": 0.4,       # same keyword, different TLD than the brand's known domains
    "homoglyph": 0.95,
    "substitution": 0.9,
    "omission": 0.85,
    "insertion": 0.8,
    "repetition": 0.8,
    "transposition": 0.85,
    "hyphenation": 0.7,
    "combosquat": 0.75,
    "fuzzy": 0.5,
}


def _registrable_label(domain: str) -> str:
    """Strip a common TLD suffix (best-effort, no full public-suffix-list)."""
    domain = domain.strip().lower().rstrip(".")
    if domain.startswith("*."):
        domain = domain[2:]
    parts = domain.split(".")
    if len(parts) < 2:
        return domain
    # drop the last 1 or 2 labels depending on whether it looks like a
    # second-level ccTLD (co.uk, com.au, ...)
    if len(parts) >= 3 and parts[-2] in {"co", "com", "org", "net", "gov", "ac"} and len(parts[-1]) == 2:
        return ".".join(parts[:-2])
    return ".".join(parts[:-1])


def classify_domain(domain: str, keyword: str, permutation_set: dict) -> tuple | None:
    """Classify whether `domain` is a lookalike of `keyword`.

    Returns (match_type, confidence, matched_label) or None if no match.
    """
    kw = keyword.strip().lower()
    label = _registrable_label(domain)
    if not label:
        return None

    if label == kw:
        return "identical", CONFIDENCE_BY_TYPE["identical"], label

    if label in permutation_set:
        match_type = permutation_set[label]
        return match_type, CONFIDENCE_BY_TYPE.get(match_type, 0.6), label

    # generic combosquat catch-all: keyword appears as a whole chunk inside a
    # longer label that wasn't already covered by the fixed word list above
    if kw in label and label != kw:
        return "combosquat", CONFIDENCE_BY_TYPE["combosquat"], label

    # fuzzy fallback: small edit distance relative to keyword length, catches
    # permutations not covered by the generators above (e.g. two-character typos)
    if abs(len(label) - len(kw)) <= 2:
        dist = levenshtein(label, kw)
        if 0 < dist <= 2 and len(kw) >= 4:
            return "fuzzy", CONFIDENCE_BY_TYPE["fuzzy"], label

    return None
