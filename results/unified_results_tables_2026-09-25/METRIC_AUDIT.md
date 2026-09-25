# Metric audit — unified descriptive results tables (2026-09-25)

For every column in `tables/unified_dreaddit.csv` and `tables/unified_goemotions.csv`: the exact definition
as implemented in the frozen code, whether the quantity existed for all five runs, the source file(s), and
whether anything had to be newly calculated for this package.

Scope statement first, because it governs everything below:

> **No inferential test was run. No frozen artifact was created, modified, repaired, rescored or rerun. No
> model or API call was made. No metric definition was invented or changed.** Every number in the two tables
> is copied from a frozen artifact; the generator's only arithmetic is a verification recomputation whose
> results are discarded after comparison.

---

## 0. Where the definitions come from

All classification metrics are defined once, in code, and that definition is frozen:

- `evaluation/publication_experiments/runner/metrics.py`
  — `METRIC_POLICY_VERSION = "1.0.0"`, `class MetricPolicy`, `_prf()`, `cell_metrics()`.
- `evaluation/publication_experiments/runner/parse.py` — `PARSER_VERSION = "1.0.0"`; decides which records
  are valid, which are `MODEL_BEHAVIOUR`-invalid, and which are `SAFETY_INTERCEPT`.

Two policy clauses in `MetricPolicy` shape every denominator:

| Clause | Value | Consequence |
|---|---|---|
| `exclude_safety_intercept_from_model_attribution` | `True` | The deterministic crisis path fires before any model call, so those items are reported separately and never attributed to a model. Dreaddit 16 per run, GoEmotions 1 per run. |
| `effective_accuracy_denominator` | `"all_attributable"` | A model cannot improve its score by declining to answer. |

Record buckets per cell (`cell_metrics`), with `N_unaccounted` asserted to 0:

```
N_total = N_safety_intercept + N_attributable
N_attributable = N_valid + N_model_invalid + N_infra_failed + N_unaccounted
```

Across the whole grid: 100,350 records, 1,275 safety intercepts, 99,075 attributable, 97,089 valid,
1,986 model-invalid, **0 infrastructure failures**, 0 unaccounted.

**Label lists** (the macro denominator):

| Dataset | Labels | n labels |
|---|---|---|
| Dreaddit | `0` (non-stress), `1` (stress) | 2 |
| GoEmotions | `non_distress`, `frustration`, `sadness`, `fear`, `anxiety` | 5 |

The label list is fixed per dataset and does **not** shrink when a class is absent from a run's predictions.
`_prf()` assigns precision = 0.0 and recall = 0.0 when the relevant denominator is zero, and the macro
average is the unweighted mean over the full fixed label list. This is why GoEmotions macro-F1 sits near
0.53–0.59 while accuracy sits near 0.78: the four minority classes carry equal weight to `non_distress`.

**Five-run summarisation.** Every `mean ± SD` in the tables is the mean and the **sample** standard deviation
(n − 1 denominator, `statistics.fmean` / `statistics.stdev`) of the **five per-run values** — never a value
recomputed on the five runs pooled together. This matters: pooling would change the estimand and would
pseudoreplicate. The frozen statistical analysis plan fixes the five-run mean as the estimand
(`inferential_2026-09-21/STATISTICAL_ANALYSIS_PLAN.md`, ll. 43–46).

---

## 1. Column-by-column audit

### `Model`

- **Definition** — display label for the pinned provider/model identifier. `google/gemma-4-31b-it` →
  *Gemma 4 31B*, `meta-llama/llama-4-scout` → *Llama 4 Scout*, `microsoft/phi-4` → *Phi-4*,
  `mistralai/mistral-small-2603` → *Mistral Small 4*, `qwen/qwen3.5-27b` → *Qwen3.5 27B*.
- **All five runs?** Yes — the model id is pinned per run in the run config (`pin_provider`), identical
  across the five runs of a cell.
- **Source** — `results/descriptive_2026-09-21/per_run_results.csv` (`model`), and the same labels appear in
  `results/rq1_rq3_reporting_2026-09-21/tables/rq3_<dataset>_latency.csv` via `SHORT` in
  `code/rq3_latency_tables.py`.
- **Newly calculated?** No.
- **Note** — the label strings in the latency tables are the authority used for the join
  (*Gemma 4 31B*, *Qwen3.5 27B*). The `rq1_rq3_tables` display variants ("Gemma 4 31B IT", "Qwen 3.5 27B")
  are **not** a source in this package.

### `Prompt Strategy`

- **Definition** — one of the three prompting conditions declared in every run config:
  `zero-shot`, `zero-shot-cot`, `one-shot-cot` (rendered *zero-shot / zero-shot-CoT / one-shot-CoT*).
- **All five runs?** Yes — all three strategies run inside each of the five runs, over the identical item set.
- **Source** — `per_run_results.csv` (`strategy`); configs e.g. `configs/pub_001_dreaddit_qwen.yaml`
  (`strategies: [zero-shot, zero-shot-cot, one-shot-cot]`, `runs: 5`).
- **Newly calculated?** No.

### `Conditional Accuracy (mean ± SD)`

- **Definition** — `accuracy_conditional = correct / N_valid`. Correct predictions divided by the
  configuration's **own valid predictions**. `metrics.py`, `cell_metrics()`:
  `"accuracy_conditional": correct / len(valid)`.
- **All five runs?** Yes — present for all 5 runs of all 30 configurations.
- **Source** — five-run mean ± SD: `results/rq1_rq3_reporting_2026-09-21/rq12_full_precision.json`
  → `aggregates["<dataset>|<model_id>|<strategy>"].acc_cond.{mean,sd}`.
  Per-run values: `results/descriptive_2026-09-21/per_run_results.csv` (`accuracy_conditional`).
  Independent five-run aggregate: `results/descriptive_2026-09-21/aggregate_five_runs.json`
  (`accuracy_conditional.{mean,sd}`) and `aggregate_results.csv`.
- **Newly calculated?** No.
- **Interpretation constraint** — the denominator differs by row, so this column must **not** be used to rank
  models or strategies. It is reported for transparency and because
  `Effective = Conditional × Evaluability` makes the invalid-output cost visible.

### `Effective Accuracy (mean ± SD)`

- **Definition** — `accuracy_effective = correct / N_attributable`. Correct predictions divided by **every
  item dispatched to the model**, so an invalid output counts as a miss. `metrics.py`:
  `"accuracy_effective": correct / len(attributable)`.
- **All five runs?** Yes.
- **Source** — `rq12_full_precision.json` → `aggregates[cell].acc_eff.{mean,sd}`; per-run
  `per_run_results.csv` (`accuracy_effective`); independent aggregate `aggregate_five_runs.json`
  (`accuracy_effective.{mean,sd}`).
- **Newly calculated?** No.
- **Note** — this is the primary accuracy column, and it is the metric the frozen inferential package tested
  for RQ1 and RQ2.

### `Macro-Precision (mean ± SD)`

- **Definition** — unweighted mean of per-class precision over the **fixed** label list:
  `macro_precision = Σ_c precision_c / n_labels`, with `precision_c = TP_c / (TP_c + FP_c)` and
  `precision_c = 0.0` when `TP_c + FP_c = 0`. Computed on the valid predictions only.
  `metrics.py`, `_prf()` + `cell_metrics()`:
  `"macro_precision": sum(v["precision"] for v in per_class.values()) / len(labels)`.
- **All five runs?** Yes — per-run `macro_precision` is present for all 5 runs of all 30 configurations in
  `per_run_results.csv`.
- **Source** — five-run mean ± SD: `rq12_full_precision.json` → `aggregates[cell].macro_p.{mean,sd}`.
  Per-run: `descriptive_2026-09-21/per_run_results.csv` (`macro_precision`). Frozen configuration-level
  table: `rq1_rq3_reporting_2026-09-21/tables/rq1_<dataset>.csv` (`macro_precision`).
- **Newly calculated?** **Not for this package.** But the *five-run aggregate* of macro-P is not in the
  descriptive package: `aggregate_five_runs.json` and `aggregate_results.csv` carry five-run mean/SD only for
  `accuracy_conditional`, `accuracy_effective`, `macro_f1` and `evaluability` (see `metrics.py`,
  `aggregate_cells()`, which loops over exactly those three metrics plus evaluability). The macro-P/macro-R
  five-run mean ± SD was aggregated on **2026-09-21** in the reporting package, from the frozen per-run
  values, and is disclosed there — `rq1_rq3_reporting_2026-09-21/REPORT.md` line 30: *"The five-run macro-P
  and macro-R are not in the frozen aggregate files. They are the same mean ± SD applied to the frozen
  per-run values, which were cross-checked."* This package **reuses** that stored value at full precision and
  re-verifies it (§2); it does not re-derive a new one.

### `Macro-Recall (mean ± SD)`

- **Definition** — `macro_recall = Σ_c recall_c / n_labels`, `recall_c = TP_c / (TP_c + FN_c)`, `0.0` when the
  denominator is zero. Computed on the valid predictions only. `metrics.py`:
  `"macro_recall": sum(v["recall"] for v in per_class.values()) / len(labels)`.
- **All five runs?** Yes, same as macro-precision.
- **Source** — `rq12_full_precision.json` → `aggregates[cell].macro_r.{mean,sd}`; per-run
  `per_run_results.csv` (`macro_recall`); frozen table `tables/rq1_<dataset>.csv` (`macro_recall`).
- **Newly calculated?** No — identical situation and identical disclosure to macro-precision.

### `Macro-F1 (mean ± SD)`

- **Definition** — `macro_f1 = Σ_c F1_c / n_labels`, with `F1_c = 2·P_c·R_c / (P_c + R_c)` and `F1_c = 0.0`
  when `P_c + R_c = 0`. This is the **unweighted mean of per-class F1**, not the F1 of the macro-averaged
  precision and recall — the two differ, and the frozen implementation is the former. `metrics.py`:
  `"macro_f1": sum(v["f1"] for v in per_class.values()) / len(labels)`.
- **All five runs?** Yes.
- **Source** — `rq12_full_precision.json` → `aggregates[cell].macro_f1.{mean,sd}`; per-run
  `per_run_results.csv` (`macro_f1`); independent aggregate `aggregate_five_runs.json`
  (`macro_f1.{mean,sd}`) and `aggregate_results.csv`.
- **Newly calculated?** No.

### `Invalid Outputs (Σ 5 runs)`

- **Definition** — count of attributable records whose `failure_class == "MODEL_BEHAVIOUR"`, summed over the
  five runs. A record is `MODEL_BEHAVIOUR`-invalid when the offline parser cannot extract an in-vocabulary
  prediction from the **stored raw response**. `metrics.py`:
  `model_invalid = [r for r in attributable if r.get("failure_class") == "MODEL_BEHAVIOUR"]`.
- **Not** a transport/network failure. Transport is a separate axis (`runner/failures.py`,
  `classify_transport`, `RETRYABLE = {Transport.INFRA_TRANSIENT}`) and is the only input to retry; a parse
  failure is never retried. The scored grid contains **0** infrastructure failures.
- **All five runs?** Yes — a per-run count for all 5 runs of all 30 configurations.
- **Source** — `rq12_full_precision.json` → `aggregates[cell].sum_N_model_invalid`; per-run
  `per_run_results.csv` (`N_model_invalid`); frozen `tables/rq1_<dataset>.csv` (`model_invalid_5runs`,
  `invalid_per_run`); `aggregate_results.csv` (`sum_N_model_invalid`).
- **Newly calculated?** No. (It is a **sum**, not a mean, and is labelled `Σ 5 runs` for that reason.)
- **Cross-reference** — every one of these 1,986 records is classified individually in
  `results/invalid_output_audit_2026-09-25/invalid_outputs_row_level.csv`.

### `Invalid Output Rate (mean ± SD)`

- **Definition** — per run, `N_model_invalid / N_attributable`; then mean ± SD over the five runs.
  `metrics.py`, `rates`: `"model_invalid_rate": len(model_invalid) / len(attributable)`.
- **All five runs?** Yes.
- **Source** — `rq12_full_precision.json` → `aggregates[cell].invalid_rate.{mean,sd}`. Recoverable per-run
  from `per_run_results.csv` as `N_model_invalid / N_attributable`, and equal to `1 − evaluability` exactly
  because `N_infra_failed = 0` and `N_unaccounted = 0` in every cell.
- **Newly calculated?** No.
- **Why the column is here** — it makes the accuracy gap arithmetic rather than mysterious:
  `Effective = Conditional × (1 − Invalid Output Rate)` holds exactly, per run.
- **Note** — this column is an addition beyond the requested column list, not a substitution: the requested
  `Invalid Outputs` count is present as its own column.

### `Total System Response Time (s, mean ± SD)`

- **Definition** — the **client-measured end-to-end wall clock for one complete assessment**: the runner's
  `time.perf_counter` bracket around the whole HTTP POST to `/api/workflow/evaluate`, i.e. the safety check,
  the four parallel agents, the report agent, workflow creation, polling and result extraction. One value per
  authoritative assessment, taken from the **terminal** attempt. Per run: the arithmetic mean over
  LLM-served terminal attempts. Table value: mean ± sample SD of those **five per-run means**.
  Safety-intercepted assessments are excluded (they short-circuit before any agent call) and counted
  separately in the source table as `n_safety_excluded_5runs`.
- **All five runs?** Yes — `code/rq3_latency_tables.py` asserts exactly 5 cells per configuration
  (`assert len(cs) == 5`) and 150 cells / 100,350 records overall.
- **Source** — `results/rq1_rq3_reporting_2026-09-21/tables/rq3_<dataset>_latency.csv`, field
  `client_latency_mean_s`, copied **verbatim as a string** (already formatted `mm.mm ± ss.ss`, two decimals,
  `ROUND_HALF_UP`). Upstream: `rq3_terminal_latency_records.jsonl` → `rq3_latency_per_cell.json`, both
  produced from hash-verified raw files.
- **Newly calculated?** No — the string is copied, not recomputed. No rounding was re-applied.
- **Why mean and not median/p90** — requested. The median is also the weaker statistic here: the workflow is
  polled every 3,000 ms (`mastra_poll_interval_ms: 3000` in every run config), so medians land on the
  3-second lattice (e.g. Qwen/Dreaddit 9.08 / 9.08 / 9.07 s) and hide within-model differences. Median and
  p90 remain available, unchanged, in the same frozen source table.
- **Caveats that must travel with this column** — (i) 3-second measurement resolution, so several
  within-model strategy gaps are smaller than one poll; (ii) strategies ran in sequential blocks, confounding
  strategy with time of day and provider load (`executed_utc` in the source table); (iii) model is confounded
  with serving provider, so cross-model differences partly reflect infrastructure. The server-side check
  agrees: `server_latency_ms` (Express `Date.now()` delta) tracks the client value to about 6 ms at the
  median, so the column is not a client-side artefact.

### Supplementary file: `tables/per_class_supplement.csv`

- **Definitions** — per-class `precision`, `recall`, `f1` exactly as in `_prf()` above (0.0 when undefined),
  and `predicted_share` = the fraction of valid predictions assigned to that class; each as five-run
  mean ± SD.
- **All five runs?** Yes.
- **Source** — `rq12_full_precision.json` → `aggregates[cell].per_class[<class>].{precision,recall,f1,
  predicted_share}.{mean,sd}`.
- **Newly calculated?** The metric values, no. **One column is newly sourced and is labelled accordingly:**
  `support_in_attributable_pool`. `rq12_full_precision.json`'s `per_class` object carries
  `precision / recall / f1 / predicted_share` but **no** `support`, so support was taken from
  `rq12_full_precision.json` → `baselines[<dataset>].attributable_class_counts`
  (Dreaddit `{0: 344, 1: 355}`; GoEmotions `{non_distress: 487, frustration: 81, sadness: 33, fear: 15,
  anxiety: 6}`). That is the class support in the **attributable pool**, which is identical for all 15
  configurations of a dataset and is therefore *not* the per-run valid-pool support in configurations that
  produced invalid outputs. The column name says "in attributable pool" for exactly this reason. No metric
  was computed from it.

---

## 2. Verification performed, and its result

`code/build_unified_tables.py` runs three independent checks while it builds, and writes any disagreement to
`tables/_verification.json` rather than resolving it:

1. **Recomputation check.** For all 30 configurations × 6 metrics (`acc_cond`, `acc_eff`, `macro_p`,
   `macro_r`, `macro_f1`, `invalid_rate`), the five-run mean and sample SD are recomputed from the frozen
   per-run values in `descriptive_2026-09-21/per_run_results.csv` using `statistics.fmean` /
   `statistics.stdev` and compared with `rq12_full_precision.json` at a 1e-9 tolerance.
2. **Second-source check.** For the four metrics that `descriptive_2026-09-21/aggregate_five_runs.json`
   contains (`accuracy_conditional`, `accuracy_effective`, `macro_f1`, `evaluability`), the table value is
   compared against that independently written aggregate.
3. **Count check.** Each `Invalid Outputs (Σ 5 runs)` value is compared against the sum of the five per-run
   `N_model_invalid` values.

**Result: `{"discrepancies": []}` — 0 disagreements.** Nothing had to be reconciled, and nothing was
silently resolved.

Latency values were not recomputed, only copied; their upstream derivation is asserted inside the frozen
`rq3_latency_tables.py` (150 cells, 100,350 records, 5 cells per configuration).

---

## 3. Discrepancy against the requested column list

The requested columns were:

```
Model | Prompt Strategy | Conditional Accuracy | Effective Accuracy |
Precision | Recall | F1-score | Macro-F1 | Invalid Outputs | Total System Response Time
```

**What the frozen artifacts actually contain.** The existing LLM results table
`rq1_rq3_reporting_2026-09-21/tables/rq1_dreaddit.csv` has exactly three P/R/F columns, and their names are
`macro_precision`, `macro_recall`, `macro_f1`. `per_run_results.csv` likewise has `macro_precision`,
`macro_recall`, `macro_f1` and nothing else of that kind. **There is no non-macro, configuration-level
precision, recall or F1-score anywhere in the frozen artifacts.** Non-macro precision/recall/F1 exists only
*per class*, inside `per_class`.

**Consequence.** A `Precision` column and a `Recall` column would have to be the macro values, and an
`F1-score` column would have to be the macro value too — i.e. the same number as `Macro-F1`, printed twice
under two different names. That would misrepresent the metric to a reader and would look, in a paper, like
two distinct results.

**What was done instead**, per the instruction *"If the existing table actually used macro-precision and
macro-recall, preserve those exact definitions and label the columns accurately"*:

- the three columns are labelled **Macro-Precision**, **Macro-Recall**, **Macro-F1**;
- the duplicate `F1-score` column is **not** printed;
- the non-macro values are supplied in full in `tables/per_class_supplement.csv` (105 rows =
  2 datasets × 15 configurations × their label list), which is the only place they exist.

**If a per-class F1 column is wanted in the main table after all**, the defensible option is a *named* class
column — for Dreaddit `F1 (stress, class 1)` and for GoEmotions `F1 (anxiety)` — read from
`per_class[<class>].f1.{mean,sd}`. That is a labelling change only, requires no new computation, and the
values are already in the supplement. It was not done unilaterally because it changes what the table claims.

**No other discrepancy was found.** In particular the requested `Invalid Outputs` column is preserved
(as a five-run sum), and the requested response-time statistic is the client end-to-end mean ± SD across the
five runs, not the median or p90.

---

## 4. Confirmation

- **No inferential test was run.** No p-value, confidence interval, permutation, bootstrap or McNemar test
  was computed in this package, and no strategy-vs-strategy comparison was tested. The frozen statistical
  analysis plan states "RQ3. No inference." (`STATISTICAL_ANALYSIS_PLAN.md`, l. 226), and the six frozen
  inferential families remain the only tested hypotheses.
- **No frozen artifact was created, modified, deleted or rerun.** All writes went to
  `results/unified_results_tables_2026-09-25/`. `descriptive_2026-09-21/`,
  `rq1_rq3_reporting_2026-09-21/`, `inferential_2026-09-21/`, `invalid_output_audit_2026-09-25/`,
  `final_rq_results_2026-09-25/`, `rq3_inference_design_2026-09-25/`, the runner code, the configs, the
  prompts and the raw stores were opened read-only.
- **The existing detailed latency tables were not replaced.**
  `rq1_rq3_reporting_2026-09-21/tables/rq3_dreaddit_latency.csv` and `rq3_goemotions_latency.csv` are
  untouched and remain the supplementary replication evidence, including the median and p90 columns.
- **No experiment was rerun and no model or API call was made.**
- **No metric definition was invented or changed.** Every definition in §1 is quoted from
  `runner/metrics.py` at `METRIC_POLICY_VERSION = "1.0.0"`.
- **No output was repaired and rescored.** The 1,986 model-invalid records are counted as invalid, exactly as
  the frozen parser classified them.
