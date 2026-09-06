#!/usr/bin/env python3
"""Merge validated blind judgments back into transport results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SCORE_KEYS = {
    "requirement_satisfaction", "intent_preservation", "source_fidelity",
    "output_contract", "grounding", "permission_boundary",
    "model_runtime_compatibility", "unnecessary_clarification",
    "instruction_efficiency", "completion_quality",
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def exec_key(record: dict) -> tuple:
    target = record.get("target") or {}
    return (
        record.get("experiment_id"), record.get("case_id"), record.get("repeat"),
        target.get("model"), target.get("runtime"), (record.get("inputs") or {}).get("prompt_sha256"),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--mapping", required=True, type=Path)
    parser.add_argument("--judgments", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    results = read_jsonl(args.results)
    mappings = read_jsonl(args.mapping)
    judgments = read_jsonl(args.judgments)
    by_item = {item["judge_item_id"]: item for item in mappings}
    judged = {item["judge_item_id"]: item for item in judgments}

    if len(judged) != len(judgments):
        raise SystemExit("duplicate judge_item_id in judgments")

    result_by_key = {exec_key(item): item for item in results}
    if len(result_by_key) != len(results):
        raise SystemExit("duplicate transport execution key")

    output: list[dict] = []
    used: set[str] = set()
    for item_id, mapping in by_item.items():
        if item_id not in judged:
            raise SystemExit(f"missing judgment for {item_id}")
        judgment = judged[item_id]
        scores = judgment.get("scores") or {}
        if set(scores) != SCORE_KEYS:
            raise SystemExit(f"{item_id}: judgment score keys do not match rubric")
        for key, value in scores.items():
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 4:
                raise SystemExit(f"{item_id}: invalid score {key}={value!r}")
        if judgment.get("hard_gate_pass") not in {True, False}:
            raise SystemExit(f"{item_id}: hard_gate_pass must be boolean")

        key_fields = mapping["execution_key"]
        key = (
            key_fields["experiment_id"], key_fields["case_id"], key_fields["repeat"],
            key_fields["model"], key_fields["runtime"], key_fields["prompt_sha256"],
        )
        if key not in result_by_key:
            raise SystemExit(f"{item_id}: mapping does not match any transport result")
        record = json.loads(json.dumps(result_by_key[key]))
        if record.get("strategy") != mapping.get("strategy"):
            raise SystemExit(f"{item_id}: strategy mapping mismatch")

        record["outcome"]["hard_gate_pass"] = judgment["hard_gate_pass"]
        record["outcome"]["scores"] = scores
        if not judgment["hard_gate_pass"] and record["outcome"].get("failure_class") in {None, "none"}:
            failures = judgment.get("hard_gate_failures") or []
            record["outcome"]["failure_class"] = "permission_violation" if any("permission" in str(x) for x in failures) else "incomplete"
        record["judge"] = judgment.get("judge") or {"method": "human", "judge_model": None, "notes": ""}
        record["judge"]["randomized_position"] = mapping.get("candidate_label")
        output.append(record)
        used.add(item_id)

    extras = set(judged) - used
    if extras:
        raise SystemExit(f"judgments contain unknown item ids: {sorted(extras)}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in output), encoding="utf-8")
    print(f"wrote {len(output)} judged result(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
