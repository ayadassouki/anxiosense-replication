# Invalid outputs — does excluding them bias the reported quality metrics?

Inputs: `invalid_output_audit_2026-09-25/invalid_outputs_row_level.jsonl` (1,986 model-invalid records,
verified against that package's manifest) and `descriptive_2026-09-21/authoritative_records.jsonl` for the
item pool's class composition. The taxonomy is **not** redone here.

> **This section contains the only genuinely new calculation in the package.**
> `code/02_exploratory_selection_effect.py` → `tables/exploratory_invalid_class_composition.csv`.
> It is **exploratory**, it is **not** part of the frozen inferential analysis, and its p-values carry a Holm
> correction **within their own 30-test family only**. No frozen result was altered.

## The question, stated precisely

`acc_cond = correct ÷ valid` and `acc_eff = correct ÷ attributable`, so
`acc_eff = acc_cond × evaluability` **exactly**. The gap between them is therefore arithmetic, not empirical,
and its size alone says nothing about bias.

The bias question is different: **are the dropped items systematically different from the kept items?** If a
configuration's invalid outputs are drawn disproportionately from one class, conditional accuracy is computed
on a pool whose composition differs from the benchmark's, and it is no longer comparable across
configurations.

## Method (exploratory)

For each of the 30 configurations: compare the ground-truth class composition of its invalid records with the
composition of the attributable item pool (Dreaddit 355/699 = 0.5079 class `1`; GoEmotions 487/622 = 0.7830
`non_distress`). Exact two-sided binomial test; Holm correction across the 30 tests. Also reported: the
enrichment ratio, and the majority share of the pool that *survives* into conditional accuracy.

## OBSERVATION

| Configuration | Invalid (5 runs) | Majority share of invalids | Expected | Ratio | Exploratory Holm p | Valid-pool majority share |
|---|---|---|---|---|---|---|
| **Qwen3.5 27B · Dreaddit · ZS-CoT** | 269 | **0.9405** | 0.5079 | **1.85** | **2.6 × 10⁻⁵³** | 0.4718 |
| **Llama 4 Scout · GoEmotions · 1S-CoT** | 143 | 0.9091 | 0.7830 | 1.16 | **2.0 × 10⁻³** | 0.7769 |
| **Llama 4 Scout · Dreaddit · ZS** | 106 | 0.7264 | 0.5079 | 1.43 | **1.2 × 10⁻⁴** | 0.5010 |
| **Llama 4 Scout · Dreaddit · ZS-CoT** | 52 | 0.7308 | 0.5079 | 1.44 | **2.4 × 10⁻²** | 0.5045 |
| Phi-4 · GoEmotions · 1S-CoT | 499 | 0.8156 | 0.7830 | 1.04 | 1.00 (n.s.) | 0.7767 |
| Llama 4 Scout · GoEmotions · ZS-CoT | 193 | 0.8601 | 0.7830 | 1.10 | 0.15 (n.s.) | 0.7779 |
| Phi-4 · GoEmotions · ZS | 191 | 0.8010 | 0.7830 | 1.02 | 1.00 (n.s.) | 0.7818 |
| Phi-4 · GoEmotions · ZS-CoT | 183 | 0.7650 | 0.7830 | 0.98 | 1.00 (n.s.) | 0.7841 |
| Phi-4 · Dreaddit · ZS | 106 | 0.4245 | 0.5079 | 0.84 | 1.00 (n.s.) | 0.5105 |

Full 30-row table in `tables/exploratory_invalid_class_composition.csv`.

**Four of thirty configurations show class-selective invalidity that survives Holm correction within this
exploratory family.** All four involve Qwen on Dreaddit zero-shot-CoT or Llama.

## STATISTICAL EVIDENCE

- **The specific pattern previously suspected for Phi-4 / GoEmotions / one-shot-CoT is NOT supported.** That
  cell has by far the largest conditional-minus-effective gap in the grid (0.1281: 0.8011 vs 0.6730) and the
  lowest evaluability (0.8395), but its invalids are only 1.04× enriched in the majority class
  (0.8156 vs 0.7830 expected, exploratory Holm p = 1.00). The gap there is driven by the **volume** of invalid
  outputs, not by which items are lost. The surviving pool is 0.7767 `non_distress` against a benchmark of
  0.7830 — a shift of −0.6 percentage points.
- **The strongest selection effect is elsewhere and is unambiguous:** Qwen3.5 27B / Dreaddit / zero-shot-CoT.
  253 of its 269 invalid records (94.05%) have ground truth `1` (stress), against 50.79% expected; the
  surviving pool is 47.18% class `1` instead of 50.79%, a shift of −3.6 percentage points. Its conditional
  accuracy (0.6525) is computed on a materially different item mix from every other configuration's.
- **Even where the enrichment is significant, the shift in the surviving pool is small** — at most 3.6
  percentage points (Qwen/Dreaddit/ZS-CoT), and under 1 point for the three Llama cells.
- **One configuration is enriched in the opposite direction** (Phi-4 / Dreaddit / ZS, ratio 0.84), though not
  significantly.

## INTERPRETATION

1. **Effective accuracy is unaffected by this issue** and remains the right publication metric: it keeps every
   attributable item in the denominator, so no selection can occur.
2. **Conditional accuracy is not comparable across configurations** where the invalid rate is non-trivial,
   and for Qwen/Dreaddit/zero-shot-CoT specifically it is computed on a measurably different class mix. Report
   it beside effective accuracy for transparency, never as the headline, and never rank configurations by it.
3. **The size of the conditional-minus-effective gap is not a bias indicator.** The largest gap in the grid
   (Phi-4/GoEmotions/1S-CoT) has no detectable selection effect, while the clearest selection effect
   (Qwen/Dreaddit/ZS-CoT) has a gap of only 0.0502. These are different phenomena and the paper should not
   conflate them.
4. **Direction of any residual bias is not established.** Knowing that the dropped items skew toward class `1`
   does not tell us whether conditional accuracy is inflated or deflated; that depends on the model's
   per-class accuracy on the dropped items, which is unknowable because those items produced no prediction.

## LIMITATION

- **Exploratory.** These 30 tests were not pre-specified, are not in the frozen plan, and their Holm family is
  separate from every frozen family. They should be described as exploratory in the paper or omitted.
- **Ground truth of a dropped item is observable; the model's would-be answer is not.** No analysis can
  recover what the model would have predicted, so the *direction* of bias in conditional accuracy is not
  identifiable from these data. Any statement beyond "the dropped items are not a random sample" is
  unsupported.
- **Class composition is only one axis.** Items could also be selected on length, crisis language or topic;
  none of that was tested here.
- **A separate, still-open question.** `descriptive_2026-09-21/ISSUES_FOR_AUDIT.md` item 1 records that in
  Phi-4/GoEmotions/one-shot-CoT run 5, 197 of the 229 newly `fail_unparseable` samples had been
  `ok_empty_list` (i.e. `non_distress`) in run 4, and that this run's conditional macro-F1 *rises* to 0.6231
  while effective accuracy falls to 0.4486. That is a **run-level** phenomenon about which items moved between
  runs; the analysis above is a **pooled** class-composition analysis and does not settle it. It needs its own
  run-level test before anything is claimed about it.
- **No causal claim is made.** Nothing here explains *why* particular items fail; the invalid-output audit
  keeps that question separate and unresolved.

## Recommended wording for the paper

> Model-invalid outputs are excluded from conditional accuracy but retained in the denominator of effective
> accuracy, which is the metric reported throughout. An exploratory check of whether invalid outputs are drawn
> disproportionately from the majority class found significant class-selective invalidity in 4 of 30
> configurations after Holm correction within that exploratory family, the strongest being Qwen3.5 27B under
> zero-shot chain-of-thought on Dreaddit (94.1% of invalid items were stress-positive against 50.8%
> expected). The configuration with the largest conditional-versus-effective gap, Phi-4 under one-shot
> chain-of-thought on GoEmotions, showed no such enrichment; its gap reflects the volume of invalid outputs
> rather than which items were lost. Conditional accuracy is therefore reported for transparency only and is
> not used for ranking.
