#!/usr/bin/env python3
"""Materialize deterministic neutral evaluation candidates.

This helper intentionally materializes only the neutral baseline. Legacy and v4
candidates should be produced by their respective prompt-generation paths so the
comparison measures the actual strategies rather than hand-written approximations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


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
        parts.append("Critical acceptance conditions: " + ", ".join(str(x) for x in gates) + ".")
    return "\n\n".join(parts)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--materializer-revision", default="deterministic-neutral-v1")
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    count = 0

    with args.out.open("w", encoding="utf-8") as out:
        for lineno, raw in enumerate(args.plan.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            job = json.loads(raw)
            strategy = job.get("strategy")
            if strategy != "neutral":
                continue
            prompt = neutral_prompt(job)
            job["candidate"] = {
                "prompt": prompt,
                "prompt_sha256": sha256(prompt),
                "generator_model": None,
                "generator_runtime": None,
                "materialized_at": now,
                "materializer_revision": args.materializer_revision,
            }
            job["status"] = "ready"
            out.write(json.dumps(job, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1

    if count == 0:
        raise SystemExit("no neutral jobs were materialized")
    print(f"materialized {count} neutral candidate(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
