# SUPERSEDED — the RQ3 prompting-strategy sections of this package

**Added 2026-09-29.** This notice applies **only to the RQ3 prompting-strategy discussion** in this
package. RQ1, RQ2, the latency analysis and the invalid-output selection-effect analysis are **not
superseded** and stand as written.

## What happened, in order

| Artifact | UTC |
|---|---|
| Frozen RQ1/RQ2 statistical analysis plan — states "RQ3. No inference." | 2026-09-21 |
| `FINAL_RESULTS_SUMMARY.md` and `RQ3_PROMPTING_STRATEGIES.md` written | **2026-09-25T20:44:46Z** |
| `rq3_strategy_inference_2026-09-25/PREREGISTRATION_FREEZE.json` — `execution_status_at_freeze: NOT YET EXECUTED` | **2026-09-25T22:04:33Z** |
| RQ3 strategy analysis executed (`analysis_manifest.json` `created_utc`) | **2026-09-25T22:04:45Z** |
| Result tables written | **2026-09-25T22:21:07Z** |

## The earlier statements were true when written

When this package was assembled, it was **correct** that no strategy-vs-strategy hypothesis existed
in the frozen 2026-09-21 inferential package. That remains correct today: the frozen package's six
Holm families are `RQ1-primary-{dreaddit,goemotions}`, `RQ1-mcnemar-{dreaddit,goemotions}` and
`RQ2-primary-{dreaddit,goemotions}`, none of which compares prompting strategies, and the frozen
plan does say "RQ3. No inference."

Nothing in that earlier reasoning was wrong, and nothing in it has been rewritten. What changed is
that a **separate, later analysis** was carried out — and a reader of this package alone would not
know it exists. Hence this notice.

## What the later analysis is

`results/rq3_strategy_inference_2026-09-25/` — a **post-hoc / exploratory** inferential analysis of
prompting strategy on classification quality. Start with its `RQ3_STRATEGY_INFERENCE_REPORT.md`.

It is labelled post-hoc because, although the estimation procedure was pre-specified and frozen on
2026-09-21 and applied unchanged, the **contrasts were chosen after the descriptive results were
known**. It is not a confirmatory analysis, and RQ1 and RQ2 remain this study's only pre-specified
confirmatory analyses.

What it tested: within each model and dataset, three pairwise strategy contrasts (zero-shot vs
zero-shot-CoT, zero-shot vs one-shot-CoT, zero-shot-CoT vs one-shot-CoT), on two co-primary outcomes
(effective accuracy and macro-F1). Statistical unit = the benchmark item carrying all five runs,
n = 699 (Dreaddit) / 622 (GoEmotions). Paired item-level permutation, P = 10,000, whole five-run
vector swapped per item. Item-cluster bootstrap, B = 4,000, one shared index per dataset, 95%
percentile intervals. Invalid outputs counted as incorrect, not conditioned away.

Families and correction — Holm–Bonferroni within each dataset:

| Family | Size |
|---|---|
| `RQ3-primary-dreaddit` | 30 |
| `RQ3-primary-goemotions` | 30 |
| `RQ3-mcnemar-dreaddit` (secondary) | 15 |
| `RQ3-mcnemar-goemotions` (secondary) | 15 |

Study-wide multiplicity across RQ1, RQ2 and RQ3 is **not** controlled — the same items and
configurations are reused, and Holm controls the family-wise error rate only within each declared
family.

## What is significant — and how to count it

**20 of 60 rows** in `tables/rq3_strategy_pairs_primary.csv` are Holm-significant,
where a row is one *dataset × model × strategy-pair × metric*:

| Dataset | Effective accuracy | Macro-F1 | Rows |
|---|---|---|---|
| Dreaddit | 7 / 15 | 7 / 15 | 14 / 30 |
| GoEmotions | 6 / 15 | 0 / 15 | 6 / 30 |

**Those 20 metric-specific rows correspond to 14 distinct strategy contrasts, not
20 distinct comparisons.** 6 contrasts are significant on **both** co-primary metrics and
therefore occupy two rows each; 7 are significant on effective accuracy only; 1 on
macro-F1 only. Any text quoting "20" must say **rows**, or quote **14 contrasts**.

### Dreaddit

| Model | Contrast | Significant on |
|---|---|---|
| Gemma 4 31B | zero-shot vs one-shot-CoT | both |
| Gemma 4 31B | zero-shot vs zero-shot-CoT | both |
| Mistral Small 4 | zero-shot vs zero-shot-CoT | both |
| Phi-4 | zero-shot vs zero-shot-CoT | macro-F1 only |
| Phi-4 | zero-shot-CoT vs one-shot-CoT | both |
| Qwen3.5 27B | zero-shot vs one-shot-CoT | both |
| Qwen3.5 27B | zero-shot vs zero-shot-CoT | both |
| Qwen3.5 27B | zero-shot-CoT vs one-shot-CoT | effective accuracy only |

### GoEmotions

| Model | Contrast | Significant on |
|---|---|---|
| Llama 4 Scout | zero-shot-CoT vs one-shot-CoT | effective accuracy only |
| Mistral Small 4 | zero-shot vs zero-shot-CoT | effective accuracy only |
| Mistral Small 4 | zero-shot-CoT vs one-shot-CoT | effective accuracy only |
| Phi-4 | zero-shot vs one-shot-CoT | effective accuracy only |
| Phi-4 | zero-shot vs zero-shot-CoT | effective accuracy only |
| Phi-4 | zero-shot-CoT vs one-shot-CoT | effective accuracy only |

Secondary exact McNemar on majority-vote (>= 3/5) effective correctness: **10 of
30** (7 Dreaddit, 3 GoEmotions). It cannot promote a
non-significant primary result, and disagreements are reported as disagreements.

## What the later analysis does not support

- No globally best strategy, and no pooled strategy main effect across models — not computed, by design.
- No causal claim. Strategy, prompt length and exemplar presence change together.
- No conditional-accuracy ranking. Denominators differ by arm; that table carries confidence
  intervals only and **no p-values**.
- All three GoEmotions Phi-4 effective-accuracy results are driven by a single anomalous run (run 5:
  271 invalid outputs, effective accuracy 0.4486, five-run SD 0.1258) and McNemar does not confirm
  any of them. Report with that caveat or not at all.
- The GoEmotions macro-F1 null (0 of
  15) is **inconclusive, not negative** — attributable class supports
  are 487 / 81 / 33 / 15 / 6, so six `anxiety` items carry one fifth of the metric.
- **Nothing about latency or efficiency.** The frozen refusal of inferential latency analysis stands
  unchanged, and `LATENCY_ANALYSIS.md` in this package remains correct as written.

## Practical guidance

Write the paper's RQ3 **classification-quality** results from
`results/rq3_strategy_inference_2026-09-25/`, labelled post-hoc / exploratory. Use this package for
RQ1, RQ2, latency and the invalid-output analysis. Where this package says a strategy comparison is
untested, read that as true of the frozen 2026-09-21 package and see the later analysis for the
tested result.
