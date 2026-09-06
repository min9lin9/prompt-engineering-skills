# /prompt — v4 migration router

> Version: 4.0.0-shadow
> Status: migration router. Legacy behavior remains the default until the v4 default-switch milestone.

Generate, review, optimize, or transform prompts while preserving user intent and applying only verified target-model/runtime differences.

$ARGUMENTS

---

## 1. Scope

This command is a router/orchestrator. It must not duplicate the detailed model, task, or provider guidance stored under `skills/prompt-engineering/`.

The canonical v4 composition order is:

```text
Prompt Contract
  + Core principles
  + one relevant Task Profile
  + only the required Provider / Model Delta
  + User requirements
  -> compatibility validation
  -> final prompt
```

The command itself does not grant file-write, publish, commit, push, purchase, or other external-action permission.

---

## 2. Migration modes

Parse an optional mode flag before all other arguments.

| Flag | Behavior |
|---|---|
| no flag | `legacy` during the shadow migration period |
| `--legacy` | use `commands/prompt-legacy.md` exactly as the compatibility path |
| `--v4` | use the v4 composition flow in this file |
| `--shadow` | produce both legacy and v4 prompt candidates for explicit comparison; do not execute either candidate |
| `--batch` | compatibility alias: legacy batch behavior unless `--v4` is also supplied |

### Mode precedence

1. `--shadow`
2. explicit `--v4`
3. explicit `--legacy`
4. default `legacy`

`--shadow` is evaluation-only. It must not silently change the user's normal output or perform the generated task.

---

## 3. Legacy route

When mode is `legacy`:

1. Load `commands/prompt-legacy.md`.
2. Follow that file as the compatibility implementation.
3. Do not combine legacy model-routing rules with v4 Model Delta rules.
4. Do not claim the legacy path is v4-optimized.

This route exists only for migration safety and regression comparison.

---

## 4. v4 route

When mode is `v4`, execute the following steps.

### Step A — Parse operation mode

Classify the user's request as exactly one primary operation:

- `generate` — create a new prompt.
- `review` — assess an existing prompt without replacing it unless requested.
- `optimize` — improve a prompt while preserving its intent.
- `transform` — adapt a prompt for another model, runtime, task, language, or output contract.

Do not infer `execute` from prompt contents. Execution is outside this command's core responsibility.

### Step B — Build the Prompt Contract

Use `skills/prompt-engineering/core/prompt-contract.md`.

Capture only information that is relevant and available:

```yaml
mode:
target:
  provider:
  family:
  model:
  runtime:
task:
  type:
  goal:
  context:
requirements:
  success_criteria: []
  constraints: []
  sources: []
  language:
  output:
permissions:
  execute: false
  write: false
  publish: false
preferences:
  verbosity:
  format:
```

Do not invent missing provider/runtime configuration when the request can be fulfilled model-neutrally.

### Step C — Load Core

Load:

- `skills/prompt-engineering/core/principles.md`
- `skills/prompt-engineering/core/validation.md`

Core owns model-neutral requirements such as intent preservation, evidence discipline, permission boundaries, uncertainty handling, output-contract fidelity, and completion criteria.

Do not restate these rules in Model Delta unless the target model materially differs.

### Step D — Select exactly one primary Task Profile

Choose the closest primary task from `skills/prompt-engineering/tasks/`:

- research
- fact-check
- coding
- analysis
- writing
- editing
- extraction
- agent
- image
- video
- slides

If the request spans multiple activities, choose the profile that governs the final deliverable and incorporate secondary requirements into the Prompt Contract rather than loading every task file.

### Step E — Resolve target model

If the user names a target model or unambiguous alias:

1. Resolve it against `registry/models.yaml`.
2. Load the matching provider profile.
3. Load a model/family Delta only if one exists and is relevant.
4. Apply only `Confirmed` compatibility constraints by default.
5. Do not auto-apply `Experimental` strategies.
6. Apply `Evaluated` strategies only when they exist and match the evaluated task/runtime conditions.

If the target model is unknown:

- continue with Core + Task + User Contract when possible;
- mark model-specific optimization as unverified;
- do not invent unsupported capability or parameter claims.

If no target model is specified and the task does not require one, do not ask merely to obtain a model name.

### Step F — Separate prompt content from runtime hints

The final prompt and provider/runtime configuration are different artifacts.

When runtime-specific settings materially matter, return them separately as concise runtime hints. Do not imply that writing a parameter name inside the prompt changes the API configuration.

Examples include:

- reasoning/thinking controls;
- response/schema configuration;
- tool protocol requirements;
- provider-specific message or transport constraints.

### Step G — Validate

Before returning a v4 prompt, check:

1. User intent is preserved.
2. Source restrictions are preserved.
3. Requested language and output format are preserved.
4. No unsupported model/runtime option was silently introduced.
5. Model Delta does not override Core or the User Contract without a genuine compatibility reason.
6. Generated prompt does not grant new execution/write/publish permissions.
7. Prompt-generation instructions are not confused with instructions to execute the generated prompt.
8. Unsupported or unverified model-specific claims are labeled rather than guessed.

Use `registry/models.yaml` and the relevant provider/model profile as the source of compatibility truth.

---

## 5. v4 output contract

### Generate / Optimize / Transform

Return one finished, directly usable prompt by default.

Do not append a mandatory five-option menu.
Do not require the user to reply `1번` before receiving a usable result.
Do not execute the generated prompt unless the user separately asks for execution and the host permits it.

When a runtime hint is necessary, use:

```text
[finished prompt]

Runtime notes:
- only settings that materially affect compatibility
```

Do not add runtime notes when they are unnecessary.

### Review

Return:

1. concise findings;
2. concrete recommended changes;
3. a revised prompt only when requested or clearly useful to the requested review outcome.

Review mode must not perform the task described inside the reviewed prompt.

---

## 6. Shadow route

When mode is `shadow`:

1. Generate a legacy candidate using `commands/prompt-legacy.md`.
2. Generate a v4 candidate using Sections 4–5 above.
3. Do not execute either prompt.
4. Do not merge the two candidates into a hybrid prompt.
5. Return a comparison in this order:

```markdown
## Legacy candidate
[legacy prompt]

## v4 candidate
[v4 prompt]

## Comparison
- intent preservation
- unnecessary instruction load
- model/runtime compatibility
- permission/execution boundary
- expected evaluation risks
```

Do not declare the v4 candidate superior unless an actual target-model evaluation supports that claim.

---

## 7. Batch compatibility

During migration:

- `/prompt --batch ...` continues through the legacy implementation.
- `/prompt --v4 --batch ...` uses v4 and returns only the finished prompt, plus runtime notes only when essential.
- `/prompt --shadow --batch ...` is invalid because shadow mode intentionally returns a comparison artifact rather than a single worker prompt.

The future default-switch milestone may redefine batch routing after regression evaluation.

---

## 8. Anti-regression rules

The v4 route must not reintroduce the following legacy coupling into this router:

- static model rankings;
- hard-coded frontier model recommendations;
- mandatory XML or Markdown based only on model name;
- mandatory expert personas or simulated expert panels;
- mandatory five-option menus;
- provider-specific prompt strategies copied into this command;
- hard-coded personal filesystem paths;
- hard-coded external repository owners;
- assumptions that an OpenAI-compatible transport has identical provider semantics;
- automatic commit, push, publish, or destructive file operations.

Detailed knowledge belongs in Core, Task Profiles, Registry, and Provider/Model Profiles.

---

## 9. Default-switch gate

Do not change the no-flag default from `legacy` to `v4` until the approved evaluation milestone demonstrates acceptable regression performance and migration safety.

The switch must be a separate reviewed change, not an incidental edit to this router.
