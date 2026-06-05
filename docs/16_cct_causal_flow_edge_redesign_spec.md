# 16 — CCT Causal-Flow Edge Redesign Specification

## Status and scope

Status: **specification-only, not implemented**.

Task 20 follows the Task 19 decision to pursue Option C: redesign CCT graph/feature extraction around richer non-position causal-flow edges before any scoring or calibration. This document defines candidate representation edges only. It does **not** define scoring weights, scoring formulas, ranks, calibration, grid search, LOSO, refinement variants, ablations, statistical tests, corpus edits, gold-label edits, or paper-ready result tables.

The current checkout does not contain `docs/15_cct_causal_flow_descriptor_spec.md` or implementation modules at `src/cctdiag/cct/builder.py`, `src/cctdiag/cct/features.py`, or `src/cctdiag/cct/descriptors.py`; this spec therefore remains independent of graph-builder behavior and feature-extraction code.

## Representation / descriptor / scoring separation

- **Representation edges**: directed, typed relations between visible trace steps, visible evidence references, and visible tool-output contexts. This document only specifies candidate edge semantics and future extraction constraints.
- **Descriptors/features**: future summaries of representation edges may be proposed in a later task, but no feature extraction is implemented or authorized here.
- **Scoring rules**: scoring weights, formulas, ranks, thresholds, calibration, and comparison to gold labels are explicitly out of scope.

## Anti-leakage constraints

Future edge extraction must not read or derive from:

- `private_labels`;
- `gold_failure_step`;
- `gold_failure_agent`;
- H6 private evidence fields, including propagation, irreversibility, and recovery rationales;
- `label_rationale` or other label metadata;
- `provenance`;
- correctness terms or correctness annotations;
- rank, score, prediction, or model-output fields;
- `scenario_group` or `perturbation_type` as extraction input.

## Anti-shortcut constraints

Future edge extraction must not depend on:

- fixed step position alone;
- agent identity alone;
- fixed scenario names;
- perturbation labels;
- builder-specific phrases alone;
- content volume alone.

Every extracted edge must require a visible relation between two steps, a step and evidence fields, or a step and tool output. Scenario and perturbation distributions may be used only as audit metadata after extraction, never as extraction inputs.

## Candidate non-position causal-flow edge types

| Edge type | Definition | Source node type | Target node type | Visible fields used | Forbidden fields | Deterministic extraction rule for future prototype | Expected directionality | CCT thesis relation | Supports | Leakage risk | Lexical shortcut / template sensitivity risk | Feasible without LLM/judge? | Future status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `constraint_shift_edge` | A visible requirement, constraint, caveat, or condition is softened, strengthened, dropped, or reframed between steps. | Step or visible constraint mention in a step. | Later step that restates or acts on the constraint. | `input_message`, `output_message`, `tool_output`, `visible_step_notes`, handoff fields only as relation context. | All private/gold/provenance/scenario/perturbation fields. | Detect repeated constraint tokens or normalized requirement phrases that change modal status across visible step text; require a source and later target mention. | Earlier visible constraint context to later transformed use. | Encodes causal loss or distortion of task constraints. | handoff, evidence flow, propagation, recoverability. | Medium: may accidentally mirror label language if visible text contains failure terms; audit forbidden terms. | Medium: builder wording may use repeated modal phrases; require normalized relation plus cross-field evidence. | Yes, with deterministic lexicons and normalization. | Primary candidate for sample prototype. |
| `evidence_conflict_edge` | A later step selects or emphasizes evidence that visibly conflicts with another available evidence item or tool output. | Evidence item/tool-output context. | Step using or choosing conflicting evidence. | `evidence_items`, `evidence_used`, `tool_output`, `input_message`, `output_message`. | Private labels, gold fields, H6 evidence, label rationale, provenance, scenario/perturbation. | Detect visible conflict markers or mutually exclusive evidence mentions where selected evidence differs from stronger/contrasting tool-output text. | Evidence/tool context to step decision. | Encodes evidential inconsistency in causal flow. | evidence flow, semantic collision, irreversibility. | Medium-high: conflict terms can overlap with generated diagnostic language; audit lexicon. | High: conflict templates may be scenario-specific; require relation between evidence/tool output and step output. | Partly; deterministic prototype should be conservative. | Primary candidate with high-risk audit. |
| `evidence_omission_edge` | A visible evidence item or caveat available upstream is not carried into a downstream step where it remains operationally relevant. | Upstream evidence item/tool-output/caveat. | Downstream step omitting it. | `evidence_items`, `evidence_used`, `tool_output`, `input_message`, `output_message`, `visible_step_notes`. | Private labels, gold fields, H6 evidence, label rationale, provenance, scenario/perturbation. | Detect evidence/caveat mention upstream and absence from a downstream action statement that references the same decision context; require visible upstream availability. | Upstream visible evidence to downstream omission point. | Encodes causal information loss. | handoff, evidence flow, propagation, recoverability. | Medium: omission can resemble gold failure if target known; no gold comparison during readiness. | Medium-high: absence rules are sensitive to paraphrase/template variation. | Yes for conservative token/phrase matching; broader semantic omission needs later review. | Experimental-only until omission audits are strong. |
| `downstream_dependency_edge` | A downstream step explicitly depends on an upstream decision, constraint, evidence selection, or handoff content. | Upstream step or tool-output context. | Later dependent step. | `handoff_from`, `handoff_to`, `input_message`, `output_message`, `tool_output`. | Private/gold/H6/provenance/scenario/perturbation fields. | Detect explicit dependency verbs or references to prior decision artifacts in later visible text; require non-identity textual relation, not handoff chain alone. | Upstream operational content to downstream dependent action. | Encodes propagation channels across the trace. | handoff, propagation, cross-agent dependency. | Low-medium: can be extracted from visible flow if private fields excluded. | Medium: fixed handoff templates could create false positives; require content relation beyond adjacency. | Yes. | Primary candidate. |
| `correction_opportunity_edge` | A visible later step has enough information to correct or question an earlier problematic transformation, regardless of whether correction occurs. | Earlier questionable step/content. | Later visible review/check/opportunity context. | `input_message`, `output_message`, `tool_output`, `visible_step_notes`. | Private labels, H6 recovery labels/evidence, gold fields, provenance, scenario/perturbation. | Detect later visible check/review/tool-output mentioning the same constraint/evidence plus challenge/caveat terms; do not compare to gold. | Earlier content to later opportunity context. | Encodes recoverability affordances without using private recovery labels. | recoverability, evidence flow, handoff. | Medium: recovery concepts may leak if private wording appears in visible text; audit recovery/correctness lexicon. | Medium: review-step templates may be position-like; require content-specific relation. | Yes for conservative rules. | Diagnostic-only in first prototype. |
| `correction_attempt_edge` | A visible step attempts to repair, revise, escalate, or reconcile an earlier constraint/evidence issue. | Later correcting step. | Earlier issue/content or downstream revised content. | `input_message`, `output_message`, `tool_output`, `visible_step_notes`. | Private labels, H6 evidence, gold fields, provenance, scenario/perturbation. | Detect visible repair/revision/escalation language tied to a previously mentioned constraint/evidence item; require before/after content relation. | Later correction attempt back to issue or forward to revised downstream content, recorded with explicit direction convention. | Encodes active recovery mechanisms. | recoverability, propagation. | Medium: correction terms can imply correctness; avoid correctness labels and audit terms. | Medium-high: may be rare or template-dependent in current corpus. | Yes for conservative rules. | Diagnostic-only until corpus coverage is known. |
| `unresolved_caveat_edge` | A visible caveat remains present or is introduced but is not resolved before terminal delivery/action. | Caveat mention in step/tool output. | Later step where caveat remains unresolved or impacts action. | `input_message`, `output_message`, `tool_output`, `visible_step_notes`. | Private H6 irreversibility/recovery evidence, gold fields, label rationale, provenance, scenario/perturbation. | Detect caveat/uncertainty markers linked to an operational item and no later visible resolution marker; require trace-local evidence chain. | Caveat source to later unresolved state/action. | Encodes unresolved uncertainty propagation. | propagation, irreversibility, semantic collision. | Medium: unresolved status can imply outcome; no terminal/gold comparison during readiness. | High: absence of resolution is paraphrase-sensitive. | Partly; conservative deterministic extraction only. | Experimental-only. |
| `semantic_collision_edge` | Two visible terms, readings, assumptions, or interpretations collide semantically and one path is selected or carried forward. | Competing interpretation/evidence context. | Step selecting or propagating one interpretation. | `input_message`, `output_message`, `tool_output`, `visible_step_notes`. | Private labels, gold fields, H6 evidence, provenance, scenario/perturbation. | Detect paired contrast markers or alternative readings in visible text and later selection/carry-forward of one option. | Collision context to selected downstream interpretation. | Encodes ambiguity resolution and semantic failure modes. | semantic collision, evidence flow, propagation. | Medium: scenario-specific semantic words may leak if overfit; scenario names forbidden. | High: current synthetic templates may make collisions lexically regular. | Yes for conservative contrast-pattern rules. | Primary candidate with template audit. |
| `tool_alignment_edge` | A step's output aligns with, ignores, or contradicts visible tool output without using private labels. | Tool-output node/context. | Step output/action node. | `tool_call`, `tool_output`, `output_message`, `evidence_used`. | Private labels, gold fields, H6 evidence, label rationale, provenance, scenario/perturbation. | Compare normalized key terms in tool output with step output/evidence used; flag alignment/omission/contradiction relation without assigning correctness. | Tool output to step output/action. | Encodes whether external evidence enters the causal trace. | evidence flow, tool use, irreversibility. | Low-medium if relation labels avoid correctness; audit for correct/incorrect terms. | Medium: tool-output templates may dominate; require content overlap/contrast. | Yes. | Primary candidate. |
| `cross_agent_dependency_edge` | A visible dependency crosses agent boundaries through handoff content, evidence, or tool-output reliance. | Upstream agent step content. | Downstream different-agent step content. | `handoff_from`, `handoff_to`, `input_message`, `output_message`, `tool_output`, `evidence_used`. | Private labels, gold failure agent/step, H6 evidence, provenance, scenario/perturbation. | Detect same content/evidence/constraint referenced across different visible step records and different handoff roles; do not use fixed agent IDs as signal. | Upstream content-bearing step to downstream different-agent dependent step. | Encodes multi-agent causal propagation central to CCT. | handoff, cross-agent dependency, propagation. | Low-medium if agent identity is not predictive input. | Medium: fixed five-agent chain may create position shortcut; require content relation beyond handoff. | Yes. | Primary candidate. |

## Future validation requirements

A future sample prototype must validate edge representation before any scoring task is considered. Required audits:

1. Edge count distribution by edge type.
2. Edge sparsity/density per trace.
3. Scenario distribution as audit-only metadata after extraction.
4. Perturbation distribution as audit-only metadata after extraction.
5. Duplicate graph signature reduction relative to current proxy-heavy representation.
6. Private leakage audit covering all forbidden fields and forbidden terms.
7. Lexical-template audit to detect builder-specific phrase dependence.
8. Perturbation sensitivity audit focused on whether non-causal textual perturbations spuriously change edges.
9. No comparison to `gold_failure_step`, `gold_failure_agent`, H6 labels, or private rationales during edge-readiness audit.

## Future readiness gates

- `CCT_CAUSAL_FLOW_EDGE_SPEC_READY_FOR_SAMPLE_PROTOTYPE = yes`
- `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`

The next task should be a **sample-only edge prototype** that emits reviewable sample graphs and audit summaries without scoring, ranking, calibration, gold-label comparison, or corpus changes.

## Task 20A sample-prototype constraint clarification

A future or current sample prototype may implement only a subset of these edges and must consume `make_full_trace_prediction_view(record)` output rather than raw records. Sample artifacts may include scenario/case-variant composition only as audit metadata outside edge extraction and outside edge records. Full-corpus extraction, gold-label comparison, H6-label comparison, ranking, scoring, calibration, and result-table generation remain prohibited until a separate explicit authorization.

## Task 20B refined sample constraint clarification

Task 20B keeps extraction sample-only and prediction-view-only while refining node identifiers and extraction notes to reduce template-pattern repetition. Refinement may add trace-scoped node IDs and relation-specific notes, but it must not add gold/H6 comparisons, scenario or perturbation extraction inputs, scoring fields, ranking fields, calibration, or full-corpus extraction. Missing scoring-configuration provenance must be handled by a separate protocol-recovery task rather than silent recreation.

## Task 21 representation-only robustness clarification

After the scoring-config hash mismatch adjudication, causal-flow edge work remains representation-only. Robustness audits may inspect sample edge counts, visible-field requirements, clean/perturbed sample stability, and template sensitivity, but they must not restore or recreate `configs/cct_scoring.yaml`, run scoring, rank candidate steps, compare edges to gold/H6 labels, calibrate, grid search, run LOSO, refine scoring, ablate, perform statistical tests, or produce paper-ready result tables. Any future full-corpus edge audit must be separately authorized as representation-only and must preserve no-gold/no-scoring constraints.

## Task 22 narrowed strong-edge stress-test clarification

Task 22 keeps stress testing narrowed to `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge`. A future narrow full-corpus audit may be considered for these three edge types only if it remains representation-only, prediction-view-only, and no-gold/no-scoring. `constraint_shift_edge`, `semantic_collision_edge`, and unimplemented Task 20 edge types remain outside the narrowed audit scope until separate sample refinement or prototyping.

## Task 23 full-corpus strong-edge audit clarification

Task 23 permits a representation-only full-corpus audit of `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge` only. The audit may join scenario, perturbation, and case-variant metadata after extraction for descriptive audit stratification, but these metadata remain forbidden as extraction inputs and forbidden for future scoring unless separately authorized. Full generated edge JSON should follow generated-artifact policy when it would create an unreviewable diff; compact samples, manifests, and reports remain tracked. This clarification does not authorize scoring, ranking, gold/H6 comparison, calibration, ablation, statistical testing, or paper-ready result tables.

## Task 24 redesigned graph integration clarification

Task 24 integrates only `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge` into redesigned graph artifacts together with prediction-view-safe base sequence/handoff edges. `constraint_shift_edge`, `semantic_collision_edge`, and unimplemented Task 20 edge types remain excluded from redesigned graph artifacts. Graph artifacts may be used only for a future representation-only feature audit; this clarification does not authorize scoring, ranking, gold/H6 comparison, calibration, ablation, statistical testing, or paper-ready result tables.
