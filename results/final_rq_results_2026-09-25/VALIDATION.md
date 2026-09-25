# VALIDATION — final RQ results package

Generated 2026-09-25T17:06:35.721838+00:00 by `code/03_validate.py`.
This package is read-only with respect to every existing artifact: it reads the frozen packages and
writes only inside `final_rq_results_2026-09-25/`.

## Checks

| # | Check | Result | Detail |
|---|---|---|---|
| 1 | All 5 models x 3 strategies x 2 datasets present in every table | **PASS** | 5 models, 3 strategies, 2 datasets = 30 configurations; rq1 tables 15 rows each; 0 tables with gaps |
| 2 | Five-run point estimates agree across three independent frozen sources | **PASS** | 90 comparisons of acc_eff / acc_cond / macro_f1 across rq12_full_precision.json, inferential configuration_level_ci.csv and rq1_rq3_tables; 0 disagreements (tolerance 1e-9) |
| 3 | Majority baselines match the frozen values | **PASS** | Dreaddit frozen scalar 0.516084 (369/715) and attributable 355/699 = 0.507868; GoEmotions frozen scalar 0.781701 (487/623) and attributable 487/622 = 0.782958 |
| 4 | Latency values are copied verbatim from the frozen latency tables | **PASS** | 30 configurations x 7 fields compared against rq1_rq3_reporting_2026-09-21/tables/rq3_*_latency.csv; 0 mismatches |
| 5 | Invalid-output counts reconcile with the invalid-output audit | **PASS** | sum_N_model_invalid in rq12_full_precision.json vs per-cell row counts in the audit: 0 mismatches across 30 configurations; audit total 1986 (expected 1,986) |
| 6 | Inferential tallies match the frozen inferential tables | **PASS** | RQ1 Holm-significant of 30 pairs: Dreaddit acc_eff 13, macro_f1 20; GoEmotions acc_eff 21, macro_f1 0. RQ2 of 15 per dataset: Dreaddit 15 above / 0 below / 0 n.s.; GoEmotions 2 above / 5 below / 8 n.s. Per-strategy sums in rq3_inferential.csv reproduce the per-dataset totals. |
| 7 | No strategy-vs-strategy hypothesis exists in the frozen inferential package | **PASS** | Frozen Holm families: ['RQ1-mcnemar-dreaddit', 'RQ1-mcnemar-goemotions', 'RQ1-primary-dreaddit', 'RQ1-primary-goemotions', 'RQ2-primary-dreaddit', 'RQ2-primary-goemotions']. None compares prompting strategies; the plan states 'RQ3. No inference.' All RQ3 strategy statements in this package are therefore descriptive. |
| 8 | Every provenance row points at an existing frozen file | **PASS** | 396 provenance rows referencing 6 distinct source files; 0 missing |
| 9 | Frozen descriptive package is byte-identical to its freeze inventory | **PASS** | 32 files compared against verification_2026-09-21/freeze_hashes_after.txt: 0 changed, 0 missing, 0 added |
| 10 | Every upstream file this package reads is present and unmodified | **PASS** | invalid_output_audit_2026-09-25/invalid_outputs_row_level.jsonl matches the audit manifest (yes); the four inferential tables, rq12_full_precision.json and both frozen latency tables were read and are present |
| 11 | Invalid-output audit package matches its own manifest (advisory) | **ADVISORY** | 15 files checked against invalid_output_audit_2026-09-25/CHECKSUMS.sha256; 2 differ: ['cell_level_invalid_vs_quality.csv', 'invalid_output_audit_report.md']. NOTE: these files were modified outside this session's build of this package and are NOT inputs to it — every number here that touches the audit comes from invalid_outputs_row_level.jsonl, which matches its manifest. Re-run that package's own code/05_validate.py to refresh its manifest. |
| 12 | Re-running this package's generators changes nothing outside the new directory | **PASS** | 124 files under results/ outside final_rq_results_2026-09-25/ inventoried (mtime + size), both generators re-run, inventory re-taken: 0 changed |
| 13 | Every decimal number in the prose is traceable to a table value | **PASS** | 7 markdown files scanned against 3345 distinct numeric values from the eight tables and result_provenance.csv (code spans and scientific-notation p-values excluded; 16 documented constants exempt): 0 unmatched |

Overall for this package: **ALL CHECKS PASS** (ADVISORY rows are notices about neighbouring packages; they are reported in full and do not affect this package's status).

## Source artifacts read

| Package | Role |
|---|---|
| `descriptive_2026-09-21` | frozen grid, per-cell metrics, authoritative records |
| `verification_2026-09-21` | independent verification and the freeze hash inventory |
| `rq1_rq3_reporting_2026-09-21` | five-run means/SDs at full precision, baselines, latency |
| `inferential_2026-09-21` | bootstrap CIs, permutation tests, Holm decisions, McNemar |
| `invalid_output_audit_2026-09-25` | 1,986 model-invalid records and their taxonomy |

## Checksums

| file | bytes | sha256 |
|---|---|---|
| `FINAL_RESULTS_SUMMARY.md` | 7,665 | `5e18d7e0685bcbcab697b401f9fa2b61841309508abffd558dd7b6648b4504fe` |
| `INVALID_OUTPUT_SELECTION_EFFECT.md` | 7,961 | `73e8e7c776e537b3923721b7c2f5497564e6e71dce28e617a062abca9b736b5f` |
| `LATENCY_ANALYSIS.md` | 6,051 | `26483ddc6ef791fd9151ce82641cd8d720e25db9e7b9a6e8b1693f36c3526337` |
| `README.md` | 6,025 | `80eab0e14531a2da92a9be926841bdf24ad18e4eb7807e3082a33d59e264df30` |
| `RQ1_MODEL_COMPARISON.md` | 10,995 | `b9cb93c33e22d4c6aca33c907098c34f68075f12a3c078038f360644a539f8ef` |
| `RQ2_BENCHMARK_PERFORMANCE.md` | 7,581 | `43b11923c4037debe5783a811243f7b476890db252a2616a152a0be1897f90ad` |
| `RQ3_PROMPTING_STRATEGIES.md` | 8,313 | `aba34bb2e68ae31f1be89b7bd13e0dc000057a3a96d935f49f22b0b33e2d7050` |
| `code/01_build_tables.py` | 19,892 | `df8dd76789b76c2d58a89d00dc8a1d33b41bef2c85aca9c71fdb7dcfa565efcc` |
| `code/02_exploratory_selection_effect.py` | 6,465 | `10bfd56848fbb576df7ba516eb33fc480f6f0e4e09c03ca95efde46d8fe35e3e` |
| `code/03_validate.py` | 17,997 | `bd8b9ca3dc493538949a416fc7d12ffd408f606428ec22e9b2702bf094640464` |
| `result_provenance.csv` | 79,165 | `08521588fe6ef7111184103b0c1871bc5ceecedd9afb42b75d340b3fcf40def2` |
| `tables/exploratory_invalid_class_composition.csv` | 4,986 | `16965d28d1bea99e96a49dc52a7c72847dcf5a63c04327bf742a47393df73d54` |
| `tables/latency.csv` | 13,332 | `64494f2b6aacc7fb511224bf4664d08f951c522fa42dc490cdf5451b28b1e7e5` |
| `tables/rq1_dreaddit.csv` | 3,925 | `8db8b867c9558e3d714adbd240ee62b5e9a4929aa650fc818629c070a04c7075` |
| `tables/rq1_goemotions.csv` | 3,942 | `b4dd21f9686308a0ed40b858d46e30944f137b5af3de6f72e0cada0cd520916f` |
| `tables/rq2_summary.csv` | 7,559 | `8bb3d135324aa3bc74876bfeb5ac926f36efc1cc1c40c629e1b9f47e83f1f75e` |
| `tables/rq3_accuracy.csv` | 2,743 | `cba9598abb71f0a3a45b222962d16325bb06c17969277f9a18dfd4dbb10a6ff2` |
| `tables/rq3_inferential.csv` | 3,129 | `7d4d259a7ffc5f9eba1a739a0111c130d0e126c745c9031bb06d35d841d06485` |
| `tables/rq3_macro_f1.csv` | 2,748 | `0596a947f11d3b32f148c9691b94a8abac6fb50e5bb633cecb8f371ff759bf28` |
