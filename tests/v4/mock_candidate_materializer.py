#!/usr/bin/env python3
"""Synthetic candidate materializer used only by CI."""
import hashlib
import json
import sys

job = json.loads(sys.stdin.read())
strategy = job.get("strategy")
if strategy not in {"legacy", "v4"}:
    raise SystemExit("mock materializer only supports legacy or v4")
base = job.get("case_prompt") or ""
prompt = f"[{strategy.upper()} SYNTHETIC CANDIDATE]\n\n{base}"
print(json.dumps({
    "strategy": strategy,
    "prompt": prompt,
    "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
    "generator_model": "synthetic-ci",
    "generator_runtime": "mock",
    "materializer_revision": "synthetic-ci-v1"
}))
