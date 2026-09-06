#!/usr/bin/env python3
"""Validate v4 distribution adapters and generated knowledge packs."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
GPTS = ROOT / "instructions" / "GPTs-Prompt-Generator.md"
GEMS = ROOT / "instructions" / "Gems-Prompt-Generator.md"
LEGACY_GPTS = ROOT / "legacy" / "instructions" / "GPTs-Prompt-Generator.md"
LEGACY_GEMS = ROOT / "legacy" / "instructions" / "Gems-Prompt-Generator.md"
BUILD = ROOT / "scripts" / "build.py"

REQUIRED_ADAPTER_SNIPPETS = (
    "thin runtime adapter",
    "Execution boundary",
    "Prompt Contract",
    "Experimental",
)


def main() -> int:
    errors: list[str] = []

    for path in (GPTS, GEMS, LEGACY_GPTS, LEGACY_GEMS, BUILD):
        if not path.exists():
            errors.append(f"missing required distribution asset: {path.relative_to(ROOT)}")

    if errors:
        for error in errors:
            print(f"- {error}")
        return 1

    for path in (GPTS, GEMS):
        text = path.read_text(encoding="utf-8")
        if len(text.encode("utf-8")) > 8_000:
            errors.append(f"{path.relative_to(ROOT)} exceeds 8KB thin-adapter budget")
        for snippet in REQUIRED_ADAPTER_SNIPPETS:
            if snippet not in text:
                errors.append(f"{path.relative_to(ROOT)} missing {snippet!r}")
        for forbidden in ("LMArena", "5가지 옵션 반드시", "전문가 3인 토론", "treylom/"):
            if forbidden in text:
                errors.append(f"{path.relative_to(ROOT)} reintroduced legacy coupling: {forbidden!r}")

    if LEGACY_GPTS.stat().st_size <= GPTS.stat().st_size:
        errors.append("legacy GPTs snapshot is not larger than thin adapter; snapshot may be wrong")
    if LEGACY_GEMS.stat().st_size <= GEMS.stat().st_size:
        errors.append("legacy Gems snapshot is not larger than thin adapter; snapshot may be wrong")

    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.run(
            [sys.executable, str(BUILD), "--output-dir", tmp],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            errors.append(f"build.py failed: {proc.stderr.strip() or proc.stdout.strip()}")
        else:
            for name in ("prompt-engineering-guide.md", "gpts-knowledge.md", "gems-knowledge.md"):
                path = Path(tmp) / name
                if not path.exists():
                    errors.append(f"builder did not produce {name}")
                    continue
                text = path.read_text(encoding="utf-8")
                if "GENERATED FILE — DO NOT EDIT DIRECTLY" not in text:
                    errors.append(f"{name} missing generated-file header")
                if "registry/models.yaml" not in text:
                    errors.append(f"{name} missing registry source section")
                if "skills/prompt-engineering/core/prompt-contract.md" not in text:
                    errors.append(f"{name} missing Prompt Contract source")
                if "skills/prompt-engineering/tasks/research.md" not in text:
                    errors.append(f"{name} missing Task Profile source")
                if "skills/prompt-engineering/models/openai.md" not in text:
                    errors.append(f"{name} missing Model Profile source")

    if errors:
        print("v4 distribution validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("v4 distribution validation OK")
    print(f"GPTs adapter bytes: {GPTS.stat().st_size}")
    print(f"Gems adapter bytes: {GEMS.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
