# Release Evidence Assembly

Live smoke evaluation is intentionally executed in small provider/model-specific shards. Release assessment, however, must operate on one coherent evidence bundle.

Use `scripts/assemble_release_evidence.py` only after each shard has completed blind judging and passed `scripts/validate_eval_import.py`.

```bash
python scripts/assemble_release_evidence.py \
  judged/openai.jsonl \
  judged/anthropic.jsonl \
  judged/gemini.jsonl \
  judged/qwen.jsonl \
  --out release/evidence.jsonl \
  --summary release/evidence-summary.json
```

## Assembly invariants

The assembler requires:

- `dataset=holdout` for every result;
- exactly one `experiment_id` across all shards;
- scored/judged results rather than raw transport results;
- judge method provenance;
- exact candidate prompt SHA-256;
- code and profile revision provenance;
- unique execution keys across shards.

An execution key is the tuple of experiment, case, strategy, repeat, provider, model, and runtime. Duplicates are rejected even when identical, because silently double-counting repeated artifacts would distort release metrics. A duplicate with a different prompt hash is reported as a conflicting duplicate.

## What assembly does not do

Assembly does not:

- judge outputs;
- repair incomplete shards;
- average away hard-gate failures;
- approve the release;
- promote Registry support maturity;
- switch the Router default.

After assembly, validate the combined JSONL, generate the release report, run machine evidence assessment, and then perform the human material-regression review.
