"""RQ3 step 2 - descriptive latency tables from rq3_terminal_latency_records.jsonl (produced by step 1
from hash-verified raw files). One latency value per authoritative assessment = the TERMINAL attempt's
client-measured latency_ms (runner wall-clock around POST /api/workflow/evaluate) and the server's
server_latency_ms (Express Date.now() delta for the same request). Safety-intercepted assessments are
excluded from the latency statistics (they short-circuit before any LLM/agent call) and counted separately.
Per run: mean, median, p90 over LLM-served terminal attempts. Five-run: mean and sample SD (n-1) of the
five per-run values. No pooling across models or datasets. Stdlib only."""
import json, os, csv, collections, statistics as S, math
from decimal import Decimal, ROUND_HALF_UP
# Package directory (.../results/rq1_rq3_reporting_2026-09-21), derived from this file's location.
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(OUT, "tables")
SHORT = {"google/gemma-4-31b-it": "Gemma 4 31B", "meta-llama/llama-4-scout": "Llama 4 Scout",
         "microsoft/phi-4": "Phi-4", "mistralai/mistral-small-2603": "Mistral Small 4", "qwen/qwen3.5-27b": "Qwen3.5 27B"}
STRATS = ["zero-shot", "zero-shot-cot", "one-shot-cot"]
summ = json.load(open(os.path.join(OUT, "rq3_extract_summary.json")))
conc = {}
for run, o in summ["overlap_check"].items():
    for c, (h, n) in o["cells_affected"].items(): conc[c] = (h, n)
recs = collections.defaultdict(list)
for l in open(os.path.join(OUT, "rq3_terminal_latency_records.jsonl")):
    recs[json.loads(l)["cell_id"]].append(json.loads(l))
assert len(recs) == 150 and sum(map(len, recs.values())) == 100350

def q(xs, p):  # nearest-rank percentile
    xs = sorted(xs); return xs[max(0, math.ceil(p * len(xs)) - 1)]
def r2(x): return str(Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
def msd(xs): return (S.fmean(xs), S.stdev(xs))
cell = {}
for cid, rs in recs.items():
    llm = [r for r in rs if r["final_outcome_class"] != "SAFETY_INTERCEPT"]
    lat = [r["latency_ms"] / 1000 for r in llm]; srv = [r["server_latency_ms"] / 1000 for r in llm]
    ts = sorted(r["timestamp_utc"] for r in rs)
    cell[cid] = {"n_llm": len(llm), "n_safety": len(rs) - len(llm), "missing_latency": sum(r["latency_ms"] is None for r in llm),
                 "mean_s": S.fmean(lat), "median_s": S.median(lat), "p90_s": q(lat, 0.9), "min_s": min(lat), "max_s": max(lat),
                 "server_mean_s": S.fmean(srv), "server_median_s": S.median(srv),
                 "retried_assessments": sum(r["n_attempts"] > 1 for r in rs),
                 "first_utc": ts[0], "last_utc": ts[-1], "source_run": rs[0]["source_run"],
                 "concurrent_other_run_share": (conc[cid][0] / conc[cid][1]) if cid in conc else 0.0,
                 "bucket_counts_s": dict(sorted(collections.Counter(int(round(x / 3.0)) * 3 for x in lat).items()))}
agg = {}
rows = collections.defaultdict(list)
for cid in sorted(cell):
    ds, mo, st, rn = cid.split("|"); agg.setdefault((ds, mo, st), []).append(cell[cid])
for (ds, mo, st), cs in agg.items():
    assert len(cs) == 5
    m_mean, s_mean = msd([c["mean_s"] for c in cs]); m_med, s_med = msd([c["median_s"] for c in cs])
    m_p90, s_p90 = msd([c["p90_s"] for c in cs]); m_srv, s_srv = msd([c["server_mean_s"] for c in cs])
    rows[ds].append({"model": SHORT[mo], "strategy": st,
                     "client_latency_mean_s": "%s ± %s" % (r2(m_mean), r2(s_mean)),
                     "client_latency_median_s": "%s ± %s" % (r2(m_med), r2(s_med)),
                     "client_latency_p90_s": "%s ± %s" % (r2(m_p90), r2(s_p90)),
                     "server_latency_mean_s": "%s ± %s" % (r2(m_srv), r2(s_srv)),
                     "n_llm_served_5runs": sum(c["n_llm"] for c in cs), "n_safety_excluded_5runs": sum(c["n_safety"] for c in cs),
                     "missing_latency": sum(c["missing_latency"] for c in cs),
                     "retried_assessments_5runs": sum(c["retried_assessments"] for c in cs),
                     "executed_utc": "%s → %s" % (min(c["first_utc"] for c in cs)[:16], max(c["last_utc"] for c in cs)[:16]),
                     "source_run": "/".join(sorted({c["source_run"] for c in cs})),
                     "share_during_other_run_on_same_machine": r2(S.fmean([c["concurrent_other_run_share"] for c in cs]))})
for ds in rows:
    order = {s: i for i, s in enumerate(STRATS)}
    rows[ds].sort(key=lambda r: (r["model"], order[r["strategy"]]))
    with open(os.path.join(T, "rq3_%s_latency.csv" % ds), "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[ds][0])); wr.writeheader(); wr.writerows(rows[ds])
json.dump({"per_cell": cell}, open(os.path.join(OUT, "rq3_latency_per_cell.json"), "w"), indent=1)
# within-model ordering of strategies by five-run mean latency (descriptive)
order_out = {}
for (ds, mo, st), cs in agg.items():
    order_out.setdefault(ds, {}).setdefault(SHORT[mo], {})[st] = round(S.fmean([c["mean_s"] for c in cs]), 4)
json.dump(order_out, open(os.path.join(OUT, "rq3_strategy_means_by_model.json"), "w"), indent=1)
for ds in rows:
    print(ds)
    for r in rows[ds]: print("  ", r["model"], r["strategy"], r["client_latency_mean_s"], r["client_latency_median_s"], r["server_latency_mean_s"], r["retried_assessments_5runs"], r["executed_utc"], r["share_during_other_run_on_same_machine"])
