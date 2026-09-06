#!/usr/bin/env python3
"""Reference executor for Gemini generateContent API.

Official endpoint pattern:
  POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent
Credential: GEMINI_API_KEY
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

from _common import emit, env_required, load_job, transport_result


def main() -> int:
    job = load_job()
    api_key = env_required("GEMINI_API_KEY")
    model = job["target"]["model"]
    prompt = job["candidate"]["prompt"]
    base = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta").rstrip("/")
    url = f"{base}/models/{urllib.parse.quote(model, safe='')}:generateContent?key={urllib.parse.quote(api_key, safe='')}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:2000]
        raise SystemExit(f"Gemini HTTP {exc.code}: {detail}")
    latency_ms = int((time.perf_counter() - started) * 1000)

    parts: list[str] = []
    finish_reason = None
    for candidate in data.get("candidates") or []:
        finish_reason = finish_reason or candidate.get("finishReason")
        for part in (candidate.get("content") or {}).get("parts") or []:
            if isinstance(part.get("text"), str):
                parts.append(part["text"])
    usage = data.get("usageMetadata") or {}
    emit(transport_result(
        job,
        output_text="\n".join(parts),
        input_tokens=usage.get("promptTokenCount"),
        output_tokens=usage.get("candidatesTokenCount"),
        latency_ms=latency_ms,
        model_version=model,
        stop_reason=finish_reason,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
