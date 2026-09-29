# Descriptive publication results - 2026-09-21

Derived outputs only. No raw run data was modified; runs were read, never written.
No model/API calls. Scoring uses the repository's own parse() and cell_metrics()/aggregate_cells()
unchanged (parser 1.0.0, metric policy 1.0.0). rescore.py was NOT used because it writes
into run directories.

Files
- code/stage_a_parse.py      parses every final terminal attempt of one source run
- code/stage_b_compose.py    composes the 150-cell grid, validates, freezes, scores
- parsed/<run>.jsonl         parsed terminal records per source run (all cells of that run)
- source_parse_summaries/    per-run parse counts + SHA-256 of raw index/attempts/experiment.json
- frozen_grid_manifest.json  composition rule, per-cell source run, record hashes, validation
- authoritative_records.jsonl the 100,350 records actually scored
- cell_metrics.json          full cell_metrics() output for all 150 cells
- aggregate_five_runs.json   aggregate_cells() output (mean/sd across runs)
- per_run_results.csv        150 rows
- aggregate_results.csv      30 rows (mean/sd plus summed counts)
- ISSUES_FOR_AUDIT.md        anomalies found, preserved, not fixed

Composition: Dreaddit x Gemma = pub_011 minus cell dreaddit|google/gemma-4-31b-it|one-shot-cot|run5,
plus all 715 records of pub_013 for that cell. Validation: 150 cells, 100,350 records, 0 problems.
