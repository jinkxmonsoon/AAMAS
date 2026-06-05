# CCT Revision Path Decision Gate

## Scope

This decision gate selects a next methodological direction after negative diagnostic evidence from Tasks 18 through 18F. It is a governance/reporting artifact only. It does not implement or run scoring, ranking, calibration, grid search, LOSO, refinement, ablation, statistical tests, corpus changes, gold-label changes, or paper-ready result tables.

## Option decision matrix

| Option | Scientific rationale | Expected benefit | Validity risk | Overfitting risk | Implementation cost | H1/H2/H3/H4/H6 impact | Allowed now? | Required next task if selected |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A — Calibrate current features | Try to adjust weights/thresholds after uncalibrated underperformance. | Could improve numeric fit if current features contain useful signal. | High: current evidence indicates weak/non-discriminative and proxy-heavy features, so calibration may optimize artifacts rather than causal attribution. | High: calibration before feature validity can overfit to corpus regularities and baseline gaps. | Medium. | H1/H2 remain unsupported; H3 remains blocked because calibration is premature; H4 blocked; H6 unsupported by scoring. | Blocked. | First complete a feature-validity redesign gate; only then propose a separately authorized calibration task. |
| B — Add descriptor-augmented features to scoring | Use Task 18C/18D descriptors and Task 18E augmented rows directly in scoring. | Could add causal-flow information beyond coarse structural fields. | High: Task 18E readiness remains `no`; duplicate-row reduction was only modest, and descriptor scoring could encode unvalidated shortcuts. | Medium-high: new descriptor columns could be tuned to observed failures without proving general validity. | Medium. | H1/H2 remain unsupported until a future authorized scoring task; H3 still blocked; H4 blocked; H6 open but unsupported. | Blocked. | Define an explicit descriptor-validity acceptance gate before any scoring integration. |
| C — Redesign CCT graph/feature extraction around richer non-position causal-flow edges before scoring | Address the diagnosed representation failure directly by improving causal-flow encoding rather than calibrating proxy-heavy features. | Best chance of improving construct validity and reducing reliance on position/identity/content-volume proxies. | Medium: redesign may still encode shortcuts unless audited, but it targets the identified root cause. | Medium: lower than A/B if paired with pre-scoring audits and frozen acceptance criteria. | High. | H1/H2 remain unsupported now but get a valid future test path; H3 remains blocked until feature validity is established; H4 remains blocked; H6 remains open. | Allowed only as a future explicitly scoped design/prototype task with no scoring. | Draft and audit a revised CCT graph/feature extraction specification focused on non-position causal-flow edges, with leakage/shortcut/readiness gates before scoring. |
| D — Reformulate paper contribution away from performance superiority toward protocol/benchmark/representation diagnostics | Align claims with current negative evidence and strengths in protocol, benchmark, leakage correction, and representation diagnostics. | Reduces claim risk and may produce a scientifically honest contribution even if performance superiority remains unsupported. | Low-medium: risk is under-claiming or losing methodological ambition, but it avoids unsupported superiority. | Low: does not tune methods to improve scores. | Low-medium. | H1/H2 remain unsupported; H3/H4 remain blocked unless future evidence changes; H6 remains open/unsupported by scoring; allowed claims become diagnostic/protocol-focused. | Allowed as claim-boundary work, not as empirical performance reporting. | Prepare a claims-and-positioning revision that excludes superiority claims and foregrounds protocol/benchmark diagnostics. |

## Gate decision

- Selected primary path: **Option C**.
- Secondary claim-positioning guardrail: **Option D** should constrain manuscript language until future evidence supports stronger claims.
- Rejected immediate path: **Option A**, because calibration is premature before feature validity.
- Rejected immediate path: **Option B**, because descriptor scoring is premature while descriptor readiness remains `no`.

## Current lock state

- No scoring is authorized by this gate.
- No calibration is authorized by this gate.
- No descriptor-augmented scoring integration is authorized by this gate.
- No protocol revision is authorized by this gate.
- A future Option C task may draft/prototype a richer causal-flow graph/feature representation only if it preserves the no-scoring/no-calibration/no-corpus-change constraints or receives explicit written authorization for any protected change.
