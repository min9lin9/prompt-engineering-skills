# v4 Validation Contract

Validation is proportional to the task and risk. It verifies the Prompt Contract without turning every request into a broad test suite.

## Universal checks

Before returning a generated or transformed prompt, verify:

- the requested operation mode is preserved;
- the target model/runtime is not silently changed;
- source restrictions are preserved;
- output requirements are represented;
- permissions are not escalated;
- unsupported model/runtime assumptions are not presented as facts;
- model-specific rules do not duplicate or contradict Core/Task requirements.

## Task checks

Each Task Profile defines its own observable validation checks. Apply only the checks relevant to the selected task.

## Model checks

Model/runtime compatibility checks come from the Registry and Confirmed Model Delta claims. They are separate from task-quality evaluation.

## Failure behavior

If validation fails:

1. Correct the generated prompt when the fix is deterministic and does not change user intent.
2. Mark unsupported or unknown model behavior as unverified when generic fallback is still useful.
3. Ask for input only when the missing value materially changes the requested result and cannot be safely assumed.
4. Never claim integration or quality validation that was not actually performed.

## Non-goals

Validation does not imply:

- provider API integration testing;
- target-model quality evaluation;
- authorization to execute the prompt;
- full security review;
- exhaustive testing unrelated to the task.
