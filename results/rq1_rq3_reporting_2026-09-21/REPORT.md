# AnxioSense publication grid: RQ1–RQ3 reporting (2026-09-21)

This is a reporting step on the frozen, independently verified results in `descriptive_2026-09-21`. That folder, the raw run data, the parser (1.0.0) and the scoring policy (MetricPolicy 1.0.0) were not changed. There were no model or API calls, no reruns and no significance tests. Every invalid output, refusal, out-of-vocabulary (OOV) prediction, `{}` output and the Phi-4 GoEmotions one-shot-CoT run 5 are included exactly as the frozen pipeline scored them.

**Measured** marks a value computed from stored records. **Interpretation** marks a reading of those values.

---

## 0. Inputs, definitions and rounding

**Grid.** 2 datasets × 5 models × 3 prompting strategies × 5 runs = 150 cells and 100,350 authoritative records. Dreaddit has 715 items per cell (16 safety intercepts, 699 attributable). GoEmotions has 623 scoreable items per cell (1 safety intercept, 622 attributable).

**Source for every RQ1/RQ2 number.** `descriptive_2026-09-21/authoritative_records.jsonl`, recomputed here with exact rational arithmetic (`code/rq12_tables.py`). It was then cross-checked against the frozen `per_run_results.csv`, `cell_metrics.json`, `aggregate_results.csv` and `aggregate_five_runs.json`, and against the verification record `verification_2026-09-21/metrics_verification_result.json`.

- 4,457 checks were run: 3,811 bit-identical and 646 differing only in the last binary digit. Every one of those 646 is already listed in the independent verification. There were **0 conflicts**, so no value had to be chosen between sources (`rq12_crosscheck.json`).

**Metric definitions (MetricPolicy 1.0.0, as frozen).**

- *Safety intercepts* are excluded from model attribution. They short-circuit before any LLM call.
- *Attributable* = N_total − N_safety.
- *Valid* = the stored `prediction_valid` is true.
- *Model-invalid* = the stored `failure_class` is `MODEL_BEHAVIOUR`: unparseable, truncated, `{}`, refusal or OOV, exactly as the parser classified it.
- *Conditional accuracy* = correct / valid.
- *Effective accuracy* = correct / attributable. Invalid outputs count as wrong.
- *Per-class precision, recall and F1* are computed on valid predictions. A value is 0 when undefined.
- *Macro-P, macro-R and macro-F1* are the unweighted means over the fixed label list: Dreaddit [0, 1]; GoEmotions [anxiety, fear, sadness, frustration, non_distress].
- *Evaluability* = valid / attributable.
- *Five-run value* = the mean of the five per-run values, ± the sample SD (n − 1).
  - For acc. (cond.), acc. (eff.), macro-F1 and evaluability, these are the frozen aggregates.
  - The five-run macro-P and macro-R are not in the frozen aggregate files. They are the same mean ± SD applied to the frozen per-run values, which were cross-checked.

**Majority baseline (frozen).** Dreaddit 369/715 = 0.516 (class 1). GoEmotions 487/623 = 0.782 (non_distress).

- These are computed over all included items, while model accuracies exclude safety intercepts.
- On the attributable set, the majority rates are 355/699 = 0.508 and 487/622 = 0.783.
- **Measured:** using the attributable-set rate instead of the frozen baseline does not change any "runs above baseline" count in this report.

**Rounding rule.**

- Accuracy-type values are shown to 3 decimals, ROUND_HALF_UP.
- Rounding is applied to the exact rational value (means) or to a 60-digit decimal (SDs), never to a binary float.
- **Checked:** no presented five-run value lies exactly on a 3-decimal half boundary. No presented value rounds differently from the corresponding frozen float.
- The two known per-run half-boundary cases are both per-class F1 for class 1 on Dreaddit:
  - Llama 4 Scout zero-shot run 1: exact 59/80 = 0.7375 → 0.738 under this rule.
  - Qwen3.5 27B one-shot-CoT run 4: exact 0.4875 → 0.488.
  - Neither appears in a presented table, because the tables show five-run aggregates.
- Latency values are shown in seconds to 2 decimals (ROUND_HALF_UP of the measured float).
- A displayed 1.000 or ±0.000 can hide a small non-zero value. The count columns give the exact numbers.

**Interpretation boundary.** Dreaddit scores the Referral agent's `risk_level` (low → 0; moderate/urgent → 1) against *stress vs non-stress* labels. It is a stress-detection proxy. It does not validate the GoEmotions `anxiety` class or clinical anxiety detection.

---

## RQ1: Which LLM yields the best results?

### RQ1 · Dreaddit (binary stress; 5-run mean ± SD)

Source: `tables/rq1_dreaddit.csv`, built from `authoritative_records.jsonl` and cross-checked as above. Infrastructure failures = 0 in every cell. Safety intercepts = 16 per run in every cell.

| Model | Strategy | Acc. (cond.) | Acc. (eff.) | Macro-P | Macro-R | Macro-F1 | Evaluability | Valid / attrib. (Σ5) | Model-invalid per run |
|---|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot | 0.693 ± 0.004 | 0.693 ± 0.004 | 0.760 ± 0.003 | 0.697 ± 0.004 | 0.675 ± 0.005 | 1.000 ± 0.000 | 3495 / 3495 | 0/0/0/0/0 |
|  | zero-shot-cot | 0.675 ± 0.001 | 0.675 ± 0.001 | 0.754 ± 0.004 | 0.679 ± 0.001 | 0.650 ± 0.001 | 1.000 ± 0.000 | 3495 / 3495 | 0/0/0/0/0 |
|  | one-shot-cot | 0.676 ± 0.006 | 0.676 ± 0.006 | 0.756 ± 0.005 | 0.680 ± 0.006 | 0.651 ± 0.008 | 1.000 ± 0.000 | 3495 / 3495 | 0/0/0/0/0 |
| Llama 4 Scout | zero-shot | 0.752 ± 0.005 | 0.730 ± 0.003 | 0.755 ± 0.005 | 0.753 ± 0.005 | 0.752 ± 0.005 | 0.970 ± 0.005 | 3389 / 3495 | 19/22/27/19/19 |
|  | zero-shot-cot | 0.744 ± 0.005 | 0.733 ± 0.005 | 0.753 ± 0.004 | 0.745 ± 0.004 | 0.742 ± 0.005 | 0.985 ± 0.002 | 3443 / 3495 | 13/9/10/10/10 |
|  | one-shot-cot | 0.752 ± 0.004 | 0.750 ± 0.005 | 0.758 ± 0.004 | 0.753 ± 0.004 | 0.751 ± 0.005 | 0.998 ± 0.001 | 3487 / 3495 | 2/1/2/2/1 |
| Mistral Small 4 | zero-shot | 0.686 ± 0.003 | 0.686 ± 0.004 | 0.758 ± 0.003 | 0.690 ± 0.003 | 0.666 ± 0.004 | 1.000 ± 0.001 | 3494 / 3495 | 0/0/1/0/0 |
|  | zero-shot-cot | 0.661 ± 0.004 | 0.661 ± 0.004 | 0.752 ± 0.008 | 0.666 ± 0.004 | 0.631 ± 0.004 | 1.000 ± 0.001 | 3494 / 3495 | 1/0/0/0/0 |
|  | one-shot-cot | 0.674 ± 0.005 | 0.674 ± 0.005 | 0.757 ± 0.007 | 0.678 ± 0.005 | 0.648 ± 0.006 | 1.000 ± 0.000 | 3495 / 3495 | 0/0/0/0/0 |
| Phi-4 | zero-shot | 0.745 ± 0.012 | 0.722 ± 0.016 | 0.751 ± 0.011 | 0.746 ± 0.012 | 0.744 ± 0.013 | 0.970 ± 0.010 | 3389 / 3495 | 20/34/17/17/18 |
|  | zero-shot-cot | 0.706 ± 0.003 | 0.700 ± 0.002 | 0.742 ± 0.003 | 0.709 ± 0.003 | 0.696 ± 0.004 | 0.992 ± 0.003 | 3466 / 3495 | 8/4/4/6/7 |
|  | one-shot-cot | 0.733 ± 0.010 | 0.730 ± 0.010 | 0.747 ± 0.011 | 0.735 ± 0.010 | 0.730 ± 0.010 | 0.995 ± 0.001 | 3479 / 3495 | 4/4/2/3/3 |
| Qwen3.5 27B | zero-shot | 0.692 ± 0.001 | 0.691 ± 0.001 | 0.757 ± 0.001 | 0.696 ± 0.001 | 0.674 ± 0.001 | 0.998 ± 0.001 | 3488 / 3495 | 2/1/1/1/2 |
|  | zero-shot-cot | 0.653 ± 0.004 | 0.602 ± 0.005 | 0.747 ± 0.004 | 0.634 ± 0.005 | 0.598 ± 0.006 | 0.923 ± 0.004 | 3226 / 3495 | 54/55/50/53/57 |
|  | one-shot-cot | 0.648 ± 0.001 | 0.647 ± 0.002 | 0.757 ± 0.001 | 0.653 ± 0.001 | 0.610 ± 0.002 | 0.999 ± 0.001 | 3491 / 3495 | 0/1/1/1/1 |

### RQ1 · GoEmotions (5-class; 5-run mean ± SD)

Source: `tables/rq1_goemotions.csv`, built the same way. Infrastructure failures = 0 in every cell. Safety intercepts = 1 per run in every cell.

| Model | Strategy | Acc. (cond.) | Acc. (eff.) | Macro-P | Macro-R | Macro-F1 | Evaluability | Valid / attrib. (Σ5) | Model-invalid per run |
|---|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot | 0.820 ± 0.004 | 0.820 ± 0.004 | 0.711 ± 0.015 | 0.552 ± 0.004 | 0.593 ± 0.007 | 1.000 ± 0.000 | 3110 / 3110 | 0/0/0/0/0 |
|  | zero-shot-cot | 0.817 ± 0.004 | 0.817 ± 0.004 | 0.709 ± 0.011 | 0.543 ± 0.003 | 0.583 ± 0.008 | 1.000 ± 0.000 | 3110 / 3110 | 0/0/0/0/0 |
|  | one-shot-cot | 0.815 ± 0.004 | 0.813 ± 0.003 | 0.695 ± 0.010 | 0.551 ± 0.002 | 0.585 ± 0.005 | 0.998 ± 0.003 | 3103 / 3110 | 0/0/1/2/4 |
| Llama 4 Scout | zero-shot | 0.727 ± 0.007 | 0.700 ± 0.008 | 0.497 ± 0.017 | 0.632 ± 0.014 | 0.520 ± 0.017 | 0.964 ± 0.004 | 2997 / 3110 | 20/22/23/22/26 |
|  | zero-shot-cot | 0.728 ± 0.010 | 0.683 ± 0.009 | 0.517 ± 0.013 | 0.619 ± 0.027 | 0.530 ± 0.013 | 0.938 ± 0.002 | 2917 / 3110 | 39/38/40/39/37 |
|  | one-shot-cot | 0.767 ± 0.008 | 0.732 ± 0.009 | 0.536 ± 0.012 | 0.622 ± 0.010 | 0.544 ± 0.013 | 0.954 ± 0.002 | 2967 / 3110 | 27/27/30/29/30 |
| Mistral Small 4 | zero-shot | 0.770 ± 0.008 | 0.766 ± 0.005 | 0.542 ± 0.018 | 0.623 ± 0.012 | 0.561 ± 0.011 | 0.995 ± 0.003 | 3093 / 3110 | 1/2/6/3/5 |
|  | zero-shot-cot | 0.746 ± 0.007 | 0.741 ± 0.008 | 0.499 ± 0.007 | 0.633 ± 0.016 | 0.536 ± 0.010 | 0.994 ± 0.001 | 3091 / 3110 | 4/5/3/4/3 |
|  | one-shot-cot | 0.786 ± 0.005 | 0.783 ± 0.005 | 0.592 ± 0.011 | 0.617 ± 0.006 | 0.594 ± 0.008 | 0.996 ± 0.002 | 3098 / 3110 | 3/4/2/1/2 |
| Phi-4 | zero-shot | 0.784 ± 0.008 | 0.736 ± 0.016 | 0.583 ± 0.026 | 0.551 ± 0.013 | 0.534 ± 0.016 | 0.939 ± 0.015 | 2919 / 3110 | 51/37/43/27/33 |
|  | zero-shot-cot | 0.809 ± 0.003 | 0.762 ± 0.009 | 0.635 ± 0.019 | 0.577 ± 0.013 | 0.563 ± 0.011 | 0.941 ± 0.014 | 2927 / 3110 | 29/48/43/35/28 |
|  | one-shot-cot | 0.801 ± 0.004 | 0.673 ± 0.126 | 0.647 ± 0.030 | 0.550 ± 0.056 | 0.541 ± 0.049 | 0.840 ± 0.154 | 2611 / 3110 | 51/62/49/66/271 |
| Qwen3.5 27B | zero-shot | 0.786 ± 0.001 | 0.786 ± 0.001 | 0.594 ± 0.007 | 0.565 ± 0.007 | 0.572 ± 0.007 | 1.000 ± 0.000 | 3110 / 3110 | 0/0/0/0/0 |
|  | zero-shot-cot | 0.790 ± 0.002 | 0.790 ± 0.002 | 0.607 ± 0.004 | 0.566 ± 0.008 | 0.579 ± 0.006 | 1.000 ± 0.000 | 3110 / 3110 | 0/0/0/0/0 |
|  | one-shot-cot | 0.773 ± 0.000 | 0.770 ± 0.000 | 0.559 ± 0.000 | 0.585 ± 0.000 | 0.567 ± 0.000 | 0.997 ± 0.000 | 3100 / 3110 | 2/2/2/2/2 |

### RQ1 · Dreaddit: what the measured values show

**Measured**

- **Llama 4 Scout** has the highest five-run conditional accuracy, effective accuracy, macro-F1 and macro-recall under **each** of the three strategies.
  - Highest cells: zero-shot at acc. (cond.) 0.752 and macro-F1 0.752, and one-shot-CoT at acc. (cond.) 0.752, acc. (eff.) 0.750 and macro-F1 0.751.
- **Phi-4** is next: zero-shot macro-F1 0.744, one-shot-CoT 0.730.
- **Gemma, Mistral and Qwen** have macro-F1 0.598–0.675.
  - They label most items as not stressed: class-0 recall 0.942–0.974 against class-1 recall 0.302–0.450. See the Dreaddit per-class table in RQ2.
- **Macro-precision gives a different ranking** within a narrow band (0.742–0.760). Gemma zero-shot is highest (0.760) and Phi-4 zero-shot-CoT lowest (0.742).
- **Invalid outputs change the picture for the two leading models under zero-shot.**
  - Llama and Phi-4 each have 106 model-invalid outputs over five runs (evaluability 0.970).
  - Their accuracy drops from conditional to effective: Llama 0.752 → 0.730; Phi-4 0.745 → 0.722.
  - Gemma and Mistral are the most evaluable (≥ 3,494 / 3,495 valid in every cell).
  - Qwen zero-shot-CoT has the most invalid outputs: 269, evaluability 0.923, effective accuracy 0.602.
- All 15 cells exceed the 0.516 baseline on both accuracy measures in every run.

**Interpretation**

- On Dreaddit, Llama 4 Scout has the highest observed accuracy, effective accuracy, macro-F1 and macro-recall. This is consistent across all three strategies, so it does not depend on which accuracy-type metric is chosen.
- Two qualifiers apply:
  1. Phi-4 is close behind, and the top cells differ by amounts similar to their run-to-run SDs (e.g. Phi-4 zero-shot ± 0.012).
  2. Llama's zero-shot advantage is partly offset by a higher invalid-output rate than Gemma or Mistral.
- Ranked by macro-precision or evaluability, Llama is not first.

### RQ1 · GoEmotions: what the measured values show

**Measured**

- **Gemma 4 31B** has the highest conditional accuracy, effective accuracy and macro-precision under every strategy. Its accuracies are 0.813–0.820, and its evaluability is 0.998–1.000.
- **Macro-F1 does not have a single leader.**
  - Gemma is highest under zero-shot (0.593) and zero-shot-CoT (0.583).
  - Under one-shot-CoT, Mistral Small 4 (0.594) is above Gemma (0.585).
  - Mistral one-shot-CoT (0.594) vs Gemma zero-shot (0.593) is the largest macro-F1 pair in the grid, separated by less than either SD.
- **Macro-recall runs the other way.** Gemma has the lowest macro-recall cell (0.543, zero-shot-CoT). Llama 4 Scout and Mistral lead: zero-shot Llama 0.632, zero-shot-CoT Mistral 0.633, one-shot-CoT Llama 0.622.
- **Phi-4: conditional and effective accuracy disagree.**
  - Among models, its conditional accuracy is second only to Gemma (best cell: zero-shot-CoT 0.809).
  - Its evaluability is 0.840–0.941, so its effective accuracy is lower (0.673–0.762).
  - Phi-4 one-shot-CoT has the lowest effective accuracy of any cell, 0.673 ± 0.126. That is driven by run 5, where 271 of 622 attributable outputs were invalid. The run is included as frozen.
- **Llama 4 Scout** has the lowest accuracies (0.727–0.767 cond.) but among the highest macro-recall.
- **Qwen3.5 27B** is almost fully evaluable, and its runs are nearly identical: SD ≤ 0.002 on accuracies, down to 0.000 at 3 decimals for one-shot-CoT.

**Interpretation**

- On GoEmotions, the answer depends on the metric:
  - accuracy and macro-precision favour Gemma;
  - macro-F1 is a near-tie between Gemma and Mistral (one-shot-CoT);
  - macro-recall favours Llama and Mistral;
  - conditional vs effective accuracy moves Phi-4 from second to fourth when models are ranked by their best cell.
- The accuracy-type ranking largely tracks how often each model predicts the majority class. See RQ2.

### RQ1 · Across datasets

**Measured**

- The model with the highest Dreaddit results (Llama 4 Scout) has the lowest GoEmotions accuracies.
- The model with the highest GoEmotions accuracies (Gemma 4 31B) is in the lower group on Dreaddit macro-F1 (0.650–0.675).

**Interpretation**

"Best LLM" cannot responsibly be reduced to one model. The leader changes with the dataset, and on GoEmotions it also changes with the metric (accuracy vs macro-F1 vs macro-recall vs effective accuracy). Invalid-output rates change the picture further for Llama, Phi-4 and Qwen. Descriptively:

- **Dreaddit:** Llama 4 Scout is the consistent leader, with Phi-4 close.
- **GoEmotions:** Gemma leads on accuracy, Gemma and Mistral share macro-F1, and Llama and Mistral lead on recall.

No statistical superiority is claimed; significance testing has not been done.

---

## RQ2: What is the accuracy of AnxioSense?

### What "AnxioSense accuracy" can and cannot mean here

**What was evaluated.** The evaluation called AnxioSense's `/api/workflow/evaluate` path, which runs the multi-agent workflow in social-media mode: emotion, symptom, context and referral agents, then the report step. Each configuration uses **one** LLM with **one** prompting strategy.

- The Dreaddit label comes from the Referral agent's risk level.
- The GoEmotions label comes from the Emotion agent's first emotion, mapped through the frozen V1 mapping.

There are **30 configurations** (5 models × 3 strategies) per dataset. Each has its own accuracy.

**No single overall figure exists.** The publication runner, the frozen grid manifest and MetricPolicy 1.0.0 define no aggregation across models or strategies, and none across the two datasets, which score different agents on different targets. **No pre-specified single overall AnxioSense accuracy exists, and none is produced here.** Results are given per configuration and as ranges.

**What the older protocol says.** The July 2026 `evaluation/AnxioSense_Experimental_Setup.docx` (§6.3) does not aggregate either. It *designates* a configuration for RQ2: "Full pipeline (top LLM, 1S-CoT)". The top LLM is defined as the highest macro-F1 "on symptom extraction" among the five models under one-shot-CoT on Dreaddit. Three caveats apply:

1. Symptom extraction was not scored in this grid.
2. Choosing the "top" model on these same test items selects on the evaluation data, which is optimistic.
3. Whether that document governs the publication analysis is a decision for Aya and the supervisors.

For transparency only, here is what the rule would pick if Dreaddit referral macro-F1 were substituted for symptom-extraction macro-F1:

- It would select **Llama 4 Scout, one-shot-CoT**, whose Dreaddit macro-F1 of 0.751 is above Phi-4's 0.730.
- That configuration measures:
  - **Dreaddit:** acc. (cond.) 0.752 ± 0.004, acc. (eff.) 0.750 ± 0.005, macro-F1 0.751 ± 0.005.
  - **GoEmotions:** acc. (cond.) 0.767 ± 0.008 and acc. (eff.) 0.732 ± 0.009, **both below the 0.782 majority baseline in all 5 runs**, with macro-F1 0.544 ± 0.013.

This is not presented as "the" AnxioSense accuracy.

**Metric and task limits.**

- Cohen's weighted κ is listed in that protocol for RQ2, but it is not part of the frozen scoring policy and is not computed here.
- Dreaddit measures stress vs non-stress through a referral-level proxy, not anxiety.

### RQ2 · Dreaddit (majority baseline 0.516; Δ = five-run mean − baseline)

Source: `tables/rq2_dreaddit.csv`. Baseline from the frozen dataset manifest, 369/715. "Runs > base" counts runs whose exact per-run accuracy exceeds 369/715.

| Model | Strategy | Acc. (cond.) | Acc. (eff.) | Macro-F1 | Δ cond. − base | Δ eff. − base | Runs > base (cond.) | Runs > base (eff.) | Evaluability | Model-invalid (Σ5) |
|---|---|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot | 0.693 ± 0.004 | 0.693 ± 0.004 | 0.675 ± 0.005 | 0.177 | 0.177 | 5 | 5 | 1.000 ± 0.000 | 0 |
|  | zero-shot-cot | 0.675 ± 0.001 | 0.675 ± 0.001 | 0.650 ± 0.001 | 0.159 | 0.159 | 5 | 5 | 1.000 ± 0.000 | 0 |
|  | one-shot-cot | 0.676 ± 0.006 | 0.676 ± 0.006 | 0.651 ± 0.008 | 0.159 | 0.159 | 5 | 5 | 1.000 ± 0.000 | 0 |
| Llama 4 Scout | zero-shot | 0.752 ± 0.005 | 0.730 ± 0.003 | 0.752 ± 0.005 | 0.236 | 0.214 | 5 | 5 | 0.970 ± 0.005 | 106 |
|  | zero-shot-cot | 0.744 ± 0.005 | 0.733 ± 0.005 | 0.742 ± 0.005 | 0.228 | 0.217 | 5 | 5 | 0.985 ± 0.002 | 52 |
|  | one-shot-cot | 0.752 ± 0.004 | 0.750 ± 0.005 | 0.751 ± 0.005 | 0.236 | 0.234 | 5 | 5 | 0.998 ± 0.001 | 8 |
| Mistral Small 4 | zero-shot | 0.686 ± 0.003 | 0.686 ± 0.004 | 0.666 ± 0.004 | 0.170 | 0.170 | 5 | 5 | 1.000 ± 0.001 | 1 |
|  | zero-shot-cot | 0.661 ± 0.004 | 0.661 ± 0.004 | 0.631 ± 0.004 | 0.145 | 0.145 | 5 | 5 | 1.000 ± 0.001 | 1 |
|  | one-shot-cot | 0.674 ± 0.005 | 0.674 ± 0.005 | 0.648 ± 0.006 | 0.157 | 0.157 | 5 | 5 | 1.000 ± 0.000 | 0 |
| Phi-4 | zero-shot | 0.745 ± 0.012 | 0.722 ± 0.016 | 0.744 ± 0.013 | 0.229 | 0.206 | 5 | 5 | 0.970 ± 0.010 | 106 |
|  | zero-shot-cot | 0.706 ± 0.003 | 0.700 ± 0.002 | 0.696 ± 0.004 | 0.190 | 0.184 | 5 | 5 | 0.992 ± 0.003 | 29 |
|  | one-shot-cot | 0.733 ± 0.010 | 0.730 ± 0.010 | 0.730 ± 0.010 | 0.217 | 0.214 | 5 | 5 | 0.995 ± 0.001 | 16 |
| Qwen3.5 27B | zero-shot | 0.692 ± 0.001 | 0.691 ± 0.001 | 0.674 ± 0.001 | 0.176 | 0.175 | 5 | 5 | 0.998 ± 0.001 | 7 |
|  | zero-shot-cot | 0.653 ± 0.004 | 0.602 ± 0.005 | 0.598 ± 0.006 | 0.136 | 0.086 | 5 | 5 | 0.923 ± 0.004 | 269 |
|  | one-shot-cot | 0.648 ± 0.001 | 0.647 ± 0.002 | 0.610 ± 0.002 | 0.132 | 0.131 | 5 | 5 | 0.999 ± 0.001 | 4 |

Supplementary, Dreaddit per-class (`tables/rq2_dreaddit_per_class.csv`, per-class metrics as frozen in `cell_metrics.json`, five-run mean ± SD):

| Model | Strategy | Recall (0 = not stressed) | F1 (0) | Recall (1 = stressed) | F1 (1) | Predicted share of 1 |
|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot | 0.947 ± 0.003 | 0.752 ± 0.002 | 0.448 ± 0.008 | 0.597 ± 0.007 | 0.254 ± 0.005 |
|  | zero-shot-cot | 0.953 ± 0.005 | 0.743 ± 0.001 | 0.405 ± 0.004 | 0.558 ± 0.002 | 0.228 ± 0.004 |
|  | one-shot-cot | 0.956 ± 0.002 | 0.744 ± 0.004 | 0.404 ± 0.012 | 0.558 ± 0.012 | 0.227 ± 0.006 |
| Llama 4 Scout | zero-shot | 0.800 ± 0.008 | 0.763 ± 0.005 | 0.705 ± 0.009 | 0.740 ± 0.006 | 0.453 ± 0.007 |
|  | zero-shot-cot | 0.834 ± 0.008 | 0.763 ± 0.004 | 0.656 ± 0.011 | 0.721 ± 0.006 | 0.414 ± 0.009 |
|  | one-shot-cot | 0.827 ± 0.005 | 0.766 ± 0.004 | 0.679 ± 0.008 | 0.736 ± 0.005 | 0.430 ± 0.005 |
| Mistral Small 4 | zero-shot | 0.949 ± 0.003 | 0.749 ± 0.002 | 0.431 ± 0.007 | 0.583 ± 0.006 | 0.244 ± 0.004 |
|  | zero-shot-cot | 0.961 ± 0.007 | 0.736 ± 0.003 | 0.370 ± 0.005 | 0.526 ± 0.006 | 0.207 ± 0.004 |
|  | one-shot-cot | 0.958 ± 0.005 | 0.743 ± 0.004 | 0.398 ± 0.008 | 0.553 ± 0.009 | 0.223 ± 0.004 |
| Phi-4 | zero-shot | 0.817 ± 0.022 | 0.758 ± 0.012 | 0.675 ± 0.027 | 0.730 ± 0.015 | 0.434 ± 0.020 |
|  | zero-shot-cot | 0.897 ± 0.006 | 0.750 ± 0.002 | 0.520 ± 0.009 | 0.642 ± 0.006 | 0.315 ± 0.007 |
|  | one-shot-cot | 0.850 ± 0.018 | 0.759 ± 0.009 | 0.620 ± 0.019 | 0.702 ± 0.013 | 0.388 ± 0.016 |
| Qwen3.5 27B | zero-shot | 0.942 ± 0.001 | 0.751 ± 0.001 | 0.450 ± 0.002 | 0.597 ± 0.002 | 0.257 ± 0.002 |
|  | zero-shot-cot | 0.965 ± 0.001 | 0.746 ± 0.002 | 0.302 ± 0.009 | 0.451 ± 0.011 | 0.161 ± 0.004 |
|  | one-shot-cot | 0.974 ± 0.000 | 0.732 ± 0.001 | 0.332 ± 0.003 | 0.489 ± 0.003 | 0.181 ± 0.002 |

### RQ2 · GoEmotions (majority baseline 0.782; Δ = five-run mean − baseline)

Source: `tables/rq2_goemotions.csv`. Baseline from the frozen dataset manifest, 487/623.

| Model | Strategy | Acc. (cond.) | Acc. (eff.) | Macro-F1 | Δ cond. − base | Δ eff. − base | Runs > base (cond.) | Runs > base (eff.) | Evaluability | Model-invalid (Σ5) |
|---|---|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot | 0.820 ± 0.004 | 0.820 ± 0.004 | 0.593 ± 0.007 | 0.038 | 0.038 | 5 | 5 | 1.000 ± 0.000 | 0 |
|  | zero-shot-cot | 0.817 ± 0.004 | 0.817 ± 0.004 | 0.583 ± 0.008 | 0.036 | 0.036 | 5 | 5 | 1.000 ± 0.000 | 0 |
|  | one-shot-cot | 0.815 ± 0.004 | 0.813 ± 0.003 | 0.585 ± 0.005 | 0.033 | 0.031 | 5 | 5 | 0.998 ± 0.003 | 7 |
| Llama 4 Scout | zero-shot | 0.727 ± 0.007 | 0.700 ± 0.008 | 0.520 ± 0.017 | -0.055 | -0.081 | 0 | 0 | 0.964 ± 0.004 | 113 |
|  | zero-shot-cot | 0.728 ± 0.010 | 0.683 ± 0.009 | 0.530 ± 0.013 | -0.054 | -0.099 | 0 | 0 | 0.938 ± 0.002 | 193 |
|  | one-shot-cot | 0.767 ± 0.008 | 0.732 ± 0.009 | 0.544 ± 0.013 | -0.015 | -0.050 | 0 | 0 | 0.954 ± 0.002 | 143 |
| Mistral Small 4 | zero-shot | 0.770 ± 0.008 | 0.766 ± 0.005 | 0.561 ± 0.011 | -0.012 | -0.016 | 0 | 0 | 0.995 ± 0.003 | 17 |
|  | zero-shot-cot | 0.746 ± 0.007 | 0.741 ± 0.008 | 0.536 ± 0.010 | -0.036 | -0.041 | 0 | 0 | 0.994 ± 0.001 | 19 |
|  | one-shot-cot | 0.786 ± 0.005 | 0.783 ± 0.005 | 0.594 ± 0.008 | 0.004 | 0.001 | 4 | 3 | 0.996 ± 0.002 | 12 |
| Phi-4 | zero-shot | 0.784 ± 0.008 | 0.736 ± 0.016 | 0.534 ± 0.016 | 0.003 | -0.045 | 3 | 0 | 0.939 ± 0.015 | 191 |
|  | zero-shot-cot | 0.809 ± 0.003 | 0.762 ± 0.009 | 0.563 ± 0.011 | 0.028 | -0.020 | 5 | 0 | 0.941 ± 0.014 | 183 |
|  | one-shot-cot | 0.801 ± 0.004 | 0.673 ± 0.126 | 0.541 ± 0.049 | 0.019 | -0.109 | 5 | 0 | 0.840 ± 0.154 | 499 |
| Qwen3.5 27B | zero-shot | 0.786 ± 0.001 | 0.786 ± 0.001 | 0.572 ± 0.007 | 0.004 | 0.004 | 5 | 5 | 1.000 ± 0.000 | 0 |
|  | zero-shot-cot | 0.790 ± 0.002 | 0.790 ± 0.002 | 0.579 ± 0.006 | 0.008 | 0.008 | 5 | 5 | 1.000 ± 0.000 | 0 |
|  | one-shot-cot | 0.773 ± 0.000 | 0.770 ± 0.000 | 0.567 ± 0.000 | -0.009 | -0.012 | 0 | 0 | 0.997 ± 0.000 | 10 |

Supplementary, GoEmotions per-class recall and non_distress prediction share (`tables/rq2_goemotions_per_class.csv`; F1 and all predicted shares are in the CSV):

| Model | Strategy | anxiety recall | fear recall | sadness recall | frustration recall | non_distress recall | non_distress predicted share |
|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot | 0.667 ± 0.000 | 0.600 ± 0.000 | 0.242 ± 0.000 | 0.294 ± 0.016 | 0.955 ± 0.003 | 0.890 ± 0.001 |
|  | zero-shot-cot | 0.667 ± 0.000 | 0.600 ± 0.000 | 0.242 ± 0.000 | 0.247 ± 0.015 | 0.960 ± 0.003 | 0.901 ± 0.002 |
|  | one-shot-cot | 0.667 ± 0.000 | 0.600 ± 0.000 | 0.261 ± 0.017 | 0.280 ± 0.022 | 0.950 ± 0.004 | 0.886 ± 0.001 |
| Llama 4 Scout | zero-shot | 0.767 ± 0.094 | 0.731 ± 0.078 | 0.462 ± 0.009 | 0.397 ± 0.024 | 0.800 ± 0.005 | 0.716 ± 0.003 |
|  | zero-shot-cot | 0.727 ± 0.116 | 0.705 ± 0.012 | 0.455 ± 0.034 | 0.405 ± 0.021 | 0.804 ± 0.009 | 0.719 ± 0.009 |
|  | one-shot-cot | 0.820 ± 0.018 | 0.707 ± 0.037 | 0.432 ± 0.018 | 0.275 ± 0.019 | 0.877 ± 0.007 | 0.801 ± 0.007 |
| Mistral Small 4 | zero-shot | 0.700 ± 0.075 | 0.747 ± 0.030 | 0.364 ± 0.000 | 0.452 ± 0.028 | 0.852 ± 0.008 | 0.766 ± 0.008 |
|  | zero-shot-cot | 0.733 ± 0.091 | 0.787 ± 0.030 | 0.358 ± 0.014 | 0.469 ± 0.017 | 0.817 ± 0.008 | 0.729 ± 0.005 |
|  | one-shot-cot | 0.667 ± 0.000 | 0.800 ± 0.000 | 0.339 ± 0.025 | 0.395 ± 0.017 | 0.883 ± 0.004 | 0.800 ± 0.003 |
| Phi-4 | zero-shot | 0.670 ± 0.053 | 0.705 ± 0.051 | 0.308 ± 0.020 | 0.144 ± 0.034 | 0.929 ± 0.012 | 0.878 ± 0.010 |
|  | zero-shot-cot | 0.720 ± 0.073 | 0.734 ± 0.042 | 0.321 ± 0.044 | 0.155 ± 0.043 | 0.954 ± 0.004 | 0.895 ± 0.008 |
|  | one-shot-cot | 0.760 ± 0.146 | 0.597 ± 0.107 | 0.310 ± 0.055 | 0.124 ± 0.103 | 0.958 ± 0.019 | 0.902 ± 0.041 |
| Qwen3.5 27B | zero-shot | 0.667 ± 0.000 | 0.653 ± 0.030 | 0.248 ± 0.014 | 0.358 ± 0.000 | 0.899 ± 0.000 | 0.826 ± 0.001 |
|  | zero-shot-cot | 0.667 ± 0.000 | 0.613 ± 0.030 | 0.273 ± 0.000 | 0.378 ± 0.011 | 0.900 ± 0.001 | 0.824 ± 0.002 |
|  | one-shot-cot | 0.667 ± 0.000 | 0.667 ± 0.000 | 0.273 ± 0.000 | 0.457 ± 0.000 | 0.864 ± 0.000 | 0.779 ± 0.000 |

### RQ2 · Plain factual interpretation

**Dreaddit, measured**

- Across the 15 configurations:
  - conditional accuracy 0.648–0.752;
  - effective accuracy 0.602–0.750;
  - macro-F1 0.598–0.752.
- Every configuration exceeds the 0.516 majority baseline on both accuracy measures in all 5 runs.
- The attributable set is close to balanced: 355 stressed / 344 not stressed.
  - So accuracy and macro-F1 track each other.
  - Where they separate (Gemma, Mistral, Qwen: macro-F1 below conditional accuracy in every cell), the per-class table shows why: those models recall class 0 far better than class 1.
- A constant "stressed" predictor on the attributable set would have macro-F1 0.337, as a derived reference (not a frozen result).

**GoEmotions, measured**

- Across the 15 configurations:
  - conditional accuracy 0.727–0.820;
  - effective accuracy 0.673–0.820;
  - macro-F1 0.520–0.594.
- **Several configurations are at or below the 0.782 majority baseline.** These are reported, not hidden:
  - 6 of 15 on mean conditional accuracy;
  - 9 of 15 on mean effective accuracy.
- Only Gemma (all three strategies) and Qwen (zero-shot and zero-shot-CoT) exceed the baseline on both measures in all 5 runs.
- Mistral one-shot-CoT is marginal: 4/5 runs above on conditional accuracy, 3/5 on effective.
- Phi-4's effective accuracy is below the baseline in every run under all three strategies. Its conditional accuracy is above the baseline in 5/5 runs (zero-shot-CoT, one-shot-CoT) and 3/5 runs (zero-shot).

**Why accuracy and macro-F1 diverge on GoEmotions (class imbalance)**

**Measured**

- The attributable set has 487 non_distress (78.3%), 81 frustration, 33 sadness, 15 fear and **6 anxiety** items.
- A constant non_distress predictor would reach accuracy 0.782 but macro-F1 0.176 and macro-recall 0.200 (derived reference).
- Accuracy is therefore dominated by the majority class. Macro-F1 weights each of the five classes equally, so the rare distress classes count as much as non_distress.
- Gemma predicts non_distress for 0.886–0.901 of its valid outputs, against a true share of 0.783.
  - This gives non_distress recall 0.950–0.960 and the highest accuracies.
  - But sadness recall is 0.242–0.261 and frustration recall 0.247–0.294.
- Llama 4 Scout predicts non_distress less often (0.716–0.801).
  - Its sadness recall is higher (0.432–0.462).
  - Its accuracy is lower.

**Interpretation**

- High GoEmotions accuracy here mostly reflects agreement on non_distress. It is not evidence of distress-class detection.
- No configuration's macro-F1 exceeds 0.594. Every configuration has macro-F1 far above the constant predictor's 0.176. So the models do separate distress classes, but only partially.
- The anxiety class has 6 items, so one item moves anxiety recall by 1/6 (≈ 0.167). Per-class anxiety values are very coarse.
- Under the frozen mapping, a non_distress prediction arises from an empty emotion list (`ok_empty_list`).

**Conditional vs effective accuracy**

- Conditional accuracy ignores invalid outputs; effective accuracy counts them as wrong.
- They differ most for Phi-4 (GoEmotions), Llama 4 Scout (both datasets) and Qwen zero-shot-CoT (Dreaddit). Reporting only conditional accuracy would favour models that fail to produce a usable answer more often.

---

## RQ3: Which prompting strategy is the most efficient?

### RQ3 · Latency-data audit (from saved records only)

All 11 source runs (the 10 grid runs plus the pub_013 replacement run)' `raw/attempts.jsonl` and `raw/index.jsonl` were sha256-verified against the frozen grid manifest before reading (all matched). The extraction script is `code/rq3_latency_extract.py`, with outputs in `rq3_extract_summary.json`.

**1. Latency fields that exist** (in 100% of attempt records unless stated):

| Field | Unit | Meaning (from code) |
|---|---|---|
| `latency_ms` | ms (float) | Runner client wall-clock (`time.perf_counter`) around the whole HTTP POST to Express `/api/workflow/evaluate`. |
| `server_latency_ms` | ms (int) | Express `Date.now() − requestStart`, from request receipt to just before the response is sent. Covers workflow creation, start, polling and result extraction. |
| `response_body.metadata.latency_ms` | ms (int) | Same value as `server_latency_ms`. Present only when a response body parsed (101,066 of 102,137 attempts). |
| `mastra_poll_interval_ms` | ms | Effective Mastra poll cadence, verified at preflight. **3000 in every run.** |
| `timestamp_utc` | ISO time | When the attempt was written. |
| `token_usage` | tokens | Not a latency. The server takes the first `tokenUsage` object it finds in the workflow output, so it is not documented as a per-assessment total. Missing for 2,134 LLM-served terminal attempts. Not used. |

**2. What is not recorded.**

- No per-agent timing (emotion, symptom, context, referral, report).
- No phase timings. The Experimental Setup document's `preAssessMs`, `mastraMs` and `groundingMs` are absent.
- No `server_step_timings`, although it was planned in the runner design (`parallelMs`, `reportMs`, `totalMs`).
- No provider-side processing time and no time-to-first-token.
- No host or machine identifier, and no concurrency level.

**3. Completeness.**

- All 100,350 authoritative (terminal) attempts have `latency_ms` and `server_latency_ms`. 0 are missing.
- 99,075 are LLM-served. 1,275 are safety intercepts: they short-circuit before any agent call (median about 7 ms), so they are excluded from the latency statistics and counted separately.

**Comparability**

- **Poll quantisation.** 99,049 of 99,075 (99.97%) LLM-served terminal latencies lie within 0.5 s of a multiple of 3 s.
  - Client minus server is a median of about 6 ms (p99 about 17 ms), so the harness adds almost nothing.
  - The server sleeps 3 s before each status check, so each value is essentially (number of polls × 3 s). The workflow actually finished somewhere in the preceding ≈ 3 s.
  - Measurement resolution is therefore 3 s, and medians sit on the lattice. For example, Qwen's Dreaddit medians are 9.08 / 9.08 / 9.07 s across strategies.
- **Execution order.** The runner loops model → strategy → run → sample. Within each model × dataset, the three strategies ran in consecutive time blocks (zero-shot first, one-shot-CoT last). **Strategy is confounded with time**: provider load and time of day. It is also plausibly confounded with local Mastra storage growth, which was not measured.
- **Machine.**
  - Runs were executed on two machines. This is inferred from where the run folders are stored (Aya's repo vs the USB copied from Heba's laptop), because `experiment.json` records no host.
  - Within each model × dataset, all strategies ran on the same machine. The one exception is Gemma Dreaddit one-shot-CoT run 5 (pub_013, Aya, 2026-09-19/20), whereas runs 1–4 ran on Heba's machine on 2026-09-16.
  - Comparisons across models also cross machines and upstream providers.
- **Concurrent load.** 10,072 of 10,725 Llama 4 Scout Dreaddit terminal attempts were recorded while another run (pub_004, Gemma via DeepInfra, not part of the grid) was active on the same machine.
  - By strategy: zero-shot 82%, zero-shot-CoT 100%, one-shot-CoT 100%.
  - No other grid cell overlaps another run on the same machine.
- **Retries.** The latency used is that of the terminal (successful) attempt. Time spent in earlier failed attempts and backoff is not included. The number of retried assessments is shown per row.
- **Run-to-run drift.** This is large for some models. For example, Gemma Dreaddit one-shot-CoT has per-run mean latencies of 16.88, 20.29, 14.37, 10.09 and 14.08 s.

**4. Can total system response time be calculated?** **Yes, descriptively.** It is the end-to-end wall-clock per assessment of the AnxioSense evaluation path, from both the client and the server side, complete for every record. Limits:

- the 3 s resolution;
- the order, machine and concurrency confounds above.

It covers the `/api/workflow/evaluate` path (social-media mode, no GAD-7), not the user-facing `/run` path.

**5. Can individual-agent latency be calculated?** **No.** No per-agent or per-phase timing was stored, and it cannot be derived from a single end-to-end number, because four agents run in parallel before the report step.

- Mastra's own observability store may contain per-span timings keyed by the recorded `mastra_run_id`.
- That store is not part of the frozen experiment records, is split across two machines, and was **not** inspected or used here.

**Verdict on RQ3 support.** The planned analysis is supported **only partially**:

- *Total system response time*: reportable descriptively, with the caveats above.
- *Individual-agent processing latency*: not answerable from the recorded evidence.

### RQ3 · Dreaddit latency by model × strategy (LLM-served terminal attempts; 5-run mean ± SD of per-run statistics)

Source: `tables/rq3_dreaddit_latency.csv`, built from `rq3_terminal_latency_records.jsonl`, which was extracted from hash-verified raw files. Client = `latency_ms`, server = `server_latency_ms`. Per run: mean, median and p90 (nearest rank). The five-run value is the mean ± sample SD of the five per-run statistics. Models are not pooled.

\*Machine is inferred from where the run folder is stored. "Share during other run" = fraction of the cell's terminal attempts recorded while another run was active on the same machine.

| Model | Strategy | Client mean (s) | Client median (s) | Client p90 (s) | Server mean (s) | n (Σ5) | Retried (Σ5) | Machine* | Share during other run | Executed (UTC) |
|---|---|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot | 15.07 ± 2.73 | 12.06 ± 2.13 | 26.53 ± 5.80 | 15.07 ± 2.73 | 3495 | 10 | Heba | 0.00 | 2026-09-15T04:42 → 2026-09-17T02:06 |
|  | zero-shot-cot | 13.10 ± 1.97 | 10.26 ± 1.65 | 22.92 ± 4.03 | 13.09 ± 1.97 | 3495 | 10 | Heba | 0.00 | 2026-09-15T20:12 → 2026-09-16T09:47 |
|  | one-shot-cot | 15.14 ± 3.77 | 12.68 ± 3.91 | 26.51 ± 7.79 | 15.14 ± 3.77 | 3495 | 34 | Aya+Heba | 0.00 | 2026-09-16T09:47 → 2026-09-20T02:48 |
| Llama 4 Scout | zero-shot | 12.46 ± 0.88 | 12.07 ± 0.01 | 17.53 ± 2.49 | 12.46 ± 0.88 | 3495 | 4 | Heba | 0.82 | 2026-09-06T15:19 → 2026-09-07T03:57 |
|  | zero-shot-cot | 14.08 ± 2.11 | 12.70 ± 1.38 | 19.92 ± 4.02 | 14.08 ± 2.11 | 3495 | 9 | Heba | 1.00 | 2026-09-07T03:58 → 2026-09-07T22:33 |
|  | one-shot-cot | 10.23 ± 0.64 | 9.67 ± 1.34 | 13.32 ± 1.61 | 10.23 ± 0.64 | 3495 | 2 | Heba | 1.00 | 2026-09-07T22:33 → 2026-09-08T09:01 |
| Mistral Small 4 | zero-shot | 5.36 ± 0.03 | 6.06 ± 0.00 | 6.07 ± 0.00 | 5.35 ± 0.03 | 3495 | 3 | Aya | 0.00 | 2026-09-06T13:13 → 2026-09-06T18:56 |
|  | zero-shot-cot | 5.25 ± 0.11 | 6.06 ± 0.01 | 6.07 ± 0.01 | 5.24 ± 0.11 | 3495 | 0 | Aya | 0.00 | 2026-09-06T18:56 → 2026-09-07T00:33 |
|  | one-shot-cot | 4.89 ± 0.12 | 6.04 ± 0.00 | 6.05 ± 0.00 | 4.88 ± 0.12 | 3495 | 0 | Aya | 0.00 | 2026-09-07T00:33 → 2026-09-07T05:48 |
| Phi-4 | zero-shot | 12.91 ± 1.36 | 10.88 ± 1.64 | 18.10 ± 3.67 | 12.90 ± 1.36 | 3495 | 10 | Aya | 0.00 | 2026-09-07T14:40 → 2026-09-08T03:57 |
|  | zero-shot-cot | 12.86 ± 1.19 | 12.08 ± 0.01 | 16.30 ± 2.68 | 12.85 ± 1.19 | 3495 | 0 | Aya | 0.00 | 2026-09-08T03:57 → 2026-09-08T16:56 |
|  | one-shot-cot | 10.13 ± 1.84 | 9.65 ± 1.35 | 12.68 ± 3.29 | 10.12 ± 1.84 | 3495 | 3 | Aya | 0.00 | 2026-09-08T16:56 → 2026-09-13T16:53 |
| Qwen3.5 27B | zero-shot | 9.05 ± 0.27 | 9.08 ± 0.00 | 9.70 ± 1.34 | 9.04 ± 0.27 | 3495 | 0 | Aya | 0.00 | 2026-09-05T03:25 → 2026-09-05T12:43 |
|  | zero-shot-cot | 8.67 ± 0.24 | 9.08 ± 0.00 | 9.11 ± 0.01 | 8.66 ± 0.24 | 3495 | 0 | Aya | 0.00 | 2026-09-05T12:43 → 2026-09-05T21:38 |
|  | one-shot-cot | 8.40 ± 0.45 | 9.07 ± 0.01 | 9.11 ± 0.02 | 8.39 ± 0.45 | 3495 | 1 | Aya | 0.00 | 2026-09-05T21:38 → 2026-09-06T06:18 |

### RQ3 · GoEmotions latency by model × strategy

Source: `tables/rq3_goemotions_latency.csv` (same definitions).

| Model | Strategy | Client mean (s) | Client median (s) | Client p90 (s) | Server mean (s) | n (Σ5) | Retried (Σ5) | Machine* | Share during other run | Executed (UTC) |
|---|---|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot | 11.54 ± 1.38 | 7.88 ± 1.65 | 19.91 ± 2.70 | 11.53 ± 1.38 | 3110 | 9 | Aya | 0.00 | 2026-09-15T16:16 → 2026-09-16T02:54 |
|  | zero-shot-cot | 14.17 ± 3.54 | 11.48 ± 3.30 | 24.14 ± 6.74 | 14.16 ± 3.54 | 3110 | 21 | Aya | 0.00 | 2026-09-16T02:54 → 2026-09-17T02:02 |
|  | one-shot-cot | 10.09 ± 2.75 | 7.86 ± 2.69 | 16.29 ± 6.59 | 10.09 ± 2.75 | 3110 | 22 | Aya | 0.00 | 2026-09-16T16:10 → 2026-09-17T04:15 |
| Llama 4 Scout | zero-shot | 10.78 ± 1.26 | 9.07 ± 2.13 | 18.11 ± 2.12 | 10.77 ± 1.26 | 3110 | 22 | Aya | 0.00 | 2026-09-11T17:39 → 2026-09-13T16:18 |
|  | zero-shot-cot | 11.02 ± 2.20 | 9.07 ± 3.01 | 19.32 ± 3.45 | 11.01 ± 2.20 | 3110 | 28 | Aya | 0.00 | 2026-09-12T04:16 → 2026-09-13T16:18 |
|  | one-shot-cot | 10.00 ± 1.34 | 8.46 ± 1.34 | 14.49 ± 2.52 | 9.99 ± 1.34 | 3110 | 31 | Aya | 0.00 | 2026-09-12T17:05 → 2026-09-13T16:12 |
| Mistral Small 4 | zero-shot | 3.98 ± 0.48 | 3.05 ± 0.01 | 6.06 ± 0.01 | 3.97 ± 0.48 | 3110 | 0 | Aya | 0.00 | 2026-09-09T18:02 → 2026-09-09T21:55 |
|  | zero-shot-cot | 3.43 ± 0.11 | 3.04 ± 0.00 | 5.44 ± 1.34 | 3.42 ± 0.11 | 3110 | 0 | Aya | 0.00 | 2026-09-09T21:55 → 2026-09-10T01:19 |
|  | one-shot-cot | 3.32 ± 0.16 | 3.04 ± 0.00 | 3.64 ± 1.34 | 3.31 ± 0.16 | 3110 | 1 | Aya | 0.00 | 2026-09-10T01:19 → 2026-09-11T17:13 |
| Phi-4 | zero-shot | 13.07 ± 0.35 | 11.47 ± 1.30 | 18.07 ± 0.00 | 13.06 ± 0.35 | 3110 | 17 | Heba | 0.00 | 2026-09-10T18:03 → 2026-09-11T06:23 |
|  | zero-shot-cot | 13.09 ± 1.89 | 9.65 ± 1.35 | 21.69 ± 5.39 | 13.08 ± 1.89 | 3110 | 34 | Heba | 0.00 | 2026-09-11T06:24 → 2026-09-12T22:22 |
|  | one-shot-cot | 10.63 ± 2.23 | 9.65 ± 1.35 | 17.48 ± 6.52 | 10.63 ± 2.23 | 3110 | 5 | Heba | 0.00 | 2026-09-11T19:15 → 2026-09-12T05:03 |
| Qwen3.5 27B | zero-shot | 7.27 ± 0.56 | 6.04 ± 0.00 | 9.65 ± 1.34 | 7.27 ± 0.56 | 3110 | 3 | Heba | 0.00 | 2026-09-09T19:24 → 2026-09-10T02:10 |
|  | zero-shot-cot | 7.32 ± 0.37 | 6.04 ± 0.00 | 9.05 ± 0.00 | 7.32 ± 0.37 | 3110 | 0 | Heba | 0.00 | 2026-09-10T02:10 → 2026-09-10T08:56 |
|  | one-shot-cot | 7.32 ± 0.33 | 6.04 ± 0.00 | 9.05 ± 0.01 | 7.32 ± 0.33 | 3110 | 9 | Heba | 0.00 | 2026-09-10T08:56 → 2026-09-10T17:08 |

### RQ3 · Plain factual interpretation

**Measured**

- **Differences between models are much larger than differences between strategies.**
  - Mistral Small 4 has mean client latency 4.89–5.36 s on Dreaddit and 3.32–3.98 s on GoEmotions.
  - Gemma 4 31B has 13.10–15.14 s on Dreaddit and 10.09–14.17 s on GoEmotions.
- **One-shot-CoT had the lowest five-run mean latency for 4 of 5 models on each dataset.**
  - Dreaddit: all models except Gemma, where zero-shot-CoT was lowest at 13.10 s.
  - GoEmotions: all models except Qwen, where zero-shot was lowest at 7.27 s against 7.32 s for both CoT strategies.
- **Several of these differences are within the measurement's limits.**
  - For Mistral and Qwen they are below the 3 s resolution. Their medians are identical across strategies: Mistral 6.04–6.06 s on Dreaddit and 3.04–3.05 s on GoEmotions; Qwen 9.07–9.08 s and 6.04 s.
  - For Gemma, Llama and Phi-4 they are of the same order as the run-to-run SDs (up to ± 3.77 s).
- In each run's initial dispatch, the one-shot-CoT block was executed **last** within its model. Later resume/retry invocations re-dispatched a small number of items out of order, and Gemma Dreaddit one-shot-CoT run 5 was run days later on the other machine. So the strategy ordering cannot be separated from time effects.
- Server and client means agree to within about 0.01 s everywhere.

**Interpretation**

- The stored records do not show that any prompting strategy makes the system faster in a way that can be separated from:
  - the 3 s poll quantisation;
  - execution order and time;
  - machine differences;
  - for Llama Dreaddit, concurrent load.
- The consistent direction (one-shot-CoT lowest in 8 of 10 model × dataset pairs) is a descriptive observation only. It is not an efficiency conclusion. A controlled comparison would need randomised or interleaved strategy order, finer timing and per-agent timing.
- **Performance and efficiency are separate results.** The highest-accuracy strategy is not automatically the most efficient, and the reverse holds too. For example, Qwen one-shot-CoT on Dreaddit has Qwen's lowest mean latency (8.40 s) and its lowest conditional accuracy (0.648).
- The setup document's own RQ3 wording ("minimises false positive symptom extractions while maintaining recall") is a different, accuracy-type question. Symptom extraction was not scored in this grid.

---

## What these results do NOT establish yet

- **No inferential statistics.** No significance test has been performed. None of the differences above may be described as statistically significant, and "higher" and "lower" are descriptive only.
  - The five-run SDs reflect variation between repeated runs on the **same items**. They are not item-sampling uncertainty or confidence intervals.
  - A near-zero SD (e.g. Qwen) shows the model was consistent across runs, not that its accuracy is precisely estimated.
- **No single overall AnxioSense accuracy.** None is pre-specified, and none was produced. The older protocol's "top LLM, 1S-CoT" rule is a selection on test data, and its criterion (symptom extraction) was not measured.
- **No clinical claim.**
  - Dreaddit measures stress vs non-stress through a referral-level proxy.
  - It does not validate anxiety detection or the GoEmotions `anxiety` class.
  - GoEmotions has only 6 anxiety items.
  - Both datasets are Reddit text, not a clinical population.
- **No per-agent efficiency result.** Agent-level and phase latency were not recorded. Total response time is 3 s-quantised and confounded with execution order, machine and, for Llama Dreaddit, concurrent load.
- **Results are conditional on the frozen methodology.** Under the frozen parser and policy:
  - `{}` outputs, malformed JSON, refusals and OOV labels are model-invalid;
  - non_distress arises from empty emotion lists;
  - Dreaddit outputs whose readable `risk_level` sits inside unparseable text stay invalid;
  - Phi-4 GoEmotions one-shot-CoT run 5 is included.

  Alternative policies were neither applied nor evaluated here. The open items in `descriptive_2026-09-21/ISSUES_FOR_AUDIT.md` remain open.
- **Serving configuration.** Results apply to the model/provider routes used, e.g. Gemma served by CoreWeave at fp4. They may not transfer to other serving setups.
- **Protocol items not covered.** Cohen's weighted κ, per-agent/phase efficiency metrics, and RQ4/RQ5 measures listed in the Experimental Setup document are not addressed by these tables.

---

## Files in this folder

- `code/rq12_tables.py`: RQ1/RQ2 recomputation, cross-check and tables. It aborts on any conflict.
- `code/rq3_latency_extract.py`: hash-verified, read-only latency audit, concurrency check and per-record latency extract.
- `code/rq3_latency_tables.py`: RQ3 tables.
- `code/build_report.py`: renders this report from the CSVs and checks every quoted number against them.
- `tables/*.csv`: all presented tables.
- `rq12_full_precision.json`: exact rational values and 60-digit SDs.
- `rq12_crosscheck.json`, `rq1_metric_ranks.json`.
- `rq3_extract_summary.json`, `rq3_terminal_latency_records.jsonl`, `rq3_latency_per_cell.json`, `rq3_strategy_means_by_model.json`.
- `report_number_check.json`, `freeze_check.txt`.
