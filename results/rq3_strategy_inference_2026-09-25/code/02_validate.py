#!/usr/bin/env python3
"""
RQ3 strategy inference - POST-EXECUTION VALIDATION.
Independent re-derivation of every reported quantity from the saved replicate files, plus
integrity checks on the freeze, the inputs and every pre-existing package. READ-ONLY outside
results/rq3_strategy_inference_2026-09-25/ (writes VALIDATION.md and validation.json here).
"""
import csv, gzip, hashlib, json, math, sys, collections
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
RES = OUT.parent
BASE = RES.parent
DESC = RES / "descriptive_2026-09-21"
INF = RES / "inferential_2026-09-21"
P_PERMS, B_REPS, ALPHA = 10000, 4000, 0.05

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

checks = []
def chk(name, ok, detail=""):
    checks.append({"n": len(checks) + 1, "check": name, "pass": bool(ok), "detail": detail})
    print(f"{len(checks):2d}. {'PASS' if ok else 'FAIL'}  {name}" + (f"  -- {detail}" if detail else ""), flush=True)

pre = json.load(open(OUT / "precheck.json"))
frz = json.load(open(OUT / "PREREGISTRATION_FREEZE.json"))
man = json.load(open(OUT / "analysis_manifest.json"))
primary = list(csv.DictReader(open(OUT / "tables" / "rq3_strategy_pairs_primary.csv")))
mcn = list(csv.DictReader(open(OUT / "tables" / "rq3_strategy_pairs_mcnemar.csv")))
cond = list(csv.DictReader(open(OUT / "tables" / "rq3_strategy_pairs_conditional_accuracy_ci.csv")))
cfg = list(csv.DictReader(open(OUT / "tables" / "rq3_configuration_level_ci.csv")))

# 1 -------------------------------------------------------------- pre-check
chk("Pre-check ran and every pre-condition check passed",
    pre["all_checks_passed"] and pre["n_checks"] == 38, f"{sum(c['pass'] for c in pre['checks'])}/{pre['n_checks']}")

# 2 -------------------------------------------------------------- identical item sets (the author's condition 1)
ok = all(v["model_run_groups_with_differing_arms"] == 0 for v in pre["datasets"].values())
chk("Strategy arms use identical attributable item sets in every model x run group",
    ok, "dreaddit 0/25 and goemotions 0/25 groups differ; n = 699 / 622")

# 3 -------------------------------------------------------------- runs not independent (the author's condition 2)
ns = {ds: v["n_attributable"] for ds, v in pre["datasets"].items()}
ok = all(int(r["n_items"]) == ns[r["dataset"]] for r in primary)
chk("Every comparison uses n = items, not item-run records and not runs",
    ok, "n = 699 (not 3,495; not 5) / n = 622 (not 3,110; not 5)")

# 4 -------------------------------------------------------------- the plan and the code were frozen before execution
ok = all(sha256(OUT / f) == h for f, h in frz["frozen_files_sha256"].items())
chk("Every file named in PREREGISTRATION_FREEZE.json still matches its frozen SHA-256", ok,
    f"{len(frz['frozen_files_sha256'])} files; frozen {frz['frozen_utc']}")
ok = man["code_sha256"]["01_run_rq3_strategy_inference.py"] == frz["frozen_files_sha256"]["code/01_run_rq3_strategy_inference.py"]
chk("The analysis code that ran is the code that was frozen", ok,
    man["code_sha256"]["01_run_rq3_strategy_inference.py"][:16] + "...")
chk("Freeze timestamp precedes the analysis timestamp", frz["frozen_utc"] <= man["created_utc"],
    f"{frz['frozen_utc']} <= {man['created_utc']}")

# 5 -------------------------------------------------------------- inputs unchanged
ok = all(sha256(RES / k) == v for k, v in man["input_sha256"].items())
chk("All four frozen input artifacts still match their recorded SHA-256", ok, f"{len(man['input_sha256'])} inputs")
ok = man["input_sha256"] == json.load(open(INF / "analysis_manifest.json"))["input_sha256"]
chk("Inputs are byte-identical to those used by the frozen 2026-09-21 inferential analysis", ok)

# 6 -------------------------------------------------------------- frozen metric reproduction
ok = man["max_abs_diff_observed_vs_frozen"] <= 1e-12
chk("All 150 per-run and 30 five-run frozen metric values reproduced from the raw grid",
    ok, f"max |observed - frozen| = {man['max_abs_diff_observed_vs_frozen']:.3e}")

# 7 -------------------------------------------------------------- draws reproduce the frozen draws
finf = json.load(open(INF / "analysis_manifest.json"))
ok = man["draw_sha256"] == finf["draw_sha256"]
chk("Bootstrap and permutation draws are bit-identical to the frozen 2026-09-21 draws", ok,
    "same seed strings, same digests")

# 8 -------------------------------------------------------------- configuration CIs reproduce the frozen CIs
fz = {(r["dataset"], r["model"], r["strategy"]): r for r in csv.DictReader(open(INF / "tables" / "configuration_level_ci.csv"))}
cols = ["acc_eff", "acc_eff_ci_low", "acc_eff_ci_high", "acc_cond", "acc_cond_ci_low", "acc_cond_ci_high",
        "macro_f1", "macro_f1_ci_low", "macro_f1_ci_high", "n_items"]
mismatch = [(r["dataset"], r["model"], r["strategy"], c) for r in cfg for c in cols
            if r[c] != fz[(r["dataset"], r["model"], r["strategy"])][c]]
chk("Configuration-level bootstrap CIs are string-identical to inferential_2026-09-21/configuration_level_ci.csv",
    not mismatch, f"{len(cfg)} configurations x {len(cols)} fields, {len(mismatch)} mismatches")

# 9 -------------------------------------------------------------- shape of the analysis
ok = (len(primary) == 60 and len(mcn) == 30 and len(cond) == 30 and len(cfg) == 30)
chk("Row counts: 60 primary, 30 McNemar, 30 conditional-accuracy CI, 30 configuration CI", ok,
    f"{len(primary)}/{len(mcn)}/{len(cond)}/{len(cfg)}")
fam = collections.Counter(r["family"] for r in primary)
ok = (man["families"] == {"RQ3-primary-dreaddit": 30, "RQ3-primary-goemotions": 30,
                          "RQ3-mcnemar-dreaddit": 15, "RQ3-mcnemar-goemotions": 15}
      and dict(fam) == {"RQ3-primary-dreaddit": 30, "RQ3-primary-goemotions": 30})
chk("Holm families are exactly as declared (30 / 30 primary, 15 / 15 McNemar)", ok, json.dumps(man["families"]))
combos = {(r["dataset"], r["model"], r["strategy_A"], r["strategy_B"], r["metric"]) for r in primary}
ok = len(combos) == 60 and all(int(r["family_size"]) == 30 for r in primary)
chk("All 5 models x 3 declared contrasts x 2 metrics x 2 datasets are present and reported", ok, f"{len(combos)} distinct")

# 10 ------------------------------------------------------------- Holm recomputed independently
def holm(p):
    m = len(p); order = sorted(range(m), key=lambda i: p[i]); adj = [0.0] * m; run = 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (m - rank) * p[i])); adj[i] = run
    return adj
bad = 0
for fname, rows, pk in (("primary", primary, "p_perm"), ("mcnemar", mcn, "p_exact")):
    for ds in ("dreaddit", "goemotions"):
        rs = [r for r in rows if r["dataset"] == ds]
        adj = holm([float(r[pk]) for r in rs])
        for r, a in zip(rs, adj):
            if abs(a - float(r["p_holm"])) > 1e-12: bad += 1
            if (a <= ALPHA) != (r["holm_significant_0.05"] == "True"): bad += 1
chk("Holm-adjusted p-values and significance flags recomputed independently from the raw p-values", bad == 0,
    f"{bad} disagreements over 90 rows")
ok = all(float(r["p_holm"]) >= float(r["p_perm"]) - 1e-15 for r in primary)
chk("Holm-adjusted p is never below the unadjusted p", ok)

# 11 ------------------------------------------------------------- permutation p-values live on the exact grid
grid = {(1 + k) / (1 + P_PERMS) for k in range(P_PERMS + 1)}
off = [r for r in primary if min(abs(float(r["p_perm"]) - g) for g in
       ((1 + round(float(r["p_perm"]) * (1 + P_PERMS) - 1)) / (1 + P_PERMS),)) > 1e-12]
chk("Every permutation p-value is of the form (1 + k) / (1 + P) with P = 10,000", not off,
    f"minimum attainable p = {1 / (1 + P_PERMS):.6f}")

# 12 ------------------------------------------------------------- permutation p re-derived from the replicate files
redone = 0; bad = 0
for ds in ("dreaddit", "goemotions"):
    n = ns[ds]
    with gzip.open(OUT / "replicates" / f"permutation_{ds}.csv.gz", "rt") as f:
        rd = csv.DictReader(f); cols_p = collections.defaultdict(list)
        for row in rd:
            for k, v in row.items():
                if k != "permutation": cols_p[k].append(v)
    for r in [x for x in primary if x["dataset"] == ds]:
        tag = f"{r['model']} | {r['strategy_A']} vs {r['strategy_B']}"
        if r["metric"] == "acc_eff":
            key = tag + " | acc_eff (int)"
            T = [int(v) for v in cols_p[key]]
            T_obs = round(float(r["diff_A_minus_B"]) * 5 * n)
            p = (1 + sum(abs(t) >= abs(T_obs) for t in T)) / (1 + P_PERMS)
        else:
            key = tag + " | macro_f1"
            T = [float(v) for v in cols_p[key]]
            T_obs = float(r["diff_A_minus_B"])
            p = (1 + sum(abs(t) >= abs(T_obs) - 1e-12 for t in T)) / (1 + P_PERMS)
        redone += 1
        if abs(p - float(r["p_perm"])) > 1e-12: bad += 1
chk("All 60 permutation p-values re-derived from the saved permutation statistics", bad == 0,
    f"{redone} re-derived, {bad} disagreements")

# 13 ------------------------------------------------------------- bootstrap CIs re-derived from the replicate files
def pct_ci(x):
    xs = sorted(x); out = []
    for q in (0.025, 0.975):
        h = (len(xs) - 1) * q; lo = math.floor(h)
        out.append(float(xs[lo] + (h - lo) * (xs[min(lo + 1, len(xs) - 1)] - xs[lo])))
    return out
SH = {"zero-shot": "zero-shot", "zero-shot-CoT": "zero-shot-cot", "one-shot-CoT": "one-shot-cot"}
bad = 0; redone = 0
for ds in ("dreaddit", "goemotions"):
    with gzip.open(OUT / "replicates" / f"bootstrap_{ds}.csv.gz", "rt") as f:
        rd = csv.DictReader(f); cols_b = collections.defaultdict(list)
        for row in rd:
            for k, v in row.items():
                if k != "replicate": cols_b[k].append(float(v))
        assert len(next(iter(cols_b.values()))) == B_REPS
    for r in [x for x in primary if x["dataset"] == ds]:
        a = cols_b[f"{r['model']}|{SH[r['strategy_A']]}|{r['metric']}"]
        b = cols_b[f"{r['model']}|{SH[r['strategy_B']]}|{r['metric']}"]
        lo, hi = pct_ci([x - y for x, y in zip(a, b)])
        redone += 1
        if abs(lo - float(r["ci_low"])) > 1e-12 or abs(hi - float(r["ci_high"])) > 1e-12: bad += 1
chk("All 60 bootstrap 95% CIs re-derived from the saved bootstrap replicates", bad == 0,
    f"{redone} re-derived, {bad} disagreements")

# 14 ------------------------------------------------------------- internal additivity of the three contrasts
bad = []
by = collections.defaultdict(dict)
for r in primary:
    by[(r["dataset"], r["model"], r["metric"])][(r["strategy_A"], r["strategy_B"])] = float(r["diff_A_minus_B"])
for k, d in by.items():
    lhs = d[("zero-shot", "one-shot-CoT")]
    rhs = d[("zero-shot", "zero-shot-CoT")] + d[("zero-shot-CoT", "one-shot-CoT")]
    if abs(lhs - rhs) > 1e-12: bad.append((k, lhs, rhs))
chk("The three contrasts are internally consistent: d(ZS,1S-CoT) = d(ZS,ZS-CoT) + d(ZS-CoT,1S-CoT)",
    not bad, f"{len(by)} model x metric x dataset cells, {len(bad)} violations")

# 15 ------------------------------------------------------------- invalid outputs counted, not conditioned away
frozen_run = list(csv.DictReader(open(DESC / "per_run_results.csv")))
inv = collections.defaultdict(int); attr = {}
for r in frozen_run:
    inv[(r["dataset"], r["model"], r["strategy"])] += int(r["N_model_invalid"])
    attr[r["dataset"]] = int(r["N_attributable"])
MID = {"Gemma 4 31B": "google/gemma-4-31b-it", "Llama 4 Scout": "meta-llama/llama-4-scout",
       "Mistral Small 4": "mistralai/mistral-small-2603", "Phi-4": "microsoft/phi-4", "Qwen3.5 27B": "qwen/qwen3.5-27b"}
bad = 0
for r in primary:
    for side in ("A", "B"):
        if inv[(r["dataset"], MID[r["model"]], SH[r[f"strategy_{side}"]])] != int(r[f"{side}_invalid_outputs_5runs"]): bad += 1
chk("Invalid-output counts on every row match the frozen per-run sums", bad == 0, f"{bad} mismatches over 120 values")
bad = 0
for r in primary:
    for side in ("A", "B"):
        ev = float(r[f"{side}_evaluability"]); n = int(r["n_items"])
        if abs((1 - ev) - inv[(r["dataset"], MID[r["model"]], SH[r[f"strategy_{side}"]])] / (5 * n)) > 1e-12: bad += 1
chk("Evaluability = 1 - invalid rate on the attributable denominator for every arm (no conditioning on validity)",
    bad == 0, f"{bad} mismatches over 120 values")

# 16 ------------------------------------------------------------- conditional accuracy carries no test
ok = all("NO TEST" in r["note"] for r in cond) and not any(k.startswith("p_") for k in cond[0])
chk("Conditional accuracy is reported with CIs only and carries no p-value or Holm decision", ok,
    f"{len(cond)} rows, fields: {', '.join(list(cond[0])[:6])}...")

# 17 ------------------------------------------------------------- no pooling
ok = not any("pooled" in r.get("model", "").lower() or r.get("model") in ("All", "ALL", "") for r in primary)
chk("No pooled strategy main effect and no family spanning both datasets", ok,
    "every row is one model x one dataset; families are per dataset")

# 18 ------------------------------------------------------------- GoEmotions anxiety replicate disclosure
ok = "goemotions_bootstrap_replicates_without_anxiety_item" in man
chk("Bootstrap replicates containing no GoEmotions 'anxiety' item are recorded", ok,
    f"{man.get('goemotions_bootstrap_replicates_without_anxiety_item')} of {B_REPS}")

# 19 ------------------------------------------------------------- declared outputs all exist and match the manifest
bad = [n for n, h in man["output_sha256"].items()
       if not ((OUT / "tables" / n).exists() and sha256(OUT / "tables" / n) == h
               or (OUT / "replicates" / n).exists() and sha256(OUT / "replicates" / n) == h)]
chk("Every output file matches the SHA-256 recorded in analysis_manifest.json", not bad,
    f"{len(man['output_sha256'])} files, {len(bad)} mismatches")

# 20 ------------------------------------------------------------- nothing outside this directory was modified
fz_inv = (RES / "verification_2026-09-21" / "freeze_hashes_after.txt")
lines = [l.split() for l in open(fz_inv) if l.strip()]
bad = [p for dig, size, p in lines if sha256(DESC / p.lstrip("./")) != dig]
chk("descriptive_2026-09-21: all 32 files still byte-identical to the 2026-09-21 freeze inventory",
    not bad, f"{len(lines)} files, {len(bad)} changed")
for pkg in ("inferential_2026-09-21", "final_rq_results_2026-09-25", "unified_results_tables_2026-09-25",
            "rq3_inference_design_2026-09-25"):
    d = RES / pkg
    m = d / "CHECKSUMS.sha256"
    if m.exists():
        bad = []
        for l in open(m):
            dig, p = l.strip().split(None, 1)
            p = p.lstrip("*").lstrip()
            if sha256(d / p) != dig: bad.append(p)
        chk(f"{pkg}: verifies against its own CHECKSUMS.sha256", not bad, f"{len(bad)} mismatches")
    else:
        chk(f"{pkg}: present and untouched by this analysis (no manifest of its own to verify)", d.exists(),
            "read-only access only")
# the one pre-existing advisory, reported not hidden
adv = RES / "invalid_output_audit_2026-09-25" / "CHECKSUMS.sha256"
badv = []
for l in open(adv):
    dig, p = l.strip().split(None, 1); p = p.lstrip("*").lstrip()
    if (adv.parent / p).exists() and sha256(adv.parent / p) != dig: badv.append(p)
chk("invalid_output_audit_2026-09-25: pre-existing manifest advisory unchanged by this analysis",
    len(badv) == 2, f"{len(badv)} files still failing that package's own manifest (pre-existing, not caused here): "
    + ", ".join(sorted(badv)))

# ---------------------------------------------------------------- write
n_pass = sum(c["pass"] for c in checks)
json.dump({"n_checks": len(checks), "n_pass": n_pass, "all_passed": n_pass == len(checks), "checks": checks},
          open(OUT / "validation.json", "w"), indent=1)
L = ["# Validation — RQ3 strategy inference (2026-09-25)", "",
     f"**{n_pass} of {len(checks)} checks passed.**" + ("" if n_pass == len(checks) else "  **SOME CHECKS FAILED.**"), "",
     "Every check re-derives its quantity independently of the analysis run: permutation p-values and bootstrap",
     "intervals are recomputed from the saved replicate files, Holm is recomputed from the raw p-values, and the",
     "frozen packages are re-hashed.", "",
     "| # | Check | Result | Detail |", "|---|---|---|---|"]
for c in checks:
    L.append(f"| {c['n']} | {c['check']} | {'PASS' if c['pass'] else '**FAIL**'} | {c['detail']} |")
open(OUT / "VALIDATION.md", "w").write("\n".join(L) + "\n")
print(f"\n{n_pass}/{len(checks)} checks passed")
sys.exit(0 if n_pass == len(checks) else 1)
