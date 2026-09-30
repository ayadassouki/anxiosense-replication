"""RQ3 step 1 - READ-ONLY latency audit of the saved raw records behind the frozen grid.

Inputs (read-only): results/descriptive_2026-09-21/{frozen_grid_manifest_public.json, authoritative_records.jsonl}
                    and, for each of the 10 source runs, raw/attempts.jsonl + raw/index.jsonl.
The raw files are sha256-checked against the frozen manifest BEFORE use; any mismatch aborts.
Also reads only timestamps from every other run directory on the same storage location, to detect
overlapping (concurrent) execution. Writes only into results/rq1_rq3_reporting_2026-09-21/.
Stdlib only. No network. No model calls."""
import json, os, re, hashlib, glob, collections, sys, datetime as dt
# Repo-relative roots, derived from this file's location.
OUT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES  = os.path.dirname(OUT)                      # <repo>/results
REPO = os.path.dirname(RES)                      # <repo>
F = os.path.join(RES, "descriptive_2026-09-21")
# Raw run evidence lives outside the public repository (see PROVENANCE.md); point RUNS at a
# local copy of external_run_evidence to re-run this step. Machine attribution for each run is
# preserved in rq3_extract_summary.json (overlap_check, activity_windows) and in REPORT.md.
RUNS = os.environ.get("ANXIOSENSE_RUNS_ROOT", os.path.join(REPO, "external_run_evidence"))
fm = json.load(open(os.path.join(F, "frozen_grid_manifest_public.json")))

def local(p):  # manifest run_dir ('external_run_evidence/<run>') -> local raw-evidence path
    return os.path.join(RUNS, os.path.basename(p.rstrip("/")))
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def ts(s): return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()

summary = {"hash_checks": {}, "abort": None}
# 1. authoritative terminal attempts, by source run
auth = collections.defaultdict(dict)
for line in open(os.path.join(F, "authoritative_records.jsonl"), encoding="utf-8"):
    r = json.loads(line)
    auth[r["source_run"]][r["terminal_attempt_uuid"]] = (r["cell_id"], r["sample_id"], r["final_outcome_class"])
assert sum(len(v) for v in auth.values()) == 100350

TIMING_KEY = re.compile(r"(latenc|_ms$|ms$|timing|duration|elapsed|started|finished|time)", re.I)
key_inventory = collections.Counter()
out_rows = []
per_run = {}
for run, src in sorted(fm["sources"].items()):
    rd = local(src["run_dir"])
    a_p, i_p = os.path.join(rd, "raw/attempts.jsonl"), os.path.join(rd, "raw/index.jsonl")
    ha, hi = sha(a_p), sha(i_p)
    ok = ha == src["raw_attempts_sha256"] and hi == src["raw_index_sha256"]
    summary["hash_checks"][run] = {"attempts_sha256_ok": ha == src["raw_attempts_sha256"],
                                   "index_sha256_ok": hi == src["raw_index_sha256"], "run_dir": rd}
    if not ok:
        summary["abort"] = f"raw hash mismatch for {run}"; break
    want = auth[run]
    # index: map terminal uuid -> list of attempt uuids of that assessment
    term_attempts = {}
    for line in open(i_p, encoding="utf-8"):
        r = json.loads(line)
        if r.get("terminal_attempt_uuid") in want:
            term_attempts[r["terminal_attempt_uuid"]] = r.get("attempts") or [r["terminal_attempt_uuid"]]
    needed = set(want)
    for lst in term_attempts.values(): needed.update(lst)
    att = {}
    n_lines = 0
    for line in open(a_p, encoding="utf-8"):
        n_lines += 1
        r = json.loads(line)
        u = r["attempt_uuid"]
        # key inventory over every attempt of this run (top level + response_body.metadata)
        for k in r:
            if TIMING_KEY.search(k): key_inventory[("attempt", k)] += 1
        md = ((r.get("response_body") or {}).get("metadata") or {})
        for k in md:
            if TIMING_KEY.search(k): key_inventory[("response_body.metadata", k)] += 1
        for k in (r.get("response_body") or {}):
            if TIMING_KEY.search(k): key_inventory[("response_body", k)] += 1
        if u in needed:
            tu = r.get("token_usage") or {}
            att[u] = {"latency_ms": r.get("latency_ms"), "server_latency_ms": r.get("server_latency_ms"),
                      "poll_ms": r.get("mastra_poll_interval_ms"), "timestamp_utc": r.get("timestamp_utc"),
                      "http_status": r.get("http_status"), "outcome_class": r.get("outcome_class"),
                      "safety_override": r.get("safety_override"),
                      "input_tokens": tu.get("input_tokens"), "output_tokens": tu.get("output_tokens"),
                      "upstream_provider": r.get("upstream_provider")}
    missing_term = [u for u in want if u not in att]
    for u, (cid, sid, foc) in want.items():
        t = att.get(u, {})
        lst = term_attempts.get(u, [u])
        lat_all = [att.get(x, {}).get("latency_ms") for x in lst]
        out_rows.append({"cell_id": cid, "sample_id": sid, "source_run": run, "terminal_attempt_uuid": u,
                         "final_outcome_class": foc, "n_attempts": len(lst),
                         "latency_ms": t.get("latency_ms"), "server_latency_ms": t.get("server_latency_ms"),
                         "latency_ms_all_attempts_sum": (sum(lat_all) if all(v is not None for v in lat_all) else None),
                         "poll_ms": t.get("poll_ms"), "timestamp_utc": t.get("timestamp_utc"),
                         "http_status": t.get("http_status"), "terminal_outcome_class": t.get("outcome_class"),
                         "safety_override": t.get("safety_override"),
                         "input_tokens": t.get("input_tokens"), "output_tokens": t.get("output_tokens"),
                         "upstream_provider": t.get("upstream_provider")})
    per_run[run] = {"attempt_lines": n_lines, "terminal_attempts": len(want),
                    "terminal_attempts_missing_in_raw": len(missing_term),
                    "assessments_with_index_attempt_list": len(term_attempts)}
    print(run, per_run[run], flush=True)

if summary["abort"]:
    json.dump(summary, open(os.path.join(OUT, "rq3_extract_summary.json"), "w"), indent=1); sys.exit(summary["abort"])

# 2. concurrency check: active intervals of every run dir on each storage location (timestamps only)
TS = re.compile(r'"timestamp_utc": "([^"]+)"')
def intervals(path, gap=600):
    t = []
    for line in open(path, encoding="utf-8", errors="replace"):
        m = TS.search(line)
        if m: t.append(ts(m.group(1)))
    t.sort(); iv = []
    for x in t:
        if iv and x - iv[-1][1] <= gap: iv[-1][1] = x
        else: iv.append([x, x])
    return iv, len(t)
# ---------------------------------------------------------------------------------------------
# Storage/machine provenance: a HISTORICAL FACT about how these runs were collected, NOT a
# property of the directory layout shipped in this replication package.
#
# When the experiments were executed the raw evidence lived in two separate places: Aya's
# working repository (evaluation/publication_experiments/runs) and a USB copy of Heba's laptop
# (publication_experiments_from_second_machine/runs). The original version of this script determined each
# run's location by globbing those two roots, so "location" meant "which physical store this
# run folder was found in".
#
# The public package distributes ALL raw evidence under a single directory
# (external_run_evidence/), so that two-root split no longer exists on disk and the location is
# not recoverable from any path available here. It is also NOT a function of the run id: nine
# bench_* runs and pub_004 were on the USB despite not matching any pub_00{3,7,8,11} pattern.
# The mapping below is therefore carried as explicit provenance data, transcribed verbatim from
# activity_windows[*].location in the frozen results/rq1_rq3_reporting_2026-09-21/
# rq3_extract_summary.json written by the original two-root run. Do not derive it from run ids.
#
# See PROVENANCE.md and the REPORT.md note: "Machine is inferred from where the run folder is
# stored." A run absent from the frozen record is labelled "unknown" so that it can never be
# silently grouped onto a machine it was not observed on.
RUN_STORAGE_LOCATION = {
    "bench_002_google_gemma-4-31b-it": "heba_usb",
    "bench_002_qwen_qwen3.5-27b": "aya_repo",
    "bench_003_official_dreaddit_qwen": "aya_repo",
    "bench_004_official_dreaddit_qwen": "aya_repo",
    "bench_005_poll250_dreaddit_qwen": "aya_repo",
    "bench_006_goemotions_scale_qwen": "aya_repo",
    "bench_007_llama_smoke_heba": "heba_usb",
    "bench_009_phi_smoke": "aya_repo",
    "bench_009_phi_smoke_aborted_mistral": "aya_repo",
    "bench_010_gemma_heba_smoke": "heba_usb",
    "bench_010_goemotions715_mistral_smoke": "aya_repo",
    "bench_011_goemotions715_qwen_smoke": "heba_usb",
    "bench_012_goemotions715_llama_smoke": "aya_repo",
    "bench_012_goemotions715_phi_smoke": "heba_usb",
    "bench_013_dreaddit_gemma_fp4_reliability": "heba_usb",
    "bench_014_dreaddit_gemma_fp4_recheck": "heba_usb",
    "bench_015_gemma_fp4_aya_recheck": "aya_repo",
    "bench_016_dreaddit_gemma_fp4_coreweave": "heba_usb",
    "bench_017_dreaddit_gemma_fp4_coreweave_w2": "heba_usb",
    "pub_001_dreaddit_qwen": "aya_repo",
    "pub_002_dreaddit_mistral": "aya_repo",
    "pub_003_dreaddit_llama": "heba_usb",
    "pub_004_dreaddit_gemma": "heba_usb",
    "pub_005_dreaddit_phi": "aya_repo",
    "pub_006_goemotions715_mistral": "aya_repo",
    "pub_007_goemotions715_qwen": "heba_usb",
    "pub_008_goemotions715_phi": "heba_usb",
    "pub_009_goemotions715_llama": "aya_repo",
    "pub_010_goemotions715_gemma": "aya_repo",
    "pub_011_dreaddit_gemma_coreweave": "heba_usb",
    "pub_012_goemotions715_gemma_coreweave": "aya_repo",
    "pub_013_dreaddit_gemma_coreweave_osc_run5": "aya_repo",
    "smoke_001": "aya_repo",
}

def storage_location(run):  # historical storage/machine label for a run id (provenance lookup)
    return RUN_STORAGE_LOCATION.get(run, "unknown")

locs = {"external_run_evidence": RUNS}
activity = {}
for loc, d in locs.items():
    for rd in sorted(glob.glob(os.path.join(d, "*/raw/attempts.jsonl"))):
        name = rd.split("/")[-3]; iv, n = intervals(rd)
        activity[name] = {"location": storage_location(name), "n_attempts": n, "intervals": iv}
run_loc = {run: storage_location(run) for run in fm["sources"]}
overlap = {}
for run in fm["sources"]:
    others = [(n, a) for n, a in activity.items() if a["location"] == run_loc[run] and n != run]
    rows = [r for r in out_rows if r["source_run"] == run and r["timestamp_utc"]]
    hit = collections.Counter(); per_cell_hit = collections.Counter(); per_cell_n = collections.Counter()
    for r in rows:
        x = ts(r["timestamp_utc"]); cell = r["cell_id"]; per_cell_n[cell] += 1; any_hit = False
        for n, a in others:
            if any(s <= x <= e for s, e in a["intervals"]): hit[n] += 1; any_hit = True
        if any_hit: per_cell_hit[cell] += 1
    overlap[run] = {"location_inferred_from_storage": run_loc[run], "terminal_attempts": len(rows),
                    "terminal_attempts_during_other_run_activity": sum(per_cell_hit.values()),
                    "by_other_run": dict(hit),
                    "cells_affected": {c: [per_cell_hit[c], per_cell_n[c]] for c in sorted(per_cell_n) if per_cell_hit[c]}}

with open(os.path.join(OUT, "rq3_terminal_latency_records.jsonl"), "w") as f:
    for r in sorted(out_rows, key=lambda r: (r["cell_id"], r["sample_id"])): f.write(json.dumps(r, sort_keys=True) + "\n")
summary.update({"per_run": per_run, "rows_written": len(out_rows),
                "timing_key_inventory": {f"{a}:{k}": v for (a, k), v in sorted(key_inventory.items())},
                "overlap_check": overlap,
                "activity_windows": {n: {"location": a["location"], "n_attempts": a["n_attempts"],
                                         "n_intervals": len(a["intervals"]),
                                         "first_utc": dt.datetime.utcfromtimestamp(a["intervals"][0][0]).isoformat() if a["intervals"] else None,
                                         "last_utc": dt.datetime.utcfromtimestamp(a["intervals"][-1][1]).isoformat() if a["intervals"] else None}
                                     for n, a in activity.items()}})
json.dump(summary, open(os.path.join(OUT, "rq3_extract_summary.json"), "w"), indent=1, default=str)
print("DONE", len(out_rows))
