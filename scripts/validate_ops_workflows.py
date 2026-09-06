#!/usr/bin/env python3
"""Validate v4 operational command boundaries."""

from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "update": ROOT / "commands" / "prompt-update.md",
    "sync": ROOT / "commands" / "prompt-sync.md",
    "auto": ROOT / "commands" / "auto-prompt.md",
}


def main() -> int:
    errors: list[str] = []
    texts: dict[str, str] = {}

    for name, path in FILES.items():
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
            continue
        texts[name] = path.read_text(encoding="utf-8")

    if errors:
        for error in errors:
            print(f"- {error}")
        return 1

    common_forbidden = (
        r"treylom/",
        r"/mnt/c/Users/",
        r"~/.claude/",
        r"\.claude/agents/",
        r"git\s+push\s+origin",
    )
    for name, text in texts.items():
        for pattern in common_forbidden:
            if re.search(pattern, text, re.I):
                errors.append(f"{name}: forbidden operational coupling {pattern!r}")

    update = texts["update"]
    for required in ("Default behavior is read-only", "Confirmed capability/runtime fact", "Mutation boundary"):
        if required not in update:
            errors.append(f"update: missing contract {required!r}")

    sync = texts["sync"]
    for required in ("`dry-run` is the default", "Shared directories are additive only", "separate explicit user authorization"):
        if required not in sync:
            errors.append(f"sync: missing safety contract {required!r}")
    if re.search(r"rsync[^\n]*--delete", sync, re.I):
        errors.append("sync: embeds destructive rsync command instead of policy-level guard")

    auto = texts["auto"]
    for required in ("optional workflow", "registry/models.yaml", "Do not assume a fixed author/source name"):
        if required.lower() not in auto.lower():
            errors.append(f"auto: missing portability contract {required!r}")
    if re.search(r"난이도.*XML|difficulty.*XML", auto, re.I):
        errors.append("auto: reintroduced complexity-to-syntax coupling")

    if errors:
        print("v4 ops workflow validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("v4 ops workflow validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
