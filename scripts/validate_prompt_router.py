#!/usr/bin/env python3
"""Validate the v4 /prompt migration router and legacy shadow snapshot."""

from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "commands" / "prompt.md"
LEGACY = ROOT / "commands" / "prompt-legacy.md"
FIXTURES = ROOT / "tests" / "v4" / "prompt-router-fixtures.yaml"

# Git blob SHA of commands/prompt.md at the PR-006 baseline.
LEGACY_GIT_BLOB_SHA = "6eec56007b8599ac3e833915bcb5630fc16b8b58"

REQUIRED_ROUTER_SNIPPETS = (
    "default `legacy`",
    "`--legacy`",
    "`--v4`",
    "`--shadow`",
    "Prompt Contract",
    "skills/prompt-engineering/core/principles.md",
    "skills/prompt-engineering/core/validation.md",
    "registry/models.yaml",
    "Select exactly one primary Task Profile",
    "Do not execute the generated prompt",
    "Do not change the no-flag default from `legacy` to `v4`",
)

FORBIDDEN_ROUTER_PATTERNS = (
    re.compile(r"\bLMArena\b", re.I),
    re.compile(r"treylom/", re.I),
    re.compile(r"~/.claude/", re.I),
    re.compile(r"\bgit\s+push\b", re.I),
    re.compile(r"\brsync\b[^\n]*--delete", re.I),
    re.compile(r"5가지\s*옵션\s*반드시", re.I),
    re.compile(r"mandatory\s+expert\s+(?:panel|debate)", re.I),
)


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def main() -> int:
    errors: list[str] = []

    if not ROUTER.exists():
        errors.append("commands/prompt.md is missing")
    if not LEGACY.exists():
        errors.append("commands/prompt-legacy.md is missing")
    if not FIXTURES.exists():
        errors.append("tests/v4/prompt-router-fixtures.yaml is missing")

    if errors:
        for error in errors:
            print(f"- {error}")
        return 1

    router_text = ROUTER.read_text(encoding="utf-8")
    legacy_bytes = LEGACY.read_bytes()

    # The router must remain an orchestrator, not regress into a second mega-guide.
    if len(router_text.encode("utf-8")) > 24_000:
        errors.append("commands/prompt.md exceeds 24KB router budget")

    for snippet in REQUIRED_ROUTER_SNIPPETS:
        if snippet not in router_text:
            errors.append(f"router missing required contract: {snippet!r}")

    for pattern in FORBIDDEN_ROUTER_PATTERNS:
        if pattern.search(router_text):
            errors.append(f"router reintroduced forbidden legacy coupling: {pattern.pattern}")

    actual_legacy_sha = git_blob_sha(legacy_bytes)
    if actual_legacy_sha != LEGACY_GIT_BLOB_SHA:
        errors.append(
            "legacy shadow snapshot drifted: "
            f"expected {LEGACY_GIT_BLOB_SHA}, got {actual_legacy_sha}"
        )

    if "no flag | `legacy`" not in router_text:
        errors.append("no-flag migration default is not explicitly legacy")

    if not re.search(r"`?/prompt --shadow --batch`?[^\n]*invalid", router_text, re.I):
        errors.append("shadow/batch incompatibility is not explicit")

    if errors:
        print("v4 prompt router validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("v4 prompt router validation OK")
    print(f"router bytes: {len(router_text.encode('utf-8'))}")
    print(f"legacy snapshot blob: {actual_legacy_sha}")
    print("default route: legacy (shadow migration)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
