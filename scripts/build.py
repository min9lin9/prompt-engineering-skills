#!/usr/bin/env python3
"""Build reproducible v4 distribution knowledge packs from canonical sources."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "prompt-engineering"
REGISTRY = ROOT / "registry" / "models.yaml"
OUT = ROOT / "generated"

HEADER = """<!-- GENERATED FILE — DO NOT EDIT DIRECTLY -->
<!-- Source: Prompt Engineering Skills v4 canonical Core / Task / Model / Registry -->

"""


def canonical_files() -> list[Path]:
    files: list[Path] = []
    for subdir in ("core", "tasks", "models"):
        base = SKILL / subdir
        if base.exists():
            files.extend(sorted(base.rglob("*.md"), key=lambda p: p.as_posix()))
    if REGISTRY.exists():
        files.append(REGISTRY)
    return files


def section(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8").rstrip()
    return f"\n---\n\n# Source: `{rel}`\n\n{text}\n"


def render(title: str, platform_note: str) -> str:
    parts = [HEADER, f"# {title}\n\n", platform_note.rstrip(), "\n"]
    for path in canonical_files():
        parts.append(section(path))
    return "".join(parts)


def outputs() -> dict[str, str]:
    common = render(
        "Prompt Engineering Skills v4 — Unified Knowledge Pack",
        "Use Core + exactly one relevant Task Profile + only the relevant Provider/Model Delta. Registry capability facts are not prompt-strategy claims.",
    )
    return {
        "prompt-engineering-guide.md": common,
        "gpts-knowledge.md": render(
            "Prompt Engineering Skills v4 — GPTs Knowledge Pack",
            "This file is knowledge for the thin GPTs adapter. It does not grant execution permissions and does not override host policies.",
        ),
        "gems-knowledge.md": render(
            "Prompt Engineering Skills v4 — Gems Knowledge Pack",
            "This file is knowledge for the thin Gems adapter. Apply target-model deltas only when relevant; do not force Gemini syntax onto other targets.",
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    built = outputs()
    for name, content in built.items():
        path = args.output_dir / name
        path.write_text(content, encoding="utf-8")
        print(f"generated {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path} ({len(content.encode('utf-8'))} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
