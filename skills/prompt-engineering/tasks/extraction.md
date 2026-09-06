---
task: extraction
version: 1
---

# Extraction

## Goal
Extract only requested information from the permitted input into the requested schema or structure.

## Required inputs
- source content
- fields/schema to extract
- missing-value policy when not implied by the schema

## Rules
- Do not infer a field value that is absent from the source unless inference is explicitly requested.
- Use `null`, an empty value, or the user-defined sentinel for missing fields.
- Preserve source units, dates, identifiers, and categorical meaning unless normalization is requested.
- Return only fields allowed by the output contract when strict schema mode is requested.

## Validation
- Every required field is present in the output structure.
- No extra field appears in strict mode.
- Missing values follow the declared policy.
- Extracted values are traceable to the source content.

## Do not
- add explanatory prose when machine-readable output only was requested;
- fabricate plausible values;
- introduce provider-specific structured-output syntax here.
