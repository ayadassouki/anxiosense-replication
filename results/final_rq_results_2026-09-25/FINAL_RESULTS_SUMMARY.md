# Final results summary — AnxioSense

## AI-Assistance Disclosure

Generative AI tools were used to assist with analysis scripting, organization, verification, and drafting of this reporting package. Quantitative findings were derived from the frozen AnxioSense experimental artifacts and verified against their source files. AI-generated suggestions were not treated as experimental evidence, and the original frozen experimental results were not modified.

---

## The experiment in one paragraph

Two datasets × five models × three prompting strategies × five runs = 150 cells, 100,350 records. Dreaddit is
binary stress detection (699 attributable items per run, majority baseline 0.5079); GoEmotions is 5-class
distress classification (622 attributable items per run, majority baseline 0.7830). 1,275 safety intercepts
fire before any model call and are excluded from model attribution. 1,986 records (2.005%) are model-invalid.
**Zero infrastructure failures survive into the scored grid.**

## Headline metric

**Effective accuracy** (correct ÷ attributable) is the publication metric, reported with **macro-F1**.
Conditional accuracy (correct ÷ valid) is reported beside it for transparency but is not used for ranking —
see `INVALID_OUTPUT_SELECTION_EFFECT.md`.

## RQ1 — which model

| | Dreaddit | GoEmotions |
|---|---|---|
| Leader on effective accuracy | **Llama 4 Scout** (0.7296 / 0.7330 / 0.7502 across ZS / ZS-CoT / 1S-CoT) | **Gemma 4 31B** (0.8196 / 0.8174 / 0.8132) |
| Best single macro-F1 | Llama 4 Scout ZS, 0.7519 | Mistral 1S-CoT, 0.5940 (Gemma ZS 0.5932) |
| Model pairs Holm-significant, effective accuracy | 13 / 30 | 21 / 30 |
| Model pairs Holm-significant, macro-F1 | 20 / 30 | **0 / 30** |

**No model leads both datasets.** On GoEmotions macro-F1 no model pair separates at all — the class supports
on the attributable pool are 487 / 81 / 33 / 15 / 6, so six `anxiety` items carry a fifth of the metric and every CI spans
roughly 0.45–0.67. Llama versus Phi-4 separates in only 1 of 6 Dreaddit comparisons, and on GoEmotions the two
Holm-significant accuracy comparisons between them point in **opposite directions** depending on strategy.

## RQ2 — versus the majority baseline

| | Above baseline (Holm-sig) | Below (Holm-sig) | Not distinguishable |
|---|---|---|---|
| Dreaddit (baseline 0.5079) | **15 / 15** | 0 | 0 |
| GoEmotions (baseline 0.7830) | **2 / 15** (Gemma ZS, ZS-CoT) | 5 / 15 | 8 / 15 |

Dreaddit is unambiguous: every configuration beats a majority-class predictor under both the primary
permutation test and exact McNemar, under both baseline definitions. GoEmotions is not: only Gemma exceeds the
baseline, by ~3.5 accuracy points at Holm p = 0.044, and **McNemar does not confirm either result**
(p = 0.088, 0.104). Five configurations are significantly *worse* than answering `non_distress` to everything.
Because 78.3% of GoEmotions items are `non_distress`, accuracy near 0.78 is the constant-predictor level, and
macro-F1 (0.52–0.59 against a constant predictor's 0.176) is the metric that shows the system doing anything.

## RQ3 — prompting strategy

> **SUPERSEDED IN PART — see `SUPERSEDED.md`.** This section was written 2026-09-25 20:44:46Z.
> A separate **post-hoc / exploratory** analysis was frozen at 22:04:33Z and executed at 22:04:45Z
> the same day, and it *does* test strategy contrasts: 20 of 60 metric-specific rows are
> Holm-significant, corresponding to **14 distinct strategy contrasts** (6 significant on both
> co-primary metrics, 7 on effective accuracy only, 1 on macro-F1 only). The statement below
> remains true of the **frozen 2026-09-21** package. See `results/rq3_strategy_inference_2026-09-25/` for the tested result.

**No strategy-vs-strategy test exists in the frozen package** (the plan states "RQ3. No inference."), so every
strategy statement is descriptive. Descriptively, no strategy wins everywhere: one-shot-CoT is best for 2 of 5
models on Dreaddit and 2 of 5 on GoEmotions; zero-shot is best for 3 of 5 on Dreaddit.

The metrics disagree about the ordering. On Dreaddit **zero-shot separates 0 of 10 model pairs on effective
accuracy but 6 of 10 on macro-F1**; on GoEmotions accuracy separates 21 of 30 pairs and macro-F1 separates
none. Within-model, the accuracy-optimal and macro-F1-optimal strategies disagree for Llama and Phi-4 on
Dreaddit (one-shot-CoT on accuracy, zero-shot on macro-F1).

The largest single within-model effect is Qwen on Dreaddit, where zero-shot-CoT is 0.0887 below zero-shot on
effective accuracy — but its evaluability falls from 0.9980 to 0.9230 at the same time and its conditional
accuracy falls by only 0.0399, so that effect is substantially a serialisation failure, not a reasoning
failure.

## Latency

End-to-end **client** wall clock for one complete assessment (`latency_ms`), per-run mean, then mean ± SD over
five runs, in seconds. Available for all 30 configurations. Measurement resolution is **3 s** (poll cadence),
strategies ran in sequential blocks, model is confounded with serving provider, and **all three** Llama Dreaddit configurations (15 of 15 cells)
ran under concurrent load. **Nothing about latency was tested.** Display the client mean, not the median — the
medians sit on the 3 s lattice (Qwen's Dreaddit medians are 9.08 / 9.08 / 9.07 s).

Range: 3.32 s (Mistral GoEmotions 1S-CoT) to 15.14 s (Gemma Dreaddit 1S-CoT).

## Invalid outputs and selection

Effective accuracy is immune to selection by construction. Conditional accuracy is not comparable across
configurations. An exploratory, clearly separated analysis found class-selective invalidity surviving Holm
correction in **4 of 30 configurations**, the strongest being Qwen / Dreaddit / zero-shot-CoT (94.1% of invalid
items are stress-positive against 50.8% expected). **The pattern previously suspected for Phi-4 / GoEmotions /
one-shot-CoT is not supported** — that cell has the largest conditional-minus-effective gap (0.1281) but no
detectable class enrichment; its gap reflects invalid-output *volume*, not *which* items were lost.

## Unresolved before paper writing

1. **Decide the framing of "AnxioSense accuracy."** There are 30 configuration accuracies and no configuration
   was pre-designated as the system. Whatever goes in the abstract is a post-hoc choice and must be stated as
   one.
2. **Decide how RQ3 is defined in the paper.** The frozen plan's RQ3 is *efficiency/latency*; the results
   question asked here is *prompting strategy*. Neither had an inferential test when this was written. A post-hoc analysis has since tested the prompting-strategy reading — see `SUPERSEDED.md` — but it is labelled exploratory, so if the paper needs *confirmatory* tested
   strategy claims, that is a new pre-registered analysis, not a reanalysis.
3. **The GoEmotions macro-F1 result (0/30 pairs separated)** needs an explicit sentence in the limitations: at
   these class supports the study is not powered to rank models on macro-F1.
4. **The run-level Phi-4 GoEmotions one-shot-CoT question** (`ISSUES_FOR_AUDIT.md` item 1: 197 samples moved
   from `ok_empty_list` in run 4 to `fail_unparseable` in run 5; conditional macro-F1 *rises* while effective
   accuracy falls) is still open. The pooled analysis here does not settle it.
5. **Gemma's two "above baseline" GoEmotions results are not confirmed by McNemar.** Decide whether to report
   them as significant, and say which test is primary.
6. **Scope statement needed:** the evaluation graded the `/api/workflow/evaluate` social-media path, scored
   from the referral agent (Dreaddit) and the emotion agent (GoEmotions). GAD-7, the final report agent and the
   recommendation personalisation were not evaluated.
7. **Housekeeping (not a results issue):** two files in `invalid_output_audit_2026-09-25/` no longer match that
   package's own `CHECKSUMS.sha256` (`cell_level_invalid_vs_quality.csv`, `invalid_output_audit_report.md`).
   They were changed outside this package's build and are **not** inputs to it. Re-run that package's
   `code/05_validate.py` to refresh its manifest before archiving.

## Where each number comes from

`result_provenance.csv` — 396 rows mapping every headline number to a source file and field.
`VALIDATION.md` — 12 checks, all passing for this package, including a three-way cross-source agreement test
on all 90 five-run point estimates and a re-run test proving the generators write nothing outside this
directory.
