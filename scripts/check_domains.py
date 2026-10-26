"""Check domain availability + price via Porkbun API. Read-only: never registers.

Usage: python scripts/check_domains.py runs/2026-10-26/domains.json
Input: {"idea-slug": ["a.com", "b.com", ...], ...}
Writes results back into <input>.results.json.
"""
import json
import sys
import time
import urllib.request

from load_env import require

API = "https://api.porkbun.com/api/json/v3/domain/checkDomain/"


def check(domain: str, creds: dict) -> dict:
    body = json.dumps({"apikey": creds["PORKBUN_API_KEY"],
                       "secretapikey": creds["PORKBUN_SECRET_API_KEY"]}).encode()
    for attempt in range(2):  # stop after two failures, per run rules
        try:
            req = urllib.request.Request(API + domain, data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.load(r)
            resp = data.get("response", {})
            return {"domain": domain, "status": data.get("status"),
                    "available": resp.get("avail") == "yes",
                    "price": resp.get("price"), "renewal": resp.get("additional", {})
                    .get("renewal", {}).get("price"), "premium": resp.get("premium") == "yes"}
        except Exception as e:  # noqa: BLE001
            err = str(e)
            time.sleep(2)
    return {"domain": domain, "error": err}


def main() -> None:
    creds = require("PORKBUN_API_KEY", "PORKBUN_SECRET_API_KEY")
    src = sys.argv[1]
    ideas = json.load(open(src))
    out = {}
    for slug, domains in ideas.items():
        out[slug] = []
        for d in domains:
            out[slug].append(check(d, creds))
            time.sleep(10)  # checkDomain is rate-limited (~1 per 10s)
    json.dump(out, open(src.replace(".json", ".results.json"), "w"), indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
