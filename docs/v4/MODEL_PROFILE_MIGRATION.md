# v4 Provider / Model Profile Migration

> PR-004 scope: OpenAI, Anthropic, Google only. Legacy model guides remain available during shadow migration.

## Migration rule

v4 model knowledge is split into three evidence levels:

1. **Confirmed** — facts supported by current official provider documentation.
2. **Evaluated** — prompt strategies that have passed v4 target-model outcome evaluation.
3. **Experimental** — plausible strategies awaiting evaluation.

Only Confirmed facts are used as compatibility constraints in PR-004. No legacy prompt recommendation is automatically promoted to Evaluated.

## OpenAI

Legacy source: `skills/gpt-5.5-prompt-enhancement.md`.

Migrated now:
- provider/runtime separation;
- model-specific reasoning compatibility;
- GPT-6 Astra delta and invalid `reasoning.effort=none` guard.

Not yet promoted:
- outcome-first wording as a universal OpenAI default;
- fixed retrieval budgets;
- fixed reasoning-effort recommendations by task.

## Anthropic

Legacy source: `skills/claude-4.7-prompt-strategies.md`.

Migrated now:
- Messages API / structured-output capability boundary;
- Claude 5 adaptive-thinking differences;
- Fable/Mythos always-on thinking constraints;
- Sonnet 5 sampling/manual-thinking migration constraints.

Not yet promoted:
- XML as a required Claude prompt syntax;
- mandatory tool-use or subagent wording;
- model ranking heuristics.

## Google

Legacy source: `skills/gemini-3.1-prompt-strategies.md`.

Migrated now:
- `thinking_level` capability boundary;
- Gemini 3.8 Flash supported thinking levels;
- `minimal` incompatibility and migration away from `thinking_budget`.

Not yet promoted:
- mandatory context/task separator syntax;
- fixed long-context placement rules;
- forced explicit planning/self-critique prompts.

## Compatibility policy

Legacy files are not deleted in PR-004. They remain available for shadow comparisons and backwards compatibility until later distribution/default-switch milestones.

Provider/model profiles cannot grant execution, write, publish, commit, or push permissions. Runtime compatibility facts do not override Prompt Contract source or output constraints.
