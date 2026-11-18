#!/usr/bin/env python3
"""Check relative Markdown links to tracked local files.

External URLs and Markdown anchors are intentionally not resolved.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def check_links(root: Path) -> list[str]:
    errors: list[str] = []
    for page in sorted(root.rglob("*.md")):
        if any(part in (".git", ".venv", ".cache") for part in page.parts):
            continue
        content = page.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(content):
            raw = match.group(1).strip()
            if not raw or raw.startswith(("#", "http://", "https://", "mailto:")):
                continue
            pathpart = unquote(raw.split("#", 1)[0].split("?", 1)[0])
            if not pathpart or pathpart.startswith("<"):
                continue
            target = (page.parent / pathpart).resolve()
            if not target.is_relative_to(root.resolve()):
                errors.append(f"{page.relative_to(root)}: link escapes repository: {raw}")
            elif not target.is_file():
                errors.append(f"{page.relative_to(root)}: missing target: {raw}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    errors = check_links(args.root.resolve())
    for error in errors:
        print("FAIL:", error)
    if errors:
        return 2
    print("PASS: relative Markdown file links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
