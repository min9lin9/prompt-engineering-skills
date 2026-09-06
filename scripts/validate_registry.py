#!/usr/bin/env python3
"""Static validation for the v4 model registry.

This validator intentionally checks only structural/capability claims that are
represented in registry/models.yaml. It does not claim integration or quality
verification.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "models.yaml"

LIFECYCLES = {"frontier", "stable", "legacy", "experimental", "deprecated"}
SUPPORT_FIELDS = {
    "spec_verified",
    "static_validation",
    "integration_verified",
    "quality_evaluated",
}


def parse_scalar(value: str):
    value = value.strip()
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [item.strip() for item in inner.split(",")]
    return value


def load_minimal_registry(text: str):
    """Parse the intentionally simple registry subset without external deps."""
    models = {}
    current_model = None
    section = None
    subsection = None

    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()

        if indent == 2 and line.endswith(":") and line != "models:":
            current_model = line[:-1]
            models[current_model] = {}
            section = None
            subsection = None
            continue
        if current_model is None:
            continue
        if indent == 4 and line.endswith(":"):
            section = line[:-1]
            models[current_model][section] = {}
            subsection = None
            continue
        if indent == 6 and line.endswith(":"):
            subsection = line[:-1]
            models[current_model][section][subsection] = {}
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed = parse_scalar(value)
        if indent == 4:
            models[current_model][key] = parsed
        elif indent == 6 and section:
            models[current_model][section][key] = parsed
        elif indent == 8 and section and subsection:
            models[current_model][section][subsection][key] = parsed

    return models


def main() -> int:
    if not REGISTRY.exists():
        print("ERROR: registry/models.yaml is missing")
        return 1

    models = load_minimal_registry(REGISTRY.read_text(encoding="utf-8"))
    errors = []
    aliases = {}

    if not models:
        errors.append("registry contains no models")

    for model_id, model in models.items():
        for field in ("provider", "family", "lifecycle", "capabilities", "runtime", "support"):
            if field not in model:
                errors.append(f"{model_id}: missing required field {field}")

        lifecycle = model.get("lifecycle")
        if lifecycle not in LIFECYCLES:
            errors.append(f"{model_id}: invalid lifecycle {lifecycle!r}")

        for alias in model.get("aliases", []) or []:
            normalized = alias.lower()
            previous = aliases.get(normalized)
            if previous and previous != model_id:
                errors.append(f"duplicate alias {alias!r}: {previous} and {model_id}")
            aliases[normalized] = model_id

        support = model.get("support", {})
        missing_support = SUPPORT_FIELDS.difference(support)
        if missing_support:
            errors.append(f"{model_id}: missing support fields {sorted(missing_support)}")
        if support.get("quality_evaluated") and not support.get("integration_verified"):
            errors.append(f"{model_id}: quality_evaluated requires integration_verified")

        reasoning = model.get("reasoning", {})
        values = reasoning.get("values", []) if isinstance(reasoning, dict) else []
        if model_id == "gpt-6-astra" and "none" in values:
            errors.append("gpt-6-astra: reasoning 'none' must not be allowed")
        if model_id == "kimi-k3" and "medium" in values:
            errors.append("kimi-k3: reasoning 'medium' must not be allowed")
        if model_id == "gemini-3.8-flash" and "minimal" in values:
            errors.append("gemini-3.8-flash: thinking 'minimal' must not be allowed")

    if re.search(r"treylom/(?:prompt-engineering-skills|obsidian-ai-vault)", REGISTRY.read_text(encoding="utf-8")):
        errors.append("registry must not hard-code legacy upstream repositories")

    if errors:
        print("v4 registry validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"v4 registry validation OK: {len(models)} models")
    print("note: static validation does not imply integration or quality evaluation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
