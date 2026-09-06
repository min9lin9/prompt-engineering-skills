#!/usr/bin/env python3
"""Assemble judged evaluation shards into one release-evidence JSONL bundle."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> list[dict]:
    rows = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise SystemExit(f"{path}:{lineno}: result must be an object")
        rows.append(row)
    if not rows:
        raise SystemExit(f"{path}: no result rows")
    return rows


def key(row: dict) -> tuple:
    target = row.get("target") or {}
    return (
        row.get("experiment_id"),
        row.get("case_id"),
        row.get("strategy"),
        row.get("repeat"),
        target.get("provider"),
        target.get("model"),
        target.get("runtime"),
    )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("inputs", nargs="+", type=Path)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--summary", type=Path)
    args = p.parse_args()

    all_rows: list[dict] = []
    experiments: set[str] = set()
    datasets: set[str] = set()
    seen: dict[tuple, dict] = {}

    for path in args.inputs:
        for row in load(path):
            experiment_id = row.get("experiment_id")
            dataset = row.get("dataset")
            if not experiment_id:
                raise SystemExit(f"{path}: result missing experiment_id")
            if dataset != "holdout":
                raise SystemExit(f"{path}: release evidence must use holdout data only")
            experiments.add(str(experiment_id))
            datasets.add(str(dataset))
            outcome = row.get("outcome") or {}
            scores = outcome.get("scores")
            if not isinstance(scores, dict) or not scores:
                raise SystemExit(f"{path}: result is not judged/scored: {key(row)}")
            judge = row.get("judge") or {}
            if not judge.get("method"):
                raise SystemExit(f"{path}: result is missing judge provenance: {key(row)}")
            inputs = row.get("inputs") or {}
            if not inputs.get("prompt_sha256"):
                raise SystemExit(f"{path}: result missing prompt hash: {key(row)}")
            provenance = row.get("provenance") or {}
            if not provenance.get("code_revision") or not provenance.get("profile_revision"):
                raise SystemExit(f"{path}: result missing release provenance: {key(row)}")

            k = key(row)
            if k in seen:
                prior = seen[k]
                prior_hash = (prior.get("inputs") or {}).get("prompt_sha256")
                this_hash = inputs.get("prompt_sha256")
                if prior_hash != this_hash:
                    raise SystemExit(f"conflicting duplicate execution key with different prompt hash: {k}")
                raise SystemExit(f"duplicate execution key: {k}")
            seen[k] = row
            all_rows.append(row)

    if len(experiments) != 1:
        raise SystemExit(f"release evidence cannot mix experiment ids: {sorted(experiments)}")
    if datasets != {"holdout"}:
        raise SystemExit(f"unexpected dataset mix: {sorted(datasets)}")

    all_rows.sort(key=lambda r: tuple(str(v) for v in key(r)))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in all_rows),
        encoding="utf-8",
    )

    providers = sorted({(r.get("target") or {}).get("provider") for r in all_rows})
    models = sorted({(r.get("target") or {}).get("model") for r in all_rows})
    strategies = sorted({r.get("strategy") for r in all_rows})
    hard_gate_failures = sum(1 for r in all_rows if not (r.get("outcome") or {}).get("hard_gate_pass"))
    summary = {
        "experiment_id": next(iter(experiments)),
        "dataset": "holdout",
        "result_count": len(all_rows),
        "providers": providers,
        "models": models,
        "strategies": strategies,
        "hard_gate_failures": hard_gate_failures,
        "input_shards": [str(p) for p in args.inputs],
    }
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
