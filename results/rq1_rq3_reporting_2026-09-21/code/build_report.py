"""Fill REPORT_template.md placeholders {{TABLE:name}} with markdown tables rendered verbatim from tables/*.csv,
write REPORT.md, then check every 3-decimal and latency number quoted in the narrative against the table cells
and derived JSON. Unmatched numbers are listed in report_number_check.json (and the build fails)."""
import csv, os, re, json, sys
# Package directory (.../results/rq1_rq3_reporting_2026-09-21), derived from this file's location.
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(OUT, "tables")
MACH = {"pub_003": "Heba", "pub_007": "Heba", "pub_008": "Heba", "pub_011": "Heba"}
def machine(src):
    ms = sorted({MACH.get(s[:7], "Aya") for s in src.split("/")}); return "+".join(ms)
VIEWS = {
 "rq1": [("model", "Model"), ("strategy", "Strategy"), ("acc_conditional", "Acc. (cond.)"), ("acc_effective", "Acc. (eff.)"),
         ("macro_precision", "Macro-P"), ("macro_recall", "Macro-R"), ("macro_f1", "Macro-F1"), ("evaluability", "Evaluability"),
         ("valid_over_attributable_5runs", "Valid / attrib. (Σ5)"), ("invalid_per_run", "Model-invalid per run")],
 "rq2": [("model", "Model"), ("strategy", "Strategy"), ("acc_conditional", "Acc. (cond.)"), ("acc_effective", "Acc. (eff.)"),
         ("macro_f1", "Macro-F1"), ("acc_cond_minus_baseline", "Δ cond. − base"), ("acc_eff_minus_baseline", "Δ eff. − base"),
         ("runs_acc_cond_above_baseline", "Runs > base (cond.)"), ("runs_acc_eff_above_baseline", "Runs > base (eff.)"),
         ("evaluability", "Evaluability"), ("model_invalid_5runs", "Model-invalid (Σ5)")],
 "rq3": [("model", "Model"), ("strategy", "Strategy"), ("client_latency_mean_s", "Client mean (s)"),
         ("client_latency_median_s", "Client median (s)"), ("client_latency_p90_s", "Client p90 (s)"),
         ("server_latency_mean_s", "Server mean (s)"), ("n_llm_served_5runs", "n (Σ5)"),
         ("retried_assessments_5runs", "Retried (Σ5)"), ("_machine", "Machine*"),
         ("share_during_other_run_on_same_machine", "Share during other run"), ("executed_utc", "Executed (UTC)")],
 "pc_go": None, "pc_dr": None}
def render(name):
    rows = list(csv.DictReader(open(os.path.join(T, name + ".csv"))))
    key = "rq1" if name.startswith("rq1") else "rq2" if name in ("rq2_dreaddit", "rq2_goemotions") else "rq3" if name.startswith("rq3") else None
    if name == "rq2_goemotions_per_class":
        cols = [("model", "Model"), ("strategy", "Strategy")] + [(c + "_recall", c + " recall") for c in
                ("anxiety", "fear", "sadness", "frustration", "non_distress")] + [("non_distress_pred_share", "non_distress predicted share")]
    elif name == "rq2_dreaddit_per_class":
        cols = [("model", "Model"), ("strategy", "Strategy"), ("class0_recall", "Recall (0 = not stressed)"), ("class0_f1", "F1 (0)"),
                ("class1_recall", "Recall (1 = stressed)"), ("class1_f1", "F1 (1)"), ("class1_pred_share", "Predicted share of 1")]
    elif key is None:
        cols = [(c, c.replace("_", " ")) for c in rows[0]]
    else:
        cols = VIEWS[key]
    for r in rows: r["_machine"] = machine(r.get("source_run", ""))
    out = ["| " + " | ".join(h for _, h in cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    last = None
    for r in rows:
        cells = [r[c] for c, _ in cols]
        if cells[0] == last: cells[0] = ""
        else: last = cells[0]
        out.append("| " + " | ".join(str(x) for x in cells) + " |")
    return "\n".join(out), rows
tpl = open(os.path.join(OUT, "REPORT_template.md"), encoding="utf-8").read()
pool = set()
def fill(m):
    md, rows = render(m.group(1))
    for r in rows:
        for v in r.values(): pool.update(re.findall(r"-?\d+\.\d+", str(v)))
    return md
report = re.sub(r"\{\{TABLE:([a-z0-9_]+)\}\}", fill, tpl)
for f in ("tables/rq2_goemotions_per_class.csv", "tables/rq2_dreaddit_per_class.csv"):
    for r in csv.DictReader(open(os.path.join(OUT, f))):
        for v in r.values(): pool.update(re.findall(r"-?\d+\.\d+", v))
def walk(o):
    if isinstance(o, dict): [walk(v) for v in o.values()]
    elif isinstance(o, list): [walk(v) for v in o]
    elif isinstance(o, str): pool.update(re.findall(r"-?\d+\.\d+", o))
    elif isinstance(o, float):
        pool.add("%.3f" % o); pool.add("%.2f" % o)
for j in ("rq1_metric_ranks.json", "rq3_strategy_means_by_model.json"): walk(json.load(open(os.path.join(OUT, j))))
fp = json.load(open(os.path.join(OUT, "rq12_full_precision.json")))["baselines"]
walk(fp)
per_cell = json.load(open(os.path.join(OUT, "rq3_latency_per_cell.json")))["per_cell"]
for c in per_cell.values(): pool.add("%.2f" % c["mean_s"]); pool.add("%.2f" % c["median_s"])
narr = re.sub(r"\{\{TABLE:[a-z0-9_]+\}\}", "", tpl)
narr = re.sub(r"`[^`]*`", "", narr)            # ignore code spans (hashes, file names)
nums = re.findall(r"(?<![\w.])(-?\d+\.\d{2,3})(?![\d])", narr)
EXEMPT = set(json.load(open(os.path.join(OUT, "report_exempt_numbers.json")))) if os.path.exists(os.path.join(OUT, "report_exempt_numbers.json")) else set()
unmatched = sorted({n for n in nums if n not in pool and n.lstrip("-") not in pool and n not in EXEMPT})
json.dump({"numbers_checked": len(nums), "unmatched": unmatched, "exempt_used": sorted(EXEMPT & set(nums))},
          open(os.path.join(OUT, "report_number_check.json"), "w"), indent=1)
print("numbers checked", len(nums), "unmatched", unmatched)
if unmatched: sys.exit("UNMATCHED NUMBERS - REPORT.md not written")
open(os.path.join(OUT, "REPORT.md"), "w", encoding="utf-8").write(report)
print("REPORT.md written")
