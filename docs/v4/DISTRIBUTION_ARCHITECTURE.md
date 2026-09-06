# v4 Distribution Architecture

## Purpose

PR-009 separates canonical prompt-engineering knowledge from platform-specific runtime instructions.

## Canonical sources

The editable sources of truth are:

- `skills/prompt-engineering/core/`
- `skills/prompt-engineering/tasks/`
- `skills/prompt-engineering/models/`
- `registry/models.yaml`

Platform adapters must not duplicate these technical rules.

## Thin adapters

`instructions/GPTs-Prompt-Generator.md` and `instructions/Gems-Prompt-Generator.md` now contain only:

- product role;
- operation modes;
- knowledge-routing order;
- execution boundary;
- model-unknown fallback behavior;
- output behavior;
- evidence-level handling.

They intentionally do not contain model rankings, provider capability tables, mandatory expert debates, mandatory five-option menus, or model-specific prompt templates.

## Legacy snapshots

The pre-v4 platform instructions are preserved verbatim under:

- `legacy/instructions/GPTs-Prompt-Generator.md`
- `legacy/instructions/Gems-Prompt-Generator.md`

These snapshots exist for migration review and regression comparison. They are not canonical sources for new v4 behavior.

## Generated knowledge packs

`scripts/build.py` deterministically concatenates the canonical sources into three distribution files:

- `generated/prompt-engineering-guide.md`
- `generated/gpts-knowledge.md`
- `generated/gems-knowledge.md`

The generated files are build artifacts, not hand-edited source files. GitHub Actions builds them and uploads them as the `prompt-engineering-v4-knowledge-packs` artifact.

## Why generated files are not canonical

Checking a manually maintained unified guide into the canonical editing path would recreate the old drift problem. The builder makes the direction one-way:

```text
Core + Task + Model + Registry
            |
            v
        build.py
            |
            v
Generated knowledge packs
```

Changes must flow from canonical source to generated output, never the reverse.

## Validation

`scripts/validate_distribution.py` enforces:

- thin-adapter size budgets;
- required execution and evidence boundaries;
- absence of selected legacy couplings;
- existence of legacy snapshots;
- successful deterministic generation;
- inclusion of Core, Task, Model, and Registry material in each pack.

Passing this validation does not imply target-model quality evaluation or provider integration verification.
