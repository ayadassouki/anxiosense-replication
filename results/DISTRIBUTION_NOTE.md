# Distribution note — `descriptive_2026-09-21`

**Added 2026-09-29.** This note explains the relationship between the 2026-09-21 freeze of the
descriptive package and what this replication repository actually distributes. It documents an
**intentional, sanitised subset** — not a corrupted or broken freeze.

## The freeze is intact

`verification_2026-09-21/freeze_hashes_after.txt` is the dated attestation over the complete
**32-file** `descriptive_2026-09-21/` package. It is unmodified (sha256 `5567988b1fd708fa4a81808c36b728f8a5fa471ffa2822a79d3830d41927ece5`)
and byte-identical to `freeze_hashes_before.txt`, which is what establishes that the independent
verification step changed nothing.

**That attestation still holds.** The source working tree in which the freeze was taken verifies
against this same inventory at **32 exact / 0 changed / 0 missing**, with the full `parsed/`
directory present and the original `run_dir` values in place. Nothing was lost, corrupted or
silently altered.

## What this repository distributes

**20 of the 32 recorded files.** The original 32-file freeze remains the historical record; this
public repository ships 20 of those files. Every artifact that any reported analysis reads is
present: `authoritative_records.jsonl`, `cell_metrics.json`, `aggregate_five_runs.json`,
`aggregate_results.csv`, `per_run_results.csv`, the composition code and the 11 per-run
source-parse summaries. The frozen grid manifest ships only as its sanitised public derivative
`frozen_grid_manifest_public.json`. Of the 12 files not distributed, 11 are parsed intermediates
withheld for size and one is the private grid manifest withheld for privacy.

### Not distributed — 11 per-run parsed intermediates

| recorded path | recorded bytes |
|---|---|
| `parsed/pub_001_dreaddit_qwen.jsonl` | 16,930,250 |
| `parsed/pub_002_dreaddit_mistral.jsonl` | 17,495,188 |
| `parsed/pub_003_dreaddit_llama.jsonl` | 17,379,948 |
| `parsed/pub_005_dreaddit_phi.jsonl` | 16,943,218 |
| `parsed/pub_006_goemotions715_mistral.jsonl` | 15,062,577 |
| `parsed/pub_007_goemotions715_qwen.jsonl` | 14,549,242 |
| `parsed/pub_008_goemotions715_phi.jsonl` | 14,624,444 |
| `parsed/pub_009_goemotions715_llama.jsonl` | 14,962,193 |
| `parsed/pub_011_dreaddit_gemma_coreweave.jsonl` | 17,432,575 |
| `parsed/pub_012_goemotions715_gemma_coreweave.jsonl` | 15,010,293 |
| `parsed/pub_013_dreaddit_gemma_coreweave_osc_run5.jsonl` | 1,176,706 |

Total **161,566,634 bytes**. These are per-run intermediates produced by the parser and consumed
only by the composition step; they are **not inputs to any reported metric, test statistic or
table**. They were excluded for size. They were never tracked in this repository's git history.

### Not distributed - the private frozen grid manifest

| recorded path | recorded bytes | recorded sha256 |
|---|---|---|
| `frozen_grid_manifest.json` | 124,408 | `fba6a4617558b64bec61cee18e2a0b63e9457a03c6a3d94cd8e1a1916527dfa8` |

Withheld for **privacy**, not size: 11 of its `run_dir` values are absolute filesystem paths on the
machines the experiments ran on. Its sanitised public derivative `frozen_grid_manifest_public.json`
(sha256 `30ad583d7b3af45a3ae62fd182c0a1a575af8a1202ee6d1a7a285b26dce4149e`, 123,665 bytes) **is**
distributed, and is what every public analysis and verification script reads. The two differ in
those 11 `run_dir` strings and in nothing else, so no experimental value, metric, test statistic or
reported result depends on the difference.

The historical records - `PREREGISTRATION_FREEZE.json`, `analysis_manifest.json`,
`INPUT_HASHES.sha256`, `precheck.json`, `source_hashes.txt` and the 2026-09-21 attestations -
continue to record the private manifest's hash `fba6a461...`, because that is what the analysis
actually read. They are deliberately left unchanged. Where the private original is absent,
`rq3_strategy_inference_2026-09-25/code/02_validate.py` verifies the declared public derivative in
its place and prints which mode it used.

### Sanitised — 11 source-parse summaries

| path |
|---|
| `source_parse_summaries/pub_001_dreaddit_qwen.json` |
| `source_parse_summaries/pub_002_dreaddit_mistral.json` |
| `source_parse_summaries/pub_003_dreaddit_llama.json` |
| `source_parse_summaries/pub_005_dreaddit_phi.json` |
| `source_parse_summaries/pub_006_goemotions715_mistral.json` |
| `source_parse_summaries/pub_007_goemotions715_qwen.json` |
| `source_parse_summaries/pub_008_goemotions715_phi.json` |
| `source_parse_summaries/pub_009_goemotions715_llama.json` |
| `source_parse_summaries/pub_011_dreaddit_gemma_coreweave.json` |
| `source_parse_summaries/pub_012_goemotions715_gemma_coreweave.json` |
| `source_parse_summaries/pub_013_dreaddit_gemma_coreweave_osc_run5.json` |

On 2026-09-23 these files were path-sanitised for public release, in the same operation that
produced `frozen_grid_manifest_public.json`: the private absolute `run_dir` was rewritten to
`external_run_evidence/<run>`, and the rewriter added one trailing newline. Sizes therefore differ
from the inventory by **−59 bytes** for the four second-machine runs and **−71 bytes** for the seven
first-machine runs — the difference between the two private path prefixes.

**Every other byte is identical to the freeze**, including `parser_version`, all of
`parse_status_counts`, and all four embedded SHA-256 values
(`raw_index_sha256`, `raw_attempts_sha256`, `experiment_json_sha256`, `parsed_output_sha256`).

### Reconstruction recipe — verify the delta yourself

For each of the 11: take the distributed file, replace `external_run_evidence/<run>` with that
run's `run_dir` from `descriptive_2026-09-21/frozen_grid_manifest.json`, and remove one trailing
newline. The result reproduces **both** the size and the SHA-256 recorded in
`freeze_hashes_after.txt`, for all 11 of 11. `verification_2026-09-21/verify_distributed_subset.py`
performs exactly this check when the unredacted manifest is available, and otherwise verifies the
11 files against their documented distributed hashes in `freeze_hashes_distributed.txt`. It reports
which mode it ran in, and both modes fail on anything unexplained.

## What this does and does not mean

`run_dir` is a provenance path. It is not an input to any computation. No experimental value, no
metric, no test statistic and no reported result differs between the frozen package and the
distributed one.

Verifying this repository against `freeze_hashes_after.txt` therefore yields, by design:

| bucket | count |
|---|---|
| exact match | 9 |
| documented `run_dir` sanitisation | 11 |
| intentionally not distributed (11 parsed intermediates + the private grid manifest) | 12 |
| **unexplained** | **0** |

Any result other than 9 / 11 / 12 / 0 is a genuine finding and should be investigated.

## Files

- `verification_2026-09-21/freeze_hashes_after.txt` — the 2026-09-21 attestation. **Do not modify.**
- `verification_2026-09-21/freeze_hashes_before.txt` — identical to the above. **Do not modify.**
- `verification_2026-09-21/VERIFICATION_METHOD.md` — the verification method as written on
  2026-09-21. Left byte-intact; its hash is recorded in
  `rq1_rq3_reporting_2026-09-21/freeze_check.txt`. Read this note alongside it for scope.
- `verification_2026-09-21/freeze_hashes_distributed.txt` — derived inventory of the 20 distributed
  files as shipped, plus the one entry withheld for privacy.
- `verification_2026-09-21/verify_distributed_subset.py` — the re-runnable partition check.

## Data availability

The public repository supports **full verification and re-derivation** of every reported result:
all 150 per-run and 30 five-run metric values, the 60 permutation p-values, the 60 bootstrap 95%
confidence intervals and every Holm decision can be independently recomputed from the released
replicates, tables and manifests. `rq3_strategy_inference_2026-09-25/code/02_validate.py` does
exactly that, in 32 checks, on a fresh public clone.

**End-to-end re-execution** of the analysis additionally requires the unredacted
`frozen_grid_manifest.json`, which the frozen preregistered scripts `code/00_precheck.py` and
`code/01_run_rq3_strategy_inference.py` read directly. It is withheld from public distribution
because 11 of its `run_dir` values are absolute paths on the collection machines, and it is
available from the authors on request. It differs from the distributed
`frozen_grid_manifest_public.json` in those 11 sanitised `run_dir` strings and in nothing else.
