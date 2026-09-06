#!/usr/bin/env python3
"""Run prepared v4 evaluation jobs through an external executor.

The repository intentionally does not embed provider credentials or SDKs. Each job
is serialized as one JSON object to the executor's stdin. The executor must emit
exactly one result JSON object on stdout using evals/result-schema.md.

Example:
  python scripts/prepare_eval_run.py ... > /tmp/plan.jsonl
  python scripts/run_eval_jobs.py --plan /tmp/plan.jsonl \
    --executor ./local/provider_executor.py --out /tmp/results.jsonl

The executor is invoked without a shell. Environment/credential handling is owned
by the caller's runtime, not this repository.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def load_plan(path: Path) -> list[dict]:
    jobs: list[dict] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            job = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"invalid plan JSON at line {lineno}: {exc}") from exc
        if not isinstance(job, dict):
            raise SystemExit(f"plan line {lineno} is not a JSON object")
        jobs.append(job)
    if not jobs:
        raise SystemExit("evaluation plan is empty")
    return jobs


def execution_key(job: dict) -> tuple:
    target = job.get("target") or {}
    return (
        job.get("experiment_id"),
        job.get("case_id"),
        job.get("strategy"),
        job.get("repeat"),
        target.get("provider"),
        target.get("model"),
        target.get("runtime"),
    )


def run_one(executor: list[str], job: dict, timeout: int) -> dict:
    proc = subprocess.run(
        executor,
        input=json.dumps(job, ensure_ascii=False) + "\n",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"executor failed for {execution_key(job)} with exit {proc.returncode}: "
            f"{proc.stderr.strip()[:1000]}"
        )

    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        raise RuntimeError(
            f"executor must emit exactly one JSON line for {execution_key(job)}; got {len(lines)}"
        )
    try:
        result = json.loads(lines[0])
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"executor emitted invalid JSON for {execution_key(job)}: {exc}") from exc
    if not isinstance(result, dict):
        raise RuntimeError(f"executor result is not an object for {execution_key(job)}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--executor", required=True, nargs="+", help="Executable and arguments; no shell expansion")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--limit", type=int, default=0, help="0 means all jobs")
    parser.add_argument("--resume", action="store_true", help="Skip execution keys already present in --out")
    args = parser.parse_args()

    jobs = load_plan(args.plan)
    if args.limit > 0:
        jobs = jobs[: args.limit]

    existing: set[tuple] = set()
    if args.resume and args.out.exists():
        for raw in args.out.read_text(encoding="utf-8").splitlines():
            if not raw.strip():
                continue
            try:
                existing.add(execution_key(json.loads(raw)))
            except Exception:
                raise SystemExit("cannot resume from malformed existing result file")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if args.resume and args.out.exists() else "w"
    completed = 0
    with args.out.open(mode, encoding="utf-8") as fh:
        for job in jobs:
            key = execution_key(job)
            if key in existing:
                continue
            result = run_one(args.executor, job, args.timeout)
            fh.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")
            fh.flush()
            completed += 1
            print(f"completed {completed}: {key}", file=sys.stderr)

    print(f"wrote {completed} result(s) to {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
