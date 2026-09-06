#!/usr/bin/env python3
"""Generate a non-mutating v4 default-switch readiness report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REVIEW = ROOT / "evals" / "release-review.yaml"
DEFAULT_PLAN = ROOT / "release" / "default-switch-plan.yaml"
ROUTER = ROOT / "commands" / "prompt.md"


def scalar(text: str, key: str) -> str | None:
    prefix = f"{key}:"
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(prefix):
            value = line[len(prefix):].strip()
            return None if value in {"null", "~", ""} else value
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    review = args.review.read_text(encoding="utf-8")
    plan = args.plan.read_text(encoding="utf-8")
    router = ROUTER.read_text(encoding="utf-8")

    review_status = scalar(review, "status") or "unknown"
    regression_status = scalar(review, "material_regression_review") or "unknown"
    machine_assessment = scalar(review, "machine_assessment")

    blockers: list[str] = []
    if review_status != "approved":
        blockers.append(f"release review status is {review_status!r}, not 'approved'")
    if regression_status != "approved":
        blockers.append(f"material regression review is {regression_status!r}, not 'approved'")
    if machine_assessment in {None, "null"}:
        blockers.append("machine assessment is missing")
    if "| no flag | `legacy`" not in router:
        blockers.append("router no-flag legacy default marker is missing; inspect manually")
    if "mutate_router: false" not in plan or "delete_files: false" not in plan:
        blockers.append("dry-run plan safety invariants are missing")

    report = {
        "release_candidate": scalar(plan, "release_candidate") or "v4-default-switch",
        "mode": "dry-run",
        "ready_for_switch_pr": not blockers,
        "blockers": blockers,
        "current_default": "legacy",
        "proposed_default": "v4",
        "proposed_changes": [
            "change only the no-flag default route from legacy to v4",
            "retain --legacy and --shadow compatibility paths",
            "retain commands/prompt-legacy.md during observation",
            "defer legacy deletion/archive work to a separate reviewed cleanup PR",
        ],
        "mutations_performed": [],
    }

    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
