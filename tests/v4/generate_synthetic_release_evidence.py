#!/usr/bin/env python3
"""Generate test-only release evidence with required provider/model coverage."""
import hashlib
import json
import sys
from pathlib import Path

out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/tmp/synthetic-release.jsonl')
models = [
    ('openai','gpt-6-astra','openai-responses'),
    ('openai','gpt-5.6-luna','openai-responses'),
    ('anthropic','claude-sonnet-5','anthropic-messages'),
    ('google','gemini-3.8-flash','gemini-api'),
    ('qwen','qwen3.8-flash-next','qwen-cloud'),
    ('moonshot','kimi-k3','kimi-api'),
]
strategies = ['legacy','neutral','v4']
rows = []
for provider, model, runtime in models:
    for strategy in strategies:
        for repeat in range(1,4):
            prompt = f'synthetic:{model}:{strategy}:{repeat}'
            rows.append({
                'experiment_id':'synthetic-release-fixture',
                'case_id':'synthetic-case',
                'dataset':'holdout',
                'strategy':strategy,
                'repeat':repeat,
                'target':{'provider':provider,'model':model,'runtime':runtime,'model_version_or_snapshot':'fixture'},
                'settings':{'reasoning':None,'temperature':None,'max_output_tokens':128,'tools':[]},
                'inputs':{'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'source_snapshot':'synthetic-fixture'},
                'outcome':{
                    'completed':True,'hard_gate_pass':True,
                    'scores':{
                        'requirement_satisfaction':4,'intent_preservation':4,'source_fidelity':4,
                        'output_contract':4,'grounding':4,'permission_boundary':4,
                        'model_runtime_compatibility':4,'unnecessary_clarification':4,
                        'instruction_efficiency':4,'completion_quality':4},
                    'structured_output_valid':True,'failure_class':'none'},
                'telemetry':{'input_tokens':1,'output_tokens':1,'latency_ms':1,'cost_usd':None},
                'judge':{'method':'deterministic','judge_model':None,'randomized_position':None,'notes':'TEST ONLY'},
                'provenance':{'run_at':'2000-01-01T00:00:00Z','code_revision':'fixture','profile_revision':'fixture'}
            })
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(''.join(json.dumps(r, sort_keys=True)+'\n' for r in rows), encoding='utf-8')
print(f'wrote {len(rows)} synthetic records to {out}')
