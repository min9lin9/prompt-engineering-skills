# Live Evaluation Execution

The repository owns evaluation planning, common result validation, evidence aggregation, and release gating. It does **not** own provider credentials or force every provider through one SDK.

## Execution boundary

1. `scripts/prepare_eval_run.py` creates deterministic jobs.
2. `scripts/run_eval_jobs.py` sends one JSON job to an external executor over stdin.
3. The executor calls the target model/runtime and emits exactly one JSON result line.
4. `scripts/validate_eval_import.py` validates imported evidence.
5. `scripts/generate_release_report.py` summarizes validated evidence.
6. A separate reviewed change may update `evals/release-gate.yaml`, Registry maturity flags, or the Router default.

The runner invokes the executor without `shell=True`. Credential handling remains outside the repository and may use environment variables, a secret manager, local runtime configuration, or another approved mechanism.

## Executor contract

The external executor receives one job JSON object on stdin and must emit one result object following `evals/result-schema.md` on stdout. Diagnostic text belongs on stderr. Multiple JSON lines on stdout are rejected.

The executor must preserve the execution key:

- experiment ID;
- case ID;
- target provider/model/runtime;
- strategy;
- repeat number.

It must record actual model/runtime identity when the provider exposes a version or snapshot and must not report missing telemetry as zero unless zero is the real observed value.

## Evidence safety

Synthetic CI fixtures under `tests/v4/` are never release evidence. Real release evidence belongs under the approved results workflow and must pass the import validator before being considered by the release report.

No runner or report command may automatically:

- promote `integration_verified` or `quality_evaluated`;
- change `status: blocked` to approved;
- switch `/prompt` to v4 by default;
- commit, push, publish, or upload results externally.

## Why external executors

Provider APIs and local serving runtimes differ in authentication, request schema, tool protocols, reasoning controls, and versioning. Keeping those calls behind an executor contract prevents the prompt-engineering repository from becoming a universal API gateway while still supporting reproducible evaluation of OpenAI, Anthropic, Google, Qwen, Kimi, GLM, DeepSeek, Grok, MiniMax, Mistral, and future runtimes.
