#!/usr/bin/env python3
"""Synthetic executor used only to test the live-eval runner contract."""

from __future__ import annotations

import hashlib
import json
import sys

raw = sys.stdin.read().strip()
job = json.loads(raw)
target = job.get("target") or {}
prompt_seed = json.dumps(job, sort_keys=True, ensure_ascii=False).encode("utf-8")
sha = hashlib.sha256(prompt_seed).hexdigest()

scores = {
    "requirement_satisfaction": 4,
    "intent_preservation": 4,
    "source_fidelity": 4,
    "output_contract": 4,
    "grounding": 4,
    "permission_boundary": 4,
    "model_runtime_compatibility": 4,
    "unnecessary_clarification": 4,
    "instruction_efficiency": 4,
    "completion_quality": 4,
}

result = {
    "experiment_id": job.get("experiment_id"),
    "case_id": job.get("case_id"),
    "dataset": job.get("dataset", "holdout"),
    "strategy": job.get("strategy"),
    "repeat": job.get("repeat"),
    "target": {
        "provider": target.get("provider"),
        "model": target.get("model"),
        "runtime": target.get("runtime"),
        "model_version_or_snapshot": "synthetic-test-only",
    },
    "settings": {
        "reasoning": None,
        "temperature": None,
        "max_output_tokens": None,
        "tools": [],
    },
    "inputs": {
        "prompt_sha256": sha,
        "source_snapshot": "synthetic-test-only",
    },
    "outcome": {
        "completed": True,
        "hard_gate_pass": True,
        "scores": scores,
        "structured_output_valid": True,
        "failure_class": "none",
    },
    "telemetry": {
        "input_tokens": 1,
        "output_tokens": 1,
        "latency_ms": 1,
        "cost_usd": 0.0,
    },
    "judge": {
        "method": "deterministic",
        "judge_model": None,
        "randomized_position": None,
        "notes": "synthetic CI fixture; never release evidence",
    },
    "provenance": {
        "run_at": "2026-09-06T00:00:00Z",
        "code_revision": "synthetic-ci",
        "profile_revision": "synthetic-ci",
    },
}

print(json.dumps(result, ensure_ascii=False))
