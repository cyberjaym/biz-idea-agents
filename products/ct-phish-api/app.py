"""REST API for the CT-log phishing/typosquat monitoring MVP.

Endpoints:
  GET  /health
  POST /brands              {"keyword": "...", "owner": "...", "legit_domains": ["..."]}
  GET  /brands
  GET  /alerts?brand=X&match_type=Y&min_confidence=0.8
  POST /ingest/run?mode=sample|crtsh   -- trigger one ingestion cycle synchronously
"""
from __future__ import annotations

from flask import Flask, jsonify, request

import db
from ingest import run_ingest_cycle

app = Flask(__name__)
db.init_db()


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/brands")
def create_brand():
    body = request.get_json(silent=True) or {}
    keyword = (body.get("keyword") or "").strip()
    owner = (body.get("owner") or "").strip()
    legit_domains = body.get("legit_domains") or []

    if not keyword or not owner:
        return jsonify({"error": "both 'keyword' and 'owner' are required"}), 400
    if not isinstance(legit_domains, list):
        return jsonify({"error": "'legit_domains' must be a list of strings"}), 400

    if db.get_brand_by_keyword(keyword):
        return jsonify({"error": f"brand keyword '{keyword.lower()}' already registered"}), 409

    brand = db.create_brand(keyword, owner, legit_domains)
    return jsonify(brand), 201


@app.get("/brands")
def get_brands():
    return jsonify(db.list_brands())


@app.get("/alerts")
def get_alerts():
    brand = request.args.get("brand")
    match_type = request.args.get("match_type")
    min_confidence = request.args.get("min_confidence", type=float)
    return jsonify(db.list_alerts(brand=brand, match_type=match_type, min_confidence=min_confidence))


@app.post("/ingest/run")
def ingest_run():
    mode = request.args.get("mode", "sample")
    if mode not in ("sample", "crtsh"):
        return jsonify({"error": "mode must be 'sample' or 'crtsh'"}), 400
    summary = run_ingest_cycle(mode=mode)
    return jsonify(summary)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
