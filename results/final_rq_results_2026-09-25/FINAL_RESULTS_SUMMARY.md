# AnxioSense — Results Summary

## Study at a Glance

- **Datasets:** Dreaddit — binary stress detection, **699** attributable items per run, majority
  baseline **0.5079**. GoEmotions — 5-class distress classification, **622** attributable items per
  run, majority baseline **0.7830**.
- **Models (5):** Llama 4 Scout, Phi-4, Gemma 4 31B, Mistral Small 4, Qwen3.5 27B — all served via
  OpenRouter, one pinned provider each.
- **Prompting strategies (3):** zero-shot, zero-shot-CoT, one-shot-CoT.
- **Runs:** **5 per configuration**, so every reported figure is a five-run mean with an SD.
- **Scale:** 2 × 5 × 3 = **30 configurations**, **150 configuration-cells**, **100,350 records**.
- **Primary publication metric:** **effective accuracy** = correct ÷ attributable. Invalid outputs
  count as incorrect, so the denominator never shrinks.
- **Reported alongside it:** **macro-F1** (unweighted mean of per-class F1, computed on valid
  predictions only). Conditional accuracy = correct ÷ valid is shown for transparency and is **not**
  used for ranking.
- **Invalid-output treatment:** 1,986 unparseable outputs are kept in the denominator, not dropped.
- **Safety intercepts:** **1,275** fire before any model call and are excluded from model attribution.
- **Infrastructure failures:** **zero** survive into the scored grid (verified).

## RQ1 — Model Comparison

### Key Numbers

| | Dreaddit | GoEmotions |
|---|---|---|
| Highest effective accuracy | **Llama 4 Scout** — 0.7296 / 0.7330 / **0.7502** (ZS / ZS-CoT / 1S-CoT) | **Gemma 4 31B** — **0.8196** / 0.8174 / 0.8132 |
| Strongest single point estimate | **0.7502** [0.7202, 0.7803] Llama 1S-CoT | **0.8196** [0.7907, 0.8489] Gemma ZS |
| Highest macro-F1 | 0.7519 Llama ZS | 0.5940 Mistral 1S-CoT (Gemma ZS 0.5932) |
| Model pairs Holm-significant, effective accuracy | **13 / 30** | **21 / 30** |
| Model pairs Holm-significant, macro-F1 | **20 / 30** | **0 / 30** |

### Key Observations

1. **No model leads both datasets.** Llama 4 Scout has the highest effective accuracy on every
   Dreaddit strategy; Gemma 4 31B has the highest on every GoEmotions strategy. These are point
   estimates plus significance counts — not a single "best model" verdict.
2. **Llama on Dreaddit** reaches 0.7502 effective accuracy under one-shot-CoT, its strongest
   configuration, and its 0.7519 macro-F1 under zero-shot is the highest macro-F1 anywhere in the
   study. Its advantage over the other models is Holm-significant in the two CoT strategies.
3. **Gemma on GoEmotions** reaches 0.8196 effective accuracy and, under zero-shot, is
   Holm-significantly better than **all four** other models on the secondary exact-McNemar test —
   the clearest model-level separation in the study.
4. **The 0 / 30 GoEmotions macro-F1 result is the important negative.** Not one model pair separates.
   This is a statement about the study's resolution, not about the models being equal: at these class
   supports the design cannot rank models on macro-F1, and saying so is part of the contribution.
5. **Class imbalance is why.** GoEmotions attributable supports are **487 / 81 / 33 / 15 / 6**, so six
   `anxiety` items carry roughly a fifth of macro-F1 and every confidence interval spans about
   0.45–0.67. Expect wide intervals and do not read small macro-F1 gaps as real.
6. **Two leaders are not cleanly separable from each other.** Llama versus Phi-4 separates in only
   1 of 6 Dreaddit comparisons, and on GoEmotions the two Holm-significant accuracy comparisons
   between them point in **opposite directions** depending on strategy.

## RQ2 — Performance Against Majority Baseline

### Key Numbers

| Dataset | Baseline | Significantly Above | Significantly Below | Not Distinguishable |
|---|---|---|---|---|
| Dreaddit | 0.5079 | **15 / 15** | 0 | 0 |
| GoEmotions | 0.7830 | **2 / 15** (Gemma ZS, ZS-CoT) | **5 / 15** | **8 / 15** |

Largest margin above baseline: **+0.2423** [0.1888, 0.2947] for Llama 1S-CoT on Dreaddit
(permutation p = 1.0 × 10⁻⁴, Holm p = 0.0015). Largest margin **below** baseline: **−0.1100**
[−0.1325, −0.0865] for Phi-4 1S-CoT on GoEmotions.

### Key Observations

1. **Dreaddit is the clean positive result.** All **15 of 15** configurations beat a majority-class
   predictor, every one Holm-significant, and the result holds under both the **primary permutation
   test and the secondary exact McNemar**, and under both baseline definitions. This is the strongest
   claim in the study and needs no hedging.
2. **GoEmotions does not replicate that picture.** Only 2 of 15 exceed the baseline; **5 of 15 are
   significantly worse** than answering `non_distress` to everything; 8 are indistinguishable from it.
3. **The imbalance explains the shape of the result.** 78.3% of GoEmotions items are `non_distress`,
   so accuracy near 0.78 *is* the constant-predictor level. Accuracy is close to uninformative on this
   benchmark, which is a measurement finding — not evidence that the models cannot classify distress.
4. **Primary versus secondary disagree for Gemma.** Gemma's two above-baseline results are
   significant on the **primary permutation test** (Holm p = 0.044 for both, margins +0.0367 and
   +0.0344) but **not confirmed by exact McNemar** (Holm p = 0.088 and 0.104). Report both, and state
   which test is primary — this is decision item 4 below.
5. **Where the system does show signal on GoEmotions, it shows in macro-F1**, 0.52–0.59 against a
   constant predictor's 0.176 — which is also the metric the study cannot use to rank models (RQ1
   observation 4). Say both halves of that sentence together.

## RQ3 — Prompting Strategy

> **Uses the current post-hoc strategy analysis** in `results/rq3_strategy_inference_2026-09-25/`,
> not the superseded statement in the 2026-09-25 20:44Z package that no strategy test exists. The
> supersession is recorded in `SUPERSEDED.md`.

### Key Numbers

| | Count |
|---|---|
| Metric-specific strategy comparisons | **60** |
| Holm-significant | **20** |
| Distinct strategy contrasts behind those rows | **14** |
| Significant on **both** co-primary metrics | 6 |
| Effective accuracy **only** | 7 |
| Macro-F1 **only** | 1 |

Framework: paired item-level permutation, **P = 10,000**; item-cluster bootstrap, **B = 4,000**, 95%
percentile CIs; Holm within dataset across 30 primary comparisons.

### Key Observations

1. **This analysis is post-hoc / exploratory.** Its freeze file labels it so: the estimation
   procedure was frozen 2026-09-21 and applied unchanged, but the contrasts were declared after the
   descriptive results were known. Present it as exploratory, never as preregistered confirmatory work.
2. **"20 significant" is not "20 comparisons."** 20 metric-specific rows correspond to **14 distinct
   contrasts**, because a contrast can appear once per metric. Use the 14 when counting findings.
3. **No universal strategy wins.** Direction is inconsistent across models and datasets — CoT helps
   some configurations and hurts others. There is no defensible "use chain-of-thought" conclusion.
4. **The two largest effects are format-compliance failures, not reasoning failures.** Verified
   example: **Qwen on Dreaddit**, zero-shot-CoT is **0.0887** below zero-shot on effective accuracy —
   but evaluability falls from **0.9980 to 0.9230** over the same comparison and conditional accuracy
   falls by only **0.0399**. Most of that gap is the model failing to serialise valid JSON, not
   failing to reason. The same caution applies to Phi-4 / GoEmotions / one-shot-CoT.
5. **So separate the two mechanisms whenever quoting a strategy effect:** did accuracy on parseable
   answers change, or did the share of parseable answers change? The metric policy makes the second
   visible instead of hiding it.

## Invalid Outputs and Reliability

### Key Numbers

| | Value |
|---|---|
| Attributable records | **99,075** |
| Model-invalid records | **1,986** |
| Invalid rate | **2.005%** |
| Safety intercepts (excluded from attribution) | **1,275** |
| Infrastructure failures in the scored grid | **0** |
| Strongest class-selective invalidity | Qwen / Dreaddit / ZS-CoT — **94.1%** of invalid items are stress-positive vs **50.8%** expected |
| Configurations with Holm-significant class-selective invalidity | **4 / 30** |
| Largest conditional-minus-effective gap | **0.1281** — Phi-4 / GoEmotions / 1S-CoT |

### Key Observations

1. **Effective accuracy is preferred because it is immune to selection by construction** — the
   denominator is the full attributable pool whether or not the model produced parseable output.
2. **Conditional accuracy can look artificially strong**, because it silently drops the items the
   model failed on. It is not comparable across configurations with different invalid rates.
3. **Phi-4 / GoEmotions / one-shot-CoT is the clearest illustration:** conditional accuracy 0.8011
   (second best on the dataset) versus effective accuracy 0.6730 (worst), a 0.1281 gap from 499
   unparseable outputs, 16.05% of that cell. Same model, same items — the metric choice flips it from
   near-leader to last.
4. **But that cell is not a selection-bias example.** The exploratory analysis found **no** detectable
   class enrichment there: its gap reflects invalid-output **volume**, not *which* items were lost.
   The earlier suspicion about it is **not supported**.
5. **Volume and selectivity are different problems.** Qwen / Dreaddit / ZS-CoT is the selectivity case
   (the wrong *kind* of item goes missing); Phi-4 / GoEmotions / 1S-CoT is the volume case. Keep them
   apart in discussion.
6. **Run-level stability matters too** — that Phi-4 cell's across-run SD is 0.1258 on effective
   accuracy and 0.1543 on evaluability, so it is unstable across runs rather than a settled property.

## Latency

### Key Numbers

| | Configuration | Mean client latency |
|---|---|---|
| Fastest | Mistral Small 4 — GoEmotions, 1S-CoT | **3.32 ± 0.16 s** |
| Slowest | Gemma 4 31B — Dreaddit, 1S-CoT | **15.14 ± 3.77 s** |

Available for all 30 configurations, as end-to-end client wall clock for one complete assessment.

### Key Observations

1. **Descriptive only. Nothing about latency was statistically tested.** Do not report a fastest model.
2. **Measurement resolution is 3 s** (poll cadence), so quote the **mean**, not the median — the
   medians sit on the 3 s lattice (Qwen's Dreaddit medians are 9.08 / 9.08 / 9.07 s).
3. **Model is confounded with serving provider and quantization** — Mistral→Mistral, Gemma→CoreWeave
   (fp4 directive), Llama and Phi-4→DeepInfra, Qwen→Alibaba. This measures deployments, not models.
4. **Concurrency confound:** all three Llama Dreaddit configurations (15 of 15 cells) ran under
   concurrent load on the same machine.
5. **Strategies ran in sequential blocks**, so block order is not separable from strategy.
6. Safe phrasing: "per-assessment latency ranged from about 3 to 15 seconds across configurations,
   but serving conditions were not controlled, so we treat this as deployment context rather than a
   model comparison."

## What I Can Say in the Meeting

> Since we last spoke I finished a full audit of the replication package and it now verifies
> end-to-end — 32 independent checks pass, both on my machine and on a clean clone from GitHub, so
> someone else can download it and re-derive every number we report. Along the way I found a real bug
> in the invalid-output reporting: a model-name mismatch in one join was silently zeroing two models,
> so the invalid-output table said 1,689 records when the correct total is 1,986. I fixed the join,
> regenerated only that table, and confirmed none of the accuracy, macro-F1 or latency numbers moved.
>
> On the results themselves: for stress detection on Dreaddit, all fifteen configurations beat the
> majority baseline, with the strongest at about 75% effective accuracy — that one's solid under both
> tests. GoEmotions is a harder story: the baseline is already 78% because the data is so imbalanced,
> only Gemma beats it, and five configurations actually do worse than a constant predictor. So I think
> the honest framing there is that accuracy is the wrong yardstick for that benchmark, and macro-F1 is
> the right one but our class supports are too small to rank models with it.
>
> I also ran an exploratory analysis of prompting strategy, since the frozen plan didn't test it.
> Twenty of sixty comparisons come out significant, but the two biggest effects are really formatting
> failures — the model stops producing valid JSON — rather than worse reasoning, so I don't want to
> over-claim there.
>
> What I need from you both is mainly framing: which accuracy number we call "AnxioSense accuracy"
> when there are thirty configurations, how we define RQ3 in the paper, and whether Gemma's
> above-baseline result counts as significant given the two tests disagree.

## Questions / Decisions for Alvine and Abel

### Scientific / paper decisions

- [ ] **1. How do we frame "AnxioSense accuracy"?** There are 30 configuration accuracies and no
      configuration was pre-designated as the system. Whatever goes in the abstract is a post-hoc
      choice and must be stated as one.
- [ ] **2. How is RQ3 defined in the paper?** The frozen plan's RQ3 is *efficiency / latency*; the
      question we actually want to answer is *prompting strategy*. A post-hoc analysis now tests the
      strategy reading, but it is labelled exploratory. If the paper needs **confirmatory** strategy
      claims, that is a new preregistered analysis, not a reanalysis.
- [ ] **3. GoEmotions macro-F1 power limitation.** 0 / 30 pairs separate. Agree the explicit
      limitations sentence: at these class supports the study is not powered to rank models on macro-F1.
- [ ] **4. Gemma's GoEmotions above-baseline result.** Significant on the primary permutation test
      (Holm p = 0.044) but not on exact McNemar (Holm p = 0.088, 0.104). Decide which test is primary
      and how to report the disagreement.
- [ ] **5. Evaluation scope statement.** We graded the `/api/workflow/evaluate` social-media path,
      scored from the referral agent (Dreaddit) and the emotion agent (GoEmotions). GAD-7, the final
      report agent and recommendation personalisation were **not** evaluated. Agree the wording.
- [ ] **6. Phi-4 / GoEmotions / one-shot-CoT run-level question — still open.**
      `ISSUES_FOR_AUDIT.md` item 1: 197 samples moved from `ok_empty_list` in run 4 to
      `fail_unparseable` in run 5, and conditional macro-F1 *rises* while effective accuracy falls.
      The pooled analysis does not settle it. Decide whether it needs a run-level appendix.
- [ ] **7. Limitation to acknowledge:** decoding parameters (temperature, max_tokens, seed, top-p/top-k)
      were **not explicitly set** — provider defaults applied throughout. Run-to-run variance therefore
      includes uncontrolled provider-side sampling.

### Repository housekeeping (not research issues)

- [ ] Publish to `main` or keep the work on the `repo-cleanup` branch for review first.
- [ ] One tracked file, `rq3_terminal_latency_records.jsonl`, is 55.75 MB — above GitHub's 50 MB
      recommendation. Decide whether to move it to Git LFS before archiving.
- [ ] The duplicated `evaluation/publication_experiments/results/` tree still holds the only copy of
      some `rq1_rq3_tables` inputs that canonical scripts read. Relocation is a separate, deferred task.
- [ ] **Resolved, no action needed:** both invalid-output-audit checksum discrepancies are closed and
      that package verifies 15/15. Do **not** re-run its `05_validate.py` — regenerating the manifest
      would erase the documented correction.

## One-Line Takeaways

- **RQ1:** Llama 4 Scout has the highest effective accuracy on Dreaddit and Gemma 4 31B on GoEmotions — no model leads both, and on GoEmotions macro-F1 no model pair separates at all.
- **RQ2:** All 15 Dreaddit configurations beat the majority baseline and the result survives both tests; on GoEmotions only 2 of 15 beat an already-high 78.3% baseline and 5 fall significantly below it.
- **RQ3:** Exploratory testing finds 14 distinct significant strategy contrasts with no universal winner, and the largest effects are format-compliance failures rather than reasoning gains.
