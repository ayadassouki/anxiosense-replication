"""Build two unified descriptive results tables (Dreaddit, GoEmotions) for RQ1/RQ2/RQ3.

READ-ONLY outside OUT. No new metric is defined, no inferential test is run, and no frozen
artifact is modified. Every value is either copied from a frozen artifact or is the frozen
mean +/- sample SD of frozen per-run values, recomputed here only to VERIFY the copy.

Sources
  rq1_rq3_reporting_2026-09-21/rq12_full_precision.json      five-run mean (exact fraction) and
                                                             SD (60-digit decimal) for acc_cond,
                                                             acc_eff, macro_p, macro_r, macro_f1,
                                                             evaluability, invalid_rate, per_class
  descriptive_2026-09-21/per_run_results.csv                 per-run values, all 5 runs (verification)
  descriptive_2026-09-21/aggregate_five_runs.json            frozen five-run mean/SD (verification)
  descriptive_2026-09-21/aggregate_results.csv               frozen five-run mean/SD (verification)
  rq1_rq3_reporting_2026-09-21/tables/rq3_<ds>_latency.csv    client end-to-end latency, mean +/- SD
"""
import json, os, csv, statistics, collections

REPO = os.environ["REPO"]; OUT = os.environ["OUT"]
RES = f"{REPO}/evaluation/publication_experiments/results"
DESC, REP = f"{RES}/descriptive_2026-09-21", f"{RES}/rq1_rq3_reporting_2026-09-21"
os.makedirs(f"{OUT}/tables", exist_ok=True)

FP = json.load(open(f"{REP}/rq12_full_precision.json"))
AGG, BASE = FP["aggregates"], FP["baselines"]
FROZEN5 = json.load(open(f"{DESC}/aggregate_five_runs.json"))
MODELS = [("Gemma 4 31B", "google/gemma-4-31b-it"), ("Llama 4 Scout", "meta-llama/llama-4-scout"),
          ("Mistral Small 4", "mistralai/mistral-small-2603"), ("Phi-4", "microsoft/phi-4"),
          ("Qwen3.5 27B", "qwen/qwen3.5-27b")]
STRATS = [("zero-shot", "zero-shot"), ("zero-shot-CoT", "zero-shot-cot"), ("one-shot-CoT", "one-shot-cot")]
DATASETS = ["dreaddit", "goemotions"]
# The frozen latency tables in rq1_rq3_reporting_2026-09-21 use the same display labels as
# MODELS above ("Gemma 4 31B", "Qwen3.5 27B"). The later rq1_rq3_tables package uses different
# labels ("Gemma 4 31B IT", "Qwen 3.5 27B"); that package is NOT a source here.

def load(p): return list(csv.DictReader(open(p, encoding="utf-8")))
per_run = collections.defaultdict(dict)
for r in load(f"{DESC}/per_run_results.csv"):
    per_run[(r["dataset"], r["model"], r["strategy"])][int(r["run"])] = r
lat = {}
for ds in DATASETS:
    for r in load(f"{REP}/tables/rq3_{ds}_latency.csv"):
        lat[(ds, r["model"], r["strategy"])] = r

def ms(mean, sd, nd=4):
    return f"{float(mean):.{nd}f} ± {float(sd):.{nd}f}"

ISSUES = []
def note(msg): ISSUES.append(msg)

COLS = ["Model", "Prompt Strategy",
        "Conditional Accuracy (mean ± SD)", "Effective Accuracy (mean ± SD)",
        "Macro-Precision (mean ± SD)", "Macro-Recall (mean ± SD)", "Macro-F1 (mean ± SD)",
        "Invalid Outputs (Σ 5 runs)", "Invalid Output Rate (mean ± SD)",
        "Total System Response Time (s, mean ± SD)"]

def build(ds):
    rows = []
    for mname, mid in MODELS:
        for sname, sid in STRATS:
            a = AGG[f"{ds}|{mid}|{sid}"]
            L = lat[(ds, mname, sid)]
            # --- verification 1: five-run mean/SD recomputed from the frozen per-run values
            pr = per_run[(ds, mid, sid)]
            if sorted(pr) != [1, 2, 3, 4, 5]:
                note(f"{ds}|{mid}|{sid}: per-run rows are {sorted(pr)}, expected runs 1-5")
            for key, col in (("acc_cond", "accuracy_conditional"), ("acc_eff", "accuracy_effective"),
                             ("macro_p", "macro_precision"), ("macro_r", "macro_recall"),
                             ("macro_f1", "macro_f1"), ("evaluability", "evaluability")):
                vals = [float(pr[i][col]) for i in range(1, 6)]
                m_rec, s_rec = statistics.fmean(vals), statistics.stdev(vals)
                m_fp, s_fp = a[key]["mean"]["float"], a[key]["sd"]["float"]
                if abs(m_rec - m_fp) > 1e-9 or abs(s_rec - s_fp) > 1e-9:
                    note(f"{ds}|{mid}|{sid} {key}: recomputed {m_rec:.12f}±{s_rec:.12f} vs "
                         f"rq12_full_precision {m_fp:.12f}±{s_fp:.12f}")
            # --- verification 2: against the frozen descriptive aggregate
            f5 = FROZEN5.get(f"{ds}|{mid}|{sid}")
            if f5 is None:
                note(f"{ds}|{mid}|{sid}: missing from aggregate_five_runs.json")
            else:
                for key, fk in (("acc_cond", "accuracy_conditional"), ("acc_eff", "accuracy_effective"),
                                ("macro_f1", "macro_f1"), ("evaluability", "evaluability")):
                    if abs(a[key]["mean"]["float"] - f5[fk]["mean"]) > 1e-9 or \
                       abs(a[key]["sd"]["float"] - f5[fk]["sd"]) > 1e-9:
                        note(f"{ds}|{mid}|{sid} {key}: rq12_full_precision vs aggregate_five_runs.json differ")
                if "macro_p" in f5 or "macro_r" in f5:
                    note(f"{ds}|{mid}|{sid}: aggregate_five_runs.json unexpectedly contains macro_p/macro_r")
            # --- verification 3: invalid count against the per-run sum
            inv_sum = sum(int(pr[i]["N_model_invalid"]) for i in range(1, 6))
            if inv_sum != a["sum_N_model_invalid"]:
                note(f"{ds}|{mid}|{sid}: invalid count {a['sum_N_model_invalid']} vs per-run sum {inv_sum}")
            rows.append({
                "Model": mname, "Prompt Strategy": sname,
                "Conditional Accuracy (mean ± SD)": ms(a["acc_cond"]["mean"]["float"], a["acc_cond"]["sd"]["float"]),
                "Effective Accuracy (mean ± SD)": ms(a["acc_eff"]["mean"]["float"], a["acc_eff"]["sd"]["float"]),
                "Macro-Precision (mean ± SD)": ms(a["macro_p"]["mean"]["float"], a["macro_p"]["sd"]["float"]),
                "Macro-Recall (mean ± SD)": ms(a["macro_r"]["mean"]["float"], a["macro_r"]["sd"]["float"]),
                "Macro-F1 (mean ± SD)": ms(a["macro_f1"]["mean"]["float"], a["macro_f1"]["sd"]["float"]),
                "Invalid Outputs (Σ 5 runs)": a["sum_N_model_invalid"],
                "Invalid Output Rate (mean ± SD)": ms(a["invalid_rate"]["mean"]["float"],
                                                      a["invalid_rate"]["sd"]["float"]),
                "Total System Response Time (s, mean ± SD)": L["client_latency_mean_s"],
            })
    return rows

for ds in DATASETS:
    rows = build(ds)
    with open(f"{OUT}/tables/unified_{ds}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); w.writerows(rows)
    with open(f"{OUT}/tables/unified_{ds}.md", "w", encoding="utf-8") as fh:
        fh.write("| " + " | ".join(COLS) + " |\n|" + "---|" * len(COLS) + "\n")
        for r in rows:
            fh.write("| " + " | ".join(str(r[c]) for c in COLS) + " |\n")
    print(f"tables/unified_{ds}.csv + .md: {len(rows)} rows")

# per-class supplement: the ONLY place a non-macro precision/recall/F1 exists
PC = ["dataset", "model", "strategy", "class", "support_in_attributable_pool",
      "precision_mean ± SD", "recall_mean ± SD", "f1_mean ± SD", "predicted_share_mean ± SD"]
pc_rows = []
for ds in DATASETS:
    for mname, mid in MODELS:
        for sname, sid in STRATS:
            a = AGG[f"{ds}|{mid}|{sid}"]
            for cls in sorted(a["per_class"]):
                c = a["per_class"][cls]
                # per_class carries precision/recall/f1/predicted_share but not support;
                # support is a fixed property of the attributable item pool, taken from the
                # frozen baselines block.
                sup_v = BASE[ds]["attributable_class_counts"].get(cls)
                pc_rows.append({
                    "dataset": ds, "model": mname, "strategy": sname, "class": cls,
                    "support_in_attributable_pool": "" if sup_v is None else str(sup_v),
                    "precision_mean ± SD": ms(c["precision"]["mean"]["float"], c["precision"]["sd"]["float"]),
                    "recall_mean ± SD": ms(c["recall"]["mean"]["float"], c["recall"]["sd"]["float"]),
                    "f1_mean ± SD": ms(c["f1"]["mean"]["float"], c["f1"]["sd"]["float"]),
                    "predicted_share_mean ± SD": ms(c["predicted_share"]["mean"]["float"],
                                                    c["predicted_share"]["sd"]["float"])
                        if "predicted_share" in c else "",
                })
with open(f"{OUT}/tables/per_class_supplement.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=PC); w.writeheader(); w.writerows(pc_rows)
print("tables/per_class_supplement.csv:", len(pc_rows), "rows")

print("\nbaselines (context for RQ2):")
for ds in DATASETS:
    b = BASE[ds]
    print(f"  {ds}: frozen scalar {b['frozen']} ({b['count']}/{b['n']}), "
          f"attributable {b['attributable_majority_count']}/{b['attributable_n']} = "
          f"{b['attributable_majority_rate']['float']:.6f}")

print("\nVERIFICATION:", "no discrepancies" if not ISSUES else f"{len(ISSUES)} DISCREPANCIES")
for m in ISSUES: print("  !!", m)
json.dump({"discrepancies": ISSUES}, open(f"{OUT}/tables/_verification.json", "w"), indent=1)
