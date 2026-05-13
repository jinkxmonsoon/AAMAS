# Pilot Lessons Learned (Journal-v1)

## What worked
- Schema, label, leakage, and integrity audits run end-to-end on pilot corpus.
- Parent-child links are valid and scenario coverage is complete.
- H6 minimum coverage counts are satisfied in pilot audit.

## What looked weak
- Several labels rely on terse evidence fields; non-trivial semantics are under-specified.
- Recoverability vs irreversibility boundary needs stronger operational examples.
- Partial-observability perturbations can increase ambiguity without explicit uncertainty policy usage.

## Scenario groups needing stronger design rules
- clean_broken_handoff
- cross_agent_propagation
- semantic_collision
- complex_collaboration

## Perturbation constraints to strengthen
- partial_observability: add explicit uncertainty-tagging guidance.
- tool_output_truncation: define acceptable truncation severity bands.

## Label-definition refinements needed
- Add explicit recovered-intermediate-error examples.
- Add explicit evidence templates for propagation claims.
- Add mandatory failed-recovery evidence when irreversibility=true.

## H6 usability assessment
- Usable as pilot signal only.
- Still high-risk for main corpus claims until richer rationale templates and adjudication SOP examples are frozen.

## Required protocol changes before full corpus generation
1. Freeze adjudication examples for irreversibility/propagation/recoverability.
2. Add uncertainty/ borderline labeling policy examples to rubric.
3. Require stronger evidence snippets for every positive H6 label.
4. Re-run pilot after protocol refinements before unlocking main corpus generation.
