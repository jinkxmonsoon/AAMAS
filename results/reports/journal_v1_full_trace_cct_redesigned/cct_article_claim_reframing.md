# CCT Article Claim Reframing

## Selected article frame

The journal article should be reframed as a **protocol-first diagnostic representation and benchmark paper**, not a performance-superiority method paper.

## Allowed claims under Path B

- CCT provides a structured full-trace representation for auditing multi-agent collaboration failures.
- The project identifies and controls leakage, shortcut, failure-centered schema, provenance, and artifact-reviewability risks.
- Full-trace representation is necessary for fair failure-attribution analysis.
- Naive structural scoring and simple causal-flow feature redesign were insufficient in the controlled trace bank.
- Descriptor augmentation and causal-flow edges can be generated under prediction-view-safe constraints, but are not yet ready for scoring.
- The work provides a reproducible benchmark/protocol foundation for future failure-attribution research.
- Negative results are scientifically useful because they show that proxy-heavy graph features and simple edge counts do not automatically solve structural failure attribution.

## Forbidden claims

- CCT improves automatic failure attribution.
- CCT outperforms baselines.
- CCT is robust under perturbations.
- CCT scoring is ready for calibration.
- Descriptor-augmented features improve scoring.
- The causal-flow redesign validates H1 or H2.
- The redesigned graph features are ready for scoring.
- Current results are paper-ready performance evidence.
- Current CCT features explain H6 outcomes.

## Required wording shift

Use language such as:

- "We present a protocol-first benchmark and representation audit for multi-agent failure attribution."
- "The controlled audits identify leakage, shortcut, and representation-degeneracy failure modes."
- "Negative findings show that naive structural scoring and simple causal-flow feature counts are insufficient."
- "The artifact provides a reproducible foundation for future method development."

Avoid language such as:

- "CCT outperforms baselines."
- "CCT improves attribution."
- "The redesigned features solve the scoring problem."
- "The method is robust or calibrated."

## H-status wording

The paper may state that H1/H2 remain unsupported under current evidence, H3/H4 are blocked, and H6 remains open but unsupported by scoring. It must not present these hypotheses as validated.
