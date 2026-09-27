"""SQLite storage for brands and alerts. Zero external DB dependency."""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.environ.get("CT_PHISH_DB", os.path.join(os.path.dirname(__file__), "ct_phish.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL UNIQUE,
    owner TEXT NOT NULL,
    legit_domains TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_id INTEGER NOT NULL REFERENCES brands(id),
    brand_keyword TEXT NOT NULL,
    domain TEXT NOT NULL,
    match_type TEXT NOT NULL,
    confidence REAL NOT NULL,
    source TEXT NOT NULL,
    issuer TEXT,
    cert_seen_at TEXT,
    created_at TEXT NOT NULL,
    UNIQUE(brand_id, domain)
);
"""


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = get_conn()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_brand(keyword: str, owner: str, legit_domains: list | None = None) -> dict:
    keyword = keyword.strip().lower()
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO brands (keyword, owner, legit_domains, created_at) VALUES (?, ?, ?, ?)",
            (keyword, owner, json.dumps(legit_domains or []), _now()),
        )
        conn.commit()
        return get_brand(cur.lastrowid)
    finally:
        conn.close()


def list_brands() -> list[dict]:
    conn = get_conn()
    try:
        rows = conn.execute("SELECT * FROM brands ORDER BY id").fetchall()
        return [dict(r) | {"legit_domains": json.loads(r["legit_domains"])} for r in rows]
    finally:
        conn.close()


def get_brand(brand_id: int) -> dict | None:
    conn = get_conn()
    try:
        row = conn.execute("SELECT * FROM brands WHERE id = ?", (brand_id,)).fetchone()
        if not row:
            return None
        return dict(row) | {"legit_domains": json.loads(row["legit_domains"])}
    finally:
        conn.close()


def get_brand_by_keyword(keyword: str) -> dict | None:
    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM brands WHERE keyword = ?", (keyword.strip().lower(),)
        ).fetchone()
        if not row:
            return None
        return dict(row) | {"legit_domains": json.loads(row["legit_domains"])}
    finally:
        conn.close()


def insert_alert(
    brand_id: int,
    brand_keyword: str,
    domain: str,
    match_type: str,
    confidence: float,
    source: str,
    issuer: str | None = None,
    cert_seen_at: str | None = None,
) -> bool:
    """Insert an alert. Returns True if newly inserted, False if a duplicate
    (same brand + domain already recorded)."""
    conn = get_conn()
    try:
        try:
            conn.execute(
                """INSERT INTO alerts
                   (brand_id, brand_keyword, domain, match_type, confidence, source, issuer, cert_seen_at, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (brand_id, brand_keyword, domain, match_type, confidence, source, issuer, cert_seen_at, _now()),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    finally:
        conn.close()


def list_alerts(brand: str | None = None, match_type: str | None = None, min_confidence: float | None = None) -> list[dict]:
    conn = get_conn()
    try:
        query = "SELECT * FROM alerts WHERE 1=1"
        params: list = []
        if brand:
            query += " AND brand_keyword = ?"
            params.append(brand.strip().lower())
        if match_type:
            query += " AND match_type = ?"
            params.append(match_type)
        if min_confidence is not None:
            query += " AND confidence >= ?"
            params.append(min_confidence)
        query += " ORDER BY created_at DESC"
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
