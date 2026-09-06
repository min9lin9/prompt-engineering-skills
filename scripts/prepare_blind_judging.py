#!/usr/bin/env python3
"""Prepare blinded judge items from transport-only evaluation results."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path


def stable_id(record: dict) -> str:
    target = record.get("target") or {}
    raw = "|".join(str(x) for x in [
        record.get("experiment_id"), record.get("case_id"), record.get("repeat"),
        target.get("model"), target.get("runtime"), record.get("strategy"),
        (record.get("inputs") or {}).get("prompt_sha256"),
    ])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--mapping-out", required=True, type=Path)
    parser.add_argument("--seed", type=int, default=20260906)
    args = parser.parse_args()

    records = [json.loads(line) for line in args.results.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not records:
        raise SystemExit("no transport results found")

    rng = random.Random(args.seed)
    shuffled = list(records)
    rng.shuffle(shuffled)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.mapping_out.parent.mkdir(parents=True, exist_ok=True)
    judge_lines: list[str] = []
    mapping_lines: list[str] = []

    for index, record in enumerate(shuffled, 1):
        item_id = stable_id(record)
        opaque = f"candidate-{index:04d}"
        target = record.get("target") or {}
        item = {
            "judge_item_id": item_id,
            "candidate_label": opaque,
            "case_id": record.get("case_id"),
            "dataset": record.get("dataset"),
            "case_prompt": (record.get("inputs") or {}).get("source_snapshot"),
            "target": {"model": target.get("model"), "runtime": target.get("runtime")},
            "raw_output": record.get("raw_output"),
            "rubric": "evals/rubric.md",
            "required_hard_gates": record.get("hard_gates", []),
        }
        mapping = {
            "judge_item_id": item_id,
            "candidate_label": opaque,
            "strategy": record.get("strategy"),
            "execution_key": {
                "experiment_id": record.get("experiment_id"),
                "case_id": record.get("case_id"),
                "repeat": record.get("repeat"),
                "model": target.get("model"),
                "runtime": target.get("runtime"),
                "prompt_sha256": (record.get("inputs") or {}).get("prompt_sha256"),
            },
        }
        judge_lines.append(json.dumps(item, ensure_ascii=False, sort_keys=True))
        mapping_lines.append(json.dumps(mapping, ensure_ascii=False, sort_keys=True))

    args.out.write_text("\n".join(judge_lines) + "\n", encoding="utf-8")
    args.mapping_out.write_text("\n".join(mapping_lines) + "\n", encoding="utf-8")
    print(f"prepared {len(judge_lines)} blinded judge item(s) with seed {args.seed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
