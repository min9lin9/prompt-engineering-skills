# Prompt Contract v1

Prompt Contract is the internal normalization layer for Prompt Engineering Skills v4.
It is intentionally small: it preserves user intent and separates prompt semantics from provider/runtime payload details.

## Contract

```yaml
version: 1
mode: generate | review | optimize | transform

generator:
  model: optional

target:
  provider: optional
  family: optional
  model: optional
  runtime: optional

task:
  type: required
  goal: required
  context: []

requirements:
  success_criteria: []
  constraints: []
  sources: []
  language: optional
  output: {}

permissions:
  execute: false
  write: false
  publish: false

preferences:
  verbosity: optional
  format: optional
```

## Invariants

1. `generator.model` and `target.model` are independent concepts.
2. Target-model adaptation must not silently change the user's goal, source scope, language, output contract, or permissions.
3. Prompt text is not execution authorization.
4. Model profiles cannot raise `execute`, `write`, or `publish` permissions.
5. Provider/runtime parameters are not embedded into the semantic contract unless they materially affect prompt generation.
6. If the target model is unknown, Core + Task fallback is allowed, but model-specific optimization must be reported as unverified.
7. Do not require a target model when a model-neutral prompt can satisfy the request.

## Resolution order

Within the v4 prompt-engineering layer, apply rules in this order, subject to the host application's higher-level policies and safety requirements:

1. explicit user task requirements and source/output constraints;
2. runtime capability constraints;
3. model/provider confirmed deltas;
4. task-profile defaults;
5. core defaults.

A lower-level rule cannot weaken a higher-level requirement.

## Modes

### generate
Create a new finished prompt.

### review
Evaluate an existing prompt. Do not execute or mutate the target artifact unless separately requested.

### optimize
Improve a prompt while preserving the Prompt Contract.

### transform
Adapt a prompt for another model, runtime, task surface, or output format while preserving intent.

## Non-goals

Prompt Contract is not:

- a provider API request schema;
- a prompt programming language;
- an agent state machine;
- a permission system for the host application;
- a replacement for model/runtime documentation.
