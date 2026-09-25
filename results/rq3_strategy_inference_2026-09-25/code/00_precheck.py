#!/usr/bin/env python3
"""
RQ3 strategy inference - PRE-CHECK. Runs BEFORE the analysis plan addendum is frozen and
BEFORE any test is executed. Produces no p-value and no strategy comparison statistic.

Purpose (the two conditions the author required be verified and recorded first):
  (1) the three strategy arms are scored on IDENTICAL attributable item sets within each
      dataset, and within each model x run group;
  (2) the five runs are carried as a per-item vector and are never treated as independent
      observations (the data structure makes pooling impossible by construction).

It also records the SHA-256 of every input artifact and reproduces the frozen random draws
so that the declared seed strings can be fixed in the addendum before anything is tested.

READ-ONLY. Writes only into results/rq3_strategy_inference_2026-09-25/.
"""
import collections, hashlib, json, os, platform, random, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
RES = OUT.parent
BASE = RES.parent
DESC = RES / "descriptive_2026-09-21"
INF = RES / "inferential_2026-09-21"

EXPECTED_SHA256 = {   # identical to the frozen inferential analysis
    DESC / "authoritative_records.jsonl": "97c8ca960e0f349dda121515fb45855e9c8787cc8a5cc35a0ce292c1d214a18a",
    DESC / "frozen_grid_manifest.json": "fba6a4617558b64bec61cee18e2a0b63e9457a03c6a3d94cd8e1a1916527dfa8",
    DESC / "per_run_results.csv": "6b3f374a0e76d2c8068c06cc077a2affadd1cd15ac91aab027efeb591efe86ec",
    DESC / "aggregate_results.csv": "4242c3634c8939714eb0b7ff25b446783f1747add91c36040a95bf02f1646768",
}
LABELS = {"dreaddit": [0, 1], "goemotions": ["anxiety", "fear", "sadness", "frustration", "non_distress"]}
N_ITEMS = {"dreaddit": 715, "goemotions": 623}
N_SAFETY = {"dreaddit": 16, "goemotions": 1}
MODELS = ["google/gemma-4-31b-it", "meta-llama/llama-4-scout", "mistralai/mistral-small-2603",
          "microsoft/phi-4", "qwen/qwen3.5-27b"]
STRATS = ["zero-shot", "zero-shot-cot", "one-shot-cot"]
RUNS = [1, 2, 3, 4, 5]
B_REPS, P_PERMS = 4000, 10000
BOOT_SEED, PERM_SEED = "20260921", "20260922"      # reused verbatim from the frozen RQ1/RQ2 analysis
FROZEN_DRAW_SHA = {
    "dreaddit": {"bootstrap_indices_u16le": "5aad14ca8cbb2ccc8c358623ac81504778c3994187db6750346c7fc326edae9d",
                 "permutation_bits_le": "92a9304c0f72f5e114418e5146b6bccb9562afa4685405f04e065499660ddba4"},
    "goemotions": {"bootstrap_indices_u16le": "14bbb591b3f0635b5994a5dd62d53e09a40e15d5e97a1836c5092048db3420c2",
                   "permutation_bits_le": "aaf61859c93f1f566c950a1053c7898414ede99f0c9cc93d653dc4fac77e1af7"},
}
FROZEN_ITEMS_SHA = {"dreaddit": "50042e17fdb030a1444a7ae47c0259909a0191a15c6979fed50576a8a2a4f636",
                    "goemotions": "0fe806ef9e4bbfebf0d6cdac5cc42b026d89aa7f493af0119f6ce6a5ae734c57"}

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def fail(msg):
    sys.exit("PRECHECK FAIL-CLOSED: " + msg)

checks = []
def record(name, ok, detail):
    checks.append({"check": name, "pass": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name + " - " + detail, flush=True)
    if not ok: fail(name)

# ---------------------------------------------------------------- 1. input integrity
inputs = {}
for p, h in EXPECTED_SHA256.items():
    got = sha256(p); inputs[str(p.relative_to(RES))] = got
    record(f"input hash {p.name}", got == h, f"{got[:16]}...")
fm = json.load(open(DESC / "frozen_grid_manifest.json"))
for ds, info in fm["manifests"].items():
    mp = BASE / "manifests" / info["file"]; got = sha256(mp)
    inputs["manifests/" + info["file"]] = got
    record(f"dataset manifest {ds}", got == info["file_sha256"], f"{got[:16]}...")

# ---------------------------------------------------------------- 2. load the frozen grid
records_by_cell = collections.defaultdict(list)
n_lines = 0
with open(DESC / "authoritative_records.jsonl", encoding="utf-8") as f:
    for line in f:
        r = json.loads(line); n_lines += 1; records_by_cell[r["cell_id"]].append(r)
record("grid size", n_lines == 100350 and len(records_by_cell) == 150,
       f"{len(records_by_cell)} cells / {n_lines} records")
record("cell set matches frozen manifest", set(records_by_cell) == set(fm["cells"]), "150/150")

gt = {}
for ds, info in fm["manifests"].items():
    M = json.load(open(BASE / "manifests" / info["file"]))
    gt[ds] = {s: M["ground_truth"][s] for s in M["included_sample_ids"]}
    record(f"{ds} manifest size", len(gt[ds]) == N_ITEMS[ds], str(len(gt[ds])))

# ---------------------------------------------------------------- 3. CONDITION 1: identical item sets
summary = {}
for ds in ("dreaddit", "goemotions"):
    cells = {c: v for c, v in records_by_cell.items() if c.startswith(ds + "|")}
    full = {frozenset(r["sample_id"] for r in v) for v in cells.values()}
    safe = {frozenset(r["sample_id"] for r in v if r["final_outcome_class"] == "SAFETY_INTERCEPT") for v in cells.values()}
    record(f"{ds}: one full item set across all 75 cells", len(full) == 1, f"{len(full)} distinct set(s), size {len(next(iter(full)))}")
    record(f"{ds}: one safety-intercept set across all 75 cells", len(safe) == 1,
           f"{len(safe)} distinct set(s), size {len(next(iter(safe)))}")
    ids, sf = next(iter(full)), next(iter(safe))
    record(f"{ds}: safety count as frozen", len(sf) == N_SAFETY[ds], f"{len(sf)} == {N_SAFETY[ds]}")
    attributable = sorted(ids - sf)
    ish = hashlib.sha256("\n".join(attributable).encode()).hexdigest()
    record(f"{ds}: attributable item list reproduces the frozen inferential item hash",
           ish == FROZEN_ITEMS_SHA[ds], f"{ish[:16]}... n={len(attributable)}")

    # the decisive strategy-specific check: within every model x run group, do the three arms differ?
    groups_differing = 0
    per_group = []
    for m in MODELS:
        for run in RUNS:
            sets = {}
            for s in STRATS:
                v = cells[f"{ds}|{m}|{s}|run{run}"]
                sets[s] = frozenset(r["sample_id"] for r in v if r["final_outcome_class"] != "SAFETY_INTERCEPT")
            distinct = len(set(sets.values()))
            if distinct != 1: groups_differing += 1
            per_group.append({"model": m, "run": run, "distinct_attributable_sets": distinct,
                              "n": len(sets[STRATS[0]])})
    record(f"{ds}: model x run groups where the 3 strategy arms differ in attributable items",
           groups_differing == 0, f"{groups_differing} of {len(per_group)} groups differ")
    record(f"{ds}: every arm has exactly n={len(attributable)} attributable items",
           all(g["n"] == len(attributable) for g in per_group), "25 model x run groups x 3 arms")
    summary[ds] = {"n_full": len(ids), "n_safety": len(sf), "n_attributable": len(attributable),
                   "items_sha256": ish, "model_run_groups_checked": len(per_group),
                   "model_run_groups_with_differing_arms": groups_differing,
                   "safety_sample_ids": sorted(sf)}

# ---------------------------------------------------------------- 4. CONDITION 2: runs are nested, not independent
for ds in ("dreaddit", "goemotions"):
    cells = {c: v for c, v in records_by_cell.items() if c.startswith(ds + "|")}
    sf = set(summary[ds]["safety_sample_ids"])
    items = sorted({r["sample_id"] for r in next(iter(cells.values()))} - sf)
    pos = {s: i for i, s in enumerate(items)}
    n = len(items)
    # array is (item, strategy, run) PER MODEL: the run axis is retained, never flattened into the item axis
    for m in MODELS:
        arr = np.full((n, len(STRATS), len(RUNS)), -1, dtype=np.int64)
        for si, s in enumerate(STRATS):
            for run in RUNS:
                seen = 0
                for r in cells[f"{ds}|{m}|{s}|run{run}"]:
                    if r["sample_id"] in sf: continue
                    seen += 1
                    if r["prediction_valid"]: arr[pos[r["sample_id"]], si, run - 1] = LABELS[ds].index(r["parsed_prediction"])
                if seen != n: fail(f"{ds} {m} {s} run{run}: attributable count {seen} != {n}")
        record(f"{ds} {m}: five-run vector retained per item x strategy",
               arr.shape == (n, 3, 5), f"array shape {arr.shape} (item x strategy x run)")
    record(f"{ds}: independent units for a strategy contrast",
           True, f"n = {n} items, NOT {5 * n} item-run records and NOT 5 runs")

# ---------------------------------------------------------------- 5. reproduce the frozen random draws
def digest_indices(idx):
    h = hashlib.sha256()
    for row in idx: h.update(np.asarray(row, dtype="<u2").tobytes())
    return h.hexdigest()
def digest_bits(bits, n):
    h = hashlib.sha256()
    for b in bits: h.update(b.to_bytes((n + 7) // 8, "little"))
    return h.hexdigest()

draws = {}
for ds in ("dreaddit", "goemotions"):
    n = summary[ds]["n_attributable"]
    rng = random.Random(f"{BOOT_SEED}|{ds}|bootstrap")
    idx = [[rng.randrange(n) for _ in range(n)] for _ in range(B_REPS)]
    rng2 = random.Random(f"{PERM_SEED}|{ds}|permutation")
    bits = [rng2.getrandbits(n) for _ in range(P_PERMS)]
    d = {"bootstrap_indices_u16le": digest_indices(idx), "permutation_bits_le": digest_bits(bits, n)}
    draws[ds] = d
    for k in d:
        record(f"{ds}: {k} reproduces the frozen 2026-09-21 draw", d[k] == FROZEN_DRAW_SHA[ds][k], d[k][:16] + "...")

# ---------------------------------------------------------------- 6. write the record
out = {"created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "python": platform.python_version(), "numpy": np.__version__,
       "purpose": "pre-analysis verification; contains no strategy comparison and no p-value",
       "input_sha256": inputs, "datasets": summary, "draw_sha256": draws,
       "declared_seed_strings": {"bootstrap": {ds: f"{BOOT_SEED}|{ds}|bootstrap" for ds in summary},
                                 "permutation": {ds: f"{PERM_SEED}|{ds}|permutation" for ds in summary}},
       "B": B_REPS, "P": P_PERMS, "checks": checks,
       "all_checks_passed": all(c["pass"] for c in checks), "n_checks": len(checks)}
json.dump(out, open(OUT / "precheck.json", "w"), indent=1)
with open(OUT / "INPUT_HASHES.sha256", "w") as f:
    for k in sorted(inputs): f.write(f"{inputs[k]}  {k}\n")
print(f"\nPRECHECK COMPLETE: {sum(c['pass'] for c in checks)}/{len(checks)} checks passed")
