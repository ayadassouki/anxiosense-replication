# Inferential analysis: RQ1 and RQ2 (frozen AnxioSense publication grid)

Date: 2026-09-21. This is analysis material, not manuscript prose. The design is in `STATISTICAL_ANALYSIS_PLAN.md`: it was written and approved (options D1–D4) before any test was run. Nothing frozen was modified:

- raw runs, manifests and `descriptive_2026-09-21`;
- the parser and MetricPolicy 1.0.0;
- `rq1_rq3_reporting_2026-09-21`;
- the verification artifacts.

There were no API calls and no reruns. Every invalid output is kept as frozen, and so is Phi-4 GoEmotions one-shot-CoT run 5. The Gemma Dreaddit replacement is used exactly as frozen: pub_011 for 14 cells, pub_013 for `one-shot-cot|run5`. This is asserted per cell, and the analysis aborts otherwise.

**Measured** = computed from the frozen records. **Interpretation** = a reading of those numbers.

## 0. How to read the tables

- **Items.** Dreaddit n = 699, GoEmotions n = 622 attributable items per configuration. These are the items that were not safety-intercepted; the same set is used in every cell.
- **Values.** Five-run means as frozen (e.g. Dreaddit Llama 4 Scout one-shot-CoT effective accuracy 0.750). Δ = A − B.
- **95% CI.** Item-cluster bootstrap: 4,000 replicates, resampling items with all 15 configurations × 5 runs attached. Percentile intervals. CIs are **per comparison, not multiplicity-adjusted**.
- **p (perm.).** Paired item-level permutation test, 10,000 swap sets. The smallest attainable value is 1/10001, shown as "<0.0001".
- **Holm p.** Holm-adjusted within the pre-declared family:
  - RQ1 primary: 60 per dataset;
  - RQ1 McNemar: 30;
  - RQ2 primary: 15;
  - RQ2 McNemar: 15.
- **"Holm sig."** Holm p ≤ 0.05.
- **McNemar b / c.** Items where A is majority-correct (correct in ≥ 3 of 5 runs) and B is not / the reverse. Exact two-sided test. This is a secondary, conservative check.
- **Effective accuracy.** Invalid output = wrong. **Macro-F1.** Frozen definition, per-class metrics on valid predictions.
- **Conditional accuracy.** CIs only, no tests, because the denominators differ between configurations (plan §B7).
- **Rounding.** 3 decimals for values, effects and CIs; 4 decimals for p; ROUND_HALF_UP of the stored value.
  - One CI bound lies at a 3-decimal half boundary: the GoEmotions Phi-4 zero-shot RQ2 upper bound, stored as −0.02249999999999986 and shown as −0.022.
  - The independent verification found last-bit float differences (≤ 1.1e-16) in CI bounds, so this displayed digit could equally be −0.023. No decision depends on it: the whole interval is below 0.

## 1. Verification status

The independent verification (`verification/verify_inferential.py`, stdlib only, no shared code) **PASSED with 0 discrepancies**:

- 90,512 exact checks;
- 153,530 floating-point checks: 104,818 bit-identical and 48,712 differing only in the last bits (max 4.4e-16);
- all 4,000 × 15 effective-accuracy bootstrap replicates per dataset recomputed;
- 200 × 15 macro-F1 and conditional-accuracy replicates per dataset recomputed;
- every 10th permutation statistic recomputed for accuracy, and every 50th for macro-F1;
- every permutation p, McNemar count and p, Holm value and CI bound re-derived;
- the seeds and draw digests match.

Details are in `verification/VERIFICATION.md`. Observed five-run values equal the frozen `aggregate_results.csv` within 2.2e-16. All input hashes match the frozen values (`source_hashes.txt`).

---

## RQ1: Which LLM yields the best results?

### RQ1 · Dreaddit, effective accuracy (primary; with McNemar check)

{{TABLE:rq1_dreaddit_acc_eff}}

### RQ1 · Dreaddit, macro-F1 (primary)

{{TABLE:rq1_dreaddit_macro_f1}}

### RQ1 · GoEmotions, effective accuracy (primary; with McNemar check)

{{TABLE:rq1_goemotions_acc_eff}}

### RQ1 · GoEmotions, macro-F1 (primary)

{{TABLE:rq1_goemotions_macro_f1}}

Conditional-accuracy differences (CIs only) are in `tables/rq1_dreaddit_conditional.md` and `tables/rq1_goemotions_conditional.md`.

### RQ1 · Measured

**Dreaddit** (family of 60): 33 comparisons are Holm-significant, 13 of 30 on effective accuracy and 20 of 30 on macro-F1.

- **Llama 4 Scout and Phi-4 vs Gemma 4 31B, Mistral Small 4 and Qwen3.5 27B** (18 pairs over 3 strategies):
  - All 18 observed differences favour Llama or Phi-4.
  - **18 of 18 are Holm-significant on macro-F1.** Examples: one-shot-CoT Llama − Mistral +0.103 [+0.071, +0.135]; Llama − Qwen +0.141 [+0.104, +0.178].
  - **11 of 18 are Holm-significant on effective accuracy.**
- **Under zero-shot**, none of those 6 pairs is Holm-significant on effective accuracy (Δ between +0.029 and +0.043), although all 6 are on macro-F1 (Δ +0.069 to +0.086).
  - At zero-shot, Llama and Phi-4 have 106 invalid outputs each over five runs, which count as wrong in effective accuracy.
  - The McNemar majority-vote check is significant for 3 of those 6 pairs (Gemma vs Phi-4, Mistral vs Phi-4, Phi-4 vs Qwen).
- **Llama 4 Scout vs Phi-4** is Holm-significant only on zero-shot-CoT macro-F1: +0.046 [+0.023, +0.069], Holm p 0.0120. It is not significant on:
  - zero-shot (acc. +0.007, F1 +0.008);
  - one-shot-CoT (acc. +0.020, F1 +0.021);
  - zero-shot-CoT effective accuracy (+0.033, Holm p 0.1456).
- **Among Gemma, Mistral and Qwen:**
  - Gemma vs Mistral is not significant under any strategy or metric.
  - Qwen is lower than Gemma and Mistral under zero-shot-CoT: Gemma − Qwen acc. +0.072, F1 +0.052; Mistral − Qwen acc. +0.059.
- **Primary and McNemar disagree on 4 of 30 accuracy pairs** (listed in `summary_counts.json`).

**GoEmotions** (family of 60): 21 of 30 effective-accuracy comparisons are Holm-significant; **0 of 30 macro-F1 comparisons are.**

- **Effective accuracy, Gemma 4 31B:**
  - Higher than Llama 4 Scout and Phi-4 under all three strategies (Δ +0.056 to +0.140).
  - Higher than Mistral under zero-shot (+0.054) and zero-shot-CoT (+0.076), but not one-shot-CoT (+0.030, Holm p 0.3002).
  - Higher than Qwen under zero-shot (+0.033, Holm p 0.0240) and one-shot-CoT (+0.043), but not zero-shot-CoT (+0.028).
- **Effective accuracy, Llama and Phi-4 vs Gemma/Mistral/Qwen:** 17 of 18 observed differences favour Gemma, Mistral or Qwen, and 14 of 18 are Holm-significant.
- **Macro-F1:**
  - No difference survives Holm. Only 3 of 30 have raw p < 0.05.
  - Observed |Δ| ranges from 0.004 to 0.073.
  - The CIs are wide (width 0.075–0.164) because of the rare classes.
- **Phi-4 one-shot-CoT** (which includes the frozen run-5 collapse) is significantly below Gemma, Llama, Mistral and Qwen on effective accuracy under the primary test. McNemar does **not** confirm it against Llama, Mistral or Qwen, because the majority vote over 5 runs absorbs a failure confined mostly to one run.
- **Primary and McNemar disagree on 5 of 30 accuracy pairs.**

**Monte Carlo sensitivity.** P = 10,000 permutations gives each p-value some simulation error. For these Holm-significant decisions, the 99% Monte Carlo range of Holm p crosses 0.05:

- Dreaddit zero-shot-CoT Mistral vs Phi-4, effective accuracy: Holm p 0.0420, range 0.019–0.0712;
- GoEmotions zero-shot Gemma vs Qwen, effective accuracy: Holm p 0.0240, range 0.006–0.0524.

Dreaddit one-shot-CoT Gemma vs Qwen macro-F1 (Holm p 0.0729) could cross in the other direction. These three are fragile. See `summary_counts.json` → `monte_carlo_sensitivity`.

### RQ1 · Interpretation

- **Dreaddit.** The data support a two-tier structure: Llama 4 Scout and Phi-4 above Gemma 4 31B, Mistral Small 4 and Qwen3.5 27B.
  - On macro-F1 this holds for every such pair under every strategy.
  - On effective accuracy it holds under zero-shot-CoT (except Gemma vs Phi-4) and one-shot-CoT, but not under zero-shot, where the two leaders' invalid outputs shrink the gap below what the test can separate.
  - The data do **not** support a single best model: Llama and Phi-4 are distinguishable in 1 of 6 strategy × metric comparisons.
- **GoEmotions.** Effective accuracy favours Gemma over most alternatives. Macro-F1, which is the class-balanced measure relevant to distress-class detection, separates **no** pair of models. Because 78% of attributable items are non_distress, the accuracy differences largely reflect agreement on that majority class.
- **Across datasets,** the model groupings reverse. "Which LLM is best" has a dataset- and metric-specific answer, not a single one.

---

## RQ2: What is the accuracy of AnxioSense?

As in the descriptive report, **no single overall AnxioSense accuracy is defined, and none is computed.** Inference is per configuration, against the majority baseline.

- **Primary baseline:** the constant majority-class predictor, scored on the same attributable items and resampled together with the configuration (355/699 = 0.508 Dreaddit; 487/622 = 0.783 GoEmotions).
- **Sensitivity (last column):** the fixed frozen scalar (0.516 and 0.782), CI only.

### RQ2 · Dreaddit

{{TABLE:rq2_dreaddit}}

### RQ2 · GoEmotions

{{TABLE:rq2_goemotions}}

Configuration-level 95% CIs for effective accuracy, conditional accuracy and macro-F1: `tables/cfg_dreaddit.md`, `tables/cfg_goemotions.md`.

### RQ2 · Measured

**Dreaddit.**
- All 15 configurations are above the paired baseline and Holm-significant, under both the permutation test and McNemar.
- The effects range from +0.094 [+0.025, +0.161] (Qwen zero-shot-CoT) to +0.242 [+0.189, +0.295] (Llama one-shot-CoT).
- The sensitivity CIs against the frozen 0.516 all exclude 0 as well.
- The paired CIs are wider than the sensitivity CIs (e.g. ±0.06 vs ±0.03). The baseline's own item-sampling variability is included, and those models' correctness is negatively related to the majority-class indicator: they are more accurate on class-0 items.

**GoEmotions.**
- **Holm-significantly above baseline: 2 of 15.** Gemma zero-shot, +0.037 [+0.012, +0.062], and zero-shot-CoT, +0.034 [+0.010, +0.059], both at Holm p 0.0440.
  - Both are Monte Carlo-fragile: the 99% range of Holm p is 0.0313–0.0537.
  - McNemar does not confirm them (Holm p 0.0876 and 0.1037).
- **Holm-significantly below baseline: 5 of 15.**
  - Llama zero-shot −0.083;
  - Llama zero-shot-CoT −0.100;
  - Llama one-shot-CoT −0.051 (Holm p 0.0440, Monte Carlo-fragile);
  - Phi-4 zero-shot −0.047;
  - Phi-4 one-shot-CoT −0.110.
- **Not distinguishable from baseline: 8 of 15.** This includes Gemma one-shot-CoT, all three Mistral configurations, all three Qwen configurations and Phi-4 zero-shot-CoT.
- The fixed-scalar sensitivity CIs exclude 0 for 3 configurations above and 6 below.
- **Macro-F1 vs the constant predictor** (descriptive; not tested because the constant's value is trivially low):
  - Constant predictor: 0.337 on Dreaddit and 0.176 on GoEmotions.
  - Every configuration is far higher. Lowest configuration CI lower bounds: 0.559 (Dreaddit Qwen zero-shot-CoT) and 0.442 (GoEmotions Phi-4 one-shot-CoT).
  - GoEmotions macro-F1 CIs are wide, e.g. Gemma zero-shot 0.593 [0.482, 0.671].

### RQ2 · Interpretation

- **Dreaddit** (binary stress vs non-stress, via the Referral agent): every configuration's effective accuracy is above the majority baseline, with effects of roughly +0.09 to +0.24 and CIs excluding 0.
- **GoEmotions** (Emotion agent, 5 classes, 78% majority class): no configuration is robustly above baseline on effective accuracy. At most two Gemma configurations are, marginally and Monte Carlo-fragile. Five are below. Accuracy therefore gives no evidence that the emotion pipeline beats "always non_distress".
  - Macro-F1 shows the configurations do discriminate among classes far better than the constant predictor.
  - These two statements are compatible: they measure different things under heavy class imbalance.
- **"AnxioSense accuracy"** is configuration- and dataset-specific:
  - Dreaddit effective accuracy 0.602–0.750;
  - GoEmotions effective accuracy 0.673–0.820, with only a minority of configurations distinguishable from its baseline.

---

## RQ3

Not analysed inferentially, as planned. The confounds in `rq1_rq3_reporting_2026-09-21/REPORT.md` (3 s quantisation, fixed strategy order, machine, provider and time, concurrent load for Llama Dreaddit, no per-agent timing) mean no test could attribute a latency difference to the prompting strategy. RQ3 remains descriptive.

---

## What the inferential results establish and do not establish

**Descriptive vs statistically supported.**
- Differences in the descriptive tables are observations.
- Only rows marked "Holm sig." in the pre-declared families are statistically supported differences.
- Everything else, including every GoEmotions macro-F1 model difference, is **not** shown to differ.
- A non-significant result is not evidence of equality. Some CIs are wide enough to include practically meaningful differences, e.g. GoEmotions macro-F1 CIs up to 0.164 wide.

**Practical effect sizes.**
- Supported Dreaddit model differences are 0.046–0.144 in macro-F1.
- Supported GoEmotions accuracy differences are 0.033–0.140.
- Dreaddit gains over baseline are 0.094–0.242.
- Whether these magnitudes matter for screening is a substantive judgement these statistics do not make.

**Fragile results.** Five Holm-significant decisions have 99% Monte Carlo ranges that cross 0.05:
- 2 in RQ1: Dreaddit zero-shot-CoT Mistral vs Phi-4, and GoEmotions zero-shot Gemma vs Qwen, both effective accuracy;
- 3 in RQ2: GoEmotions Gemma zero-shot and zero-shot-CoT, and Llama one-shot-CoT.

One non-significant decision could also cross: Dreaddit one-shot-CoT Gemma vs Qwen macro-F1. Several significant results are also not confirmed by McNemar. None of these should carry a conclusion on its own.

**Repeated runs.**
- Inference is over items. The 5 runs are averaged within items and never counted as independent observations.
- Intervals are conditional on the 5 observed runs. They do not capture run-to-run variability beyond those runs, and the runs were not resampled.
- The McNemar check uses majority vote, which discards within-item run disagreement. That is why it disagrees with the primary test for Phi-4 one-shot-CoT on GoEmotions.

**Invalid outputs.**
- Effective accuracy and macro-F1 keep invalid outputs as frozen: counted wrong in accuracy, and contributing nothing to tp/fp/fn in macro-F1.
- The two metrics weight invalid outputs differently, which explains part of their disagreement (e.g. Dreaddit zero-shot).
- Conditional accuracy has only CIs, on changing denominators.

**Class imbalance.**
- GoEmotions accuracy is dominated by non_distress (487/622).
- The anxiety class has 6 items. 14 of 4,000 bootstrap replicates contained no anxiety item, and its F1 was set to 0 as the frozen policy requires.
- No per-class inference was performed, and none should be drawn for anxiety.

**Dataset and task limits.**
- Dreaddit is stress vs non-stress, scored from the Referral agent's risk level. It does not validate anxiety detection or the GoEmotions `anxiety` class.
- Both datasets are Reddit text.
- Results are conditional on the frozen parser, MetricPolicy 1.0.0 and the serving routes used (e.g. Gemma via CoreWeave fp4).

**Clinical limits.** Nothing here is clinical validation. There is no clinical population, no clinician reference standard, and no deployment outcome.

**Protocol differences.**
- The July setup document's Wilcoxon + Bonferroni plan was not used, because it cannot reach p < 0.05 with 5 runs and ignores item sampling (plan §B12).
- Cohen's weighted κ and symptom-extraction metrics named there are not part of the frozen scoring and were not analysed.

**RQ3.** Latency remains descriptive and confounded. No inferential claim about prompting-strategy efficiency is made.
