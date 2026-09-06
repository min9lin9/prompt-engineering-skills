#!/usr/bin/env python3
"""Non-mutating baseline guardrails for the v4 migration.

This script intentionally reports known legacy hazards as findings rather than
failing the build. PR-001 establishes visibility first; later PRs can promote
specific checks to hard failures after migration paths exist.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Rule:
    id: str
    pattern: re.Pattern[str]
    paths: tuple[str, ...]
    severity: str
    description: str


RULES = (
    Rule(
        "LEGACY_UPSTREAM_REPO",
        re.compile(r"treylom/(?:prompt-engineering-skills|obsidian-ai-vault)"),
        ("README.md", "commands"),
        "warning",
        "Legacy upstream repository is hard-coded in an operational/documentation path.",
    ),
    Rule(
        "AUTOMATIC_GIT_PUSH",
        re.compile(r"\bgit\s+push\b"),
        ("commands",),
        "warning",
        "A command document contains git push semantics; v4 must gate push behind explicit authorization.",
    ),
    Rule(
        "DESTRUCTIVE_RSYNC",
        re.compile(r"\brsync\b[^\n]*--delete"),
        ("commands",),
        "warning",
        "A command contains destructive rsync --delete semantics; only dedicated mirrors may ever use it.",
    ),
    Rule(
        "EXTERNAL_CLAUDE_AGENT_DEPENDENCY",
        re.compile(r"\.claude/(?:agents|skills)/"),
        ("commands/auto-prompt.md",),
        "info",
        "Optional auto-prompt workflow depends on external Claude assets.",
    ),
)


def iter_files(scope: str):
    path = ROOT / scope
    if not path.exists():
        return
    if path.is_file():
        yield path
        return
    yield from path.rglob("*.md")


def main() -> int:
    findings: list[tuple[Rule, Path, int, str]] = []
    for rule in RULES:
        for scope in rule.paths:
            for path in iter_files(scope) or ():
                try:
                    lines = path.read_text(encoding="utf-8").splitlines()
                except UnicodeDecodeError:
                    continue
                for lineno, line in enumerate(lines, 1):
                    if rule.pattern.search(line):
                        findings.append((rule, path.relative_to(ROOT), lineno, line.strip()))

    print("v4 baseline guardrails")
    print(f"repository: {ROOT}")
    print(f"findings: {len(findings)}")
    for rule, path, lineno, line in findings:
        print(f"[{rule.severity}] {rule.id} {path}:{lineno}: {line}")

    # PR-001 snapshots known hazards; it does not fail on legacy findings.
    # Structural execution failures still return non-zero via exceptions.
    return 0


if __name__ == "__main__":
    sys.exit(main())
