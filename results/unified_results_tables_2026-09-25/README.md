# Unified descriptive results tables — Dreaddit and GoEmotions

Two tables, 15 rows each (5 models × 3 prompting strategies), combining classification quality,
invalid-output behaviour and **Total System Response Time** so that RQ1, RQ2 and RQ3 can be read from one
place, as requested at the supervisor meeting.

**Read-only.** Nothing outside this directory was created or modified. No experiment was rerun, no model API
was called, **no inferential test was run**, and no metric definition was invented. The existing detailed
latency tables in `rq1_rq3_reporting_2026-09-21/tables/` are untouched and remain the supplementary
replication evidence.

## Files

| File | Contents |
|---|---|
| `tables/unified_dreaddit.csv` / `.md` | 15 rows — the Dreaddit unified table |
| `tables/unified_goemotions.csv` / `.md` | 15 rows — the GoEmotions unified table |
| `tables/per_class_supplement.csv` | 105 rows — per-class precision / recall / F1 (mean ± SD) and class support; the only place a non-macro precision, recall or F1 exists |
| `tables/_verification.json` | the discrepancy list produced by the build (empty) |
| `code/build_unified_tables.py` | the read-only generator, which also runs the verification |
| `METRIC_AUDIT.md` | definition, run coverage, source file and "newly calculated?" for every column |
| `CHECKSUMS.sha256` | SHA-256 manifest of the nine files above (excludes itself) |

## One important labelling correction

The requested column list contained **both** `F1-score` and `Macro-F1`. In the frozen artifacts these would
be the same number: the existing LLM results table
(`rq1_rq3_reporting_2026-09-21/tables/rq1_dreaddit.csv`) has exactly three P/R/F columns, named
`macro_precision`, `macro_recall`, `macro_f1`, and there is **no separate non-macro precision, recall or
F1-score** at the configuration level.

Rather than print one quantity twice under two names, the tables use the accurate labels
**Macro-Precision, Macro-Recall, Macro-F1** and the per-class values are supplied separately in
`tables/per_class_supplement.csv`. See `METRIC_AUDIT.md` § "Discrepancy against the requested column list"
for the full reasoning and for what to do if a per-class F1 column is wanted in the main table after all.

## Column → research question map

| Column | RQ1 | RQ2 | RQ3 | Source artifact | Field |
|---|---|---|---|---|---|
| Model | ✓ | | | `descriptive_2026-09-21/per_run_results.csv` | `model` |
| Prompt Strategy | | | ✓ | same | `strategy` |
| Conditional Accuracy (mean ± SD) | secondary | secondary | secondary | `rq1_rq3_reporting_2026-09-21/rq12_full_precision.json` | `aggregates[cell].acc_cond.{mean,sd}` |
| Effective Accuracy (mean ± SD) | **primary** | **primary** | **primary** | same | `aggregates[cell].acc_eff.{mean,sd}` |
| Macro-Precision (mean ± SD) | ✓ | ✓ | ✓ | same | `aggregates[cell].macro_p.{mean,sd}` |
| Macro-Recall (mean ± SD) | ✓ | ✓ | ✓ | same | `aggregates[cell].macro_r.{mean,sd}` |
| Macro-F1 (mean ± SD) | **co-primary** | **co-primary** | **co-primary** | same | `aggregates[cell].macro_f1.{mean,sd}` |
| Invalid Outputs (Σ 5 runs) | ✓ | ✓ | ✓ | same | `aggregates[cell].sum_N_model_invalid` |
| Invalid Output Rate (mean ± SD) | ✓ | ✓ | ✓ | same | `aggregates[cell].invalid_rate.{mean,sd}` |
| Total System Response Time (s, mean ± SD) | ✓ | | ✓ | `rq1_rq3_reporting_2026-09-21/tables/rq3_<dataset>_latency.csv` | `client_latency_mean_s` |

### How to use each table for each question

**RQ1 — which LLM yields the best results?** Compare the five models *within a fixed prompting strategy*
(rows share a strategy), using effective accuracy **and** macro-F1, with invalid outputs and response time
as additional criteria. The statistically supported model comparisons already exist and are **not repeated
here**: see `inferential_2026-09-21/tables/rq1_model_pairs_primary.csv` (paired item-level permutation,
Holm-corrected) and the summary in `final_rq_results_2026-09-25/RQ1_MODEL_COMPARISON.md`. Differences visible
in these tables are descriptive unless that package says otherwise.

**RQ2 — what is the accuracy of AnxioSense?** Read the accuracy columns against the majority baseline, which
is **not** a column because it is a constant per dataset:

| Dataset | Majority baseline, frozen scalar | Majority baseline on the attributable pool |
|---|---|---|
| Dreaddit | 0.516084 (369/715) | 355/699 = 0.507868 |
| GoEmotions | 0.781701 (487/623) | 487/622 = 0.782958 |

On GoEmotions an accuracy near 0.78 is the constant-predictor level, so macro-F1 must be read alongside it.
The tested comparisons against the baseline are in
`inferential_2026-09-21/tables/rq2_configuration_vs_baseline.csv`.

**RQ3 — which prompting strategy is the most efficient?** Compare the three strategies *within a fixed model*
(rows share a model), using classification quality **and** Total System Response Time together. These
comparisons are **descriptive only**: the frozen statistical plan states "RQ3. No inference.", and no
strategy-vs-strategy hypothesis test exists in any package. See
`rq3_inference_design_2026-09-25/RQ3_INFERENCE_DESIGN.md` for why, and what a defensible test would require.

## Reading the response-time column

`Total System Response Time` is the **client end-to-end wall clock for one complete assessment** — the runner's
`time.perf_counter` around the whole HTTP POST to `/api/workflow/evaluate`, covering the safety check, the
four parallel agents and the report agent, plus workflow creation, polling and result extraction. Per run it
is the mean over LLM-served terminal attempts; the table value is the mean ± sample SD of those five per-run
means. Safety intercepts (16 per Dreaddit run, 1 per GoEmotions run) short-circuit before any agent call and
are excluded.

Three caveats that belong in any caption using this column:

1. **Measurement resolution is 3 seconds** — the workflow is polled at that cadence, so a value is
   essentially (number of polls × 3 s). Several within-model strategy differences are smaller than one poll.
2. **Strategies ran in sequential blocks**, so strategy is confounded with time of day and provider load.
3. **Model is confounded with serving provider**, so cross-model response-time differences partly reflect
   infrastructure, not the model.

The median and p90 statistics are deliberately **not** in this table, per the request; they remain in the
supplementary frozen latency tables. The medians are the less informative choice here because they land on
the 3-second lattice.

## Reading the invalid-output columns

`Effective Accuracy = Conditional Accuracy × Evaluability`, exactly, and
`Evaluability = 1 − Invalid Output Rate`. So the gap between the two accuracy columns is arithmetic, and the
invalid columns are what explain it. Two rows make this concrete:

- **Qwen3.5 27B / Dreaddit / zero-shot-CoT**: conditional 0.6525, effective 0.6023, 269 invalid outputs.
  Most of the accuracy loss relative to the model's other strategies is a serialisation failure, not a
  reasoning failure.
- **Phi-4 / GoEmotions / one-shot-CoT**: conditional 0.8011, effective 0.6730, 499 invalid outputs, and an
  effective-accuracy SD of 0.1258 across the five runs.

Conditional accuracy is reported for transparency only. It is computed on each configuration's own valid
predictions, so its denominator differs by row and it must not be used to rank models or strategies; see
`final_rq_results_2026-09-25/INVALID_OUTPUT_SELECTION_EFFECT.md`.

## Verification performed by the generator

`code/build_unified_tables.py` re-derives every five-run mean and SD from the frozen per-run values in
`descriptive_2026-09-21/per_run_results.csv` and compares it with `rq12_full_precision.json`, and separately
compares against `descriptive_2026-09-21/aggregate_five_runs.json` for the four metrics that file contains.
Invalid-output counts are checked against the per-run sums. Latency strings are copied verbatim.
**Result: 0 discrepancies** across 30 configurations × 6 metrics plus 30 invalid-count checks
(`tables/_verification.json`).
