#!/usr/bin/env python3
"""Check required Lumeryn development documents and report their SHA-256."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "AGENTS.md",
    "docs/MASTER_PLAN.md",
    "docs/PROJECT_STATE.md",
    "docs/DECISIONS/ADR-0001-foundation.md",
)
WO_PATTERN = re.compile(r"^[A-Z][A-Z0-9-]{2,60}$")
MASTER_SECTIONS = tuple(f"## {n}." for n in range(1, 24))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check(root: Path, work_order: str) -> dict:
    failures: list[str] = []
    if WO_PATTERN.fullmatch(work_order):
        wo = f"docs/WORK_ORDERS/{work_order}.md"
    else:
        failures.append("Invalid Work Order ID")
        wo = "docs/WORK_ORDERS/__INVALID__.md"
    file_info: dict[str, dict] = {}
    for name in (*REQUIRED, wo):
        path = root / name
        if not path.is_file():
            failures.append(f"Missing document: {name}")
            continue
        if path.stat().st_size == 0:
            failures.append(f"Empty document: {name}")
        file_info[name] = {"sha256": sha256(path), "bytes": path.stat().st_size}

    master = root / "docs/MASTER_PLAN.md"
    if master.is_file():
        source = master.read_text(encoding="utf-8")
        for marker in MASTER_SECTIONS:
            if marker not in source:
                failures.append(f"Missing master section: {marker}")

    agents = root / "AGENTS.md"
    if agents.is_file():
        content = agents.read_text(encoding="utf-8")
        if "docs/MASTER_PLAN.md" not in content or "docs/PROJECT_STATE.md" not in content:
            failures.append("Agent instructions must reference master plan and project state")

    wo_file = root / wo
    if wo_file.is_file():
        content = wo_file.read_text(encoding="utf-8")
        if work_order not in content or "docs/MASTER_PLAN.md" not in content:
            failures.append("Work Order must reference its ID and master plan")
    return {
        "work_order": work_order,
        "status": "PASS" if not failures else "FAIL",
        "master_sha256": sha256(master) if master.is_file() else None,
        "files": file_info,
        "errors": failures,
        "notice": "Hash validation does not prove a human or AI actually read the document.",
    }


def read_full_docs(root: Path, work_order: str) -> None:
    for name in (*REQUIRED, f"docs/WORK_ORDERS/{work_order}.md"):
        path = root / name
        print(f"\n===== BEGIN {name} =====")
        print(path.read_text(encoding="utf-8"))
        print(f"===== END {name} =====")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("check", "read"))
    parser.add_argument("--wo", required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    result = check(args.root.resolve(), args.wo)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] == "PASS" and args.command == "read":
        read_full_docs(args.root.resolve(), args.wo)
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
