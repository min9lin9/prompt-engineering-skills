#!/usr/bin/env python3
"""Select a balanced legacy/neutral/v4 smoke subset from an evaluation plan."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = ("legacy", "neutral", "v4")


def load(path: Path) -> list[dict]:
    rows = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            rows.append(json.loads(raw))
    if not rows:
        raise SystemExit("input plan is empty")
    return rows


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--plan", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--provider", required=True)
    p.add_argument("--model")
    p.add_argument("--cases", type=int, default=1)
    args = p.parse_args()
    if args.cases < 1 or args.cases > 10:
        raise SystemExit("--cases must be between 1 and 10")

    rows = [r for r in load(args.plan) if (r.get("target") or {}).get("provider") == args.provider]
    if args.model:
        rows = [r for r in rows if (r.get("target") or {}).get("model") == args.model]
    if not rows:
        raise SystemExit("no rows match requested provider/model")

    groups: dict[tuple, dict[str, dict]] = {}
    for row in rows:
        key = (
            row.get("case_id"),
            row.get("repeat"),
            (row.get("target") or {}).get("provider"),
            (row.get("target") or {}).get("model"),
            (row.get("target") or {}).get("runtime"),
        )
        groups.setdefault(key, {})[row.get("strategy")] = row

    selected = []
    for key in sorted(groups, key=lambda x: tuple(str(v) for v in x)):
        by_strategy = groups[key]
        if all(s in by_strategy for s in REQUIRED):
            selected.extend(by_strategy[s] for s in REQUIRED)
            if len(selected) >= args.cases * len(REQUIRED):
                break

    if len(selected) != args.cases * len(REQUIRED):
        raise SystemExit(
            f"requested {args.cases} balanced case(s), found only {len(selected) // len(REQUIRED)}"
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in selected),
        encoding="utf-8",
    )
    models = sorted({(r.get("target") or {}).get("model") for r in selected})
    print(f"selected {len(selected)} job(s): {args.cases} balanced legacy/neutral/v4 case(s)")
    print("models: " + ", ".join(models))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
