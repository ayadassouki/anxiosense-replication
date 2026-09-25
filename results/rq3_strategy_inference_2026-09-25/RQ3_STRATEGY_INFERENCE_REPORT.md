# RQ3 — prompting-strategy inferential analysis

**Status: POST-HOC / EXPLORATORY.** This analysis uses frozen experimental data and a method that was
selected and frozen **before** any RQ3 test was run, but the contrasts were chosen **after** the descriptive
strategy results were known. It is therefore exploratory. No result below confirms a hypothesis, and RQ1 and
RQ2 remain the paper's pre-specified confirmatory analyses.

| | |
|---|---|
| Plan | `RQ3_SAP_ADDENDUM.md`, frozen `2026-09-25T22:04:33Z` |
| Analysis executed | `2026-09-25T22:04:45Z` |
| Estimation procedure | `inferential_2026-09-21/STATISTICAL_ANALYSIS_PLAN.md`, applied **unchanged** |
| Validation | **32 of 32 checks passed** (`VALIDATION.md`) |
| Environment | Python 3.10.12, numpy 2.2.6 |

---

## 1. What was tested

**RQ3 (classification-quality reading).** Within each model and dataset, does the prompting strategy change
classification performance?

| Element | As executed |
|---|---|
| Statistical unit | The benchmark item, carrying all five runs. n = 699 (Dreaddit), 622 (GoEmotions) |
| Contrasts | zero-shot vs zero-shot-CoT; zero-shot vs one-shot-CoT; zero-shot-CoT vs one-shot-CoT — within model, within dataset |
| Primary outcomes | Effective accuracy and Macro-F1 (co-primary) |
| Invalid outputs | Counted as **incorrect** on the attributable denominator; the analysis is **not** conditioned on valid outputs |
| Primary test | Paired item-level permutation, whole five-run vector swapped per item, P = 10,000; Macro-F1 recomputed after each permutation |
| Intervals | Item-cluster bootstrap, B = 4,000, shared resampled index per dataset, 95% percentile |
| Correction | Holm within each dataset across the **30** primary comparisons (5 models × 3 pairs × 2 metrics) |
| Threshold | α = 0.05 on the Holm-adjusted p |
| Secondary | Exact McNemar on majority-vote (≥ 3/5) effective correctness, own family of 15 per dataset |
| Descriptive only | Conditional accuracy and evaluability — CIs, **no p-values** |
| Pooling | None. No strategy main effect across models; no family spanning both datasets |

**Pre-conditions verified and recorded before the plan was frozen** (`precheck.json`, 38/38 checks):

- The three strategy arms are scored on **identical attributable item sets**. Checking every model × run
  group directly: **0 of 25 groups differ on Dreaddit and 0 of 25 on GoEmotions.** One full item set and one
  safety-intercept set exist per dataset across all 75 cells, so the pairing is complete — no item is missing
  from any arm and no complete-case deletion occurs anywhere in the primary analysis.
- The **five runs are not treated as independent observations**. The data are held as
  `(item × strategy × run)` arrays — `(699, 3, 5)` and `(622, 3, 5)` — and the run axis is never folded into
  the item axis. Independent units are 699 / 622 **items**, not 3,495 / 3,110
  item-run records and not 5 runs. Runs are never paired across arms and never resampled.

---

## 2. Headline

| Dataset | Effective accuracy | Macro-F1 | Total | McNemar (secondary) |
|---|---|---|---|---|
| Dreaddit | 7 / 15 Holm-significant | 7 / 15 | **14 / 30** | 7 / 15 |
| GoEmotions | 6 / 15 | **0 / 15** | **6 / 30** | 3 / 15 |

All 30 comparisons per dataset are reported below, significant or not, as the frozen addendum requires.

---

## 3. Dreaddit — all 30 primary comparisons (n = 699 items)

### 3.1 Effective accuracy

| Model | Contrast (A vs B) | A: mean ± SD | B: mean ± SD | Diff (A−B) | 95% CI | p (unadj.) | p (Holm) | Sig. at .05 |
|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot vs zero-shot-CoT | 0.6933 ± 0.0040 | 0.6747 ± 0.0008 | +0.0186 | [+0.0094, +0.0280] | &lt;0.0001 | 0.0030 | **yes** |
| Gemma 4 31B | zero-shot vs one-shot-CoT | 0.6933 ± 0.0040 | 0.6755 ± 0.0064 | +0.0177 | [+0.0089, +0.0278] | 0.0005 | 0.0085 | **yes** |
| Gemma 4 31B | zero-shot-CoT vs one-shot-CoT | 0.6747 ± 0.0008 | 0.6755 ± 0.0064 | −0.0009 | [−0.0074, +0.0057] | 0.8651 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs zero-shot-CoT | 0.7296 ± 0.0027 | 0.7330 ± 0.0049 | −0.0034 | [−0.0166, +0.0103] | 0.6537 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs one-shot-CoT | 0.7296 ± 0.0027 | 0.7502 ± 0.0049 | −0.0206 | [−0.0349, −0.0063] | 0.0061 | 0.0976 | no |
| Llama 4 Scout | zero-shot-CoT vs one-shot-CoT | 0.7330 ± 0.0049 | 0.7502 ± 0.0049 | −0.0172 | [−0.0303, −0.0037] | 0.0129 | 0.1806 | no |
| Mistral Small 4 | zero-shot vs zero-shot-CoT | 0.6861 ± 0.0036 | 0.6609 ± 0.0042 | +0.0252 | [+0.0126, +0.0381] | 0.0002 | 0.0042 | **yes** |
| Mistral Small 4 | zero-shot vs one-shot-CoT | 0.6861 ± 0.0036 | 0.6735 ± 0.0053 | +0.0126 | [+0.0011, +0.0243] | 0.0365 | 0.3650 | no |
| Mistral Small 4 | zero-shot-CoT vs one-shot-CoT | 0.6609 ± 0.0042 | 0.6735 ± 0.0053 | −0.0126 | [−0.0237, −0.0014] | 0.0304 | 0.3344 | no |
| Phi-4 | zero-shot vs zero-shot-CoT | 0.7222 ± 0.0164 | 0.7001 ± 0.0022 | +0.0220 | [+0.0029, +0.0409] | 0.0262 | 0.3144 | no |
| Phi-4 | zero-shot vs one-shot-CoT | 0.7222 ± 0.0164 | 0.7299 ± 0.0101 | −0.0077 | [−0.0235, +0.0083] | 0.3629 | 1.0000 | no |
| Phi-4 | zero-shot-CoT vs one-shot-CoT | 0.7001 ± 0.0022 | 0.7299 ± 0.0101 | −0.0298 | [−0.0455, −0.0137] | 0.0004 | 0.0072 | **yes** |
| Qwen3.5 27B | zero-shot vs zero-shot-CoT | 0.6910 ± 0.0014 | 0.6023 ± 0.0049 | +0.0887 | [+0.0655, +0.1122] | &lt;0.0001 | 0.0030 | **yes** |
| Qwen3.5 27B | zero-shot vs one-shot-CoT | 0.6910 ± 0.0014 | 0.6475 ± 0.0016 | +0.0435 | [+0.0249, +0.0627] | &lt;0.0001 | 0.0030 | **yes** |
| Qwen3.5 27B | zero-shot-CoT vs one-shot-CoT | 0.6023 ± 0.0049 | 0.6475 ± 0.0016 | −0.0452 | [−0.0655, −0.0249] | &lt;0.0001 | 0.0030 | **yes** |

### 3.2 Macro-F1

| Model | Contrast (A vs B) | A: mean ± SD | B: mean ± SD | Diff (A−B) | 95% CI | p (unadj.) | p (Holm) | Sig. at .05 |
|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot vs zero-shot-CoT | 0.6748 ± 0.0049 | 0.6503 ± 0.0009 | +0.0245 | [+0.0141, +0.0357] | &lt;0.0001 | 0.0030 | **yes** |
| Gemma 4 31B | zero-shot vs one-shot-CoT | 0.6748 ± 0.0049 | 0.6510 ± 0.0080 | +0.0238 | [+0.0132, +0.0356] | &lt;0.0001 | 0.0030 | **yes** |
| Gemma 4 31B | zero-shot-CoT vs one-shot-CoT | 0.6503 ± 0.0009 | 0.6510 ± 0.0080 | −0.0006 | [−0.0084, +0.0071] | 0.8719 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs zero-shot-CoT | 0.7519 ± 0.0050 | 0.7424 ± 0.0048 | +0.0095 | [−0.0032, +0.0224] | 0.1451 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs one-shot-CoT | 0.7519 ± 0.0050 | 0.7510 ± 0.0045 | +0.0009 | [−0.0131, +0.0149] | 0.9003 | 1.0000 | no |
| Llama 4 Scout | zero-shot-CoT vs one-shot-CoT | 0.7424 ± 0.0048 | 0.7510 ± 0.0045 | −0.0086 | [−0.0218, +0.0047] | 0.2031 | 1.0000 | no |
| Mistral Small 4 | zero-shot vs zero-shot-CoT | 0.6657 ± 0.0041 | 0.6312 ± 0.0042 | +0.0345 | [+0.0196, +0.0501] | 0.0002 | 0.0042 | **yes** |
| Mistral Small 4 | zero-shot vs one-shot-CoT | 0.6657 ± 0.0041 | 0.6481 ± 0.0061 | +0.0176 | [+0.0042, +0.0315] | 0.0106 | 0.1590 | no |
| Mistral Small 4 | zero-shot-CoT vs one-shot-CoT | 0.6312 ± 0.0042 | 0.6481 ± 0.0061 | −0.0169 | [−0.0306, −0.0038] | 0.0133 | 0.1806 | no |
| Phi-4 | zero-shot vs zero-shot-CoT | 0.7439 ± 0.0126 | 0.6964 ± 0.0038 | +0.0475 | [+0.0292, +0.0657] | &lt;0.0001 | 0.0030 | **yes** |
| Phi-4 | zero-shot vs one-shot-CoT | 0.7439 ± 0.0126 | 0.7302 ± 0.0101 | +0.0136 | [−0.0021, +0.0296] | 0.0897 | 0.8072 | no |
| Phi-4 | zero-shot-CoT vs one-shot-CoT | 0.6964 ± 0.0038 | 0.7302 ± 0.0101 | −0.0339 | [−0.0502, −0.0179] | 0.0003 | 0.0057 | **yes** |
| Qwen3.5 27B | zero-shot vs zero-shot-CoT | 0.6742 ± 0.0012 | 0.5983 ± 0.0061 | +0.0760 | [+0.0515, +0.1010] | &lt;0.0001 | 0.0030 | **yes** |
| Qwen3.5 27B | zero-shot vs one-shot-CoT | 0.6742 ± 0.0012 | 0.6105 ± 0.0020 | +0.0638 | [+0.0417, +0.0871] | &lt;0.0001 | 0.0030 | **yes** |
| Qwen3.5 27B | zero-shot-CoT vs one-shot-CoT | 0.5983 ± 0.0061 | 0.6105 ± 0.0020 | −0.0122 | [−0.0356, +0.0114] | 0.2939 | 1.0000 | no |

### 3.3 Invalid-output context for the same 15 contrasts

Effective accuracy counts an invalid output as incorrect, so a change in parseability moves it directly.
`Effective = Conditional × Evaluability` and `Evaluability = 1 − invalid rate` hold exactly. This table is a
**descriptive companion**, not a mediation analysis: it shows how much of a contrast co-occurs with a change
in parseability, and says nothing about what caused what.

| Model | Contrast (A vs B) | Invalid A (Σ5) | Invalid B (Σ5) | Evaluability A | Evaluability B | Δ evaluability (A−B) | 95% CI |
|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot vs zero-shot-CoT | 0 | 0 | 1.0000 | 1.0000 | +0.0000 | [+0.0000, +0.0000] |
| Gemma 4 31B | zero-shot vs one-shot-CoT | 0 | 0 | 1.0000 | 1.0000 | +0.0000 | [+0.0000, +0.0000] |
| Gemma 4 31B | zero-shot-CoT vs one-shot-CoT | 0 | 0 | 1.0000 | 1.0000 | +0.0000 | [+0.0000, +0.0000] |
| Llama 4 Scout | zero-shot vs zero-shot-CoT | 106 | 52 | 0.9697 | 0.9851 | −0.0155 | [−0.0229, −0.0080] |
| Llama 4 Scout | zero-shot vs one-shot-CoT | 106 | 8 | 0.9697 | 0.9977 | −0.0280 | [−0.0352, −0.0212] |
| Llama 4 Scout | zero-shot-CoT vs one-shot-CoT | 52 | 8 | 0.9851 | 0.9977 | −0.0126 | [−0.0172, −0.0083] |
| Mistral Small 4 | zero-shot vs zero-shot-CoT | 1 | 1 | 0.9997 | 0.9997 | +0.0000 | [+0.0000, +0.0000] |
| Mistral Small 4 | zero-shot vs one-shot-CoT | 1 | 0 | 0.9997 | 1.0000 | −0.0003 | [−0.0009, +0.0000] |
| Mistral Small 4 | zero-shot-CoT vs one-shot-CoT | 1 | 0 | 0.9997 | 1.0000 | −0.0003 | [−0.0009, +0.0000] |
| Phi-4 | zero-shot vs zero-shot-CoT | 106 | 29 | 0.9697 | 0.9917 | −0.0220 | [−0.0286, −0.0155] |
| Phi-4 | zero-shot vs one-shot-CoT | 106 | 16 | 0.9697 | 0.9954 | −0.0258 | [−0.0323, −0.0195] |
| Phi-4 | zero-shot-CoT vs one-shot-CoT | 29 | 16 | 0.9917 | 0.9954 | −0.0037 | [−0.0072, −0.0003] |
| Qwen3.5 27B | zero-shot vs zero-shot-CoT | 7 | 269 | 0.9980 | 0.9230 | +0.0750 | [+0.0567, +0.0936] |
| Qwen3.5 27B | zero-shot vs one-shot-CoT | 7 | 4 | 0.9980 | 0.9989 | −0.0009 | [−0.0023, +0.0000] |
| Qwen3.5 27B | zero-shot-CoT vs one-shot-CoT | 269 | 4 | 0.9230 | 0.9989 | −0.0758 | [−0.0944, −0.0575] |

### 3.4 Secondary — exact McNemar on majority-vote correctness (≥ 3 of 5 runs)

| Model | Contrast (A vs B) | A majority-correct | B majority-correct | b | c | Δ majority acc. | p exact | p (Holm) | Sig. at .05 |
|---|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot vs zero-shot-CoT | 487 | 470 | 20 | 3 | +0.0243 | 0.0005 | 0.0049 | **yes** |
| Gemma 4 31B | zero-shot vs one-shot-CoT | 487 | 469 | 20 | 2 | +0.0258 | 0.0001 | 0.0015 | **yes** |
| Gemma 4 31B | zero-shot-CoT vs one-shot-CoT | 470 | 469 | 7 | 6 | +0.0014 | 1.0000 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs zero-shot-CoT | 517 | 521 | 19 | 23 | −0.0057 | 0.6440 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs one-shot-CoT | 517 | 522 | 18 | 23 | −0.0072 | 0.5327 | 1.0000 | no |
| Llama 4 Scout | zero-shot-CoT vs one-shot-CoT | 521 | 522 | 22 | 23 | −0.0014 | 1.0000 | 1.0000 | no |
| Mistral Small 4 | zero-shot vs zero-shot-CoT | 481 | 462 | 29 | 10 | +0.0272 | 0.0034 | 0.0304 | **yes** |
| Mistral Small 4 | zero-shot vs one-shot-CoT | 481 | 468 | 23 | 10 | +0.0186 | 0.0351 | 0.2639 | no |
| Mistral Small 4 | zero-shot-CoT vs one-shot-CoT | 462 | 468 | 11 | 17 | −0.0086 | 0.3449 | 1.0000 | no |
| Phi-4 | zero-shot vs zero-shot-CoT | 527 | 492 | 62 | 27 | +0.0501 | 0.0003 | 0.0029 | **yes** |
| Phi-4 | zero-shot vs one-shot-CoT | 527 | 512 | 48 | 33 | +0.0215 | 0.1193 | 0.7156 | no |
| Phi-4 | zero-shot-CoT vs one-shot-CoT | 492 | 512 | 30 | 50 | −0.0286 | 0.0330 | 0.2639 | no |
| Qwen3.5 27B | zero-shot vs zero-shot-CoT | 483 | 422 | 71 | 10 | +0.0873 | &lt;0.0001 | &lt;0.0001 | **yes** |
| Qwen3.5 27B | zero-shot vs one-shot-CoT | 483 | 452 | 42 | 11 | +0.0443 | &lt;0.0001 | 0.0003 | **yes** |
| Qwen3.5 27B | zero-shot-CoT vs one-shot-CoT | 422 | 452 | 12 | 42 | −0.0429 | &lt;0.0001 | 0.0007 | **yes** |

### 3.5 Conditional accuracy — descriptive, no test

Denominators differ by arm, so these are not comparable across strategies and carry no p-value.

| Model | Contrast (A vs B) | A cond. acc. ± SD | B cond. acc. ± SD | Diff (A−B) | 95% CI |
|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot vs zero-shot-CoT | 0.6933 ± 0.0040 | 0.6747 ± 0.0008 | +0.0186 | [+0.0094, +0.0280] |
| Gemma 4 31B | zero-shot vs one-shot-CoT | 0.6933 ± 0.0040 | 0.6755 ± 0.0064 | +0.0177 | [+0.0089, +0.0278] |
| Gemma 4 31B | zero-shot-CoT vs one-shot-CoT | 0.6747 ± 0.0008 | 0.6755 ± 0.0064 | −0.0009 | [−0.0074, +0.0057] |
| Llama 4 Scout | zero-shot vs zero-shot-CoT | 0.7525 ± 0.0050 | 0.7441 ± 0.0046 | +0.0083 | [−0.0043, +0.0213] |
| Llama 4 Scout | zero-shot vs one-shot-CoT | 0.7525 ± 0.0050 | 0.7519 ± 0.0044 | +0.0005 | [−0.0134, +0.0144] |
| Llama 4 Scout | zero-shot-CoT vs one-shot-CoT | 0.7441 ± 0.0046 | 0.7519 ± 0.0044 | −0.0078 | [−0.0208, +0.0053] |
| Mistral Small 4 | zero-shot vs zero-shot-CoT | 0.6863 ± 0.0033 | 0.6611 ± 0.0039 | +0.0252 | [+0.0126, +0.0381] |
| Mistral Small 4 | zero-shot vs one-shot-CoT | 0.6863 ± 0.0033 | 0.6735 ± 0.0053 | +0.0128 | [+0.0013, +0.0246] |
| Mistral Small 4 | zero-shot-CoT vs one-shot-CoT | 0.6611 ± 0.0039 | 0.6735 ± 0.0053 | −0.0124 | [−0.0237, −0.0012] |
| Phi-4 | zero-shot vs zero-shot-CoT | 0.7447 ± 0.0124 | 0.7060 ± 0.0031 | +0.0387 | [+0.0198, +0.0572] |
| Phi-4 | zero-shot vs one-shot-CoT | 0.7447 ± 0.0124 | 0.7333 ± 0.0098 | +0.0115 | [−0.0038, +0.0270] |
| Phi-4 | zero-shot-CoT vs one-shot-CoT | 0.7060 ± 0.0031 | 0.7333 ± 0.0098 | −0.0272 | [−0.0431, −0.0113] |
| Qwen3.5 27B | zero-shot vs zero-shot-CoT | 0.6924 ± 0.0010 | 0.6525 ± 0.0035 | +0.0399 | [+0.0211, +0.0588] |
| Qwen3.5 27B | zero-shot vs one-shot-CoT | 0.6924 ± 0.0010 | 0.6482 ± 0.0014 | +0.0441 | [+0.0254, +0.0634] |
| Qwen3.5 27B | zero-shot-CoT vs one-shot-CoT | 0.6525 ± 0.0035 | 0.6482 ± 0.0014 | +0.0043 | [−0.0121, +0.0207] |

---

## 4. GoEmotions — all 30 primary comparisons (n = 622 items)

### 4.1 Effective accuracy

| Model | Contrast (A vs B) | A: mean ± SD | B: mean ± SD | Diff (A−B) | 95% CI | p (unadj.) | p (Holm) | Sig. at .05 |
|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot vs zero-shot-CoT | 0.8196 ± 0.0038 | 0.8174 ± 0.0037 | +0.0023 | [−0.0045, +0.0100] | 0.6032 | 1.0000 | no |
| Gemma 4 31B | zero-shot vs one-shot-CoT | 0.8196 ± 0.0038 | 0.8132 ± 0.0029 | +0.0064 | [+0.0006, +0.0129] | 0.0478 | 0.8125 | no |
| Gemma 4 31B | zero-shot-CoT vs one-shot-CoT | 0.8174 ± 0.0037 | 0.8132 ± 0.0029 | +0.0042 | [−0.0032, +0.0113] | 0.3070 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs zero-shot-CoT | 0.7003 ± 0.0084 | 0.6826 ± 0.0092 | +0.0177 | [−0.0026, +0.0383] | 0.0867 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs one-shot-CoT | 0.7003 ± 0.0084 | 0.7318 ± 0.0092 | −0.0315 | [−0.0550, −0.0077] | 0.0082 | 0.1886 | no |
| Llama 4 Scout | zero-shot-CoT vs one-shot-CoT | 0.6826 ± 0.0092 | 0.7318 ± 0.0092 | −0.0492 | [−0.0714, −0.0264] | 0.0002 | 0.0054 | **yes** |
| Mistral Small 4 | zero-shot vs zero-shot-CoT | 0.7656 ± 0.0053 | 0.7412 ± 0.0078 | +0.0244 | [+0.0116, +0.0386] | 0.0005 | 0.0125 | **yes** |
| Mistral Small 4 | zero-shot vs one-shot-CoT | 0.7656 ± 0.0053 | 0.7830 ± 0.0047 | −0.0174 | [−0.0322, −0.0022] | 0.0265 | 0.5459 | no |
| Mistral Small 4 | zero-shot-CoT vs one-shot-CoT | 0.7412 ± 0.0078 | 0.7830 ± 0.0047 | −0.0418 | [−0.0598, −0.0244] | &lt;0.0001 | 0.0030 | **yes** |
| Phi-4 | zero-shot vs zero-shot-CoT | 0.7363 ± 0.0164 | 0.7617 ± 0.0090 | −0.0254 | [−0.0383, −0.0125] | 0.0002 | 0.0054 | **yes** |
| Phi-4 | zero-shot vs one-shot-CoT | 0.7363 ± 0.0164 | 0.6730 ± 0.1258 | +0.0633 | [+0.0463, +0.0810] | &lt;0.0001 | 0.0030 | **yes** |
| Phi-4 | zero-shot-CoT vs one-shot-CoT | 0.7617 ± 0.0090 | 0.6730 ± 0.1258 | +0.0887 | [+0.0717, +0.1061] | &lt;0.0001 | 0.0030 | **yes** |
| Qwen3.5 27B | zero-shot vs zero-shot-CoT | 0.7862 ± 0.0011 | 0.7897 ± 0.0021 | −0.0035 | [−0.0119, +0.0048] | 0.4572 | 1.0000 | no |
| Qwen3.5 27B | zero-shot vs one-shot-CoT | 0.7862 ± 0.0011 | 0.7701 ± 0.0000 | +0.0161 | [−0.0013, +0.0344] | 0.0854 | 1.0000 | no |
| Qwen3.5 27B | zero-shot-CoT vs one-shot-CoT | 0.7897 ± 0.0021 | 0.7701 ± 0.0000 | +0.0196 | [+0.0032, +0.0370] | 0.0278 | 0.5459 | no |

### 4.2 Macro-F1

| Model | Contrast (A vs B) | A: mean ± SD | B: mean ± SD | Diff (A−B) | 95% CI | p (unadj.) | p (Holm) | Sig. at .05 |
|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot vs zero-shot-CoT | 0.5932 ± 0.0071 | 0.5832 ± 0.0082 | +0.0099 | [−0.0005, +0.0226] | 0.0836 | 1.0000 | no |
| Gemma 4 31B | zero-shot vs one-shot-CoT | 0.5932 ± 0.0071 | 0.5852 ± 0.0055 | +0.0079 | [−0.0071, +0.0235] | 0.3064 | 1.0000 | no |
| Gemma 4 31B | zero-shot-CoT vs one-shot-CoT | 0.5832 ± 0.0082 | 0.5852 ± 0.0055 | −0.0020 | [−0.0178, +0.0143] | 0.8048 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs zero-shot-CoT | 0.5202 ± 0.0175 | 0.5296 ± 0.0134 | −0.0095 | [−0.0397, +0.0218] | 0.5257 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs one-shot-CoT | 0.5202 ± 0.0175 | 0.5443 ± 0.0126 | −0.0241 | [−0.0632, +0.0172] | 0.2061 | 1.0000 | no |
| Llama 4 Scout | zero-shot-CoT vs one-shot-CoT | 0.5296 ± 0.0134 | 0.5443 ± 0.0126 | −0.0147 | [−0.0575, +0.0278] | 0.5067 | 1.0000 | no |
| Mistral Small 4 | zero-shot vs zero-shot-CoT | 0.5615 ± 0.0106 | 0.5357 ± 0.0104 | +0.0258 | [+0.0027, +0.0496] | 0.0240 | 0.5279 | no |
| Mistral Small 4 | zero-shot vs one-shot-CoT | 0.5615 ± 0.0106 | 0.5940 ± 0.0079 | −0.0325 | [−0.0683, +0.0026] | 0.0369 | 0.6641 | no |
| Mistral Small 4 | zero-shot-CoT vs one-shot-CoT | 0.5357 ± 0.0104 | 0.5940 ± 0.0079 | −0.0583 | [−0.0999, −0.0164] | 0.0021 | 0.0504 | no |
| Phi-4 | zero-shot vs zero-shot-CoT | 0.5342 ± 0.0161 | 0.5634 ± 0.0105 | −0.0292 | [−0.0556, −0.0030] | 0.0260 | 0.5459 | no |
| Phi-4 | zero-shot vs one-shot-CoT | 0.5342 ± 0.0161 | 0.5406 ± 0.0494 | −0.0064 | [−0.0419, +0.0324] | 0.7218 | 1.0000 | no |
| Phi-4 | zero-shot-CoT vs one-shot-CoT | 0.5634 ± 0.0105 | 0.5406 ± 0.0494 | +0.0229 | [−0.0068, +0.0544] | 0.1552 | 1.0000 | no |
| Qwen3.5 27B | zero-shot vs zero-shot-CoT | 0.5723 ± 0.0071 | 0.5793 ± 0.0060 | −0.0070 | [−0.0254, +0.0124] | 0.4902 | 1.0000 | no |
| Qwen3.5 27B | zero-shot vs one-shot-CoT | 0.5723 ± 0.0071 | 0.5673 ± 0.0000 | +0.0050 | [−0.0208, +0.0350] | 0.7399 | 1.0000 | no |
| Qwen3.5 27B | zero-shot-CoT vs one-shot-CoT | 0.5793 ± 0.0060 | 0.5673 ± 0.0000 | +0.0120 | [−0.0182, +0.0447] | 0.4511 | 1.0000 | no |

**Not one** of the 15 Macro-F1 contrasts reaches significance after Holm correction. The correct word is
**inconclusive**, not "no difference": class supports on the attributable pool are non_distress 487,
frustration 81, sadness 33, fear 15, **anxiety 6**, so one fifth of Macro-F1 rests on six items and the
intervals are correspondingly wide. 14 of
4,000 bootstrap replicates contain no `anxiety` item at all; per MetricPolicy 1.0.0 its recall and F1
are 0 in those replicates, applied verbatim. This mirrors the frozen RQ1 result, where 0 of 30 GoEmotions
Macro-F1 model contrasts were significant either.

### 4.3 Invalid-output context

| Model | Contrast (A vs B) | Invalid A (Σ5) | Invalid B (Σ5) | Evaluability A | Evaluability B | Δ evaluability (A−B) | 95% CI |
|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot vs zero-shot-CoT | 0 | 0 | 1.0000 | 1.0000 | +0.0000 | [+0.0000, +0.0000] |
| Gemma 4 31B | zero-shot vs one-shot-CoT | 0 | 7 | 1.0000 | 0.9977 | +0.0023 | [+0.0006, +0.0042] |
| Gemma 4 31B | zero-shot-CoT vs one-shot-CoT | 0 | 7 | 1.0000 | 0.9977 | +0.0023 | [+0.0006, +0.0042] |
| Llama 4 Scout | zero-shot vs zero-shot-CoT | 113 | 193 | 0.9637 | 0.9379 | +0.0257 | [+0.0145, +0.0376] |
| Llama 4 Scout | zero-shot vs one-shot-CoT | 113 | 143 | 0.9637 | 0.9540 | +0.0096 | [−0.0013, +0.0215] |
| Llama 4 Scout | zero-shot-CoT vs one-shot-CoT | 193 | 143 | 0.9379 | 0.9540 | −0.0161 | [−0.0277, −0.0048] |
| Mistral Small 4 | zero-shot vs zero-shot-CoT | 17 | 19 | 0.9945 | 0.9939 | +0.0006 | [−0.0029, +0.0045] |
| Mistral Small 4 | zero-shot vs one-shot-CoT | 17 | 12 | 0.9945 | 0.9961 | −0.0016 | [−0.0048, +0.0013] |
| Mistral Small 4 | zero-shot-CoT vs one-shot-CoT | 19 | 12 | 0.9939 | 0.9961 | −0.0023 | [−0.0058, +0.0003] |
| Phi-4 | zero-shot vs zero-shot-CoT | 191 | 183 | 0.9386 | 0.9412 | −0.0026 | [−0.0138, +0.0090] |
| Phi-4 | zero-shot vs one-shot-CoT | 191 | 499 | 0.9386 | 0.8395 | +0.0990 | [+0.0839, +0.1141] |
| Phi-4 | zero-shot-CoT vs one-shot-CoT | 183 | 499 | 0.9412 | 0.8395 | +0.1016 | [+0.0855, +0.1174] |
| Qwen3.5 27B | zero-shot vs zero-shot-CoT | 0 | 0 | 1.0000 | 1.0000 | +0.0000 | [+0.0000, +0.0000] |
| Qwen3.5 27B | zero-shot vs one-shot-CoT | 0 | 10 | 1.0000 | 0.9968 | +0.0032 | [+0.0000, +0.0080] |
| Qwen3.5 27B | zero-shot-CoT vs one-shot-CoT | 0 | 10 | 1.0000 | 0.9968 | +0.0032 | [+0.0000, +0.0080] |

### 4.4 Secondary — exact McNemar on majority-vote correctness (≥ 3 of 5 runs)

| Model | Contrast (A vs B) | A majority-correct | B majority-correct | b | c | Δ majority acc. | p exact | p (Holm) | Sig. at .05 |
|---|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot vs zero-shot-CoT | 510 | 508 | 5 | 3 | +0.0032 | 0.7266 | 1.0000 | no |
| Gemma 4 31B | zero-shot vs one-shot-CoT | 510 | 506 | 6 | 2 | +0.0064 | 0.2891 | 1.0000 | no |
| Gemma 4 31B | zero-shot-CoT vs one-shot-CoT | 508 | 506 | 7 | 5 | +0.0032 | 0.7744 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs zero-shot-CoT | 436 | 425 | 40 | 29 | +0.0177 | 0.2284 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs one-shot-CoT | 436 | 459 | 31 | 54 | −0.0370 | 0.0165 | 0.1981 | no |
| Llama 4 Scout | zero-shot-CoT vs one-shot-CoT | 425 | 459 | 24 | 58 | −0.0547 | 0.0002 | 0.0029 | **yes** |
| Mistral Small 4 | zero-shot vs zero-shot-CoT | 481 | 460 | 24 | 3 | +0.0338 | &lt;0.0001 | 0.0007 | **yes** |
| Mistral Small 4 | zero-shot vs one-shot-CoT | 481 | 492 | 13 | 24 | −0.0177 | 0.0989 | 0.9887 | no |
| Mistral Small 4 | zero-shot-CoT vs one-shot-CoT | 460 | 492 | 13 | 45 | −0.0514 | &lt;0.0001 | 0.0005 | **yes** |
| Phi-4 | zero-shot vs zero-shot-CoT | 479 | 483 | 15 | 19 | −0.0064 | 0.6076 | 1.0000 | no |
| Phi-4 | zero-shot vs one-shot-CoT | 479 | 481 | 22 | 24 | −0.0032 | 0.8830 | 1.0000 | no |
| Phi-4 | zero-shot-CoT vs one-shot-CoT | 483 | 481 | 23 | 21 | +0.0032 | 0.8804 | 1.0000 | no |
| Qwen3.5 27B | zero-shot vs zero-shot-CoT | 489 | 490 | 4 | 5 | −0.0016 | 1.0000 | 1.0000 | no |
| Qwen3.5 27B | zero-shot vs one-shot-CoT | 489 | 479 | 21 | 11 | +0.0161 | 0.1102 | 0.9917 | no |
| Qwen3.5 27B | zero-shot-CoT vs one-shot-CoT | 490 | 479 | 21 | 10 | +0.0177 | 0.0708 | 0.7783 | no |

### 4.5 Conditional accuracy — descriptive, no test

| Model | Contrast (A vs B) | A cond. acc. ± SD | B cond. acc. ± SD | Diff (A−B) | 95% CI |
|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot vs zero-shot-CoT | 0.8196 ± 0.0038 | 0.8174 ± 0.0037 | +0.0023 | [−0.0045, +0.0100] |
| Gemma 4 31B | zero-shot vs one-shot-CoT | 0.8196 ± 0.0038 | 0.8150 ± 0.0041 | +0.0046 | [−0.0011, +0.0109] |
| Gemma 4 31B | zero-shot-CoT vs one-shot-CoT | 0.8174 ± 0.0037 | 0.8150 ± 0.0041 | +0.0023 | [−0.0048, +0.0091] |
| Llama 4 Scout | zero-shot vs zero-shot-CoT | 0.7267 ± 0.0071 | 0.7278 ± 0.0103 | −0.0011 | [−0.0190, +0.0173] |
| Llama 4 Scout | zero-shot vs one-shot-CoT | 0.7267 ± 0.0071 | 0.7671 ± 0.0084 | −0.0404 | [−0.0618, −0.0184] |
| Llama 4 Scout | zero-shot-CoT vs one-shot-CoT | 0.7278 ± 0.0103 | 0.7671 ± 0.0084 | −0.0393 | [−0.0609, −0.0169] |
| Mistral Small 4 | zero-shot vs zero-shot-CoT | 0.7698 ± 0.0076 | 0.7457 ± 0.0072 | +0.0241 | [+0.0116, +0.0375] |
| Mistral Small 4 | zero-shot vs one-shot-CoT | 0.7698 ± 0.0076 | 0.7860 ± 0.0046 | −0.0162 | [−0.0308, −0.0010] |
| Mistral Small 4 | zero-shot-CoT vs one-shot-CoT | 0.7457 ± 0.0072 | 0.7860 ± 0.0046 | −0.0403 | [−0.0582, −0.0232] |
| Phi-4 | zero-shot vs zero-shot-CoT | 0.7845 ± 0.0076 | 0.8094 ± 0.0035 | −0.0249 | [−0.0350, −0.0149] |
| Phi-4 | zero-shot vs one-shot-CoT | 0.7845 ± 0.0076 | 0.8011 ± 0.0044 | −0.0166 | [−0.0305, −0.0023] |
| Phi-4 | zero-shot-CoT vs one-shot-CoT | 0.8094 ± 0.0035 | 0.8011 ± 0.0044 | +0.0083 | [−0.0043, +0.0208] |
| Qwen3.5 27B | zero-shot vs zero-shot-CoT | 0.7862 ± 0.0011 | 0.7897 ± 0.0021 | −0.0035 | [−0.0119, +0.0048] |
| Qwen3.5 27B | zero-shot vs one-shot-CoT | 0.7862 ± 0.0011 | 0.7726 ± 0.0000 | +0.0136 | [−0.0035, +0.0310] |
| Qwen3.5 27B | zero-shot-CoT vs one-shot-CoT | 0.7897 ± 0.0021 | 0.7726 ± 0.0000 | +0.0171 | [+0.0010, +0.0339] |

---

## 5. Where the two metrics disagree

6 contrasts are significant on **both** effective accuracy and Macro-F1; 7 on effective
accuracy only; 1 on Macro-F1 only. A strategy difference is therefore not one phenomenon — which
metric is used changes the answer, which is why both were declared co-primary rather than one being chosen
after the fact.

| Significant on | Contrast |
|---|---|
| both metrics | Dreaddit · Gemma 4 31B · zero-shot vs zero-shot-CoT |
| both metrics | Dreaddit · Gemma 4 31B · zero-shot vs one-shot-CoT |
| both metrics | Dreaddit · Mistral Small 4 · zero-shot vs zero-shot-CoT |
| both metrics | Dreaddit · Phi-4 · zero-shot-CoT vs one-shot-CoT |
| both metrics | Dreaddit · Qwen3.5 27B · zero-shot vs zero-shot-CoT |
| both metrics | Dreaddit · Qwen3.5 27B · zero-shot vs one-shot-CoT |
| effective accuracy only | Dreaddit · Qwen3.5 27B · zero-shot-CoT vs one-shot-CoT |
| effective accuracy only | GoEmotions · Llama 4 Scout · zero-shot-CoT vs one-shot-CoT |
| effective accuracy only | GoEmotions · Mistral Small 4 · zero-shot vs zero-shot-CoT |
| effective accuracy only | GoEmotions · Mistral Small 4 · zero-shot-CoT vs one-shot-CoT |
| effective accuracy only | GoEmotions · Phi-4 · zero-shot vs zero-shot-CoT |
| effective accuracy only | GoEmotions · Phi-4 · zero-shot vs one-shot-CoT |
| effective accuracy only | GoEmotions · Phi-4 · zero-shot-CoT vs one-shot-CoT |
| Macro-F1 only | Dreaddit · Phi-4 · zero-shot vs zero-shot-CoT |

---

## 6. Where the primary and secondary tests disagree — and why it matters

The permutation test and the McNemar check disagree on **5 of 30** effective-accuracy contrasts.
**Every one of them is Phi-4.**

| Contrast | Permutation (primary) | McNemar (secondary) |
|---|---|---|
| Dreaddit · Phi-4 · zero-shot vs zero-shot-CoT | p Holm = 0.3144 — not significant | p Holm = 0.0029 — significant |
| Dreaddit · Phi-4 · zero-shot-CoT vs one-shot-CoT | p Holm = 0.0072 — significant | p Holm = 0.2639 — not significant |
| GoEmotions · Phi-4 · zero-shot vs zero-shot-CoT | p Holm = 0.0054 — significant | p Holm = 1.0000 — not significant |
| GoEmotions · Phi-4 · zero-shot vs one-shot-CoT | p Holm = 0.0030 — significant | p Holm = 1.0000 — not significant |
| GoEmotions · Phi-4 · zero-shot-CoT vs one-shot-CoT | p Holm = 0.0030 — significant | p Holm = 1.0000 — not significant |

**The three GoEmotions Phi-4 contrasts are not robust, and the report says so.** The primary test's estimand
is the five-run mean, so a single catastrophic run moves it; the McNemar check collapses each item to a
majority vote over five runs and is almost unaffected by one bad run. The frozen per-run values show exactly
that pattern for Phi-4 / GoEmotions / one-shot-CoT:

| Run | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Invalid outputs | 51 | 62 | 49 | 66 | 271 |
| Effective accuracy | 0.7331 | 0.7219 | 0.7412 | 0.7203 | 0.4486 |

Run 5 alone contributes 271 of that
configuration's 499
invalid outputs. **Any Phi-4 GoEmotions strategy claim should be reported as driven by run-to-run
instability, not as a stable property of one-shot-CoT**, and the five-run effective-accuracy SD of
0.1258 should be quoted beside it.

**The contrasting case is Qwen3.5 27B / Dreaddit / zero-shot-CoT**, where the two tests agree and the effect
is stable. Its invalid outputs are spread evenly over the five runs
(54, 55, 50, 53, 57), evaluability is
0.9230,
and the zero-shot vs zero-shot-CoT difference is +0.0887
in effective accuracy with 95% CI [+0.0655,
+0.1122] — the largest strategy
effect anywhere in this analysis, and a **serialisation** effect: the paired evaluability change is
+0.0750.

---

## 7. Answer to RQ3

### Dreaddit

**Prompting strategy does change classification performance on Dreaddit, but the direction depends on the
model, and chain-of-thought does not help.** 7 of 15 effective-accuracy and
7 of 15 Macro-F1 contrasts survive Holm correction.

- On **Macro-F1 the direction is unanimous**: plain zero-shot is higher than zero-shot-CoT in
  5 of 5 models and higher than
  one-shot-CoT in 5 of 5; one-shot-CoT
  is higher than zero-shot-CoT in 5
  of 5. Not all of these reach significance, but no model shows the opposite ordering.
- **Adding an exemplar recovers some of what chain-of-thought costs.** Where the zero-shot-CoT vs one-shot-CoT
  contrast is significant it always favours one-shot-CoT.
- **Two different mechanisms are visible, and they should not be conflated.** The largest effects belong to
  the two models with fragile output formatting (Qwen3.5 27B, Phi-4), and for those the effective-accuracy
  differences move with evaluability (§ 3.3). But **Gemma 4 31B produced 0 invalid outputs in all three
  Dreaddit arms** and Mistral Small 4 produced 1, 1 and 0 — evaluability is 1.0000 / 1.0000 / 1.0000 and
  0.9997 / 0.9997 / 1.0000 — and both models still show significant zero-shot advantages on both metrics.
  For those two models the CoT penalty **cannot** be a parsing artefact; it is a change in the decisions the
  system makes.
- **What must not be said:** that chain-of-thought "harms reasoning". These contrasts measure end-to-end
  deployed behaviour, in which unparseable output is a real cost; the analysis does not separate a reasoning
  change from a formatting change, and the descriptive conditional-accuracy table (§ 3.5) exists precisely so
  the reader can see that the two move differently.

### GoEmotions

**On GoEmotions, prompting strategy has no demonstrated effect on class-balanced performance, and its
effect on effective accuracy is model-specific and partly an artefact of run instability.**
6 of 15 effective-accuracy contrasts are significant and
**0 of 15 Macro-F1 contrasts**.

- The Macro-F1 null is **inconclusive, not negative** — with 6 `anxiety` items the design has little power
  for this metric, as § 4.2 sets out.
- Of the 6 significant effective-accuracy contrasts, **3 are Phi-4 and are
  driven by a single anomalous run** (§ 6); they should be reported with that caveat or not relied on. The
  remaining ones are Llama 4 Scout and Mistral Small 4, where one-shot-CoT beats zero-shot-CoT, and Mistral
  where zero-shot beats zero-shot-CoT.
- The descriptive best strategy differs by model and by metric — on effective accuracy:
  Gemma 4 31B → zero-shot, Llama 4 Scout → one-shot-cot, Mistral Small 4 → one-shot-cot, Phi-4 → zero-shot-cot, Qwen3.5 27B → zero-shot-cot.
- **Accuracy near 0.78 on this dataset is the constant-predictor level** (majority baseline 0.782958 on the
  attributable pool), so an effective-accuracy difference here should never be read on its own.

### Across both datasets

**No prompting strategy is best.** The descriptive best strategy by effective accuracy is
zero-shot for 3 of 5 models on
Dreaddit but for 1 of 5 on
GoEmotions, and the significant contrasts point in opposite directions across models. A pooled "strategy main
effect" would average over these interactions and was not computed, by design.

---

## 8. What this analysis does not support

- **No causal claim.** Strategy, prompt length and exemplar presence change together across the three
  conditions; nothing here separates them. No statement about *why* a strategy changes behaviour.
- **No global "best strategy" claim**, and no pooled main effect across models.
- **No confirmatory language.** The label is post-hoc / exploratory regardless of how small a p-value is.
- **Nothing about latency or efficiency.** The frozen plan's refusal of inferential latency analysis
  (3-second poll quantisation, fixed strategy order, machine, provider, time of day, concurrent load, no
  per-agent timing) stands unchanged. If the paper's RQ3 is read as *efficiency*, the response-time column in
  `unified_results_tables_2026-09-25/` remains **descriptive only**.
- **No conclusion of "no difference"** from a non-significant contrast — in particular not from the
  GoEmotions Macro-F1 family.
- **No conditional-accuracy ranking.** Denominators differ by arm; a complete-case strategy comparison would
  in the worst case retain 195 of 622 items (Phi-4 / GoEmotions), and precisely the items that model could
  parse.

## 9. Limitations, as declared before the results were seen

- **Post-hoc.** Contrasts chosen after the descriptive results were known.
- **Study-wide multiplicity is not controlled.** RQ1, RQ2 and RQ3 reuse the same items and configurations;
  Holm controls the family-wise error rate only within each declared family.
- **Intervals are conditional on the five observed runs** — item-sampling uncertainty, not run-sampling.
  Run-to-run SD is reported in every table for this reason.
- **Monte-Carlo noise is shared with RQ1**, because the same frozen seed strings and therefore the same draws
  were reused (deliberately, so that the configuration-level CIs reproduce the frozen ones bit-for-bit).
- **Strategy arms ran in sequential blocks**, so strategy is confounded with time of day and provider load.
  Stated, not corrected.
- **`prompt_set_sha256` differs for one Gemma Dreaddit cell** (one-shot-CoT, run 5, the `pub_013`
  replacement). All five per-agent prompt hashes are byte-identical to `pub_011`; the enclosing directory
  hash changed for unrelated reasons. Disclosed, not corrected.

## 10. Reproduction

```
python3 code/00_precheck.py                      # 38 pre-condition checks; no test, no p-value
python3 code/01_run_rq3_strategy_inference.py    # the frozen analysis
python3 code/02_validate.py                      # 32 independent validation checks
python3 code/03_build_report.py                  # this file
```

Inputs are hash-pinned; the run fails closed on any mismatch. The saved replicate files
(`replicates/permutation_*.csv.gz`, `replicates/bootstrap_*.csv.gz`) allow every p-value and every interval
to be re-derived without re-running the analysis — `02_validate.py` does exactly that for all 60 of each.

