#!/usr/bin/env python3
"""Reference executor for OpenAI-compatible Chat Completions transports.

Intended for providers/runtimes that explicitly expose an OpenAI-compatible
`/v1/chat/completions` endpoint. Compatibility is transport-level only; provider
semantics and reasoning controls remain governed by the v4 Registry/Model Delta.

Environment:
  COMPAT_API_KEY      required
  COMPAT_BASE_URL     required, e.g. https://provider.example/v1
  COMPAT_AUTH_HEADER  optional, default Authorization
  COMPAT_AUTH_PREFIX  optional, default "Bearer "
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
    api_key = env_required("COMPAT_API_KEY")
    base = env_required("COMPAT_BASE_URL").rstrip("/")
    header_name = os.getenv("COMPAT_AUTH_HEADER", "Authorization")
    prefix = os.getenv("COMPAT_AUTH_PREFIX", "Bearer ")
    prompt = job["candidate"]["prompt"]
    model = job["target"]["model"]

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }
    req = urllib.request.Request(
        base + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={header_name: prefix + api_key, "Content-Type": "application/json"},
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:2000]
        raise SystemExit(f"compatible API HTTP {exc.code}: {detail}")
    latency_ms = int((time.perf_counter() - started) * 1000)

    text = ""
    finish_reason = None
    choices = data.get("choices") or []
    if choices:
        first = choices[0]
        finish_reason = first.get("finish_reason")
        content = (first.get("message") or {}).get("content")
        if isinstance(content, str):
            text = content
    usage = data.get("usage") or {}
    emit(transport_result(
        job,
        output_text=text,
        input_tokens=usage.get("prompt_tokens"),
        output_tokens=usage.get("completion_tokens"),
        latency_ms=latency_ms,
        model_version=data.get("model") or model,
        stop_reason=finish_reason,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
