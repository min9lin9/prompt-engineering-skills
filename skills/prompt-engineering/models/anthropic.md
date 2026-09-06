---
provider: anthropic
version: 1
verified_at: 2026-09-06
---

# Anthropic Provider Profile

## Scope
Provider-level Claude facts. Task behavior remains model-neutral; model-specific thinking and migration differences belong in deltas.

## Confirmed
- Claude API uses the Messages API for current Claude models.
- Current Claude models support structured outputs through `output_config.format` where listed as compatible by Anthropic.
- Adaptive thinking is the current thinking mechanism for Claude 4.6+ and Claude 5 families.
- Thinking configuration and sampling restrictions vary by model; resolve them from the selected model delta/registry rather than assuming provider-wide equivalence.

Official references:
- https://platform.claude.com/docs/en/claude_api_primer
- https://platform.claude.com/docs/en/build-with-claude/structured-outputs

## Evaluated
- None yet. No Anthropic-wide prompt strategy has passed v4 outcome evaluation.

## Experimental
- XML sectioning from the legacy Claude guide remains an optional formatting strategy, not a provider requirement.
- Explicit scope wording for literal instruction-following should be evaluated per task rather than enabled globally.

## Boundary
Do not repeat Core rules, infer hidden chain-of-thought, or grant execution permissions.
