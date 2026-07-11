# btom_v2 Real-LLM Validation Blocker

## Scope

This report records why the requested Groq-backed `btom_v2` real-LLM micro-pilot could not be consolidated in this checkout without fabricating code, results, or protocol state.

## Requested inspection targets

The requested files are not present anywhere under `/workspace/AAMAS` in this checkout:

- `btom_v2/prompts.py`
- `btom_v2/action_parser.py`
- `btom_v2/llm_policy.py`
- `btom_v2/real_llm_clients.py`
- `btom_v2/runner_llm_real_smoke.py`

The repository currently exposes the `cctdiag` package in `src/cctdiag/`, not a `btom_v2` package.

## Backend availability

`GROQ_API_KEY` is not present in the runtime environment used for this validation attempt. No API key, authorization header, or secret value was logged.

## Methodological decision

Because the target `btom_v2` modules and runner are absent from this checkout, creating replacement modules or synthetic validation outputs here would alter the project scope and risk fabricating a real-LLM validation result. The requested micro-pilot was therefore not run.

## Non-actions

- No symbolic environment dynamics were modified.
- No scenario definitions were modified.
- No symbolic policies were modified.
- No prompt/parser/runner code for `btom_v2` was fabricated.
- No Groq API call was made from this checkout.
- No scoring, calibration, ablation, statistical testing, or paper-ready performance claim was produced.

## Required next step

Provide the checkout or branch that contains `btom_v2/prompts.py`, `btom_v2/action_parser.py`, `btom_v2/llm_policy.py`, `btom_v2/real_llm_clients.py`, and `btom_v2/runner_llm_real_smoke.py`, plus a runtime with `GROQ_API_KEY` configured. Then rerun the requested micro-pilot exactly as specified.
