# Inferential analysis: RQ1 and RQ2 (frozen AnxioSense publication grid)

Date: 2026-09-21. This is analysis material, not manuscript prose. The design is in `STATISTICAL_ANALYSIS_PLAN.md`: it was written and approved (options D1–D4) before any test was run. Nothing frozen was modified:

- raw runs, manifests and `descriptive_2026-09-21`;
- the parser and MetricPolicy 1.0.0;
- `rq1_rq3_reporting_2026-09-21`;
- the verification artifacts.

There were no API calls and no reruns. Every invalid output is kept as frozen, and so is Phi-4 GoEmotions one-shot-CoT run 5. The Gemma Dreaddit replacement is used exactly as frozen: pub_011 for 14 cells, pub_013 for `one-shot-cot|run5`. This is asserted per cell, and the analysis aborts otherwise.

**Measured** = computed from the frozen records. **Interpretation** = a reading of those numbers.

## 0. How to read the tables

- **Items.** Dreaddit n = 699, GoEmotions n = 622 attributable items per configuration. These are the items that were not safety-intercepted; the same set is used in every cell.
- **Values.** Five-run means as frozen (e.g. Dreaddit Llama 4 Scout one-shot-CoT effective accuracy 0.750). Δ = A − B.
- **95% CI.** Item-cluster bootstrap: 4,000 replicates, resampling items with all 15 configurations × 5 runs attached. Percentile intervals. CIs are **per comparison, not multiplicity-adjusted**.
- **p (perm.).** Paired item-level permutation test, 10,000 swap sets. The smallest attainable value is 1/10001, shown as "<0.0001".
- **Holm p.** Holm-adjusted within the pre-declared family:
  - RQ1 primary: 60 per dataset;
  - RQ1 McNemar: 30;
  - RQ2 primary: 15;
  - RQ2 McNemar: 15.
- **"Holm sig."** Holm p ≤ 0.05.
- **McNemar b / c.** Items where A is majority-correct (correct in ≥ 3 of 5 runs) and B is not / the reverse. Exact two-sided test. This is a secondary, conservative check.
- **Effective accuracy.** Invalid output = wrong. **Macro-F1.** Frozen definition, per-class metrics on valid predictions.
- **Conditional accuracy.** CIs only, no tests, because the denominators differ between configurations (plan §B7).
- **Rounding.** 3 decimals for values, effects and CIs; 4 decimals for p; ROUND_HALF_UP of the stored value.
  - One CI bound lies at a 3-decimal half boundary: the GoEmotions Phi-4 zero-shot RQ2 upper bound, stored as −0.02249999999999986 and shown as −0.022.
  - The independent verification found last-bit float differences (≤ 1.1e-16) in CI bounds, so this displayed digit could equally be −0.023. No decision depends on it: the whole interval is below 0.

## 1. Verification status

The independent verification (`verification/verify_inferential.py`, stdlib only, no shared code) **PASSED with 0 discrepancies**:

- 90,512 exact checks;
- 153,530 floating-point checks: 104,818 bit-identical and 48,712 differing only in the last bits (max 4.4e-16);
- all 4,000 × 15 effective-accuracy bootstrap replicates per dataset recomputed;
- 200 × 15 macro-F1 and conditional-accuracy replicates per dataset recomputed;
- every 10th permutation statistic recomputed for accuracy, and every 50th for macro-F1;
- every permutation p, McNemar count and p, Holm value and CI bound re-derived;
- the seeds and draw digests match.

Details are in `verification/VERIFICATION.md`. Observed five-run values equal the frozen `aggregate_results.csv` within 2.2e-16. All input hashes match the frozen values (`source_hashes.txt`).

---

## RQ1: Which LLM yields the best results?

### RQ1 · Dreaddit, effective accuracy (primary; with McNemar check)

| Strategy | Model A | Model B | A value | B value | Δ (A−B) | 95% CI | p (perm.) | Holm p | Holm sig. | McNemar b / c | McNemar Holm p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zero-shot | Gemma 4 31B | Llama 4 Scout | 0.693 | 0.730 | -0.036 | [-0.070, -0.005] | 0.0300 | 0.5399 | no | 64 / 94 | 0.2283 |
| zero-shot | Gemma 4 31B | Mistral Small 4 | 0.693 | 0.686 | +0.007 | [-0.012, +0.027] | 0.4833 | 1.0000 | no | 31 / 25 | 1.0000 |
| zero-shot | Gemma 4 31B | Phi-4 | 0.693 | 0.722 | -0.029 | [-0.057, -0.001] | 0.0470 | 0.7049 | no | 50 / 90 | 0.0146 (sig.) |
| zero-shot | Gemma 4 31B | Qwen3.5 27B | 0.693 | 0.691 | +0.002 | [-0.018, +0.022] | 0.8486 | 1.0000 | no | 29 / 25 | 1.0000 |
| zero-shot | Llama 4 Scout | Mistral Small 4 | 0.730 | 0.686 | +0.043 | [+0.011, +0.077] | 0.0092 | 0.2116 | no | 103 / 67 | 0.0992 |
| zero-shot | Llama 4 Scout | Phi-4 | 0.730 | 0.722 | +0.007 | [-0.014, +0.028] | 0.5025 | 1.0000 | no | 44 / 54 | 1.0000 |
| zero-shot | Llama 4 Scout | Qwen3.5 27B | 0.730 | 0.691 | +0.039 | [+0.006, +0.072] | 0.0253 | 0.4840 | no | 99 / 65 | 0.1268 |
| zero-shot | Mistral Small 4 | Phi-4 | 0.686 | 0.722 | -0.036 | [-0.064, -0.008] | 0.0121 | 0.2662 | no | 46 / 92 | 0.0022 (sig.) |
| zero-shot | Mistral Small 4 | Qwen3.5 27B | 0.686 | 0.691 | -0.005 | [-0.028, +0.018] | 0.7029 | 1.0000 | no | 39 / 41 | 1.0000 |
| zero-shot | Phi-4 | Qwen3.5 27B | 0.722 | 0.691 | +0.031 | [+0.002, +0.061] | 0.0380 | 0.6459 | no | 93 / 49 | 0.0047 (sig.) |
| zero-shot-cot | Gemma 4 31B | Llama 4 Scout | 0.675 | 0.733 | -0.058 | [-0.088, -0.029] | 0.0002 | 0.0066 | **yes** | 47 / 98 | 0.0006 (sig.) |
| zero-shot-cot | Gemma 4 31B | Mistral Small 4 | 0.675 | 0.661 | +0.014 | [-0.006, +0.033] | 0.1943 | 1.0000 | no | 38 / 30 | 1.0000 |
| zero-shot-cot | Gemma 4 31B | Phi-4 | 0.675 | 0.700 | -0.025 | [-0.047, -0.004] | 0.0242 | 0.4840 | no | 35 / 57 | 0.2802 |
| zero-shot-cot | Gemma 4 31B | Qwen3.5 27B | 0.675 | 0.602 | +0.072 | [+0.048, +0.098] | <0.0001 | 0.0060 | **yes** | 70 / 22 | <0.0001 (sig.) |
| zero-shot-cot | Llama 4 Scout | Mistral Small 4 | 0.733 | 0.661 | +0.072 | [+0.041, +0.104] | <0.0001 | 0.0060 | **yes** | 113 / 54 | 0.0001 (sig.) |
| zero-shot-cot | Llama 4 Scout | Phi-4 | 0.733 | 0.700 | +0.033 | [+0.010, +0.056] | 0.0056 | 0.1456 | no | 74 / 45 | 0.1268 |
| zero-shot-cot | Llama 4 Scout | Qwen3.5 27B | 0.733 | 0.602 | +0.131 | [+0.096, +0.167] | <0.0001 | 0.0060 | **yes** | 150 / 51 | <0.0001 (sig.) |
| zero-shot-cot | Mistral Small 4 | Phi-4 | 0.661 | 0.700 | -0.039 | [-0.062, -0.017] | 0.0015 | 0.0420 | **yes** | 37 / 67 | 0.0635 |
| zero-shot-cot | Mistral Small 4 | Qwen3.5 27B | 0.661 | 0.602 | +0.059 | [+0.033, +0.084] | <0.0001 | 0.0060 | **yes** | 70 / 30 | 0.0016 (sig.) |
| zero-shot-cot | Phi-4 | Qwen3.5 27B | 0.700 | 0.602 | +0.098 | [+0.071, +0.126] | <0.0001 | 0.0060 | **yes** | 100 / 30 | <0.0001 (sig.) |
| one-shot-cot | Gemma 4 31B | Llama 4 Scout | 0.676 | 0.750 | -0.075 | [-0.106, -0.043] | <0.0001 | 0.0060 | **yes** | 52 / 105 | 0.0006 (sig.) |
| one-shot-cot | Gemma 4 31B | Mistral Small 4 | 0.676 | 0.674 | +0.002 | [-0.016, +0.020] | 0.8616 | 1.0000 | no | 27 / 26 | 1.0000 |
| one-shot-cot | Gemma 4 31B | Phi-4 | 0.676 | 0.730 | -0.054 | [-0.081, -0.029] | 0.0002 | 0.0066 | **yes** | 41 / 84 | 0.0029 (sig.) |
| one-shot-cot | Gemma 4 31B | Qwen3.5 27B | 0.676 | 0.647 | +0.028 | [+0.008, +0.048] | 0.0079 | 0.1896 | no | 39 / 22 | 0.3566 |
| one-shot-cot | Llama 4 Scout | Mistral Small 4 | 0.750 | 0.674 | +0.077 | [+0.045, +0.109] | <0.0001 | 0.0060 | **yes** | 108 / 54 | 0.0006 (sig.) |
| one-shot-cot | Llama 4 Scout | Phi-4 | 0.750 | 0.730 | +0.020 | [-0.002, +0.042] | 0.0734 | 0.9541 | no | 47 / 37 | 1.0000 |
| one-shot-cot | Llama 4 Scout | Qwen3.5 27B | 0.750 | 0.647 | +0.103 | [+0.067, +0.138] | <0.0001 | 0.0060 | **yes** | 129 / 59 | <0.0001 (sig.) |
| one-shot-cot | Mistral Small 4 | Phi-4 | 0.674 | 0.730 | -0.056 | [-0.083, -0.030] | <0.0001 | 0.0060 | **yes** | 45 / 89 | 0.0032 (sig.) |
| one-shot-cot | Mistral Small 4 | Qwen3.5 27B | 0.674 | 0.647 | +0.026 | [+0.005, +0.048] | 0.0218 | 0.4578 | no | 44 / 28 | 0.6110 |
| one-shot-cot | Phi-4 | Qwen3.5 27B | 0.730 | 0.647 | +0.082 | [+0.053, +0.113] | <0.0001 | 0.0060 | **yes** | 106 / 46 | <0.0001 (sig.) |

### RQ1 · Dreaddit, macro-F1 (primary)

| Strategy | Model A | Model B | A value | B value | Δ (A−B) | 95% CI | p (perm.) | Holm p | Holm sig. |
|---|---|---|---|---|---|---|---|---|---|
| zero-shot | Gemma 4 31B | Llama 4 Scout | 0.675 | 0.752 | -0.077 | [-0.111, -0.045] | <0.0001 | 0.0060 | **yes** |
| zero-shot | Gemma 4 31B | Mistral Small 4 | 0.675 | 0.666 | +0.009 | [-0.013, +0.032] | 0.4222 | 1.0000 | no |
| zero-shot | Gemma 4 31B | Phi-4 | 0.675 | 0.744 | -0.069 | [-0.098, -0.041] | <0.0001 | 0.0060 | **yes** |
| zero-shot | Gemma 4 31B | Qwen3.5 27B | 0.675 | 0.674 | +0.001 | [-0.023, +0.023] | 0.9626 | 1.0000 | no |
| zero-shot | Llama 4 Scout | Mistral Small 4 | 0.752 | 0.666 | +0.086 | [+0.053, +0.120] | <0.0001 | 0.0060 | **yes** |
| zero-shot | Llama 4 Scout | Phi-4 | 0.752 | 0.744 | +0.008 | [-0.014, +0.029] | 0.4467 | 1.0000 | no |
| zero-shot | Llama 4 Scout | Qwen3.5 27B | 0.752 | 0.674 | +0.078 | [+0.045, +0.112] | <0.0001 | 0.0060 | **yes** |
| zero-shot | Mistral Small 4 | Phi-4 | 0.666 | 0.744 | -0.078 | [-0.107, -0.051] | <0.0001 | 0.0060 | **yes** |
| zero-shot | Mistral Small 4 | Qwen3.5 27B | 0.666 | 0.674 | -0.009 | [-0.035, +0.017] | 0.5246 | 1.0000 | no |
| zero-shot | Phi-4 | Qwen3.5 27B | 0.744 | 0.674 | +0.070 | [+0.041, +0.100] | <0.0001 | 0.0060 | **yes** |
| zero-shot-cot | Gemma 4 31B | Llama 4 Scout | 0.650 | 0.742 | -0.092 | [-0.123, -0.062] | <0.0001 | 0.0060 | **yes** |
| zero-shot-cot | Gemma 4 31B | Mistral Small 4 | 0.650 | 0.631 | +0.019 | [-0.004, +0.043] | 0.1283 | 1.0000 | no |
| zero-shot-cot | Gemma 4 31B | Phi-4 | 0.650 | 0.696 | -0.046 | [-0.070, -0.023] | 0.0004 | 0.0120 | **yes** |
| zero-shot-cot | Gemma 4 31B | Qwen3.5 27B | 0.650 | 0.598 | +0.052 | [+0.024, +0.081] | 0.0002 | 0.0066 | **yes** |
| zero-shot-cot | Llama 4 Scout | Mistral Small 4 | 0.742 | 0.631 | +0.111 | [+0.080, +0.144] | <0.0001 | 0.0060 | **yes** |
| zero-shot-cot | Llama 4 Scout | Phi-4 | 0.742 | 0.696 | +0.046 | [+0.023, +0.069] | 0.0004 | 0.0120 | **yes** |
| zero-shot-cot | Llama 4 Scout | Qwen3.5 27B | 0.742 | 0.598 | +0.144 | [+0.108, +0.182] | <0.0001 | 0.0060 | **yes** |
| zero-shot-cot | Mistral Small 4 | Phi-4 | 0.631 | 0.696 | -0.065 | [-0.091, -0.041] | <0.0001 | 0.0060 | **yes** |
| zero-shot-cot | Mistral Small 4 | Qwen3.5 27B | 0.631 | 0.598 | +0.033 | [+0.001, +0.065] | 0.0432 | 0.6911 | no |
| zero-shot-cot | Phi-4 | Qwen3.5 27B | 0.696 | 0.598 | +0.098 | [+0.068, +0.129] | <0.0001 | 0.0060 | **yes** |
| one-shot-cot | Gemma 4 31B | Llama 4 Scout | 0.651 | 0.751 | -0.100 | [-0.132, -0.068] | <0.0001 | 0.0060 | **yes** |
| one-shot-cot | Gemma 4 31B | Mistral Small 4 | 0.651 | 0.648 | +0.003 | [-0.018, +0.024] | 0.8025 | 1.0000 | no |
| one-shot-cot | Gemma 4 31B | Phi-4 | 0.651 | 0.730 | -0.079 | [-0.106, -0.052] | <0.0001 | 0.0060 | **yes** |
| one-shot-cot | Gemma 4 31B | Qwen3.5 27B | 0.651 | 0.610 | +0.040 | [+0.016, +0.066] | 0.0027 | 0.0729 | no |
| one-shot-cot | Llama 4 Scout | Mistral Small 4 | 0.751 | 0.648 | +0.103 | [+0.071, +0.135] | <0.0001 | 0.0060 | **yes** |
| one-shot-cot | Llama 4 Scout | Phi-4 | 0.751 | 0.730 | +0.021 | [-0.001, +0.043] | 0.0679 | 0.9505 | no |
| one-shot-cot | Llama 4 Scout | Qwen3.5 27B | 0.751 | 0.610 | +0.141 | [+0.104, +0.178] | <0.0001 | 0.0060 | **yes** |
| one-shot-cot | Mistral Small 4 | Phi-4 | 0.648 | 0.730 | -0.082 | [-0.110, -0.055] | <0.0001 | 0.0060 | **yes** |
| one-shot-cot | Mistral Small 4 | Qwen3.5 27B | 0.648 | 0.610 | +0.038 | [+0.010, +0.065] | 0.0070 | 0.1750 | no |
| one-shot-cot | Phi-4 | Qwen3.5 27B | 0.730 | 0.610 | +0.120 | [+0.089, +0.153] | <0.0001 | 0.0060 | **yes** |

### RQ1 · GoEmotions, effective accuracy (primary; with McNemar check)

| Strategy | Model A | Model B | A value | B value | Δ (A−B) | 95% CI | p (perm.) | Holm p | Holm sig. | McNemar b / c | McNemar Holm p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zero-shot | Gemma 4 31B | Llama 4 Scout | 0.820 | 0.700 | +0.119 | [+0.090, +0.150] | <0.0001 | 0.0060 | **yes** | 98 / 24 | <0.0001 (sig.) |
| zero-shot | Gemma 4 31B | Mistral Small 4 | 0.820 | 0.766 | +0.054 | [+0.028, +0.079] | <0.0001 | 0.0060 | **yes** | 51 / 22 | 0.0155 (sig.) |
| zero-shot | Gemma 4 31B | Phi-4 | 0.820 | 0.736 | +0.083 | [+0.064, +0.104] | <0.0001 | 0.0060 | **yes** | 45 / 14 | 0.0014 (sig.) |
| zero-shot | Gemma 4 31B | Qwen3.5 27B | 0.820 | 0.786 | +0.033 | [+0.015, +0.052] | 0.0006 | 0.0240 | **yes** | 31 / 10 | 0.0232 (sig.) |
| zero-shot | Llama 4 Scout | Mistral Small 4 | 0.700 | 0.766 | -0.065 | [-0.093, -0.037] | 0.0002 | 0.0092 | **yes** | 30 / 75 | 0.0003 (sig.) |
| zero-shot | Llama 4 Scout | Phi-4 | 0.700 | 0.736 | -0.036 | [-0.064, -0.009] | 0.0124 | 0.4464 | no | 38 / 81 | 0.0021 (sig.) |
| zero-shot | Llama 4 Scout | Qwen3.5 27B | 0.700 | 0.786 | -0.086 | [-0.116, -0.056] | <0.0001 | 0.0060 | **yes** | 30 / 83 | <0.0001 (sig.) |
| zero-shot | Mistral Small 4 | Phi-4 | 0.766 | 0.736 | +0.029 | [+0.002, +0.056] | 0.0343 | 1.0000 | no | 51 / 49 | 1.0000 |
| zero-shot | Mistral Small 4 | Qwen3.5 27B | 0.766 | 0.786 | -0.021 | [-0.046, +0.003] | 0.1028 | 1.0000 | no | 28 / 36 | 1.0000 |
| zero-shot | Phi-4 | Qwen3.5 27B | 0.736 | 0.786 | -0.050 | [-0.072, -0.027] | 0.0002 | 0.0092 | **yes** | 28 / 38 | 1.0000 |
| zero-shot-cot | Gemma 4 31B | Llama 4 Scout | 0.817 | 0.683 | +0.135 | [+0.105, +0.166] | <0.0001 | 0.0060 | **yes** | 110 / 27 | <0.0001 (sig.) |
| zero-shot-cot | Gemma 4 31B | Mistral Small 4 | 0.817 | 0.741 | +0.076 | [+0.047, +0.105] | <0.0001 | 0.0060 | **yes** | 75 / 27 | <0.0001 (sig.) |
| zero-shot-cot | Gemma 4 31B | Phi-4 | 0.817 | 0.762 | +0.056 | [+0.037, +0.074] | <0.0001 | 0.0060 | **yes** | 36 / 11 | 0.0069 (sig.) |
| zero-shot-cot | Gemma 4 31B | Qwen3.5 27B | 0.817 | 0.790 | +0.028 | [+0.008, +0.048] | 0.0076 | 0.2964 | no | 31 / 13 | 0.1147 |
| zero-shot-cot | Llama 4 Scout | Mistral Small 4 | 0.683 | 0.741 | -0.059 | [-0.087, -0.029] | 0.0003 | 0.0129 | **yes** | 43 / 78 | 0.0244 (sig.) |
| zero-shot-cot | Llama 4 Scout | Phi-4 | 0.683 | 0.762 | -0.079 | [-0.108, -0.050] | <0.0001 | 0.0060 | **yes** | 40 / 98 | <0.0001 (sig.) |
| zero-shot-cot | Llama 4 Scout | Qwen3.5 27B | 0.683 | 0.790 | -0.107 | [-0.138, -0.078] | <0.0001 | 0.0060 | **yes** | 27 / 92 | <0.0001 (sig.) |
| zero-shot-cot | Mistral Small 4 | Phi-4 | 0.741 | 0.762 | -0.021 | [-0.051, +0.009] | 0.1850 | 1.0000 | no | 49 / 72 | 0.4505 |
| zero-shot-cot | Mistral Small 4 | Qwen3.5 27B | 0.741 | 0.790 | -0.049 | [-0.076, -0.022] | 0.0004 | 0.0168 | **yes** | 28 / 58 | 0.0232 (sig.) |
| zero-shot-cot | Phi-4 | Qwen3.5 27B | 0.762 | 0.790 | -0.028 | [-0.052, -0.004] | 0.0270 | 0.9179 | no | 36 / 43 | 1.0000 |
| one-shot-cot | Gemma 4 31B | Llama 4 Scout | 0.813 | 0.732 | +0.081 | [+0.055, +0.109] | <0.0001 | 0.0060 | **yes** | 67 / 20 | <0.0001 (sig.) |
| one-shot-cot | Gemma 4 31B | Mistral Small 4 | 0.813 | 0.783 | +0.030 | [+0.009, +0.051] | 0.0079 | 0.3002 | no | 37 / 23 | 0.7397 |
| one-shot-cot | Gemma 4 31B | Phi-4 | 0.813 | 0.673 | +0.140 | [+0.121, +0.160] | <0.0001 | 0.0060 | **yes** | 42 / 17 | 0.0232 (sig.) |
| one-shot-cot | Gemma 4 31B | Qwen3.5 27B | 0.813 | 0.770 | +0.043 | [+0.020, +0.067] | 0.0002 | 0.0092 | **yes** | 43 / 16 | 0.0111 (sig.) |
| one-shot-cot | Llama 4 Scout | Mistral Small 4 | 0.732 | 0.783 | -0.051 | [-0.079, -0.025] | 0.0004 | 0.0168 | **yes** | 30 / 63 | 0.0146 (sig.) |
| one-shot-cot | Llama 4 Scout | Phi-4 | 0.732 | 0.673 | +0.059 | [+0.033, +0.085] | <0.0001 | 0.0060 | **yes** | 36 / 58 | 0.3274 |
| one-shot-cot | Llama 4 Scout | Qwen3.5 27B | 0.732 | 0.770 | -0.038 | [-0.068, -0.008] | 0.0111 | 0.4107 | no | 39 / 59 | 0.4895 |
| one-shot-cot | Mistral Small 4 | Phi-4 | 0.783 | 0.673 | +0.110 | [+0.085, +0.136] | <0.0001 | 0.0060 | **yes** | 52 / 41 | 1.0000 |
| one-shot-cot | Mistral Small 4 | Qwen3.5 27B | 0.783 | 0.770 | +0.013 | [-0.011, +0.036] | 0.3009 | 1.0000 | no | 40 / 27 | 0.9945 |
| one-shot-cot | Phi-4 | Qwen3.5 27B | 0.673 | 0.770 | -0.097 | [-0.125, -0.071] | <0.0001 | 0.0060 | **yes** | 51 / 49 | 1.0000 |

### RQ1 · GoEmotions, macro-F1 (primary)

| Strategy | Model A | Model B | A value | B value | Δ (A−B) | 95% CI | p (perm.) | Holm p | Holm sig. |
|---|---|---|---|---|---|---|---|---|---|
| zero-shot | Gemma 4 31B | Llama 4 Scout | 0.593 | 0.520 | +0.073 | [-0.013, +0.145] | 0.0271 | 0.9179 | no |
| zero-shot | Gemma 4 31B | Mistral Small 4 | 0.593 | 0.561 | +0.032 | [-0.029, +0.088] | 0.2624 | 1.0000 | no |
| zero-shot | Gemma 4 31B | Phi-4 | 0.593 | 0.534 | +0.059 | [+0.003, +0.113] | 0.0212 | 0.7419 | no |
| zero-shot | Gemma 4 31B | Qwen3.5 27B | 0.593 | 0.572 | +0.021 | [-0.018, +0.058] | 0.2501 | 1.0000 | no |
| zero-shot | Llama 4 Scout | Mistral Small 4 | 0.520 | 0.561 | -0.041 | [-0.097, +0.017] | 0.0966 | 1.0000 | no |
| zero-shot | Llama 4 Scout | Phi-4 | 0.520 | 0.534 | -0.014 | [-0.069, +0.048] | 0.6125 | 1.0000 | no |
| zero-shot | Llama 4 Scout | Qwen3.5 27B | 0.520 | 0.572 | -0.052 | [-0.120, +0.031] | 0.0956 | 1.0000 | no |
| zero-shot | Mistral Small 4 | Phi-4 | 0.561 | 0.534 | +0.027 | [-0.021, +0.077] | 0.2997 | 1.0000 | no |
| zero-shot | Mistral Small 4 | Qwen3.5 27B | 0.561 | 0.572 | -0.011 | [-0.063, +0.044] | 0.6763 | 1.0000 | no |
| zero-shot | Phi-4 | Qwen3.5 27B | 0.534 | 0.572 | -0.038 | [-0.091, +0.013] | 0.1472 | 1.0000 | no |
| zero-shot-cot | Gemma 4 31B | Llama 4 Scout | 0.583 | 0.530 | +0.054 | [-0.036, +0.128] | 0.1327 | 1.0000 | no |
| zero-shot-cot | Gemma 4 31B | Mistral Small 4 | 0.583 | 0.536 | +0.048 | [-0.022, +0.114] | 0.1468 | 1.0000 | no |
| zero-shot-cot | Gemma 4 31B | Phi-4 | 0.583 | 0.563 | +0.020 | [-0.031, +0.070] | 0.4213 | 1.0000 | no |
| zero-shot-cot | Gemma 4 31B | Qwen3.5 27B | 0.583 | 0.579 | +0.004 | [-0.033, +0.042] | 0.8333 | 1.0000 | no |
| zero-shot-cot | Llama 4 Scout | Mistral Small 4 | 0.530 | 0.536 | -0.006 | [-0.059, +0.048] | 0.8053 | 1.0000 | no |
| zero-shot-cot | Llama 4 Scout | Phi-4 | 0.530 | 0.563 | -0.034 | [-0.090, +0.030] | 0.2278 | 1.0000 | no |
| zero-shot-cot | Llama 4 Scout | Qwen3.5 27B | 0.530 | 0.579 | -0.050 | [-0.123, +0.036] | 0.1457 | 1.0000 | no |
| zero-shot-cot | Mistral Small 4 | Phi-4 | 0.536 | 0.563 | -0.028 | [-0.073, +0.022] | 0.3000 | 1.0000 | no |
| zero-shot-cot | Mistral Small 4 | Qwen3.5 27B | 0.536 | 0.579 | -0.044 | [-0.101, +0.021] | 0.1359 | 1.0000 | no |
| zero-shot-cot | Phi-4 | Qwen3.5 27B | 0.563 | 0.579 | -0.016 | [-0.063, +0.031] | 0.5216 | 1.0000 | no |
| one-shot-cot | Gemma 4 31B | Llama 4 Scout | 0.585 | 0.544 | +0.041 | [-0.036, +0.105] | 0.2095 | 1.0000 | no |
| one-shot-cot | Gemma 4 31B | Mistral Small 4 | 0.585 | 0.594 | -0.009 | [-0.067, +0.045] | 0.7415 | 1.0000 | no |
| one-shot-cot | Gemma 4 31B | Phi-4 | 0.585 | 0.541 | +0.045 | [-0.001, +0.094] | 0.0719 | 1.0000 | no |
| one-shot-cot | Gemma 4 31B | Qwen3.5 27B | 0.585 | 0.567 | +0.018 | [-0.026, +0.061] | 0.3963 | 1.0000 | no |
| one-shot-cot | Llama 4 Scout | Mistral Small 4 | 0.544 | 0.594 | -0.050 | [-0.113, +0.022] | 0.0847 | 1.0000 | no |
| one-shot-cot | Llama 4 Scout | Phi-4 | 0.544 | 0.541 | +0.004 | [-0.052, +0.070] | 0.9050 | 1.0000 | no |
| one-shot-cot | Llama 4 Scout | Qwen3.5 27B | 0.544 | 0.567 | -0.023 | [-0.084, +0.049] | 0.4478 | 1.0000 | no |
| one-shot-cot | Mistral Small 4 | Phi-4 | 0.594 | 0.541 | +0.053 | [+0.004, +0.103] | 0.0369 | 1.0000 | no |
| one-shot-cot | Mistral Small 4 | Qwen3.5 27B | 0.594 | 0.567 | +0.027 | [-0.015, +0.072] | 0.2231 | 1.0000 | no |
| one-shot-cot | Phi-4 | Qwen3.5 27B | 0.541 | 0.567 | -0.027 | [-0.072, +0.016] | 0.2838 | 1.0000 | no |

Conditional-accuracy differences (CIs only) are in `tables/rq1_dreaddit_conditional.md` and `tables/rq1_goemotions_conditional.md`.

### RQ1 · Measured

**Dreaddit** (family of 60): 33 comparisons are Holm-significant, 13 of 30 on effective accuracy and 20 of 30 on macro-F1.

- **Llama 4 Scout and Phi-4 vs Gemma 4 31B, Mistral Small 4 and Qwen3.5 27B** (18 pairs over 3 strategies):
  - All 18 observed differences favour Llama or Phi-4.
  - **18 of 18 are Holm-significant on macro-F1.** Examples: one-shot-CoT Llama − Mistral +0.103 [+0.071, +0.135]; Llama − Qwen +0.141 [+0.104, +0.178].
  - **11 of 18 are Holm-significant on effective accuracy.**
- **Under zero-shot**, none of those 6 pairs is Holm-significant on effective accuracy (Δ between +0.029 and +0.043), although all 6 are on macro-F1 (Δ +0.069 to +0.086).
  - At zero-shot, Llama and Phi-4 have 106 invalid outputs each over five runs, which count as wrong in effective accuracy.
  - The McNemar majority-vote check is significant for 3 of those 6 pairs (Gemma vs Phi-4, Mistral vs Phi-4, Phi-4 vs Qwen).
- **Llama 4 Scout vs Phi-4** is Holm-significant only on zero-shot-CoT macro-F1: +0.046 [+0.023, +0.069], Holm p 0.0120. It is not significant on:
  - zero-shot (acc. +0.007, F1 +0.008);
  - one-shot-CoT (acc. +0.020, F1 +0.021);
  - zero-shot-CoT effective accuracy (+0.033, Holm p 0.1456).
- **Among Gemma, Mistral and Qwen:**
  - Gemma vs Mistral is not significant under any strategy or metric.
  - Qwen is lower than Gemma and Mistral under zero-shot-CoT: Gemma − Qwen acc. +0.072, F1 +0.052; Mistral − Qwen acc. +0.059.
- **Primary and McNemar disagree on 4 of 30 accuracy pairs** (listed in `summary_counts.json`).

**GoEmotions** (family of 60): 21 of 30 effective-accuracy comparisons are Holm-significant; **0 of 30 macro-F1 comparisons are.**

- **Effective accuracy, Gemma 4 31B:**
  - Higher than Llama 4 Scout and Phi-4 under all three strategies (Δ +0.056 to +0.140).
  - Higher than Mistral under zero-shot (+0.054) and zero-shot-CoT (+0.076), but not one-shot-CoT (+0.030, Holm p 0.3002).
  - Higher than Qwen under zero-shot (+0.033, Holm p 0.0240) and one-shot-CoT (+0.043), but not zero-shot-CoT (+0.028).
- **Effective accuracy, Llama and Phi-4 vs Gemma/Mistral/Qwen:** 17 of 18 observed differences favour Gemma, Mistral or Qwen, and 14 of 18 are Holm-significant.
- **Macro-F1:**
  - No difference survives Holm. Only 3 of 30 have raw p < 0.05.
  - Observed |Δ| ranges from 0.004 to 0.073.
  - The CIs are wide (width 0.075–0.164) because of the rare classes.
- **Phi-4 one-shot-CoT** (which includes the frozen run-5 collapse) is significantly below Gemma, Llama, Mistral and Qwen on effective accuracy under the primary test. McNemar does **not** confirm it against Llama, Mistral or Qwen, because the majority vote over 5 runs absorbs a failure confined mostly to one run.
- **Primary and McNemar disagree on 5 of 30 accuracy pairs.**

**Monte Carlo sensitivity.** P = 10,000 permutations gives each p-value some simulation error. For these Holm-significant decisions, the 99% Monte Carlo range of Holm p crosses 0.05:

- Dreaddit zero-shot-CoT Mistral vs Phi-4, effective accuracy: Holm p 0.0420, range 0.019–0.0712;
- GoEmotions zero-shot Gemma vs Qwen, effective accuracy: Holm p 0.0240, range 0.006–0.0524.

Dreaddit one-shot-CoT Gemma vs Qwen macro-F1 (Holm p 0.0729) could cross in the other direction. These three are fragile. See `summary_counts.json` → `monte_carlo_sensitivity`.

### RQ1 · Interpretation

- **Dreaddit.** The data support a two-tier structure: Llama 4 Scout and Phi-4 above Gemma 4 31B, Mistral Small 4 and Qwen3.5 27B.
  - On macro-F1 this holds for every such pair under every strategy.
  - On effective accuracy it holds under zero-shot-CoT (except Gemma vs Phi-4) and one-shot-CoT, but not under zero-shot, where the two leaders' invalid outputs shrink the gap below what the test can separate.
  - The data do **not** support a single best model: Llama and Phi-4 are distinguishable in 1 of 6 strategy × metric comparisons.
- **GoEmotions.** Effective accuracy favours Gemma over most alternatives. Macro-F1, which is the class-balanced measure relevant to distress-class detection, separates **no** pair of models. Because 78% of attributable items are non_distress, the accuracy differences largely reflect agreement on that majority class.
- **Across datasets,** the model groupings reverse. "Which LLM is best" has a dataset- and metric-specific answer, not a single one.

---

## RQ2: What is the accuracy of AnxioSense?

As in the descriptive report, **no single overall AnxioSense accuracy is defined, and none is computed.** Inference is per configuration, against the majority baseline.

- **Primary baseline:** the constant majority-class predictor, scored on the same attributable items and resampled together with the configuration (355/699 = 0.508 Dreaddit; 487/622 = 0.783 GoEmotions).
- **Sensitivity (last column):** the fixed frozen scalar (0.516 and 0.782), CI only.

### RQ2 · Dreaddit

| Model | Strategy | Eff. acc. [95% CI] | Baseline (attrib.) | Δ vs baseline [95% CI] | p (perm.) | Holm p | Holm sig. | McNemar b / c | McNemar Holm p | Sensitivity: Δ vs frozen scalar [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot | 0.693 [0.659, 0.727] | 0.508 | +0.185 [+0.123, +0.249] | <0.0001 | 0.0015 | **yes** | 326 / 194 | <0.0001 (sig.) | +0.177 [+0.143, +0.211] |
| Gemma 4 31B | zero-shot-cot | 0.675 [0.641, 0.709] | 0.508 | +0.167 [+0.104, +0.232] | <0.0001 | 0.0015 | **yes** | 327 / 212 | <0.0001 (sig.) | +0.159 [+0.125, +0.193] |
| Gemma 4 31B | one-shot-cot | 0.676 [0.642, 0.709] | 0.508 | +0.168 [+0.104, +0.232] | <0.0001 | 0.0015 | **yes** | 328 / 214 | <0.0001 (sig.) | +0.159 [+0.126, +0.193] |
| Llama 4 Scout | zero-shot | 0.730 [0.700, 0.759] | 0.508 | +0.222 [+0.171, +0.274] | <0.0001 | 0.0015 | **yes** | 271 / 109 | <0.0001 (sig.) | +0.214 [+0.184, +0.243] |
| Llama 4 Scout | zero-shot-cot | 0.733 [0.703, 0.763] | 0.508 | +0.225 [+0.173, +0.278] | <0.0001 | 0.0015 | **yes** | 284 / 118 | <0.0001 (sig.) | +0.217 [+0.187, +0.247] |
| Llama 4 Scout | one-shot-cot | 0.750 [0.720, 0.780] | 0.508 | +0.242 [+0.189, +0.295] | <0.0001 | 0.0015 | **yes** | 279 / 112 | <0.0001 (sig.) | +0.234 [+0.204, +0.264] |
| Mistral Small 4 | zero-shot | 0.686 [0.652, 0.719] | 0.508 | +0.178 [+0.116, +0.241] | <0.0001 | 0.0015 | **yes** | 328 / 202 | <0.0001 (sig.) | +0.170 [+0.136, +0.203] |
| Mistral Small 4 | zero-shot-cot | 0.661 [0.627, 0.695] | 0.508 | +0.153 [+0.088, +0.219] | <0.0001 | 0.0015 | **yes** | 332 / 225 | <0.0001 (sig.) | +0.145 [+0.111, +0.179] |
| Mistral Small 4 | one-shot-cot | 0.674 [0.639, 0.706] | 0.508 | +0.166 [+0.103, +0.230] | <0.0001 | 0.0015 | **yes** | 330 / 217 | <0.0001 (sig.) | +0.157 [+0.123, +0.190] |
| Phi-4 | zero-shot | 0.722 [0.695, 0.750] | 0.508 | +0.214 [+0.165, +0.264] | <0.0001 | 0.0015 | **yes** | 286 / 114 | <0.0001 (sig.) | +0.206 [+0.179, +0.234] |
| Phi-4 | zero-shot-cot | 0.700 [0.671, 0.730] | 0.508 | +0.192 [+0.135, +0.249] | <0.0001 | 0.0015 | **yes** | 309 / 172 | <0.0001 (sig.) | +0.184 [+0.155, +0.214] |
| Phi-4 | one-shot-cot | 0.730 [0.702, 0.758] | 0.508 | +0.222 [+0.170, +0.275] | <0.0001 | 0.0015 | **yes** | 291 / 134 | <0.0001 (sig.) | +0.214 [+0.186, +0.242] |
| Qwen3.5 27B | zero-shot | 0.691 [0.657, 0.724] | 0.508 | +0.183 [+0.120, +0.244] | <0.0001 | 0.0015 | **yes** | 324 / 196 | <0.0001 (sig.) | +0.175 [+0.141, +0.208] |
| Qwen3.5 27B | zero-shot-cot | 0.602 [0.566, 0.638] | 0.508 | +0.094 [+0.025, +0.161] | 0.0067 | 0.0067 | **yes** | 329 / 262 | 0.0066 (sig.) | +0.086 [+0.050, +0.122] |
| Qwen3.5 27B | one-shot-cot | 0.647 [0.613, 0.681] | 0.508 | +0.140 [+0.074, +0.206] | <0.0001 | 0.0015 | **yes** | 335 / 238 | 0.0001 (sig.) | +0.131 [+0.097, +0.165] |

### RQ2 · GoEmotions

| Model | Strategy | Eff. acc. [95% CI] | Baseline (attrib.) | Δ vs baseline [95% CI] | p (perm.) | Holm p | Holm sig. | McNemar b / c | McNemar Holm p | Sensitivity: Δ vs frozen scalar [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot | 0.820 [0.791, 0.849] | 0.783 | +0.037 [+0.012, +0.062] | 0.0043 | 0.0440 | **yes** | 45 / 22 | 0.0876 | +0.038 [+0.009, +0.067] |
| Gemma 4 31B | zero-shot-cot | 0.817 [0.787, 0.847] | 0.783 | +0.034 [+0.010, +0.059] | 0.0043 | 0.0440 | **yes** | 40 / 19 | 0.1037 | +0.036 [+0.005, +0.065] |
| Gemma 4 31B | one-shot-cot | 0.813 [0.783, 0.842] | 0.783 | +0.030 [+0.005, +0.056] | 0.0206 | 0.1648 | no | 45 / 26 | 0.3193 | +0.031 [+0.001, +0.061] |
| Llama 4 Scout | zero-shot | 0.700 [0.667, 0.734] | 0.783 | -0.083 [-0.120, -0.044] | <0.0001 | 0.0015 | **yes** | 60 / 111 | 0.0017 (sig.) | -0.081 [-0.115, -0.047] |
| Llama 4 Scout | zero-shot-cot | 0.683 [0.648, 0.716] | 0.783 | -0.100 [-0.139, -0.062] | <0.0001 | 0.0015 | **yes** | 62 / 124 | <0.0001 (sig.) | -0.099 [-0.134, -0.066] |
| Llama 4 Scout | one-shot-cot | 0.732 [0.698, 0.766] | 0.783 | -0.051 [-0.086, -0.017] | 0.0040 | 0.0440 | **yes** | 51 / 79 | 0.1930 | -0.050 [-0.084, -0.016] |
| Mistral Small 4 | zero-shot | 0.766 [0.732, 0.798] | 0.783 | -0.017 [-0.054, +0.019] | 0.3398 | 1.0000 | no | 66 / 72 | 1.0000 | -0.016 [-0.050, +0.016] |
| Mistral Small 4 | zero-shot-cot | 0.741 [0.706, 0.774] | 0.783 | -0.042 [-0.080, -0.004] | 0.0310 | 0.2170 | no | 65 / 92 | 0.3388 | -0.041 [-0.075, -0.008] |
| Mistral Small 4 | one-shot-cot | 0.783 [0.752, 0.813] | 0.783 | 0.000 [-0.032, +0.032] | 1.0000 | 1.0000 | no | 59 / 54 | 1.0000 | +0.001 [-0.030, +0.031] |
| Phi-4 | zero-shot | 0.736 [0.706, 0.766] | 0.783 | -0.047 [-0.070, -0.022] | 0.0004 | 0.0048 | **yes** | 33 / 41 | 1.0000 | -0.045 [-0.075, -0.016] |
| Phi-4 | zero-shot-cot | 0.762 [0.731, 0.792] | 0.783 | -0.021 [-0.045, +0.003] | 0.0937 | 0.5621 | no | 31 / 35 | 1.0000 | -0.020 [-0.051, +0.011] |
| Phi-4 | one-shot-cot | 0.673 [0.646, 0.700] | 0.783 | -0.110 [-0.132, -0.086] | <0.0001 | 0.0015 | **yes** | 27 / 33 | 1.0000 | -0.109 [-0.135, -0.082] |
| Qwen3.5 27B | zero-shot | 0.786 [0.753, 0.818] | 0.783 | +0.003 [-0.028, +0.034] | 0.8625 | 1.0000 | no | 51 / 49 | 1.0000 | +0.004 [-0.028, +0.036] |
| Qwen3.5 27B | zero-shot-cot | 0.790 [0.758, 0.821] | 0.783 | +0.007 [-0.024, +0.039] | 0.6884 | 1.0000 | no | 52 / 49 | 1.0000 | +0.008 [-0.024, +0.040] |
| Qwen3.5 27B | one-shot-cot | 0.770 [0.738, 0.804] | 0.783 | -0.013 [-0.048, +0.023] | 0.5288 | 1.0000 | no | 60 / 68 | 1.0000 | -0.012 [-0.044, +0.022] |

Configuration-level 95% CIs for effective accuracy, conditional accuracy and macro-F1: `tables/cfg_dreaddit.md`, `tables/cfg_goemotions.md`.

### RQ2 · Measured

**Dreaddit.**
- All 15 configurations are above the paired baseline and Holm-significant, under both the permutation test and McNemar.
- The effects range from +0.094 [+0.025, +0.161] (Qwen zero-shot-CoT) to +0.242 [+0.189, +0.295] (Llama one-shot-CoT).
- The sensitivity CIs against the frozen 0.516 all exclude 0 as well.
- The paired CIs are wider than the sensitivity CIs (e.g. ±0.06 vs ±0.03). The baseline's own item-sampling variability is included, and those models' correctness is negatively related to the majority-class indicator: they are more accurate on class-0 items.

**GoEmotions.**
- **Holm-significantly above baseline: 2 of 15.** Gemma zero-shot, +0.037 [+0.012, +0.062], and zero-shot-CoT, +0.034 [+0.010, +0.059], both at Holm p 0.0440.
  - Both are Monte Carlo-fragile: the 99% range of Holm p is 0.0313–0.0537.
  - McNemar does not confirm them (Holm p 0.0876 and 0.1037).
- **Holm-significantly below baseline: 5 of 15.**
  - Llama zero-shot −0.083;
  - Llama zero-shot-CoT −0.100;
  - Llama one-shot-CoT −0.051 (Holm p 0.0440, Monte Carlo-fragile);
  - Phi-4 zero-shot −0.047;
  - Phi-4 one-shot-CoT −0.110.
- **Not distinguishable from baseline: 8 of 15.** This includes Gemma one-shot-CoT, all three Mistral configurations, all three Qwen configurations and Phi-4 zero-shot-CoT.
- The fixed-scalar sensitivity CIs exclude 0 for 3 configurations above and 6 below.
- **Macro-F1 vs the constant predictor** (descriptive; not tested because the constant's value is trivially low):
  - Constant predictor: 0.337 on Dreaddit and 0.176 on GoEmotions.
  - Every configuration is far higher. Lowest configuration CI lower bounds: 0.559 (Dreaddit Qwen zero-shot-CoT) and 0.442 (GoEmotions Phi-4 one-shot-CoT).
  - GoEmotions macro-F1 CIs are wide, e.g. Gemma zero-shot 0.593 [0.482, 0.671].

### RQ2 · Interpretation

- **Dreaddit** (binary stress vs non-stress, via the Referral agent): every configuration's effective accuracy is above the majority baseline, with effects of roughly +0.09 to +0.24 and CIs excluding 0.
- **GoEmotions** (Emotion agent, 5 classes, 78% majority class): no configuration is robustly above baseline on effective accuracy. At most two Gemma configurations are, marginally and Monte Carlo-fragile. Five are below. Accuracy therefore gives no evidence that the emotion pipeline beats "always non_distress".
  - Macro-F1 shows the configurations do discriminate among classes far better than the constant predictor.
  - These two statements are compatible: they measure different things under heavy class imbalance.
- **"AnxioSense accuracy"** is configuration- and dataset-specific:
  - Dreaddit effective accuracy 0.602–0.750;
  - GoEmotions effective accuracy 0.673–0.820, with only a minority of configurations distinguishable from its baseline.

---

## RQ3

Not analysed inferentially, as planned. The confounds in `rq1_rq3_reporting_2026-09-21/REPORT.md` (3 s quantisation, fixed strategy order, machine, provider and time, concurrent load for Llama Dreaddit, no per-agent timing) mean no test could attribute a latency difference to the prompting strategy. RQ3 remains descriptive.

---

## What the inferential results establish and do not establish

**Descriptive vs statistically supported.**
- Differences in the descriptive tables are observations.
- Only rows marked "Holm sig." in the pre-declared families are statistically supported differences.
- Everything else, including every GoEmotions macro-F1 model difference, is **not** shown to differ.
- A non-significant result is not evidence of equality. Some CIs are wide enough to include practically meaningful differences, e.g. GoEmotions macro-F1 CIs up to 0.164 wide.

**Practical effect sizes.**
- Supported Dreaddit model differences are 0.046–0.144 in macro-F1.
- Supported GoEmotions accuracy differences are 0.033–0.140.
- Dreaddit gains over baseline are 0.094–0.242.
- Whether these magnitudes matter for screening is a substantive judgement these statistics do not make.

**Fragile results.** Five Holm-significant decisions have 99% Monte Carlo ranges that cross 0.05:
- 2 in RQ1: Dreaddit zero-shot-CoT Mistral vs Phi-4, and GoEmotions zero-shot Gemma vs Qwen, both effective accuracy;
- 3 in RQ2: GoEmotions Gemma zero-shot and zero-shot-CoT, and Llama one-shot-CoT.

One non-significant decision could also cross: Dreaddit one-shot-CoT Gemma vs Qwen macro-F1. Several significant results are also not confirmed by McNemar. None of these should carry a conclusion on its own.

**Repeated runs.**
- Inference is over items. The 5 runs are averaged within items and never counted as independent observations.
- Intervals are conditional on the 5 observed runs. They do not capture run-to-run variability beyond those runs, and the runs were not resampled.
- The McNemar check uses majority vote, which discards within-item run disagreement. That is why it disagrees with the primary test for Phi-4 one-shot-CoT on GoEmotions.

**Invalid outputs.**
- Effective accuracy and macro-F1 keep invalid outputs as frozen: counted wrong in accuracy, and contributing nothing to tp/fp/fn in macro-F1.
- The two metrics weight invalid outputs differently, which explains part of their disagreement (e.g. Dreaddit zero-shot).
- Conditional accuracy has only CIs, on changing denominators.

**Class imbalance.**
- GoEmotions accuracy is dominated by non_distress (487/622).
- The anxiety class has 6 items. 14 of 4,000 bootstrap replicates contained no anxiety item, and its F1 was set to 0 as the frozen policy requires.
- No per-class inference was performed, and none should be drawn for anxiety.

**Dataset and task limits.**
- Dreaddit is stress vs non-stress, scored from the Referral agent's risk level. It does not validate anxiety detection or the GoEmotions `anxiety` class.
- Both datasets are Reddit text.
- Results are conditional on the frozen parser, MetricPolicy 1.0.0 and the serving routes used (e.g. Gemma via CoreWeave fp4).

**Clinical limits.** Nothing here is clinical validation. There is no clinical population, no clinician reference standard, and no deployment outcome.

**Protocol differences.**
- The July setup document's Wilcoxon + Bonferroni plan was not used, because it cannot reach p < 0.05 with 5 runs and ignores item sampling (plan §B12).
- Cohen's weighted κ and symptom-extraction metrics named there are not part of the frozen scoring and were not analysed.

**RQ3.** Latency remains descriptive and confounded. No inferential claim about prompting-strategy efficiency is made.
