# RQ3 statistical analysis plan — addendum

**Addendum to** `results/inferential_2026-09-21/STATISTICAL_ANALYSIS_PLAN.md` (frozen 2026-09-21,
"APPROVED 2026-09-21. Written before any test was run.").

**Status: POST-HOC / EXPLORATORY.** The estimation procedure was pre-specified and frozen on 2026-09-21 for
RQ1 and RQ2 and is applied here unchanged. The RQ3 strategy contrasts were declared in
`results/rq3_inference_design_2026-09-25/RQ3_INFERENCE_DESIGN.md` § 8 and in this addendum **before any RQ3
test was run**, but **after** the descriptive strategy results were known. This addendum is therefore a
pre-analysis freeze, not a pre-registration of an untouched dataset, and the analysis must be labelled
*post-hoc / exploratory* wherever it is reported.

**Written and frozen before execution.** This file, the pre-check record (`precheck.json`,
`INPUT_HASHES.sha256`) and the analysis code (`code/01_run_rq3_strategy_inference.py`) are hashed together
into `PREREGISTRATION_FREEZE.json` with a UTC timestamp. The analysis was executed only after that file was
written. No strategy-comparison p-value was computed, inspected or used to alter any element below.

---

## 1. Question

**RQ3 (as analysed here).** Within a given model and dataset, how does the prompting strategy — zero-shot,
zero-shot chain-of-thought, one-shot chain-of-thought — affect classification performance?

This is the **classification-quality** reading of RQ3. It is **not** the latency/efficiency reading. The
frozen plan's refusal of RQ3 inference (§ C: *"RQ3. Descriptive only; no inferential latency analysis"*;
§ E: *"RQ3. No inference."*) was reasoned entirely about latency confounds — 3-second poll quantisation,
fixed strategy order, machine, provider, time of day, concurrent load, no per-agent timing. **That refusal
stands unchanged for latency.** Nothing in this addendum authorises an inferential claim about response time.

---

## 2. Pre-conditions, verified and recorded before freezing

Both were verified by `code/00_precheck.py`; the full record is in `precheck.json` (38/38 checks passed).

| Pre-condition | Result |
|---|---|
| One full item set per dataset across all 75 cells | Dreaddit 1 set of 715; GoEmotions 1 set of 623 |
| One safety-intercept set per dataset across all 75 cells | Dreaddit 16; GoEmotions 1 — identical in every cell, therefore neutral to a strategy contrast |
| **Model × run groups in which the three strategy arms differ in their attributable item set** | **Dreaddit 0 of 25; GoEmotions 0 of 25** |
| Every arm scored on the full attributable pool | Dreaddit n = 699; GoEmotions n = 622 |
| Attributable item list reproduces the frozen inferential item hash | `50042e17…` / `0fe806ef…` — identical to `inferential_2026-09-21/analysis_manifest.json` |
| Five runs retained as a per-item vector | Arrays are `(item × strategy × run)` = `(699, 3, 5)` and `(622, 3, 5)` for every model; the run axis is never folded into the item axis |
| Independent units for a strategy contrast | **699 / 622 items** — not 3,495 / 3,110 item-run records, and not 5 runs |

**The strategy arms are therefore exactly paired by item**, and the pairing is complete: no item is missing
from any arm, so no complete-case deletion occurs anywhere in the primary analysis.

---

## 3. Design (fixed; no element may change after this file is frozen)

| Element | Specification |
|---|---|
| **Estimand** | Within one dataset and one model, the difference between two prompting strategies in the frozen five-run metric, on the fixed attributable item pool (699 / 622), conditional on the five observed runs. |
| **Statistical unit** | The benchmark item, carrying all of its five runs under each strategy. n = 699 (Dreaddit), 622 (GoEmotions). |
| **Primary outcome** | Effective accuracy: correct ÷ attributable, per run, averaged over the five runs. A model-invalid output is **incorrect**. |
| **Co-primary outcome** | Macro-F1: unweighted mean of per-class F1 over the fixed label list (2 Dreaddit / 5 GoEmotions), per `MetricPolicy 1.0.0`, per run, averaged over the five runs. |
| **Secondary, descriptive only** | Conditional accuracy and evaluability: bootstrap CIs only, **no p-values, no Holm**, explicitly labelled as conditioning on each configuration's own valid predictions. |
| **Contrasts** | Three pairwise strategy contrasts, within model, within dataset: zero-shot vs zero-shot-CoT; zero-shot vs one-shot-CoT; zero-shot-CoT vs one-shot-CoT. |
| **Contrast count** | 3 pairs × 5 models × 2 metrics = **30 primary comparisons per dataset**, 60 in total. **All are reported**, significant or not. |
| **Treatment of the five runs** | Runs stay nested inside their item. Runs are never paired across strategies (run *k* of one arm is never matched to run *k* of another). Runs are never resampled. Runs are never treated as independent observations. |
| **Treatment of invalid outputs** | Kept exactly as frozen and counted as incorrect on the attributable denominator. **The primary analysis is not conditioned on valid outputs.** No repair, no rescoring, no deletion. |
| **Treatment of safety intercepts** | Excluded once from the item pool, as frozen; identical in every arm. |
| **Primary test — effective accuracy** | Paired item-level permutation. For each item, with probability ½ the **entire five-run outcome vector** of arm A is swapped with that of arm B; both arms' five-run metrics are recomputed on the swapped assignment. P = **10,000** swap sets per dataset. p = (1 + #{\|T\*\| ≥ \|T_obs\|}) / (1 + P). |
| **Primary test — Macro-F1** | The identical whole-item swap, but the statistic is **recomputed from the swapped confusion matrices**, not decomposed into per-item contributions. Macro-F1 is a dataset-level functional and has no per-item decomposition. No McNemar for Macro-F1. |
| **Confidence intervals** | Paired item-cluster bootstrap. B = **4,000**. Items resampled with replacement, each item carrying all of its configurations × five runs. **One shared index vector per dataset**, used by every configuration in that dataset. 95% percentile intervals, linear interpolation between order statistics. CIs reported on the difference and on each configuration. |
| **Correction** | Holm–Bonferroni, **within each dataset, across the 30 primary comparisons** (5 models × 3 strategy pairs × 2 metrics). |
| **Threshold** | α = 0.05 applied to the **Holm-adjusted** p-value, matching the frozen plan. |
| **Families** | `RQ3-primary-dreaddit` (30), `RQ3-primary-goemotions` (30), `RQ3-mcnemar-dreaddit` (15), `RQ3-mcnemar-goemotions` (15). |
| **Pooling** | **None.** No pooled strategy main effect across models, and no family spanning both datasets. |

### 3.1 Secondary test (declared here, before execution)

Exact McNemar on per-item **majority-vote effective correctness** (correct in ≥ 3 of 5 runs; 5 is odd, so
there are no ties), effective accuracy only, in its **own** Holm family of 15 per dataset. This mirrors
decision D2 of the frozen plan and provides a check with no Monte-Carlo component. It is **secondary**: it
cannot promote a non-significant primary result, and a disagreement between the two is reported as a
disagreement, not resolved in favour of either.

### 3.2 Random draws

The seed strings are **reused verbatim from the frozen 2026-09-21 analysis**:

- bootstrap: `20260921|<dataset>|bootstrap`
- permutation: `20260922|<dataset>|permutation`

Reason: identical draws make this package's configuration-level bootstrap CIs **bit-identical** to the frozen
`inferential_2026-09-21/tables/configuration_level_ci.csv`, which is a strong reproduction check and removes
any suspicion that a seed was chosen after seeing a result. The draws are independent of which pairs are
tested, so reuse introduces no bias; it does mean RQ3 and RQ1 share Monte-Carlo noise, which is stated as a
limitation. `code/00_precheck.py` verified before freezing that both draws reproduce the frozen SHA-256
digests exactly (`5aad14ca…`, `92a9304c…`, `14bbb591…`, `aaf61859…`).

### 3.3 What is deliberately NOT done

- No conditional-accuracy hypothesis test (denominators differ by arm; a complete-case strategy comparison
  would retain as few as 195 of 622 items for Phi-4 / GoEmotions, and precisely the items that model could
  parse).
- No pooled strategy main effect across models (it would average over large model × strategy interactions of
  opposite sign).
- No family spanning both datasets (different item pools, different tasks, different baselines).
- No latency or efficiency inference.
- No per-class inference on the GoEmotions `anxiety` class (n = 6).
- No mediation analysis. The paired evaluability change is reported as a **descriptive companion only**.
- No repair, rescoring, re-running or modification of any frozen artifact.

---

## 4. Reporting rules, fixed before execution

1. **All 30 primary comparisons per dataset are reported**, with observed difference, 95% CI, unadjusted p,
   Holm-adjusted p, and the significance decision — regardless of outcome. Reporting a subset would convert
   this from a disciplined post-hoc analysis into selective reporting.
2. Each row also carries the descriptive five-run mean ± SD for both arms, and the evaluability / invalid-output
   context for both arms.
3. A non-significant result is reported as **"not significant after Holm correction"**, never as evidence of
   no difference. For GoEmotions Macro-F1 in particular, the correct word for a null result is
   **inconclusive**: with class supports 487 / 81 / 33 / 15 / 6, one fifth of Macro-F1 rests on six items.
4. The number of bootstrap replicates containing no GoEmotions `anxiety` item is reported.
5. No causal claim about *why* a strategy changes behaviour. Strategy, prompt length and exemplar presence
   change together; nothing in this design separates them.
6. No claim that a strategy is globally best. The analysis supports within-model, within-dataset statements
   only.
7. The words **post-hoc** and **exploratory** appear in the report and in any paper text derived from it, and
   RQ1 / RQ2 remain labelled pre-specified confirmatory analyses so the distinction is visible.

---

## 5. Known limitations, stated before the results are seen

- **Post-hoc.** The contrasts were chosen after the descriptive results were known. No RQ3 p-value should be
  described as confirming a hypothesis.
- **Study-wide multiplicity is not controlled.** RQ1, RQ2 and RQ3 reuse the same items and configurations;
  Holm controls the family-wise error rate only within each declared family.
- **The intervals are conditional on the five observed runs.** They express item-sampling uncertainty, not
  "what would happen with a different set of runs". Run-to-run SD is reported separately.
- **Shared Monte-Carlo noise with RQ1** (deliberate, § 3.2).
- **GoEmotions Macro-F1 is underpowered** by construction of the benchmark subset.
- **Strategy arms ran in sequential blocks**, so strategy is confounded with time of day and provider load.
  This is harmless for a *paired item-level* contrast of accuracy only to the extent that the provider's
  behaviour did not differ systematically between blocks; it cannot be ruled out from these data and is a
  stated limitation, not a corrected confound.
- **`prompt_set_sha256` differs for one Gemma Dreaddit cell** (`one-shot-cot`, run 5, the `pub_013`
  replacement). All five per-agent prompt hashes are byte-identical to `pub_011`; the enclosing directory
  hash changed for unrelated reasons. Disclosed, not corrected.

---

## 6. Outputs

A new directory only: `results/rq3_strategy_inference_2026-09-25/`, containing this addendum, the freeze
record, input hashes, pre-check record, analysis code, full result tables, replicate files, validation and
report. **No existing package, frozen artifact, raw output, parser, config or prompt is modified.**
