#!/usr/bin/env python3
"""Materialize legacy or v4 prompt candidates using one fixed OpenAI generator model.

This executor is for candidate generation, not target-model evaluation. It reads one
pending evaluation job from stdin and emits one candidate JSON object on stdout.
Credentials come only from OPENAI_API_KEY. The generator model is controlled by
PROMPT_MATERIALIZER_MODEL and defaults to gpt-5.6-sol.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_job() -> dict:
    raw = input().strip()
    if not raw:
        raise SystemExit("materializer requires one JSON job on stdin")
    job = json.loads(raw)
    if job.get("strategy") not in {"legacy", "v4"}:
        raise SystemExit("openai_prompt_materializer only accepts legacy or v4 jobs")
    return job


def v4_context(job: dict) -> str:
    task = str(job.get("task") or "analysis").strip()
    target = job.get("target") or {}
    provider = str(target.get("provider") or "").strip().lower()
    pieces = [
        read("commands/prompt.md"),
        read("skills/prompt-engineering/core/prompt-contract.md"),
        read("skills/prompt-engineering/core/principles.md"),
        read("skills/prompt-engineering/core/validation.md"),
        read("registry/models.yaml"),
    ]
    task_path = ROOT / "skills" / "prompt-engineering" / "tasks" / f"{task}.md"
    if task_path.exists():
        pieces.append(task_path.read_text(encoding="utf-8"))
    provider_path = ROOT / "skills" / "prompt-engineering" / "models" / f"{provider}.md"
    if provider_path.exists():
        pieces.append(provider_path.read_text(encoding="utf-8"))
    provider_dir = provider_path.with_suffix("")
    if provider_dir.is_dir():
        model_name = str(target.get("model") or "").lower()
        for child in sorted(provider_dir.glob("*.md")):
            stem = child.stem.lower()
            if stem in model_name or model_name in stem:
                pieces.append(child.read_text(encoding="utf-8"))
                break
    return "\n\n---\n\n".join(pieces)


def build_input(job: dict) -> str:
    strategy = job["strategy"]
    framework = read("commands/prompt-legacy.md") if strategy == "legacy" else v4_context(job)
    target = job.get("target") or {}
    request = job.get("case_prompt") or ""
    return f"""You are materializing one prompt candidate for a controlled evaluation.

Strategy under test: {strategy}
Target provider: {target.get('provider')}
Target model: {target.get('model')}
Target runtime: {target.get('runtime')}
Task type: {job.get('task')}

Framework instructions to apply:
<framework>
{framework}
</framework>

User request to turn into a finished prompt:
<request>
{request}
</request>

Return exactly one finished prompt for the target model. Do not execute the task.
Do not discuss the framework, strategy name, evaluation, or your reasoning. Do not
wrap the result in a Markdown code fence.
"""


def main() -> int:
    job = load_job()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required")
    model = os.getenv("PROMPT_MATERIALIZER_MODEL", "gpt-5.6-sol")
    base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    payload = {"model": model, "input": build_input(job)}
    req = urllib.request.Request(
        base + "/responses",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:2000]
        raise SystemExit(f"OpenAI materializer HTTP {exc.code}: {detail}")

    prompt = data.get("output_text") or ""
    if not prompt:
        parts = []
        for item in data.get("output") or []:
            for content in item.get("content") or []:
                if content.get("type") in {"output_text", "text"} and content.get("text"):
                    parts.append(content["text"])
        prompt = "\n".join(parts)
    prompt = prompt.strip()
    if not prompt:
        raise SystemExit("materializer returned empty prompt")

    result = {
        "strategy": job["strategy"],
        "prompt": prompt,
        "prompt_sha256": sha256(prompt),
        "generator_model": data.get("model") or model,
        "generator_runtime": "openai-responses",
        "materialized_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "materializer_revision": "openai-prompt-materializer-v1",
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
