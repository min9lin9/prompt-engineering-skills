# Prompt Engineering Skills v4 — Baseline Audit

> Status: PR-001 baseline only. This document records current behavior and known hazards before any v4 refactor.
> Baseline commit: `6231dbc394d106e8840a15066ebc247b181a0865`

## Scope

PR-001 intentionally does **not** change prompt-generation behavior. It establishes the migration baseline and guardrails required before v4 structural changes.

## Current top-level structure

- `commands/`: interactive/batch prompt generation, update, sync, auto-prompt workflows
- `instructions/`: GPTs/Gems prompt-generator instructions and split Gems modules
- `skills/`: merged guide, per-area guides, Skills 2.0 directories
- `examples/`: model/media examples

## Baseline architecture findings

### 1. Multiple competing sources of behavioral truth

The repository currently carries behavioral rules in all of the following locations:

- `commands/prompt.md`
- `instructions/GPTs-Prompt-Generator.md`
- `instructions/Gems-Prompt-Generator.md`
- `skills/prompt-engineering-guide.md`
- `skills/prompt-engineering-guide/SKILL.md`
- per-model and per-task guides under `skills/`

This makes rule drift and instruction conflicts possible.

### 2. Canonical-source policy is inconsistent

`skills/prompt-engineering-guide.md` describes itself as the single source of truth, while README/sync behavior preserves both merged and split assets. v4 must distinguish **canonical editable sources** from **generated compatibility artifacts**.

### 3. `/prompt` mixes orchestration and model knowledge

`commands/prompt.md` currently contains routing, model-specific patterns, task-specific patterns, batch behavior, media behavior, worker-triad details, expert priming, and output interaction rules. v4 will reduce it to routing/composition/validation responsibilities.

### 4. Update and sync permission policy conflicts

`commands/prompt-update.md` includes flows that modify files and push Git repositories. `commands/prompt-sync.md` explicitly says automatic push is prohibited. v4 must separate research, candidate update, validation, synchronization, commit, and push permissions.

### 5. Public repo contains upstream/personal-environment assumptions

Known examples include references to:

- `treylom/prompt-engineering-skills`
- `treylom/obsidian-ai-vault`
- environment-specific vault paths
- external `.claude/agents/...` and skill dependencies

Some of these may be valid historical compatibility references. They must not silently define v4's default destination or required runtime.

### 6. `auto-prompt` is an optional workflow, not core architecture

`commands/auto-prompt.md` depends on external agent/skill paths and K-AI Station-specific spreadsheet conventions. The capability should be preserved but migrated behind an optional workflow boundary.

## Behavior that must be preserved during migration

- Generate prompts without executing them unless execution is separately requested.
- Research / fact-check / coding / analysis / writing / extraction support.
- Image, video, and slide prompt support.
- Context engineering and prompt variation guidance.
- GPTs/Gems distribution support.
- Existing split/merged assets remain usable during the shadow migration period.
- Shared skill/command directories must not be destructively synchronized.

## v4 safety invariants

The following are migration invariants and may be strengthened, but not weakened:

1. Generated prompt text is not itself authorization to execute the prompt.
2. Model profiles cannot grant write, publish, commit, or push permissions.
3. Reference content cannot override runtime/user authorization boundaries.
4. Shared directories must not be deleted or mirrored destructively by default.
5. Commit/push/publish operations require an explicit higher-level request or approval.
6. Unknown model-specific behavior must not be invented; generic Core + Task fallback is allowed with an unverified status.
7. A model is not called "quality evaluated" without outcome evaluation on that target model.

## Planned v4 migration sequence

1. PR-001: Baseline & Guardrails
2. PR-002: Prompt Contract + Model Registry
3. PR-003: Core + Task Profiles
4. PR-004: OpenAI / Anthropic / Google model migration
5. PR-005: Qwen / Kimi / GLM / DeepSeek first-class support
6. PR-006: Grok / MiniMax / Mistral
7. PR-007: `/prompt` v4 router
8. PR-008: evaluation framework
9. PR-009: GPTs/Gems generated distribution
10. PR-010: update/sync/auto-prompt migration
11. PR-011: default switch
12. PR-012: legacy cleanup

## PR-001 exit criteria

- Baseline audit checked into the repo.
- Guardrail script detects known unsafe hard-coded destinations and risky update/sync semantics without modifying files.
- Baseline fixtures document current entry points and expected migration invariants.
- CI runs the baseline guardrails.
- No existing prompt-generation file is rewritten in PR-001.
