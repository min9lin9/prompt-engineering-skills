# Reference Evaluation Executors

This directory contains small reference executors for the v4 evaluation runner.

Each executor:

- reads one JSON job from stdin;
- requires `candidate.prompt` and verifies `candidate.prompt_sha256`;
- obtains credentials only from environment variables;
- sends the exact candidate prompt to the selected target transport;
- writes exactly one normalized result JSON object to stdout;
- writes diagnostics to stderr;
- never stores credentials in the repository;
- does not judge the answer by itself beyond transport/completion metadata.

Reference executors are transport adapters, not release evidence. Real imported results still require scoring/judging and `scripts/validate_eval_import.py` before they may participate in the release gate.
