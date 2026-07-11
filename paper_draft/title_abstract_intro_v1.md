# Title, Abstract, and Introduction Draft v1

## Scope and non-action boundary

This draft is writing-only. It does not implement code, run experiments, modify corpus/gold labels, run scoring, rank steps, calibrate, ablate, perform statistical tests, restore scoring configuration, or produce performance tables.

## Title options

1. **Protocol-First Failure Attribution for Multi-Agent Collaboration: Full-Trace Representation, Leakage Governance, and Negative CCT Diagnostics**
2. **Auditing Multi-Agent Failure Attribution: A Full-Trace Benchmark Protocol and Diagnostic CCT Representation Study**
3. **Why Naive Structural Scoring Fails for Collaborative Failure Attribution: A Protocol-First CCT Benchmark Audit**
4. **From Failure-Centered Labels to Full-Trace Diagnostics: A Governed Benchmark for Multi-Agent Attribution Research**
5. **Causal-Flow Representation Diagnostics for Multi-Agent Failure Attribution: Protocol, Artifacts, and Negative Findings**

## Preferred title

**Protocol-First Failure Attribution for Multi-Agent Collaboration: Full-Trace Representation, Leakage Governance, and Negative CCT Diagnostics**

## Abstract v1

Attributing failures in collaborative multi-agent systems is difficult because the decisive error may be distributed across handoffs, tool outputs, partial observations, and downstream recoverability conditions. Benchmark design can make this problem easier than it appears: failure-centered schemas may leak labels, shortcut baselines may exploit metadata or position, and incomplete provenance can obscure whether a reported result is reproducible. We present a protocol-first full-trace benchmark and diagnostic representation audit for Collaborative Causal Trace (CCT) failure attribution. The protocol separates prediction-view-safe trace fields from private labels and provenance, records artifact manifests, and applies leakage, shortcut, provenance, and representation-degeneracy gates before any scoring claim. Under this governance, frozen uncalibrated CCT diagnostics did not support H1/H2 and are bounded by missing frozen scoring-configuration provenance. Descriptor augmentation and causal-flow edge redesign were feasible under prediction-view-safe constraints, but redesigned graph features remained highly degenerate, with only 6 unique feature vectors across 420 traces. These negative findings show that naive structural scoring and simple causal-flow counts are insufficient under the current representation. The contribution is therefore not a performance-superiority claim, but a reproducible benchmark/protocol foundation for future failure-attribution research.

## Introduction draft v1

Collaborative multi-agent systems increasingly combine specialist agents, tool calls, handoffs, and intermediate evidence. When such a system fails, the final incorrect outcome is rarely the whole diagnostic object. The decisive failure may appear earlier, propagate through later steps, become irreversible only after a missed correction opportunity, or be masked by plausible downstream text. Failure attribution therefore requires more than identifying the final bad answer: it requires a representation of the complete trace, the visible evidence available at each step, and the operational dependencies through which an error could influence later behavior.

This paper studies that representation problem from a protocol-first perspective. A benchmark for multi-agent failure diagnosis can accidentally encode the answer if it is organized around the failure label rather than the observable trace. Gold failure steps, responsible agents, label rationales, provenance records, scenario metadata, and perturbation tags are useful for audit and reporting, but unsafe as prediction inputs. Even visible fields can create shortcuts when trace position, agent identity, fixed templates, or content volume dominate the representation. A method that appears to localize failures may instead exploit these artifacts. For this reason, failure-attribution research needs explicit prediction views, leakage audits, shortcut checks, and artifact provenance before performance claims are meaningful.

We use Collaborative Causal Trace (CCT) as a diagnostic representation for this protocol. In this paper, CCT is not presented as a validated automatic attribution method. Instead, it provides a structured way to audit full traces, handoffs, visible evidence, tool-output relationships, and candidate causal-flow edges. The Journal-v1 protocol migrates from failure-centered records to full-trace records, separates visible trace fields from private labels and provenance, and records generated-artifact policies so that large intermediate artifacts remain reproducible without overwhelming review.

The resulting evidence is intentionally conservative. Frozen uncalibrated CCT diagnostics did not support H1/H2 under the current features, and the frozen scoring configuration is not reproducible from the active checkout. Subsequent descriptor augmentation and causal-flow edge redesign were kept representation-only. They passed leakage-oriented audits, but did not solve the representation problem: the redesigned graph features remained highly degenerate, producing only 6 unique feature vectors across 420 traces. This result is not treated as a failed performance paper; it is treated as methodological evidence that naive structural scoring, simple descriptor augmentation, and simple causal-flow counts are not sufficient for collaborative failure attribution under the current representation.

The contribution of this work is therefore a benchmark/protocol and diagnostic-representation foundation. We show how to structure full-trace failure-attribution artifacts, how to separate private labels from prediction-safe views, how to record leakage/shortcut/provenance and artifact-reviewability gates, and how negative representation diagnostics can prevent premature scoring or calibration. The claims are deliberately bounded: we do not claim that CCT improves automatic failure attribution, outperforms baselines, is robust under perturbations, is ready for calibration, validates H1/H2, or is production-ready. Instead, we provide a reproducible protocol and evidence map for future methods that must overcome the representation and governance failures documented here.
