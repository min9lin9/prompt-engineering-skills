#!/usr/bin/env python3
"""Prepare a deterministic evaluation plan without calling providers.

The produced plan contains case metadata and the original holdout task text, but it
is not executable release evidence until each row receives an immutable candidate
prompt according to evals/candidate-contract.md.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPERIMENT = ROOT / "evals" / "experiments" / "frontier-release-candidate.json"
HOLDOUT = ROOT / "evals" / "cases" / "holdout.yaml"
REGISTRY = ROOT / "registry" / "models.yaml"


def parse_holdout(text: str) -> dict[str, dict]:
    cases: dict[str, dict] = {}
    blocks = re.split(r"(?m)^\s*- id:\s*", text)[1:]
    for block in blocks:
        lines = block.splitlines()
        case_id = lines[0].strip()
        task_match = re.search(r"(?m)^\s*task:\s*([^\n#]+)", block)
        prompt_match = re.search(r"(?m)^\s*prompt:\s*([^\n#]+)", block)
        targets_match = re.search(r"(?m)^\s*target_matrix:\s*\[([^\]]*)\]", block)
        gates_match = re.search(r"(?m)^\s*hard_gates:\s*\[([^\]]*)\]", block)
        targets = [x.strip() for x in targets_match.group(1).split(",")] if targets_match else []
        hard_gates = [x.strip() for x in gates_match.group(1).split(",")] if gates_match else []
        cases[case_id] = {
            "task": task_match.group(1).strip() if task_match else None,
            "prompt": prompt_match.group(1).strip() if prompt_match else None,
            "targets": targets,
            "hard_gates": hard_gates,
        }
    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", default=str(DEFAULT_EXPERIMENT))
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    experiment_path = Path(args.experiment)
    experiment = json.loads(experiment_path.read_text(encoding="utf-8"))
    holdout = parse_holdout(HOLDOUT.read_text(encoding="utf-8"))
    registry = REGISTRY.read_text(encoding="utf-8")

    target_by_model = {item["model"]: item for item in experiment["targets"]}
    errors: list[str] = []

    for model in target_by_model:
        if not re.search(rf"(?m)^\s{{2}}{re.escape(model)}:\s*$", registry):
            errors.append(f"experiment target missing from Registry: {model}")

    for case_id in experiment["cases"]:
        if case_id not in holdout:
            errors.append(f"experiment case missing from holdout dataset: {case_id}")
        elif not holdout[case_id].get("prompt"):
            errors.append(f"holdout case has no prompt text: {case_id}")

    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    rows: list[dict] = []
    for case_id in experiment["cases"]:
        case = holdout[case_id]
        applicable = [model for model in case["targets"] if model in target_by_model]
        if not applicable:
            errors.append(f"no experiment target applies to case: {case_id}")
            continue
        for model in applicable:
            target = target_by_model[model]
            for strategy in experiment["strategies"]:
                for repeat in range(1, int(experiment["repeats"]) + 1):
                    rows.append({
                        "experiment_id": experiment["experiment_id"],
                        "dataset": experiment["dataset"],
                        "case_id": case_id,
                        "task": case["task"],
                        "case_prompt": case["prompt"],
                        "strategy": strategy,
                        "repeat": repeat,
                        "target": target,
                        "hard_gates": case["hard_gates"],
                        "candidate": None,
                        "status": "needs_candidate",
                    })

    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    output = Path(args.output) if args.output else ROOT / "evals" / "results" / experiment["experiment_id"] / "plan.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")

    providers = sorted({row["target"]["provider"] for row in rows})
    models = sorted({row["target"]["model"] for row in rows})
    print(f"prepared {len(rows)} candidate-pending execution(s)")
    print(f"providers: {', '.join(providers)}")
    print(f"models: {', '.join(models)}")
    print(f"output: {output.relative_to(ROOT) if output.is_relative_to(ROOT) else output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
