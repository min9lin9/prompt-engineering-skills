# Manual Live Evaluation

The repository never performs paid/live model evaluation from ordinary PR or push CI. Live execution is opt-in through `.github/workflows/v4-live-eval-manual.yml` and requires an explicit `workflow_dispatch` action.

## Preconditions

1. Configure `OPENAI_API_KEY` because the live workflow uses one fixed OpenAI generator model to materialize the legacy and v4 prompt candidates. Neutral candidates are deterministic and do not call a generator model.
2. Configure the target-provider secret required by the selected executor family.
3. Choose an exact Registry `target_provider` and `target_model`.
4. Start with `smoke_cases=1`. One smoke case executes exactly three target calls: legacy, neutral, and v4.

## Workflow inputs

- `executor_family`: `openai`, `anthropic`, `gemini`, or `compatible`.
- `target_provider`: Registry provider id such as `openai`, `anthropic`, `google`, `qwen`, `kimi`, `glm`, `deepseek`, `mistral`, or `minimax`.
- `target_model`: exact Registry model id.
- `experiment_path`: release-candidate experiment manifest.
- `smoke_cases`: 1–10 balanced holdout cases.
- `materializer_model`: fixed OpenAI generator model used for both legacy and v4 candidate generation. Default: `gpt-5.6-sol`.
- `timeout_seconds`: per materializer/target call timeout.

## Provider secrets

- Candidate materialization: `OPENAI_API_KEY`.
- OpenAI target: `OPENAI_API_KEY`.
- Anthropic target: `ANTHROPIC_API_KEY`.
- Gemini target: `GEMINI_API_KEY`.
- Explicit OpenAI-compatible target: `COMPAT_API_KEY` and `COMPAT_BASE_URL`.

Secrets are consumed only by the manually-dispatched job and are not written to evidence artifacts.

## Execution sequence

The workflow:

1. expands the holdout experiment into a pending execution plan;
2. selects balanced triplets for exactly one target model with `legacy`, `neutral`, and `v4` represented once per selected case/repeat;
3. materializes legacy and v4 candidates using the same fixed generator model;
4. materializes neutral candidates deterministically;
5. validates candidate hashes and provenance;
6. selects exactly one target reference executor family;
7. executes the balanced target-model smoke set;
8. creates a blinded judging packet;
9. uploads the pending plan, ready candidate plan, raw results, blind packet, and blind mapping as an unjudged artifact.

The candidate generator model and the target model are separate experimental variables. The generator model must remain fixed within a comparison so that legacy/neutral/v4 differences are not confounded with generator changes.

## Execution boundary

The workflow does **not**:

- judge its own outputs;
- set `quality_evaluated=true`;
- edit `registry/models.yaml`;
- approve `evals/release-review.yaml`;
- switch `/prompt` to v4 by default;
- commit or push evidence automatically.

## After the run

Download the artifact, perform blind judging, merge judgments, validate the final result import, generate the release report, run machine evidence assessment, and complete the human release review. Only after those steps may a dedicated default-switch PR be considered.
