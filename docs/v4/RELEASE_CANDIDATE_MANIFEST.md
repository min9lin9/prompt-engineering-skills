# Release Candidate Manifest

A release-candidate manifest is the immutable reference point for one v4 default-switch decision. It binds the exact judged evidence bundle to the human-readable report, machine assessment, and human review record using SHA-256 digests.

## Why this exists

Evaluation evidence can be regenerated, reports can be edited, and a review record can change from pending to approved. A default-switch decision must never silently drift to newer or different evidence after review. The manifest makes such drift detectable.

## Bound artifacts

- judged holdout release evidence JSONL;
- generated release report;
- machine evidence assessment;
- human release-review record.

The manifest also records the experiment id, provider/model coverage, strategies, result count, and all code/profile revisions claimed by the evidence rows.

## Workflow

1. Assemble judged provider shards with `assemble_release_evidence.py`.
2. Validate the assembled result import.
3. Generate the release report.
4. Generate the machine assessment.
5. Complete or retain the human review record.
6. Create the manifest with `create_release_candidate_manifest.py`.
7. Re-run the same command with `--verify` immediately before a default-switch PR is reviewed or merged.

If any bound file changes after manifest creation, verification must fail and a new manifest/review cycle is required.

## Boundary

A manifest does not approve a release, change Registry maturity, edit the Router, sign cryptographically with a private key, or attest that evidence is truthful. It only gives content-addressed integrity across the release decision artifacts.
