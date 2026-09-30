# RQ3 inference — design note

**Status: DESIGN ONLY. No statistical test was run. No significance result appears in this note.**
Nothing outside `results/rq3_inference_design_2026-09-25/` was created or modified. No experiment was rerun
and no model API was called.

**Paper RQ3 as stated by the author:** *"How do zero-shot, zero-shot chain-of-thought, and one-shot
chain-of-thought prompting strategies affect model performance?"*

Labels used throughout:

- **VERIFIED FACT** — read directly from a repository artifact; the file and field are given here and in
  `EVIDENCE_MAP.md`.
- **STATISTICAL INTERPRETATION** — a methodological consequence of those facts.
- **RECOMMENDATION** — what I propose, for the author and supervisors to accept or reject.
- **LIMITATION** — something that would remain true even if the recommendation is adopted.

---

## 1. Design verification

### 1.1 Are exactly the same samples evaluated under all three strategies?

**VERIFIED FACT.** Yes, exactly. Recomputed from `descriptive_2026-09-21/authoritative_records.jsonl` over
all 150 cells:

| Dataset | Cells | Distinct full sample sets | Set size | Distinct attributable sets | Set size |
|---|---|---|---|---|---|
| Dreaddit | 75 | **1** | 715 | **1** | 699 |
| GoEmotions | 75 | **1** | 623 | **1** | 622 |

There is exactly **one** item set per dataset across every model, every strategy and every run, and exactly
one attributable subset. Checking model × run groups directly: **0 groups** in which the three strategies
differ in their attributable item set.

This matches the frozen plan, § 2: *"Within a dataset, all 15 configurations (model × strategy) were scored
on the identical 699 / 622 items."* Note that this sentence covers **strategy** pairs, not only model pairs.

**VERIFIED FACT — the strategy manipulation is clean.** One config per model runs all three strategies
against one dataset manifest with the same model id, provider pin, retry policy and endpoint
(`configs/pub_001_dreaddit_qwen.yaml`: `strategies: [zero-shot, zero-shot-cot, one-shot-cot]`,
`runs: 5`, one `datasets:` entry). The only thing that varies between the three conditions is the prompt set.

**VERIFIED FACT — one apparent exception, checked and cleared.** `prompt_set_sha256` is `8a65d46237d2…` in
29 of the 30 dataset × model × strategy cells, but `d831e49717af…` in
`dreaddit | google/gemma-4-31b-it | one-shot-cot | run 5` (the `pub_013` replacement cell). Comparing the
per-agent prompt hashes recorded on the attempts of `pub_013` against `pub_011`:

| Agent | pub_011 (runs 1–4) | pub_013 (run 5) |
|---|---|---|
| emotion | `38e256ccaf1e0cb6` (3,771 ch) | `38e256ccaf1e0cb6` (3,771 ch) |
| symptom | `d049410a8b20b31e` (4,572 ch) | `d049410a8b20b31e` (4,572 ch) |
| context | `ca91dbb511c26235` (3,442 ch) | `ca91dbb511c26235` (3,442 ch) |
| referral | `b16db6cd21abc1ee` (5,078 ch) | `b16db6cd21abc1ee` (5,078 ch) |
| report | `0ff2166f07f8cc1c` (8,324 ch) | `0ff2166f07f8cc1c` (8,324 ch) |

All five are byte-identical. `prompt_set_sha256` hashes the enclosing prompt-set directory, which changed
between the two run dates for reasons unrelated to the one-shot-CoT prompt text. **The prompt actually used
was the same.** This should be stated in the paper rather than left for a reviewer to find.

### 1.2 Are the observations paired at the sample level?

**VERIFIED FACT.** Yes. The frozen plan, § 2: *"A comparison of configuration A with configuration B is
paired **by item**."* Because a configuration is a model × strategy pair and the item set is identical, a
strategy contrast within a model is an item-paired comparison in exactly the same sense as the RQ1 model
contrasts that were already tested.

### 1.3 How do the five runs interact with the pairing?

**VERIFIED FACT — runs are explicitly NOT paired across configurations.** Frozen plan, § 2:

> *"Runs are **not** paired across configurations. Run *k* of A and run *k* of B were executed at different
> times, on different processes and sometimes on different machines, so the run index carries no shared
> information."*

**VERIFIED FACT — pooling runs as independent observations is already ruled out.** Frozen plan, § 3:

> *"The 5 runs are repeated measurements of the **same** item under the same configuration. They are *not* 5
> independent samples: treating 5 × 699 records as 3,495 independent observations would be
> pseudoreplication."*

**VERIFIED FACT — the frozen estimand.** § 3: *"The runs stay nested inside their item. The estimand is the
frozen five-run quantity: the mean over the 5 runs of the per-run metric… For accuracy-type metrics this
equals the mean over items of each item's 5-run average correctness, so no information is discarded."*

### 1.4 Should each model × dataset be analysed separately?

**VERIFIED FACT.** The frozen design already separates by dataset (separate Holm families, separate item
pools, separate baselines) and the plan's D1 option (c) — averaging an effect over the three strategies — was
rejected with the reason: *"it averages over strong model × strategy interactions (e.g. Phi-4 GoEmotions
one-shot-CoT)."*

**STATISTICAL INTERPRETATION.** The same argument applies with the roles swapped. Pooling a strategy effect
over five models would average over model × strategy interactions that the descriptive results show are
large and of opposite sign (for example, one-shot-CoT is the highest-accuracy strategy for some models and
the lowest for others). A pooled "strategy main effect" would therefore be an average of heterogeneous
quantities and would not answer the paper's question for any particular model.

**RECOMMENDATION.** Analyse **within model × dataset**. Report the 5 models × 2 datasets separately. Do not
report a pooled main effect of strategy.

### 1.5 Do safety intercepts and invalid outputs affect the pairing?

**VERIFIED FACT — safety intercepts do not.** Frozen plan, § 8: *"They are excluded from model attribution,
as frozen. The excluded items are identical in every cell (16 / 1), so they are removed once from the item
pool and never resampled."* Confirmed above: exactly one attributable set per dataset. Safety intercepts are
therefore **neutral** for a strategy contrast — they remove the same 16 (Dreaddit) or 1 (GoEmotions) items
from every arm.

**VERIFIED FACT — invalid outputs do, if and only if the metric conditions on validity.** Invalid outputs
differ by configuration, so the set of *valid* predictions differs between strategies. Recomputed
complete-case counts, i.e. how many items would survive if a comparison required a valid prediction in every
arm:

| Dataset | Model | Attributable n | Worst strategy pair, single run | All 3 strategies, single run | All 3 strategies × all 5 runs |
|---|---|---|---|---|---|
| Dreaddit | Gemma 4 31B | 699 | 699 | 699 | 699 |
| Dreaddit | Llama 4 Scout | 699 | 663 | 662 | 585 |
| Dreaddit | Phi-4 | 699 | 662 | 659 | 576 |
| Dreaddit | Mistral Small 4 | 699 | 698 | 698 | 698 |
| Dreaddit | Qwen3.5 27B | 699 | 641 | 641 | 633 |
| GoEmotions | Gemma 4 31B | 622 | 618 | 618 | 615 |
| GoEmotions | Llama 4 Scout | 622 | 572 | 566 | 530 |
| GoEmotions | **Phi-4** | 622 | **333** | **319** | **195** |
| GoEmotions | Mistral Small 4 | 622 | 615 | 615 | 609 |
| GoEmotions | Qwen3.5 27B | 622 | 620 | 620 | 620 |

**STATISTICAL INTERPRETATION.** Effective accuracy and macro-F1 as frozen are computed on the **attributable**
denominator, so the pairing is complete and balanced: every arm is scored on all 699 / 622 items. Conditional
accuracy is not, and a complete-case strategy comparison would in the worst case retain 195 of 622 items
(Phi-4 / GoEmotions) — and precisely the items the model was able to answer. That is not a missing-at-random
deletion; it changes the estimand from "performance on the benchmark" to "performance on the subset this
configuration could parse".

### 1.6 Which outcome should RQ3 use?

**VERIFIED FACT — what the frozen design treats as primary.** The plan makes effective accuracy and macro-F1
the two co-primary metrics for RQ1, effective accuracy the primary metric for RQ2, and states of conditional
accuracy: *"CIs only (configuration level and RQ1 pair differences). No p-values and no Holm."*

**VERIFIED FACT — why conditional accuracy is secondary.** Frozen plan, § 7: *"Conditional accuracy
(correct / valid) has a different denominator for each configuration. A 'paired' comparison of conditional
accuracy therefore compares different item subsets."*

**RECOMMENDATION.** **Both** effective accuracy and macro-F1, as co-primary, mirroring RQ1. Effective accuracy
answers "does the strategy change how often the system gets the benchmark item right, counting unusable
output as wrong"; macro-F1 answers "does the strategy change performance across classes rather than on the
majority class". The completed results package already shows these two metrics rank strategies differently
within a model, so reporting only one would be a metric-selection decision made after seeing the data.
Conditional accuracy stays **descriptive**, with CIs only, exactly as in the frozen plan.

### 1.7 Did the frozen plan prohibit RQ3 inference, or simply not include it?

This distinction matters and the evidence is specific.

**VERIFIED FACT.** The plan's title is *"Statistical analysis plan: inferential RQ1 / RQ2"*. RQ3 is outside
its declared scope by title.

**VERIFIED FACT.** The only substantive RQ3 statement in section C reads:

> *"**RQ3.** Descriptive only; no inferential latency analysis. The confounds documented in
> `rq1_rq3_reporting_2026-09-21/REPORT.md` (3 s quantisation, fixed strategy order, machine, provider and
> time, concurrent load for Llama Dreaddit, no per-agent timing) mean no test could attribute a latency
> difference to the prompting strategy."*

and section E adds the two-word line: *"**RQ3.** No inference."*

**STATISTICAL INTERPRETATION.** In the frozen plan, **RQ3 means latency/efficiency**, and the stated reason
for refusing inference is a list of **latency-specific** confounds — poll quantisation, machine, provider,
concurrent load, absence of per-agent timing. None of those reasons applies to a comparison of accuracy or
macro-F1. The plan therefore **did not prohibit strategy inference on the quality metrics; it never
considered it**, because the author's RQ3 at that time was a different question from the paper's RQ3 now.

**LIMITATION.** "Not prohibited" is not the same as "pre-specified". See § 7.

---

## 2. The statistical unit

**RECOMMENDATION. The statistical unit is the benchmark item (sample), carrying all of its repeated
measurements.** Concretely, for a contrast of strategy S₁ against strategy S₂ within one model and one
dataset, item *i* contributes one paired observation:

```
item i  →  ( mean over 5 runs of correctness under S₁ ,  mean over 5 runs of correctness under S₂ )
```

with correctness defined as frozen **effective** correctness: valid **and** equal to ground truth; an invalid
output is incorrect.

Why this unit and not the alternatives:

| Candidate unit | Verdict | Reason |
|---|---|---|
| Individual sample prediction (item × run), pooled | **Rejected** | 5 × 699 = 3,495 correlated records treated as independent. The frozen plan names this explicitly: *"treating 5 × 699 records as 3,495 independent observations would be pseudoreplication."* |
| Run-level metric (n = 5 per configuration) | **Rejected** | Runs are not paired across configurations (frozen plan § 2), so a paired run-level test has no valid pairing. The plan also records the power consequence: *"With n = 5 the smallest attainable two-sided exact Wilcoxon p-value is 0.0625, so no comparison could ever reach 0.05 before correction."* It also discards item-sampling uncertainty entirely. |
| **Item, with runs nested inside it** | **Recommended** | Preserves the within-item dependence across runs, preserves the between-strategy pairing, and reproduces the frozen five-run estimand exactly: *"For accuracy-type metrics this equals the mean over items of each item's 5-run average correctness, so no information is discarded."* |
| Item, after majority-vote collapse (≥ 3/5) | **Secondary only** | One binary per item makes exact McNemar applicable, which is why the frozen plan uses it as a secondary check (D2), but it discards the within-item run variation. |

**STATISTICAL INTERPRETATION.** The number of independent units for a strategy contrast is therefore
**699 (Dreaddit) or 622 (GoEmotions)** — not 3,495 / 3,110, and not 5.

---

## 3. Proposed tests

### 3.1 Effective accuracy

**RECOMMENDATION — primary: paired item-level permutation test, exactly the frozen RQ1 procedure applied to
strategy pairs.**

For each item, with probability ½ swap the *entire five-run outcome vector* of strategy S₁ with that of
strategy S₂, recompute both configurations' five-run effective accuracy on the swapped data, and form the
difference. P = 10,000 swap sets; p = (1 + #{|T\*| ≥ |T_obs|}) / (1 + P).

**VERIFIED FACT — the existing code is already configuration-generic.** In
`inferential_2026-09-21/code/run_inferential.py`, the permutation routine is
`def perm_pair(ci, cj): """Swap test: for swapped items, A receives B's five run outcomes and vice versa."""`
— it takes two configuration indices, with no assumption that they share a strategy. The count tensor is
indexed by configuration, and the same routine already returns statistics for both `acc_eff` and `macro_f1`.
**Applying it to strategy pairs requires no methodological change — only a different list of pairs and a
different Holm family.**

**RECOMMENDATION — confidence intervals: paired item-cluster bootstrap, B = 4,000**, percentile intervals,
one shared index vector per dataset across all configurations, exactly as frozen (plan §§ 4–5).

**RECOMMENDATION — secondary: exact McNemar on majority-vote effective correctness** (correct in ≥ 3 of 5
runs; 5 is odd so there are no ties), in its own Holm family, as the conservative check. This mirrors decision
D2 and gives the reviewer a test with no Monte-Carlo component.

**Why not a plain McNemar as the primary test?** Frozen plan § 6: *"Each item has 5 outcomes per
configuration, not 1, so McNemar **cannot be applied without an aggregation decision**."* The aggregation
throws away run-to-run variation, which for a strategy comparison is part of what is being compared.

**Why not a repeated-measures model (GLMM / GEE with item and run random effects)?** *STATISTICAL
INTERPRETATION.* It is a defensible alternative and would use the run structure more richly. Three arguments
against making it primary here: (i) it introduces distributional assumptions the frozen analysis deliberately
avoided, so RQ1 and RQ3 would rest on different inferential foundations in the same paper; (ii) with 5 runs it
would estimate a run-level variance component from very few levels; (iii) it is not reproducible from the
existing frozen code. If a supervisor prefers it, it should be a **sensitivity analysis**, not the primary.

### 3.2 Macro-F1

**VERIFIED FACT — macro-F1 is not decomposable into per-item contributions.** The frozen plan states
*"McNemar does not apply to macro-F1 or conditional accuracy, which are not per-item binary outcomes."*
Macro-F1 is a dataset-level functional of the whole confusion matrix.

**RECOMMENDATION — do not force the accuracy test onto macro-F1. Use the permutation test, but only because
it is a *recompute-the-statistic* procedure**, not because it is the same test. The item-level swap is valid
for any statistic that is a function of the item set: swap whole items between arms, **recompute macro-F1
from scratch on the swapped assignment**, and compare with the observed difference. This is what the frozen
code already does (`T_obs_f1 = OBS["macro_f1"][ci] − OBS["macro_f1"][cj]`, with the permuted statistic
recomputed, not decomposed). CIs likewise come from recomputing macro-F1 inside each bootstrap replicate.
**No McNemar, and no per-item contribution, for macro-F1.**

**LIMITATION — GoEmotions class support.** *VERIFIED FACT:* the frozen plan already restricts per-class
inference — *"No inference on the GoEmotions anxiety class (n = 6: one item moves recall by 1/6)"* — and
records that *"GoEmotions anxiety has 6 items, so about 0.25% of replicates (≈ 10) will contain no anxiety
item. MetricPolicy 1.0.0 then sets the undefined recall and F1 to 0."* *STATISTICAL INTERPRETATION:* with
supports of 487 / 81 / 33 / 15 / 6 on the attributable pool, a fifth of GoEmotions macro-F1 rests on six items, so macro-F1 CIs there
are very wide and the strategy contrast will have low power. That is a **property of the benchmark subset,
not a fixable analysis choice.** A non-significant GoEmotions macro-F1 contrast must be reported as
*inconclusive*, never as evidence of no difference.

**RECOMMENDATION.** Report, alongside every GoEmotions macro-F1 contrast, the number of bootstrap replicates
containing no `anxiety` item, as the frozen plan already requires.

---

## 4. Multiple comparisons

**The contrasts.** 3 strategy pairs (ZS vs ZS-CoT, ZS vs 1S-CoT, ZS-CoT vs 1S-CoT) × 5 models × 2 metrics =
**30 hypotheses per dataset**, 60 in total.

**VERIFIED FACT — the frozen precedent.** RQ1 uses *"one Holm family per dataset covering both primary
metrics"* — 10 model pairs × 3 strategies × 2 metrics = 60 per dataset — chosen because it is *"conservative,
no tiny families, and it respects strategy"*. RQ2 uses one family of 15 per dataset. The McNemar secondary
check always gets **its own** family.

**RECOMMENDATION.**

| Family | Members | Size |
|---|---|---|
| `RQ3-primary-dreaddit` | 3 strategy pairs × 5 models × {effective accuracy, macro-F1} | 30 |
| `RQ3-primary-goemotions` | same | 30 |
| `RQ3-mcnemar-dreaddit` | 3 strategy pairs × 5 models, effective accuracy only | 15 |
| `RQ3-mcnemar-goemotions` | same | 15 |

**Why one family per dataset and not per model.** *STATISTICAL INTERPRETATION.* The five models are analysed
on the same item set within a dataset and are reported together as one claim ("how strategy affects
performance"); splitting into five families of 6 would make each correction weaker purely because the results
were sliced more finely. Conversely, merging the two datasets into one family of 60 would apply a
GoEmotions-driven penalty to Dreaddit conclusions that are about a different item pool and a different task.
One family per dataset matches the frozen precedent exactly and is the choice that is **hardest to pass**
among the defensible options, which is the right property here.

**Explicitly rejected:** one family per model × dataset (6 tests each); one family per metric; a family that
drops the metric dimension. Each would increase the number of significant results, and none has a
justification independent of that effect.

**LIMITATION — study-wide error rate.** Holm controls the family-wise error rate **within** each declared
family. RQ1, RQ2 and a new RQ3 reuse the same items and the same configurations, so the study-wide error rate
across all three research questions is not controlled by any of these corrections. This should be stated in
the limitations, as it already implicitly applies to RQ1 versus RQ2.

---

## 5. How the five runs enter the inference

**RECOMMENDATION — aggregate within item, cluster by item, do not resample runs.** Precisely:

1. For each item × configuration, keep all five per-run outcomes.
2. The estimand is the frozen five-run quantity — the mean over runs of the per-run metric.
3. The bootstrap resamples **items** (with replacement), each item carrying all of its configurations × 5 runs.
4. The permutation swaps **whole items**, moving all five runs together.
5. Runs are **not** resampled, and run *k* of S₁ is never matched to run *k* of S₂.

**VERIFIED FACT — this is the frozen methodology, not a new choice.** Plan § 4: *"Cluster = one item,
carrying all of its 15 configurations × 5 runs = 75 predictions per dataset. Resampling whole items keeps the
within-item dependence across runs, which is where pseudoreplication would come from, and the
between-configuration pairing, which is what makes differences precise."* Plan § 5: *"draw 699 (or 622) item
indices **with replacement** … using one index vector shared by all 15 configurations of that dataset."*

**Trade-offs, stated honestly:**

| Option | Pro | Con | Verdict |
|---|---|---|---|
| Aggregate to item means first, then cluster-bootstrap items | Matches the frozen estimand; no pseudoreplication; reuses frozen code | Run-to-run variability is not propagated into the interval | **Recommended** |
| Two-stage bootstrap (resample items **and** runs) | Propagates stochastic-decoding uncertainty | *VERIFIED FACT*, plan D3: *"Two-stage resampling with only 5 runs gives unstable variance estimates"*; and it would change the estimand away from the frozen five-run quantity, so RQ3 would no longer be comparable with RQ1 and RQ2 | **Rejected as primary**; possible sensitivity analysis |
| Paired run-level test (n = 5) | Simple | Runs are not paired across configurations; exact Wilcoxon floor is p = 0.0625 at n = 5, so nothing could survive correction; ignores item sampling | **Rejected** |
| Majority-vote collapse (≥ 3/5), then McNemar | Exact, assumption-light, no Monte Carlo | Discards within-item run variation | **Recommended as the secondary check only** |

**LIMITATION.** The recommended intervals express **item-sampling** uncertainty **conditional on the five
observed runs**. They are not "what would happen with a different set of runs". The run-to-run SD must
continue to be reported separately, as in the descriptive tables. This matters most where run variability is
extreme — the completed results package flags one configuration with a five-run effective-accuracy SD above
0.12 and another with an SD of exactly 0.

---

## 6. Invalid outputs in a paired strategy comparison

**RECOMMENDATION — represent an invalid output as an incorrect answer on the attributable denominator.
Do not delete it, and do not condition on validity.**

**VERIFIED FACT.** This is the frozen rule, already applied in RQ1 and RQ2. Plan § 7: *"They are kept exactly
as frozen. For effective accuracy and macro-F1 they count as not-correct on the attributable denominator."*
§ 6: *"'Correct' is the frozen **effective** correctness: valid and equal to ground truth. A model-invalid
output is **incorrect**."*

**STATISTICAL INTERPRETATION — why this matters more for RQ3 than for RQ1.** A prompting strategy changes how
the model formats its answer, not only what it decides. The completed results package records a
configuration whose effective accuracy falls by 0.0887 relative to zero-shot while its *conditional* accuracy
falls by less than half that, with evaluability dropping from 0.9980 to 0.9230 — i.e. much of the effective
difference is a serialisation effect. **This is not a nuisance to be removed; for RQ3 it is part of the
effect being measured.** A reader asking "how does prompting strategy affect performance?" is asking about
deployed behaviour, and output the system cannot parse is a real cost of that strategy. Deleting invalid
outputs would answer a different question.

**RECOMMENDATION — report the mechanism alongside the effect, without changing the estimand.** For every
strategy contrast, report the paired change in **evaluability** as a descriptive companion column, so a
reader can see how much of an effective-accuracy difference co-occurs with a change in parseability. This is
a descriptive decomposition, **not** a mediation analysis, and must not be described as one.

**Would conditional accuracy introduce selection bias here? — Yes.**

- *VERIFIED FACT.* Denominators differ by configuration (plan § 7), and the complete-case table in § 1.5 shows
  the retained item count falling to 195 of 622 in the worst case.
- *VERIFIED FACT.* The completed results package's exploratory analysis found class-selective invalidity
  surviving Holm correction in 4 of 30 configurations, the strongest with invalid items enriched in one class
  by a factor of about 1.85.
- *STATISTICAL INTERPRETATION.* The items that drop out are not a random sample of the benchmark, they differ
  by arm, and the model's would-be answer on a dropped item is unobservable, so the **direction** of the bias
  is not identifiable.

**RECOMMENDATION.** Conditional accuracy remains **secondary and descriptive**: CIs only, no p-values, no
Holm, labelled *"conditional on each configuration's own evaluable predictions; denominators differ"* — the
wording already used in the frozen package. It must not be used to rank strategies.

---

## 7. Relationship to the frozen analysis plan

**The honest answer is C — post-hoc.** Specifically: **a post-hoc analysis that reuses a pre-specified
estimation procedure.** It is not (A), and calling it (B) would overstate it.

Why not **A (already specified, not run)**: the plan's title is *"inferential RQ1 / RQ2"*; no strategy
contrast is enumerated anywhere in it; its decision table (D1–D4) never mentions one; and section E says
*"RQ3. No inference."*

Why not **B (a justified extension)** without qualification: the descriptive strategy results are already
known to the analyst, including which contrasts look large. Choosing to test now, after seeing them, is
selection of hypotheses on the basis of observed data. The fact that the *procedure* is pre-specified does not
make the *hypotheses* pre-specified.

Why it is nevertheless **a disciplined** post-hoc analysis, and what should be said about that:

- **VERIFIED FACT.** The estimation machinery, the estimand, the pairing rule, the clustering rule, the
  invalid-output rule, the safety-intercept rule and the Holm procedure were all fixed on 2026-09-21 *"before
  any test was run"*, and the code is configuration-generic. Nothing about the method would be chosen after
  seeing an RQ3 p-value.
- **VERIFIED FACT.** The plan's refusal of RQ3 inference was reasoned about **latency** confounds, not about
  accuracy. So this is not overriding a considered prohibition on the quality metrics.
- **LIMITATION.** The full contrast set (3 pairs × 5 models × 2 metrics per dataset) must be declared and
  reported **in full** before the analysis is run — every contrast, significant or not. Reporting a subset
  afterwards would convert a disciplined post-hoc analysis into selective reporting.

### Required labelling in the paper

- Call it **post-hoc / exploratory** in the methods section, in those words.
- State that the statistical procedure was pre-specified and frozen on 2026-09-21 for RQ1/RQ2 and was applied
  unchanged, and that the RQ3 contrasts were declared before the tests were run but after the descriptive
  results were known.
- Report all 60 contrasts (30 per dataset), with effect sizes and CIs, not only the significant ones.
- Do not describe an RQ3 result as "confirming" a hypothesis.
- Keep RQ1 and RQ2 labelled as pre-specified confirmatory analyses, so the distinction is visible to a reader.
- **RECOMMENDATION.** Write and freeze a short RQ3 analysis-plan addendum — the specification in § 8 — with a
  timestamp and hashes of its inputs, before running anything, exactly as was done on 2026-09-21. That is what
  makes the post-hoc label survive scrutiny.

---

## 8. Proposed RQ3 analysis specification — NOT EXECUTED

Present this to the supervisors for approval. Nothing below has been run.

| Element | Specification |
|---|---|
| **Estimand** | Within one dataset and one model, the difference between two prompting strategies in the frozen five-run metric, on the fixed attributable item pool (699 Dreaddit / 622 GoEmotions), conditional on the five observed runs. |
| **Statistical unit** | The benchmark item, carrying all of its 5 runs under each strategy. n = 699 / 622. |
| **Primary metric** | Effective accuracy (correct ÷ attributable; an invalid output is incorrect). |
| **Co-primary metric** | Macro-F1, unweighted over the fixed label list, per `MetricPolicy 1.0.0`. |
| **Secondary, descriptive only** | Conditional accuracy (CIs only, no tests); evaluability change per contrast. |
| **Strategy contrasts** | zero-shot vs zero-shot-CoT; zero-shot vs one-shot-CoT; zero-shot-CoT vs one-shot-CoT. Within model, within dataset. 3 × 5 × 2 datasets = 30 contrasts per metric. |
| **Treatment of 5 runs** | Runs nested inside the item; item means over runs; runs never paired across strategies; runs not resampled. |
| **Treatment of invalid outputs** | Kept; counted as incorrect on the attributable denominator. No deletion, no repair, no rescoring. |
| **Treatment of safety intercepts** | Excluded once from the item pool, as frozen; identical in every arm, therefore neutral to the contrast. |
| **Test — effective accuracy** | Paired item-level permutation, whole five-run vectors swapped per item, P = 10,000; p = (1 + #{\|T\*\| ≥ \|T_obs\|}) / (1 + P). Seed string declared and recorded before running. |
| **Test — macro-F1** | Same item-level swap, but the statistic is **recomputed** from the swapped confusion matrices, not decomposed. No McNemar. |
| **Secondary test** | Exact McNemar on per-item majority-vote effective correctness (≥ 3 of 5), effective accuracy only, own Holm family. |
| **Confidence intervals** | Paired item-cluster bootstrap, B = 4,000, 95% percentile intervals, one shared index vector per dataset. CIs on the **difference**, and on each configuration. |
| **Correction** | Holm–Bonferroni within family. |
| **Families** | `RQ3-primary-dreaddit` (30), `RQ3-primary-goemotions` (30), `RQ3-mcnemar-dreaddit` (15), `RQ3-mcnemar-goemotions` (15). |
| **Threshold** | α = 0.05 on the Holm-adjusted p-value, matching the frozen plan. |
| **Reporting** | All 60 primary contrasts reported with difference, 95% CI, raw p, Holm-adjusted p and decision — significant or not. Plus evaluability change and the count of bootstrap replicates containing no GoEmotions `anxiety` item. |
| **Status** | **Post-hoc / exploratory.** Procedure pre-specified 2026-09-21; contrasts declared in this note, after the descriptive results were known. |
| **Outputs** | A new directory, e.g. `results/rq3_inferential_2026-XX-XX/`, with its own plan addendum, code, replicate files, manifest and checksums. **No existing package is modified.** |

### What this analysis WOULD let you say

- "Within model *M* on dataset *D*, one-shot chain-of-thought differed from zero-shot in effective accuracy by
  Δ (95% CI …); this difference was / was not significant after Holm correction across the 30 strategy
  contrasts for that dataset."
- "The direction and size of the strategy effect differs across models" — if that is what the contrasts show —
  "so no single strategy is best across models."
- "Accuracy and macro-F1 do not agree about the strategy ordering for model *M*" — with both tested, this
  becomes a statistical statement rather than a descriptive one.
- "For model *M*, the effective-accuracy difference between strategies co-occurs with a change in
  evaluability of X points", as a descriptive companion.
- Honest negative results: "no strategy contrast reached significance for dataset *D* on macro-F1", with the
  power limitation stated.

### What this analysis would still NOT let you say

- **"Chain-of-thought prompting improves performance"** as a general claim. The design supports within-model,
  within-dataset contrasts only; a pooled main effect is not recommended and would average over large
  interactions.
- **Any causal attribution to a single prompt property.** Strategy, prompt length and exemplar presence change
  together across the three conditions; nothing in this design separates them.
- **"Strategy X is best."** Two metrics, five models and two datasets will not agree, and the analysis is
  post-hoc.
- **Anything about latency or efficiency.** Those confounds are real and unaddressed; the frozen plan's
  refusal stands.
- **A confirmatory claim.** The label is exploratory regardless of how small the p-values are.
- **A conclusion of "no difference" from a non-significant GoEmotions macro-F1 contrast.** With six `anxiety`
  items, that contrast is underpowered; the correct word is *inconclusive*.
- **Any statement about mechanism** — why a strategy changes behaviour. The invalid-output audit keeps that
  question separate and open.

---

## 9. Unresolved questions requiring a human decision

1. **Approve or reject the post-hoc label.** If the supervisors want a confirmatory RQ3, that needs a new
   pre-registered analysis on data not yet examined — which this grid is not.
2. **Co-primary or single primary metric?** This note recommends both effective accuracy and macro-F1 as
   co-primary, mirroring RQ1. Choosing one would halve each Holm family to 15 and make significance easier;
   that is a reason for caution, not for doing it.
3. **Family definition.** One family per dataset (30) is recommended. A supervisor may prefer one family per
   dataset per metric (15), matching an earlier precedent. Decide **before** running.
4. **Is a pooled strategy main effect wanted at all?** Not recommended. If a supervisor wants one, it needs
   its own model (e.g. a mixed-effects model with item and model random effects) and its own justification,
   and the interaction should be reported alongside it.
5. **Should a GLMM/GEE sensitivity analysis be run?** Optional. If yes, declare it as a sensitivity analysis
   now, not after seeing the permutation results.
6. **Disclosure of the July protocol discrepancy.** *VERIFIED FACT:* the frozen plan already notes that the
   July `AnxioSense_Experimental_Setup.docx` § 6.4 specified *"Wilcoxon signed-rank + Bonferroni"*, that this
   is *"Not appropriate here"*, and that *"this discrepancy should be disclosed in the paper."* Since the July
   protocol's test was over runs, this disclosure is **more** relevant to RQ3 than to RQ1. Decide the exact
   wording.
7. **The Gemma `prompt_set_sha256` difference** (§ 1.1) is cleared at the prompt-text level but should still
   be disclosed in the replication package so no reviewer has to rediscover it.
8. **Whether to report the evaluability companion column** as recommended in § 6, and how to word it so it is
   not read as a mediation analysis.
9. **Study-wide multiplicity.** Whether the paper acknowledges that RQ1, RQ2 and RQ3 share the same items and
   that no correction spans them.

---

## 10. What was inspected for this note

`configs/pub_001_dreaddit_qwen.yaml`; `descriptive_2026-09-21/authoritative_records.jsonl` (150 cells,
100,350 records, recomputed item sets); `descriptive_2026-09-21/parsed/*.jsonl` (prompt-set hashes);
`runs/pub_013_.../raw/attempts.jsonl` and the external evidence copy of `runs/pub_011_.../raw/attempts.jsonl`
(per-agent prompt hashes); `inferential_2026-09-21/STATISTICAL_ANALYSIS_PLAN.md` (sections A–F);
`inferential_2026-09-21/code/run_inferential.py` (permutation and bootstrap routines);
`inferential_2026-09-21/tables/*.csv` (family names and coverage);
`invalid_output_audit_2026-09-25/invalid_outputs_row_level.jsonl`;
`final_rq_results_2026-09-25/` (existing descriptive strategy tables).

Per-claim file and line references are in `EVIDENCE_MAP.md`.
