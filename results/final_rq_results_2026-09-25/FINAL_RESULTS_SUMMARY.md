# AnxioSense — Results Summary

This document summarises the verified results contained in this replication package. All values are
read from frozen artifacts in `results/`; no figure reported here was recomputed for the purpose of
this summary. Where a claim rests on an exploratory rather than a preregistered analysis, this is
stated explicitly.

## 1. Evaluation Overview

The evaluation covers two benchmark datasets, five language models and three prompting strategies,
each executed in five independent runs, giving **30 configurations** and **150 experimental cells**
comprising **100,350 scored records**.

| Property | Value |
|---|---|
| Datasets | Dreaddit (binary stress detection); GoEmotions 715-item subset (5-class distress classification) |
| Models | Llama 4 Scout, Phi-4, Gemma 4 31B, Mistral Small 4, Qwen3.5 27B |
| Prompting strategies | zero-shot, zero-shot chain-of-thought, one-shot chain-of-thought |
| Runs per configuration | 5 |
| Configurations / cells | 30 / 150 |
| Total records | 100,350 |
| Attributable records | 99,075 |
| Safety intercepts | 1,275 |
| Model-invalid records | 1,986 (2.005% of attributable) |
| Infrastructure failures in the scored grid | 0 |
| Attributable items per run | 699 (Dreaddit); 622 (GoEmotions) |
| Majority baselines | 0.5079 (Dreaddit); 0.7830 (GoEmotions) |

**Safety intercepts.** 1,275 records were intercepted by the safety layer before any model call was
issued. These are excluded from model attribution, yielding attributable pools of 699 Dreaddit items
and 622 GoEmotions items per run. The excluded counts are constant across strategies within a
dataset, so all strategy arms are compared on identical item sets.

**Invalid-output treatment.** An output that cannot be parsed into the required label vocabulary is
recorded as model-invalid and counted as incorrect on the attributable denominator. Invalid outputs
are not dropped from the analysis.

**Metrics.** The primary accuracy metric is **effective accuracy**, defined as correct predictions
divided by the attributable pool. **Macro-F1**, the unweighted mean of per-class F1 over the fixed
label list, is co-reported; per-class precision, recall and F1 are computed on valid predictions
only, so an invalid output contributes to neither the numerator nor the denominator of any class.
**Conditional accuracy** (correct divided by valid) is reported for transparency but is not used for
ranking, because its denominator varies with each configuration's invalid-output rate.

**Inferential framework.** Comparisons use paired item-level permutation tests with P = 10,000, and
item-cluster bootstrap with B = 4,000 draws and 95% percentile confidence intervals. The unit of
analysis is the benchmark item carrying its five runs; the run axis is never folded into the item
axis. Holm correction is applied within declared families. Exact McNemar on majority-vote (≥3/5)
effective correctness serves as a secondary test in its own family. Independent revalidation
reproduces all 150 per-run and 30 five-run frozen metric values to a maximum absolute difference of
2.220 × 10⁻¹⁶.

## 2. RQ1 — Model Performance

| | Dreaddit | GoEmotions |
|---|---|---|
| Highest effective accuracy (model) | Llama 4 Scout | Gemma 4 31B |
| Effective accuracy by strategy (ZS / ZS-CoT / 1S-CoT) | 0.7296 / 0.7330 / 0.7502 | 0.8196 / 0.8174 / 0.8132 |
| Strongest point estimate, 95% CI | 0.7502 [0.7202, 0.7803] (1S-CoT) | 0.8196 [0.7907, 0.8489] (ZS) |
| Highest macro-F1, 95% CI | 0.7519 [0.7214, 0.7818] (Llama, ZS) | 0.5940 [0.4865, 0.6681] (Mistral, 1S-CoT) |
| Next-highest macro-F1 | 0.7510 (Llama, 1S-CoT) | 0.5932 [0.4818, 0.6712] (Gemma, ZS) |
| Holm-significant model pairs, effective accuracy | 13 / 30 | 21 / 30 |
| Holm-significant model pairs, macro-F1 | 20 / 30 | 0 / 30 |

Model performance is dataset-dependent, and no model leads on both benchmarks. Llama 4 Scout attains
the highest effective accuracy in all three Dreaddit strategies, reaching 0.7502 under one-shot
chain-of-thought, and also records the highest macro-F1 observed anywhere in the study, 0.7519 under
zero-shot. Gemma 4 31B attains the highest effective accuracy in all three GoEmotions strategies,
reaching 0.8196 under zero-shot. These are descriptive point estimates; the accompanying significance
counts, not the ordering of means, establish which differences are supported inferentially.

On Dreaddit, 13 of 30 model-pair comparisons are Holm-significant on effective accuracy and 20 of 30
on macro-F1. The two leading models are not cleanly separable from one another: Llama 4 Scout and
Phi-4 separate in only one of six Dreaddit comparisons, and the secondary exact-McNemar test finds no
significant difference between them in any strategy. On GoEmotions, 21 of 30 comparisons are
Holm-significant on effective accuracy, and Gemma 4 31B is significantly superior to all four other
models under zero-shot on the secondary test, the clearest model-level separation obtained in the
study. Two Holm-significant GoEmotions accuracy comparisons between Llama 4 Scout and Phi-4 point in
opposite directions depending on strategy, so no consistent ordering between those two models can be
asserted for that dataset.

The GoEmotions macro-F1 result requires explicit treatment: **no model pair separates**, 0 of 30. This
is a limitation of resolution rather than evidence of equivalence. The attributable class supports for
GoEmotions are 487, 81, 33, 15 and 6 items, so the smallest class contributes approximately one fifth
of the macro-F1 statistic from six observations. The resulting bootstrap intervals span roughly
0.45–0.67 for every model and overlap completely. Consequently, GoEmotions macro-F1 values may be
reported descriptively but must not be used to rank models. Dreaddit macro-F1, by contrast, separates
20 of 30 pairs and supports inferential comparison.

## 3. RQ2 — Comparison With Majority Baseline

| Dataset | Majority Baseline | Significantly Above | Significantly Below | Not Distinguishable |
|---|---|---|---|---|
| Dreaddit | 0.5079 | 15 / 15 | 0 | 0 |
| GoEmotions | 0.7830 | 2 / 15 | 5 / 15 | 8 / 15 |

On Dreaddit the result is unambiguous. All fifteen configurations exceed a majority-class predictor,
every comparison Holm-significant under the primary permutation test, and the conclusion is
unchanged under the secondary exact-McNemar test and under both baseline definitions. The largest
margin is +0.2423 [0.1888, 0.2947] for Llama 4 Scout under one-shot chain-of-thought (permutation
p = 1.0 × 10⁻⁴; Holm-adjusted p = 0.0015).

On GoEmotions the evidence is substantially weaker, and its interpretation is governed by the class
distribution: 487 of 622 attributable items belong to `non_distress`, so a constant predictor attains
0.7830 effective accuracy. Only two configurations significantly exceed this level — Gemma 4 31B
under zero-shot (+0.0367 [0.0119, 0.0621]) and under zero-shot chain-of-thought (+0.0344
[0.0103, 0.0592]), both at Holm-adjusted p = 0.0440. Five configurations are significantly **below**
the baseline: Llama 4 Scout in all three strategies (largest deficit −0.1003 [−0.1392, −0.0617],
Holm-adjusted p = 0.0015) and Phi-4 under zero-shot (−0.0466 [−0.0704, −0.0225], p = 0.0048) and
one-shot chain-of-thought (−0.1100 [−0.1325, −0.0865], p = 0.0015). The remaining eight are not
distinguishable from the baseline.

The two tests disagree for Gemma 4 31B, and the disagreement is reported rather than resolved. The
primary permutation test finds both Gemma configurations significantly above baseline
(Holm-adjusted p = 0.0440 in each case), whereas the secondary exact-McNemar test on majority-vote
effective correctness does not (Holm-adjusted p = 0.0876 for zero-shot and p = 0.1037 for zero-shot
chain-of-thought). The permutation test is the preregistered primary analysis; the McNemar result is
a secondary check conducted in its own family. Both should be cited together, and the above-baseline
claim for GoEmotions should be qualified accordingly.

Because accuracy near 0.78 on GoEmotions coincides with the constant-predictor level, accuracy is
close to uninformative on that benchmark. Macro-F1 values of 0.52–0.59, against 0.176 for a constant
predictor, indicate that the system does discriminate between classes; however, as established in
Section 2, those macro-F1 values cannot be used to order models.

## 4. RQ3 — Prompting Strategy

The frozen 2026-09-21 package contains no strategy-versus-strategy inferential test. A separate
analysis in `results/rq3_strategy_inference_2026-09-25/` supplies one. That analysis is labelled
**post-hoc and exploratory** in its own preregistration freeze: the estimation procedure was frozen
on 2026-09-21 for RQ1 and RQ2 and applied unchanged, but the strategy contrasts were declared after
the descriptive results were known. It is not a confirmatory analysis and must not be described as
preregistered.

| Quantity | Value |
|---|---|
| Metric-specific strategy comparisons | 60 |
| Holm-significant comparisons | 20 |
| Distinct significant strategy contrasts | 14 |
| Significant on both co-primary metrics | 6 |
| Significant on effective accuracy only | 7 |
| Significant on macro-F1 only | 1 |

The distinction between 20 significant rows and 14 distinct contrasts is material: a single contrast
may appear twice, once per co-primary metric, so the number of independent findings is 14. Declared
scope is within model and within dataset, with no pooling across models or datasets, and Holm
correction is applied within 30 primary comparisons per dataset.

No prompting strategy dominates consistently. Significant effects occur in both directions across
models and datasets, and the sign of a strategy contrast for one model does not predict its sign for
another. On this evidence no general recommendation in favour of chain-of-thought prompting, or
against it, is supportable.

Several of the largest effective-accuracy differences are associated with changes in output
evaluability rather than with classification performance alone. The clearest verified instance is
Qwen3.5 27B on Dreaddit: zero-shot chain-of-thought is 0.0887 [0.0655, 0.1122] below zero-shot on
effective accuracy (Holm-adjusted p = 0.0030), while evaluability falls from 0.9980 to 0.9230 across
the same contrast and conditional accuracy falls by only 0.0399. The majority of the effective-accuracy
difference therefore reflects a failure to emit parseable structured output rather than a decline in
classification quality on the answers that were produced. Strategy effects of this kind should be
reported with the corresponding evaluability change so that the two mechanisms remain distinguishable.

## 5. Invalid Outputs and Evaluability

| Quantity | Value |
|---|---|
| Attributable records | 99,075 |
| Model-invalid records | 1,986 |
| Invalid-output rate | 2.005% |
| Safety intercepts | 1,275 |
| Infrastructure failures in the scored grid | 0 |
| Configurations with Holm-significant class-selective invalidity | 4 / 30 |
| Strongest class-selective result | Qwen3.5 27B / Dreaddit / zero-shot-CoT: 94.1% of invalid items stress-positive against 50.8% expected |
| Largest conditional-minus-effective gap | 0.1281 (Phi-4 / GoEmotions / one-shot-CoT) |

Effective accuracy retains invalid outputs in its denominator because doing so makes the metric
invariant to selection. Conditional accuracy removes exactly those items on which a model failed to
produce usable output, so its value rises as the invalid-output rate rises and it is not comparable
across configurations with differing rates.

Phi-4 on GoEmotions under one-shot chain-of-thought illustrates the divergence. Its conditional
accuracy is 0.8011 [0.7706, 0.8304], the second highest on that dataset, while its effective accuracy
is 0.6730 [0.6463, 0.7000], the lowest. The 0.1281 gap arises from 499 invalid outputs, 16.05% of the
cell's attributable pool, with mean evaluability 0.8395. The across-run standard deviations for this
cell are 0.1258 on effective accuracy and 0.1543 on evaluability, indicating run-level instability
rather than a stable configuration property.

Two distinct phenomena must be separated. **Invalid-output volume** concerns how many items were lost;
**class-selective invalidity** concerns whether the lost items are non-randomly distributed across
classes. An exploratory, clearly separated analysis identified Holm-significant class-selective
invalidity in 4 of 30 configurations, the strongest being Qwen3.5 27B on Dreaddit under zero-shot
chain-of-thought. The Phi-4 GoEmotions one-shot-CoT cell is a volume case only: it exhibits the
largest conditional-minus-effective gap in the study but **no detectable class enrichment**, and it
must not be characterised as class-selective invalidity.

## 6. Latency

Configuration-level mean end-to-end client latency for one complete assessment ranges from
**3.32 ± 0.16 s** (Mistral Small 4, GoEmotions, one-shot chain-of-thought) to **15.14 ± 3.77 s**
(Gemma 4 31B, Dreaddit, one-shot chain-of-thought). Values are available for all 30 configurations.

Latency results are **descriptive only**. No statistical comparison of latency was performed, and no
model is identified as fastest. Four limitations constrain interpretation. First, measurement
resolution is 3 s, set by the polling cadence; medians consequently fall on that lattice, so means
rather than medians should be cited. Second, model is confounded with serving provider and
quantization: Mistral Small 4 was served by Mistral, Gemma 4 31B by CoreWeave under an fp4 request
directive, Llama 4 Scout and Phi-4 by DeepInfra, and Qwen3.5 27B by Alibaba. Third, all three Llama
4 Scout Dreaddit configurations (15 of 15 cells) executed under concurrent load on the same machine.
Fourth, strategies executed in sequential blocks, so block order is not separable from strategy.
These figures therefore characterise deployments as observed, not model efficiency.

## 7. Limitations

1. **GoEmotions class imbalance.** Attributable class supports are 487, 81, 33, 15 and 6 items. The
   `non_distress` majority proportion of 0.7830 places the constant-predictor accuracy near the
   observed accuracy range, limiting the informativeness of accuracy on that benchmark.
2. **Limited power for GoEmotions macro-F1.** No model pair separates (0 of 30) and bootstrap
   intervals span approximately 0.45–0.67. The study is not powered to rank models on macro-F1 for
   this dataset. Additionally, 14 of 4,000 bootstrap replicates contain no `anxiety` item at all.
3. **Exploratory status of the RQ3 strategy analysis.** The contrasts were declared after the
   descriptive results were known. Confirmatory strategy claims would require a new preregistered
   analysis, not a reanalysis of these artifacts.
4. **Latency confounding.** Provider, quantization, concurrency and sequential block order are not
   separable from model and strategy, and measurement resolution is 3 s.
5. **Provider-default decoding parameters.** Temperature, maximum tokens, seed and top-p/top-k were
   not explicitly set; provider defaults applied throughout. Run-to-run variance therefore includes
   uncontrolled provider-side sampling. The sole recorded per-model deviation is a disabled reasoning
   mode for Qwen3.5 27B, which is not a sampling parameter.
6. **Scope of evaluation.** The evaluation graded the social-media assessment path, scored from the
   referral agent (Dreaddit) and the emotion agent (GoEmotions). GAD-7 administration, the final
   report agent and recommendation personalisation were not evaluated.
7. **Dataset framing.** Dreaddit is a binary stress-versus-non-stress benchmark and does not validate
   the GoEmotions `anxiety` class.

## 8. Summary of Findings

On Dreaddit, the evidence for above-baseline performance is strong and internally consistent. All
fifteen configurations exceed the majority-class baseline, every comparison survives Holm correction
under the primary permutation test, the conclusion is unchanged under the secondary exact-McNemar
test and under both baseline definitions, and the largest margin is +0.2423 [0.1888, 0.2947]. This is
the most robust result in the study.

On GoEmotions the accuracy evidence is considerably less conclusive. Only two of fifteen
configurations significantly exceed a baseline of 0.7830, five are significantly below it, and eight
are indistinguishable from it. The two above-baseline results are not confirmed by the secondary test.
The principal determinant is the class distribution rather than model capability: with 78.3% of items
in a single class, accuracy on this benchmark carries little discriminative information, and macro-F1,
which does show the system distinguishing classes, cannot be used to order models at the available
class supports.

Model performance is dataset-dependent. Llama 4 Scout attains the highest effective accuracy across
all Dreaddit strategies and the highest macro-F1 in the study; Gemma 4 31B attains the highest
effective accuracy across all GoEmotions strategies and is the only model significantly superior to
every other on the secondary test for that dataset. No model leads on both benchmarks, and the two
strongest models on Dreaddit are not reliably separable from one another.

No prompting strategy is universally superior. Exploratory post-hoc testing identifies 14 distinct
Holm-significant strategy contrasts from 60 metric-specific comparisons, with effects in both
directions across models and datasets. Several of the largest effective-accuracy differences coincide
with substantial changes in output evaluability, indicating that structured-output compliance, not
classification quality alone, contributes materially to the observed differences.

Accounting for invalid outputs is essential to evaluating pipelines of this kind. Although the overall
invalid-output rate is low at 2.005%, it is highly uneven, and the choice of denominator can reverse a
configuration's standing: Phi-4 on GoEmotions under one-shot chain-of-thought ranks second on
conditional accuracy and last on effective accuracy on the same items. Reporting effective accuracy
alongside evaluability, and separating invalid-output volume from class-selective invalidity, is
therefore treated here as a requirement of the metric policy rather than a supplementary diagnostic.
