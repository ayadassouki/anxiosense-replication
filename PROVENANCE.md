# Provenance and Public Sanitization

This repository is a curated replication package for the AnxioSense publication experiments.

## Frozen scientific manifest

The authoritative frozen grid manifest used by the analysis is:

`experiment/results/descriptive_2026-09-21/frozen_grid_manifest.json`

Original SHA-256:

`fba6a4617558b64bec61cee18e2a0b63e9457a03c6a3d94cd8e1a1916527dfa8`

This file is retained byte-for-byte because analysis scripts use its frozen hash as an integrity check.

## Public provenance derivative

`frozen_grid_manifest_public.json` is a privacy-sanitized derivative of the frozen manifest.

Only four `run_dir` values referring to a secondary execution machine were replaced with neutral `external_run_evidence/<run>` paths. No run identifiers, model outputs, predictions, labels, metrics, hashes, experimental conditions, or statistical results were changed.

Public derivative SHA-256:

`30ad583d7b3af45a3ae62fd182c0a1a575af8a1202ee6d1a7a285b26dce4149e`

The corresponding `run_dir` fields in four source-parse summaries were sanitized in the same way. These path fields identify historical storage locations and are not inputs to the statistical analysis.

The untouched source evidence is retained in the project's private evidence archive.

## Verification

After public-path sanitization:

- the RQ1-RQ3 table generator passed all 19 hash checks and 1,740 cross-check comparisons;
- the independent inferential verifier returned `passed: true` and `ISSUES: 0`.

The sanitization therefore does not alter the reported experimental or statistical results.
