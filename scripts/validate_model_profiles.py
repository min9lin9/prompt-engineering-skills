#!/usr/bin/env python3
"""Static validation for v4 provider/model profiles.

Checks structure, official-evidence hygiene, registry linkage, and selected
provider compatibility invariants. It does not claim provider integration or
model-quality evaluation.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "skills" / "prompt-engineering" / "models"
REGISTRY = ROOT / "registry" / "models.yaml"

REQUIRED = (
    "openai.md",
    "openai/gpt-6-astra.md",
    "anthropic.md",
    "anthropic/claude-5.md",
    "google.md",
    "google/gemini-3.8-flash.md",
    "qwen.md",
    "qwen/qwen3.8-flash-next.md",
    "kimi.md",
    "kimi/kimi-k3.md",
    "glm.md",
    "glm/glm-5.3.md",
    "glm/glm-5.3-flash.md",
    "deepseek.md",
    "deepseek/deepseek-v4.md",
)
REQUIRED_SECTIONS = ("## Confirmed", "## Evaluated", "## Experimental", "## Boundary")
OFFICIAL_DOMAINS = {
    "openai": "developers.openai.com",
    "anthropic": "platform.claude.com",
    "google": "ai.google.dev",
    "qwen": "huggingface.co/Qwen",
    "moonshot": "platform.kimi.ai",
    "zai": "docs.z.ai",
    "deepseek": "api-docs.deepseek.com",
}
FORBIDDEN_DEFAULT_CLAIMS = (
    re.compile(r"\bLMArena\b", re.I),
    re.compile(r"\bbest\s+model\b", re.I),
    re.compile(r"\bmust\s+always\s+use\b", re.I),
)


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*([^\n]+)$", text)
    return match.group(1).strip() if match else None


def require_registry_block(registry_text: str, model: str, snippets: tuple[str, ...], errors: list[str]) -> None:
    match = re.search(rf"(?ms)^  {re.escape(model)}:\n(.*?)(?=^  [\w.-]+:\n|\Z)", registry_text)
    if not match:
        errors.append(f"registry missing model block: {model}")
        return
    block = match.group(1)
    for snippet in snippets:
        if snippet not in block:
            errors.append(f"{model}: registry missing invariant {snippet!r}")


def main() -> int:
    errors: list[str] = []
    registry_text = REGISTRY.read_text(encoding="utf-8") if REGISTRY.exists() else ""

    for rel in REQUIRED:
        path = MODELS / rel
        if not path.exists():
            errors.append(f"missing required profile: {rel}")
            continue

        text = path.read_text(encoding="utf-8")
        provider = frontmatter_value(text, "provider")
        if provider not in OFFICIAL_DOMAINS:
            errors.append(f"{rel}: missing/unknown provider frontmatter")
            continue

        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{rel}: missing section {section}")

        domain = OFFICIAL_DOMAINS[provider]
        if domain not in text:
            errors.append(f"{rel}: no official {provider} reference ({domain})")

        for pattern in FORBIDDEN_DEFAULT_CLAIMS:
            if pattern.search(text):
                errors.append(f"{rel}: contains unscoped ranking/default claim: {pattern.pattern}")

        model = frontmatter_value(text, "model")
        family = frontmatter_value(text, "family")
        if model and re.search(rf"(?m)^\s{{2}}{re.escape(model)}:\s*$", registry_text) is None:
            errors.append(f"{rel}: model {model!r} is not present in registry")
        if family and family not in registry_text:
            errors.append(f"{rel}: family {family!r} is not represented in registry")

        if "quality_evaluated: true" in text or "integration_verified: true" in text:
            errors.append(f"{rel}: profile must not self-promote support maturity")

    # Core compatibility invariants derived from official provider documentation.
    require_registry_block(registry_text, "kimi-k3", ("values: [low, high, max]", "always_on: true"), errors)
    require_registry_block(registry_text, "glm-5.3", ("values: [low, high, max]", "always_on: true"), errors)
    require_registry_block(registry_text, "glm-5.3-flash", ("values: [low, high, max]", "always_on: true", "multimodal: true"), errors)
    require_registry_block(registry_text, "deepseek-v4-pro", ("values: [low, high, max]", "default: high", "toggle: [enabled, disabled]"), errors)
    require_registry_block(registry_text, "deepseek-v4-flash", ("values: [low, high, max]", "default: high", "toggle: [enabled, disabled]"), errors)
    require_registry_block(registry_text, "qwen3.8-flash-next", ("structured_output: runtime-dependent", "default: runtime-dependent"), errors)

    if errors:
        print("v4 model profile validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"v4 model profile validation OK: {len(REQUIRED)} required profiles")
    print("note: profile validation does not imply provider integration or quality evaluation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
