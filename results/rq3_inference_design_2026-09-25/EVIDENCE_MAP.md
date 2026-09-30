# Evidence map — RQ3 inference design note

Every **VERIFIED FACT** in `RQ3_INFERENCE_DESIGN.md`, with the artifact it came from. Paths are relative to
`evaluation/publication_experiments/`. Line numbers refer to the files as read on 2026-09-25.

Read-only: this note and the design note were the only files created; nothing outside
`results/rq3_inference_design_2026-09-25/` was modified.

---

## A. Design and pairing

| # | Claim | Source | Location | Evidence |
|---|---|---|---|---|
| A1 | Exactly one item set per dataset across all 75 cells: Dreaddit 715, GoEmotions 623 | `results/descriptive_2026-09-21/authoritative_records.jsonl` | recomputed over 150 cells | 1 distinct sample set per dataset; set sizes 715 / 623 |
| A2 | Exactly one attributable item set per dataset: 699 / 622 | same | same | 1 distinct attributable set per dataset |
| A3 | The three strategies never differ in attributable item set within a model × run | same | same | 0 model × run groups with differing sets |
| A4 | The frozen plan already states the identical-item fact for **configurations**, which includes strategy | `results/inferential_2026-09-21/STATISTICAL_ANALYSIS_PLAN.md` | § 2, l. 38 | "Within a dataset, all 15 configurations (model × strategy) were scored on the identical 699 / 622 items." |
| A5 | Comparisons are item-paired | same | § 2, l. 39 | "A comparison of configuration A with configuration B is paired **by item**." |
| A6 | One config runs all three strategies, one dataset, fixed model pin and retry policy | `configs/pub_001_dreaddit_qwen.yaml` | `strategies:`, `datasets:`, `runs:`, `models:`, `retry:` | `strategies: [zero-shot, zero-shot-cot, one-shot-cot]`; `runs: 5`; one manifest; `pin_provider: Alibaba`; `enabled: true` for one model only |
| A7 | Config comment states the strategy scope explicitly | same | header comment | "strategies  all three frozen prompt sets: zero-shot, zero-shot-cot, one-shot-cot" |

## B. Prompt-set hash anomaly (checked and cleared)

| # | Claim | Source | Location | Evidence |
|---|---|---|---|---|
| B1 | 29 of 30 dataset × model × strategy cells share `prompt_set_sha256` `8a65d46237d2…` | `results/descriptive_2026-09-21/parsed/*.jsonl` | `prompt_set_sha256` | recomputed |
| B2 | The exception is `dreaddit \| google/gemma-4-31b-it \| one-shot-cot \| run 5`, experiment `pub_013_dreaddit_gemma_coreweave_osc_run5`, hash `d831e49717af…`, 715 records | same | same | recomputed |
| B3 | All five per-agent prompt hashes are identical between `pub_011` (runs 1–4) and `pub_013` (run 5) | `runs/pub_013_dreaddit_gemma_coreweave_osc_run5/raw/attempts.jsonl`; external evidence copy of `runs/pub_011_dreaddit_gemma_coreweave/raw/attempts.jsonl` | `prompt_sha256.{emotion,symptom,context,referral,report}` | emotion `38e256ccaf1e0cb6` (3,771 ch); symptom `d049410a8b20b31e` (4,572); context `ca91dbb511c26235` (3,442); referral `b16db6cd21abc1ee` (5,078); report `0ff2166f07f8cc1c` (8,324) — identical on both sides |

## C. Runs, pseudoreplication, estimand

| # | Claim | Source | Location | Evidence |
|---|---|---|---|---|
| C1 | Runs are not paired across configurations | `STATISTICAL_ANALYSIS_PLAN.md` | § 2, l. 40 | "Runs are **not** paired across configurations. Run *k* of A and run *k* of B were executed at different times, on different processes and sometimes on different machines, so the run index carries no shared information." |
| C2 | Pooling 5 runs as independent observations is pseudoreplication | same | § 3, l. 43 | "They are *not* 5 independent samples: treating 5 × 699 records as 3,495 independent observations would be pseudoreplication." |
| C3 | The estimand is the five-run mean, runs nested in item | same | § 3, l. 44 | "The runs stay nested inside their item. The estimand is the frozen five-run quantity: the mean over the 5 runs of the per-run metric." |
| C4 | Item-mean aggregation discards no information for accuracy-type metrics | same | § 3, l. 45 | "For accuracy-type metrics this equals the mean over items of each item's 5-run average correctness, so no information is discarded." |
| C5 | Runs are not resampled | same | § 3, l. 46 | "The runs themselves are **not** resampled. The resulting intervals express item-sampling uncertainty given the observed stochastic behaviour." |
| C6 | Cluster = item carrying all configurations × runs | same | § 4, ll. 49–52 | "Cluster = one item, carrying all of its 15 configurations × 5 runs = 75 predictions per dataset." |
| C7 | One shared bootstrap index vector across configurations; B = 4,000; percentile intervals | same | § 5, ll. 55–59 | "draw 699 (or 622) item indices **with replacement** … using one index vector shared by all 15 configurations of that dataset"; "Replicates B = 4,000"; "95% percentile intervals" |
| C8 | Run-level Wilcoxon is rejected, with the power reason | same | § B table, l. 103 | "It would treat the 5 runs as the paired sample. Runs are not paired across configurations. With n = 5 the smallest attainable two-sided exact Wilcoxon p-value is 0.0625, so no comparison could ever reach 0.05 before correction." |
| C9 | Two-stage (item + run) bootstrap was considered and rejected | same | D3 discussion, l. 156 | "Two-stage resampling with only 5 runs gives unstable variance estimates. This is disclosed as a limitation." |
| C10 | Majority-vote aggregation for McNemar is ≥ 3 of 5, no ties | same | D2 (a), l. 143 | "An item counts as correct if it was effectively correct in ≥ 3 of 5 runs. 5 is odd, so there are no ties." |

## D. Metrics, invalid outputs, safety intercepts

| # | Claim | Source | Location | Evidence |
|---|---|---|---|---|
| D1 | Invalid outputs count as not-correct on the attributable denominator | `STATISTICAL_ANALYSIS_PLAN.md` | § 7, l. 68 | "They are kept exactly as frozen. For effective accuracy and macro-F1 they count as not-correct on the attributable denominator." |
| D2 | Effective correctness definition | same | § 6, l. 63 | "'Correct' is the frozen **effective** correctness: valid and equal to ground truth. A model-invalid output is **incorrect**." |
| D3 | Conditional accuracy compares different item subsets | same | § 7, l. 70 | "Conditional accuracy (correct / valid) has a different denominator for each configuration. A 'paired' comparison of conditional accuracy therefore compares different item subsets." |
| D4 | Conditional accuracy is secondary: CIs only, no tests | same | § E, l. 224 | "**Conditional accuracy.** CIs only (configuration level and RQ1 pair differences). No p-values and no Holm." |
| D5 | Safety intercepts removed once from the pool, identical in every cell | same | § 8, l. 73 | "The excluded items are identical in every cell (16 / 1), so they are removed once from the item pool and never resampled." |
| D6 | McNemar does not apply to macro-F1 | same | § 6, l. 65 | "McNemar does not apply to macro-F1 or conditional accuracy, which are not per-item binary outcomes." |
| D7 | McNemar needs an aggregation decision because each item has 5 outcomes | same | § 6, l. 64 | "Each item has 5 outcomes per configuration, not 1, so McNemar **cannot be applied without an aggregation decision**." |
| D8 | No inference on the GoEmotions anxiety class | same | § C, l. 115 | "No inference on the GoEmotions anxiety class (n = 6: one item moves recall by 1/6)." |
| D9 | ~0.25% of bootstrap replicates contain no anxiety item; undefined F1 set to 0 | same | § 5, l. 59 | "GoEmotions anxiety has 6 items, so about 0.25% of replicates (≈ 10) will contain no anxiety item. MetricPolicy 1.0.0 then sets the undefined recall and F1 to 0." |
| D10 | Complete-case cost of conditioning on validity | `results/descriptive_2026-09-21/authoritative_records.jsonl` | recomputed per model × dataset | Worst case Phi-4 / GoEmotions: 622 attributable → 333 (worst strategy pair, one run) → 319 (all 3 strategies, one run) → **195** (all 3 strategies × all 5 runs). Full table in § 1.5 of the design note. |

## E. Scope of the frozen plan

| # | Claim | Source | Location | Evidence |
|---|---|---|---|---|
| E1 | The plan's declared scope is RQ1 and RQ2 | `STATISTICAL_ANALYSIS_PLAN.md` | title, l. 1 | "# Statistical analysis plan: inferential RQ1 / RQ2" |
| E2 | The plan was written before any test was run | same | l. 3 | "Status: **APPROVED 2026-09-21. Written before any test was run.** … No p-value, CI or replicate existed when these decisions were made." |
| E3 | The plan's RQ3 paragraph is about latency, and the reasons given are latency-specific | same | § C, l. 128 | "**RQ3.** Descriptive only; no inferential latency analysis. The confounds … (3 s quantisation, fixed strategy order, machine, provider and time, concurrent load for Llama Dreaddit, no per-agent timing) mean no test could attribute a latency difference to the prompting strategy." |
| E4 | Section E repeats the refusal in two words | same | § E, l. 226 | "**RQ3.** No inference." |
| E5 | No strategy-vs-strategy contrast is enumerated anywhere in the plan | same | §§ A–F, D1–D4 | RQ1 is "model-vs-model **within the same dataset and the same prompting strategy**" (l. 118); RQ2 is configuration vs baseline (ll. 122–126); D1's four options are all about the RQ1 model family |
| E6 | Averaging over strategies was considered and rejected because of interactions | same | D1 option (c), l. 138 | "Model effect averaged over the 3 strategies … averages over strong model × strategy interactions (e.g. Phi-4 GoEmotions one-shot-CoT)." |
| E7 | The July protocol specified a different test, and the discrepancy must be disclosed | same | § B table, l. 103 | "Wilcoxon signed-rank + Bonferroni, as in the July `AnxioSense_Experimental_Setup.docx` §6.4 — **Not appropriate here** … this discrepancy should be disclosed in the paper." |
| E8 | The frozen Holm families contain no strategy contrast | `results/inferential_2026-09-21/tables/*.csv` | `family` column | Distinct values: `RQ1-primary-dreaddit`, `RQ1-primary-goemotions`, `RQ1-mcnemar-dreaddit`, `RQ1-mcnemar-goemotions`, `RQ2-primary-dreaddit`, `RQ2-primary-goemotions` |

## F. Reusability of the frozen implementation

| # | Claim | Source | Location | Evidence |
|---|---|---|---|---|
| F1 | The permutation routine takes two arbitrary configuration indices | `results/inferential_2026-09-21/code/run_inferential.py` | `def perm_pair(ci, cj)`, l. 291 | docstring: "Swap test: for swapped items, A receives B's five run outcomes and vice versa." No assumption that the two share a strategy |
| F2 | The same routine already produces both metrics | same | ll. 302–303 | `T_obs_f1 = float(OBS[ds]["macro_f1"][ci] - OBS[ds]["macro_f1"][cj])`; `T_perm_f1 = mA["macro_f1"] - mB["macro_f1"]` |
| F3 | Macro-F1 is recomputed inside the permutation, not decomposed | same | `metrics_from_counts`, ll. 166–175 | metrics are derived from the count tensor per replicate |
| F4 | Header records the frozen family structure and test parameters | same | ll. 22–25 | "Paired item-level swap test, P = 10,000 swap sets per dataset"; "HOLM families (per dataset): RQ1 primary 60 (10 pairs x 3 strategies x {acc_eff, macro_f1})" |
| F5 | Frozen decisions D2 and D3 as executed | `STATISTICAL_ANALYSIS_PLAN.md` | § F table, ll. 179–180 | D2: "exact McNemar on per-item **majority-vote effective correctness** … Secondary … in its own Holm family per dataset"; D3: "**paired item-level permutation test**, 10,000 random swaps per dataset. CIs come from the 4,000-replicate item-cluster bootstrap." |

## G. Descriptive context quoted in the design note

| # | Claim | Source | Location |
|---|---|---|---|
| G1 | One configuration's effective accuracy falls 0.0887 vs zero-shot while conditional accuracy falls less than half that, with evaluability 0.9980 → 0.9230 | `results/final_rq_results_2026-09-25/RQ3_PROMPTING_STRATEGIES.md` and `tables/rq3_accuracy.csv`, `tables/rq1_dreaddit.csv` | Qwen3.5 27B, Dreaddit |
| G2 | One configuration has a five-run effective-accuracy SD above 0.12; another has SD exactly 0 | `results/final_rq_results_2026-09-25/tables/rq1_goemotions.csv` | `acc_eff_sd` |
| G3 | Class-selective invalidity survives Holm in 4 of 30 configurations; strongest enrichment ratio ≈ 1.85 | `results/final_rq_results_2026-09-25/tables/exploratory_invalid_class_composition.csv` | `exploratory_holm_significant_0.05`, `enrichment_ratio` — **exploratory, not frozen** |

**No RQ3 significance result is reported in either document. No test was run.**
