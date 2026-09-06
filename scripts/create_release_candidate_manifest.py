#!/usr/bin/env python3
"""Create or verify an immutable release-candidate manifest.

The manifest binds one judged release-evidence bundle to its generated report,
machine assessment, human review record, and the code/profile revisions that the
evidence claims to evaluate. It never approves a release or mutates Registry state.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise SystemExit("evidence bundle is empty")
    return rows


def evidence_metadata(rows: list[dict]) -> dict:
    experiments = {row.get("experiment_id") for row in rows}
    datasets = {row.get("dataset") for row in rows}
    code_revs = {(row.get("provenance") or {}).get("code_revision") for row in rows}
    profile_revs = {(row.get("provenance") or {}).get("profile_revision") for row in rows}
    if len(experiments) != 1 or None in experiments:
        raise SystemExit("manifest requires exactly one non-empty experiment_id")
    if datasets != {"holdout"}:
        raise SystemExit("manifest evidence must be holdout-only")
    if None in code_revs or None in profile_revs:
        raise SystemExit("every evidence row must identify code/profile revision")
    return {
        "experiment_id": next(iter(experiments)),
        "dataset": "holdout",
        "result_count": len(rows),
        "providers": sorted({(r.get("target") or {}).get("provider") for r in rows if (r.get("target") or {}).get("provider")}),
        "models": sorted({(r.get("target") or {}).get("model") for r in rows if (r.get("target") or {}).get("model")}),
        "strategies": sorted({r.get("strategy") for r in rows if r.get("strategy")}),
        "code_revisions": sorted(code_revs),
        "profile_revisions": sorted(profile_revs),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--evidence", required=True, type=Path)
    p.add_argument("--report", required=True, type=Path)
    p.add_argument("--assessment", required=True, type=Path)
    p.add_argument("--review", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--verify", action="store_true")
    args = p.parse_args()

    files = {
        "evidence": args.evidence,
        "report": args.report,
        "assessment": args.assessment,
        "review": args.review,
    }
    for label, path in files.items():
        if not path.is_file():
            raise SystemExit(f"{label} file missing: {path}")

    metadata = evidence_metadata(load_jsonl(args.evidence))
    current = {
        "version": 1,
        "release_candidate": "v4-default-switch",
        "evidence": metadata,
        "artifacts": {
            label: {"path": str(path), "sha256": digest(path)} for label, path in files.items()
        },
    }

    if args.verify:
        if not args.out.is_file():
            raise SystemExit("manifest file missing for verification")
        expected = json.loads(args.out.read_text(encoding="utf-8"))
        if expected != current:
            raise SystemExit("release-candidate manifest mismatch: evidence or review artifacts changed")
        print("release-candidate manifest verification passed")
        return 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote release-candidate manifest: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
