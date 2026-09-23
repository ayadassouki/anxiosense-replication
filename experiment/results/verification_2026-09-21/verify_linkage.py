"""Independent verification, part 1: authoritative_records.jsonl <-> frozen grid manifest
<-> dataset manifests <-> parsed source files. Stdlib only; imports NOTHING from runner/.
Read-only on descriptive_2026-09-21 and manifests/."""
import json, os, hashlib, collections, sys
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
F = os.path.join(BASE, "results/descriptive_2026-09-21")
V = os.path.join(BASE, "results/verification_2026-09-21")
issues = []
def bad(msg): issues.append(msg)
def fsha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

fm = json.load(open(os.path.join(F, "frozen_grid_manifest_public.json")))
if not fm["validation"]["passed"]: bad("frozen manifest records validation not passed")

# dataset manifests: file hash + self-hash must match what the freeze recorded
dsman = {}
for ds, info in fm["manifests"].items():
    p = os.path.join(BASE, "manifests", info["file"])
    if fsha(p) != info["file_sha256"]: bad("%s manifest file sha changed" % ds)
    d = json.load(open(p)); dsman[ds] = d
    payload = {k: v for k, v in d.items() if k not in ("created_utc", "manifest_sha256")}
    rec = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()
    if rec != d["manifest_sha256"] or rec != info["manifest_sha256"]: bad("%s manifest self-hash mismatch" % ds)

# Parsed source files are private audit intermediates and are not distributed
# in the public replication package. If present, verify them against the
# freeze and use them for record-level source comparison. Otherwise, continue
# with all checks reproducible from the published artifacts.
parsed_by_uuid = {}
parsed_source_verification = True

for run, source_info in fm["sources"].items():
    parsed_path = os.path.join(F, "parsed", run + ".jsonl")
    if not os.path.exists(parsed_path):
        parsed_source_verification = False
        continue

    if fsha(parsed_path) != source_info["parsed_output_sha256"]:
        bad("parsed file hash changed: " + run)

    for line in open(parsed_path, encoding="utf-8"):
        r = json.loads(line)
        parsed_by_uuid[r["terminal_attempt_uuid"]] = r

# authoritative records
cells = collections.defaultdict(list); keys = set(); n = 0; bad_lines = 0
FIELDS = ("source_run","cell_id","dataset","model","strategy","run","sample_id","final_outcome_class",
          "ground_truth","parse_status","parsed_prediction","prediction_valid","failure_class",
          "failure_reason","include_in_metrics","upstream_provider")
for line in open(os.path.join(F, "authoritative_records.jsonl"), encoding="utf-8"):
    try: r = json.loads(line)
    except Exception: bad_lines += 1; continue
    n += 1
    cid = "%s|%s|%s|run%d" % (r["dataset"], r["model"], r["strategy"], r["run"])
    if cid != r["cell_id"]: bad("cell_id inconsistent with coordinates: %s" % r["cell_id"])
    k = (r["dataset"], r["model"], r["strategy"], r["run"], r["sample_id"])
    if k in keys: bad("duplicate key %s" % (k,))
    keys.add(k); cells[r["cell_id"]].append(r)
    if parsed_source_verification:
        src = parsed_by_uuid.get(r["terminal_attempt_uuid"])
        if src is None:
            bad("record not found in parsed source: %s" % r["terminal_attempt_uuid"])
        else:
            for f in FIELDS:
                if src.get(f) != r.get(f):
                    bad("field %s differs from parsed source for %s" % (f, r["terminal_attempt_uuid"]))
    M = dsman[r["dataset"]]
    if r["ground_truth"] != M["ground_truth"].get(r["sample_id"]): bad("ground truth != dataset manifest %s" % (k,))
    safe = r["final_outcome_class"] == "SAFETY_INTERCEPT"
    if safe != (r["failure_class"] == "SAFETY_INTERCEPT"): bad("safety flag inconsistency %s" % (k,))
    if bool(r["prediction_valid"]) != (r["parsed_prediction"] is not None): bad("prediction_valid vs prediction inconsistency %s" % (k,))
    if bool(r["include_in_metrics"]) != bool(r["prediction_valid"]): bad("include_in_metrics != prediction_valid %s" % (k,))

# cell-level comparison with the frozen manifest
mcells = fm["cells"]
if set(cells) != set(mcells): bad("cell sets differ: only_records=%d only_manifest=%d" % (len(set(cells)-set(mcells)), len(set(mcells)-set(cells))))
for cid, recs in cells.items():
    m = mcells.get(cid)
    if not m: continue
    ds = cid.split("|")[0]
    if len(recs) != m["n"] or m["n"] != m["expected_n"]: bad("%s n=%d manifest n=%s expected=%s" % (cid, len(recs), m["n"], m["expected_n"]))
    if {r["source_run"] for r in recs} != {m["source_run"]}: bad("%s source_run differs" % cid)
    if dict(collections.Counter(r["final_outcome_class"] for r in recs)) != m["final_outcomes"]: bad("%s final_outcomes differ" % cid)
    if dict(collections.Counter(r["parse_status"] for r in recs)) != m["parse_status"]: bad("%s parse_status differ" % cid)
    if sorted(r["sample_id"] for r in recs if r["final_outcome_class"] == "SAFETY_INTERCEPT") != m["safety_ids"]: bad("%s safety ids differ" % cid)
    h = hashlib.sha256("\n".join(sorted("%s|%s" % (r["sample_id"], r["terminal_attempt_uuid"]) for r in recs)).encode()).hexdigest()
    if h != m["records_sha256"]: bad("%s records_sha256 differs" % cid)
    if {r["sample_id"] for r in recs} != set(dsman[ds]["included_sample_ids"]): bad("%s sample set != dataset manifest" % cid)

# composition rule spot check for Gemma/Dreaddit
g = "dreaddit|google/gemma-4-31b-it|one-shot-cot|run5"
gsrc = {r["source_run"] for r in cells.get(g, [])}
other = {r["source_run"] for c, rs in cells.items() if c.startswith("dreaddit|google/gemma-4-31b-it|") and c != g for r in rs}

out = {"records": n, "bad_json_lines": bad_lines,
       "parsed_source_verification_performed": parsed_source_verification,
       "cells": len(cells), "manifest_cells": len(mcells),
       "manifest_totals": fm["totals"], "distinct_keys": len(keys),
       "gemma_replaced_cell_sources": sorted(gsrc), "gemma_other_cells_sources": sorted(other),
       "per_dataset_records": dict(collections.Counter(c.split("|")[0] for c, rs in cells.items() for _ in rs)),
       "issues": issues, "n_issues": len(issues)}
json.dump(out, open(os.path.join(V, "linkage_result.json"), "w"), indent=2)
print(json.dumps({k: v for k, v in out.items() if k != "issues"}, indent=1))
for i in issues[:30]: print("ISSUE:", i)
print("LINKAGE PASSED:", not issues)
