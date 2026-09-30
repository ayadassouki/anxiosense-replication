# Latency — what was measured, and what may be displayed

Table: `tables/latency.csv` (30 rows, copied verbatim from the frozen latency tables — validation check 4
compares 30 configurations × 7 fields and finds 0 mismatches).

## A. How latency was measured

Two clocks were recorded on every attempt, documented in
`rq1_rq3_reporting_2026-09-21/REPORT.md` § "Latency instrumentation":

| Field | Unit | What it covers |
|---|---|---|
| `latency_ms` | ms (float) | Runner **client** wall clock (`time.perf_counter`) around the whole HTTP POST to Express `/api/workflow/evaluate` |
| `server_latency_ms` | ms (int) | Express `Date.now() − requestStart`: request receipt to just before the response is sent. Covers workflow creation, start, polling and result extraction |
| `response_body.metadata.latency_ms` | ms (int) | The same value as `server_latency_ms` (present on 101,066 of 102,137 attempts) |
| `mastra_poll_interval_ms` | ms | Effective Mastra poll cadence — **3000 in every run** |

Client minus server is a median of about 6 ms (p99 ≈ 17 ms), so the harness itself adds essentially nothing.

## B. Which statistic the existing results used

Per run, three statistics over the LLM-served terminal attempts: **mean, median and p90 (nearest rank)**. The
reported five-run value is the **mean ± sample SD of those five per-run statistics**. Models are never pooled.
The frozen tables are `rq1_rq3_reporting_2026-09-21/tables/rq3_dreaddit_latency.csv` and
`rq3_goemotions_latency.csv`, built from `rq3_terminal_latency_records.jsonl`, which was extracted from
hash-verified raw files (all 11 source runs pass their `attempts`/`index` SHA-256 checks in
`rq3_extract_summary.json`).

## C. Units

The frozen tables report **seconds**, converted from the millisecond fields, formatted as `mean ± SD`.

## D. What the quantity is

**End-to-end client latency for one complete assessment.** It is *not* model latency and *not* time to first
token. One value covers the whole multi-agent workflow — safety check, the four parallel agents, the report
agent — plus workflow creation, polling and result extraction. There is **no per-agent or per-phase timing**
in the frozen data: the product path `/api/workflow/run` logs `preAssess` / `mastra` / `groundingEval`
timings, but the publication runner used `/evaluate`, which computes none of them.

## E. Averaging

Yes — five runs, aggregated as mean ± sample SD (n − 1) of the per-run statistics. All 100,350 terminal
attempts have both latency fields; 0 are missing. The 1,275 safety intercepts short-circuit before any agent
call (median ≈ 7 ms) and are **excluded** from the latency statistics and counted separately.

## F. Availability

Complete: every dataset × model × strategy cell has latency, i.e. all 30 configurations, each over
3,495 (Dreaddit) or 3,110 (GoEmotions) LLM-served attempts.

## Recommendation: which measure to display

**Display the client mean in seconds (`client_latency_mean_s`), with the five-run SD, and state the 3-second
resolution in the caption.** Reasons:

- Client and server agree to ~6 ms, so the choice between them is immaterial; the client clock is the one a
  user would experience and is the one the existing results already use.
- The **median is the wrong choice here** even though it is normally more robust: the server sleeps 3 s before
  each status check, so each value is essentially *(number of polls × 3 s)* and the medians land on the 3 s
  lattice. Qwen's Dreaddit medians are 9.08 / 9.08 / 9.07 s across the three strategies — the lattice hides
  the differences the mean can still see.
- p90 is worth keeping in the appendix as a tail indicator, not in the main table.

## Latency by dataset × model × strategy (client mean ± SD, seconds)

| Model | Dreaddit ZS | Dreaddit ZS-CoT | Dreaddit 1S-CoT | GoEmotions ZS | GoEmotions ZS-CoT | GoEmotions 1S-CoT |
|---|---|---|---|---|---|---|
| Gemma 4 31B | 15.07 ± 2.73 | 13.10 ± 1.97 | 15.14 ± 3.77 | 11.54 ± 1.38 | 14.17 ± 3.54 | 10.09 ± 2.75 |
| Llama 4 Scout | 12.46 ± 0.88 | 14.08 ± 2.11 | 10.23 ± 0.64 | 10.78 ± 1.26 | 11.02 ± 2.20 | 10.00 ± 1.34 |
| Mistral Small 4 | 5.36 ± 0.03 | 5.25 ± 0.11 | 4.89 ± 0.12 | 3.98 ± 0.48 | 3.43 ± 0.11 | 3.32 ± 0.16 |
| Phi-4 | 12.91 ± 1.36 | 12.86 ± 1.19 | 10.13 ± 1.84 | 13.07 ± 0.35 | 13.09 ± 1.89 | 10.63 ± 2.23 |
| Qwen3.5 27B | 9.05 ± 0.27 | 8.67 ± 0.24 | 8.40 ± 0.45 | 7.27 ± 0.56 | 7.32 ± 0.37 | 7.32 ± 0.33 |

## Confounds that must appear in the caption or limitations

These are documented in the frozen reporting package and are the reason the statistical plan says
*"RQ3. No inference."* — **no latency difference in this table has been tested.**

1. **3-second measurement resolution.** Every value is quantised by the poll cadence, while several
   within-model strategy differences are under 1 s.
2. **Strategies ran in sequential blocks**, so strategy is confounded with time of day and provider load.
3. **Model is confounded with serving provider** (Mistral 3.3–5.4 s on the Mistral API versus Gemma
   10.1–15.1 s on CoreWeave). Cross-model latency comparisons say as much about infrastructure as about the
   model.
4. **Concurrent load.** `share_during_other_run_on_same_machine` is 1.00 for Llama/Dreaddit one-shot-CoT,
   1.00 for zero-shot-CoT and 0.82 for zero-shot — **all three** Llama Dreaddit configurations ran while
   another run shared the host (pub_004, Gemma via DeepInfra, not part of the grid). In per-run terms that
   is 15 of 15 Llama Dreaddit cells and 10,072 of 10,725 terminal attempts.
5. **Run-to-run drift.** Gemma Dreaddit one-shot-CoT has per-run means of 16.88, 20.29, 14.37, 10.09 and
   14.08 s.
6. **No per-agent timing, no time-to-first-token, no cost.**

## Safe wording for the paper

> Latency is reported as end-to-end client wall-clock time for one complete assessment, averaged per run and
> then across five runs. Measurement resolution is 3 s because the workflow is polled at that cadence, and
> prompting strategies were executed in sequential blocks, so latency differences between strategies are
> reported descriptively and were not tested. Cross-model latency also reflects differences in serving
> provider.
