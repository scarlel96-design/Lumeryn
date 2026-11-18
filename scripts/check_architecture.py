#!/usr/bin/env python3
"""Check static Clean Architecture boundaries and obvious Python import cycles.

Source-level checks do not enforce runtime/plugin sandboxing.
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
    names: set[str] = set()
    package = module.rsplit(".", 1)[0] if "." in module else module
    if module.endswith(("domain", "application", "infrastructure", "bootstrap")):
        package = module
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                components = package.split(".")
                ascend = node.level - 1
                if ascend >= len(components):
                    names.add("__invalid_relative_import__")
                    continue
                prefix = ".".join(components[:len(components) - ascend])
                target = prefix + ("." + node.module if node.module else "")
            else:
                target = node.module or ""
            names.add(target)
            for alias in node.names:
                names.add(target + "." + alias.name)
    return names


def find_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    visited: set[str] = set()
    active: set[str] = set()
    path: list[str] = []
    cycles: list[list[str]] = []

    def visit(node: str) -> None:
        visited.add(node)
        active.add(node)
        path.append(node)
        for next_node in sorted(graph[node]):
            if next_node not in graph:
                continue
            if next_node in active:
                start = path.index(next_node)
                cycle = path[start:] + [next_node]
                if cycle not in cycles:
                    cycles.append(cycle)
            elif next_node not in visited:
                visit(next_node)
        path.pop()
        active.remove(node)

    for node in sorted(graph):
        if node not in visited:
            visit(node)
    return cycles


def scan(root: Path) -> list[str]:
    package_root = root / "src/lumeryn"
    failures: list[str] = []
    if not package_root.is_dir():
        return ["Missing src/lumeryn package"]
    parsed: dict[str, set[str]] = {}
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
        names = imported_names(tree, module)
        parsed[module] = names
        for imported in names:
            if any(imported == prefix or imported.startswith(prefix + ".") for prefix in forbidden):
                failures.append(f"{relative}: forbidden import {imported} in {layer}")
            if imported == "__invalid_relative_import__":
                failures.append(f"{relative}: invalid relative import")
    graph = {
        name: {dep for dep in deps if dep in parsed and dep != name}
        for name, deps in parsed.items()
    }
    for cycle in find_cycles(graph):
        failures.append("Import cycle: " + " -> ".join(cycle))
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    failures = scan(args.root.resolve())
    if failures:
        print("FAIL: architecture boundary or import cycle")
        for failure in failures:
            print(f"- {failure}")
        return 2
    print("PASS: static architecture import boundaries and cycles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
