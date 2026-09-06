#!/usr/bin/env python3
from pathlib import Path
import py_compile
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    ROOT / "scripts" / "run_candidate_materializers.py",
    ROOT / "tests" / "v4" / "mock_candidate_materializer.py",
    ROOT / "docs" / "v4" / "CANDIDATE_GENERATION_BRIDGE.md",
]
errors = []
for path in required:
    if not path.exists():
        errors.append(f"missing {path.relative_to(ROOT)}")
for path in required[:2]:
    if path.exists():
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:
            errors.append(f"compile failed {path.relative_to(ROOT)}: {exc}")

bridge = (ROOT / "scripts" / "run_candidate_materializers.py").read_text(encoding="utf-8") if required[0].exists() else ""
checks = {
    "no shell execution": "shell=True" not in bridge and "os.system" not in bridge,
    "hash recomputation": "hashlib.sha256" in bridge,
    "legacy materializer": "--legacy-materializer" in bridge,
    "v4 materializer": "--v4-materializer" in bridge,
    "neutral deterministic path": "neutral_prompt" in bridge,
    "strategy mismatch guard": "strategy mismatch" in bridge,
    "revision required": "materializer_revision is required" in bridge,
}
for name, ok in checks.items():
    if not ok:
        errors.append(f"failed contract check: {name}")

if errors:
    print("candidate bridge validation FAILED")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print("candidate bridge validation OK")
