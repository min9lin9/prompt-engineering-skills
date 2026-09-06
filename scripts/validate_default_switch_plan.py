#!/usr/bin/env python3
"""Static guardrails for the v4 default-switch dry-run plan."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "release" / "default-switch-plan.yaml"
PLANNER = ROOT / "scripts" / "plan_default_switch.py"
ROUTER = ROOT / "commands" / "prompt.md"
REVIEW = ROOT / "evals" / "release-review.yaml"

errors: list[str] = []

for path in (PLAN, PLANNER, ROUTER, REVIEW):
    if not path.exists():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")

if not errors:
    plan = PLAN.read_text(encoding="utf-8")
    planner = PLANNER.read_text(encoding="utf-8")
    router = ROUTER.read_text(encoding="utf-8")
    review = REVIEW.read_text(encoding="utf-8")

    required_plan_markers = [
        "mode: dry-run-only",
        "mutate_router: false",
        "mutate_registry: false",
        "delete_files: false",
        "commit_or_push: false",
        "preserve_explicit_legacy_flag: true",
        "preserve_shadow_mode: true",
        "cleanup_requires_separate_pr: true",
    ]
    for marker in required_plan_markers:
        if marker not in plan:
            errors.append(f"default switch plan missing: {marker}")

    if "| no flag | `legacy`" not in router:
        errors.append("router no longer exposes legacy as the no-flag default before approval")
    if "status: pending" not in review:
        errors.append("test expects release-review.yaml to remain pending before live evidence review")

    forbidden = ["git push", "subprocess.run([\"git\"", "delete_file(", "update_file("]
    for token in forbidden:
        if token in planner:
            errors.append(f"planner contains mutation primitive: {token}")

if errors:
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("default switch dry-run plan validation passed")
