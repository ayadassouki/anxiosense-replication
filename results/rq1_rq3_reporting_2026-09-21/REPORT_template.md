# AnxioSense publication grid: RQ1–RQ3 reporting (2026-09-21)

This is a reporting step on the frozen, independently verified results in `descriptive_2026-09-21`. That folder, the raw run data, the parser (1.0.0) and the scoring policy (MetricPolicy 1.0.0) were not changed. There were no model or API calls, no reruns and no significance tests. Every invalid output, refusal, out-of-vocabulary (OOV) prediction, `{}` output and the Phi-4 GoEmotions one-shot-CoT run 5 are included exactly as the frozen pipeline scored them.

**Measured** marks a value computed from stored records. **Interpretation** marks a reading of those values.

---

## 0. Inputs, definitions and rounding

**Grid.** 2 datasets × 5 models × 3 prompting strategies × 5 runs = 150 cells and 100,350 authoritative records. Dreaddit has 715 items per cell (16 safety intercepts, 699 attributable). GoEmotions has 623 scoreable items per cell (1 safety intercept, 622 attributable).

**Source for every RQ1/RQ2 number.** `descriptive_2026-09-21/authoritative_records.jsonl`, recomputed here with exact rational arithmetic (`code/rq12_tables.py`). It was then cross-checked against the frozen `per_run_results.csv`, `cell_metrics.json`, `aggregate_results.csv` and `aggregate_five_runs.json`, and against the verification record `verification_2026-09-21/metrics_verification_result.json`.

- 4,457 checks were run: 3,811 bit-identical and 646 differing only in the last binary digit. Every one of those 646 is already listed in the independent verification. There were **0 conflicts**, so no value had to be chosen between sources (`rq12_crosscheck.json`).

**Metric definitions (MetricPolicy 1.0.0, as frozen).**

- *Safety intercepts* are excluded from model attribution. They short-circuit before any LLM call.
- *Attributable* = N_total − N_safety.
- *Valid* = the stored `prediction_valid` is true.
- *Model-invalid* = the stored `failure_class` is `MODEL_BEHAVIOUR`: unparseable, truncated, `{}`, refusal or OOV, exactly as the parser classified it.
- *Conditional accuracy* = correct / valid.
- *Effective accuracy* = correct / attributable. Invalid outputs count as wrong.
- *Per-class precision, recall and F1* are computed on valid predictions. A value is 0 when undefined.
- *Macro-P, macro-R and macro-F1* are the unweighted means over the fixed label list: Dreaddit [0, 1]; GoEmotions [anxiety, fear, sadness, frustration, non_distress].
- *Evaluability* = valid / attributable.
- *Five-run value* = the mean of the five per-run values, ± the sample SD (n − 1).
  - For acc. (cond.), acc. (eff.), macro-F1 and evaluability, these are the frozen aggregates.
  - The five-run macro-P and macro-R are not in the frozen aggregate files. They are the same mean ± SD applied to the frozen per-run values, which were cross-checked.

**Majority baseline (frozen).** Dreaddit 369/715 = 0.516 (class 1). GoEmotions 487/623 = 0.782 (non_distress).

- These are computed over all included items, while model accuracies exclude safety intercepts.
- On the attributable set, the majority rates are 355/699 = 0.508 and 487/622 = 0.783.
- **Measured:** using the attributable-set rate instead of the frozen baseline does not change any "runs above baseline" count in this report.

**Rounding rule.**

- Accuracy-type values are shown to 3 decimals, ROUND_HALF_UP.
- Rounding is applied to the exact rational value (means) or to a 60-digit decimal (SDs), never to a binary float.
- **Checked:** no presented five-run value lies exactly on a 3-decimal half boundary. No presented value rounds differently from the corresponding frozen float.
- The two known per-run half-boundary cases are both per-class F1 for class 1 on Dreaddit:
  - Llama 4 Scout zero-shot run 1: exact 59/80 = 0.7375 → 0.738 under this rule.
  - Qwen3.5 27B one-shot-CoT run 4: exact 0.4875 → 0.488.
  - Neither appears in a presented table, because the tables show five-run aggregates.
- Latency values are shown in seconds to 2 decimals (ROUND_HALF_UP of the measured float).
- A displayed 1.000 or ±0.000 can hide a small non-zero value. The count columns give the exact numbers.

**Interpretation boundary.** Dreaddit scores the Referral agent's `risk_level` (low → 0; moderate/urgent → 1) against *stress vs non-stress* labels. It is a stress-detection proxy. It does not validate the GoEmotions `anxiety` class or clinical anxiety detection.

---

## RQ1: Which LLM yields the best results?

### RQ1 · Dreaddit (binary stress; 5-run mean ± SD)

Source: `tables/rq1_dreaddit.csv`, built from `authoritative_records.jsonl` and cross-checked as above. Infrastructure failures = 0 in every cell. Safety intercepts = 16 per run in every cell.

{{TABLE:rq1_dreaddit}}

### RQ1 · GoEmotions (5-class; 5-run mean ± SD)

Source: `tables/rq1_goemotions.csv`, built the same way. Infrastructure failures = 0 in every cell. Safety intercepts = 1 per run in every cell.

{{TABLE:rq1_goemotions}}

### RQ1 · Dreaddit: what the measured values show

**Measured**

- **Llama 4 Scout** has the highest five-run conditional accuracy, effective accuracy, macro-F1 and macro-recall under **each** of the three strategies.
  - Highest cells: zero-shot at acc. (cond.) 0.752 and macro-F1 0.752, and one-shot-CoT at acc. (cond.) 0.752, acc. (eff.) 0.750 and macro-F1 0.751.
- **Phi-4** is next: zero-shot macro-F1 0.744, one-shot-CoT 0.730.
- **Gemma, Mistral and Qwen** have macro-F1 0.598–0.675.
  - They label most items as not stressed: class-0 recall 0.942–0.974 against class-1 recall 0.302–0.450. See the Dreaddit per-class table in RQ2.
- **Macro-precision gives a different ranking** within a narrow band (0.742–0.760). Gemma zero-shot is highest (0.760) and Phi-4 zero-shot-CoT lowest (0.742).
- **Invalid outputs change the picture for the two leading models under zero-shot.**
  - Llama and Phi-4 each have 106 model-invalid outputs over five runs (evaluability 0.970).
  - Their accuracy drops from conditional to effective: Llama 0.752 → 0.730; Phi-4 0.745 → 0.722.
  - Gemma and Mistral are the most evaluable (≥ 3,494 / 3,495 valid in every cell).
  - Qwen zero-shot-CoT has the most invalid outputs: 269, evaluability 0.923, effective accuracy 0.602.
- All 15 cells exceed the 0.516 baseline on both accuracy measures in every run.

**Interpretation**

- On Dreaddit, Llama 4 Scout has the highest observed accuracy, effective accuracy, macro-F1 and macro-recall. This is consistent across all three strategies, so it does not depend on which accuracy-type metric is chosen.
- Two qualifiers apply:
  1. Phi-4 is close behind, and the top cells differ by amounts similar to their run-to-run SDs (e.g. Phi-4 zero-shot ± 0.012).
  2. Llama's zero-shot advantage is partly offset by a higher invalid-output rate than Gemma or Mistral.
- Ranked by macro-precision or evaluability, Llama is not first.

### RQ1 · GoEmotions: what the measured values show

**Measured**

- **Gemma 4 31B** has the highest conditional accuracy, effective accuracy and macro-precision under every strategy. Its accuracies are 0.813–0.820, and its evaluability is 0.998–1.000.
- **Macro-F1 does not have a single leader.**
  - Gemma is highest under zero-shot (0.593) and zero-shot-CoT (0.583).
  - Under one-shot-CoT, Mistral Small 4 (0.594) is above Gemma (0.585).
  - Mistral one-shot-CoT (0.594) vs Gemma zero-shot (0.593) is the largest macro-F1 pair in the grid, separated by less than either SD.
- **Macro-recall runs the other way.** Gemma has the lowest macro-recall cell (0.543, zero-shot-CoT). Llama 4 Scout and Mistral lead: zero-shot Llama 0.632, zero-shot-CoT Mistral 0.633, one-shot-CoT Llama 0.622.
- **Phi-4: conditional and effective accuracy disagree.**
  - Among models, its conditional accuracy is second only to Gemma (best cell: zero-shot-CoT 0.809).
  - Its evaluability is 0.840–0.941, so its effective accuracy is lower (0.673–0.762).
  - Phi-4 one-shot-CoT has the lowest effective accuracy of any cell, 0.673 ± 0.126. That is driven by run 5, where 271 of 622 attributable outputs were invalid. The run is included as frozen.
- **Llama 4 Scout** has the lowest accuracies (0.727–0.767 cond.) but among the highest macro-recall.
- **Qwen3.5 27B** is almost fully evaluable, and its runs are nearly identical: SD ≤ 0.002 on accuracies, down to 0.000 at 3 decimals for one-shot-CoT.

**Interpretation**

- On GoEmotions, the answer depends on the metric:
  - accuracy and macro-precision favour Gemma;
  - macro-F1 is a near-tie between Gemma and Mistral (one-shot-CoT);
  - macro-recall favours Llama and Mistral;
  - conditional vs effective accuracy moves Phi-4 from second to fourth when models are ranked by their best cell.
- The accuracy-type ranking largely tracks how often each model predicts the majority class. See RQ2.

### RQ1 · Across datasets

**Measured**

- The model with the highest Dreaddit results (Llama 4 Scout) has the lowest GoEmotions accuracies.
- The model with the highest GoEmotions accuracies (Gemma 4 31B) is in the lower group on Dreaddit macro-F1 (0.650–0.675).

**Interpretation**

"Best LLM" cannot responsibly be reduced to one model. The leader changes with the dataset, and on GoEmotions it also changes with the metric (accuracy vs macro-F1 vs macro-recall vs effective accuracy). Invalid-output rates change the picture further for Llama, Phi-4 and Qwen. Descriptively:

- **Dreaddit:** Llama 4 Scout is the consistent leader, with Phi-4 close.
- **GoEmotions:** Gemma leads on accuracy, Gemma and Mistral share macro-F1, and Llama and Mistral lead on recall.

No statistical superiority is claimed; significance testing has not been done.

---

## RQ2: What is the accuracy of AnxioSense?

### What "AnxioSense accuracy" can and cannot mean here

**What was evaluated.** The evaluation called AnxioSense's `/api/workflow/evaluate` path, which runs the multi-agent workflow in social-media mode: emotion, symptom, context and referral agents, then the report step. Each configuration uses **one** LLM with **one** prompting strategy.

- The Dreaddit label comes from the Referral agent's risk level.
- The GoEmotions label comes from the Emotion agent's first emotion, mapped through the frozen V1 mapping.

There are **30 configurations** (5 models × 3 strategies) per dataset. Each has its own accuracy.

**No single overall figure exists.** The publication runner, the frozen grid manifest and MetricPolicy 1.0.0 define no aggregation across models or strategies, and none across the two datasets, which score different agents on different targets. **No pre-specified single overall AnxioSense accuracy exists, and none is produced here.** Results are given per configuration and as ranges.

**What the older protocol says.** The July 2026 `evaluation/AnxioSense_Experimental_Setup.docx` (§6.3) does not aggregate either. It *designates* a configuration for RQ2: "Full pipeline (top LLM, 1S-CoT)". The top LLM is defined as the highest macro-F1 "on symptom extraction" among the five models under one-shot-CoT on Dreaddit. Three caveats apply:

1. Symptom extraction was not scored in this grid.
2. Choosing the "top" model on these same test items selects on the evaluation data, which is optimistic.
3. Whether that document governs the publication analysis is a decision for Aya and the supervisors.

For transparency only, here is what the rule would pick if Dreaddit referral macro-F1 were substituted for symptom-extraction macro-F1:

- It would select **Llama 4 Scout, one-shot-CoT**, whose Dreaddit macro-F1 of 0.751 is above Phi-4's 0.730.
- That configuration measures:
  - **Dreaddit:** acc. (cond.) 0.752 ± 0.004, acc. (eff.) 0.750 ± 0.005, macro-F1 0.751 ± 0.005.
  - **GoEmotions:** acc. (cond.) 0.767 ± 0.008 and acc. (eff.) 0.732 ± 0.009, **both below the 0.782 majority baseline in all 5 runs**, with macro-F1 0.544 ± 0.013.

This is not presented as "the" AnxioSense accuracy.

**Metric and task limits.**

- Cohen's weighted κ is listed in that protocol for RQ2, but it is not part of the frozen scoring policy and is not computed here.
- Dreaddit measures stress vs non-stress through a referral-level proxy, not anxiety.

### RQ2 · Dreaddit (majority baseline 0.516; Δ = five-run mean − baseline)

Source: `tables/rq2_dreaddit.csv`. Baseline from the frozen dataset manifest, 369/715. "Runs > base" counts runs whose exact per-run accuracy exceeds 369/715.

{{TABLE:rq2_dreaddit}}

Supplementary, Dreaddit per-class (`tables/rq2_dreaddit_per_class.csv`, per-class metrics as frozen in `cell_metrics.json`, five-run mean ± SD):

{{TABLE:rq2_dreaddit_per_class}}

### RQ2 · GoEmotions (majority baseline 0.782; Δ = five-run mean − baseline)

Source: `tables/rq2_goemotions.csv`. Baseline from the frozen dataset manifest, 487/623.

{{TABLE:rq2_goemotions}}

Supplementary, GoEmotions per-class recall and non_distress prediction share (`tables/rq2_goemotions_per_class.csv`; F1 and all predicted shares are in the CSV):

{{TABLE:rq2_goemotions_per_class}}

### RQ2 · Plain factual interpretation

**Dreaddit, measured**

- Across the 15 configurations:
  - conditional accuracy 0.648–0.752;
  - effective accuracy 0.602–0.750;
  - macro-F1 0.598–0.752.
- Every configuration exceeds the 0.516 majority baseline on both accuracy measures in all 5 runs.
- The attributable set is close to balanced: 355 stressed / 344 not stressed.
  - So accuracy and macro-F1 track each other.
  - Where they separate (Gemma, Mistral, Qwen: macro-F1 below conditional accuracy in every cell), the per-class table shows why: those models recall class 0 far better than class 1.
- A constant "stressed" predictor on the attributable set would have macro-F1 0.337, as a derived reference (not a frozen result).

**GoEmotions, measured**

- Across the 15 configurations:
  - conditional accuracy 0.727–0.820;
  - effective accuracy 0.673–0.820;
  - macro-F1 0.520–0.594.
- **Several configurations are at or below the 0.782 majority baseline.** These are reported, not hidden:
  - 6 of 15 on mean conditional accuracy;
  - 9 of 15 on mean effective accuracy.
- Only Gemma (all three strategies) and Qwen (zero-shot and zero-shot-CoT) exceed the baseline on both measures in all 5 runs.
- Mistral one-shot-CoT is marginal: 4/5 runs above on conditional accuracy, 3/5 on effective.
- Phi-4's effective accuracy is below the baseline in every run under all three strategies. Its conditional accuracy is above the baseline in 5/5 runs (zero-shot-CoT, one-shot-CoT) and 3/5 runs (zero-shot).

**Why accuracy and macro-F1 diverge on GoEmotions (class imbalance)**

**Measured**

- The attributable set has 487 non_distress (78.3%), 81 frustration, 33 sadness, 15 fear and **6 anxiety** items.
- A constant non_distress predictor would reach accuracy 0.782 but macro-F1 0.176 and macro-recall 0.200 (derived reference).
- Accuracy is therefore dominated by the majority class. Macro-F1 weights each of the five classes equally, so the rare distress classes count as much as non_distress.
- Gemma predicts non_distress for 0.886–0.901 of its valid outputs, against a true share of 0.783.
  - This gives non_distress recall 0.950–0.960 and the highest accuracies.
  - But sadness recall is 0.242–0.261 and frustration recall 0.247–0.294.
- Llama 4 Scout predicts non_distress less often (0.716–0.801).
  - Its sadness recall is higher (0.432–0.462).
  - Its accuracy is lower.

**Interpretation**

- High GoEmotions accuracy here mostly reflects agreement on non_distress. It is not evidence of distress-class detection.
- No configuration's macro-F1 exceeds 0.594. Every configuration has macro-F1 far above the constant predictor's 0.176. So the models do separate distress classes, but only partially.
- The anxiety class has 6 items, so one item moves anxiety recall by 1/6 (≈ 0.167). Per-class anxiety values are very coarse.
- Under the frozen mapping, a non_distress prediction arises from an empty emotion list (`ok_empty_list`).

**Conditional vs effective accuracy**

- Conditional accuracy ignores invalid outputs; effective accuracy counts them as wrong.
- They differ most for Phi-4 (GoEmotions), Llama 4 Scout (both datasets) and Qwen zero-shot-CoT (Dreaddit). Reporting only conditional accuracy would favour models that fail to produce a usable answer more often.

---

## RQ3: Which prompting strategy is the most efficient?

### RQ3 · Latency-data audit (from saved records only)

All 11 source runs (the 10 grid runs plus the pub_013 replacement run)' `raw/attempts.jsonl` and `raw/index.jsonl` were sha256-verified against the frozen grid manifest before reading (all matched). The extraction script is `code/rq3_latency_extract.py`, with outputs in `rq3_extract_summary.json`.

**1. Latency fields that exist** (in 100% of attempt records unless stated):

| Field | Unit | Meaning (from code) |
|---|---|---|
| `latency_ms` | ms (float) | Runner client wall-clock (`time.perf_counter`) around the whole HTTP POST to Express `/api/workflow/evaluate`. |
| `server_latency_ms` | ms (int) | Express `Date.now() − requestStart`, from request receipt to just before the response is sent. Covers workflow creation, start, polling and result extraction. |
| `response_body.metadata.latency_ms` | ms (int) | Same value as `server_latency_ms`. Present only when a response body parsed (101,066 of 102,137 attempts). |
| `mastra_poll_interval_ms` | ms | Effective Mastra poll cadence, verified at preflight. **3000 in every run.** |
| `timestamp_utc` | ISO time | When the attempt was written. |
| `token_usage` | tokens | Not a latency. The server takes the first `tokenUsage` object it finds in the workflow output, so it is not documented as a per-assessment total. Missing for 2,134 LLM-served terminal attempts. Not used. |

**2. What is not recorded.**

- No per-agent timing (emotion, symptom, context, referral, report).
- No phase timings. The Experimental Setup document's `preAssessMs`, `mastraMs` and `groundingMs` are absent.
- No `server_step_timings`, although it was planned in the runner design (`parallelMs`, `reportMs`, `totalMs`).
- No provider-side processing time and no time-to-first-token.
- No host or machine identifier, and no concurrency level.

**3. Completeness.**

- All 100,350 authoritative (terminal) attempts have `latency_ms` and `server_latency_ms`. 0 are missing.
- 99,075 are LLM-served. 1,275 are safety intercepts: they short-circuit before any agent call (median about 7 ms), so they are excluded from the latency statistics and counted separately.

**Comparability**

- **Poll quantisation.** 99,049 of 99,075 (99.97%) LLM-served terminal latencies lie within 0.5 s of a multiple of 3 s.
  - Client minus server is a median of about 6 ms (p99 about 17 ms), so the harness adds almost nothing.
  - The server sleeps 3 s before each status check, so each value is essentially (number of polls × 3 s). The workflow actually finished somewhere in the preceding ≈ 3 s.
  - Measurement resolution is therefore 3 s, and medians sit on the lattice. For example, Qwen's Dreaddit medians are 9.08 / 9.08 / 9.07 s across strategies.
- **Execution order.** The runner loops model → strategy → run → sample. Within each model × dataset, the three strategies ran in consecutive time blocks (zero-shot first, one-shot-CoT last). **Strategy is confounded with time**: provider load and time of day. It is also plausibly confounded with local Mastra storage growth, which was not measured.
- **Machine.**
  - Runs were executed on two machines. This is inferred from where the run folders are stored (Aya's repo vs the USB copied from Heba's laptop), because `experiment.json` records no host.
  - Within each model × dataset, all strategies ran on the same machine. The one exception is Gemma Dreaddit one-shot-CoT run 5 (pub_013, Aya, 2026-09-19/20), whereas runs 1–4 ran on Heba's machine on 2026-09-16.
  - Comparisons across models also cross machines and upstream providers.
- **Concurrent load.** 10,072 of 10,725 Llama 4 Scout Dreaddit terminal attempts were recorded while another run (pub_004, Gemma via DeepInfra, not part of the grid) was active on the same machine.
  - By strategy: zero-shot 82%, zero-shot-CoT 100%, one-shot-CoT 100%.
  - No other grid cell overlaps another run on the same machine.
- **Retries.** The latency used is that of the terminal (successful) attempt. Time spent in earlier failed attempts and backoff is not included. The number of retried assessments is shown per row.
- **Run-to-run drift.** This is large for some models. For example, Gemma Dreaddit one-shot-CoT has per-run mean latencies of 16.88, 20.29, 14.37, 10.09 and 14.08 s.

**4. Can total system response time be calculated?** **Yes, descriptively.** It is the end-to-end wall-clock per assessment of the AnxioSense evaluation path, from both the client and the server side, complete for every record. Limits:

- the 3 s resolution;
- the order, machine and concurrency confounds above.

It covers the `/api/workflow/evaluate` path (social-media mode, no GAD-7), not the user-facing `/run` path.

**5. Can individual-agent latency be calculated?** **No.** No per-agent or per-phase timing was stored, and it cannot be derived from a single end-to-end number, because four agents run in parallel before the report step.

- Mastra's own observability store may contain per-span timings keyed by the recorded `mastra_run_id`.
- That store is not part of the frozen experiment records, is split across two machines, and was **not** inspected or used here.

**Verdict on RQ3 support.** The planned analysis is supported **only partially**:

- *Total system response time*: reportable descriptively, with the caveats above.
- *Individual-agent processing latency*: not answerable from the recorded evidence.

### RQ3 · Dreaddit latency by model × strategy (LLM-served terminal attempts; 5-run mean ± SD of per-run statistics)

Source: `tables/rq3_dreaddit_latency.csv`, built from `rq3_terminal_latency_records.jsonl`, which was extracted from hash-verified raw files. Client = `latency_ms`, server = `server_latency_ms`. Per run: mean, median and p90 (nearest rank). The five-run value is the mean ± sample SD of the five per-run statistics. Models are not pooled.

\*Machine is inferred from where the run folder is stored. "Share during other run" = fraction of the cell's terminal attempts recorded while another run was active on the same machine.

{{TABLE:rq3_dreaddit_latency}}

### RQ3 · GoEmotions latency by model × strategy

Source: `tables/rq3_goemotions_latency.csv` (same definitions).

{{TABLE:rq3_goemotions_latency}}

### RQ3 · Plain factual interpretation

**Measured**

- **Differences between models are much larger than differences between strategies.**
  - Mistral Small 4 has mean client latency 4.89–5.36 s on Dreaddit and 3.32–3.98 s on GoEmotions.
  - Gemma 4 31B has 13.10–15.14 s on Dreaddit and 10.09–14.17 s on GoEmotions.
- **One-shot-CoT had the lowest five-run mean latency for 4 of 5 models on each dataset.**
  - Dreaddit: all models except Gemma, where zero-shot-CoT was lowest at 13.10 s.
  - GoEmotions: all models except Qwen, where zero-shot was lowest at 7.27 s against 7.32 s for both CoT strategies.
- **Several of these differences are within the measurement's limits.**
  - For Mistral and Qwen they are below the 3 s resolution. Their medians are identical across strategies: Mistral 6.04–6.06 s on Dreaddit and 3.04–3.05 s on GoEmotions; Qwen 9.07–9.08 s and 6.04 s.
  - For Gemma, Llama and Phi-4 they are of the same order as the run-to-run SDs (up to ± 3.77 s).
- In each run's initial dispatch, the one-shot-CoT block was executed **last** within its model. Later resume/retry invocations re-dispatched a small number of items out of order, and Gemma Dreaddit one-shot-CoT run 5 was run days later on the other machine. So the strategy ordering cannot be separated from time effects.
- Server and client means agree to within about 0.01 s everywhere.

**Interpretation**

- The stored records do not show that any prompting strategy makes the system faster in a way that can be separated from:
  - the 3 s poll quantisation;
  - execution order and time;
  - machine differences;
  - for Llama Dreaddit, concurrent load.
- The consistent direction (one-shot-CoT lowest in 8 of 10 model × dataset pairs) is a descriptive observation only. It is not an efficiency conclusion. A controlled comparison would need randomised or interleaved strategy order, finer timing and per-agent timing.
- **Performance and efficiency are separate results.** The highest-accuracy strategy is not automatically the most efficient, and the reverse holds too. For example, Qwen one-shot-CoT on Dreaddit has Qwen's lowest mean latency (8.40 s) and its lowest conditional accuracy (0.648).
- The setup document's own RQ3 wording ("minimises false positive symptom extractions while maintaining recall") is a different, accuracy-type question. Symptom extraction was not scored in this grid.

---

## What these results do NOT establish yet

- **No inferential statistics.** No significance test has been performed. None of the differences above may be described as statistically significant, and "higher" and "lower" are descriptive only.
  - The five-run SDs reflect variation between repeated runs on the **same items**. They are not item-sampling uncertainty or confidence intervals.
  - A near-zero SD (e.g. Qwen) shows the model was consistent across runs, not that its accuracy is precisely estimated.
- **No single overall AnxioSense accuracy.** None is pre-specified, and none was produced. The older protocol's "top LLM, 1S-CoT" rule is a selection on test data, and its criterion (symptom extraction) was not measured.
- **No clinical claim.**
  - Dreaddit measures stress vs non-stress through a referral-level proxy.
  - It does not validate anxiety detection or the GoEmotions `anxiety` class.
  - GoEmotions has only 6 anxiety items.
  - Both datasets are Reddit text, not a clinical population.
- **No per-agent efficiency result.** Agent-level and phase latency were not recorded. Total response time is 3 s-quantised and confounded with execution order, machine and, for Llama Dreaddit, concurrent load.
- **Results are conditional on the frozen methodology.** Under the frozen parser and policy:
  - `{}` outputs, malformed JSON, refusals and OOV labels are model-invalid;
  - non_distress arises from empty emotion lists;
  - Dreaddit outputs whose readable `risk_level` sits inside unparseable text stay invalid;
  - Phi-4 GoEmotions one-shot-CoT run 5 is included.

  Alternative policies were neither applied nor evaluated here. The open items in `descriptive_2026-09-21/ISSUES_FOR_AUDIT.md` remain open.
- **Serving configuration.** Results apply to the model/provider routes used, e.g. Gemma served by CoreWeave at fp4. They may not transfer to other serving setups.
- **Protocol items not covered.** Cohen's weighted κ, per-agent/phase efficiency metrics, and RQ4/RQ5 measures listed in the Experimental Setup document are not addressed by these tables.

---

## Files in this folder

- `code/rq12_tables.py`: RQ1/RQ2 recomputation, cross-check and tables. It aborts on any conflict.
- `code/rq3_latency_extract.py`: hash-verified, read-only latency audit, concurrency check and per-record latency extract.
- `code/rq3_latency_tables.py`: RQ3 tables.
- `code/build_report.py`: renders this report from the CSVs and checks every quoted number against them.
- `tables/*.csv`: all presented tables.
- `rq12_full_precision.json`: exact rational values and 60-digit SDs.
- `rq12_crosscheck.json`, `rq1_metric_ranks.json`.
- `rq3_extract_summary.json`, `rq3_terminal_latency_records.jsonl`, `rq3_latency_per_cell.json`, `rq3_strategy_means_by_model.json`.
- `report_number_check.json`, `freeze_check.txt`.
