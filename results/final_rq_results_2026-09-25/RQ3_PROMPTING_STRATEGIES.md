# RQ3 — Prompting strategy comparison

Tables: `tables/rq3_accuracy.csv`, `tables/rq3_macro_f1.csv` (30 rows each),
`tables/rq3_inferential.csv` (18 rows).

## The headline methodological fact

**The frozen inferential package contains no strategy-vs-strategy hypothesis.** **This document is superseded in part — see `SUPERSEDED.md`:** a later post-hoc analysis, `results/rq3_strategy_inference_2026-09-25/`, does test strategy contrasts. Its six Holm families are
`RQ1-primary-{dreaddit,goemotions}`, `RQ1-mcnemar-{dreaddit,goemotions}` and
`RQ2-primary-{dreaddit,goemotions}`; all RQ1 comparisons are model-vs-model **within one strategy**, and the
statistical plan states verbatim: *"RQ3. No inference."* Validation check 7 enumerates the families and
confirms this.

Consequently **every statement in this document about one prompting strategy versus another is descriptive.** For tested strategy contrasts, see `SUPERSEDED.md`.
What *is* available for strategy comparison:

| Available | Not available |
|---|---|
| Per-configuration point estimates with bootstrap CIs (effective accuracy, conditional accuracy, macro-F1) | A test of the difference between two strategies |
| Five-run SDs, so run-to-run variability can be judged | Effect sizes with CIs **on a strategy difference** |
| Within-strategy model comparisons, fully tested | Holm decisions for strategy contrasts |

`tables/rq3_accuracy.csv` and `tables/rq3_macro_f1.csv` carry a column
`strategy_difference_statistically_tested` whose value is `NO` on all 60 rows, and a column
`ci_overlaps_zero_shot_ci_within_model`. **Non-overlapping CIs are not a hypothesis test** — the CIs are on
the two estimates, not on their paired difference, and no multiplicity control applies. Treat that column as a
rough screen for which contrasts would be worth testing, never as a result.

---

## Compact publication table — effective accuracy and macro-F1 by strategy

Δ columns are the arithmetic difference from the same model's zero-shot value. **No Δ below is a tested
effect.**

### Dreaddit

| Model | Eff. acc ZS | ZS-CoT (Δ) | 1S-CoT (Δ) | Macro-F1 ZS | ZS-CoT (Δ) | 1S-CoT (Δ) |
|---|---|---|---|---|---|---|
| Gemma 4 31B | 0.6933 | 0.6747 (−0.0186) | 0.6755 (−0.0177) | 0.6748 | 0.6503 (−0.0244) | 0.6510 (−0.0238) |
| Llama 4 Scout | 0.7296 | 0.7330 (+0.0034) | **0.7502 (+0.0206)** | 0.7519 | 0.7424 (−0.0095) | 0.7510 (−0.0009) |
| Mistral Small 4 | 0.6861 | 0.6609 (−0.0252) | 0.6735 (−0.0126) | 0.6657 | 0.6312 (−0.0345) | 0.6481 (−0.0176) |
| Phi-4 | 0.7222 | 0.7001 (−0.0220) | 0.7299 (+0.0077) | 0.7439 | 0.6964 (−0.0475) | 0.7302 (−0.0137) |
| Qwen3.5 27B | 0.6910 | 0.6023 (−0.0887) | 0.6475 (−0.0435) | 0.6742 | 0.5983 (−0.0759) | 0.6105 (−0.0637) |

### GoEmotions

| Model | Eff. acc ZS | ZS-CoT (Δ) | 1S-CoT (Δ) | Macro-F1 ZS | ZS-CoT (Δ) | 1S-CoT (Δ) |
|---|---|---|---|---|---|---|
| Gemma 4 31B | 0.8196 | 0.8174 (−0.0023) | 0.8132 (−0.0064) | 0.5932 | 0.5832 (−0.0099) | 0.5852 (−0.0079) |
| Llama 4 Scout | 0.7003 | 0.6826 (−0.0177) | 0.7318 (+0.0315) | 0.5202 | 0.5296 (+0.0095) | 0.5443 (+0.0242) |
| Mistral Small 4 | 0.7656 | 0.7412 (−0.0244) | **0.7830 (+0.0174)** | 0.5615 | 0.5357 (−0.0258) | **0.5940 (+0.0325)** |
| Phi-4 | 0.7363 | 0.7617 (+0.0254) | 0.6730 (−0.0633) | 0.5342 | 0.5634 (+0.0292) | 0.5406 (+0.0064) |
| Qwen3.5 27B | 0.7862 | 0.7897 (+0.0035) | 0.7701 (−0.0161) | 0.5723 | 0.5793 (+0.0070) | 0.5673 (−0.0050) |

**Descriptive reading.** No strategy wins everywhere. One-shot-CoT is the best strategy for 2 of 5 models on
Dreaddit (Llama, Phi-4) and 2 of 5 on GoEmotions (Llama, Mistral); zero-shot is best for 3 of 5 on Dreaddit
(Gemma, Mistral, Qwen) and for Gemma on GoEmotions; zero-shot-CoT is best only for Phi-4 and Qwen on
GoEmotions. The largest single within-model effect is **Qwen on Dreaddit, where zero-shot-CoT is 0.0887 below
zero-shot on effective accuracy** — and that drop is largely a serialisation failure rather than a reasoning
failure: Qwen's evaluability falls from 0.9980 to 0.9230 under zero-shot-CoT, and 263 of its 269 invalid
records are one JSON-escaping defect (invalid-output audit § C.3). Its *conditional* accuracy falls by only
0.0399 (0.6924 → 0.6525).

---

## Accuracy and macro-F1 disagree — verified

The reviewer's earlier observation is confirmed, and it is strong.

**Within-strategy model comparisons** (`tables/rq3_inferential.csv`, from the frozen RQ1 families):

| Dataset | Strategy | Pairs Holm-sig on eff. accuracy | Pairs Holm-sig on macro-F1 |
|---|---|---|---|
| Dreaddit | zero-shot | **0 / 10** | 6 / 10 |
| Dreaddit | zero-shot-CoT | 7 / 10 | 8 / 10 |
| Dreaddit | one-shot-CoT | 6 / 10 | 6 / 10 |
| Dreaddit | *total* | *13 / 30* | *20 / 30* |
| GoEmotions | zero-shot | 7 / 10 | **0 / 10** |
| GoEmotions | zero-shot-CoT | 7 / 10 | **0 / 10** |
| GoEmotions | one-shot-CoT | 7 / 10 | **0 / 10** |
| GoEmotions | *total* | *21 / 30* | *0 / 30* |

Two distinct disagreements, and they point in opposite directions:

1. **On Dreaddit, macro-F1 separates *more* pairs than accuracy** (20 vs 13 overall). The extreme case is
   zero-shot: **not one of the ten model pairs separates on effective accuracy after Holm correction, while
   six separate on macro-F1.** (Six pairs reach raw p < 0.05 on accuracy and six have a CI excluding zero, so
   the loss is entirely the multiplicity correction across the 60-hypothesis family.) Another concrete case:
   Llama versus Phi-4 under zero-shot-CoT is Holm-significant on macro-F1 (+0.0460, CI [+0.0226, +0.0692],
   p = 0.012) but not on effective accuracy (p = 0.146).
2. **On GoEmotions, accuracy separates 21 of 30 pairs and macro-F1 separates none.** Only 3 of 30 reach raw
   p < 0.05 (2 under zero-shot, 1 under one-shot-CoT, 0 under zero-shot-CoT) and only 2 have a CI excluding
   zero. Every GoEmotions macro-F1 CI is roughly 0.45–0.67 wide, because the class supports on the attributable pool are
   487 / 81 / 33 / 15 / 6 and six `anxiety` items carry one fifth of the metric.

**Consequence for the paper: a strategy must not be called "better" on the strength of an accuracy number.**
Within-model, the accuracy-optimal and the macro-F1-optimal strategy disagree for **2 of the 10 model ×
dataset pairs**, and both are on Dreaddit:

| Model × dataset | Best strategy by effective accuracy | Best strategy by macro-F1 |
|---|---|---|
| Llama 4 Scout × Dreaddit | one-shot-CoT (0.7502) | **zero-shot** (0.7519) |
| Phi-4 × Dreaddit | one-shot-CoT (0.7299) | **zero-shot** (0.7439) |

The other eight agree. On Dreaddit macro-F1 favours zero-shot for all five models, while accuracy favours
zero-shot for three and one-shot-CoT for two. Since none of these Δ values was tested, the safe wording is
that the two metrics disagree about the ordering, not that either ordering is established.

---

## Detailed supporting table

The full 30-row detail — mean, five-run SD, CI, Δ vs zero-shot, within-model rank, CI-overlap screen and the
explicit "not tested" flag — is in `tables/rq3_accuracy.csv` and `tables/rq3_macro_f1.csv`.
`tables/rq3_inferential.csv` records, per dataset × strategy × metric: the frozen family name, the family
size, how many pairs reach raw p < 0.05, how many have a CI excluding zero, how many survive Holm, the minimum
Holm p, what the test actually tests, and the constant value
`strategy_vs_strategy_test_available = "NONE in the frozen inferential package"`. That column describes the frozen 2026-09-21 package only and is still accurate; see `SUPERSEDED.md`.

## What RQ3 can and cannot claim

**Can claim.**
- The direction and size of every within-model strategy difference, as a descriptive Δ with both metrics.
- That no prompting strategy is best across models or across datasets.
- That accuracy and macro-F1 rank strategies differently, with the GoEmotions macro-F1 result (0/30 pairs
  separated) as the clearest evidence that accuracy-only conclusions are unsafe.
- That Qwen's large zero-shot-CoT accuracy drop on Dreaddit is accompanied by an evaluability drop, so it is
  substantially a formatting effect (the conditional-accuracy drop is less than half the size).

**Cannot claim.**
- That any strategy is statistically better than another **on the basis of this package**. No such test exists in the frozen package. A later post-hoc analysis — `results/rq3_strategy_inference_2026-09-25/` — does test this; see `SUPERSEDED.md`.
- That chain-of-thought helps or hurts in general.
- Any causal attribution: strategy, prompt length and exemplar presence all change together between the three
  conditions, so they cannot be separated in this design.
- Anything about efficiency here — that is `LATENCY_ANALYSIS.md`, and it is also untested.
