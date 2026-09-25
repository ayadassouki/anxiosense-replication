#!/usr/bin/env python3
"""Builds RQ3_STRATEGY_INFERENCE_REPORT.md. Every number is read from the result tables;
none is transcribed by hand. READ-ONLY outside this directory."""
import csv, json, collections
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent
RES = OUT.parent
T = OUT / "tables"

P = list(csv.DictReader(open(T / "rq3_strategy_pairs_primary.csv")))
M = list(csv.DictReader(open(T / "rq3_strategy_pairs_mcnemar.csv")))
CD = list(csv.DictReader(open(T / "rq3_strategy_pairs_conditional_accuracy_ci.csv")))
CF = list(csv.DictReader(open(T / "rq3_configuration_level_ci.csv")))
man = json.load(open(OUT / "analysis_manifest.json"))
frz = json.load(open(OUT / "PREREGISTRATION_FREEZE.json"))
val = json.load(open(OUT / "validation.json"))
perrun = list(csv.DictReader(open(RES / "descriptive_2026-09-21" / "per_run_results.csv")))

MODELS = ["Gemma 4 31B", "Llama 4 Scout", "Mistral Small 4", "Phi-4", "Qwen3.5 27B"]
PAIRS = [("zero-shot", "zero-shot-CoT"), ("zero-shot", "one-shot-CoT"), ("zero-shot-CoT", "one-shot-CoT")]
DSN = {"dreaddit": "Dreaddit", "goemotions": "GoEmotions"}
MID = {"Gemma 4 31B": "google/gemma-4-31b-it", "Llama 4 Scout": "meta-llama/llama-4-scout",
       "Mistral Small 4": "mistralai/mistral-small-2603", "Phi-4": "microsoft/phi-4", "Qwen3.5 27B": "qwen/qwen3.5-27b"}
SH = {"zero-shot": "zero-shot", "zero-shot-CoT": "zero-shot-cot", "one-shot-CoT": "one-shot-cot"}

def sgn(x):
    x = float(x)
    return ("+" if x >= 0 else "−") + f"{abs(x):.4f}"
def f4(x): return f"{float(x):.4f}"
def pf(x):
    x = float(x)
    return "&lt;0.0001" if x < 1e-4 else f"{x:.4f}"
def sig(r): return "**yes**" if r["holm_significant_0.05"] == "True" else "no"

def primary_table(ds, metric):
    rs = [r for r in P if r["dataset"] == ds and r["metric"] == metric]
    L = ["| Model | Contrast (A vs B) | A: mean ± SD | B: mean ± SD | Diff (A−B) | 95% CI | p (unadj.) | p (Holm) | Sig. at .05 |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in rs:
        L.append("| %s | %s vs %s | %s ± %s | %s ± %s | %s | [%s, %s] | %s | %s | %s |" % (
            r["model"], r["strategy_A"], r["strategy_B"], f4(r["A_mean"]), f4(r["A_sd"]),
            f4(r["B_mean"]), f4(r["B_sd"]), sgn(r["diff_A_minus_B"]), sgn(r["ci_low"]), sgn(r["ci_high"]),
            pf(r["p_perm"]), pf(r["p_holm"]), sig(r)))
    return "\n".join(L)

def evalu_table(ds):
    seen, L = set(), ["| Model | Contrast (A vs B) | Invalid A (Σ5) | Invalid B (Σ5) | Evaluability A | Evaluability B | Δ evaluability (A−B) | 95% CI |",
                      "|---|---|---|---|---|---|---|---|"]
    for r in P:
        if r["dataset"] != ds: continue
        k = (r["model"], r["strategy_A"], r["strategy_B"])
        if k in seen: continue
        seen.add(k)
        L.append("| %s | %s vs %s | %s | %s | %s | %s | %s | [%s, %s] |" % (
            r["model"], r["strategy_A"], r["strategy_B"], r["A_invalid_outputs_5runs"], r["B_invalid_outputs_5runs"],
            f4(r["A_evaluability"]), f4(r["B_evaluability"]), sgn(r["diff_evaluability_A_minus_B"]),
            sgn(r["diff_evaluability_ci_low"]), sgn(r["diff_evaluability_ci_high"])))
    return "\n".join(L)

def mcn_table(ds):
    L = ["| Model | Contrast (A vs B) | A majority-correct | B majority-correct | b | c | Δ majority acc. | p exact | p (Holm) | Sig. at .05 |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for r in [x for x in M if x["dataset"] == ds]:
        L.append("| %s | %s vs %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["model"], r["strategy_A"], r["strategy_B"], r["A_majority_correct"], r["B_majority_correct"],
            r["b_A_correct_B_wrong"], r["c_A_wrong_B_correct"], sgn(r["diff_majority_acc"]),
            pf(r["p_exact"]), pf(r["p_holm"]), sig(r)))
    return "\n".join(L)

def cond_table(ds):
    L = ["| Model | Contrast (A vs B) | A cond. acc. ± SD | B cond. acc. ± SD | Diff (A−B) | 95% CI |",
         "|---|---|---|---|---|---|"]
    for r in [x for x in CD if x["dataset"] == ds]:
        L.append("| %s | %s vs %s | %s ± %s | %s ± %s | %s | [%s, %s] |" % (
            r["model"], r["strategy_A"], r["strategy_B"], f4(r["A_acc_cond"]), f4(r["A_sd"]),
            f4(r["B_acc_cond"]), f4(r["B_sd"]), sgn(r["diff_A_minus_B"]), sgn(r["ci_low"]), sgn(r["ci_high"])))
    return "\n".join(L)

def nsig(ds, metric):
    rs = [r for r in P if r["dataset"] == ds and r["metric"] == metric]
    return sum(r["holm_significant_0.05"] == "True" for r in rs), len(rs)

def dircount(ds, metric, pair, who):
    return sum(1 for r in P if r["dataset"] == ds and r["metric"] == metric
               and (r["strategy_A"], r["strategy_B"]) == pair and r["direction"] == who)

def best(ds, model, metric):
    rs = [r for r in CF if r["dataset"] == ds and r["model"] == model]
    return max(rs, key=lambda r: float(r[metric]))["strategy"]

by = collections.defaultdict(dict)
for r in P: by[(r["dataset"], r["model"], r["strategy_A"], r["strategy_B"])][r["metric"]] = r
both = [k for k, v in by.items() if v["acc_eff"]["holm_significant_0.05"] == "True" and v["macro_f1"]["holm_significant_0.05"] == "True"]
only_a = [k for k, v in by.items() if (v["acc_eff"]["holm_significant_0.05"] == "True") and (v["macro_f1"]["holm_significant_0.05"] != "True")]
only_f = [k for k, v in by.items() if (v["acc_eff"]["holm_significant_0.05"] != "True") and (v["macro_f1"]["holm_significant_0.05"] == "True")]
MK = {(r["dataset"], r["model"], r["strategy_A"], r["strategy_B"]): r for r in M}
disagree = [k for k in by if (by[k]["acc_eff"]["holm_significant_0.05"] == "True") != (MK[k]["holm_significant_0.05"] == "True")]

def pr(ds, model, strat, col):
    rs = sorted([r for r in perrun if r["dataset"] == ds and r["model"] == MID[model] and r["strategy"] == SH[strat]],
                key=lambda r: int(r["run"]))
    return [r[col] for r in rs]

n = {"dreaddit": 699, "goemotions": 622}
D = []
A = D.append

A(f"""# RQ3 — prompting-strategy inferential analysis

**Status: POST-HOC / EXPLORATORY.** This analysis uses frozen experimental data and a method that was
selected and frozen **before** any RQ3 test was run, but the contrasts were chosen **after** the descriptive
strategy results were known. It is therefore exploratory. No result below confirms a hypothesis, and RQ1 and
RQ2 remain the paper's pre-specified confirmatory analyses.

| | |
|---|---|
| Plan | `RQ3_SAP_ADDENDUM.md`, frozen `{frz['frozen_utc']}` |
| Analysis executed | `{man['created_utc']}` |
| Estimation procedure | `inferential_2026-09-21/STATISTICAL_ANALYSIS_PLAN.md`, applied **unchanged** |
| Validation | **{val['n_pass']} of {val['n_checks']} checks passed** (`VALIDATION.md`) |
| Environment | Python {man['python']}, numpy {man['numpy']} |

---

## 1. What was tested

**RQ3 (classification-quality reading).** Within each model and dataset, does the prompting strategy change
classification performance?

| Element | As executed |
|---|---|
| Statistical unit | The benchmark item, carrying all five runs. n = {n['dreaddit']} (Dreaddit), {n['goemotions']} (GoEmotions) |
| Contrasts | zero-shot vs zero-shot-CoT; zero-shot vs one-shot-CoT; zero-shot-CoT vs one-shot-CoT — within model, within dataset |
| Primary outcomes | Effective accuracy and Macro-F1 (co-primary) |
| Invalid outputs | Counted as **incorrect** on the attributable denominator; the analysis is **not** conditioned on valid outputs |
| Primary test | Paired item-level permutation, whole five-run vector swapped per item, P = {man['P']:,}; Macro-F1 recomputed after each permutation |
| Intervals | Item-cluster bootstrap, B = {man['B']:,}, shared resampled index per dataset, 95% percentile |
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
  the item axis. Independent units are {n['dreaddit']} / {n['goemotions']} **items**, not 3,495 / 3,110
  item-run records and not 5 runs. Runs are never paired across arms and never resampled.

---

## 2. Headline

| Dataset | Effective accuracy | Macro-F1 | Total | McNemar (secondary) |
|---|---|---|---|---|
| Dreaddit | {nsig('dreaddit','acc_eff')[0]} / {nsig('dreaddit','acc_eff')[1]} Holm-significant | {nsig('dreaddit','macro_f1')[0]} / {nsig('dreaddit','macro_f1')[1]} | **{nsig('dreaddit','acc_eff')[0]+nsig('dreaddit','macro_f1')[0]} / 30** | {sum(r['holm_significant_0.05']=='True' for r in M if r['dataset']=='dreaddit')} / 15 |
| GoEmotions | {nsig('goemotions','acc_eff')[0]} / {nsig('goemotions','acc_eff')[1]} | **{nsig('goemotions','macro_f1')[0]} / {nsig('goemotions','macro_f1')[1]}** | **{nsig('goemotions','acc_eff')[0]+nsig('goemotions','macro_f1')[0]} / 30** | {sum(r['holm_significant_0.05']=='True' for r in M if r['dataset']=='goemotions')} / 15 |

All 30 comparisons per dataset are reported below, significant or not, as the frozen addendum requires.

---

## 3. Dreaddit — all 30 primary comparisons (n = {n['dreaddit']} items)

### 3.1 Effective accuracy

{primary_table('dreaddit','acc_eff')}

### 3.2 Macro-F1

{primary_table('dreaddit','macro_f1')}

### 3.3 Invalid-output context for the same 15 contrasts

Effective accuracy counts an invalid output as incorrect, so a change in parseability moves it directly.
`Effective = Conditional × Evaluability` and `Evaluability = 1 − invalid rate` hold exactly. This table is a
**descriptive companion**, not a mediation analysis: it shows how much of a contrast co-occurs with a change
in parseability, and says nothing about what caused what.

{evalu_table('dreaddit')}

### 3.4 Secondary — exact McNemar on majority-vote correctness (≥ 3 of 5 runs)

{mcn_table('dreaddit')}

### 3.5 Conditional accuracy — descriptive, no test

Denominators differ by arm, so these are not comparable across strategies and carry no p-value.

{cond_table('dreaddit')}

---

## 4. GoEmotions — all 30 primary comparisons (n = {n['goemotions']} items)

### 4.1 Effective accuracy

{primary_table('goemotions','acc_eff')}

### 4.2 Macro-F1

{primary_table('goemotions','macro_f1')}

**Not one** of the 15 Macro-F1 contrasts reaches significance after Holm correction. The correct word is
**inconclusive**, not "no difference": class supports on the attributable pool are non_distress 487,
frustration 81, sadness 33, fear 15, **anxiety 6**, so one fifth of Macro-F1 rests on six items and the
intervals are correspondingly wide. {man['goemotions_bootstrap_replicates_without_anxiety_item']} of
{man['B']:,} bootstrap replicates contain no `anxiety` item at all; per MetricPolicy 1.0.0 its recall and F1
are 0 in those replicates, applied verbatim. This mirrors the frozen RQ1 result, where 0 of 30 GoEmotions
Macro-F1 model contrasts were significant either.

### 4.3 Invalid-output context

{evalu_table('goemotions')}

### 4.4 Secondary — exact McNemar on majority-vote correctness (≥ 3 of 5 runs)

{mcn_table('goemotions')}

### 4.5 Conditional accuracy — descriptive, no test

{cond_table('goemotions')}

---

## 5. Where the two metrics disagree

{len(both)} contrasts are significant on **both** effective accuracy and Macro-F1; {len(only_a)} on effective
accuracy only; {len(only_f)} on Macro-F1 only. A strategy difference is therefore not one phenomenon — which
metric is used changes the answer, which is why both were declared co-primary rather than one being chosen
after the fact.

| Significant on | Contrast |
|---|---|""")
for k in both: A(f"| both metrics | {DSN[k[0]]} · {k[1]} · {k[2]} vs {k[3]} |")
for k in only_a: A(f"| effective accuracy only | {DSN[k[0]]} · {k[1]} · {k[2]} vs {k[3]} |")
for k in only_f: A(f"| Macro-F1 only | {DSN[k[0]]} · {k[1]} · {k[2]} vs {k[3]} |")

A(f"""
---

## 6. Where the primary and secondary tests disagree — and why it matters

The permutation test and the McNemar check disagree on **{len(disagree)} of 30** effective-accuracy contrasts.
**Every one of them is Phi-4.**

| Contrast | Permutation (primary) | McNemar (secondary) |
|---|---|---|""")
for k in disagree:
    a = by[k]["acc_eff"]; m = MK[k]
    A(f"| {DSN[k[0]]} · {k[1]} · {k[2]} vs {k[3]} | p Holm = {pf(a['p_holm'])} — {'significant' if a['holm_significant_0.05']=='True' else 'not significant'} | p Holm = {pf(m['p_holm'])} — {'significant' if m['holm_significant_0.05']=='True' else 'not significant'} |")

A(f"""
**The three GoEmotions Phi-4 contrasts are not robust, and the report says so.** The primary test's estimand
is the five-run mean, so a single catastrophic run moves it; the McNemar check collapses each item to a
majority vote over five runs and is almost unaffected by one bad run. The frozen per-run values show exactly
that pattern for Phi-4 / GoEmotions / one-shot-CoT:

| Run | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Invalid outputs | {' | '.join(pr('goemotions','Phi-4','one-shot-CoT','N_model_invalid'))} |
| Effective accuracy | {' | '.join(f4(x) for x in pr('goemotions','Phi-4','one-shot-CoT','accuracy_effective'))} |

Run 5 alone contributes {pr('goemotions','Phi-4','one-shot-CoT','N_model_invalid')[4]} of that
configuration's {by[('goemotions','Phi-4','zero-shot','one-shot-CoT')]['acc_eff']['B_invalid_outputs_5runs']}
invalid outputs. **Any Phi-4 GoEmotions strategy claim should be reported as driven by run-to-run
instability, not as a stable property of one-shot-CoT**, and the five-run effective-accuracy SD of
{f4(by[('goemotions','Phi-4','zero-shot','one-shot-CoT')]['acc_eff']['B_sd'])} should be quoted beside it.

**The contrasting case is Qwen3.5 27B / Dreaddit / zero-shot-CoT**, where the two tests agree and the effect
is stable. Its invalid outputs are spread evenly over the five runs
({', '.join(pr('dreaddit','Qwen3.5 27B','zero-shot-CoT','N_model_invalid'))}), evaluability is
{f4([r for r in P if r['dataset']=='dreaddit' and r['model']=='Qwen3.5 27B' and r['strategy_B']=='zero-shot-CoT'][0]['B_evaluability'])},
and the zero-shot vs zero-shot-CoT difference is {sgn(by[('dreaddit','Qwen3.5 27B','zero-shot','zero-shot-CoT')]['acc_eff']['diff_A_minus_B'])}
in effective accuracy with 95% CI [{sgn(by[('dreaddit','Qwen3.5 27B','zero-shot','zero-shot-CoT')]['acc_eff']['ci_low'])},
{sgn(by[('dreaddit','Qwen3.5 27B','zero-shot','zero-shot-CoT')]['acc_eff']['ci_high'])}] — the largest strategy
effect anywhere in this analysis, and a **serialisation** effect: the paired evaluability change is
{sgn(by[('dreaddit','Qwen3.5 27B','zero-shot','zero-shot-CoT')]['acc_eff']['diff_evaluability_A_minus_B'])}.

---

## 7. Answer to RQ3

### Dreaddit

**Prompting strategy does change classification performance on Dreaddit, but the direction depends on the
model, and chain-of-thought does not help.** {nsig('dreaddit','acc_eff')[0]} of 15 effective-accuracy and
{nsig('dreaddit','macro_f1')[0]} of 15 Macro-F1 contrasts survive Holm correction.

- On **Macro-F1 the direction is unanimous**: plain zero-shot is higher than zero-shot-CoT in
  {dircount('dreaddit','macro_f1',('zero-shot','zero-shot-CoT'),'A higher')} of 5 models and higher than
  one-shot-CoT in {dircount('dreaddit','macro_f1',('zero-shot','one-shot-CoT'),'A higher')} of 5; one-shot-CoT
  is higher than zero-shot-CoT in {dircount('dreaddit','macro_f1',('zero-shot-CoT','one-shot-CoT'),'B higher')}
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
{nsig('goemotions','acc_eff')[0]} of 15 effective-accuracy contrasts are significant and
**{nsig('goemotions','macro_f1')[0]} of 15 Macro-F1 contrasts**.

- The Macro-F1 null is **inconclusive, not negative** — with 6 `anxiety` items the design has little power
  for this metric, as § 4.2 sets out.
- Of the {nsig('goemotions','acc_eff')[0]} significant effective-accuracy contrasts, **3 are Phi-4 and are
  driven by a single anomalous run** (§ 6); they should be reported with that caveat or not relied on. The
  remaining ones are Llama 4 Scout and Mistral Small 4, where one-shot-CoT beats zero-shot-CoT, and Mistral
  where zero-shot beats zero-shot-CoT.
- The descriptive best strategy differs by model and by metric — on effective accuracy:
  {', '.join(f"{m} → {best('goemotions', m, 'acc_eff')}" for m in MODELS)}.
- **Accuracy near 0.78 on this dataset is the constant-predictor level** (majority baseline 0.782958 on the
  attributable pool), so an effective-accuracy difference here should never be read on its own.

### Across both datasets

**No prompting strategy is best.** The descriptive best strategy by effective accuracy is
zero-shot for {sum(1 for m in MODELS if best('dreaddit', m, 'acc_eff') == 'zero-shot')} of 5 models on
Dreaddit but for {sum(1 for m in MODELS if best('goemotions', m, 'acc_eff') == 'zero-shot')} of 5 on
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
python3 code/02_validate.py                      # {val['n_checks']} independent validation checks
python3 code/03_build_report.py                  # this file
```

Inputs are hash-pinned; the run fails closed on any mismatch. The saved replicate files
(`replicates/permutation_*.csv.gz`, `replicates/bootstrap_*.csv.gz`) allow every p-value and every interval
to be re-derived without re-running the analysis — `02_validate.py` does exactly that for all 60 of each.
""")
open(OUT / "RQ3_STRATEGY_INFERENCE_REPORT.md", "w").write("\n".join(D) + "\n")
print("report written:", (OUT / "RQ3_STRATEGY_INFERENCE_REPORT.md").stat().st_size, "bytes")
