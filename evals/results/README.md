# Evaluation Results

This directory stores reproducible target-model evaluation records used by the v4 release gate.

## Layout

```text
evals/results/
  <experiment-id>/
    manifest.yaml
    results.jsonl
    summary.md
```

`results.jsonl` contains one record per case × strategy × repeat using the fields defined in `evals/result-schema.md`.

## Evidence rules

- Structural CI output is not model-quality evidence.
- Provider/API failures must be distinguished from model-quality failures.
- A result used for `quality_evaluated=true` must identify the exact target model/runtime, prompt hash, repository revision, profile revision, repeat, hard-gate result, and rubric scores.
- Development-set results may guide tuning but cannot by themselves unlock the default switch.
- Holdout results are required for release-gate approval.
- Results may be produced by a live provider runner or imported from an externally executed evaluation harness, but imported evidence must use the same schema and provenance requirements.

## No fabricated evidence

Do not add synthetic `success` results merely to satisfy CI. The release gate remains blocked when no real target-model results exist.
