"""Verify this repository's distributed subset of the 2026-09-21 descriptive freeze.

The 2026-09-21 attestation (verification_2026-09-21/freeze_hashes_after.txt) covers the complete
32-file descriptive_2026-09-21 package and is NOT modified by this script. The source working tree
in which the freeze was taken still verifies against it at 32 exact / 0 changed / 0 missing.

This repository distributes an intentional, sanitised SUBSET. Every inventory entry must fall into
exactly one of three expected buckets; anything else is a real finding and fails the check.

    EXACT       present and byte-identical to the inventory                      expected  9
    SANITISED   source_parse_summaries/<run>.json whose recorded size AND sha256
                are reproduced by restoring run_dir from frozen_grid_manifest.json
                and removing one trailing newline                                expected 11
    ABSENT      parsed/<run>.jsonl, not distributed for size, plus
                frozen_grid_manifest.json, not distributed for privacy (its
                sanitised public derivative frozen_grid_manifest_public.json
                ships in its place)                                              expected 12
    UNEXPLAINED anything else                                                    expected 0

See results/DISTRIBUTION_NOTE.md. Read-only; stdlib only. Exit 0 on pass, 1 on failure.
"""
import hashlib, json, os, sys

VER  = os.path.dirname(os.path.abspath(__file__))
RES  = os.path.dirname(VER)
DESC = os.path.join(RES, "descriptive_2026-09-21")
FZ_A = os.path.join(VER, "freeze_hashes_after.txt")
FZ_B = os.path.join(VER, "freeze_hashes_before.txt")
DINV = os.path.join(VER, "freeze_hashes_distributed.txt")

FREEZE_SHA256 = "5567988b1fd708fa4a81808c36b728f8a5fa471ffa2822a79d3830d41927ece5"
EXPECT = {"EXACT": 9, "SANITISED": 11, "ABSENT": 12, "UNEXPLAINED": 0}
ABSENT_BYTES = 161691042
NL = chr(10).encode()

sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
strip = lambda p: p[2:] if p.startswith("./") else p
checks = []
def chk(label, good, detail=""):
    checks.append((label, bool(good), detail))

def parse(path):
    out = []
    for line in open(path, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        f = line.split()
        if len(f) >= 3 and len(f[0]) == 64 and f[1].isdigit():
            out.append((f[0].lower(), int(f[1]), strip(f[2])))
    return out

# --- the attestation itself must be untouched ---------------------------------------------------
chk("freeze_hashes_after.txt unmodified", sha(FZ_A) == FREEZE_SHA256, sha(FZ_A))
chk("freeze_hashes_before.txt identical to after",
    open(FZ_A, "rb").read() == open(FZ_B, "rb").read())

recs = parse(FZ_A)
chk("32 inventory entries", len(recs) == 32, f"{len(recs)}")

DSTAT, DHASH = {}, {}
for _l in open(DINV, encoding="utf-8"):
    if _l.startswith("#") or not _l.strip():
        continue
    _f = _l.split()
    if len(_f) >= 3 and len(_f[0]) == 64 and _f[1].isdigit():
        DHASH[strip(_f[2])] = (_f[0].lower(), int(_f[1]))
        DSTAT[strip(_f[2])] = _f[3].lower() if len(_f) > 3 else ""
PRIVATE = {r for r, s in DSTAT.items() if s == "absent-private"}

# The unredacted grid manifest is withheld from public distribution (privacy: 11 absolute run_dir
# paths). When it is present the sanitised summaries are proved by reconstruction; when it is not,
# they are verified against their documented distributed hashes. Both modes fail on anything
# unexplained, and the mode used is printed.
_pm = os.path.join(DESC, "frozen_grid_manifest.json")
priv = json.load(open(_pm, encoding="utf-8"))["sources"] if os.path.isfile(_pm) else None
MODE = ("full reconstruction from the unredacted grid manifest" if priv is not None
        else "documented distributed hashes (unredacted grid manifest not distributed)")

# --- partition ----------------------------------------------------------------------------------
buckets = {k: [] for k in EXPECT}
field_diffs, absent_bytes = [], 0
for h, size, rel in recs:
    fp = os.path.join(DESC, rel)
    if rel in PRIVATE:
        # counted absent in EVERY environment so the partition is identical in a public clone and
        # in the author's tree; still verified against the inventory when the original is present
        if (not os.path.isfile(fp)) or (sha(fp) == h and os.path.getsize(fp) == size):
            buckets["ABSENT"].append(rel); absent_bytes += size
        else:
            buckets["UNEXPLAINED"].append(f"{rel} (private original present but altered)")
        continue
    if not os.path.isfile(fp):
        if rel.startswith("parsed/") and rel.endswith(".jsonl"):
            buckets["ABSENT"].append(rel); absent_bytes += size
        else:
            buckets["UNEXPLAINED"].append(f"{rel} (absent, not a parsed/ intermediate)")
        continue
    if sha(fp) == h and os.path.getsize(fp) == size:
        buckets["EXACT"].append(rel); continue
    run = os.path.basename(rel)[:-5]
    if rel.startswith("source_parse_summaries/") and priv is not None and run in priv:
        cur = open(fp, "rb").read()
        pub = ("external_run_evidence/" + run).encode()
        if pub in cur:
            restored = cur.replace(pub, priv[run]["run_dir"].encode())
            if restored.endswith(NL):
                restored = restored[:-1]
            if hashlib.sha256(restored).hexdigest() == h and len(restored) == size:
                buckets["SANITISED"].append(rel)
                # independent: every field except run_dir must be equal
                a = json.loads(cur); b = json.loads(restored)
                if {k: v for k, v in a.items() if k != "run_dir"} != \
                   {k: v for k, v in b.items() if k != "run_dir"}:
                    field_diffs.append(rel)
                continue
    dh = DHASH.get(rel)
    if (rel.startswith("source_parse_summaries/") and DSTAT.get(rel) == "sanitised"
            and dh and (sha(fp), os.path.getsize(fp)) == dh):
        buckets["SANITISED"].append(rel); continue
    buckets["UNEXPLAINED"].append(rel)

for k, want in EXPECT.items():
    chk(f"{k} == {want}", len(buckets[k]) == want, f"{len(buckets[k])}")
for u in buckets["UNEXPLAINED"]:
    chk(f"UNEXPLAINED entry: {u}", False)

chk("no non-run_dir field differs in any sanitised summary", not field_diffs, str(field_diffs))
chk(f"absent recorded bytes == {ABSENT_BYTES:,}", absent_bytes == ABSENT_BYTES, f"{absent_bytes:,}")
chk("every absent entry is a parsed/*.jsonl intermediate or the documented private manifest",
    all((p.startswith("parsed/") and p.endswith(".jsonl")) or p in PRIVATE for p in buckets["ABSENT"]))

# --- the derived distributed inventory ------------------------------------------------------------
dist = parse(DINV)
present = set(buckets["EXACT"]) | set(buckets["SANITISED"])
chk("distributed inventory has 21 entries (20 shipped + 1 documented private)",
    len(dist) == 21, f"{len(dist)}")
chk("distributed inventory covers exactly the present files plus the documented private entry",
    {r for _, _, r in dist} == present | PRIVATE)
bad_dist = [r for h, s, r in dist
            if r not in PRIVATE
            and not (os.path.isfile(os.path.join(DESC, r))
                    and sha(os.path.join(DESC, r)) == h
                    and os.path.getsize(os.path.join(DESC, r)) == s)]
chk("every distributed-inventory entry verifies", not bad_dist, str(bad_dist))

# --- the source tree, when reachable --------------------------------------------------------------
SRC = os.path.expanduser("~/anxiosense/evaluation/publication_experiments/results")
src_desc = os.path.join(SRC, "descriptive_2026-09-21")
src_inv = os.path.join(SRC, "verification_2026-09-21", "freeze_hashes_after.txt")
if os.path.isfile(src_inv) and os.path.isdir(src_desc):
    e = c = m = 0
    for h, size, rel in parse(src_inv):
        fp = os.path.join(src_desc, rel)
        if not os.path.isfile(fp): m += 1
        elif sha(fp) == h: e += 1
        else: c += 1
    chk("source working tree still verifies 32 exact / 0 changed / 0 missing",
        (e, c, m) == (32, 0, 0), f"exact={e} changed={c} missing={m}")
else:
    print("NOTE: source working tree not reachable; its 32/32 attestation was not re-checked here.")

# --- report ----------------------------------------------------------------------------------------
print("verify_distributed_subset - descriptive_2026-09-21")
print("  sanitised-summary verification mode: " + MODE)
print("  EXACT      %2d" % len(buckets["EXACT"]))
print("  SANITISED  %2d" % len(buckets["SANITISED"]))
print("  ABSENT     %2d  (%s bytes, intentionally not distributed)"
      % (len(buckets["ABSENT"]), format(absent_bytes, ",")))
print("  UNEXPLAINED %1d" % len(buckets["UNEXPLAINED"]))
print()
for label, good, detail in checks:
    print(("  PASS " if good else "  FAIL ") + label + (f"   [{detail}]" if detail else ""))
allgood = all(g for _, g, _ in checks)
print()
print("PASS - the distributed subset matches the 2026-09-21 freeze exactly as documented."
      if allgood else "FAIL - unexpected difference; see results/DISTRIBUTION_NOTE.md.")
sys.exit(0 if allgood else 1)
