#!/usr/bin/env python3
"""Validate the v4 default-switch release gate.

The gate is intentionally conservative: while status is `blocked`, the Router
must remain legacy-by-default. When status becomes `approved`, reproducible
holdout result evidence is required before CI can pass.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "evals" / "release-gate.yaml"
ROUTER = ROOT / "commands" / "prompt.md"
RESULTS = ROOT / "evals" / "results"
REGISTRY = ROOT / "registry" / "models.yaml"

REQUIRED_STRATEGIES = {"legacy", "neutral", "v4"}
REQUIRED_PROVIDER_FAMILIES = {"openai", "anthropic", "google", "qwen"}
MIN_MODELS = 6
MIN_REPEATS = 3


def scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*([^#\n]+?)\s*$", text)
    return match.group(1).strip().strip("'\"") if match else None


def router_default_is_legacy(text: str) -> bool:
    return (
        "| no flag | `legacy`" in text
        and "4. default `legacy`" in text
        and "Legacy behavior remains the default" in text
    )


def load_jsonl() -> list[dict]:
    records: list[dict] = []
    for path in sorted(RESULTS.glob("*/results.jsonl")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            record["__path"] = str(path.relative_to(ROOT))
            records.append(record)
    return records


def validate_approved(records: list[dict], report_path: str | None) -> list[str]:
    errors: list[str] = []
    if not report_path or report_path in {"null", "None"}:
        errors.append("approved gate requires approved_release_report")
    elif not (ROOT / report_path).exists():
        errors.append(f"approved release report does not exist: {report_path}")

    if not records:
        errors.append("approved gate requires real evaluation result records")
        return errors

    holdout = [r for r in records if r.get("dataset") == "holdout"]
    if not holdout:
        errors.append("approved gate requires holdout results")
        return errors

    strategies = {r.get("strategy") for r in holdout}
    missing_strategies = REQUIRED_STRATEGIES - strategies
    if missing_strategies:
        errors.append(f"holdout missing strategies: {sorted(missing_strategies)}")

    providers: set[str] = set()
    models: set[str] = set()
    repeats: dict[tuple[str, str, str], set[int]] = {}

    for record in holdout:
        target = record.get("target") or {}
        provider = target.get("provider")
        model = target.get("model")
        if provider:
            providers.add(provider)
        if model:
            models.add(model)

        outcome = record.get("outcome") or {}
        if outcome.get("hard_gate_pass") is not True:
            errors.append(f"hard-gate failure in {record.get('__path')} case={record.get('case_id')} strategy={record.get('strategy')}")

        inputs = record.get("inputs") or {}
        provenance = record.get("provenance") or {}
        for label, value in (
            ("prompt_sha256", inputs.get("prompt_sha256")),
            ("code_revision", provenance.get("code_revision")),
            ("profile_revision", provenance.get("profile_revision")),
        ):
            if not value:
                errors.append(f"missing {label} for case={record.get('case_id')} strategy={record.get('strategy')}")

        key = (str(record.get("case_id")), str(record.get("strategy")), str(model))
        repeat = record.get("repeat")
        if isinstance(repeat, int):
            repeats.setdefault(key, set()).add(repeat)

    missing_providers = REQUIRED_PROVIDER_FAMILIES - providers
    if missing_providers:
        errors.append(f"required provider families missing: {sorted(missing_providers)}")
    if len(models) < MIN_MODELS:
        errors.append(f"need at least {MIN_MODELS} evaluated target models, found {len(models)}")

    for key, seen in repeats.items():
        if len(seen) < MIN_REPEATS:
            errors.append(f"insufficient repeats for {key}: {len(seen)} < {MIN_REPEATS}")

    return errors


def main() -> int:
    errors: list[str] = []
    for path in (GATE, ROUTER, RESULTS, REGISTRY):
        if not path.exists():
            errors.append(f"missing required release-gate asset: {path.relative_to(ROOT)}")

    if errors:
        print("v4 release gate validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    gate_text = GATE.read_text(encoding="utf-8")
    router_text = ROUTER.read_text(encoding="utf-8")
    registry_text = REGISTRY.read_text(encoding="utf-8")
    status = scalar(gate_text, "status")
    report_path = scalar(gate_text, "approved_release_report")

    if status not in {"blocked", "approved"}:
        errors.append(f"invalid release-gate status: {status!r}")

    if status == "blocked" and not router_default_is_legacy(router_text):
        errors.append("release gate is blocked but /prompt is not explicitly legacy-by-default")

    try:
        records = load_jsonl()
    except ValueError as exc:
        errors.append(str(exc))
        records = []

    if status == "approved":
        errors.extend(validate_approved(records, report_path))

    # Maturity claims require result evidence. Static CI alone must never promote
    # integration_verified or quality_evaluated in the Registry.
    if not records:
        if re.search(r"(?m)^\s*integration_verified:\s*true\s*$", registry_text):
            errors.append("Registry claims integration_verified=true without result evidence")
        if re.search(r"(?m)^\s*quality_evaluated:\s*true\s*$", registry_text):
            errors.append("Registry claims quality_evaluated=true without result evidence")

    if errors:
        print("v4 release gate validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("v4 release gate validation OK")
    print(f"status: {status}")
    print(f"result records discovered: {len(records)}")
    if status == "blocked":
        print("default switch remains locked: legacy")
    return 0


if __name__ == "__main__":
    sys.exit(main())
