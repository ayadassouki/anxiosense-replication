# inferential_2026-09-21

Inferential statistics for RQ1 (model comparison) and RQ2 (configuration vs majority baseline) on the frozen AnxioSense publication grid. RQ3 is not analysed inferentially.

This directory is derived output only. Nothing outside it was written.

## Read first

1. `STATISTICAL_ANALYSIS_PLAN.md`: the design, written before any test was run, and the approved decisions D1–D4 (section F).
2. `REPORT.md`: tables and findings, split into Measured and Interpretation, ending with "What the inferential results establish and do not establish".
3. `verification/VERIFICATION.md`: the independent verification (PASSED, 0 discrepancies).

## Files

| Path | Content |
|---|---|
| `source_hashes.txt` | sha256 of every input, recorded before analysis |
| `code/run_inferential.py` | Main analysis: integrity checks, pairing, bootstrap, permutation, McNemar, Holm. Needs numpy. |
| `code/make_tables_md.py` | Markdown tables, `summary_counts.json`, Monte Carlo sensitivity |
| `code/build_report.py` | Renders `REPORT.md` from `REPORT_template.md` and checks every quoted number |
| `verification/verify_inferential.py` | Independent re-implementation, stdlib only |
| `tables/*.csv` | Machine-readable results at full precision (`repr` floats) |
| `tables/*.md` | Rounded presentation tables |
| `replicates/bootstrap_<ds>.csv.gz` | All 4,000 replicate values per configuration, plus the constant predictor |
| `replicates/permutation_<ds>.csv.gz` | All 10,000 permutation statistics per comparison |
| `analysis_manifest.json` | Seeds, B, P, draw digests, input/output hashes, family sizes, software versions |

## Rerun (from the repository root, on a machine with the repo)

```bash
cd ~/anxiosense/evaluation/publication_experiments/results/inferential_2026-09-21
python3 -c "import numpy; print(numpy.__version__)" || python3 -m pip install numpy
python3 code/run_inferential.py        # about 10 s; aborts on any integrity failure
python3 code/make_tables_md.py
python3 code/build_report.py
```

## Independent verification

```bash
cd ~/anxiosense/evaluation/publication_experiments/results/inferential_2026-09-21
python3 verification/verify_inferential.py   # about 3 min; exit code 0 = passed, 1 = discrepancy
```

## Expected output hashes (deterministic; a rerun must reproduce these byte-for-byte)

The files are written with fixed seeds, and the gzip files with mtime = 0. Only `analysis_manifest.json` changes between runs, because it records a timestamp.

```
6db90bc76ae23008e0d9a64888b6470dcdf105f562d340c46c82e37bd809b9ac  tables/configuration_level_ci.csv
a10aeb208781b759b8f20ae0cc69db4e6446c7aa734dd5030c65f0e8cbd896b0  tables/rq1_model_pairs_conditional_accuracy_ci.csv
849f219b0e3e3afe0ec6faa429f017b84b0d76b7d3977d5f85f4055fb2ce379a  tables/rq1_model_pairs_mcnemar.csv
9c32afaf2626f77430d3ce8dae006571fcab89b34dddb1d76de8ae49deb8c1a5  tables/rq1_model_pairs_primary.csv
2f2b96aeebc52ff80eb12bbb1e7821b9d3841b8c74526a68d35a909672ce2206  tables/rq2_configuration_vs_baseline.csv
6ae887056f1bd9e593cbb783a23565d9dcb0d1ba88b9429605f5f5c73ce79550  replicates/bootstrap_dreaddit.csv.gz
e8e585dcf3af648f95170b84a03924fd1dff0c81ddc616e1bb86d3aabc30cc1c  replicates/bootstrap_goemotions.csv.gz
9902a275e00e162f93b21d517c3587fe479a25ea67f35476a7f3463becf71e5d  replicates/permutation_dreaddit.csv.gz
62947e3e01cd92b18583f86eea861b92788dc4d9aa1758f13d9a576026945b27  replicates/permutation_goemotions.csv.gz
```

Check them with:

```bash
shasum -a 256 tables/*.csv replicates/*.gz
```

The numbers were produced with Python 3.10.12 and numpy 2.2.6. All counts are exact integers, so other numpy versions should give identical bytes. If a hash differs, run the verification script to see whether the difference is substantive.
