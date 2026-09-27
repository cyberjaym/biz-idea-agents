"""Optional standalone loop for continuous polling (run alongside app.py).

    python3 poller.py --mode crtsh --interval 300

This is what would run "in production" instead of manually calling
POST /ingest/run -- a scheduled job hitting crt.sh every N seconds/minutes
per registered brand. For the MVP demo, calling /ingest/run by hand is
simpler and enough to prove the pipeline works.
"""
from __future__ import annotations

import argparse
import time

import db
from ingest import run_ingest_cycle


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["sample", "crtsh"], default="crtsh")
    parser.add_argument("--interval", type=int, default=300, help="seconds between poll cycles")
    args = parser.parse_args()

    db.init_db()
    print(f"[poller] starting, mode={args.mode}, interval={args.interval}s")
    while True:
        summary = run_ingest_cycle(mode=args.mode)
        print(f"[poller] {summary['mode']}: checked {summary['domains_checked']} domains "
              f"across {summary['brands_checked']} brands -> {summary['new_alerts']} new alerts")
        for m in summary["matches"]:
            if m.get("error"):
                print(f"[poller]   error: {m['error']}")
            elif m.get("new"):
                print(f"[poller]   NEW ALERT: {m['domain']} -> brand={m['brand']} "
                      f"type={m['match_type']} confidence={m['confidence']}")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
