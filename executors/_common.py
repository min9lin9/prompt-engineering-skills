#!/usr/bin/env python3
"""Shared helpers for reference evaluation executors."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any

SCORE_KEYS = [
    "requirement_satisfaction", "intent_preservation", "source_fidelity",
    "output_contract", "grounding", "permission_boundary",
    "model_runtime_compatibility", "unnecessary_clarification",
    "instruction_efficiency", "completion_quality",
]


def load_job() -> dict[str, Any]:
    lines = [line for line in sys.stdin.read().splitlines() if line.strip()]
    if len(lines) != 1:
        raise SystemExit("executor requires exactly one JSON job on stdin")
    job = json.loads(lines[0])
    candidate = job.get("candidate")
    if not isinstance(candidate, dict):
        raise SystemExit("job has no materialized candidate")
    prompt = candidate.get("prompt")
    digest = candidate.get("prompt_sha256")
    if not isinstance(prompt, str) or not prompt.strip():
        raise SystemExit("candidate.prompt is missing")
    actual = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    if digest != actual:
        raise SystemExit("candidate.prompt_sha256 mismatch")
    return job


def env_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"required environment variable is not set: {name}")
    return value


def blank_scores() -> dict[str, None]:
    return {key: None for key in SCORE_KEYS}


def transport_result(job: dict[str, Any], *, output_text: str, input_tokens: int | None,
                     output_tokens: int | None, latency_ms: int | None,
                     model_version: str | None = None, stop_reason: str | None = None) -> dict[str, Any]:
    candidate = job["candidate"]
    target = dict(job.get("target") or {})
    if model_version:
        target["model_version_or_snapshot"] = model_version
    return {
        "experiment_id": job.get("experiment_id"),
        "case_id": job.get("case_id"),
        "dataset": job.get("dataset"),
        "strategy": job.get("strategy"),
        "repeat": job.get("repeat"),
        "target": target,
        "settings": {},
        "inputs": {
            "prompt_sha256": candidate["prompt_sha256"],
            "source_snapshot": job.get("case_prompt"),
        },
        "raw_output": output_text,
        "outcome": {
            "completed": bool(output_text),
            "hard_gate_pass": None,
            "scores": blank_scores(),
            "structured_output_valid": None,
            "failure_class": "none" if output_text else "incomplete",
            "stop_reason": stop_reason,
        },
        "telemetry": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_ms": latency_ms,
            "cost_usd": None,
        },
        "judge": {
            "method": "unjudged",
            "judge_model": None,
            "randomized_position": None,
            "notes": "Transport-only result. Must be judged/scored before release evidence import.",
        },
        "provenance": {
            "run_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "code_revision": os.getenv("PES_CODE_REVISION", "unknown"),
            "profile_revision": candidate.get("materializer_revision", "unknown"),
        },
    }


def emit(result: dict[str, Any]) -> None:
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
