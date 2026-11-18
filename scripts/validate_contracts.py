#!/usr/bin/env python3
"""Validate agent handoff or module manifest using versioned JSON Schemas."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "handoff": "schemas/agent-handoff.schema.json",
    "module": "schemas/module-manifest.schema.json",
}


def validate(root: Path, kind: str, candidate: Path) -> list[str]:
    try:
        from jsonschema import Draft202012Validator
    except ImportError as error:
        raise RuntimeError("Install development extras: python -m pip install -e '.[dev]'") from error

    errors: list[str] = []
    schema = json.loads((root / SCHEMAS[kind]).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    payload = json.loads(candidate.read_text(encoding="utf-8"))
    for issue in Draft202012Validator(schema).iter_errors(payload):
        loc = ".".join(map(str, issue.absolute_path)) or "$"
        errors.append(f"{loc}: {issue.message}")

    if kind == "handoff":
        master = root / "docs/MASTER_PLAN.md"
        if not master.is_file():
            errors.append("Missing master plan")
        else:
            current_sha = hashlib.sha256(master.read_bytes()).hexdigest()
            if payload.get("master_sha256") != current_sha:
                errors.append("master_sha256 differs from current master plan")
        if payload.get("status") == "COMPLETED":
            if payload.get("blockers"):
                errors.append("COMPLETED handoff cannot contain blockers")
            if not any(test.get("status") == "PASS" for test in payload.get("tests", [])):
                errors.append("COMPLETED handoff requires at least one executed PASS test")
            if payload.get("files_changed") and not payload.get("result_commit"):
                errors.append("Changed files require a result_commit before COMPLETED")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=tuple(SCHEMAS))
    parser.add_argument("file", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        issues = validate(args.root.resolve(), args.kind, args.file.resolve())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"FAIL: {error}")
        return 2
    if issues:
        print("FAIL:")
        for issue in issues:
            print(f"- {issue}")
        return 2
    print(f"PASS: {args.kind} contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
