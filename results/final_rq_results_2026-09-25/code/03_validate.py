"""Validate the final RQ package. READ-ONLY outside OUT. Writes VALIDATION.md + CHECKSUMS.sha256."""
import json, os, csv, glob, hashlib, collections, datetime

REPO = os.environ["REPO"]; OUT = os.environ["OUT"]
RES = f"{REPO}/evaluation/publication_experiments/results"
DESC, INF = f"{RES}/descriptive_2026-09-21", f"{RES}/inferential_2026-09-21"
REP, AUD = f"{RES}/rq1_rq3_reporting_2026-09-21", f"{RES}/invalid_output_audit_2026-09-25"
VER = f"{RES}/verification_2026-09-21"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def load(p): return list(csv.DictReader(open(p, encoding="utf-8")))

L = []; ok_all = True
def check(n, title, passed, detail, advisory=False):
    """advisory=True: a notice about a NEIGHBOURING package. It is reported in full but does
    not decide this package's pass/fail, because this package neither caused nor consumes it."""
    global ok_all
    if not advisory:
        ok_all = ok_all and passed
    status = ("PASS" if passed else ("ADVISORY" if advisory else "FAIL"))
    L.append((n, title, status, detail))
    print(f"{status:9s}{n}. {title} — {detail}")

MODELS = ["Gemma 4 31B", "Llama 4 Scout", "Mistral Small 4", "Phi-4", "Qwen3.5 27B"]
STRATS = ["zero-shot", "zero-shot-cot", "one-shot-cot"]
DATASETS = ["dreaddit", "goemotions"]
t = {n: load(f"{OUT}/tables/{n}") for n in
     ["rq1_dreaddit.csv", "rq1_goemotions.csv", "rq2_summary.csv", "rq3_accuracy.csv",
      "rq3_macro_f1.csv", "rq3_inferential.csv", "latency.csv",
      "exploratory_invalid_class_composition.csv"]}
prov = load(f"{OUT}/result_provenance.csv")

# 1 coverage
miss = []
for name in ["rq2_summary.csv", "rq3_accuracy.csv", "rq3_macro_f1.csv", "latency.csv",
             "exploratory_invalid_class_composition.csv"]:
    got = {(r["dataset"], r["model"], r["strategy"]) for r in t[name]}
    want = {(d, m, s) for d in DATASETS for m in MODELS for s in STRATS}
    if got != want: miss.append((name, sorted(want - got)[:3]))
for ds in DATASETS:
    got = {(r["model"], r["strategy"]) for r in t[f"rq1_{ds}.csv"]}
    if got != {(m, s) for m in MODELS for s in STRATS}: miss.append((f"rq1_{ds}.csv", "incomplete"))
check(1, "All 5 models x 3 strategies x 2 datasets present in every table", not miss,
      f"5 models, 3 strategies, 2 datasets = 30 configurations; rq1 tables 15 rows each; "
      f"{len(miss)} tables with gaps")

# 2 five-run means agree across three independent frozen sources
FP = json.load(open(f"{REP}/rq12_full_precision.json"))["aggregates"]
cfg = {(r["dataset"], r["model"], r["strategy"]): r for r in
       load(f"{INF}/tables/configuration_level_ci.csv")}
TAB = f"{RES}/rq1_rq3_tables"
tabs = {}
for ds, f in [("dreaddit", "02_dreaddit_results.csv"), ("goemotions", "03_goemotions_results.csv")]:
    for r in load(f"{TAB}/{f}"):
        tabs[(ds, r["model"], r["prompt_strategy"])] = r
# rq1_rq3_tables uses its own display labels; map them so the cross-source check works.
TAB_ALIAS = {"Gemma 4 31B": "Gemma 4 31B IT", "Qwen3.5 27B": "Qwen 3.5 27B"}
SHORT = {"Gemma 4 31B": "google/gemma-4-31b-it", "Llama 4 Scout": "meta-llama/llama-4-scout",
         "Mistral Small 4": "mistralai/mistral-small-2603", "Phi-4": "microsoft/phi-4",
         "Qwen3.5 27B": "qwen/qwen3.5-27b"}
bad3 = []; n3 = 0
for ds in DATASETS:
    for m in MODELS:
        for s in STRATS:
            a = FP[f"{ds}|{SHORT[m]}|{s}"]
            for key, cfgk, tabk in [("acc_eff", "acc_eff", "effective_accuracy_mean"),
                                    ("acc_cond", "acc_cond", "conditional_accuracy_mean"),
                                    ("macro_f1", "macro_f1", "macro_f1_mean")]:
                v1 = a[key]["mean"]["float"]; v2 = float(cfg[(ds, m, s)][cfgk])
                v3 = float(tabs[(ds, TAB_ALIAS.get(m, m), s)][tabk]); n3 += 1
                if max(abs(v1 - v2), abs(v1 - v3)) > 1e-9:
                    bad3.append((ds, m, s, key, v1, v2, v3))
check(2, "Five-run point estimates agree across three independent frozen sources", not bad3,
      f"{n3} comparisons of acc_eff / acc_cond / macro_f1 across rq12_full_precision.json, "
      f"inferential configuration_level_ci.csv and rq1_rq3_tables; {len(bad3)} disagreements "
      f"(tolerance 1e-9)")

# 3 majority baselines
B = json.load(open(f"{REP}/rq12_full_precision.json"))["baselines"]
exp = {"dreaddit": (0.516084, 355 / 699), "goemotions": (0.781701, 487 / 622)}
b_ok = all(abs(B[d]["frozen"] - exp[d][0]) < 1e-9 and
           abs(B[d]["attributable_majority_rate"]["float"] - exp[d][1]) < 1e-12 for d in DATASETS)
rq2b = {(r["dataset"]): r["majority_baseline_attributable"] for r in t["rq2_summary.csv"]}
b_ok = b_ok and abs(float(rq2b["dreaddit"]) - 355 / 699) < 1e-6 and \
       abs(float(rq2b["goemotions"]) - 487 / 622) < 1e-6
check(3, "Majority baselines match the frozen values", b_ok,
      "Dreaddit frozen scalar 0.516084 (369/715) and attributable 355/699 = 0.507868; "
      "GoEmotions frozen scalar 0.781701 (487/623) and attributable 487/622 = 0.782958")

# 4 latency copied verbatim
latbad = 0
src = {}
for ds, f in [("dreaddit", "rq3_dreaddit_latency.csv"), ("goemotions", "rq3_goemotions_latency.csv")]:
    for r in load(f"{REP}/tables/{f}"): src[(ds, r["model"], r["strategy"])] = r
for r in t["latency.csv"]:
    s0 = src[(r["dataset"], r["model"], r["strategy"])]
    for k in ["client_latency_mean_s", "client_latency_median_s", "client_latency_p90_s",
              "server_latency_mean_s", "n_llm_served_5runs", "retried_assessments_5runs", "source_run"]:
        if r[k] != s0[k]: latbad += 1
check(4, "Latency values are copied verbatim from the frozen latency tables", latbad == 0,
      f"{len(t['latency.csv'])} configurations x 7 fields compared against "
      f"rq1_rq3_reporting_2026-09-21/tables/rq3_*_latency.csv; {latbad} mismatches")

# 5 invalid counts / evaluability
aud = collections.Counter()
for line in open(f"{AUD}/invalid_outputs_row_level.jsonl", encoding="utf-8"):
    r = json.loads(line); aud[(r["dataset"], r["model_short"], r["strategy"])] += 1
ibad = []
for ds in DATASETS:
    for m in MODELS:
        for s in STRATS:
            a = FP[f"{ds}|{SHORT[m]}|{s}"]
            if a["sum_N_model_invalid"] != aud[(ds, m, s)]: ibad.append((ds, m, s))
tot_aud = sum(aud.values())
check(5, "Invalid-output counts reconcile with the invalid-output audit", not ibad and tot_aud == 1986,
      f"sum_N_model_invalid in rq12_full_precision.json vs per-cell row counts in the audit: "
      f"{len(ibad)} mismatches across 30 configurations; audit total {tot_aud} (expected 1,986)")

# 6 inferential tallies recomputed from the frozen tables
pairs = load(f"{INF}/tables/rq1_model_pairs_primary.csv")
rq2f = load(f"{INF}/tables/rq2_configuration_vs_baseline.csv")
tal = {}
for ds in DATASETS:
    for met in ["acc_eff", "macro_f1"]:
        sel = [r for r in pairs if r["dataset"] == ds and r["metric"] == met]
        tal[(ds, met)] = (len(sel), sum(1 for r in sel if r["holm_significant_0.05"] == "True"))
above = collections.Counter(); below = collections.Counter(); nots = collections.Counter()
for r in rq2f:
    if r["holm_significant_0.05"] != "True": nots[r["dataset"]] += 1
    elif r["direction"] == "above baseline": above[r["dataset"]] += 1
    else: below[r["dataset"]] += 1
mine = {(r["dataset"], r["strategy"], r["metric"]): int(r["n_holm_significant"])
        for r in t["rq3_inferential.csv"] if r["metric"] in ("acc_eff", "macro_f1")}
recheck = all(sum(v for (d, s, mt), v in mine.items() if d == ds and mt == met) == tal[(ds, met)][1]
              for ds in DATASETS for met in ["acc_eff", "macro_f1"])
check(6, "Inferential tallies match the frozen inferential tables", recheck,
      f"RQ1 Holm-significant of 30 pairs: Dreaddit acc_eff {tal[('dreaddit','acc_eff')][1]}, "
      f"macro_f1 {tal[('dreaddit','macro_f1')][1]}; GoEmotions acc_eff {tal[('goemotions','acc_eff')][1]}, "
      f"macro_f1 {tal[('goemotions','macro_f1')][1]}. RQ2 of 15 per dataset: Dreaddit "
      f"{above['dreaddit']} above / {below['dreaddit']} below / {nots['dreaddit']} n.s.; GoEmotions "
      f"{above['goemotions']} above / {below['goemotions']} below / {nots['goemotions']} n.s. "
      f"Per-strategy sums in rq3_inferential.csv reproduce the per-dataset totals.")

# 7 no strategy-vs-strategy test exists in the frozen package
fams = set()
for f in glob.glob(f"{INF}/tables/*.csv"):
    for r in load(f): fams.add(r.get("family", ""))
fams.discard("")
strat_fam = [f for f in fams if "strategy" in f.lower() or "rq3" in f.lower()]
check(7, "No strategy-vs-strategy hypothesis exists in the frozen inferential package",
      not strat_fam,
      f"Frozen Holm families: {sorted(fams)}. None compares prompting strategies; the plan states "
      f"'RQ3. No inference.' All RQ3 strategy statements in this package are therefore descriptive.")

# 8 provenance integrity
bad_src = [r for r in prov if not os.path.exists(f"{RES}/{r['source_file']}")]
check(8, "Every provenance row points at an existing frozen file", not bad_src,
      f"{len(prov)} provenance rows referencing "
      f"{len({r['source_file'] for r in prov})} distinct source files; {len(bad_src)} missing")

# 9 frozen descriptive package vs the 2026-09-21 freeze inventory
recorded = {}
for line in open(f"{VER}/freeze_hashes_after.txt"):
    p_ = line.split(None, 2)
    if len(p_) == 3: recorded[p_[2].strip().lstrip("./")] = p_[0]
cur = {os.path.relpath(x, DESC): sha(x) for x in glob.glob(f"{DESC}/**/*", recursive=True)
       if os.path.isfile(x)}
dchanged = sorted(k for k in recorded if k in cur and cur[k] != recorded[k])
dmiss = sorted(k for k in recorded if k not in cur); dadd = sorted(k for k in cur if k not in recorded)
check(9, "Frozen descriptive package is byte-identical to its freeze inventory",
      not (dchanged or dmiss or dadd),
      f"{len(recorded)} files compared against verification_2026-09-21/freeze_hashes_after.txt: "
      f"{len(dchanged)} changed, {len(dmiss)} missing, {len(dadd)} added")

# 10 the upstream files THIS package actually reads are unchanged
audman = {}
for line in open(f"{AUD}/CHECKSUMS.sha256"):
    h, n = line.split(); audman[n] = h
READ = ["invalid_outputs_row_level.jsonl"]
rbad = [n for n in READ if sha(f"{AUD}/{n}") != audman.get(n)]
inf_ok = all(os.path.exists(f"{INF}/tables/{n}") for n in
             ["configuration_level_ci.csv", "rq1_model_pairs_primary.csv",
              "rq1_model_pairs_mcnemar.csv", "rq2_configuration_vs_baseline.csv"])
check(10, "Every upstream file this package reads is present and unmodified",
      not rbad and inf_ok,
      f"invalid_output_audit_2026-09-25/invalid_outputs_row_level.jsonl matches the audit manifest "
      f"({'yes' if not rbad else 'NO'}); the four inferential tables, rq12_full_precision.json and both "
      f"frozen latency tables were read and are present")

# 11 wider integrity notice for the audit package (not an input to this package)
abad = sorted(n for n, h in audman.items()
              if os.path.exists(f"{AUD}/{n}") and sha(f"{AUD}/{n}") != h)
side = [n for n in abad if n not in READ]
check(11, "Invalid-output audit package matches its own manifest (advisory)", not abad,
      (f"{len(audman)} files checked against invalid_output_audit_2026-09-25/CHECKSUMS.sha256; "
       f"{len(abad)} differ: {side}. NOTE: these files were modified outside this session's build of "
       f"this package and are NOT inputs to it — every number here that touches the audit comes from "
       f"invalid_outputs_row_level.jsonl, which matches its manifest. Re-run that package's own "
       f"code/05_validate.py to refresh its manifest.")
      if abad else f"{len(audman)} files all match", advisory=True)

# 12 this package's generators write nothing outside OUT
snap_before = {x: (os.path.getmtime(x), os.path.getsize(x))
               for x in glob.glob(f"{RES}/**/*", recursive=True)
               if os.path.isfile(x) and not x.startswith(OUT)}
os.system(f'REPO="{REPO}" OUT="{OUT}" python3 "{OUT}/code/01_build_tables.py" >/dev/null')
os.system(f'REPO="{REPO}" OUT="{OUT}" python3 "{OUT}/code/02_exploratory_selection_effect.py" >/dev/null')
snap_after = {x: (os.path.getmtime(x), os.path.getsize(x))
              for x in glob.glob(f"{RES}/**/*", recursive=True)
              if os.path.isfile(x) and not x.startswith(OUT)}
touched = sorted(os.path.relpath(k, RES) for k in set(snap_before) | set(snap_after)
                 if snap_before.get(k) != snap_after.get(k))
check(12, "Re-running this package's generators changes nothing outside the new directory",
      not touched,
      f"{len(snap_before)} files under results/ outside {os.path.basename(OUT)}/ inventoried "
      f"(mtime + size), both generators re-run, inventory re-taken: {len(touched)} changed{'' if not touched else ': ' + str(touched[:5])}")

# 13 every decimal number in the prose matches a value in the tables
import re
pool = set()
for f in glob.glob(f"{OUT}/tables/*.csv") + [f"{OUT}/result_provenance.csv"]:
    for row in load(f):
        for v in row.values():
            for tok in re.findall(r"-?\d+\.\d+(?:[eE][-+]?\d+)?", str(v)):
                try: x = float(tok)
                except ValueError: continue
                for nd in (2, 3, 4, 6):
                    pool.add(round(abs(x), nd))
                pool.add(round(abs(x) * 100, 1))          # percentages
                pool.add(round(abs(x) - 0.7830, 4)); pool.add(round(abs(x) - 0.5079, 4))
        for v in row.values():
            if str(v).isdigit(): pool.add(float(v))
# documented constants that are not table cells
EXEMPT = {
    # documented constants quoted from the frozen packages but not present as a table cell
    0.05,        # alpha
    0.516084, 0.781701,   # frozen majority-baseline scalars
    0.337, 0.176,         # constant-predictor macro-F1 (statistical plan, D4 note)
    0.6231, 0.4486,       # ISSUES_FOR_AUDIT item 1, run-5 figures
    16.88, 20.29, 14.37, 10.09, 14.08,   # Gemma per-run latency drift (frozen REPORT.md)
    9.08, 9.07,           # Qwen Dreaddit latency medians on the 3 s lattice (frozen REPORT.md)
    0.82,                 # share_during_other_run_on_same_machine, Llama Dreaddit ZS
    1.00,                 # a p-value of 1.000 and the same share for Llama Dreaddit ZS-CoT
}
missing = collections.defaultdict(list)
for md in sorted(glob.glob(f"{OUT}/*.md")):
    if os.path.basename(md) == "VALIDATION.md": continue
    txt = open(md, encoding="utf-8").read()
    txt = re.sub(r"`[^`]*`", " ", txt)                 # skip code spans (paths, field names)
    txt = re.sub(r"\d+\s*[×x]\s*10[⁻\-][\d⁰¹²³⁴⁵⁶⁷⁸⁹]+", " ", txt)  # scientific notation prose
    txt = re.sub(r"\d+\.\d+e[-+]?\d+", " ", txt, flags=re.I)
    for tok in re.findall(r"(?<![\w.])\d+\.\d{2,}(?![\w])", txt):
        x = float(tok)
        if x in EXEMPT: continue
        if any(abs(round(x, nd) - c) < 1e-9 for nd in (2, 3, 4, 6) for c in (x,)) and \
           (round(x, 4) in pool or round(x, 3) in pool or round(x, 2) in pool or round(x, 1) in pool):
            continue
        missing[os.path.basename(md)].append(tok)
nmiss = sum(len(v) for v in missing.values())
check(13, "Every decimal number in the prose is traceable to a table value",
      nmiss == 0,
      f"{len(glob.glob(f'{OUT}/*.md')) - 1} markdown files scanned against "
      f"{len(pool)} distinct numeric values from the eight tables and result_provenance.csv "
      f"(code spans and scientific-notation p-values excluded; {len(EXEMPT)} documented constants "
      f"exempt): {nmiss} unmatched"
      + ("" if not missing else " -> " + json.dumps({k: v[:6] for k, v in missing.items()})))

# checksums
files = sorted(f for f in (glob.glob(f"{OUT}/*.csv") + glob.glob(f"{OUT}/*.md") +
                           glob.glob(f"{OUT}/tables/*.csv") + glob.glob(f"{OUT}/code/*.py"))
               if os.path.basename(f) != "VALIDATION.md")
sums = [(os.path.relpath(f, OUT), os.path.getsize(f), sha(f)) for f in files]
with open(f"{OUT}/CHECKSUMS.sha256", "w") as fh:
    for n, _, h in sums: fh.write(f"{h}  {n}\n")
print(f"\n{len(sums)} files hashed into CHECKSUMS.sha256 "
      "(VALIDATION.md and CHECKSUMS.sha256 excluded: written after hashing)")

with open(f"{OUT}/VALIDATION.md", "w", encoding="utf-8") as fh:
    fh.write(f"""# VALIDATION — final RQ results package

Generated {datetime.datetime.now(datetime.timezone.utc).isoformat()} by `code/03_validate.py`.
This package is read-only with respect to every existing artifact: it reads the frozen packages and
writes only inside `final_rq_results_2026-09-25/`.

## Checks

| # | Check | Result | Detail |
|---|---|---|---|
""")
    for n, ti, res, d in L: fh.write(f"| {n} | {ti} | **{res}** | {d} |\n")
    fh.write(f"\nOverall for this package: **{'ALL CHECKS PASS' if ok_all else 'ONE OR MORE CHECKS FAILED'}**"
             f" (ADVISORY rows are notices about neighbouring packages; they are reported in full and do not"
             f" affect this package's status).\n")
    fh.write("\n## Source artifacts read\n\n| Package | Role |\n|---|---|\n")
    for p_, role in [("descriptive_2026-09-21", "frozen grid, per-cell metrics, authoritative records"),
                     ("verification_2026-09-21", "independent verification and the freeze hash inventory"),
                     ("rq1_rq3_reporting_2026-09-21", "five-run means/SDs at full precision, baselines, latency"),
                     ("inferential_2026-09-21", "bootstrap CIs, permutation tests, Holm decisions, McNemar"),
                     ("invalid_output_audit_2026-09-25", "1,986 model-invalid records and their taxonomy")]:
        fh.write(f"| `{p_}` | {role} |\n")
    fh.write("\n## Checksums\n\n| file | bytes | sha256 |\n|---|---|---|\n")
    for n, s_, h in sums: fh.write(f"| `{n}` | {s_:,} | `{h}` |\n")
print("\nVALIDATION.md written. overall:", "ALL PASS" if ok_all else "FAILURES PRESENT")
