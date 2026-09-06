#!/usr/bin/env python3
"""Static guardrails for reference provider executors."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXECUTORS = [
    ROOT / "executors" / "openai_responses.py",
    ROOT / "executors" / "anthropic_messages.py",
    ROOT / "executors" / "gemini_generate_content.py",
    ROOT / "executors" / "openai_compatible_chat.py",
]


def main() -> int:
    errors: list[str] = []
    for path in EXECUTORS:
        if not path.exists():
            errors.append(f"missing executor: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if "load_job()" not in text:
            errors.append(f"{path.name}: must validate materialized candidate through load_job()")
        if "env_required(" not in text:
            errors.append(f"{path.name}: credentials/config must come from environment")
        if "shell=True" in text or "os.system(" in text:
            errors.append(f"{path.name}: shell execution is forbidden")
        if re.search(r"(?i)(sk-[a-z0-9_-]{12,}|api[_-]?key\s*=\s*['\"][^'\"]{8,})", text):
            errors.append(f"{path.name}: possible embedded credential")

    common = (ROOT / "executors" / "_common.py").read_text(encoding="utf-8")
    for required in ["prompt_sha256", "hashlib.sha256", "Transport-only result"]:
        if required not in common:
            errors.append(f"_common.py missing invariant: {required}")

    candidate_contract = (ROOT / "evals" / "candidate-contract.md").read_text(encoding="utf-8")
    if "Sending the raw holdout case prompt directly" not in candidate_contract:
        errors.append("candidate contract must forbid raw-case model-capability-only evaluation")

    for path in [ROOT / "executors" / "_common.py", *EXECUTORS]:
        proc = subprocess.run([sys.executable, "-m", "py_compile", str(path)], capture_output=True, text=True)
        if proc.returncode != 0:
            errors.append(f"{path.name}: Python compile failed: {proc.stderr.strip()}")

    if errors:
        print("reference executor validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("reference executor validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
