"""Load .env.local into os.environ at runtime without printing anything."""
import os
from pathlib import Path


def load_env(path: str = ".env.local") -> None:
    p = Path(__file__).resolve().parent.parent / path
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def require(*keys: str) -> dict:
    load_env()
    missing = [k for k in keys if not os.environ.get(k)]
    if missing:
        raise SystemExit(f"Missing env vars: {', '.join(missing)} (set them in .env.local)")
    return {k: os.environ[k] for k in keys}
