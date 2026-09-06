#!/usr/bin/env python3
"""Materialize neutral candidates deterministically and legacy/v4 candidates via external materializers."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def neutral_prompt(job: dict) -> str:
    goal = (job.get("case_prompt") or "").strip()
    task = (job.get("task") or "task").strip()
    gates = job.get("hard_gates") or []
    parts = [
        f"Task type: {task}",
        f"Goal: {goal}",
        "Follow the supplied evidence and constraints exactly.",
        "Do not invent missing facts, permissions, model capabilities, or runtime behavior.",
        "Return only the requested deliverable and preserve any stated read-only or approval boundary.",
    ]
    if gates:
        parts.append("Critical acceptance conditions: " + ", ".join(map(str, gates)) + ".")
    return "\n\n".join(parts)


def run_materializer(command: list[str], job: dict, timeout: int) -> dict:
    proc = subprocess.run(
        command,
        input=json.dumps(job, ensure_ascii=False) + "\n",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"materializer failed ({proc.returncode}): {proc.stderr.strip()[:1000]}")
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        raise RuntimeError(f"materializer must emit exactly one JSON object; got {len(lines)} lines")
    result = json.loads(lines[0])
    if not isinstance(result, dict):
        raise RuntimeError("materializer result must be an object")
    return result


def validate_candidate(job: dict, result: dict, expected_strategy: str) -> dict:
    strategy = result.get("strategy", expected_strategy)
    if strategy != expected_strategy:
        raise RuntimeError(f"materializer strategy mismatch: expected {expected_strategy}, got {strategy}")
    prompt = result.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise RuntimeError("materializer must return non-empty prompt")
    claimed_hash = result.get("prompt_sha256")
    actual_hash = sha256(prompt)
    if claimed_hash and claimed_hash != actual_hash:
        raise RuntimeError("materializer prompt hash mismatch")
    generator_model = result.get("generator_model")
    generator_runtime = result.get("generator_runtime")
    revision = result.get("materializer_revision")
    if not revision:
        raise RuntimeError("materializer_revision is required")
    return {
        "prompt": prompt,
        "prompt_sha256": actual_hash,
        "generator_model": generator_model,
        "generator_runtime": generator_runtime,
        "materialized_at": result.get("materialized_at") or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "materializer_revision": revision,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--legacy-materializer", nargs="+")
    parser.add_argument("--v4-materializer", nargs="+")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--neutral-revision", default="deterministic-neutral-v1")
    args = parser.parse_args()

    rows = []
    for line_no, raw in enumerate(args.plan.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        job = json.loads(raw)
        strategy = job.get("strategy")
        if strategy == "neutral":
            prompt = neutral_prompt(job)
            candidate = {
                "prompt": prompt,
                "prompt_sha256": sha256(prompt),
                "generator_model": None,
                "generator_runtime": None,
                "materialized_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "materializer_revision": args.neutral_revision,
            }
        elif strategy == "legacy":
            if not args.legacy_materializer:
                raise SystemExit(f"line {line_no}: legacy materializer required")
            candidate = validate_candidate(job, run_materializer(args.legacy_materializer, job, args.timeout), "legacy")
        elif strategy == "v4":
            if not args.v4_materializer:
                raise SystemExit(f"line {line_no}: v4 materializer required")
            candidate = validate_candidate(job, run_materializer(args.v4_materializer, job, args.timeout), "v4")
        else:
            raise SystemExit(f"line {line_no}: unsupported strategy {strategy!r}")
        job["candidate"] = candidate
        job["status"] = "ready"
        rows.append(job)

    if not rows:
        raise SystemExit("no plan rows found")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    print(f"materialized {len(rows)} candidate(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
