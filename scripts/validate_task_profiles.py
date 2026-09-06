#!/usr/bin/env python3
"""Static validation for v4 Core and Task Profiles.

The goal is separation of concerns: Task Profiles describe task semantics, not
provider/model behavior or execution authorization.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TASK_DIR = ROOT / "skills" / "prompt-engineering" / "tasks"
CORE_DIR = ROOT / "skills" / "prompt-engineering" / "core"

REQUIRED_TASKS = {
    "research",
    "fact-check",
    "coding",
    "analysis",
    "writing",
    "editing",
    "extraction",
    "agent",
    "image",
    "video",
    "slides",
}

REQUIRED_SECTIONS = ("## Goal", "## Required inputs", "## Rules", "## Validation", "## Do not")

# Task profiles must remain provider/model neutral. Generic words such as
# "model" and "runtime" are allowed when discussing separation of concerns.
FORBIDDEN_PRODUCT_TOKENS = (
    "gpt-",
    "astra",
    "claude",
    "gemini",
    "qwen",
    "kimi",
    "deepseek",
    "glm-",
    "grok",
    "minimax",
    "mistral",
    "openai",
    "anthropic",
)

FORBIDDEN_AUTHORIZATION_PATTERNS = (
    re.compile(r"\bautomatically\s+(?:commit|push|publish|send|deploy)\b", re.I),
    re.compile(r"\bwithout\s+(?:user\s+)?(?:approval|authorization)\b", re.I),
)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for raw in text[4:end].splitlines():
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def main() -> int:
    errors: list[str] = []

    for core_file in ("principles.md", "prompt-contract.md", "validation.md"):
        if not (CORE_DIR / core_file).exists():
            errors.append(f"missing core file: {core_file}")

    discovered: set[str] = set()
    for path in sorted(TASK_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        task = meta.get("task")
        if not task:
            errors.append(f"{path.name}: missing task frontmatter")
            continue
        discovered.add(task)
        if path.stem != task:
            errors.append(f"{path.name}: filename must match task id {task!r}")
        if meta.get("version") != "1":
            errors.append(f"{path.name}: version must be 1")

        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{path.name}: missing section {section}")

        lowered = text.lower()
        for token in FORBIDDEN_PRODUCT_TOKENS:
            if token in lowered:
                errors.append(f"{path.name}: provider/model token leaked into task profile: {token}")

        for pattern in FORBIDDEN_AUTHORIZATION_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path.name}: task profile contains unsafe authorization semantics: {pattern.pattern}")

    missing = REQUIRED_TASKS - discovered
    extra = discovered - REQUIRED_TASKS
    if missing:
        errors.append(f"missing required tasks: {sorted(missing)}")
    if extra:
        errors.append(f"unexpected task ids: {sorted(extra)}")

    if errors:
        print("v4 task profile validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"v4 task profile validation OK: {len(discovered)} task profiles")
    print("note: profile validation does not imply target-model quality evaluation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
