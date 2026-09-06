#!/usr/bin/env python3
"""Static validation for the v4 evaluation framework.

This validates dataset/rubric/result-contract integrity only. It does not run
providers or claim model-quality evidence.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"
REGISTRY = ROOT / "registry" / "models.yaml"

REQUIRED_FILES = (
    "README.md",
    "rubric.md",
    "baselines.md",
    "result-schema.md",
    "cases/development.yaml",
    "cases/holdout.yaml",
)

ALLOWED_TASKS = {
    "research",
    "fact-check",
    "coding",
    "analysis",
    "writing",
    "editing",
    "extraction",
    "agent",
    "image",
    "video",
    "slides",
}

SPECIAL_TARGETS = {"FutureModel-X", "ambiguous-alias"}


def case_ids(text: str) -> list[str]:
    return re.findall(r"(?m)^\s*- id:\s*([^\s]+)\s*$", text)


def task_values(text: str) -> list[str]:
    return re.findall(r"(?m)^\s+task:\s*([^\s]+)\s*$", text)


def target_values(text: str) -> list[str]:
    values: list[str] = []
    for raw in re.findall(r"(?m)^\s+target_matrix:\s*\[([^\]]*)\]", text):
        values.extend(item.strip() for item in raw.split(",") if item.strip())
    return values


def registry_models(text: str) -> set[str]:
    in_models = False
    result: set[str] = set()
    for raw in text.splitlines():
        if raw == "models:":
            in_models = True
            continue
        if not in_models:
            continue
        if raw and not raw.startswith(" "):
            break
        match = re.match(r"^  ([\w.-]+):\s*$", raw)
        if match:
            result.add(match.group(1))
    return result


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (EVALS / rel).exists():
            errors.append(f"missing eval file: evals/{rel}")

    if errors:
        for error in errors:
            print(f"- {error}")
        return 1

    dev = (EVALS / "cases/development.yaml").read_text(encoding="utf-8")
    holdout = (EVALS / "cases/holdout.yaml").read_text(encoding="utf-8")
    rubric = (EVALS / "rubric.md").read_text(encoding="utf-8")
    baselines = (EVALS / "baselines.md").read_text(encoding="utf-8")
    schema = (EVALS / "result-schema.md").read_text(encoding="utf-8")
    readme = (EVALS / "README.md").read_text(encoding="utf-8")
    registry_text = REGISTRY.read_text(encoding="utf-8")
    known_models = registry_models(registry_text)

    if "split: development" not in dev:
        errors.append("development dataset missing split marker")
    if "split: holdout" not in holdout:
        errors.append("holdout dataset missing split marker")

    dev_ids = case_ids(dev)
    holdout_ids = case_ids(holdout)
    all_ids = dev_ids + holdout_ids

    if len(all_ids) != len(set(all_ids)):
        errors.append("evaluation case IDs must be globally unique")
    if len(dev_ids) < 8:
        errors.append("development dataset must contain at least 8 cases")
    if len(holdout_ids) < 6:
        errors.append("holdout dataset must contain at least 6 cases")

    for task in task_values(dev + "\n" + holdout):
        if task not in ALLOWED_TASKS:
            errors.append(f"unknown task profile in eval case: {task}")

    for target in target_values(dev + "\n" + holdout):
        if target not in known_models and target not in SPECIAL_TARGETS:
            errors.append(f"eval target not present in registry: {target}")

    for required in ("legacy", "neutral", "v4"):
        if required not in baselines.lower():
            errors.append(f"baseline definition missing: {required}")

    for required in (
        "Requirement satisfaction",
        "Source fidelity",
        "Permission boundary",
        "Model/runtime compatibility",
        "Hard gates",
    ):
        if required not in rubric:
            errors.append(f"rubric missing dimension/section: {required}")

    for required in (
        "experiment_id:",
        "case_id:",
        "strategy:",
        "target:",
        "prompt_sha256:",
        "hard_gate_pass:",
        "code_revision:",
    ):
        if required not in schema:
            errors.append(f"result schema missing field: {required}")

    if "Do not tune prompt profiles against holdout outcomes" not in readme:
        errors.append("holdout anti-tuning policy is missing")

    if "quality_evaluated: true" in registry_text:
        errors.append("registry claims quality_evaluated before target-model outcome runs exist")

    if errors:
        print("v4 evaluation framework validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("v4 evaluation framework validation OK")
    print(f"development cases: {len(dev_ids)}")
    print(f"holdout cases: {len(holdout_ids)}")
    print("quality evidence: not yet claimed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
