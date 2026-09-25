# RQ3 prompting-strategy inferential analysis — 2026-09-25

**Post-hoc / exploratory** inferential analysis of how prompting strategy (zero-shot, zero-shot-CoT,
one-shot-CoT) affects classification performance, within each model and dataset, on the frozen AnxioSense
publication grid.

Start with **`RQ3_STRATEGY_INFERENCE_REPORT.md`**. It contains all 30 primary comparisons per dataset,
the secondary McNemar check, the invalid-output context, the answer to RQ3 per dataset, and what the
analysis does not support.

## Read this first

- The **procedure** was pre-specified and frozen on 2026-09-21 for RQ1/RQ2 and is applied here unchanged.
- The **contrasts** were declared before any RQ3 test was run, but after the descriptive results were known.
  The analysis is therefore **post-hoc / exploratory** and must be labelled that way in the paper.
- `PREREGISTRATION_FREEZE.json` records the SHA-256 of the plan, the pre-check and the analysis code at
  2026-09-25T22:04:33Z; the analysis ran at 22:04:45Z. Validation check 5 confirms the code that ran is the
  code that was frozen.
- Nothing outside this directory was created or modified. Inputs are hash-pinned and the analysis fails
  closed on any mismatch.

## Files

| File | Contents |
|---|---|
| `RQ3_SAP_ADDENDUM.md` | The frozen analysis plan — design, pre-conditions, reporting rules, limitations |
| `PREREGISTRATION_FREEZE.json` | Pre-execution freeze: hashes + timestamp, `"execution_status_at_freeze": "NOT YET EXECUTED"` |
| `precheck.json` | 38 pre-condition checks (identical item sets; runs nested, not independent; draw reproduction) |
| `INPUT_HASHES.sha256` | SHA-256 of every input artifact |
| `RQ3_STRATEGY_INFERENCE_REPORT.md` | The human-readable report — all 60 primary comparisons, McNemar, answers |
| `VALIDATION.md` / `validation.json` | 32 post-execution checks, each re-deriving its quantity independently |
| `analysis_manifest.json` | Seeds, draw digests, families, input and output hashes, environment |
| `tables/rq3_strategy_pairs_primary.csv` | 60 rows — the primary result (2 metrics × 3 pairs × 5 models × 2 datasets) |
| `tables/rq3_strategy_pairs_mcnemar.csv` | 30 rows — secondary exact McNemar |
| `tables/rq3_strategy_pairs_conditional_accuracy_ci.csv` | 30 rows — conditional accuracy, **CIs only, no test** |
| `tables/rq3_configuration_level_ci.csv` | 30 rows — configuration-level CIs; reproduce the frozen ones bit-for-bit |
| `tables/rq3_<dataset>_<metric>.md` | The four rendered result tables |
| `replicates/permutation_<dataset>.csv.gz` | All 10,000 permutation statistics per contrast |
| `replicates/bootstrap_<dataset>.csv.gz` | All 4,000 bootstrap replicate metrics per configuration |
| `code/00_precheck.py` … `code/03_build_report.py` | Re-runnable pipeline |
| `CHECKSUMS.sha256` | Manifest of every file above |

## Column meanings in `rq3_strategy_pairs_primary.csv`

`A_mean`/`A_sd` and `B_mean`/`B_sd` are the five-run mean and sample SD (n−1) for the two arms.
`diff_A_minus_B` is the observed difference in the five-run metric; `ci_low`/`ci_high` are the 95%
item-cluster bootstrap percentile interval on that difference; `p_perm` is the paired item-level permutation
p-value; `p_holm` is Holm-adjusted within the dataset's family of 30; `holm_significant_0.05` is the
decision. `A_invalid_outputs_5runs`, `B_invalid_outputs_5runs`, `A_evaluability`, `B_evaluability` and
`diff_evaluability_*` are the descriptive invalid-output companion — not a mediation analysis.

## Relationship to the other packages

- `inferential_2026-09-21/` — the frozen RQ1/RQ2 confirmatory analysis. Unchanged. The same seed strings and
  the same draws are reused here, which is why `tables/rq3_configuration_level_ci.csv` is string-identical to
  its `configuration_level_ci.csv`.
- `rq3_inference_design_2026-09-25/` — the design note this analysis implements. Unchanged.
- `unified_results_tables_2026-09-25/` — the descriptive tables. The response-time column there remains
  **descriptive only**; nothing here licenses an inferential latency claim.
