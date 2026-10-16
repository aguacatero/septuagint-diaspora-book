# Jev Integration Proposal — Shaped by the Septuagint

## Status

**Proposal only. Do not implement or activate Jev from this document.**

Evaluate Jev as a constrained evidence-adjudication layer in the GitHub → Hermes/Open Notebook → research inbox → adversarial review → canonical promotion workflow. Jev must not act as an exegete, translator, source retriever, or historian.

## Candidate role

Potential residual semantic judgments include evidence routing, adequacy of counterevidence/alternatives, overstatement of source independence, readiness for adversarial review, allusion eligibility, and whether a proposed confidence/classification is too strong for the verified record.

Jev must never bypass source/page verification, specialist textual judgment, or the canonical review process.

# Required deep-review skill stack

Use the skills below **in this order**. A generic repo review is insufficient.

## Skill sources

- Matt Pocock skills: `https://github.com/mattpocock/skills`
- K-Dense Scientific Agent Skills: `https://github.com/K-Dense-AI/scientific-agent-skills`

If installed, invoke by skill name. Otherwise read the named `SKILL.md` from the source repo and execute its procedure.

## Pass 1 — Map the research workflow

**Call:** Matt `research`

Inspect the project constitution, registry schema, current batch, TXT/NAR/CUL/HIS workflows, source-verification rules, adversarial-review path, and this proposal.

Output: `docs/jev/review/01_REPO_MAP.md`

Map every current classification/promotion judgment, its source files, and which parts can already be handled deterministically.

## Pass 2 — Methodological red team

**Call:** K-Dense `scientific-critical-thinking`

Stress-test confirmation bias, dependency/non-independence, circular classification, thesis-direction bias, evidence hierarchy, claim/evidence separation, and whether Jev could reward records merely because they are written persuasively.

Output: `docs/jev/review/02_CRITICAL_REVIEW.md`

Require symmetry tests: evidence supporting and opposing the working hypothesis must be judged by the same standard.

## Pass 3 — Scholarship/evidence review simulation

**Call:** K-Dense `peer-review`

Use its claim–evidence and reproducibility discipline to review the proposed Jev method. Adapt it to this humanities/historical-text context; do **not** pretend its biomedical frameworks replace textual criticism or ancient-language expertise.

Output: `docs/jev/review/03_PEER_REVIEW.md`

Explicitly list where specialist Greek/Hebrew, textual-critical, literary, or historical review remains mandatory.

## Pass 4 — Literature/method audit

**Call:** K-Dense `literature-review`

Use only for bounded methodological questions that need external scholarship—for example textual dependency, quotation/allusion methodology, inter-rater classification, or relevant historical-critical standards. Preserve the repo’s primary-source-first discipline.

Output when used: `docs/jev/review/04_METHOD_LITERATURE.md`

## Pass 5 — Benchmark design

**Call:** K-Dense `experimental-design`

Design a blinded comparison of:

- current human/adversarial classification;
- deterministic registry/schema rules;
- any current general-LLM baseline;
- Jev.

Create development and untouched holdout sets. Block/stratify by module (`TXT/NAR/CUL/HIS`), supportive vs contrary evidence, dependency class, and difficulty so the benchmark cannot look good by overrepresenting easy cases.

Output: `docs/jev/review/05_BENCHMARK_DESIGN.md`

## Pass 6 — Benchmark size / precision

**Call:** K-Dense `statistical-power`

Determine the sample needed to estimate false promotion, missed counterevidence, disagreement, and module-specific performance with useful precision. Do not accept an arbitrary gold-set size.

Output: `docs/jev/review/06_SAMPLE_PRECISION.md`

## Pass 7 — Model the decision vocabulary

**Call:** Matt `domain-modeling`

Sharpen terms including classification, confidence, source relationship, independence, counterevidence, alternative explanation, falsifier, disputed, rejected, canonical promotion, and human adversarial review.

Output: `docs/jev/review/07_DECISION_MODEL.md`

## Pass 8 — Design the Jev seam

**Call:** Matt `codebase-design`

Prefer one narrow adapter over distributed model calls. Specify the minimum verified evidence record, typed questions, fail-safe behavior, logs, model/question versioning, and test fake.

Output: `docs/jev/review/08_ARCHITECTURE.md`

## Pass 9 — Resolve remaining choices

**Call:** Matt `grill-with-docs`

Grill only unresolved decisions: acceptable false-promotion ceiling, whether Jev may only flag/review rather than promote, shadow duration, confidence thresholds, and model-update policy.

Output: `docs/jev/review/09_DECISIONS.md`

## Pass 10 — Final deep review

Create `docs/jev/DEEP_REVIEW.md` containing:

1. `GO`, `MODIFY`, or `NO-GO`.
2. Exact workflow insertion points.
3. Deterministic/source-verification checks that precede Jev.
4. Minimal record and typed questions.
5. Directional-neutrality and dependency-bias tests.
6. Development/gold/holdout construction.
7. Baselines and benchmark metrics.
8. False-promotion versus false-rejection cost analysis.
9. Specialist-review requirements.
10. Shadow-mode plan.
11. Security/reproducibility/versioning risks.
12. Implementation plan only if justified.

## After GO/MODIFY

**Call:** Matt `to-spec` to turn the accepted review into an implementation spec.

After implementation:

- **Call:** Matt `code-review` for standards/spec fidelity.
- **Call:** K-Dense `statistical-analysis` for blinded holdout/shadow results, calibration/error estimates, subgroup behavior, and baseline comparisons.

## Review instruction

Try to eliminate Jev first. Prefer explicit registry rules, deterministic validation, verified primary-source support, and specialist scholarship. Jev is justified only for repeated residual semantic adjudication where blinded benchmarking shows added value without thesis-direction bias.
