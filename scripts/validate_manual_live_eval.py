#!/usr/bin/env python3
"""Guardrails for the manually-triggered paid/live evaluation workflow."""

from pathlib import Path
import py_compile
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "v4-live-eval-manual.yml"
MATERIALIZER = ROOT / "executors" / "openai_prompt_materializer.py"
SELECTOR = ROOT / "scripts" / "select_eval_smoke.py"

errors: list[str] = []
if not WORKFLOW.exists():
    errors.append("manual live evaluation workflow is missing")
else:
    text = WORKFLOW.read_text(encoding="utf-8")
    required = [
        "workflow_dispatch:",
        "permissions:\n      contents: read",
        "target_provider:",
        "target_model:",
        "smoke_cases:",
        "materializer_model:",
        "select_eval_smoke.py",
        "run_candidate_materializers.py",
        "openai_prompt_materializer.py",
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

    if "-gt 10" not in text:
        errors.append("manual workflow does not enforce the smoke-case bound")
    if "/tmp/smoke-ready.jsonl" not in text:
        errors.append("manual workflow does not pass a validated ready plan to target execution")

for path in (MATERIALIZER, SELECTOR):
    if not path.exists():
        errors.append(f"required live-eval helper is missing: {path.relative_to(ROOT)}")
        continue
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError as exc:
        errors.append(f"python compile failed for {path.relative_to(ROOT)}: {exc.msg}")

if MATERIALIZER.exists():
    materializer_text = MATERIALIZER.read_text(encoding="utf-8")
    for marker in ["OPENAI_API_KEY", "PROMPT_MATERIALIZER_MODEL", "commands/prompt-legacy.md", "commands/prompt.md"]:
        if marker not in materializer_text:
            errors.append(f"materializer missing required marker: {marker}")
    if "sk-" in materializer_text:
        errors.append("materializer appears to contain a literal API key")
    if "shell=True" in materializer_text or "os.system" in materializer_text:
        errors.append("materializer contains forbidden shell execution")

if errors:
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("manual live evaluation workflow validation passed")
