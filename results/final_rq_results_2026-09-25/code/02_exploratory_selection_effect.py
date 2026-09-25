"""EXPLORATORY, NOT PART OF THE FROZEN INFERENTIAL PACKAGE.

Question: are model-invalid outputs disproportionately drawn from the majority class, so
that conditional accuracy (which drops them) is optimistically biased?

Method: for each dataset x model x strategy, compare the ground-truth class composition of
the invalid records (from the invalid-output audit) with the class composition of the
attributable item pool (from the frozen dataset manifest / authoritative records). Reports
the majority-class share among invalids, the expected share, a chi-square-free exact
binomial two-sided p-value, and the arithmetic conditional-vs-effective accuracy gap.

No frozen artifact is modified and nothing here is added to the frozen Holm families.
The p-values below are EXPLORATORY and carry no multiplicity correction.
"""
import json, os, csv, collections, math

REPO = os.environ["REPO"]; OUT = os.environ["OUT"]
RES = f"{REPO}/evaluation/publication_experiments/results"
DESC = f"{RES}/descriptive_2026-09-21"
AUD = f"{RES}/invalid_output_audit_2026-09-25"
REP = f"{RES}/rq1_rq3_reporting_2026-09-21"
FP = json.load(open(f"{REP}/rq12_full_precision.json"))
SHORT = {"google/gemma-4-31b-it": "Gemma 4 31B", "meta-llama/llama-4-scout": "Llama 4 Scout",
         "mistralai/mistral-small-2603": "Mistral Small 4", "microsoft/phi-4": "Phi-4",
         "qwen/qwen3.5-27b": "Qwen3.5 27B"}
MAJORITY = {"dreaddit": 1, "goemotions": "non_distress"}

# attributable item pool composition, from the frozen authoritative records (one run each)
pool = collections.defaultdict(collections.Counter)
seen = set()
for line in open(f"{DESC}/authoritative_records.jsonl", encoding="utf-8"):
    r = json.loads(line)
    if r["failure_class"] == "SAFETY_INTERCEPT":
        continue
    k = (r["dataset"], r["sample_id"])
    if k in seen: continue
    seen.add(k); pool[r["dataset"]][r["ground_truth"]] += 1

inv = collections.defaultdict(collections.Counter)
for line in open(f"{AUD}/invalid_outputs_row_level.jsonl", encoding="utf-8"):
    r = json.loads(line)
    inv[(r["dataset"], r["model_short"], r["strategy"])][r["ground_truth"]] += 1

def binom_two_sided(k, n, p):
    """Exact two-sided binomial p-value (method of small p-values)."""
    if n == 0: return ""
    def pmf(i): return math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
    obs = pmf(k)
    return min(1.0, sum(pmf(i) for i in range(n + 1) if pmf(i) <= obs * (1 + 1e-12)))

rows = []
for ds in ["dreaddit", "goemotions"]:
    tot = sum(pool[ds].values())
    p_maj = pool[ds][MAJORITY[ds]] / tot
    for mid, m in SHORT.items():
        for st in ["zero-shot", "zero-shot-cot", "one-shot-cot"]:
            c = inv[(ds, m, st)]; n = sum(c.values())
            a = FP["aggregates"][f"{ds}|{mid}|{st}"]
            gap = a["acc_cond"]["mean"]["float"] - a["acc_eff"]["mean"]["float"]
            k = c[MAJORITY[ds]]
            rows.append({
                "dataset": ds, "model": m, "strategy": st,
                "n_invalid_5runs": n,
                "majority_class": str(MAJORITY[ds]),
                "pool_majority_share": round(p_maj, 4),
                "invalid_majority_share": round(k / n, 4) if n else "",
                "invalid_majority_count": k,
                "enrichment_ratio": round((k / n) / p_maj, 3) if n else "",
                "exploratory_binomial_p_two_sided": f"{binom_two_sided(k, n, p_maj):.3e}" if n else "",
                "acc_cond_mean": round(a["acc_cond"]["mean"]["float"], 4),
                "acc_eff_mean": round(a["acc_eff"]["mean"]["float"], 4),
                "acc_cond_minus_acc_eff": round(gap, 4),
                "evaluability_mean": round(a["evaluability"]["mean"]["float"], 4),
                "class_counts_of_invalids": json.dumps(dict(sorted(c.items(), key=lambda x: str(x[0])))),
            })
# Holm correction ACROSS THE 30 EXPLORATORY TESTS ONLY. This is a separate, clearly
# labelled family; it is NOT added to, and does not alter, any frozen Holm family.
tested = [r for r in rows if r["exploratory_binomial_p_two_sided"] != ""]
order = sorted(tested, key=lambda r: float(r["exploratory_binomial_p_two_sided"]))
mtot = len(order); running = 0.0
for i, r in enumerate(order):
    adj = min(1.0, float(r["exploratory_binomial_p_two_sided"]) * (mtot - i))
    running = max(running, adj)
    r["exploratory_p_holm_within_this_family"] = f"{running:.3e}"
    r["exploratory_holm_significant_0.05"] = str(running < 0.05)
for r in rows:
    r.setdefault("exploratory_p_holm_within_this_family", "")
    r.setdefault("exploratory_holm_significant_0.05", "")
    # composition of the pool that SURVIVES into conditional accuracy, per run
    n = r["n_invalid_5runs"]
    if n:
        att = 699 if r["dataset"] == "dreaddit" else 622
        maj_att = 355 if r["dataset"] == "dreaddit" else 487
        inv_run = n / 5.0; inv_maj_run = r["invalid_majority_count"] / 5.0
        surv = att - inv_run
        r["valid_pool_majority_share_per_run"] = round((maj_att - inv_maj_run) / surv, 4) if surv > 0 else ""
        r["majority_share_shift_valid_minus_pool"] = round(
            (maj_att - inv_maj_run) / surv - r["pool_majority_share"], 4) if surv > 0 else ""
    else:
        r["valid_pool_majority_share_per_run"] = ""
        r["majority_share_shift_valid_minus_pool"] = ""

cols = list(rows[0].keys())
with open(f"{OUT}/tables/exploratory_invalid_class_composition.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
print("EXPLORATORY table written:", len(rows), "rows")
print("\npool majority share:", {ds: round(pool[ds][MAJORITY[ds]] / sum(pool[ds].values()), 4)
                                 for ds in pool}, "\n")
hdr = "%-11s %-16s %-14s %6s %8s %8s %6s %10s %10s %5s %8s %8s"
print(hdr % ("dataset", "model", "strategy", "nInv", "majShare", "expected", "ratio", "explor.p",
             "p_holm", "sig", "validMaj", "cond-eff"))
for r in sorted(rows, key=lambda r: -(r["n_invalid_5runs"])):
    if r["n_invalid_5runs"] < 10: continue
    print(hdr % (r["dataset"], r["model"], r["strategy"], r["n_invalid_5runs"],
                 r["invalid_majority_share"], r["pool_majority_share"], r["enrichment_ratio"],
                 r["exploratory_binomial_p_two_sided"], r["exploratory_p_holm_within_this_family"],
                 r["exploratory_holm_significant_0.05"], r["valid_pool_majority_share_per_run"],
                 r["acc_cond_minus_acc_eff"]))
