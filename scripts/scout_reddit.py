"""Phase 1: pull demand signals from Reddit via the official API (app-only OAuth).

Usage: python scripts/scout_reddit.py runs/YYYY-MM-DD/reddit_raw.json
Reads REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET / REDDIT_USER_AGENT from .env.local.
"""
import base64
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from load_env import require

DEFAULT_SUBS = ["smallbusiness", "sysadmin", "msp", "Accounting", "Bookkeeping", "realestateinvesting",
                "airbnb_hosts", "freelance", "ecommerce", "shopify", "EtsySellers", "Entrepreneur", "SaaS"]
PHRASES = ['"I wish there was"', '"is there a tool"', '"I\'d pay for"', '"alternative to"',
           '"too expensive"', '"hate that"']
YEAR = 365 * 24 * 3600


def token(c: dict) -> str:
    auth = base64.b64encode(f"{c['REDDIT_CLIENT_ID']}:{c['REDDIT_CLIENT_SECRET']}".encode()).decode()
    req = urllib.request.Request("https://www.reddit.com/api/v1/access_token",
                                 data=b"grant_type=client_credentials",
                                 headers={"Authorization": f"Basic {auth}", "User-Agent": c["REDDIT_USER_AGENT"]})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)["access_token"]


def search(sub: str, q: str, tok: str, ua: str) -> list:
    url = f"https://oauth.reddit.com/r/{sub}/search?" + urllib.parse.urlencode(
        {"q": q, "restrict_sr": 1, "sort": "top", "t": "year", "limit": 50})
    req = urllib.request.Request(url, headers={"Authorization": f"bearer {tok}", "User-Agent": ua})
    with urllib.request.urlopen(req, timeout=20) as r:
        return [c["data"] for c in json.load(r)["data"]["children"]]


def main() -> None:
    c = require("REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT")
    cfg = json.loads((Path(__file__).resolve().parent.parent / "config.json").read_text())
    subs = cfg.get("TARGET_SUBREDDITS") or DEFAULT_SUBS
    tok, cutoff, out = token(c), time.time() - YEAR, []
    for sub in subs:
        for q in PHRASES:
            for p in search(sub, q, tok, c["REDDIT_USER_AGENT"]):
                if p["created_utc"] < cutoff:
                    continue
                text = (p.get("title", "") + " " + p.get("selftext", "")).split()
                out.append({"url": "https://www.reddit.com" + p["permalink"], "subreddit": sub, "query": q,
                            "quote": " ".join(text[:24]), "upvotes": p["score"],
                            "comments": p["num_comments"],
                            "date": time.strftime("%Y-%m-%d", time.gmtime(p["created_utc"]))})
            time.sleep(1)  # stay well under the 100 req/min limit
    json.dump(out, open(sys.argv[1], "w"), indent=2)
    print(f"{len(out)} posts")


if __name__ == "__main__":
    main()
