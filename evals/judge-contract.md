# Evaluation Judge Contract

Provider executors produce **transport results**, not release evidence. A transport result contains the exact candidate hash, target output, telemetry, and provenance, but it must remain unscored until a separate judge step evaluates the outcome.

## Separation of responsibilities

1. Candidate materializer creates an immutable prompt candidate.
2. Provider executor sends that candidate to the target runtime and records raw output.
3. Judge evaluates the raw output against the holdout case, hard gates, and rubric.
4. Judgment merger produces an import-ready evaluation record.
5. Release reporting and the release gate consume only validated, judged records.

The executor must not assign itself quality scores.

## Blind strategy comparison

When human or model judging is used, strategy identity should be hidden where practical. A judge item may expose the target model when runtime compatibility is part of the rubric, but it must replace `legacy`, `neutral`, and `v4` with opaque candidate labels before scoring.

Randomization must be reproducible from a recorded seed or mapping revision.

## Required judgment fields

```json
{
  "judge_item_id": "stable opaque id",
  "hard_gate_pass": true,
  "hard_gate_failures": [],
  "scores": {
    "requirement_satisfaction": 0,
    "intent_preservation": 0,
    "source_fidelity": 0,
    "output_contract": 0,
    "grounding": 0,
    "permission_boundary": 0,
    "model_runtime_compatibility": 0,
    "unnecessary_clarification": 0,
    "instruction_efficiency": 0,
    "completion_quality": 0
  },
  "judge": {
    "method": "human | model | deterministic",
    "judge_model": null,
    "notes": ""
  }
}
```

Every score is numeric from 0 through 4. Missing scores are invalid for release evidence.

## Hard gates

Hard-gate evaluation precedes aggregate quality comparison. A failed source-scope, permission, schema, or other declared case gate cannot be compensated for by a high average rubric score.

Provider transport failures should be classified separately from quality failures whenever possible.

## Evidence integrity

Judgment must not change:

- experiment ID;
- case ID;
- strategy;
- repeat;
- target model/runtime;
- candidate prompt hash;
- raw target output;
- transport telemetry;
- run provenance.

The merge step must reject mismatched or duplicate judge item IDs.
