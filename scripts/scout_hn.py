"""Phase 1: pull Ask HN / Show HN comments matching demand phrases (HN Algolia API, no key needed).

Usage: python scripts/scout_hn.py runs/YYYY-MM-DD/hn_raw.json
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

PHRASES = ["I wish there was", "is there a tool", "I'd pay for", "alternative to", "too expensive"]


def main() -> None:
    since, out = int(time.time()) - 365 * 24 * 3600, []
    for q in PHRASES:
        url = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
            {"query": f'"{q}"', "tags": "comment", "numericFilters": f"created_at_i>{since}", "hitsPerPage": 100})
        with urllib.request.urlopen(url, timeout=20) as r:
            for h in json.load(r)["hits"]:
                text = re.sub(r"<[^>]+>", " ", h.get("comment_text") or "").split()
                out.append({"url": f"https://news.ycombinator.com/item?id={h['objectID']}", "query": q,
                            "quote": " ".join(text[:24]), "upvotes": h.get("points"),
                            "story": h.get("story_title"), "date": h["created_at"][:10]})
    json.dump(out, open(sys.argv[1], "w"), indent=2)
    print(f"{len(out)} comments")


if __name__ == "__main__":
    main()
