#!/usr/bin/env python3
"""Reference executor for Anthropic Messages API.

Official endpoint: POST https://api.anthropic.com/v1/messages
Credential: ANTHROPIC_API_KEY
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

from _common import emit, env_required, load_job, transport_result


def main() -> int:
    job = load_job()
    api_key = env_required("ANTHROPIC_API_KEY")
    target = job["target"]
    prompt = job["candidate"]["prompt"]
    base = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com").rstrip("/")
    payload = {
        "model": target["model"],
        "max_tokens": int(os.getenv("ANTHROPIC_MAX_TOKENS", "4096")),
        "messages": [{"role": "user", "content": prompt}],
    }
    req = urllib.request.Request(
        base + "/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "x-api-key": api_key,
            "anthropic-version": os.getenv("ANTHROPIC_VERSION", "2023-06-01"),
            "Content-Type": "application/json",
        },
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:2000]
        raise SystemExit(f"Anthropic HTTP {exc.code}: {detail}")
    latency_ms = int((time.perf_counter() - started) * 1000)

    text = "\n".join(
        block.get("text", "")
        for block in data.get("content") or []
        if block.get("type") == "text" and block.get("text")
    )
    usage = data.get("usage") or {}
    emit(transport_result(
        job,
        output_text=text,
        input_tokens=usage.get("input_tokens"),
        output_tokens=usage.get("output_tokens"),
        latency_ms=latency_ms,
        model_version=data.get("model"),
        stop_reason=data.get("stop_reason"),
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
