# Independent verification of `descriptive_2026-09-21`

Date: 2026-09-21. Scope: descriptive results only. No inferential statistics, no API calls, no reruns, no changes to the parser, scoring policy, raw data or results.

## Verdict

**INDEPENDENT VERIFICATION PASSED.**

- Linkage: all 150 cells and all 100,350 authoritative records correspond to the frozen grid manifest. 0 issues.
- Metrics: every count, correct count, confusion matrix, parse-status count, source run and majority baseline matches exactly. The only differences are 766 IEEE-754 floating-point rounding differences (max |diff| 2.22e-16). There are 0 substantive discrepancies.
- Freeze: `descriptive_2026-09-21/` is byte-identical before and after verification (32 files; combined digest `5567988b1fd708fa4a81808c36b728f8a5fa471ffa2822a79d3830d41927ece5` on both inventories).

## Method

Two standalone Python scripts, standard library only. They import nothing from `runner/` or from `descriptive_2026-09-21/code/`. Their only inputs are read-only files; they write only into `verification_2026-09-21/`.

### 1. `verify_linkage.py` → `linkage_result.json`

- Dataset manifest file hashes and self-hashes checked against `frozen_grid_manifest.json`.
- Each `parsed/<run>.jsonl` hash checked against `sources[run].parsed_output_sha256`.
- Every authoritative record joined to its parsed source record by `terminal_attempt_uuid`. All 16 scoring fields compared, plus the `cell_id`.
- Duplicate `(cell_id, sample_id)` keys; ground truth vs dataset manifest; consistency of safety / `prediction_valid` / `include_in_metrics`.
- Per cell: n, source_run, final-outcome counts, parse-status counts, safety IDs, and `records_sha256` (sha256 of sorted `sample_id|terminal_attempt_uuid`) against the manifest. Sample set checked against the dataset manifest.
- Result: 100,350 records; 0 bad lines; 150 cells = 150 manifest cells; 100,350 distinct keys (Dreaddit 53,625 = 75×715; GoEmotions 46,725 = 75×623). The replacement cell `dreaddit|google/gemma-4-31b-it|one-shot-cot|run5` is sourced only from pub_013; the other Dreaddit×Gemma cells are sourced only from pub_011.

### 2. `verify_metrics.py` → `metrics_verification_result.json`, `independent_per_run.csv`

- Recomputed from `authoritative_records.jsonl` only. The summary files were read only as the comparison target.
- Exact rational arithmetic (`fractions.Fraction`) for every per-cell quantity: N_total, N_safety, N_attributable, N_valid, N_model_invalid, N_infra, N_unaccounted, correct/incorrect, conditional accuracy (correct/valid), effective accuracy (correct/attributable), per-class TP/FP/FN/support/P/R/F1 (0 when undefined), macro P/R/F1 over the fixed label list, confusion matrix, evaluability, model-invalid rate, infra-failure rate.
- Five-run mean computed as an exact Fraction. Sample SD (n−1) computed via `Decimal` sqrt at 60-digit precision.
- Majority baselines computed from the dataset manifests.
- Compared against `per_run_results.csv`, `cell_metrics.json`, `aggregate_results.csv` and `aggregate_five_runs.json`. Every non-identical value was recorded, even a 1-ulp difference.

## Results

| Item | Value |
|---|---|
| Comparisons | 10,594 |
| Exact matches | 9,828 |
| Discrepancies | 766 (all float rounding; 0 non-float) |
| By location | cell_metrics.json 350 · aggregates (CSV + JSON) 296 · per_run_results.csv 120 |
| Distinct locations | 252 |
| Max abs diff | 2.22e-16 (macro/per-class F1); 1.11e-16 (macro P/R, means); ≤ 6.14e-17 (SDs) |
| Affected fields | macro P/R/F1, per-class F1, five-run means and SDs |
| Not affected | all counts, correct counts, per-run conditional/effective accuracy, confusion matrices, parse-status counts, source runs |

Cause: the pipeline accumulates in binary floating point, whereas this verification rounds an exact rational once. Summation order and intermediate rounding account for the last-bit differences.

Rounding stability: none of the 766 values changes when rounded to 4 or 6 dp. At 3 dp, 2 values sit exactly on a half boundary. Their exact values are 0.7375 and 0.4875:

- `dreaddit|meta-llama/llama-4-scout|zero-shot|run1` per_class.1.f1: reported 0.7374999999999999 (→ 0.737), exact 0.7375 (→ 0.738 half-up)
- `dreaddit|qwen/qwen3.5-27b|one-shot-cot|run4` per_class.1.f1: reported 0.48750000000000004 (→ 0.488), exact 0.4875 (→ 0.487/0.488 depending on rule)

This is a presentation note, not a result error. Any 3-dp table should round from exact values under a stated rule.

Majority baselines: Dreaddit 369/715 = 0.5160839160839161 (class 1), stored as 0.516084. GoEmotions 487/623 = 0.7817014446227929 (non_distress), stored as 0.781701. The stored values are the exact values rounded to 6 dp.

## Files

`freeze_hashes_before.txt`, `freeze_hashes_after.txt` (identical), `verify_linkage.py`, `linkage_result.json`, `verify_metrics.py`, `metrics_verification_result.json` (full list of all 766 differences), `independent_per_run.csv`, and this file.
