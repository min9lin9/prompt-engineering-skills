#!/usr/bin/env python3
"""Assess release evidence without changing Registry or router defaults."""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "evals" / "release-gate.yaml"
REVIEW = ROOT / "evals" / "release-review.yaml"


def gate_int(name: str, text: str) -> int:
    m = re.search(rf"(?m)^\s*{re.escape(name)}:\s*(\d+)\s*$", text)
    if not m:
        raise SystemExit(f"release gate missing integer {name}")
    return int(m.group(1))


def gate_list(name: str, text: str) -> list[str]:
    m = re.search(rf"(?m)^\s*{re.escape(name)}:\s*\[([^\]]*)\]\s*$", text)
    if not m:
        return []
    return [x.strip() for x in m.group(1).split(",") if x.strip()]


def load_records(paths: list[Path]) -> list[dict]:
    out = []
    for path in paths:
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            obj = json.loads(raw)
            if not isinstance(obj, dict):
                raise SystemExit(f"{path}:{line_no}: record must be object")
            out.append(obj)
    if not out:
        raise SystemExit("no evidence records")
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("paths", nargs="+", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--allow-test-fixtures", action="store_true")
    args = p.parse_args()

    if not args.allow_test_fixtures:
        for path in args.paths:
            try:
                path.resolve().relative_to((ROOT / "tests").resolve())
                raise SystemExit("test fixtures cannot be used as release evidence")
            except ValueError:
                pass

    records = load_records(args.paths)
    gate = GATE.read_text(encoding="utf-8")
    required_strategies = set(gate_list("required_strategies", gate) or ["legacy", "neutral", "v4"])
    min_repeats = gate_int("min_repeats_per_case", gate)
    min_providers = gate_int("min_verified_provider_families", gate)
    min_models = gate_int("min_verified_target_models", gate)

    hard_gate_failures = []
    bad_dataset = []
    providers, models = set(), set()
    coverage = defaultdict(lambda: defaultdict(set))
    score_rows = defaultdict(lambda: defaultdict(list))

    for record in records:
        if record.get("dataset") != "holdout":
            bad_dataset.append(record.get("case_id"))
        target = record.get("target") or {}
        provider, model = target.get("provider"), target.get("model")
        if provider:
            providers.add(provider)
        if model:
            models.add(model)
        if (record.get("outcome") or {}).get("hard_gate_pass") is not True:
            hard_gate_failures.append({"case_id": record.get("case_id"), "model": model, "strategy": record.get("strategy")})
        key = (record.get("case_id"), model, target.get("runtime"))
        strategy = record.get("strategy")
        if strategy:
            coverage[key][strategy].add(record.get("repeat"))
        scores = (record.get("outcome") or {}).get("scores") or {}
        vals = [v for v in scores.values() if isinstance(v, (int, float)) and not isinstance(v, bool)]
        if vals and strategy:
            score_rows[key][strategy].append(sum(vals) / len(vals))

    coverage_gaps = []
    for key, by_strategy in coverage.items():
        for strategy in required_strategies:
            repeats = {r for r in by_strategy.get(strategy, set()) if isinstance(r, int)}
            if len(repeats) < min_repeats:
                coverage_gaps.append({"case_model_runtime": key, "strategy": strategy, "observed_repeats": sorted(repeats)})

    deltas = []
    for key, by_strategy in score_rows.items():
        if all(s in by_strategy and by_strategy[s] for s in ["legacy", "neutral", "v4"]):
            avg = {s: sum(by_strategy[s]) / len(by_strategy[s]) for s in ["legacy", "neutral", "v4"]}
            deltas.append({
                "case_model_runtime": key,
                "legacy": avg["legacy"],
                "neutral": avg["neutral"],
                "v4": avg["v4"],
                "v4_minus_neutral": avg["v4"] - avg["neutral"],
                "v4_minus_legacy": avg["v4"] - avg["legacy"],
            })

    machine_pass = (
        not hard_gate_failures
        and not bad_dataset
        and not coverage_gaps
        and len(providers) >= min_providers
        and len(models) >= min_models
    )

    review_text = REVIEW.read_text(encoding="utf-8")
    review_approved = bool(re.search(r"(?m)^status:\s*approved\s*$", review_text))
    material_review_approved = bool(re.search(r"(?m)^material_regression_review:\s*approved\s*$", review_text))

    report = {
        "machine_gate_pass": machine_pass,
        "release_approved": machine_pass and review_approved and material_review_approved,
        "provider_count": len(providers),
        "model_count": len(models),
        "providers": sorted(providers),
        "models": sorted(models),
        "hard_gate_failures": hard_gate_failures,
        "non_holdout_records": bad_dataset,
        "coverage_gaps": coverage_gaps,
        "score_deltas": deltas,
        "human_review_status": "approved" if review_approved else "pending",
        "material_regression_review": "approved" if material_review_approved else "pending",
        "note": "Machine assessment never changes Registry maturity or router defaults."
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if machine_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
