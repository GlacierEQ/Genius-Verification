#!/usr/bin/env python3
"""Local contract validator for Genius-Verification."""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_NAME_RE = re.compile(r"^Genius-[A-Za-z0-9._-]+$")
SUPPORTED_SCHEMA = 2


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []
    genius_path = root / "GENIUS.yaml"
    if not genius_path.exists():
        errors.append("GENIUS.yaml missing")
    else:
        data = load_yaml(genius_path)
        if data.get("schema_version") != SUPPORTED_SCHEMA:
            errors.append(f"schema_version must be {SUPPORTED_SCHEMA}")
        if data.get("repository") != "Genius-Verification":
            errors.append("repository must be Genius-Verification")
        if not REPO_NAME_RE.match(str(data.get("repository", ""))):
            errors.append("invalid repository identity")
    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS — Genius-Verification contract OK (seed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
