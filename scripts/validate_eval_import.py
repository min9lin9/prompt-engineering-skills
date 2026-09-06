#!/usr/bin/env python3
"""Validate imported/live evaluation JSONL before it can be used by the release gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "models.yaml"
VALID_STRATEGIES = {"legacy", "forced-legacy", "neutral", "v4", "v4-experimental"}
VALID_FAILURES = {
    None, "none", "invalid_prompt_contract", "unsupported_runtime_setting",
    "provider_error", "rate_limit", "timeout", "truncated_output",
    "schema_invalid", "source_violation", "permission_violation",
    "factual_fabrication", "incomplete", "judge_error"
}
REQUIRED_SCORE_KEYS = {
    "requirement_satisfaction", "intent_preservation", "source_fidelity",
    "output_contract", "grounding", "permission_boundary",
    "model_runtime_compatibility", "unnecessary_clarification",
    "instruction_efficiency", "completion_quality"
}


def validate_record(record: dict, registry: str, source: str, line_no: int) -> list[str]:
    prefix = f"{source}:{line_no}"
    errors: list[str] = []
    required_top = ["experiment_id", "case_id", "dataset", "strategy", "repeat", "target", "inputs", "outcome", "provenance"]
    for key in required_top:
        if key not in record:
            errors.append(f"{prefix}: missing {key}")

    if record.get("strategy") not in VALID_STRATEGIES:
        errors.append(f"{prefix}: invalid strategy {record.get('strategy')!r}")
    if record.get("dataset") not in {"development", "holdout"}:
        errors.append(f"{prefix}: invalid dataset {record.get('dataset')!r}")
    if not isinstance(record.get("repeat"), int) or record.get("repeat", 0) < 1:
        errors.append(f"{prefix}: repeat must be a positive integer")

    target = record.get("target") or {}
    model = target.get("model")
    provider = target.get("provider")
    runtime = target.get("runtime")
    if not all([model, provider, runtime]):
        errors.append(f"{prefix}: target provider/model/runtime are required")
    elif not re.search(rf"(?m)^\s{{2}}{re.escape(str(model))}:\s*$", registry):
        errors.append(f"{prefix}: target model not found in Registry: {model}")

    inputs = record.get("inputs") or {}
    prompt_hash = inputs.get("prompt_sha256")
    if not isinstance(prompt_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", prompt_hash):
        errors.append(f"{prefix}: prompt_sha256 must be 64 lowercase hex chars")

    outcome = record.get("outcome") or {}
    if outcome.get("hard_gate_pass") not in {True, False}:
        errors.append(f"{prefix}: outcome.hard_gate_pass must be boolean")
    if outcome.get("failure_class") not in VALID_FAILURES:
        errors.append(f"{prefix}: invalid failure_class {outcome.get('failure_class')!r}")

    scores = outcome.get("scores") or {}
    missing_scores = REQUIRED_SCORE_KEYS - set(scores)
    if missing_scores:
        errors.append(f"{prefix}: missing score keys {sorted(missing_scores)}")
    for key in REQUIRED_SCORE_KEYS & set(scores):
        value = scores[key]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 4:
            errors.append(f"{prefix}: score {key} must be numeric 0..4")

    provenance = record.get("provenance") or {}
    for key in ["run_at", "code_revision", "profile_revision"]:
        if not provenance.get(key):
            errors.append(f"{prefix}: missing provenance.{key}")

    telemetry = record.get("telemetry") or {}
    for key in ["input_tokens", "output_tokens", "latency_ms", "cost_usd"]:
        if key in telemetry and telemetry[key] is not None:
            value = telemetry[key]
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
                errors.append(f"{prefix}: telemetry.{key} must be non-negative or null")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()

    registry = REGISTRY.read_text(encoding="utf-8")
    errors: list[str] = []
    count = 0
    seen_keys: set[tuple] = set()

    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            errors.append(f"missing result file: {path}")
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            count += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{path}:{line_no}: invalid JSON: {exc}")
                continue
            errors.extend(validate_record(record, registry, str(path), line_no))
            target = record.get("target") or {}
            key = (record.get("experiment_id"), record.get("case_id"), record.get("strategy"), record.get("repeat"), target.get("model"), target.get("runtime"))
            if key in seen_keys:
                errors.append(f"{path}:{line_no}: duplicate execution key {key}")
            seen_keys.add(key)

    if count == 0:
        errors.append("no evaluation records found")

    if errors:
        print("evaluation import validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("evaluation import validation OK")
    print(f"records: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
