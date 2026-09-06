# v4 Evaluation Result Schema

Each target-model run should be recorded as one result object.

```yaml
experiment_id:
case_id:
dataset: development | holdout
strategy: legacy | forced-legacy | neutral | v4 | v4-experimental
repeat: 1

target:
  provider:
  model:
  runtime:
  model_version_or_snapshot:

settings:
  reasoning:
  temperature:
  max_output_tokens:
  tools: []

inputs:
  prompt_sha256:
  source_snapshot:

outcome:
  completed: true
  hard_gate_pass: true
  scores:
    requirement_satisfaction: 0
    intent_preservation: 0
    source_fidelity: 0
    output_contract: 0
    grounding: 0
    permission_boundary: 0
    model_runtime_compatibility: 0
    unnecessary_clarification: 0
    instruction_efficiency: 0
    completion_quality: 0

  structured_output_valid:
  failure_class:

telemetry:
  input_tokens:
  output_tokens:
  latency_ms:
  cost_usd:

judge:
  method: human | deterministic | model
  judge_model:
  randomized_position:
  notes:

provenance:
  run_at:
  code_revision:
  profile_revision:
```

## Required reproducibility fields

At minimum, any result used to promote a strategy to `Evaluated` must identify:

- case ID and dataset;
- strategy;
- exact target model/runtime and available model version/snapshot identifier;
- repeat number;
- candidate prompt hash;
- hard-gate outcome;
- rubric scores;
- repository/code revision;
- profile revision or equivalent evidence version.

Cost/latency fields may be null when a provider does not expose them, but absence must not be represented as zero.

## Failure classes

Recommended normalized values:

```text
none
invalid_prompt_contract
unsupported_runtime_setting
provider_error
rate_limit
timeout
truncated_output
schema_invalid
source_violation
permission_violation
factual_fabrication
incomplete
judge_error
```

Provider failures should be separated from model-quality failures when possible.