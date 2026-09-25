"""Build the final RQ reporting tables from the frozen artifacts. READ-ONLY outside OUT.

Every value is copied or arithmetically derived from a frozen file; nothing is recomputed
under a different metric policy. Sources:

  rq1_rq3_reporting_2026-09-21/rq12_full_precision.json   five-run means (exact fractions)
                                                          and SDs (60-digit decimals),
                                                          evaluability, invalid rate, baselines
  inferential_2026-09-21/tables/configuration_level_ci.csv          per-config bootstrap CIs
  inferential_2026-09-21/tables/rq2_configuration_vs_baseline.csv   RQ2 tests
  inferential_2026-09-21/tables/rq1_model_pairs_primary.csv         RQ1 pairwise tests
  inferential_2026-09-21/tables/rq1_model_pairs_mcnemar.csv         RQ1 McNemar
  rq1_rq3_reporting_2026-09-21/tables/rq3_*_latency.csv             latency
  invalid_output_audit_2026-09-25/invalid_outputs_row_level.jsonl   invalid counts
"""
import json, os, csv, collections

REPO = os.environ["REPO"]; OUT = os.environ["OUT"]
RES = f"{REPO}/evaluation/publication_experiments/results"
REP = f"{RES}/rq1_rq3_reporting_2026-09-21"
INF = f"{RES}/inferential_2026-09-21/tables"
AUD = f"{RES}/invalid_output_audit_2026-09-25"
os.makedirs(f"{OUT}/tables", exist_ok=True)

FP = json.load(open(f"{REP}/rq12_full_precision.json"))
AGG, BASE = FP["aggregates"], FP["baselines"]
SHORT = {"google/gemma-4-31b-it": "Gemma 4 31B", "meta-llama/llama-4-scout": "Llama 4 Scout",
         "mistralai/mistral-small-2603": "Mistral Small 4", "microsoft/phi-4": "Phi-4",
         "qwen/qwen3.5-27b": "Qwen3.5 27B"}
MODELS = ["Gemma 4 31B", "Llama 4 Scout", "Mistral Small 4", "Phi-4", "Qwen3.5 27B"]
STRATS = ["zero-shot", "zero-shot-cot", "one-shot-cot"]
DATASETS = ["dreaddit", "goemotions"]
ATT_PER_RUN = {"dreaddit": 699, "goemotions": 622}

def rd(x, n=4):
    return "" if x in (None, "") else f"{float(x):.{n}f}"

def load(p):
    return list(csv.DictReader(open(p, encoding="utf-8")))

cfg_ci = {(r["dataset"], r["model"], r["strategy"]): r for r in load(f"{INF}/configuration_level_ci.csv")}
rq2 = {(r["dataset"], r["model"], r["strategy"]): r for r in load(f"{INF}/rq2_configuration_vs_baseline.csv")}
pairs = load(f"{INF}/rq1_model_pairs_primary.csv")
mcn = load(f"{INF}/rq1_model_pairs_mcnemar.csv")
lat = {}
for ds, f in [("dreaddit", "rq3_dreaddit_latency.csv"), ("goemotions", "rq3_goemotions_latency.csv")]:
    for r in load(f"{REP}/tables/{f}"):
        lat[(ds, r["model"], r["strategy"])] = r

inv = collections.Counter()
for l in open(f"{AUD}/invalid_outputs_row_level.jsonl", encoding="utf-8"):
    r = json.loads(l); inv[(r["dataset"], r["model_short"], r["strategy"])] += 1

PROV = []
def prov(result, ds, model, strategy, metric, value, src, loc):
    PROV.append({"reported_result": result, "dataset": ds, "model": model, "strategy": strategy,
                 "metric": metric, "value": value, "source_file": src, "source_field_or_location": loc})

def agg(ds, model, strat):
    mid = [k for k, v in SHORT.items() if v == model][0]
    return AGG[f"{ds}|{mid}|{strat}"], mid

# Holm-significant win/loss tallies per configuration, derived from the frozen pairwise table.
wins = collections.Counter(); losses = collections.Counter()
for r in pairs:
    if r["holm_significant_0.05"] != "True":
        continue
    hi, lo = (r["model_A"], r["model_B"]) if float(r["diff_A_minus_B"]) > 0 else (r["model_B"], r["model_A"])
    wins[(r["dataset"], hi, r["strategy"], r["metric"])] += 1
    losses[(r["dataset"], lo, r["strategy"], r["metric"])] += 1

RQ1_COLS = ["dataset", "model", "strategy", "n_attributable_per_run", "n_attributable_5runs",
            "acc_eff_mean", "acc_eff_sd", "acc_eff_ci_low", "acc_eff_ci_high",
            "acc_cond_mean", "acc_cond_sd", "acc_cond_ci_low", "acc_cond_ci_high",
            "macro_f1_mean", "macro_f1_sd", "macro_f1_ci_low", "macro_f1_ci_high",
            "macro_p_mean", "macro_r_mean",
            "evaluability_mean", "evaluability_sd", "invalid_rate_mean",
            "model_invalid_records_5runs", "safety_intercepts_5runs",
            "majority_baseline_frozen_scalar", "majority_baseline_attributable",
            "client_latency_mean_s", "client_latency_median_s",
            "holm_sig_pairwise_wins_acc_eff", "holm_sig_pairwise_losses_acc_eff",
            "holm_sig_pairwise_wins_macro_f1", "holm_sig_pairwise_losses_macro_f1"]

def rq1_rows(ds):
    rows = []
    for m in MODELS:
        for st in STRATS:
            a, mid = agg(ds, m, st)
            c = cfg_ci[(ds, m, st)]
            L = lat.get((ds, m, st), {})
            b = BASE[ds]
            row = {
                "dataset": ds, "model": m, "strategy": st,
                "n_attributable_per_run": ATT_PER_RUN[ds], "n_attributable_5runs": a["sum_N_attributable"],
                "acc_eff_mean": rd(a["acc_eff"]["mean"]["float"]), "acc_eff_sd": rd(a["acc_eff"]["sd"]["float"]),
                "acc_eff_ci_low": rd(c["acc_eff_ci_low"]), "acc_eff_ci_high": rd(c["acc_eff_ci_high"]),
                "acc_cond_mean": rd(a["acc_cond"]["mean"]["float"]), "acc_cond_sd": rd(a["acc_cond"]["sd"]["float"]),
                "acc_cond_ci_low": rd(c["acc_cond_ci_low"]), "acc_cond_ci_high": rd(c["acc_cond_ci_high"]),
                "macro_f1_mean": rd(a["macro_f1"]["mean"]["float"]), "macro_f1_sd": rd(a["macro_f1"]["sd"]["float"]),
                "macro_f1_ci_low": rd(c["macro_f1_ci_low"]), "macro_f1_ci_high": rd(c["macro_f1_ci_high"]),
                "macro_p_mean": rd(a["macro_p"]["mean"]["float"]), "macro_r_mean": rd(a["macro_r"]["mean"]["float"]),
                "evaluability_mean": rd(a["evaluability"]["mean"]["float"]),
                "evaluability_sd": rd(a["evaluability"]["sd"]["float"]),
                "invalid_rate_mean": rd(a["invalid_rate"]["mean"]["float"]),
                "model_invalid_records_5runs": a["sum_N_model_invalid"],
                "safety_intercepts_5runs": a["sum_N_safety"],
                "majority_baseline_frozen_scalar": rd(b["frozen"], 6),
                "majority_baseline_attributable": rd(b["attributable_majority_rate"]["float"], 6),
                "client_latency_mean_s": L.get("client_latency_mean_s", ""),
                "client_latency_median_s": L.get("client_latency_median_s", ""),
                "holm_sig_pairwise_wins_acc_eff": wins[(ds, m, st, "acc_eff")],
                "holm_sig_pairwise_losses_acc_eff": losses[(ds, m, st, "acc_eff")],
                "holm_sig_pairwise_wins_macro_f1": wins[(ds, m, st, "macro_f1")],
                "holm_sig_pairwise_losses_macro_f1": losses[(ds, m, st, "macro_f1")],
            }
            rows.append(row)
            src = "rq1_rq3_reporting_2026-09-21/rq12_full_precision.json"
            for met, key in [("acc_eff_mean", "acc_eff"), ("acc_cond_mean", "acc_cond"),
                             ("macro_f1_mean", "macro_f1"), ("evaluability_mean", "evaluability"),
                             ("invalid_rate_mean", "invalid_rate")]:
                prov(f"RQ1/RQ2/RQ3 {met}", ds, m, st, met, row[met], src,
                     f"aggregates['{ds}|{mid}|{st}']['{key}']['mean']['float']")
            prov("RQ1 acc_eff 95% CI", ds, m, st, "acc_eff_ci",
                 f"[{row['acc_eff_ci_low']}, {row['acc_eff_ci_high']}]",
                 "inferential_2026-09-21/tables/configuration_level_ci.csv",
                 "acc_eff_ci_low / acc_eff_ci_high")
            prov("RQ1 macro_f1 95% CI", ds, m, st, "macro_f1_ci",
                 f"[{row['macro_f1_ci_low']}, {row['macro_f1_ci_high']}]",
                 "inferential_2026-09-21/tables/configuration_level_ci.csv",
                 "macro_f1_ci_low / macro_f1_ci_high")
            prov("Invalid records (5 runs)", ds, m, st, "model_invalid_records_5runs",
                 row["model_invalid_records_5runs"], src,
                 f"aggregates['{ds}|{mid}|{st}']['sum_N_model_invalid']")
            if L:
                prov("Latency client mean (s)", ds, m, st, "client_latency_mean_s",
                     row["client_latency_mean_s"],
                     f"rq1_rq3_reporting_2026-09-21/tables/rq3_{ds}_latency.csv", "client_latency_mean_s")
    return rows

for ds in DATASETS:
    rows = rq1_rows(ds)
    with open(f"{OUT}/tables/rq1_{ds}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=RQ1_COLS); w.writeheader(); w.writerows(rows)
    print(f"tables/rq1_{ds}.csv: {len(rows)} rows")

# ── RQ2: configuration vs majority baseline (frozen tests, copied) ──────────────
RQ2_COLS = ["dataset", "model", "strategy", "n_items",
            "acc_eff", "acc_eff_ci_low", "acc_eff_ci_high",
            "macro_f1", "macro_f1_ci_low", "macro_f1_ci_high",
            "majority_baseline_attributable", "diff_vs_baseline", "diff_ci_low", "diff_ci_high",
            "p_perm", "p_holm", "holm_significant_0.05", "direction",
            "mcnemar_p_exact", "mcnemar_p_holm", "mcnemar_holm_significant_0.05",
            "sensitivity_frozen_scalar", "sensitivity_diff_vs_frozen_scalar",
            "sensitivity_ci_low", "sensitivity_ci_high",
            "evaluability_mean", "invalid_rate_mean", "model_invalid_records_5runs",
            "acc_eff_5run_sd", "macro_f1_5run_sd"]
rq2_rows = []
for ds in DATASETS:
    for m in MODELS:
        for st in STRATS:
            r = rq2[(ds, m, st)]; c = cfg_ci[(ds, m, st)]; a, mid = agg(ds, m, st)
            row = {"dataset": ds, "model": m, "strategy": st, "n_items": r["n_items"],
                   "acc_eff": rd(r["acc_eff"]), "acc_eff_ci_low": rd(r["acc_eff_ci_low"]),
                   "acc_eff_ci_high": rd(r["acc_eff_ci_high"]),
                   "macro_f1": rd(c["macro_f1"]), "macro_f1_ci_low": rd(c["macro_f1_ci_low"]),
                   "macro_f1_ci_high": rd(c["macro_f1_ci_high"]),
                   "majority_baseline_attributable": rd(r["baseline_attributable"], 6),
                   "diff_vs_baseline": rd(r["diff_vs_baseline"]), "diff_ci_low": rd(r["ci_low"]),
                   "diff_ci_high": rd(r["ci_high"]),
                   "p_perm": f"{float(r['p_perm']):.2e}", "p_holm": f"{float(r['p_holm']):.2e}",
                   "holm_significant_0.05": r["holm_significant_0.05"], "direction": r["direction"],
                   "mcnemar_p_exact": f"{float(r['mc_p_exact']):.2e}",
                   "mcnemar_p_holm": f"{float(r['mc_p_holm']):.2e}",
                   "mcnemar_holm_significant_0.05": r["mc_holm_significant_0.05"],
                   "sensitivity_frozen_scalar": rd(r["sens_frozen_scalar"], 6),
                   "sensitivity_diff_vs_frozen_scalar": rd(r["sens_diff_vs_frozen_scalar"]),
                   "sensitivity_ci_low": rd(r["sens_ci_low"]), "sensitivity_ci_high": rd(r["sens_ci_high"]),
                   "evaluability_mean": rd(a["evaluability"]["mean"]["float"]),
                   "invalid_rate_mean": rd(a["invalid_rate"]["mean"]["float"]),
                   "model_invalid_records_5runs": a["sum_N_model_invalid"],
                   "acc_eff_5run_sd": rd(a["acc_eff"]["sd"]["float"]),
                   "macro_f1_5run_sd": rd(a["macro_f1"]["sd"]["float"])}
            rq2_rows.append(row)
            prov("RQ2 vs baseline (Holm)", ds, m, st, "p_holm", row["p_holm"],
                 "inferential_2026-09-21/tables/rq2_configuration_vs_baseline.csv", "p_holm")
            prov("RQ2 vs baseline decision", ds, m, st, "holm_significant_0.05",
                 row["holm_significant_0.05"],
                 "inferential_2026-09-21/tables/rq2_configuration_vs_baseline.csv",
                 "holm_significant_0.05 / direction")
            prov("RQ2 majority baseline (attributable items)", ds, "(all)", "(all)",
                 "baseline_attributable", row["majority_baseline_attributable"],
                 "inferential_2026-09-21/tables/rq2_configuration_vs_baseline.csv", "baseline_attributable")
with open(f"{OUT}/tables/rq2_summary.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=RQ2_COLS); w.writeheader(); w.writerows(rq2_rows)
print("tables/rq2_summary.csv:", len(rq2_rows), "rows")

# ── RQ3: strategy comparison, DESCRIPTIVE. Deltas are arithmetic, not tests. ────
def strat_table(metric, mean_key, ci_lo, ci_hi, fname):
    cols = ["dataset", "model", "strategy", f"{metric}_mean", f"{metric}_5run_sd",
            f"{metric}_ci_low", f"{metric}_ci_high",
            f"delta_vs_zero_shot_{metric}", "rank_within_model",
            "ci_overlaps_zero_shot_ci_within_model", "strategy_difference_statistically_tested"]
    rows = []
    for ds in DATASETS:
        for m in MODELS:
            vals = {}
            for st in STRATS:
                a, _ = agg(ds, m, st); c = cfg_ci[(ds, m, st)]
                vals[st] = (float(a[mean_key]["mean"]["float"]), float(a[mean_key]["sd"]["float"]),
                            float(c[ci_lo]), float(c[ci_hi]))
            order = sorted(STRATS, key=lambda s: -vals[s][0])
            z = vals["zero-shot"]
            for st in STRATS:
                v = vals[st]
                overlap = not (v[3] < z[2] or v[2] > z[3])
                rows.append({"dataset": ds, "model": m, "strategy": st,
                             f"{metric}_mean": rd(v[0]), f"{metric}_5run_sd": rd(v[1]),
                             f"{metric}_ci_low": rd(v[2]), f"{metric}_ci_high": rd(v[3]),
                             f"delta_vs_zero_shot_{metric}": rd(v[0] - z[0]),
                             "rank_within_model": order.index(st) + 1,
                             "ci_overlaps_zero_shot_ci_within_model":
                                 "n/a (reference)" if st == "zero-shot" else str(overlap).lower(),
                             "strategy_difference_statistically_tested": "NO"})
    with open(f"{OUT}/tables/{fname}", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    print(f"tables/{fname}: {len(rows)} rows")
    return rows

strat_table("acc_eff", "acc_eff", "acc_eff_ci_low", "acc_eff_ci_high", "rq3_accuracy.csv")
strat_table("macro_f1", "macro_f1", "macro_f1_ci_low", "macro_f1_ci_high", "rq3_macro_f1.csv")

# ── RQ3 inferential availability: what the frozen package does and does not test ─
RQ3I_COLS = ["dataset", "strategy", "metric", "frozen_family", "n_hypotheses_in_family",
             "n_pairs_this_strategy", "n_raw_p_lt_0.05", "n_ci_excludes_zero", "n_holm_significant",
             "min_p_holm", "what_this_tests", "strategy_vs_strategy_test_available"]
rq3i = []
for ds in DATASETS:
    for st in STRATS:
        for met in ["acc_eff", "macro_f1"]:
            sel = [r for r in pairs if r["dataset"] == ds and r["strategy"] == st and r["metric"] == met]
            rq3i.append({
                "dataset": ds, "strategy": st, "metric": met,
                "frozen_family": sel[0]["family"], "n_hypotheses_in_family": sel[0]["family_size"],
                "n_pairs_this_strategy": len(sel),
                "n_raw_p_lt_0.05": sum(1 for r in sel if float(r["p_perm"]) < 0.05),
                "n_ci_excludes_zero": sum(1 for r in sel
                                          if float(r["ci_low"]) > 0 or float(r["ci_high"]) < 0),
                "n_holm_significant": sum(1 for r in sel if r["holm_significant_0.05"] == "True"),
                "min_p_holm": f"{min(float(r['p_holm']) for r in sel):.2e}",
                "what_this_tests": "model-vs-model WITHIN this strategy",
                "strategy_vs_strategy_test_available": "NONE in the frozen inferential package"})
        s = [r for r in mcn if r["dataset"] == ds and r["strategy"] == st]
        rq3i.append({"dataset": ds, "strategy": st, "metric": "majority_vote_correctness (McNemar)",
                     "frozen_family": s[0]["family"], "n_hypotheses_in_family": s[0]["family_size"],
                     "n_pairs_this_strategy": len(s), "n_raw_p_lt_0.05": sum(1 for r in s if float(r["p_exact"]) < 0.05),
                     "n_ci_excludes_zero": "", "n_holm_significant": sum(1 for r in s if r["holm_significant_0.05"] == "True"),
                     "min_p_holm": f"{min(float(r['p_holm']) for r in s):.2e}",
                     "what_this_tests": "model-vs-model WITHIN this strategy (secondary)",
                     "strategy_vs_strategy_test_available": "NONE in the frozen inferential package"})
with open(f"{OUT}/tables/rq3_inferential.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=RQ3I_COLS); w.writeheader(); w.writerows(rq3i)
print("tables/rq3_inferential.csv:", len(rq3i), "rows")

# ── latency ─────────────────────────────────────────────────────────────────────
LAT_COLS = ["dataset", "model", "strategy", "client_latency_mean_s", "client_latency_median_s",
            "client_latency_p90_s", "server_latency_mean_s", "n_llm_served_5runs",
            "n_safety_excluded_5runs", "missing_latency", "retried_assessments_5runs",
            "executed_utc", "source_run", "share_during_other_run_on_same_machine",
            "measure_displayed", "units", "aggregation", "resolution_note"]
lat_rows = []
for ds in DATASETS:
    for m in MODELS:
        for st in STRATS:
            L = lat[(ds, m, st)]
            row = {k: L.get(k, "") for k in LAT_COLS if k in L}
            row.update({"dataset": ds, "model": m, "strategy": st,
                        "measure_displayed": "client end-to-end wall clock (latency_ms) around the HTTP POST "
                                             "to /api/workflow/evaluate",
                        "units": "seconds (converted from ms in the frozen table)",
                        "aggregation": "per-run mean/median/p90, then mean +/- sample SD over the 5 runs",
                        "resolution_note": "3 s Mastra poll quantisation; safety intercepts excluded"})
            lat_rows.append(row)
            prov("Latency client median (s)", ds, m, st, "client_latency_median_s",
                 row.get("client_latency_median_s", ""),
                 f"rq1_rq3_reporting_2026-09-21/tables/rq3_{ds}_latency.csv", "client_latency_median_s")
with open(f"{OUT}/tables/latency.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=LAT_COLS, extrasaction="ignore"); w.writeheader(); w.writerows(lat_rows)
print("tables/latency.csv:", len(lat_rows), "rows")

# ── provenance ──────────────────────────────────────────────────────────────────
for ds in DATASETS:
    b = BASE[ds]
    prov("Majority baseline (frozen scalar)", ds, "(all)", "(all)", "majority_baseline_frozen",
         rd(b["frozen"], 6), "rq1_rq3_reporting_2026-09-21/rq12_full_precision.json",
         f"baselines['{ds}']['frozen']")
for ds in DATASETS:
    for met in ["acc_eff", "macro_f1"]:
        sel = [r for r in pairs if r["dataset"] == ds and r["metric"] == met]
        prov("RQ1 Holm-significant model pairs", ds, "(all)", "(all)", f"n_holm_sig_{met}",
             sum(1 for r in sel if r["holm_significant_0.05"] == "True"),
             "inferential_2026-09-21/tables/rq1_model_pairs_primary.csv",
             f"rows with dataset={ds}, metric={met}, holm_significant_0.05=True (of {len(sel)})")
with open(f"{OUT}/result_provenance.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["reported_result", "dataset", "model", "strategy", "metric",
                                       "value", "source_file", "source_field_or_location"])
    w.writeheader(); w.writerows(PROV)
print("result_provenance.csv:", len(PROV), "rows")
