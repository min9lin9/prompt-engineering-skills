#!/usr/bin/env python3
"""Validate executable evaluation candidates before provider execution."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

HEX64 = re.compile(r"^[0-9a-f]{64}$")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()

    errors: list[str] = []
    count = 0
    for raw_path in args.paths:
        path = Path(raw_path)
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            count += 1
            record = json.loads(raw)
            prefix = f"{path}:{line_no}"
            if not record.get("case_prompt"):
                errors.append(f"{prefix}: missing case_prompt")
            candidate = record.get("candidate")
            if not isinstance(candidate, dict):
                errors.append(f"{prefix}: missing candidate object")
                continue
            prompt = candidate.get("prompt")
            digest = candidate.get("prompt_sha256")
            if not isinstance(prompt, str) or not prompt.strip():
                errors.append(f"{prefix}: candidate.prompt must be non-empty")
            if not isinstance(digest, str) or not HEX64.fullmatch(digest):
                errors.append(f"{prefix}: candidate.prompt_sha256 must be 64 lowercase hex chars")
            elif isinstance(prompt, str):
                actual = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
                if digest != actual:
                    errors.append(f"{prefix}: candidate prompt hash mismatch")
            for key in ["materialized_at", "materializer_revision"]:
                if not candidate.get(key):
                    errors.append(f"{prefix}: missing candidate.{key}")
            if record.get("status") != "ready":
                errors.append(f"{prefix}: executable candidate status must be ready")

    if count == 0:
        errors.append("no candidate records found")
    if errors:
        print("candidate validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"candidate validation OK: {count} record(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
