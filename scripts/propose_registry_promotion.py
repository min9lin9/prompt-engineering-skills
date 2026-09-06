#!/usr/bin/env python3
"""Generate a review-only support-maturity promotion proposal from evaluated evidence."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "models.yaml"


def load_records(paths: list[Path]) -> list[dict]:
    out = []
    for path in paths:
        for raw in path.read_text(encoding="utf-8").splitlines():
            if raw.strip():
                out.append(json.loads(raw))
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("paths", nargs="+", type=Path)
    p.add_argument("--assessment", required=True, type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--allow-test-fixtures", action="store_true")
    args = p.parse_args()

    assessment = json.loads(args.assessment.read_text(encoding="utf-8"))
    if not assessment.get("machine_gate_pass"):
        raise SystemExit("machine release gate has not passed; no promotion proposal")

    if not args.allow_test_fixtures:
        for path in args.paths:
            try:
                path.resolve().relative_to((ROOT / "tests").resolve())
                raise SystemExit("test fixtures cannot produce a real promotion proposal")
            except ValueError:
                pass

    registry = REGISTRY.read_text(encoding="utf-8")
    by_model = defaultdict(list)
    for record in load_records(args.paths):
        model = (record.get("target") or {}).get("model")
        if model:
            by_model[model].append(record)

    proposals = []
    for model, records in sorted(by_model.items()):
        if f"  {model}:\n" not in registry:
            continue
        strategies = {r.get("strategy") for r in records}
        hard_ok = all((r.get("outcome") or {}).get("hard_gate_pass") is True for r in records)
        holdout_only = all(r.get("dataset") == "holdout" for r in records)
        provenance_ok = all(all((r.get("provenance") or {}).get(k) for k in ["run_at", "code_revision", "profile_revision"]) for r in records)
        target_completed = all((r.get("outcome") or {}).get("completed") is True for r in records)
        integration_candidate = target_completed and provenance_ok
        quality_candidate = integration_candidate and hard_ok and holdout_only and {"legacy", "neutral", "v4"}.issubset(strategies)
        proposals.append({
            "model": model,
            "integration_verified_candidate": integration_candidate,
            "quality_evaluated_candidate": quality_candidate,
            "record_count": len(records),
            "strategies": sorted(s for s in strategies if s),
            "action": "review_only_no_registry_write"
        })

    payload = {
        "assessment_release_approved": bool(assessment.get("release_approved")),
        "proposals": proposals,
        "warning": "This file is a proposal only. It does not modify registry/models.yaml. Human review is required before support maturity changes."
    }
    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
