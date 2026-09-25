# RQ1 — Model performance comparison

Tables: `tables/rq1_dreaddit.csv`, `tables/rq1_goemotions.csv` (15 rows each).
All values five-run mean ± sample SD; CIs are the frozen item-cluster bootstrap CIs (B = 4,000) on the
five-run pooled estimate.

## Which accuracy belongs in the main table

**Effective accuracy.** The frozen statistical plan designates effective accuracy and macro-F1 as the two
primary RQ1 metrics, makes effective accuracy the primary RQ2 metric, and states that conditional accuracy
gets "CIs only (configuration level and RQ1 pair differences). No p-values and no Holm."

| | `accuracy_conditional` | `accuracy_effective` |
|---|---|---|
| Denominator | valid predictions only | all attributable records |
| An invalid output… | is removed from numerator **and** denominator — it does not count as wrong | stays in the denominator — it counts against the configuration |
| Denominators comparable across models? | **No** — each configuration is scored on its own surviving items | **Yes** — every configuration is scored on the same 699 / 622 items |
| Statistically tested in the frozen package? | No (CIs only) | Yes (permutation + Holm + McNemar) |

The two diverge exactly in proportion to the invalid rate: `acc_eff = acc_cond × evaluability`. The gap is
therefore arithmetic, not empirical — see `INVALID_OUTPUT_SELECTION_EFFECT.md`. Report effective accuracy as
the headline and conditional accuracy beside it so a reader can see how much of a configuration's score
depends on items it failed to answer.

---

## RQ1 · Dreaddit (binary stress; majority baseline 0.5161 frozen scalar / 0.5079 on attributable items)

| Model | Strategy | Eff. acc ± SD | 95% CI | Macro-F1 ± SD | 95% CI | Cond. acc | Evaluability | Latency (s) |
|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | ZS | 0.6933 ± 0.0040 | [0.659, 0.727] | 0.6748 ± 0.0049 | [0.640, 0.709] | 0.6933 | 1.0000 | 15.07 ± 2.73 |
| Gemma 4 31B | ZS-CoT | 0.6747 ± 0.0008 | [0.641, 0.709] | 0.6503 ± 0.0009 | [0.616, 0.685] | 0.6747 | 1.0000 | 13.10 ± 1.97 |
| Gemma 4 31B | 1S-CoT | 0.6755 ± 0.0064 | [0.642, 0.709] | 0.6510 ± 0.0080 | [0.617, 0.686] | 0.6755 | 1.0000 | 15.14 ± 3.77 |
| **Llama 4 Scout** | ZS | 0.7296 ± 0.0027 | [0.700, 0.759] | **0.7519 ± 0.0050** | [0.721, 0.782] | 0.7525 | 0.9697 | 12.46 ± 0.88 |
| **Llama 4 Scout** | ZS-CoT | 0.7330 ± 0.0049 | [0.703, 0.763] | 0.7424 ± 0.0048 | [0.712, 0.773] | 0.7441 | 0.9851 | 14.08 ± 2.11 |
| **Llama 4 Scout** | 1S-CoT | **0.7502 ± 0.0049** | [0.720, 0.780] | 0.7510 ± 0.0045 | [0.721, 0.781] | 0.7519 | 0.9977 | 10.23 ± 0.64 |
| Mistral Small 4 | ZS | 0.6861 ± 0.0036 | [0.652, 0.719] | 0.6657 ± 0.0041 | [0.631, 0.700] | 0.6863 | 0.9997 | 5.36 ± 0.03 |
| Mistral Small 4 | ZS-CoT | 0.6609 ± 0.0042 | [0.627, 0.695] | 0.6312 ± 0.0042 | [0.595, 0.666] | 0.6611 | 0.9997 | 5.25 ± 0.11 |
| Mistral Small 4 | 1S-CoT | 0.6735 ± 0.0053 | [0.640, 0.706] | 0.6481 ± 0.0061 | [0.613, 0.682] | 0.6735 | 1.0000 | 4.89 ± 0.12 |
| Phi-4 | ZS | 0.7222 ± 0.0164 | [0.695, 0.750] | 0.7439 ± 0.0126 | [0.716, 0.771] | 0.7447 | 0.9697 | 12.91 ± 1.36 |
| Phi-4 | ZS-CoT | 0.7001 ± 0.0022 | [0.671, 0.730] | 0.6964 ± 0.0038 | [0.667, 0.726] | 0.7060 | 0.9917 | 12.86 ± 1.19 |
| Phi-4 | 1S-CoT | 0.7299 ± 0.0101 | [0.702, 0.758] | 0.7302 ± 0.0101 | [0.702, 0.758] | 0.7333 | 0.9954 | 10.13 ± 1.84 |
| Qwen3.5 27B | ZS | 0.6910 ± 0.0014 | [0.657, 0.724] | 0.6742 ± 0.0012 | [0.638, 0.708] | 0.6924 | 0.9980 | 9.05 ± 0.27 |
| Qwen3.5 27B | ZS-CoT | 0.6023 ± 0.0049 | [0.566, 0.638] | 0.5983 ± 0.0061 | [0.559, 0.636] | 0.6525 | **0.9230** | 8.67 ± 0.24 |
| Qwen3.5 27B | 1S-CoT | 0.6475 ± 0.0016 | [0.613, 0.681] | 0.6105 ± 0.0020 | [0.573, 0.647] | 0.6482 | 0.9989 | 8.40 ± 0.45 |

**Descriptive observation.** Llama 4 Scout has the highest effective accuracy in all three strategies and the
highest single macro-F1 (zero-shot, 0.7519). Qwen zero-shot-CoT is lowest on both, and is the only Dreaddit
configuration with evaluability below 0.95.

**Statistically supported (frozen tests).** Of the 30 model pairs per metric (one Holm family of 60 per
dataset), **13/30 separate on effective accuracy and 20/30 on macro-F1**. Counting Holm-significant wins and
losses per configuration (derived from `rq1_model_pairs_primary.csv`):

| Configuration | Holm-sig wins / losses, eff. acc | Holm-sig wins / losses, macro-F1 |
|---|---|---|
| Llama 4 Scout ZS-CoT | 3 / 0 | 4 / 0 |
| Llama 4 Scout 1S-CoT | 3 / 0 | 3 / 0 |
| Phi-4 1S-CoT | 3 / 0 | 3 / 0 |
| Llama 4 Scout ZS | 0 / 0 | 3 / 0 |
| Phi-4 ZS | 0 / 0 | 3 / 0 |
| Phi-4 ZS-CoT | 2 / 0 | 3 / 1 |
| Qwen3.5 27B ZS-CoT | 0 / 4 | 0 / 3 |
| Gemma 4 31B 1S-CoT | 0 / 2 | 0 / 2 |

So the defensible Dreaddit statement is: **Llama 4 Scout and Phi-4 form an upper group that is separated from
Gemma, Mistral and Qwen in several within-strategy comparisons, while Llama versus Phi-4 separates in only
1 of their 6 Dreaddit comparisons.** That one is zero-shot-CoT macro-F1 (Llama − Phi-4 = +0.0460,
CI [+0.0226, +0.0692], Holm p = 0.012); effective accuracy never separates them on Dreaddit (Holm p = 1.000,
0.146 and 0.954), and exact McNemar separates them in none of the three strategies. The exact-McNemar secondary family (30 hypotheses per dataset) gives 15 Holm-significant pairs
on Dreaddit and disagrees with the primary test on 4 of 30 pairs; those 4 are listed in
`inferential_2026-09-21/summary_counts.json` under `rq1_acc_primary_vs_mcnemar_disagree`.

---

## RQ1 · GoEmotions (5-class; majority baseline 0.7817 frozen scalar / 0.7830 on attributable items)

| Model | Strategy | Eff. acc ± SD | 95% CI | Macro-F1 ± SD | 95% CI | Cond. acc | Evaluability | Latency (s) |
|---|---|---|---|---|---|---|---|---|
| **Gemma 4 31B** | ZS | **0.8196 ± 0.0038** | [0.791, 0.849] | 0.5932 ± 0.0071 | [0.482, 0.671] | 0.8196 | 1.0000 | 11.54 ± 1.38 |
| **Gemma 4 31B** | ZS-CoT | 0.8174 ± 0.0037 | [0.787, 0.847] | 0.5832 ± 0.0082 | [0.472, 0.661] | 0.8174 | 1.0000 | 14.17 ± 3.54 |
| **Gemma 4 31B** | 1S-CoT | 0.8132 ± 0.0029 | [0.783, 0.842] | 0.5852 ± 0.0055 | [0.478, 0.664] | 0.8150 | 0.9977 | 10.09 ± 2.75 |
| Llama 4 Scout | ZS | 0.7003 ± 0.0084 | [0.667, 0.734] | 0.5202 ± 0.0175 | [0.453, 0.580] | 0.7267 | 0.9637 | 10.78 ± 1.26 |
| Llama 4 Scout | ZS-CoT | 0.6826 ± 0.0092 | [0.648, 0.716] | 0.5296 ± 0.0134 | [0.459, 0.591] | 0.7278 | 0.9379 | 11.02 ± 2.20 |
| Llama 4 Scout | 1S-CoT | 0.7318 ± 0.0092 | [0.698, 0.766] | 0.5443 ± 0.0126 | [0.466, 0.612] | 0.7671 | 0.9540 | 10.00 ± 1.34 |
| Mistral Small 4 | ZS | 0.7656 ± 0.0053 | [0.732, 0.798] | 0.5615 ± 0.0106 | [0.471, 0.636] | 0.7698 | 0.9945 | 3.98 ± 0.48 |
| Mistral Small 4 | ZS-CoT | 0.7412 ± 0.0078 | [0.706, 0.774] | 0.5357 ± 0.0104 | [0.448, 0.609] | 0.7457 | 0.9939 | 3.43 ± 0.11 |
| Mistral Small 4 | 1S-CoT | 0.7830 ± 0.0047 | [0.752, 0.813] | **0.5940 ± 0.0079** | [0.487, 0.668] | 0.7860 | 0.9961 | 3.32 ± 0.16 |
| Phi-4 | ZS | 0.7363 ± 0.0164 | [0.706, 0.766] | 0.5342 ± 0.0161 | [0.447, 0.602] | 0.7845 | 0.9386 | 13.07 ± 0.35 |
| Phi-4 | ZS-CoT | 0.7617 ± 0.0090 | [0.731, 0.792] | 0.5634 ± 0.0105 | [0.467, 0.633] | 0.8094 | 0.9412 | 13.09 ± 1.89 |
| Phi-4 | 1S-CoT | 0.6730 ± **0.1258** | [0.646, 0.700] | 0.5406 ± 0.0494 | [0.442, 0.611] | 0.8011 | **0.8395** | 10.63 ± 2.23 |
| Qwen3.5 27B | ZS | 0.7862 ± 0.0011 | [0.753, 0.818] | 0.5723 ± 0.0071 | [0.462, 0.649] | 0.7862 | 1.0000 | 7.27 ± 0.56 |
| Qwen3.5 27B | ZS-CoT | 0.7897 ± 0.0021 | [0.758, 0.821] | 0.5793 ± 0.0060 | [0.468, 0.657] | 0.7897 | 1.0000 | 7.32 ± 0.37 |
| Qwen3.5 27B | 1S-CoT | 0.7701 ± **0.0000** | [0.738, 0.804] | 0.5673 ± **0.0000** | [0.460, 0.644] | 0.7726 | 0.9968 | 7.32 ± 0.33 |

**Descriptive observation.** Gemma 4 31B has the highest effective accuracy in all three strategies, but the
highest single macro-F1 belongs to Mistral 1S-CoT (0.5940) — 0.0008 above Gemma ZS (0.5932). Two variability
extremes are worth flagging: Phi-4 1S-CoT has an effective-accuracy SD of 0.1258 across five runs (the run-5
collapse documented in `descriptive_2026-09-21/ISSUES_FOR_AUDIT.md` item 1), and Qwen 1S-CoT has an SD of
exactly 0.0000 — identical metrics in all five runs (near-determinism, ISSUES item 6; each run was verified as
a genuinely separate set of calls).

**Statistically supported (frozen tests).** **21/30 model pairs separate on effective accuracy. 0/30 separate
on macro-F1.**

This is the single most important RQ1 caveat. On GoEmotions, no model pair is distinguishable on macro-F1
after Holm correction: only 3 of 30 pairs reach raw p < 0.05, and only 2 have a CI excluding zero. The cause
is visible in the CI widths above — every macro-F1 CI spans roughly 0.45–0.67, because macro-F1 is an
unweighted mean over five classes and the class supports are 487 / 81 / 34 / 15 / **6** per run. Six `anxiety`
items drive one fifth of the metric.

| Configuration | Holm-sig wins / losses, eff. acc | Holm-sig wins / losses, macro-F1 |
|---|---|---|
| Gemma 4 31B ZS | 4 / 0 | 0 / 0 |
| Gemma 4 31B ZS-CoT | 3 / 0 | 0 / 0 |
| Gemma 4 31B 1S-CoT | 3 / 0 | 0 / 0 |
| Qwen3.5 27B ZS-CoT | 2 / 0 | 0 / 0 |
| Mistral Small 4 1S-CoT | 2 / 0 | 0 / 0 |
| Llama 4 Scout ZS-CoT | 0 / 4 | 0 / 0 |
| Phi-4 1S-CoT | 0 / 4 | 0 / 0 |

The exact-McNemar family gives 18 Holm-significant pairs on GoEmotions and disagrees with the primary test on
5 of 30 pairs.

A concrete illustration of why a single ranking is unsafe: Llama 4 Scout versus Phi-4 on GoEmotions separates
on effective accuracy in two strategies **with opposite signs** — Phi-4 higher under zero-shot-CoT
(Llama − Phi-4 = −0.0791, CI [−0.1077, −0.0498], Holm p = 0.006) and Llama higher under one-shot-CoT
(+0.0588, CI [+0.0328, +0.0852], Holm p = 0.006). On macro-F1 neither separates (Holm p = 1.000 in all three
strategies).

---

## What RQ1 can and cannot claim

**Can claim.**
- Per dataset and per strategy, which model pairs differ on effective accuracy and on macro-F1, with effect
  sizes (`diff_A_minus_B`), bootstrap CIs on the difference, permutation p-values and Holm decisions.
- That Llama 4 Scout leads every Dreaddit strategy and Gemma 4 31B leads every GoEmotions strategy on
  effective accuracy.
- That the leader does not transfer: no model leads both datasets.

**Cannot claim.**
- A single "best model". The leader changes with the dataset, and on GoEmotions macro-F1 separates no pair at
  all.
- That Llama 4 Scout is better than Phi-4 on Dreaddit *on accuracy* — none of the three effective-accuracy
  comparisons is Holm-significant, and McNemar separates them in none.
- That either of Llama 4 Scout or Phi-4 is better on GoEmotions — the two Holm-significant effective-accuracy
  comparisons point in opposite directions depending on the strategy.
- Any model ranking on GoEmotions macro-F1.
- Anything about *why* a model fails in a particular way; see the invalid-output audit, which separates
  observation from mechanism.
