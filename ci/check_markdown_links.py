#!/usr/bin/env python3
"""Fail when a tracked Markdown file links to a missing relative target."""

from __future__ import annotations

import re
from pathlib import Path


LINK = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("#", "http://", "https://", "mailto:")


def markdown_files(root: Path) -> list[Path]:
    ignored = {".git", ".venv", "node_modules"}
    return sorted(
        path
        for path in root.rglob("*.md")
        if not any(part in ignored for part in path.parts)
    )


def missing_links(root: Path) -> list[str]:
    failures = []
    for path in markdown_files(root):
        text = path.read_text(errors="replace")
        for match in LINK.finditer(text):
            target = match.group(1).strip().split()[0].strip("<>")
            if not target or target.lower() == "url" or target.startswith(EXTERNAL_PREFIXES):
                continue
            relative = target.split("#", 1)[0]
            if relative and not (path.parent / relative).resolve().exists():
                line = text.count("\n", 0, match.start()) + 1
                failures.append(f"{path.relative_to(root)}:{line}: {target}")
    return failures


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    failures = missing_links(root)
    if failures:
        print("Missing relative Markdown targets:")
        print("\n".join(failures))
        return 1
    print(f"Markdown links OK: {len(markdown_files(root))} repository files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
