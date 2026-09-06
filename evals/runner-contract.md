# Provider Evaluation Runner Contract

The repository does not require one universal provider SDK. A live or externally executed runner may be used if it emits records compatible with `evals/result-schema.md`.

## Runner responsibilities

For every case × strategy × repeat, a runner must:

1. resolve the exact target model and runtime;
2. render the candidate prompt without changing the case semantics;
3. record the prompt SHA-256 before submission;
4. submit the request using the provider/runtime's supported configuration;
5. capture completion/failure state separately from judge scores;
6. record provider errors, timeouts, truncation, and rate limits as operational failures rather than silently converting them into quality scores;
7. run deterministic checks first when available;
8. attach human/model judge output only after deterministic hard gates;
9. write one JSON object per result line;
10. preserve code/profile revisions and run timestamp.

## Secret boundary

API keys and provider credentials must never be committed to this repository or written into result files. CI-based live evaluation must obtain credentials from the execution environment's secret store.

## Provider adapters

Provider-specific runners may translate the common experiment intent into native APIs. Compatibility transports must not be assumed to have identical semantics merely because their request shapes resemble OpenAI or Anthropic APIs.

## Replay/import mode

Results generated outside GitHub Actions may be imported when the exact prompt hash, target/runtime, revisions, repeat, scores, hard gates, and provenance are retained. Imported results are subject to the same release-gate validator.

## Default-switch boundary

The runner itself may never change `commands/prompt.md`, Registry maturity flags, or `evals/release-gate.yaml`. Evidence collection and release approval remain separate reviewable actions.
