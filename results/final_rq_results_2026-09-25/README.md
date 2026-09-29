# Final RQ results package — AnxioSense

## AI-Assistance Disclosure

Generative AI tools were used to assist with analysis scripting, organization, verification, and drafting of this reporting package. Quantitative findings were derived from the frozen AnxioSense experimental artifacts and verified against their source files. AI-generated suggestions were not treated as experimental evidence, and the original frozen experimental results were not modified.

---

## What this package is

A read-only reporting layer over the already-frozen AnxioSense artifacts, assembled so the paper can be
written from a single, provenance-checked source. **No experiment was rerun, no model API was called, no
parser or metric definition was changed, and no invalid output was repaired and rescored.** Validation
check 12 re-runs both generators and confirms that nothing outside this directory changes.

## Source artifacts (all read-only)

| Package | What this package takes from it |
|---|---|
| `descriptive_2026-09-21/` | the frozen grid, per-cell metrics, authoritative records (class composition) |
| `verification_2026-09-21/` | the freeze hash inventory used to prove the descriptive package is untouched |
| `rq1_rq3_reporting_2026-09-21/` | five-run means as exact fractions, SDs as 60-digit decimals, baselines, latency |
| `inferential_2026-09-21/` | bootstrap CIs, paired permutation tests, Holm decisions, exact McNemar |
| `invalid_output_audit_2026-09-25/` | the 1,986 model-invalid records (row-level dataset only) |

Every headline number is listed in `result_provenance.csv` with the file and field it came from
(396 rows, 6 distinct source files).

## Metric policy (unchanged, restated)

`MetricPolicy 1.0.0`. Safety intercepts fire before any model call and are excluded from model attribution.

- **`accuracy_effective` = correct ÷ attributable.** Invalid outputs stay in the denominator.
- **`accuracy_conditional` = correct ÷ valid.** Invalid outputs leave both numerator and denominator, so
  they do not count as wrong.
- **`macro_f1`** = unweighted mean over the fixed label list (Dreaddit `[0, 1]`; GoEmotions
  `[anxiety, fear, sadness, frustration, non_distress]`), with per-class F1 = 0 when undefined.
  Per-class precision, recall and F1 are computed **on valid predictions only**: an invalid output
  contributes nothing to any class's tp, fp or fn. Effective accuracy and macro-F1 therefore weight
  invalid outputs differently — see `inferential_2026-09-21/STATISTICAL_ANALYSIS_PLAN.md` § 7.
- **Five-run value** = mean of the five per-run values ± sample SD (n − 1).

**Effective accuracy is the publication metric.** The frozen statistical plan makes it a primary metric for
RQ1 (with macro-F1) and the primary metric for RQ2; conditional accuracy is carried with confidence intervals
only, with no p-values and no Holm correction. See `RQ1_MODEL_COMPARISON.md` § "Which accuracy belongs in the
main table".

## What the frozen inferential package does and does not contain

| Comparison | Tested? | Where |
|---|---|---|
| Model vs model, within one dataset and one strategy | **Yes** — paired item-level permutation, bootstrap CI, Holm; plus exact McNemar as a secondary family | `rq1_model_pairs_primary.csv`, `rq1_model_pairs_mcnemar.csv` |
| Configuration vs majority baseline | **Yes** — paired permutation, bootstrap CI, Holm, McNemar, plus a baseline-choice sensitivity analysis | `rq2_configuration_vs_baseline.csv` |
| Per-configuration point estimates with CIs | **Yes** — effective accuracy, conditional accuracy, macro-F1 | `configuration_level_ci.csv` |
| **Prompting strategy vs prompting strategy** | **NO** in the frozen package; tested **post-hoc** later | nothing in the frozen package — the plan states "RQ3. No inference." Tested post-hoc in `rq3_strategy_inference_2026-09-25/`; see `SUPERSEDED.md` |
| Latency | **NO** | descriptive only, by design (documented confounds) |

Every strategy statement in `RQ3_PROMPTING_STRATEGIES.md` is therefore **descriptive** with respect to the frozen package. A later post-hoc analysis does test strategy contrasts — see `SUPERSEDED.md`. Validation check 7
enumerates the six frozen Holm families and confirms none of them compares strategies.

## Files

```
final_rq_results_2026-09-25/
├── README.md                              this file
├── RQ1_MODEL_COMPARISON.md                model comparison, per dataset
├── RQ2_BENCHMARK_PERFORMANCE.md           performance vs the majority baseline
├── RQ3_PROMPTING_STRATEGIES.md            strategy comparison (descriptive)
├── LATENCY_ANALYSIS.md                    what latency is, and what may be displayed
├── INVALID_OUTPUT_SELECTION_EFFECT.md     does dropping invalids bias the metrics?
├── FINAL_RESULTS_SUMMARY.md               one-page summary for the paper
├── VALIDATION.md                          12 checks, sources, checksums
├── result_provenance.csv                  396 rows: every headline number → source file + field
├── CHECKSUMS.sha256
├── tables/
│   ├── rq1_dreaddit.csv                   15 rows (5 models × 3 strategies)
│   ├── rq1_goemotions.csv                 15 rows
│   ├── rq2_summary.csv                    30 rows, frozen RQ2 tests copied
│   ├── rq3_accuracy.csv                   30 rows, effective accuracy by strategy
│   ├── rq3_macro_f1.csv                   30 rows, macro-F1 by strategy
│   ├── rq3_inferential.csv                18 rows: what is and is not tested per strategy
│   ├── latency.csv                        30 rows, copied verbatim from the frozen latency tables
│   └── exploratory_invalid_class_composition.csv   30 rows — NEW EXPLORATORY ANALYSIS
└── code/
    ├── 01_build_tables.py                 builds the seven tables + provenance
    ├── 02_exploratory_selection_effect.py NEW EXPLORATORY; clearly separated from the frozen package
    └── 03_validate.py                     the 12 checks + checksums
```

## The one genuinely new calculation

`code/02_exploratory_selection_effect.py` and
`tables/exploratory_invalid_class_composition.csv` are **new exploratory analysis**, created for
`INVALID_OUTPUT_SELECTION_EFFECT.md`. They are not part of the frozen inferential package, their p-values
carry a Holm correction **within their own 30-test family only**, and nothing about them changes any frozen
result. Everything else in this package is copied or arithmetically derived from a frozen file.
