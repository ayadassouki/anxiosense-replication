# Validation — RQ3 strategy inference (2026-09-25)

**32 of 32 checks passed.**

Every check re-derives its quantity independently of the analysis run: permutation p-values and bootstrap
intervals are recomputed from the saved replicate files, Holm is recomputed from the raw p-values, and the
frozen packages are re-hashed.

| # | Check | Result | Detail |
|---|---|---|---|
| 1 | Pre-check ran and every pre-condition check passed | PASS | 38/38 |
| 2 | Strategy arms use identical attributable item sets in every model x run group | PASS | dreaddit 0/25 and goemotions 0/25 groups differ; n = 699 / 622 |
| 3 | Every comparison uses n = items, not item-run records and not runs | PASS | n = 699 (not 3,495; not 5) / n = 622 (not 3,110; not 5) |
| 4 | Every file named in PREREGISTRATION_FREEZE.json still matches its frozen SHA-256 | PASS | 5 files; frozen 2026-09-25T22:04:33Z |
| 5 | The analysis code that ran is the code that was frozen | PASS | 6bce537485fbcfa2... |
| 6 | Freeze timestamp precedes the analysis timestamp | PASS | 2026-09-25T22:04:33Z <= 2026-09-25T22:04:45Z |
| 7 | All four frozen input artifacts still match their recorded SHA-256 | PASS | 4 inputs |
| 8 | Inputs are byte-identical to those used by the frozen 2026-09-21 inferential analysis | PASS |  |
| 9 | All 150 per-run and 30 five-run frozen metric values reproduced from the raw grid | PASS | max |observed - frozen| = 2.220e-16 |
| 10 | Bootstrap and permutation draws are bit-identical to the frozen 2026-09-21 draws | PASS | same seed strings, same digests |
| 11 | Configuration-level bootstrap CIs are string-identical to inferential_2026-09-21/configuration_level_ci.csv | PASS | 30 configurations x 10 fields, 0 mismatches |
| 12 | Row counts: 60 primary, 30 McNemar, 30 conditional-accuracy CI, 30 configuration CI | PASS | 60/30/30/30 |
| 13 | Holm families are exactly as declared (30 / 30 primary, 15 / 15 McNemar) | PASS | {"RQ3-primary-dreaddit": 30, "RQ3-mcnemar-dreaddit": 15, "RQ3-primary-goemotions": 30, "RQ3-mcnemar-goemotions": 15} |
| 14 | All 5 models x 3 declared contrasts x 2 metrics x 2 datasets are present and reported | PASS | 60 distinct |
| 15 | Holm-adjusted p-values and significance flags recomputed independently from the raw p-values | PASS | 0 disagreements over 90 rows |
| 16 | Holm-adjusted p is never below the unadjusted p | PASS |  |
| 17 | Every permutation p-value is of the form (1 + k) / (1 + P) with P = 10,000 | PASS | minimum attainable p = 0.000100 |
| 18 | All 60 permutation p-values re-derived from the saved permutation statistics | PASS | 60 re-derived, 0 disagreements |
| 19 | All 60 bootstrap 95% CIs re-derived from the saved bootstrap replicates | PASS | 60 re-derived, 0 disagreements |
| 20 | The three contrasts are internally consistent: d(ZS,1S-CoT) = d(ZS,ZS-CoT) + d(ZS-CoT,1S-CoT) | PASS | 20 model x metric x dataset cells, 0 violations |
| 21 | Invalid-output counts on every row match the frozen per-run sums | PASS | 0 mismatches over 120 values |
| 22 | Evaluability = 1 - invalid rate on the attributable denominator for every arm (no conditioning on validity) | PASS | 0 mismatches over 120 values |
| 23 | Conditional accuracy is reported with CIs only and carries no p-value or Holm decision | PASS | 30 rows, fields: dataset, model, strategy_A, strategy_B, A_acc_cond, A_sd... |
| 24 | No pooled strategy main effect and no family spanning both datasets | PASS | every row is one model x one dataset; families are per dataset |
| 25 | Bootstrap replicates containing no GoEmotions 'anxiety' item are recorded | PASS | 14 of 4000 |
| 26 | Every output file matches the SHA-256 recorded in analysis_manifest.json | PASS | 12 files, 0 mismatches |
| 27 | descriptive_2026-09-21: all 32 files still byte-identical to the 2026-09-21 freeze inventory | PASS | 32 files, 0 changed |
| 28 | inferential_2026-09-21: present and untouched by this analysis (no manifest of its own to verify) | PASS | read-only access only |
| 29 | final_rq_results_2026-09-25: verifies against its own CHECKSUMS.sha256 | PASS | 0 mismatches |
| 30 | unified_results_tables_2026-09-25: verifies against its own CHECKSUMS.sha256 | PASS | 0 mismatches |
| 31 | rq3_inference_design_2026-09-25: present and untouched by this analysis (no manifest of its own to verify) | PASS | read-only access only |
| 32 | invalid_output_audit_2026-09-25: pre-existing manifest advisory unchanged by this analysis | PASS | 2 files still failing that package's own manifest (pre-existing, not caused here): cell_level_invalid_vs_quality.csv, invalid_output_audit_report.md |
