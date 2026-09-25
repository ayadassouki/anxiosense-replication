#!/usr/bin/env python3
"""
RQ3 strategy inference - EXECUTION. Runs the design frozen in RQ3_SAP_ADDENDUM.md.

POST-HOC / EXPLORATORY. The estimation procedure is the one frozen on 2026-09-21 for RQ1/RQ2
(STATISTICAL_ANALYSIS_PLAN.md), applied unchanged to strategy pairs. Only the pair list and the
Holm families differ from inferential_2026-09-21/code/run_inferential.py.

UNIT          the benchmark item, carrying all 5 runs. n = 699 (dreaddit) / 622 (goemotions).
PAIRING       identical attributable item sets in all three strategy arms (verified in 00_precheck.py).
RUNS          nested inside the item; never paired across arms; never resampled; never independent.
PRIMARY       effective accuracy and macro-F1, both on the attributable denominator.
              Model-invalid outputs count as INCORRECT. The analysis is NOT conditioned on validity.
PERMUTATION   paired item-level swap of the WHOLE five-run vector, P = 10,000,
              p = (1 + #{|T*| >= |T_obs|}) / (1 + P). Macro-F1 is RECOMPUTED after each swap.
BOOTSTRAP     item-cluster, B = 4,000, one shared index vector per dataset, 95% percentile CI.
HOLM          one family per dataset over the 30 primary comparisons (5 models x 3 pairs x 2 metrics).
              McNemar secondary in its own family of 15 per dataset.
SEEDS         reused verbatim from the frozen analysis: "20260921|<ds>|bootstrap",
              "20260922|<ds>|permutation" (see addendum section 3.2).
READ-ONLY outside results/rq3_strategy_inference_2026-09-25/.
"""
import csv, gzip, hashlib, io, json, math, platform, random, sys, time, collections
from fractions import Fraction
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
RES = OUT.parent
BASE = RES.parent
DESC = RES / "descriptive_2026-09-21"
INF = RES / "inferential_2026-09-21"

EXPECTED_SHA256 = {
    DESC / "authoritative_records.jsonl": "97c8ca960e0f349dda121515fb45855e9c8787cc8a5cc35a0ce292c1d214a18a",
    DESC / "frozen_grid_manifest.json": "fba6a4617558b64bec61cee18e2a0b63e9457a03c6a3d94cd8e1a1916527dfa8",
    DESC / "per_run_results.csv": "6b3f374a0e76d2c8068c06cc077a2affadd1cd15ac91aab027efeb591efe86ec",
    DESC / "aggregate_results.csv": "4242c3634c8939714eb0b7ff25b446783f1747add91c36040a95bf02f1646768",
}
B_REPS, P_PERMS, ALPHA = 4000, 10000, 0.05
BOOT_SEED, PERM_SEED = "20260921", "20260922"
LABELS = {"dreaddit": [0, 1], "goemotions": ["anxiety", "fear", "sadness", "frustration", "non_distress"]}
N_ITEMS = {"dreaddit": 715, "goemotions": 623}
N_SAFETY = {"dreaddit": 16, "goemotions": 1}
MODELS = ["google/gemma-4-31b-it", "meta-llama/llama-4-scout", "mistralai/mistral-small-2603",
          "microsoft/phi-4", "qwen/qwen3.5-27b"]
SHORT = {"google/gemma-4-31b-it": "Gemma 4 31B", "meta-llama/llama-4-scout": "Llama 4 Scout",
         "mistralai/mistral-small-2603": "Mistral Small 4", "microsoft/phi-4": "Phi-4", "qwen/qwen3.5-27b": "Qwen3.5 27B"}
STRATS = ["zero-shot", "zero-shot-cot", "one-shot-cot"]
DISP = {"zero-shot": "zero-shot", "zero-shot-cot": "zero-shot-CoT", "one-shot-cot": "one-shot-CoT"}
CONFIGS = [(m, s) for m in MODELS for s in STRATS]
# the three declared contrasts, in the declared order; A is the earlier strategy in STRATS order
PAIRS = [("zero-shot", "zero-shot-cot"), ("zero-shot", "one-shot-cot"), ("zero-shot-cot", "one-shot-cot")]
RUNS = [1, 2, 3, 4, 5]
GEMMA_REPLACED = "dreaddit|google/gemma-4-31b-it|one-shot-cot|run5"

def gz_text_writer(path):
    return io.TextIOWrapper(gzip.GzipFile(filename="", mode="wb", fileobj=open(path, "wb"), mtime=0),
                            newline="", encoding="utf-8")

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def fail(msg):
    sys.exit("FAIL-CLOSED: " + msg)

# ================================================================ 1. integrity checks
for p, h in EXPECTED_SHA256.items():
    if sha256(p) != h: fail(f"sha256 mismatch for {p}")
fm = json.load(open(DESC / "frozen_grid_manifest.json"))
for ds, info in fm["manifests"].items():
    if sha256(BASE / "manifests" / info["file"]) != info["file_sha256"]: fail(f"dataset manifest hash {ds}")

records = collections.defaultdict(list)
n_lines = 0
with open(DESC / "authoritative_records.jsonl", encoding="utf-8") as f:
    for line in f:
        r = json.loads(line); n_lines += 1; records[r["cell_id"]].append(r)
if n_lines != 100350 or len(records) != 150: fail(f"expected 150 cells / 100,350 records, got {len(records)} / {n_lines}")
if set(records) != set(fm["cells"]): fail("cell set differs from frozen manifest")

gt_manifest = {}
for ds, info in fm["manifests"].items():
    M = json.load(open(BASE / "manifests" / info["file"]))
    gt_manifest[ds] = {s: M["ground_truth"][s] for s in M["included_sample_ids"]}
    if len(gt_manifest[ds]) != N_ITEMS[ds]: fail(f"{ds} manifest size")

src_rule = {}
for cid, recs in records.items():
    ds, model, strat, run = cid.split("|")
    fc = fm["cells"][cid]
    if len(recs) != N_ITEMS[ds] or fc["n"] != N_ITEMS[ds]: fail(f"{cid}: n")
    key = "\n".join(sorted(f'{r["sample_id"]}|{r["terminal_attempt_uuid"]}' for r in recs))
    if hashlib.sha256(key.encode()).hexdigest() != fc["records_sha256"]: fail(f"{cid}: records_sha256")
    srcs = {r["source_run"] for r in recs}
    if len(srcs) != 1: fail(f"{cid}: mixed source runs")
    src_rule[cid] = srcs.pop()
    for r in recs:
        if r["cell_id"] != cid or r["dataset"] != ds or r["model"] != model or r["strategy"] != strat: fail(f"{cid}: identity")
        if r["ground_truth"] != gt_manifest[ds].get(r["sample_id"]): fail(f"{cid} {r['sample_id']}: ground truth")
        o = (r["final_outcome_class"], r["failure_class"], r["prediction_valid"])
        if o == ("OK", None, True):
            if r["parsed_prediction"] not in LABELS[ds]: fail(f"{cid}: valid prediction outside label set")
        elif o not in {("OK", "MODEL_BEHAVIOUR", False), ("SAFETY_INTERCEPT", "SAFETY_INTERCEPT", False)}:
            fail(f"{cid}: unexpected outcome {o}")
for cid, src in src_rule.items():
    if cid.startswith("dreaddit|google/gemma-4-31b-it|"):
        want = "pub_013_dreaddit_gemma_coreweave_osc_run5" if cid == GEMMA_REPLACED else "pub_011_dreaddit_gemma_coreweave"
        if src != want: fail(f"Gemma composition: {cid} from {src}")
    if src == "pub_013_dreaddit_gemma_coreweave_osc_run5" and cid != GEMMA_REPLACED: fail("pub_013 used outside replacement cell")

# ================================================================ 2. item x config x run arrays
DATA = {}
for ds in ("dreaddit", "goemotions"):
    cells = {c: records[c] for c in records if c.startswith(ds + "|")}
    id_sets = {frozenset(r["sample_id"] for r in v) for v in cells.values()}
    safe_sets = {frozenset(r["sample_id"] for r in v if r["final_outcome_class"] == "SAFETY_INTERCEPT") for v in cells.values()}
    if len(id_sets) != 1 or len(safe_sets) != 1: fail(f"{ds}: items do not pair across cells")
    ids, safe = next(iter(id_sets)), next(iter(safe_sets))
    if ids != set(gt_manifest[ds]) or len(safe) != N_SAFETY[ds]: fail(f"{ds}: item/safety set")
    # PRE-CONDITION re-assert: the three strategy arms share one attributable set in every model x run group
    for m in MODELS:
        for run in RUNS:
            arms = {frozenset(r["sample_id"] for r in cells[f"{ds}|{m}|{s}|run{run}"]
                              if r["final_outcome_class"] != "SAFETY_INTERCEPT") for s in STRATS}
            if len(arms) != 1: fail(f"{ds} {m} run{run}: strategy arms differ in attributable items")
    items = sorted(ids - safe)
    L = LABELS[ds]; K = len(L); n = len(items); pos = {s: i for i, s in enumerate(items)}
    gt = np.array([L.index(gt_manifest[ds][s]) for s in items])
    pred = np.full((n, len(CONFIGS), 5), -1, dtype=np.int64)
    for ci, (m, s) in enumerate(CONFIGS):
        for run in RUNS:
            recs = cells[f"{ds}|{m}|{s}|run{run}"]
            seen = 0
            for r in recs:
                if r["sample_id"] in safe: continue
                seen += 1
                if r["prediction_valid"]: pred[pos[r["sample_id"]], ci, run - 1] = L.index(r["parsed_prediction"])
            if seen != n: fail(f"{ds} {m} {s} run{run}: attributable count")
    valid = pred >= 0
    correct = valid & (pred == gt[:, None, None])
    feats = [correct, valid]
    for k in range(K): feats.append(valid & (pred == k) & (gt[:, None, None] == k))   # tp_k
    for k in range(K): feats.append(valid & (pred == k) & (gt[:, None, None] != k))   # fp_k
    for k in range(K): feats.append(valid & (pred != k) & (gt[:, None, None] == k))   # fn_k
    F = np.stack(feats, axis=-1).astype(np.float64)
    maj = collections.Counter(gt_manifest[ds].values()).most_common(1)[0][0]
    DATA[ds] = {"items": items, "n": n, "K": K, "gt": gt, "pred": pred, "F": F, "correct": correct,
                "maj_index": L.index(maj), "maj_label": maj, "safe": sorted(safe)}

# ================================================================ 3. metric functions (frozen semantics)
def metrics_runs(C, n, K):
    """Per-RUN metrics; the run axis is retained. C: (..., 5, 2+3K)."""
    corr, val = C[..., 0], C[..., 1]
    tp, fp, fn = C[..., 2:2 + K], C[..., 2 + K:2 + 2 * K], C[..., 2 + 2 * K:2 + 3 * K]
    with np.errstate(divide="ignore", invalid="ignore"):
        f1 = np.where(tp > 0, 2 * tp / (2 * tp + fp + fn), 0.0)
        acc_cond = np.where(val > 0, corr / val, 0.0)
    return {"acc_eff": corr / n, "acc_cond": acc_cond, "macro_f1": f1.mean(axis=-1), "evaluability": val / n}

def metrics_from_counts(C, n, K):
    """Five-run values = mean over the run axis. Identical to the frozen function for the three frozen keys."""
    return {k: v.mean(axis=-1) for k, v in metrics_runs(C, n, K).items()}

def sample_sd(xs):
    xs = list(map(float, xs))
    if len(xs) < 2: return 0.0
    m = sum(xs) / len(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5

def pct_ci(x):
    xs = sorted(x); out = []
    for q in (0.025, 0.975):
        h = (len(xs) - 1) * q; lo = math.floor(h)
        out.append(float(xs[lo] + (h - lo) * (xs[min(lo + 1, len(xs) - 1)] - xs[lo])))
    return out

def mcnemar_exact(b, c):
    n = b + c
    if n == 0: return 1.0
    tail = Fraction(sum(math.comb(n, k) for k in range(min(b, c) + 1)), 2 ** n)
    return float(min(Fraction(1), 2 * tail))

def holm(pvals):
    m = len(pvals); order = sorted(range(m), key=lambda i: pvals[i]); adj = [0.0] * m; running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvals[i])); adj[i] = running
    return adj

# ================================================================ 4. observed values + frozen cross-check
frozen_run = {("%s|%s|%s|run%s" % (r["dataset"], r["model"], r["strategy"], r["run"])): r
              for r in csv.DictReader(open(DESC / "per_run_results.csv"))}
frozen_agg = {(r["dataset"], r["model"], r["strategy"]): r for r in csv.DictReader(open(DESC / "aggregate_results.csv"))}
OBS, PERRUN = {}, {}
maxdiff = 0.0
for ds, D in DATA.items():
    C = D["F"].sum(axis=0)                                   # (15, 5, feat)
    OBS[ds] = metrics_from_counts(C, D["n"], D["K"])
    PERRUN[ds] = metrics_runs(C, D["n"], D["K"])             # (15, 5)
    corr, val = C[..., 0], C[..., 1]
    for ci, (m, s) in enumerate(CONFIGS):
        for run in RUNS:
            fr = frozen_run[f"{ds}|{m}|{s}|run{run}"]
            if int(fr["correct"]) != corr[ci, run - 1] or int(fr["N_valid"]) != val[ci, run - 1]:
                fail(f"count mismatch {ds} {m} {s} {run}")
            for key, col in (("acc_eff", "accuracy_effective"), ("acc_cond", "accuracy_conditional"),
                             ("macro_f1", "macro_f1"), ("evaluability", "evaluability")):
                d = abs(float(PERRUN[ds][key][ci, run - 1]) - float(fr[col])); maxdiff = max(maxdiff, d)
                if d > 1e-12: fail(f"per-run {key} differs from frozen {ds} {m} {s} run{run}: {d}")
        fa = frozen_agg[(ds, m, s)]
        for key, col in (("acc_eff", "accuracy_effective_mean"), ("acc_cond", "accuracy_conditional_mean"),
                         ("macro_f1", "macro_f1_mean"), ("evaluability", "evaluability_mean")):
            d = abs(float(OBS[ds][key][ci]) - float(fa[col])); maxdiff = max(maxdiff, d)
            if d > 1e-12: fail(f"five-run {key} differs from frozen {ds} {m} {s}: {d}")

# ================================================================ 5. draws
def bootstrap_indices(ds, n):
    rng = random.Random(f"{BOOT_SEED}|{ds}|bootstrap")
    return [[rng.randrange(n) for _ in range(n)] for _ in range(B_REPS)]
def permutation_bits(ds, n):
    rng = random.Random(f"{PERM_SEED}|{ds}|permutation")
    return [rng.getrandbits(n) for _ in range(P_PERMS)]
def digest_indices(idx):
    h = hashlib.sha256()
    for row in idx: h.update(np.asarray(row, dtype="<u2").tobytes())
    return h.hexdigest()
def digest_bits(bits, n):
    h = hashlib.sha256()
    for b in bits: h.update(b.to_bytes((n + 7) // 8, "little"))
    return h.hexdigest()

manifest = {"created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "analysis": "RQ3 prompting-strategy contrasts (post-hoc / exploratory)",
            "plan": "RQ3_SAP_ADDENDUM.md", "procedure_frozen": "2026-09-21 STATISTICAL_ANALYSIS_PLAN.md (unchanged)",
            "python": platform.python_version(), "numpy": np.__version__,
            "B": B_REPS, "P": P_PERMS, "alpha": ALPHA,
            "bootstrap_seed_strings": {}, "permutation_seed_strings": {}, "draw_sha256": {},
            "input_sha256": {str(p.relative_to(RES)): h for p, h in EXPECTED_SHA256.items()},
            "max_abs_diff_observed_vs_frozen": maxdiff, "families": {}, "items": {}, "notes": [],
            "contrasts": [f"{DISP[a]} vs {DISP[b]}" for a, b in PAIRS]}
for p in sorted(HERE.glob("*.py")): manifest.setdefault("code_sha256", {})[p.name] = sha256(p)

rows_pri, rows_mc, rows_cond, rows_cfg = [], [], [], []
for ds, D in DATA.items():
    n, K, F = D["n"], D["K"], D["F"]
    t0 = time.time()
    idx = bootstrap_indices(ds, n); bits = permutation_bits(ds, n)
    manifest["bootstrap_seed_strings"][ds] = f"{BOOT_SEED}|{ds}|bootstrap"
    manifest["permutation_seed_strings"][ds] = f"{PERM_SEED}|{ds}|permutation"
    manifest["draw_sha256"][ds] = {"bootstrap_indices_u16le": digest_indices(idx), "permutation_bits_le": digest_bits(bits, n)}
    manifest["items"][ds] = {"n_attributable": n, "items_sha256": hashlib.sha256("\n".join(D["items"]).encode()).hexdigest(),
                             "safety_excluded": D["safe"], "majority_class": D["maj_label"]}
    W = np.zeros((B_REPS, n))
    for b, row in enumerate(idx): np.add.at(W[b], row, 1)
    assert (W.sum(axis=1) == n).all()
    S = np.array([[(bb >> i) & 1 for i in range(n)] for bb in bits], dtype=np.float64)

    Fflat = F.reshape(n, -1)
    Cb = (W @ Fflat).reshape(B_REPS, len(CONFIGS), 5, -1)
    REP = metrics_from_counts(Cb, n, K)
    no_anx = int((W[:, D["gt"] == 0].sum(axis=1) == 0).sum()) if ds == "goemotions" else None
    if ds == "goemotions":
        manifest["notes"].append(f"goemotions: {no_anx} of {B_REPS} bootstrap replicates contain no 'anxiety' item; "
                                 "per MetricPolicy 1.0.0 its recall/F1 = 0 in those replicates (applied verbatim).")
        manifest["goemotions_bootstrap_replicates_without_anxiety_item"] = no_anx

    with gz_text_writer(OUT / "replicates" / f"bootstrap_{ds}.csv.gz") as f:
        w = csv.writer(f); hdr = ["replicate"]
        for (m, s) in CONFIGS:
            hdr += [f"{SHORT[m]}|{s}|{k}" for k in ("acc_eff", "acc_cond", "macro_f1", "evaluability")]
        w.writerow(hdr)
        for b in range(B_REPS):
            row = [b]
            for ci in range(len(CONFIGS)):
                row += [repr(float(REP[k][b, ci])) for k in ("acc_eff", "acc_cond", "macro_f1", "evaluability")]
            w.writerow(row)

    for ci, (m, s) in enumerate(CONFIGS):
        r = {"dataset": ds, "model": SHORT[m], "strategy": s, "n_items": n}
        for k in ("acc_eff", "acc_cond", "macro_f1"):
            lo, hi = pct_ci(REP[k][:, ci]); r[k] = float(OBS[ds][k][ci]); r[k + "_ci_low"] = lo; r[k + "_ci_high"] = hi
        rows_cfg.append(r)

    corr_runs = D["correct"].sum(axis=2).astype(np.int64)
    def perm_pair(ci, cj):
        """Swap test: for swapped items, A receives B's five run outcomes and vice versa."""
        dF = (F[:, cj] - F[:, ci]).reshape(n, -1)
        base_A = F[:, ci].sum(axis=0); base_B = F[:, cj].sum(axis=0)
        shift = (S @ dF).reshape(P_PERMS, 5, -1)
        mA = metrics_from_counts(base_A[None] + shift, n, K); mB = metrics_from_counts(base_B[None] - shift, n, K)
        d_int = corr_runs[:, ci] - corr_runs[:, cj]
        T_obs_int = int(d_int.sum())
        T_perm_int = (d_int[None, :] * (1 - 2 * S)).sum(axis=1).astype(np.int64)
        p_acc = (1 + int((np.abs(T_perm_int) >= abs(T_obs_int)).sum())) / (1 + P_PERMS)
        T_obs_f1 = float(OBS[ds]["macro_f1"][ci] - OBS[ds]["macro_f1"][cj])
        T_perm_f1 = mA["macro_f1"] - mB["macro_f1"]
        p_f1 = (1 + int((np.abs(T_perm_f1) >= abs(T_obs_f1) - 1e-12).sum())) / (1 + P_PERMS)
        assert np.allclose(T_perm_int / (5 * n), mA["acc_eff"] - mB["acc_eff"], atol=1e-12)
        return p_acc, p_f1, T_perm_int, T_perm_f1

    perm_store = {}
    fam_pri, fam_mc = [], []
    for m in MODELS:
        for (sa, sb) in PAIRS:
            ci, cj = CONFIGS.index((m, sa)), CONFIGS.index((m, sb))
            p_acc, p_f1, Tpi, Tpf = perm_pair(ci, cj)
            tag = f"{SHORT[m]} | {DISP[sa]} vs {DISP[sb]}"
            perm_store[tag + " | acc_eff (int)"] = Tpi; perm_store[tag + " | macro_f1"] = Tpf
            inv_A = int(5 * n - D["F"][:, ci, :, 1].sum()); inv_B = int(5 * n - D["F"][:, cj, :, 1].sum())
            ev_A, ev_B = float(OBS[ds]["evaluability"][ci]), float(OBS[ds]["evaluability"][cj])
            ev_lo, ev_hi = pct_ci(REP["evaluability"][:, ci] - REP["evaluability"][:, cj])
            for metric, p in (("acc_eff", p_acc), ("macro_f1", p_f1)):
                vA, vB = float(OBS[ds][metric][ci]), float(OBS[ds][metric][cj])
                sdA = sample_sd(PERRUN[ds][metric][ci]); sdB = sample_sd(PERRUN[ds][metric][cj])
                lo, hi = pct_ci(REP[metric][:, ci] - REP[metric][:, cj])
                rows_pri.append({
                    "dataset": ds, "family": f"RQ3-primary-{ds}", "metric": metric, "model": SHORT[m],
                    "strategy_A": DISP[sa], "strategy_B": DISP[sb], "n_items": n,
                    "A_mean": vA, "A_sd": sdA, "B_mean": vB, "B_sd": sdB,
                    "diff_A_minus_B": vA - vB, "ci_low": lo, "ci_high": hi,
                    "p_perm": p, "direction": ("A higher" if vA > vB else "B higher" if vB > vA else "equal"),
                    "A_invalid_outputs_5runs": inv_A, "B_invalid_outputs_5runs": inv_B,
                    "A_evaluability": ev_A, "B_evaluability": ev_B,
                    "diff_evaluability_A_minus_B": ev_A - ev_B,
                    "diff_evaluability_ci_low": ev_lo, "diff_evaluability_ci_high": ev_hi,
                })
                fam_pri.append(rows_pri[-1])
            # conditional accuracy: descriptive CI only, no test
            vA, vB = float(OBS[ds]["acc_cond"][ci]), float(OBS[ds]["acc_cond"][cj])
            lo, hi = pct_ci(REP["acc_cond"][:, ci] - REP["acc_cond"][:, cj])
            rows_cond.append({"dataset": ds, "model": SHORT[m], "strategy_A": DISP[sa], "strategy_B": DISP[sb],
                              "A_acc_cond": vA, "A_sd": sample_sd(PERRUN[ds]["acc_cond"][ci]),
                              "B_acc_cond": vB, "B_sd": sample_sd(PERRUN[ds]["acc_cond"][cj]),
                              "diff_A_minus_B": vA - vB, "ci_low": lo, "ci_high": hi,
                              "A_valid_run_outcomes": int(D["F"][:, ci, :, 1].sum()),
                              "B_valid_run_outcomes": int(D["F"][:, cj, :, 1].sum()),
                              "note": "conditional on each configuration's own valid predictions; denominators differ; NO TEST"})
            # secondary: exact McNemar on majority-vote effective correctness (>= 3 of 5)
            mvA, mvB = corr_runs[:, ci] >= 3, corr_runs[:, cj] >= 3
            bb, cc = int((mvA & ~mvB).sum()), int((~mvA & mvB).sum())
            rows_mc.append({"dataset": ds, "family": f"RQ3-mcnemar-{ds}", "model": SHORT[m],
                            "strategy_A": DISP[sa], "strategy_B": DISP[sb], "n_items": n,
                            "A_majority_correct": int(mvA.sum()), "B_majority_correct": int(mvB.sum()),
                            "b_A_correct_B_wrong": bb, "c_A_wrong_B_correct": cc, "discordant": bb + cc,
                            "diff_majority_acc": (int(mvA.sum()) - int(mvB.sum())) / n, "p_exact": mcnemar_exact(bb, cc)})
            fam_mc.append(rows_mc[-1])
    for fam, key in ((fam_pri, "p_perm"), (fam_mc, "p_exact")):
        adj = holm([r[key] for r in fam])
        for r, a in zip(fam, adj): r["p_holm"] = a; r["holm_significant_0.05"] = a <= ALPHA; r["family_size"] = len(fam)
    manifest["families"][f"RQ3-primary-{ds}"] = len(fam_pri); manifest["families"][f"RQ3-mcnemar-{ds}"] = len(fam_mc)

    with gz_text_writer(OUT / "replicates" / f"permutation_{ds}.csv.gz") as f:
        w = csv.writer(f); keys = list(perm_store); w.writerow(["permutation"] + keys)
        for p_ in range(P_PERMS):
            w.writerow([p_] + [(int(perm_store[k][p_]) if k.endswith("(int)") else repr(float(perm_store[k][p_]))) for k in keys])
    print(f"{ds}: done in {time.time() - t0:.1f}s", flush=True)

# ================================================================ 6. write tables
def write_csv(name, rows):
    with open(OUT / "tables" / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader()
        for r in rows:
            for k, v in r.items():
                if type(v).__module__ == "numpy": fail(f"numpy scalar leaked into table {name}:{k}")
            w.writerow({k: (repr(v) if isinstance(v, float) else v) for k, v in r.items()})

write_csv("rq3_strategy_pairs_primary.csv", rows_pri)
write_csv("rq3_strategy_pairs_mcnemar.csv", rows_mc)
write_csv("rq3_strategy_pairs_conditional_accuracy_ci.csv", rows_cond)
write_csv("rq3_configuration_level_ci.csv", rows_cfg)

def f4(x): return f"{x:.4f}"
def sgn(x): return ("+" if x >= 0 else "−") + f"{abs(x):.4f}"
for ds in ("dreaddit", "goemotions"):
    for metric, mlabel in (("acc_eff", "Effective accuracy"), ("macro_f1", "Macro-F1")):
        rs = [r for r in rows_pri if r["dataset"] == ds and r["metric"] == metric]
        lines = [f"### {mlabel} — strategy contrasts, {ds} (n = {rs[0]['n_items']} items)", "",
                 "| Model | Contrast (A vs B) | A mean ± SD | B mean ± SD | Diff (A−B) | 95% CI | p (unadj.) | p (Holm) | Sig. |",
                 "|---|---|---|---|---|---|---|---|---|"]
        for r in rs:
            lines.append("| %s | %s vs %s | %s ± %s | %s ± %s | %s | [%s, %s] | %.4f | %.4f | %s |" % (
                r["model"], r["strategy_A"], r["strategy_B"], f4(r["A_mean"]), f4(r["A_sd"]),
                f4(r["B_mean"]), f4(r["B_sd"]), sgn(r["diff_A_minus_B"]), sgn(r["ci_low"]), sgn(r["ci_high"]),
                r["p_perm"], r["p_holm"], "**yes**" if r["holm_significant_0.05"] else "no"))
        open(OUT / "tables" / f"rq3_{ds}_{metric}.md", "w").write("\n".join(lines) + "\n")

manifest["output_sha256"] = {p.name: sha256(p) for p in sorted((OUT / "tables").glob("*"))}
manifest["output_sha256"].update({p.name: sha256(p) for p in sorted((OUT / "replicates").glob("*.gz"))})
manifest["counts"] = {"primary_rows": len(rows_pri), "mcnemar_rows": len(rows_mc),
                      "conditional_rows": len(rows_cond), "configuration_rows": len(rows_cfg)}
json.dump(manifest, open(OUT / "analysis_manifest.json", "w"), indent=1)
for ds in ("dreaddit", "goemotions"):
    pr = [r for r in rows_pri if r["dataset"] == ds]; mc = [r for r in rows_mc if r["dataset"] == ds]
    print(f"{ds}: primary {sum(r['holm_significant_0.05'] for r in pr)}/{len(pr)} Holm-significant"
          f" | mcnemar {sum(r['holm_significant_0.05'] for r in mc)}/{len(mc)}")
print("max |observed - frozen| =", maxdiff)
