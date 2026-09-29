# Provenance and Public Sanitization

This repository is a curated replication package for the AnxioSense publication
experiments. It contains the frozen analysis artifacts, the code that produced
them, and the documents that report them. It does not contain the raw model-response
evidence those artifacts were derived from (see "What is not distributed here").

Every count and hash in this file was read from the artifacts themselves when it
was written, not transcribed by hand.

## Frozen scientific manifest

The authoritative frozen grid manifest is:

`results/descriptive_2026-09-21/frozen_grid_manifest.json`

SHA-256: `fba6a4617558b64bec61cee18e2a0b63e9457a03c6a3d94cd8e1a1916527dfa8`

This file records absolute filesystem paths from the machines the experiments were
run on, so it is **retained privately and is not distributed with this package**.
It is kept byte-for-byte because the analysis scripts verify the raw run evidence
against the hashes it contains.

## Public provenance derivative

`frozen_grid_manifest_public.json` is a privacy-sanitized derivative of that manifest and is
the file the public scripts read.

SHA-256: `30ad583d7b3af45a3ae62fd182c0a1a575af8a1202ee6d1a7a285b26dce4149e`

The two manifests were compared leaf by leaf: **3,069 values, of which exactly
11 differ, and every one of them is a `run_dir` path** rewritten to a neutral
`external_run_evidence/<run>` form. No run identifiers, model outputs, predictions,
labels, metrics, hashes, experimental conditions, or statistical results differ
between the two files.

## Other sanitized artifacts

The same `run_dir` rewrite was applied to:

- the 11 per-run source-parse summaries in
  `results/descriptive_2026-09-21/source_parse_summaries/`;
- the 11 `hash_checks[*].run_dir` entries in
  `results/rq1_rq3_reporting_2026-09-21/rq3_extract_summary.json`.

These path fields record historical storage locations. They are not inputs to any
metric, test, or reported result.

## Historical storage attribution

The runs were executed on two machines, and the raw evidence originally sat in two
separate stores: the first author's working repository and a USB copy of the second
machine. The original extraction script determined each run's machine by which of
those two directories the run folder was found in.

This package distributes all raw evidence under a single `external_run_evidence/`
directory, so that split no longer exists on disk, and the machine of origin is
**not recoverable from any path in this package and is not a function of the run id**.
It is therefore carried as explicit provenance data in two places:

- `activity_windows[*].location` in `results/rq1_rq3_reporting_2026-09-21/rq3_extract_summary.json`
  (33 runs: 14 on the second machine, 19 on the first);
- the `RUN_STORAGE_LOCATION` table in
  `results/rq1_rq3_reporting_2026-09-21/code/rq3_latency_extract.py`, transcribed
  from that frozen record.

This attribution is inherited from the original data collection. A replicator
working from the distributed layout alone cannot independently re-derive it.

## What is not distributed here

- **Raw run evidence** (`raw/attempts.jsonl`, `raw/index.jsonl` and run directories):
  too large for version control, and retained in the project's private evidence
  archive. To re-run the extraction step, point `ANXIOSENSE_RUNS_ROOT` at a local
  copy of `external_run_evidence/`; the scripts sha256-verify every raw file against
  the frozen manifest before reading it and abort on any mismatch.
- **The private frozen manifest** named above.
- **Credentials.** No `.env` file, API key, or other secret is tracked in this
  repository or in its history.

## Verification after sanitization

- RQ1-RQ3 cross-check (`results/rq1_rq3_reporting_2026-09-21/rq12_crosscheck.json`):
  4,457 comparisons, 3,811 exact, 646
  agreeing to the last floating-point unit, 0 problems.
- Independent inferential verification
  (`results/inferential_2026-09-21/verification/verification_result.json`):
  `passed: true`, 0 issues.

The sanitization changes filesystem path strings only. It does not alter any
reported experimental or statistical result.
