#!/usr/bin/env python3
"""Validate mandatory Lumeryn design records before an agent starts work."""
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
    "docs/WORK_ORDER_INDEX.md",
    "docs/ARCHITECTURE.md",
    "docs/ACCEPTANCE.md",
    "docs/REQUIREMENTS_TRACEABILITY.md",
    "docs/DECISIONS/ADR-0001-foundation.md",
)
WO_PATTERN = re.compile(r"^(?:WO-[A-Z0-9-]+|FT-[0-9]{2}|REL-[0-9]{2})$")
HEADING_PATTERN = re.compile(r"^## ([0-9]+)\.\s", re.MULTILINE)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def work_order_path(work_order: str) -> str | None:
    if (
        not 3 <= len(work_order) <= 64
        or not WO_PATTERN.fullmatch(work_order)
        or ".." in work_order
        or work_order.endswith("-")
    ):
        return None
    return f"docs/WORK_ORDERS/{work_order}.md"


def check(root: Path, work_order: str) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    wo = work_order_path(work_order)
    if wo is None:
        errors.append(f"Invalid Work Order ID: {work_order}")
    paths = list(REQUIRED)
    if wo:
        paths.append(wo)
    files: dict[str, dict] = {}
    for name in paths:
        path = root / name
        if not path.is_file():
            errors.append(f"Missing required file: {name}")
            continue
        size = path.stat().st_size
        if size == 0:
            errors.append(f"Empty file: {name}")
        files[name] = {"sha256": sha256(path), "bytes": size}

    master = root / "docs/MASTER_PLAN.md"
    if master.is_file():
        content = master.read_text(encoding="utf-8")
        numbered = [int(n) for n in HEADING_PATTERN.findall(content)]
        if len(numbered) < 23:
            errors.append("Master plan contains fewer than the initial 23 numbered chapters")
        if numbered != list(range(1, len(numbered) + 1)):
            errors.append(f"Master plan chapters are not contiguous and ordered: {numbered}")

    agents = root / "AGENTS.md"
    if agents.is_file():
        text = agents.read_text(encoding="utf-8")
        for path in ("docs/MASTER_PLAN.md", "docs/PROJECT_STATE.md", "docs/WORK_ORDERS/"):
            if path not in text:
                errors.append(f"AGENTS.md missing mandatory reference: {path}")

    state = root / "docs/PROJECT_STATE.md"
    if state.is_file():
        text = state.read_text(encoding="utf-8")
        if "현재 WO" not in text or "현재 상태" not in text:
            errors.append("PROJECT_STATE.md missing current WO/status fields")
        if work_order not in text:
            warnings.append("Work Order ID is not mentioned in PROJECT_STATE.md")

    index = root / "docs/WORK_ORDER_INDEX.md"
    if index.is_file() and work_order not in index.read_text(encoding="utf-8"):
        warnings.append("Work Order ID is not in the index; verify plan approval")

    if wo and (root / wo).is_file():
        content = (root / wo).read_text(encoding="utf-8")
        if work_order not in content:
            errors.append(f"{wo} does not contain its Work Order ID")
        if "docs/MASTER_PLAN.md" not in content:
            errors.append(f"{wo} does not require reading the master plan")

    return {
        "work_order": work_order,
        "status": "PASS" if not errors else "FAIL",
        "master_sha256": sha256(master) if master.is_file() else None,
        "files": files,
        "warnings": warnings,
        "errors": errors,
        "notice": (
            "Document presence and hashes do not prove an agent read or understood them. "
            "Require a separate start report."
        ),
    }


def read_full_docs(root: Path, work_order: str) -> None:
    wo = work_order_path(work_order)
    if wo is None:
        raise ValueError("Invalid Work Order ID")
    for name in ("AGENTS.md", "docs/MASTER_PLAN.md", "docs/PROJECT_STATE.md", wo):
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
    root = args.root.resolve()
    result = check(root, args.wo)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] == "PASS" and args.command == "read":
        read_full_docs(root, args.wo)
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
