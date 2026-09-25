# RQ2 — Benchmark / dataset performance

Table: `tables/rq2_summary.csv` (30 rows). Every test column is copied from
`inferential_2026-09-21/tables/rq2_configuration_vs_baseline.csv`; nothing was recomputed.

## What was actually tested

Each of the 30 configurations is compared against a **paired constant majority-class predictor evaluated on
the same attributable items** — always class `1` on Dreaddit (355/699 = 0.5079) and always `non_distress` on
GoEmotions (487/622 = 0.7830). Primary metric: effective accuracy. Test: paired item-level permutation
(P = 10,000) with item-cluster bootstrap CIs (B = 4,000), Holm-corrected in a family of 15 per dataset. Exact
McNemar on ≥3/5 majority-vote correctness is a secondary family of 15 per dataset. A second baseline choice
(the frozen scalar 369/715 and 487/623) is carried as a CI-only sensitivity analysis.

**Macro-F1 was not tested against the baseline** — the plan records that a constant predictor's macro-F1 is
trivially low (0.337 Dreaddit, 0.176 GoEmotions), so that comparison is descriptive only.

## Why accuracy alone is misleading when the baseline is high

The two datasets sit at opposite ends of this problem.

- **Dreaddit** is near-balanced: the majority baseline is 0.5079. An accuracy of 0.73 is 0.22 above chance,
  and the gap is large relative to the CI width.
- **GoEmotions** is heavily imbalanced: 487 of 622 attributable items are `non_distress`, so **a model that
  answers `non_distress` to everything scores 0.7830**. Ten of the fifteen GoEmotions configurations have an
  effective accuracy between 0.67 and 0.79 — i.e. *at or below* what a constant answer achieves. An unqualified
  sentence such as "AnxioSense reaches 78% accuracy on GoEmotions" would describe a system indistinguishable
  from a constant predictor.

This is why macro-F1 belongs beside accuracy for GoEmotions: macro-F1 gives the four minority classes equal
weight, and every GoEmotions macro-F1 in this package sits between 0.52 and 0.60 against a constant
predictor's 0.176 — far above the constant predictor, while accuracy is not.

## RQ2 · Dreaddit (baseline 0.5079 on attributable items)

**15 of 15 configurations are above the baseline and all 15 are Holm-significant**, with exact McNemar
confirming all 15 (McNemar Holm p from 6.9 × 10⁻⁸ down to 2.1 × 10⁻¹⁷; the weakest is Qwen zero-shot-CoT at
6.6 × 10⁻³).

| Model | Strategy | Eff. acc | Δ vs baseline, 95% CI | Holm p | McNemar Holm p | Macro-F1 |
|---|---|---|---|---|---|---|
| Llama 4 Scout | 1S-CoT | 0.7502 | +0.242 [+0.189, +0.295] | 1.5e-03 | 2.1e-16 | 0.7510 |
| Llama 4 Scout | ZS-CoT | 0.7330 | +0.225 [+0.173, +0.278] | 1.5e-03 | 8.1e-16 | 0.7424 |
| Phi-4 | 1S-CoT | 0.7299 | +0.222 [+0.170, +0.275] | 1.5e-03 | 2.1e-13 | 0.7302 |
| Llama 4 Scout | ZS | 0.7296 | +0.222 [+0.171, +0.274] | 1.5e-03 | 6.3e-16 | 0.7519 |
| Phi-4 | ZS | 0.7222 | +0.214 [+0.165, +0.264] | 1.5e-03 | 5.5e-17 | 0.7439 |
| Phi-4 | ZS-CoT | 0.7001 | +0.192 [+0.135, +0.250] | 1.5e-03 | 4.3e-09 | 0.6964 |
| Gemma 4 31B | ZS | 0.6933 | +0.185 [+0.123, +0.249] | 1.5e-03 | 6.9e-08 | 0.6748 |
| Qwen3.5 27B | ZS | 0.6910 | +0.183 [+0.120, +0.244] | 1.5e-03 | 1.8e-07 | 0.6742 |
| Mistral Small 4 | ZS | 0.6861 | +0.178 [+0.116, +0.242] | 1.5e-03 | 3.4e-07 | 0.6657 |
| Gemma 4 31B | 1S-CoT | 0.6755 | +0.168 [+0.104, +0.232] | 1.5e-03 | 5.6e-06 | 0.6510 |
| Gemma 4 31B | ZS-CoT | 0.6747 | +0.167 [+0.104, +0.232] | 1.5e-03 | 5.0e-06 | 0.6503 |
| Mistral Small 4 | 1S-CoT | 0.6735 | +0.166 [+0.103, +0.230] | 1.5e-03 | 6.2e-06 | 0.6481 |
| Mistral Small 4 | ZS-CoT | 0.6609 | +0.153 [+0.088, +0.219] | 1.5e-03 | 2.0e-05 | 0.6312 |
| Qwen3.5 27B | 1S-CoT | 0.6475 | +0.140 [+0.074, +0.206] | 1.5e-03 | 1.2e-04 | 0.6105 |
| Qwen3.5 27B | ZS-CoT | 0.6023 | +0.094 [+0.025, +0.161] | 6.7e-03 | 6.6e-03 | 0.5983 |

**Supported claim:** on Dreaddit every model × strategy configuration performs above a majority-class
predictor, and the result survives Holm correction under both the primary permutation test and the
conservative McNemar check, under both baseline definitions (the sensitivity columns agree).

## RQ2 · GoEmotions (baseline 0.7830 on attributable items)

**2 of 15 above baseline (Holm-significant), 5 of 15 significantly below, 8 not distinguishable.**

| Model | Strategy | Eff. acc | Δ vs baseline, 95% CI | Holm p | Decision | McNemar Holm p | Macro-F1 |
|---|---|---|---|---|---|---|---|
| Gemma 4 31B | ZS | 0.8196 | +0.037 [+0.012, +0.062] | 4.4e-02 | **above** | 8.8e-02 | 0.5932 |
| Gemma 4 31B | ZS-CoT | 0.8174 | +0.035 [+0.010, +0.059] | 4.4e-02 | **above** | 1.0e-01 | 0.5832 |
| Gemma 4 31B | 1S-CoT | 0.8132 | +0.031 [+0.005, +0.056] | 1.7e-01 | not sig. | 3.2e-01 | 0.5852 |
| Mistral Small 4 | 1S-CoT | 0.7830 | +0.000 [−0.033, +0.033] | 1.00 | not sig. | 1.00 | 0.5940 |
| Qwen3.5 27B | ZS-CoT | 0.7897 | +0.007 [−0.024, +0.039] | 1.00 | not sig. | 1.00 | 0.5793 |
| Qwen3.5 27B | ZS | 0.7862 | +0.003 [−0.028, +0.034] | 1.00 | not sig. | 1.00 | 0.5723 |
| Qwen3.5 27B | 1S-CoT | 0.7701 | −0.013 [−0.048, +0.023] | 1.00 | not sig. | 1.00 | 0.5673 |
| Mistral Small 4 | ZS | 0.7656 | −0.018 [−0.054, +0.019] | 1.00 | not sig. | 1.00 | 0.5615 |
| Phi-4 | ZS-CoT | 0.7617 | −0.021 [−0.045, +0.003] | 5.6e-01 | not sig. | 1.00 | 0.5634 |
| Mistral Small 4 | ZS-CoT | 0.7412 | −0.042 [−0.080, −0.005] | 2.2e-01 | not sig. | 3.4e-01 | 0.5357 |
| Phi-4 | ZS | 0.7363 | −0.047 [−0.070, −0.022] | 4.8e-03 | **below** | 1.00 | 0.5342 |
| Llama 4 Scout | 1S-CoT | 0.7318 | −0.052 [−0.087, −0.017] | 4.4e-02 | **below** | 1.9e-01 | 0.5443 |
| Llama 4 Scout | ZS | 0.7003 | −0.082 [−0.120, −0.044] | 1.5e-03 | **below** | 1.7e-03 | 0.5202 |
| Llama 4 Scout | ZS-CoT | 0.6826 | −0.100 [−0.139, −0.062] | 1.5e-03 | **below** | 9.6e-05 | 0.5296 |
| Phi-4 | 1S-CoT | 0.6730 | −0.110 [−0.133, −0.087] | 1.5e-03 | **below** | 1.00 | 0.5406 |

**Two cautions on the two "above baseline" results.** Both belong to Gemma, both have Holm p = 0.044 — just
inside the threshold — and **neither is confirmed by the conservative McNemar check** (p = 0.088 and 0.104).
The honest wording is "Gemma 4 31B is the only model that exceeds the majority baseline on GoEmotions, by
about 3.5 accuracy points, and the margin is small enough that the secondary test does not confirm it."

**A caution in the other direction.** Three of the five "below baseline" results (Phi-4 ZS, Phi-4 1S-CoT,
Llama 1S-CoT) are Holm-significant under the primary permutation test but **not** under McNemar. Only Llama ZS
and Llama ZS-CoT are confirmed by both.

## What RQ2 can and cannot claim

**Can claim.**
- Dreaddit: all 15 configurations beat a majority-class predictor, confirmed by two tests and robust to the
  baseline definition.
- GoEmotions: only Gemma 4 31B exceeds the majority baseline, and only under zero-shot and zero-shot-CoT, by a
  margin the secondary test does not confirm; five configurations are significantly *worse* than answering
  `non_distress` to everything.
- On macro-F1 every configuration is far above a constant predictor on both datasets (descriptively — this
  comparison was not tested).

**Cannot claim.**
- A single "AnxioSense accuracy". There are 30 configuration-level accuracies and no configuration was
  pre-designated as the system.
- That GoEmotions accuracy near 0.78 represents useful performance — that is the constant-predictor level.
- Superiority over the baseline for any of the 8 not-significant GoEmotions configurations, in either
  direction.
