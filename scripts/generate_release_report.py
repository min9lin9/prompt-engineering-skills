#!/usr/bin/env python3
"""Generate a conservative release-evidence report from validated JSONL results.

This script summarizes evidence; it never mutates release-gate.yaml or Registry
maturity flags. A human or separate approved change must perform promotion.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

SCORE_FIELDS = [
    "requirement_satisfaction",
    "intent_preservation",
    "source_fidelity",
    "output_contract",
    "grounding",
    "permission_boundary",
    "model_runtime_compatibility",
    "unnecessary_clarification",
    "instruction_efficiency",
    "completion_quality",
]


def load_results(paths: list[Path]) -> list[dict]:
    results: list[dict] = []
    for path in paths:
        for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
            if not isinstance(obj, dict):
                raise SystemExit(f"{path}:{lineno}: result must be an object")
            results.append(obj)
    if not results:
        raise SystemExit("no evaluation results supplied")
    return results


def score_mean(result: dict) -> float | None:
    scores = ((result.get("outcome") or {}).get("scores") or {})
    values = [scores.get(field) for field in SCORE_FIELDS]
    if any(not isinstance(v, (int, float)) for v in values):
        return None
    return sum(values) / len(values)


def fmt(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.3f}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", nargs="+", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    results = load_results(args.results)
    providers = set()
    models = set()
    hard_failures = []
    groups: dict[tuple[str, str], list[float]] = defaultdict(list)
    repeats: dict[tuple[str, str, str], set[int]] = defaultdict(set)

    for item in results:
        target = item.get("target") or {}
        provider = target.get("provider")
        model = target.get("model")
        if provider:
            providers.add(provider)
        if model:
            models.add(model)
        if (item.get("outcome") or {}).get("hard_gate_pass") is not True:
            hard_failures.append(item)
        mean = score_mean(item)
        strategy = item.get("strategy")
        if model and strategy and mean is not None:
            groups[(model, strategy)].append(mean)
        case_id = item.get("case_id")
        repeat = item.get("repeat")
        if model and strategy and case_id and isinstance(repeat, int):
            repeats[(case_id, model, strategy)].add(repeat)

    lines = [
        "# v4 Evaluation Release Evidence Report",
        "",
        "> Generated from imported evaluation results. This report is evidence summary only; it does not approve the release gate or mutate Registry maturity flags.",
        "",
        "## Coverage",
        "",
        f"- Result records: {len(results)}",
        f"- Provider families observed: {len(providers)} — {', '.join(sorted(providers))}",
        f"- Target models observed: {len(models)} — {', '.join(sorted(models))}",
        f"- Hard-gate failures: {len(hard_failures)}",
        "",
        "## Mean rubric score by model / strategy",
        "",
        "| Model | Legacy | Neutral | v4 | v4-neutral | v4-legacy |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for model in sorted(models):
        means = {}
        for strategy in ("legacy", "neutral", "v4"):
            vals = groups.get((model, strategy), [])
            means[strategy] = (sum(vals) / len(vals)) if vals else None
        vn = None if means["v4"] is None or means["neutral"] is None else means["v4"] - means["neutral"]
        vl = None if means["v4"] is None or means["legacy"] is None else means["v4"] - means["legacy"]
        lines.append(
            f"| {model} | {fmt(means['legacy'])} | {fmt(means['neutral'])} | {fmt(means['v4'])} | {fmt(vn)} | {fmt(vl)} |"
        )

    lines.extend(["", "## Repeat coverage gaps", ""])
    gaps = []
    for key, seen in sorted(repeats.items()):
        if len(seen) < 3:
            gaps.append((key, sorted(seen)))
    if not gaps:
        lines.append("No observed case/model/strategy group has fewer than three repeats.")
    else:
        for (case_id, model, strategy), seen in gaps:
            lines.append(f"- `{case_id}` / `{model}` / `{strategy}`: repeats={seen}")

    lines.extend(["", "## Release-gate interpretation", ""])
    if hard_failures:
        lines.append("- **Blocked:** at least one hard-gate violation is present.")
    else:
        lines.append("- No hard-gate violation was observed in the supplied result files.")
    lines.append("- Numeric deltas are descriptive only. `require_no_material_v4_regression` has no universal numeric tolerance in the manifest, so this script does not invent one.")
    lines.append("- Provider errors and missing evidence must be reviewed separately from model-quality failures.")
    lines.append("- Gate approval, Registry promotion, and Router default switch require a separate reviewed change.")

    text = "\n".join(lines) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
