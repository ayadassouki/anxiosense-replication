"""Independent verification, part 2: recompute every descriptive number from
authoritative_records.jsonl with exact rational arithmetic (fractions.Fraction) and compare
with per_run_results.csv, aggregate_results.csv, cell_metrics.json, aggregate_five_runs.json.
Stdlib only; imports NOTHING from runner/. Definitions follow MetricPolicy 1.0.0 as documented
(safety excluded from attribution; effective-accuracy denominator = attributable; per-class
P/R/F1 = 0 when undefined; macro = unweighted mean over the fixed label list; sd = sample sd)."""
import json, os, csv, collections
from fractions import Fraction as Q
from decimal import Decimal, getcontext
getcontext().prec = 60
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
F = os.path.join(BASE, "results/descriptive_2026-09-21"); V = os.path.join(BASE, "results/verification_2026-09-21")
LABELS = {"dreaddit": [0, 1], "goemotions": ["anxiety", "fear", "sadness", "frustration", "non_distress"]}
fm = json.load(open(os.path.join(F, "frozen_grid_manifest_public.json")))

def qf(x): return float(x)          # correctly rounded
def qsqrt(q):
    return float((Decimal(q.numerator) / Decimal(q.denominator)).sqrt()) if q else 0.0

# ---------- independent computation ----------
cells = collections.defaultdict(list)
for line in open(os.path.join(F, "authoritative_records.jsonl"), encoding="utf-8"):
    r = json.loads(line); cells[r["cell_id"]].append(r)

def compute(cid, recs):
    ds = cid.split("|")[0]; L = LABELS[ds]
    safe = [r for r in recs if r["final_outcome_class"] == "SAFETY_INTERCEPT"]
    att = [r for r in recs if r["final_outcome_class"] != "SAFETY_INTERCEPT"]
    val = [r for r in att if r["prediction_valid"] is True]
    inv = [r for r in att if r["failure_class"] == "MODEL_BEHAVIOUR"]
    infra = [r for r in att if str(r["failure_class"] or "").startswith("INFRA")]
    corr = sum(1 for r in val if r["parsed_prediction"] == r["ground_truth"])
    pc = {}; conf = {str(a): {str(b): 0 for b in L} for a in L}
    for r in val:
        conf[str(r["ground_truth"])][str(r["parsed_prediction"])] += 1
    for c in L:
        tp = sum(1 for r in val if r["ground_truth"] == c and r["parsed_prediction"] == c)
        fp = sum(1 for r in val if r["ground_truth"] != c and r["parsed_prediction"] == c)
        fn = sum(1 for r in val if r["ground_truth"] == c and r["parsed_prediction"] != c)
        p = Q(tp, tp + fp) if tp + fp else Q(0); rc = Q(tp, tp + fn) if tp + fn else Q(0)
        f1 = 2 * p * rc / (p + rc) if p + rc else Q(0)
        pc[str(c)] = {"precision": p, "recall": rc, "f1": f1, "support": tp + fn, "tp": tp, "fp": fp, "fn": fn}
    k = len(L)
    return {"N_total": len(recs), "N_safety_intercept": len(safe), "N_attributable": len(att),
            "N_valid": len(val), "N_model_invalid": len(inv), "N_infra_failed": len(infra),
            "N_unaccounted": len(att) - len(val) - len(inv) - len(infra),
            "correct": corr, "incorrect": len(val) - corr,
            "accuracy_conditional": Q(corr, len(val)), "accuracy_effective": Q(corr, len(att)),
            "macro_precision": sum(v["precision"] for v in pc.values()) / k,
            "macro_recall": sum(v["recall"] for v in pc.values()) / k,
            "macro_f1": sum(v["f1"] for v in pc.values()) / k,
            "evaluability": Q(len(val), len(att)),
            "model_invalid_rate": Q(len(inv), len(att)), "infrastructure_failure_rate": Q(len(infra), len(att)),
            "per_class": pc, "confusion_matrix": conf,
            "parse_status_counts": dict(collections.Counter(r["parse_status"] for r in recs)),
            "source_run": recs[0]["source_run"]}
mine = {cid: compute(cid, recs) for cid, recs in cells.items()}

# majority baselines from dataset manifests (independently)
base = {}
for ds, info in fm["manifests"].items():
    M = json.load(open(os.path.join(BASE, "manifests", info["file"])))
    gt = [M["ground_truth"][s] for s in M["included_sample_ids"]]
    cls, cnt = collections.Counter(gt).most_common(1)[0]
    base[ds] = {"class": cls, "count": cnt, "n": len(gt), "exact": Q(cnt, len(gt)),
                "manifest_value": M["majority_baseline"], "frozen_value": info["majority_baseline"]}

# ---------- comparison machinery ----------
disc = []; stats = collections.Counter(); maxdiff = collections.defaultdict(float)
def cmp(where, field, mineval, rep):
    stats["compared"] += 1
    if isinstance(mineval, Q):
        exp = qf(mineval)
        if rep is None: disc.append((where, field, exp, rep, "missing")); return
        rep = float(rep)
        if rep == exp: stats["exact"] += 1; return
        d = abs(rep - exp); maxdiff[field] = max(maxdiff[field], d)
        disc.append((where, field, exp, rep, "float_diff=%.3e" % d)); return
    if mineval == rep: stats["exact"] += 1; return
    disc.append((where, field, mineval, rep, "value_differs"))

# per_run_results.csv
rows = list(csv.DictReader(open(os.path.join(F, "per_run_results.csv"))))
seen = set()
for row in rows:
    cid = "%s|%s|%s|run%s" % (row["dataset"], row["model"], row["strategy"], row["run"]); seen.add(cid)
    m = mine[cid]; w = "per_run:" + cid
    for f in ("N_total","N_safety_intercept","N_attributable","N_valid","N_model_invalid","N_infra_failed","N_unaccounted","correct","incorrect"):
        cmp(w, f, m[f], int(row[f]))
    for f in ("accuracy_conditional","accuracy_effective","macro_precision","macro_recall","macro_f1","evaluability"):
        cmp(w, f, m[f], row[f])
    cmp(w, "majority_baseline", base[row["dataset"]]["frozen_value"], float(row["majority_baseline"]))
    cmp(w, "parse_status_counts", m["parse_status_counts"], json.loads(row["parse_status_counts"]))
    cmp(w, "source_run", m["source_run"], row["source_run"])
if seen != set(mine): disc.append(("per_run", "row_set", len(mine), len(seen), "cell set differs"))
if len(rows) != 150: disc.append(("per_run", "row_count", 150, len(rows), "value_differs"))

# cell_metrics.json
cm = json.load(open(os.path.join(F, "cell_metrics.json")))
if set(cm) != set(mine): disc.append(("cell_metrics", "cell_set", 150, len(cm), "value_differs"))
for cid, c in cm.items():
    m = mine[cid]; w = "cell_metrics:" + cid; b = c["buckets"]
    for mf, rf in (("N_total","N_total"),("N_attributable","N_attributable"),("N_valid","N_successful_valid_predictions"),
                   ("N_model_invalid","N_model_behavior_invalid"),("N_infra_failed","N_infrastructure_failed"),
                   ("N_safety_intercept","N_safety_intercept"),("N_unaccounted","N_unaccounted")):
        cmp(w, "buckets." + rf, m[mf], b[rf])
    for f in ("evaluability","model_invalid_rate","infrastructure_failure_rate"):
        cmp(w, "rates." + f, m[f], c["rates"][f])
    mm = c["metrics"]
    for f in ("accuracy_conditional","accuracy_effective","macro_precision","macro_recall","macro_f1"):
        cmp(w, "metrics." + f, m[f], mm[f])
    for cl, v in m["per_class"].items():
        rv = mm["per_class"][cl]
        for f in ("precision","recall","f1"): cmp(w, "per_class.%s.%s" % (cl, f), v[f], rv[f])
        for f in ("support","tp","fp","fn"): cmp(w, "per_class.%s.%s" % (cl, f), v[f], rv[f])
        cmp(w, "class_support.%s" % cl, v["support"], mm["class_support"][cl])
    cmp(w, "confusion_matrix", m["confusion_matrix"], mm["confusion_matrix"])
    cmp(w, "labels", [str(x) for x in LABELS[cid.split("|")[0]]], c["labels"])
    cmp(w, "majority_baseline", base[cid.split("|")[0]]["frozen_value"], c["majority_baseline"])
    cmp(w, "parse_status_counts", m["parse_status_counts"], c["parse_status_counts"])
    cmp(w, "source_run", m["source_run"], c["source_run"])

# five-run aggregates
groups = collections.defaultdict(list)
for cid, m in mine.items():
    ds, mo, st, _ = cid.split("|"); groups[(ds, mo, st)].append(m)
def mean(xs): return sum(xs, Q(0)) / len(xs)
def sd(xs):
    mu = mean(xs); return qsqrt(sum(((x - mu) ** 2 for x in xs), Q(0)) / (len(xs) - 1))
agg_rows = {(r["dataset"], r["model"], r["strategy"]): r for r in csv.DictReader(open(os.path.join(F, "aggregate_results.csv")))}
agg_json = json.load(open(os.path.join(F, "aggregate_five_runs.json")))
if len(agg_rows) != 30 or len(agg_json) != 30: disc.append(("aggregate", "row_count", 30, (len(agg_rows), len(agg_json)), "value_differs"))
sd_disc = []
for key, ms in groups.items():
    if len(ms) != 5: disc.append(("aggregate", "n_runs", 5, len(ms), "value_differs"))
    row = agg_rows[key]; j = agg_json["|".join(key)]; w = "aggregate:" + "|".join(key)
    cmp(w, "n_runs(csv)", 5, int(row["n_runs"])); cmp(w, "n_runs(json)", 5, j["n_runs"])
    for f in ("accuracy_conditional","accuracy_effective","macro_f1","evaluability"):
        xs = [m[f] for m in ms]
        cmp(w, f + "_mean(csv)", mean(xs), row[f + "_mean"]); cmp(w, f + ".mean(json)", mean(xs), j[f]["mean"])
        s = sd(xs); stats["compared"] += 2
        for tag, rep in (("csv", float(row[f + "_sd"])), ("json", j[f]["sd"])):
            if rep == s: stats["exact"] += 1
            else:
                d = abs(rep - s); maxdiff[f + "_sd"] = max(maxdiff[f + "_sd"], d)
                disc.append((w, "%s_sd(%s)" % (f, tag), s, rep, "float_diff=%.3e" % d))
    for f, src in (("sum_N_total","N_total"),("sum_N_safety","N_safety_intercept"),("sum_N_valid","N_valid"),
                   ("sum_N_model_invalid","N_model_invalid"),("sum_correct","correct")):
        cmp(w, f, sum(m[src] for m in ms), int(row[f]))

# majority baseline self-check
for ds, b in base.items():
    cmp("baseline:" + ds, "manifest_rounded_vs_exact", round(qf(b["exact"]), 6), b["manifest_value"])
    cmp("baseline:" + ds, "frozen_vs_manifest", b["manifest_value"], b["frozen_value"])

# ---------- output ----------
float_only = [d for d in disc if str(d[4]).startswith("float_diff")]
other = [d for d in disc if not str(d[4]).startswith("float_diff")]
res = {"comparisons": stats["compared"], "exact_matches": stats["exact"],
       "discrepancies_total": len(disc), "float_rounding_discrepancies": len(float_only),
       "non_float_discrepancies": len(other), "max_abs_float_diff_by_field": dict(maxdiff),
       "majority_baselines": {ds: {"class": b["class"], "count": b["count"], "n": b["n"],
                                   "exact": str(b["exact"]), "exact_float": qf(b["exact"]),
                                   "reported": b["frozen_value"]} for ds, b in base.items()},
       "discrepancies": [{"where": a, "field": b, "independent": c, "reported": d, "kind": e} for a, b, c, d, e in disc]}
json.dump(res, open(os.path.join(V, "metrics_verification_result.json"), "w"), indent=1, default=str)
# independent per-run table for the record
with open(os.path.join(V, "independent_per_run.csv"), "w", newline="") as f:
    cols = ["cell_id","N_total","N_safety_intercept","N_attributable","N_valid","N_model_invalid","N_infra_failed",
            "N_unaccounted","correct","incorrect","accuracy_conditional","accuracy_effective","macro_precision",
            "macro_recall","macro_f1","evaluability","accuracy_conditional_exact","accuracy_effective_exact","macro_f1_exact"]
    wr = csv.writer(f); wr.writerow(cols)
    for cid in sorted(mine):
        m = mine[cid]
        wr.writerow([cid] + [m[c] for c in cols[1:10]] + [repr(qf(m[c])) for c in cols[10:16]] +
                    [str(m["accuracy_conditional"]), str(m["accuracy_effective"]), str(m["macro_f1"])])
print(json.dumps({k: v for k, v in res.items() if k != "discrepancies"}, indent=1, default=str))
for d in disc[:40]: print("DISC:", d)
