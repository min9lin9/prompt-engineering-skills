#!/usr/bin/env python3
"""Reference executor for OpenAI Responses API.

Official endpoint: POST https://api.openai.com/v1/responses
Credential: OPENAI_API_KEY
Optional base URL override: OPENAI_BASE_URL (default https://api.openai.com/v1)
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

from _common import emit, env_required, load_job, transport_result


def main() -> int:
    job = load_job()
    api_key = env_required("OPENAI_API_KEY")
    target = job["target"]
    model = target["model"]
    prompt = job["candidate"]["prompt"]

    import os
    base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    payload = {"model": model, "input": prompt}
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        base + "/responses",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:2000]
        raise SystemExit(f"OpenAI HTTP {exc.code}: {detail}")
    latency_ms = int((time.perf_counter() - started) * 1000)

    output_text = data.get("output_text") or ""
    if not output_text:
        parts = []
        for item in data.get("output") or []:
            for content in item.get("content") or []:
                if content.get("type") in {"output_text", "text"} and content.get("text"):
                    parts.append(content["text"])
        output_text = "\n".join(parts)

    usage = data.get("usage") or {}
    result = transport_result(
        job,
        output_text=output_text,
        input_tokens=usage.get("input_tokens"),
        output_tokens=usage.get("output_tokens"),
        latency_ms=latency_ms,
        model_version=data.get("model"),
        stop_reason=data.get("status"),
    )
    emit(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
