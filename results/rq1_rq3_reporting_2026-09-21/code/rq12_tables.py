"""RQ1 / RQ2 reporting tables from the FROZEN, independently verified descriptive results.

Primary input : results/descriptive_2026-09-21/authoritative_records.jsonl (read-only).
Cross-check   : per_run_results.csv, aggregate_results.csv, aggregate_five_runs.json, cell_metrics.json
                (read-only) and verification_2026-09-21/metrics_verification_result.json.
Definitions   : MetricPolicy 1.0.0 exactly as frozen (see REPORT.md). Nothing is re-parsed; parse_status,
                prediction_valid, failure_class are used exactly as stored.
Arithmetic    : exact rationals (fractions.Fraction) for every per-run metric and every five-run mean;
                sample SD (n-1) via Decimal sqrt at 60 digits.
Rounding      : presentation = 3 decimals, ROUND_HALF_UP applied to the exact value (never to a binary float).
Any cross-check failure other than the documented last-ulp float class ABORTS without writing tables.
Stdlib only. Writes only into results/rq1_rq3_reporting_2026-09-21/."""
import json, os, csv, collections, sys
from fractions import Fraction as Q
from decimal import Decimal, getcontext, ROUND_HALF_UP
getcontext().prec = 60
# Repo-relative roots, derived from this file's location:
#   <repo>/results/rq1_rq3_reporting_2026-09-21/code/rq12_tables.py
OUT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES  = os.path.dirname(OUT)                      # <repo>/results
REPO = os.path.dirname(RES)                      # <repo>
F = os.path.join(RES, "descriptive_2026-09-21")
V = os.path.join(RES, "verification_2026-09-21")
MANIFESTS = os.path.join(REPO, "evaluation", "publication_experiments", "manifests")
T = os.path.join(OUT, "tables")
LABELS = {"dreaddit": [0, 1], "goemotions": ["anxiety", "fear", "sadness", "frustration", "non_distress"]}
STRATS = ["zero-shot", "zero-shot-cot", "one-shot-cot"]
SHORT = {"google/gemma-4-31b-it": "Gemma 4 31B", "meta-llama/llama-4-scout": "Llama 4 Scout",
         "microsoft/phi-4": "Phi-4", "mistralai/mistral-small-2603": "Mistral Small 4", "qwen/qwen3.5-27b": "Qwen3.5 27B"}
fm = json.load(open(os.path.join(F, "frozen_grid_manifest_public.json")))

cells = collections.defaultdict(list)
for line in open(os.path.join(F, "authoritative_records.jsonl"), encoding="utf-8"):
    r = json.loads(line); cells[r["cell_id"]].append(r)
assert len(cells) == 150 and sum(map(len, cells.values())) == 100350

def cell(cid, recs):
    ds = cid.split("|")[0]; L = LABELS[ds]
    att = [r for r in recs if r["final_outcome_class"] != "SAFETY_INTERCEPT"]
    val = [r for r in att if r["prediction_valid"] is True]
    inv = [r for r in att if r["failure_class"] == "MODEL_BEHAVIOUR"]
    infra = [r for r in att if str(r["failure_class"] or "").startswith("INFRA")]
    corr = sum(r["parsed_prediction"] == r["ground_truth"] for r in val)
    pc = {}
    for c in L:
        tp = sum(r["ground_truth"] == c and r["parsed_prediction"] == c for r in val)
        fp = sum(r["ground_truth"] != c and r["parsed_prediction"] == c for r in val)
        fn = sum(r["ground_truth"] == c and r["parsed_prediction"] != c for r in val)
        p = Q(tp, tp + fp) if tp + fp else Q(0); rc = Q(tp, tp + fn) if tp + fn else Q(0)
        pc[str(c)] = {"precision": p, "recall": rc, "f1": (2 * p * rc / (p + rc) if p + rc else Q(0)),
                      "predicted_share": Q(tp + fp, len(val)) if val else Q(0)}
    k = len(L)
    return {"N_total": len(recs), "N_safety": len(recs) - len(att), "N_attributable": len(att), "N_valid": len(val),
            "N_model_invalid": len(inv), "N_infra": len(infra), "N_unaccounted": len(att) - len(val) - len(inv) - len(infra),
            "correct": corr,
            "acc_cond": Q(corr, len(val)), "acc_eff": Q(corr, len(att)),
            "macro_p": sum(v["precision"] for v in pc.values()) / k, "macro_r": sum(v["recall"] for v in pc.values()) / k,
            "macro_f1": sum(v["f1"] for v in pc.values()) / k,
            "evaluability": Q(len(val), len(att)), "invalid_rate": Q(len(inv), len(att)), "per_class": pc,
            "parse_status": collections.Counter(r["parse_status"] for r in recs)}
M = {cid: cell(cid, recs) for cid, recs in cells.items()}

def dec(q): return Decimal(q.numerator) / Decimal(q.denominator)
def mean(xs): return sum(xs, Q(0)) / len(xs)
def sd(xs):
    mu = mean(xs); v = sum(((x - mu) ** 2 for x in xs), Q(0)) / (len(xs) - 1)
    return dec(v).sqrt() if v else Decimal(0)
def r3(d):  # d: Fraction or Decimal -> str, ROUND_HALF_UP at 3 dp
    d = dec(d) if isinstance(d, Q) else d
    return str(d.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))
def is_tie3(d):
    d = dec(d) if isinstance(d, Q) else d
    s = (d * 1000) - (d * 1000).to_integral_value(rounding="ROUND_FLOOR")
    return s == Decimal("0.5")

# ---------------- cross-check against frozen files ----------------
ver = json.load(open(os.path.join(V, "metrics_verification_result.json")))
known = {(d["where"], d["field"]) for d in ver["discrepancies"]}
problems = []; checks = collections.Counter()
def chk(where, field, exact, rep, tol=4.5e-16):
    checks["n"] += 1
    if isinstance(exact, Q):
        e = float(exact); rep = float(rep)
        if e == rep: checks["exact"] += 1; return
        if abs(e - rep) <= tol and (where, field) in known: checks["known_ulp"] += 1; return
        problems.append((where, field, str(exact), e, rep)); return
    if isinstance(exact, Decimal):
        e = float(exact); rep = float(rep)
        if e == rep: checks["exact"] += 1; return
        if abs(e - rep) <= tol and (where, field) in known: checks["known_ulp"] += 1; return
        problems.append((where, field, str(exact), e, rep)); return
    if exact == rep: checks["exact"] += 1
    else: problems.append((where, field, exact, None, rep))

for row in csv.DictReader(open(os.path.join(F, "per_run_results.csv"))):
    cid = "%s|%s|%s|run%s" % (row["dataset"], row["model"], row["strategy"], row["run"]); m = M[cid]; w = "per_run:" + cid
    for a, b in (("N_total", "N_total"), ("N_safety", "N_safety_intercept"), ("N_attributable", "N_attributable"),
                 ("N_valid", "N_valid"), ("N_model_invalid", "N_model_invalid"), ("N_infra", "N_infra_failed"),
                 ("N_unaccounted", "N_unaccounted"), ("correct", "correct")):
        chk(w, b, m[a], int(row[b]))
    for a, b in (("acc_cond", "accuracy_conditional"), ("acc_eff", "accuracy_effective"), ("macro_p", "macro_precision"),
                 ("macro_r", "macro_recall"), ("macro_f1", "macro_f1"), ("evaluability", "evaluability")):
        chk(w, b, m[a], row[b])
cm = json.load(open(os.path.join(F, "cell_metrics.json")))
for cid, c in cm.items():
    w = "cell_metrics:" + cid; m = M[cid]
    for cl, v in m["per_class"].items():
        for f in ("precision", "recall", "f1"): chk(w, "per_class.%s.%s" % (cl, f), v[f], c["metrics"]["per_class"][cl][f])
    chk(w, "rates.model_invalid_rate", m["invalid_rate"], c["rates"]["model_invalid_rate"])

G = collections.defaultdict(dict)
for cid, m in M.items():
    ds, mo, st, rn = cid.split("|"); G[(ds, mo, st)][int(rn[3:])] = m
assert len(G) == 30 and all(sorted(v) == [1, 2, 3, 4, 5] for v in G.values())
FIELDS = ["acc_cond", "acc_eff", "macro_p", "macro_r", "macro_f1", "evaluability", "invalid_rate"]
AGG = {}
for key, runs in G.items():
    ms = [runs[i] for i in range(1, 6)]
    a = {f: {"mean": mean([m[f] for m in ms]), "sd": sd([m[f] for m in ms])} for f in FIELDS}
    for s in ("N_total", "N_safety", "N_attributable", "N_valid", "N_model_invalid", "N_infra", "N_unaccounted", "correct"):
        a["sum_" + s] = sum(m[s] for m in ms)
    a["per_class"] = {cl: {f: {"mean": mean([m["per_class"][cl][f] for m in ms]), "sd": sd([m["per_class"][cl][f] for m in ms])}
                           for f in ("precision", "recall", "f1", "predicted_share")} for cl in ms[0]["per_class"]}
    a["parse_status_sum"] = sum((m["parse_status"] for m in ms), collections.Counter())
    a["runs"] = {i: {f: runs[i][f] for f in FIELDS + ["N_valid", "N_attributable", "N_model_invalid"]} for i in range(1, 6)}
    AGG[key] = a
aggcsv = {(r["dataset"], r["model"], r["strategy"]): r for r in csv.DictReader(open(os.path.join(F, "aggregate_results.csv")))}
aggjs = json.load(open(os.path.join(F, "aggregate_five_runs.json")))
for key, a in AGG.items():
    w = "aggregate:" + "|".join(key); row = aggcsv[key]; j = aggjs["|".join(key)]
    for f, nm in (("acc_cond", "accuracy_conditional"), ("acc_eff", "accuracy_effective"), ("macro_f1", "macro_f1"), ("evaluability", "evaluability")):
        chk(w, nm + "_mean(csv)", a[f]["mean"], row[nm + "_mean"]); chk(w, nm + ".mean(json)", a[f]["mean"], j[nm]["mean"])
        chk(w, nm + "_sd(csv)", a[f]["sd"], row[nm + "_sd"]); chk(w, nm + "_sd(json)", a[f]["sd"], j[nm]["sd"])
    for s, nm in (("sum_N_total", "sum_N_total"), ("sum_N_safety", "sum_N_safety"), ("sum_N_valid", "sum_N_valid"),
                  ("sum_N_model_invalid", "sum_N_model_invalid"), ("sum_correct", "sum_correct")):
        chk(w, nm, a[s], int(row[nm]))
# baselines
BL = {}
for ds, info in fm["manifests"].items():
    Mf = json.load(open(os.path.join(MANIFESTS, info["file"])))
    gt = {s: Mf["ground_truth"][s] for s in Mf["included_sample_ids"]}
    cls, cnt = collections.Counter(gt.values()).most_common(1)[0]
    # attributable set = samples that are not safety-intercepted (identical across cells per frozen manifest)
    any_cell = next(c for c in M if c.startswith(ds + "|"))
    safe_ids = {r["sample_id"] for r in cells[any_cell] if r["final_outcome_class"] == "SAFETY_INTERCEPT"}
    att_gt = [g for s, g in gt.items() if s not in safe_ids]
    att_cnt = collections.Counter(att_gt)
    # constant majority-class predictor evaluated like a model on the attributable set (derived reference)
    L = LABELS[ds]; pmaj = Q(att_cnt[cls], len(att_gt)); f1maj = 2 * pmaj / (pmaj + 1)
    BL[ds] = {"class": cls, "count": cnt, "n": len(gt), "exact": Q(cnt, len(gt)), "frozen": info["majority_baseline"],
              "attributable_n": len(att_gt), "attributable_majority_count": att_cnt[cls],
              "attributable_majority_rate": pmaj, "attributable_class_counts": {str(k): v for k, v in sorted(att_cnt.items(), key=lambda x: str(x[0]))},
              "full_class_counts": {str(k): v for k, v in sorted(collections.Counter(gt.values()).items(), key=lambda x: str(x[0]))},
              "safety_ids_n": len(safe_ids),
              "constant_majority_macro_f1_attributable": f1maj / len(L),
              "constant_majority_macro_recall": Q(1, len(L))}
    chk("baseline:" + ds, "frozen_vs_exact_6dp", round(float(BL[ds]["exact"]), 6), info["majority_baseline"])

# rounding agreement: presented 3-dp value from exact vs 3-dp value the frozen float would give
round_notes = []
def pres(where, field, exact, frozen_float):
    a = r3(exact); b = r3(Decimal(repr(float(frozen_float))))
    tie = is_tie3(exact)
    if a != b or tie: round_notes.append({"where": where, "field": field, "exact": str(exact), "presented_half_up": a,
                                          "frozen_float": repr(float(frozen_float)), "frozen_float_rounded": b, "exact_tie": tie})
for key, a in AGG.items():
    row = aggcsv[key]; w = "aggregate:" + "|".join(key)
    for f, nm in (("acc_cond", "accuracy_conditional"), ("acc_eff", "accuracy_effective"), ("macro_f1", "macro_f1"), ("evaluability", "evaluability")):
        pres(w, nm + "_mean", a[f]["mean"], row[nm + "_mean"]); pres(w, nm + "_sd", a[f]["sd"], row[nm + "_sd"])
    for f in ("macro_p", "macro_r", "invalid_rate"):
        for s in ("mean", "sd"):
            if is_tie3(a[f][s]): round_notes.append({"where": w, "field": f + "_" + s, "exact": str(a[f][s]), "exact_tie": True})
    for cl, d in a["per_class"].items():
        for f, v in d.items():
            for s in ("mean", "sd"):
                if is_tie3(v[s]): round_notes.append({"where": w, "field": "per_class.%s.%s_%s" % (cl, f, s), "exact": str(v[s]), "exact_tie": True})

crosscheck = {"checks": checks["n"], "exact": checks["exact"], "known_last_ulp_float": checks["known_ulp"],
              "problems": [list(map(str, p)) for p in problems], "rounding_notes": round_notes}
json.dump(crosscheck, open(os.path.join(OUT, "rq12_crosscheck.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in crosscheck.items() if k != "rounding_notes"}, indent=1), "rounding_notes:", len(round_notes))
if problems:
    sys.exit("CROSS-CHECK FAILED - no tables written. See rq12_crosscheck.json")

# ---------------- tables ----------------
def pm(d): return "%s ± %s" % (r3(d["mean"]), r3(d["sd"]))
MODELS = sorted({k[1] for k in AGG}, key=lambda m: SHORT[m])
full = {}
for ds in ("dreaddit", "goemotions"):
    b = BL[ds]
    rows1, rows2 = [], []
    for mo in MODELS:
        for st in STRATS:
            a = AGG[(ds, mo, st)]
            rows1.append({"model": SHORT[mo], "model_id": mo, "strategy": st,
                          "acc_conditional": pm(a["acc_cond"]), "acc_effective": pm(a["acc_eff"]),
                          "macro_precision": pm(a["macro_p"]), "macro_recall": pm(a["macro_r"]), "macro_f1": pm(a["macro_f1"]),
                          "evaluability": pm(a["evaluability"]),
                          "valid_over_attributable_5runs": "%d / %d" % (a["sum_N_valid"], a["sum_N_attributable"]),
                          "model_invalid_5runs": a["sum_N_model_invalid"], "infra_failed_5runs": a["sum_N_infra"],
                          "safety_intercepts_5runs": a["sum_N_safety"],
                          "invalid_per_run": "/".join(str(a["runs"][i]["N_model_invalid"]) for i in range(1, 6))})
            rows2.append({"model": SHORT[mo], "strategy": st,
                          "acc_conditional": pm(a["acc_cond"]), "acc_effective": pm(a["acc_eff"]), "macro_f1": pm(a["macro_f1"]),
                          "majority_baseline": r3(b["exact"]),
                          "acc_cond_minus_baseline": r3(a["acc_cond"]["mean"] - b["exact"]),
                          "acc_eff_minus_baseline": r3(a["acc_eff"]["mean"] - b["exact"]),
                          "runs_acc_cond_above_baseline": sum(a["runs"][i]["acc_cond"] > b["exact"] for i in range(1, 6)),
                          "runs_acc_eff_above_baseline": sum(a["runs"][i]["acc_eff"] > b["exact"] for i in range(1, 6)),
                          "evaluability": pm(a["evaluability"]),
                          "model_invalid_5runs": a["sum_N_model_invalid"],
                          "valid_over_attributable_5runs": "%d / %d" % (a["sum_N_valid"], a["sum_N_attributable"])})
    for name, rows in (("rq1_%s" % ds, rows1), ("rq2_%s" % ds, rows2)):
        with open(os.path.join(T, name + ".csv"), "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
    if ds == "goemotions":
        rows3 = []
        for mo in MODELS:
            for st in STRATS:
                a = AGG[(ds, mo, st)]; r = {"model": SHORT[mo], "strategy": st}
                for cl in LABELS[ds]:
                    d = a["per_class"][cl]
                    r[cl + "_recall"] = pm(d["recall"]); r[cl + "_f1"] = pm(d["f1"]); r[cl + "_pred_share"] = pm(d["predicted_share"])
                rows3.append(r)
        with open(os.path.join(T, "rq2_goemotions_per_class.csv"), "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(rows3[0])); wr.writeheader(); wr.writerows(rows3)
    if ds == "dreaddit":
        rows3 = []
        for mo in MODELS:
            for st in STRATS:
                a = AGG[(ds, mo, st)]; r = {"model": SHORT[mo], "strategy": st}
                for cl in ("0", "1"):
                    d = a["per_class"][cl]
                    r["class%s_precision" % cl] = pm(d["precision"]); r["class%s_recall" % cl] = pm(d["recall"])
                    r["class%s_f1" % cl] = pm(d["f1"]); r["class%s_pred_share" % cl] = pm(d["predicted_share"])
                rows3.append(r)
        with open(os.path.join(T, "rq2_dreaddit_per_class.csv"), "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(rows3[0])); wr.writeheader(); wr.writerows(rows3)

# rank / metric-disagreement evidence (descriptive only, exact values)
rank = {}
for ds in ("dreaddit", "goemotions"):
    rank[ds] = {}
    for f in ("acc_cond", "acc_eff", "macro_f1", "macro_p", "macro_r", "evaluability"):
        allc = sorted(((AGG[(ds, mo, st)][f]["mean"], SHORT[mo], st) for mo in MODELS for st in STRATS), reverse=True)
        rank[ds][f] = {"top3_cells": [[r3(v), m, s] for v, m, s in allc[:3]], "bottom3_cells": [[r3(v), m, s] for v, m, s in allc[-3:]],
                       "top_model_per_strategy": {st: max(((AGG[(ds, mo, st)][f]["mean"], SHORT[mo]) for mo in MODELS))[1] for st in STRATS},
                       "model_mean_over_strategies_rank": [[m, r3(v)] for v, m in sorted(((mean([AGG[(ds, mo, st)][f]["mean"] for st in STRATS]), SHORT[mo]) for mo in MODELS), reverse=True)]}
    rank[ds]["cells_below_baseline_acc_cond"] = [[SHORT[mo], st, r3(AGG[(ds, mo, st)]["acc_cond"]["mean"])] for mo in MODELS for st in STRATS if AGG[(ds, mo, st)]["acc_cond"]["mean"] <= BL[ds]["exact"]]
    rank[ds]["cells_below_baseline_acc_eff"] = [[SHORT[mo], st, r3(AGG[(ds, mo, st)]["acc_eff"]["mean"])] for mo in MODELS for st in STRATS if AGG[(ds, mo, st)]["acc_eff"]["mean"] <= BL[ds]["exact"]]
    vals = {f: [AGG[(ds, mo, st)][f]["mean"] for mo in MODELS for st in STRATS] for f in ("acc_cond", "acc_eff", "macro_f1", "evaluability")}
    rank[ds]["range"] = {f: [r3(min(v)), r3(max(v))] for f, v in vals.items()}
json.dump(rank, open(os.path.join(OUT, "rq1_metric_ranks.json"), "w"), indent=1)

def ser(o):
    if isinstance(o, Q): return {"exact": str(o), "float": float(o)}
    if isinstance(o, Decimal): return {"decimal60": str(o), "float": float(o)}
    if isinstance(o, collections.Counter): return dict(o)
    raise TypeError(type(o))
json.dump({"aggregates": {"|".join(k): v for k, v in AGG.items()}, "baselines": BL}, open(os.path.join(OUT, "rq12_full_precision.json"), "w"), indent=1, default=ser)
print("TABLES WRITTEN")
