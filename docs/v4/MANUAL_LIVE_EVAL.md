# Manual Live Evaluation

The repository never performs paid/live model evaluation from ordinary PR or push CI. Live execution is opt-in through `.github/workflows/v4-live-eval-manual.yml` and requires an explicit `workflow_dispatch` action.

## Preconditions

1. Prepare a JSONL evaluation plan whose candidates are already materialized and validated with `status=ready`.
2. Commit that non-secret plan on the branch being evaluated or otherwise make it available at the repository-relative path supplied to the workflow.
3. Configure only the provider secret required for the selected executor.
4. Choose a small `max_jobs` value for smoke evaluation before broader runs.

## Provider secrets

- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`
- Gemini: `GEMINI_API_KEY`
- OpenAI-compatible providers: `COMPAT_API_KEY` and `COMPAT_BASE_URL`

Secrets are consumed only by the manually-dispatched job and are not written to evidence artifacts.

## Execution boundary

The workflow:

- validates candidate hashes before calling a provider;
- selects exactly one reference executor family;
- caps the number of paid/live jobs;
- invokes `run_eval_jobs.py` without shell-based executor expansion;
- produces transport results;
- creates a blinded judging packet;
- uploads an unjudged evidence artifact.

The workflow does **not**:

- judge its own outputs;
- set `quality_evaluated=true`;
- edit `registry/models.yaml`;
- approve `evals/release-review.yaml`;
- switch `/prompt` to v4 by default;
- commit or push evidence automatically.

## After the run

Download the artifact, perform the blind judging step, merge judgments, validate the final result import, generate the release report, run machine evidence assessment, and complete the human release review. Only after those steps may a dedicated default-switch PR be considered.
