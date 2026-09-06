# v4 `/prompt` Router Shadow Migration

> PR-007 scope: replace the legacy mega-command at `commands/prompt.md` with a thin migration router while preserving the PR-006 command verbatim as `commands/prompt-legacy.md`.

## Why this migration exists

The legacy `/prompt` command mixed orchestration, model rankings, provider-specific guidance, media prompting rules, batch worker rules, expert-role behavior, and execution/UI policy in one file.

v4 separates those responsibilities into:

- Prompt Contract
- Core principles and validation
- one primary Task Profile
- Provider / Model Delta
- Registry compatibility metadata
- User Contract

The Router selects these sources; it does not become another model guide.

## Migration modes

| Mode | Purpose | User-facing default? |
|---|---|---|
| `legacy` | exact compatibility implementation | yes during shadow migration |
| `v4` | new contract/core/task/delta composition | explicit opt-in |
| `shadow` | explicit legacy-vs-v4 comparison | evaluation only |

The no-flag route remains `legacy` in PR-007. Changing it to v4 requires a later reviewed default-switch milestone.

## Legacy snapshot integrity

`commands/prompt-legacy.md` reuses the exact PR-006 `commands/prompt.md` Git blob:

```text
6eec56007b8599ac3e833915bcb5630fc16b8b58
```

`validate_prompt_router.py` recomputes Git's blob SHA and fails if this snapshot drifts.

This prevents a shadow comparison from silently comparing v4 against a moving legacy baseline.

## v4 composition contract

```text
user request
  -> operation mode
  -> Prompt Contract
  -> Core
  -> one primary Task Profile
  -> target Provider / Model Delta when relevant
  -> User Contract
  -> compatibility validation
  -> final prompt
```

The Router must not independently maintain provider capability tables, model rankings, or model-specific prompting recipes.

## Execution boundary

The command generates/reviews/optimizes/transforms prompts. It does not treat instructions inside a generated or reviewed prompt as authorization to execute them.

No Model Delta can grant file write, publication, commit, push, purchase, or destructive-operation permission.

## Batch behavior during migration

- `--batch` without `--v4` stays on the legacy batch path.
- `--v4 --batch` returns one v4 worker prompt without the legacy interactive menu.
- `--shadow --batch` is invalid because shadow mode is a comparison artifact, not a single worker prompt.

## Evaluation boundary

Shadow mode may describe differences but must not declare v4 superior without target-model outcome evidence.

PR-007 does not set `quality_evaluated=true` for any model and does not perform provider integration tests.

## Default-switch gate

The no-flag default may move from `legacy` to `v4` only after the planned evaluation milestone demonstrates acceptable regression behavior and migration safety. The switch must be a separate reviewed change.