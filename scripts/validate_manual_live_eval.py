#!/usr/bin/env python3
"""Guardrails for the manually-triggered paid/live evaluation workflow."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "v4-live-eval-manual.yml"

errors: list[str] = []
if not WORKFLOW.exists():
    errors.append("manual live evaluation workflow is missing")
else:
    text = WORKFLOW.read_text(encoding="utf-8")
    required = [
        "workflow_dispatch:",
        "permissions:\n      contents: read",
        "--limit \"${{ inputs.max_jobs }}\"",
        "validate_eval_candidates.py",
        "prepare_blind_judging.py",
        "actions/upload-artifact@v4",
        "OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}",
        "ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}",
        "GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}",
        "COMPAT_API_KEY: ${{ secrets.COMPAT_API_KEY }}",
    ]
    for marker in required:
        if marker not in text:
            errors.append(f"manual workflow missing required marker: {marker}")

    forbidden = [
        "pull_request:",
        "schedule:",
        "push:\n",
        "contents: write",
        "git push",
        "registry/models.yaml",
        "release-review.yaml",
    ]
    for marker in forbidden:
        if marker in text:
            errors.append(f"manual live workflow contains forbidden behavior/trigger: {marker}")

    if "-gt 100" not in text:
        errors.append("manual workflow does not enforce the maximum job bound")

if errors:
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("manual live evaluation workflow validation passed")
