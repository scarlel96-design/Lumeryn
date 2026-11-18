#!/usr/bin/env python3
"""Check forbidden static imports across Clean Architecture boundaries.

This is a source-level guard, not a sandbox or a complete dependency scanner.
"""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_EXTERNAL = (
    "PySide6", "PyQt6", "fastapi", "langgraph", "ollama",
    "qdrant_client", "sqlalchemy", "httpx", "requests", "sqlite3", "subprocess",
)
FORBIDDEN_DOMAIN = (
    "lumeryn.application", "lumeryn.infrastructure",
    "lumeryn.bootstrap", "lumeryn.plugins",
)
FORBIDDEN_APPLICATION = (
    "lumeryn.infrastructure", "lumeryn.bootstrap", "lumeryn.plugins",
)


def module_name(path: Path, package_root: Path) -> str:
    relative = path.relative_to(package_root).with_suffix("")
    parts = list(relative.parts)
    if parts[-1] == "__init__":
        parts.pop()
    return "lumeryn" + ("." + ".".join(parts) if parts else "")


def imported_names(tree: ast.AST, module: str) -> set[str]:
    output: set[str] = set()
    # Relative imports are resolved only when the module package is known.
    package = module.rsplit(".", 1)[0] if "." in module else module
    if module.endswith(("domain", "application", "infrastructure", "bootstrap")):
        package = module
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            output.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                components = package.split(".")
                ascend = node.level - 1
                if ascend >= len(components):
                    output.add("__invalid_relative_import__")
                    continue
                prefix = ".".join(components[:len(components) - ascend])
                target = prefix + ("." + node.module if node.module else "")
            else:
                target = node.module or ""
            output.add(target)
            if not node.module:
                output.update(target + "." + alias.name for alias in node.names)
    return output


def scan(root: Path) -> list[str]:
    package_root = root / "src/lumeryn"
    failures: list[str] = []
    if not package_root.is_dir():
        return ["Missing src/lumeryn package"]
    for path in sorted(package_root.rglob("*.py")):
        relative = path.relative_to(root).as_posix()
        module = module_name(path, package_root)
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        except (SyntaxError, UnicodeError) as error:
            failures.append(f"{relative}: parse failure: {error}")
            continue
        layer = path.relative_to(package_root).parts[0]
        forbidden = ()
        if layer == "domain":
            forbidden = FORBIDDEN_DOMAIN + FORBIDDEN_EXTERNAL
        elif layer == "application":
            forbidden = FORBIDDEN_APPLICATION + FORBIDDEN_EXTERNAL
        for imported in imported_names(tree, module):
            if any(imported == prefix or imported.startswith(prefix + ".") for prefix in forbidden):
                failures.append(f"{relative}: forbidden import {imported} in {layer}")
            if imported == "__invalid_relative_import__":
                failures.append(f"{relative}: invalid relative import")
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    failures = scan(args.root.resolve())
    if failures:
        print("FAIL: architecture boundary violations")
        for failure in failures:
            print(f"- {failure}")
        return 2
    print("PASS: architecture import boundary checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
