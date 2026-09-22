# Jev Integration Proposal — Shaped by the Septuagint

## Status

**Proposal only. Do not implement or activate Jev from this document.**

This proposal asks for a deep architectural review of Jev as an independent evidence-adjudication layer in the existing GitHub → Hermes/Open Notebook → research inbox → adversarial review → canonical promotion workflow.

The target is not to have Jev interpret ancient texts. The target is to improve consistency at narrow classification and promotion boundaries after source-backed evidence has already been assembled.

## Why this repo is a strong candidate

The research registry already separates `classification`, `confidence`, support for the working hypothesis, counterevidence, alternative explanations, falsifiers, status, dependency, and linked evidence. That provides a structured state that a constrained judgment model can evaluate without asking it to generate scholarship.

**Working benefit hypothesis:** reduce inconsistent evidence classification and confirmation bias while making promotion/review decisions more reproducible. This must be benchmarked against expert/human judgments before activation.

## Candidate decision boundaries

The deep review should locate the exact source files and workflow steps where these decisions occur today:

1. Candidate evidence packet → `IN_REVIEW`/`CLASSIFIED`/`DISPUTED`/`REJECTED` routing.
2. Whether required counterevidence and alternative explanations are adequately represented.
3. Whether a proposed textual classification is supported strongly enough to retain versus mark disputed.
4. Whether source dependence has been sufficiently considered before treating observations as independent evidence.
5. Whether an allusion meets the stronger specificity/density controls required to enter NAR analysis.
6. Whether legacy material is ready to migrate into the canonical registry.
7. Whether a research packet is complete enough for human adversarial review.

Jev should be evaluated as a referee at these boundaries, not as the primary exegete.

## What Jev must not do

Jev must not:

- translate or reconstruct Greek/Hebrew texts;
- retrieve scholarship or verify page citations;
- decide textual variants from memory;
- perform quotation/allusion discovery;
- infer historical truth;
- generate missing counterevidence;
- collapse classification and confidence into one value;
- promote evidence into the canonical registry without the existing review process;
- replace specialist textual, historical, or literary judgment.

Source verification and deterministic registry validation must remain separate.

## Proposed record

One candidate evidence unit at a time, e.g.:

```json
{
  "evidence_id": "JHN-019-TXT",
  "source": "John",
  "passage": "...",
  "evidence_type": "quotation",
  "target_or_comparandum": "...",
  "source_relationship": "...",
  "module": "TXT",
  "proposed_classification": "...",
  "proposed_confidence": "Moderate",
  "supports_working_hypothesis": "mixed",
  "counterevidence": ["..."],
  "alternative_explanations": ["..."],
  "falsifier": "...",
  "source_support_verified": true,
  "known_ambiguities": ["..."]
}
```

The implementation should avoid sending entire books or research dumps when a compact verified record is sufficient.

## Candidate questions

Examples to refine during deep review:

- `classification_is_supported_by_record` → yes/no
- `counterevidence_is_materially_missing` → yes/no
- `serious_alternative_explanation_is_unaddressed` → yes/no
- `independence_is_overstated` → yes/no
- `confidence_is_too_high_for_record` → yes/no
- `ready_for_human_adversarial_review` → yes/no
- `recommended_routing` → choice: `retain`, `revise`, `dispute`, `reject`, `human_review`
- `evidential_maturity` → ordered score

Jev probabilities should inform routing; they should not silently rewrite canonical fields.

## Benchmark requirement

Build a historical gold set from records already adjudicated by the current methodology. Include supportive, contrary, mixed, dependent, disputed, rejected, and legacy examples across TXT/NAR/CUL/HIS where possible.

Measure:

- classification/routing agreement;
- false promotion rate;
- missed-counterevidence rate;
- calibration;
- performance by module;
- sensitivity to thesis direction (supportive versus contrary evidence);
- whether Jev treats hypothesis-supporting and hypothesis-opposing evidence symmetrically.

A key benchmark is **directional neutrality**: Jev must not be easier on evidence that supports the initiating thesis.

## Shadow mode

After a successful benchmark, run Jev on incoming research packets without changing the registry. Compare Jev recommendations with human adversarial review. Record disagreement cases and use them to improve question design, not to tune toward the preferred thesis.

## Architecture requirements

- One OpenRouter/Jev adapter only.
- `OPENROUTER_API_KEY` via environment/secret store; never commit the key.
- Pin and log model version during benchmark.
- Version question sets.
- Preserve input record hashes and returned probabilities.
- API failure must leave the current research workflow unchanged.
- Jev must never bypass source/page verification.

## Required deep-review deliverable

Create `docs/jev/DEEP_REVIEW.md` containing:

1. `GO`, `MODIFY`, or `NO-GO`.
2. Exact workflow insertion points.
3. Decisions that should instead be deterministic schema/tests.
4. Minimal record schema and typed question set.
5. Gold-set construction plan.
6. Bias/neutrality tests.
7. False-promotion versus false-rejection cost analysis.
8. Shadow-mode design.
9. Security/reproducibility risks.
10. Estimated benefit.
11. Implementation plan only if justified.

## Review instruction for Claude/Codex/Hermes

Challenge the proposal. Prefer deterministic registry validation, explicit methodological rules, source verification, and specialist review wherever they can resolve a decision without a model. Recommend Jev only for residual semantic adjudication that is repeated often enough to justify calibration and maintenance.
