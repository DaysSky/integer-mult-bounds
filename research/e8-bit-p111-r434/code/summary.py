"""Compare every number verify.sh produced with EXPECTED.json and print the summary, with E1's and P111-tuned's nine-
and eleven-stage c from their EXPECTED.json files.  `--record` writes EXPECTED.json from the outputs instead (used
once, then reviewed).
usage: summary.py PACKAGE_DIR OUTPUT_DIR [--record]
Adapted from P111-tuned's tune/summary.py (PR #589); prepared by DaysSky with assistance from Claude; Apache-2.0."""
import gzip
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

H, W = Path(sys.argv[1]), Path(sys.argv[2])
record = "--record" in sys.argv[3:]
J = lambda p: json.loads(Path(p).read_text())  # noqa: E731
word_p = H / "data" / "bitE8mut-p111-r434.json.gz"
x, mp = J(W / "xcheck.json"), J(W / "mutants_p.json")
cc, k4, k5, lg = J(W / "cout/columns.json"), J(W / "cout/columns_k4.json"), J(W / "cout/columns_k5.json"), \
    J(W / "cout/legality.json")
r9, r11 = J(W / "RESULT9.json"), J(W / "RESULT11.json")
names = ("pr548", "pr544", "pr535", "pr531")
raw = json.loads(gzip.open(word_p, "rt").read())
content = hashlib.sha256(json.dumps(raw, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
e1 = J(H / ".." / "e8-bit-p111-e1" / "EXPECTED.json")
tu = J(H / ".." / "e8-bit-p111-tuned" / "tune" / "EXPECTED.json")


def chain(r):
    return dict(bit_lower=r["bit_lower"], bit_lower_decimal=r["bit_lower_decimal"], bit_profile=r["bit_profile"],
                bit=r["bit"], kappa={n: {f: r["kappa"][n][f] for f in ("kappa", "kappa_decimal", "complex_lower",
                                                                         "binding_component")} for n in names})


if record:
    base_p = H / "data" / "bitE8mut-p111-r434-base.json.gz"
    e = dict(word=dict(file="data/bitE8mut-p111-r434.json.gz", file_sha256=hashlib.sha256(word_p.read_bytes()).hexdigest(),
                       base_file="data/bitE8mut-p111-r434-base.json.gz",
                       base_file_sha256=hashlib.sha256(base_p.read_bytes()).hexdigest(),
                       content_sha256=content, v=raw["v"], R=raw["R"], punctured=raw["punctured"],
                       gates={k: len(raw[k]) for k in "DABC"}, stats=raw["stats"],
                       local_histogram={str(a): b for a, b in cc["local_raw_H"]},
                       legality={k: lg[k] for k in ("records", "common_frame_ADDs", "rank_mass")},
                       five_stage_columns=cc["formal_columns_checked"], five_stage_payload_bits=cc["payload_prefix_bits"],
                       nine_stage_columns=k4["formal_columns_checked"], nine_stage_payload_bits=k4["payload_prefix_bits"],
                       eleven_stage_columns=k5["formal_columns_checked"], eleven_stage_payload_bits=k5["payload_prefix_bits"]),
             interface={k: x[k] for k in ("hypotheses", "conclusion", "interleaving")},
             nine=chain(r9), eleven=chain(r11),
             baselines=dict(e1_nine=e1["nine"]["bit_lower"], e1_eleven=e1["eleven"]["bit_lower"],
                            p111_tuned_nine=tu["nine"]["bit_lower"], p111_tuned_eleven=tu["eleven"]["bit_lower"]))
    (H / "EXPECTED.json").write_text(json.dumps(e, indent=1) + "\n")
    print("   recorded", H / "EXPECTED.json")
    sys.exit(0)

e = J(H / "EXPECTED.json")
ew = e["word"]
assert content == ew["content_sha256"] and hashlib.sha256(word_p.read_bytes()).hexdigest() == ew["file_sha256"]
assert x["status"] == "PASS_EXACT_REPLAY_AND_INTERLEAVED_INTERFACE" and x["v"] == ew["v"] and x["punctured"] == 9
assert x["copy_ranks"] == [7] * 9 and x["totals_on_punctured_hyperplanes"]
for k in ("hypotheses", "conclusion", "interleaving"):
    assert x[k] == e["interface"][k], k
assert all(x["hypotheses"].values()) and all(x["conclusion"].values())
assert mp["all_rejected"] and len(mp["controls"]) == 4
assert {str(a): b for a, b in cc["local_raw_H"]} == ew["local_histogram"]
assert (cc["payload_prefix_bits"], k4["payload_prefix_bits"], k5["payload_prefix_bits"]) == \
    (ew["five_stage_payload_bits"], ew["nine_stage_payload_bits"], ew["eleven_stage_payload_bits"])
assert (cc["formal_columns_checked"], k4["formal_columns_checked"], k5["formal_columns_checked"]) == \
    (ew["five_stage_columns"], ew["nine_stage_columns"], ew["eleven_stage_columns"])
assert (lg["records"], lg["common_frame_ADDs"], lg["rank_mass"]) == tuple(ew["legality"][k] for k in
                                                                         ("records", "common_frame_ADDs", "rank_mass"))
assert lg["rank_mass"] == 8 * ew["R"] + 63 + 14 * ew["v"]
for key, r in (("nine", r9), ("eleven", r11)):
    assert chain(r) == e[key], key
c9, c11 = F(r9["bit_lower"]), F(r11["bit_lower"])
b = e["baselines"]
assert b["e1_nine"] == e1["nine"]["bit_lower"] and b["p111_tuned_nine"] == tu["nine"]["bit_lower"]
assert c9 > F(b["e1_nine"]) > F(b["p111_tuned_nine"]) and c11 > F(b["e1_eleven"])
for n in names:
    assert r9["kappa"][n]["binding_component"] == "complex"
p = lambda a, z: "%+.4f%%" % (100 * float(F(a) / F(z) - 1))  # noqa: E731
print("PASS bit c, nine stages (PR #510's chain parameterised by P111's adapt9p.py; discovered hosting, all %d residuals "
      "hosted whole, %d banks) = %s = %s" % (r9["bit"]["hosted_residuals"], r9["bit"]["bank_assignments"], r9["bit_lower"],
                                            r9["bit_lower_decimal"]))
print("     E1 (selected frontier before this package): %s (%s); P111-tuned: %s (%s)"
      % (e1["nine"]["bit_lower_decimal"], p(c9, b["e1_nine"]), tu["nine"]["bit_lower_decimal"], p(c9, b["p111_tuned_nine"])))
print("PASS bit c, eleven stages (PR #493's chain as parameterised by PR #545) = %s = %s" % (r11["bit_lower"],
                                                                                          r11["bit_lower_decimal"]))
print("     E1: %s (%s); P111-tuned: %s (%s)" % (e1["eleven"]["bit_lower_decimal"], p(c11, b["e1_eleven"]),
                                             tu["eleven"]["bit_lower_decimal"], p(c11, b["p111_tuned_eleven"])))
for n in names:
    kk = r9["kappa"][n]
    print("PASS kappa with PR #%s's complex b = %s: %s = %s (%s-bound, unchanged)"
          % (n[2:], kk["complex_lower"], kk["kappa"], kk["kappa_decimal"], kk["binding_component"]))
print("     local paid profile %s, R = %d (P111: 439)" % (ew["local_histogram"], ew["R"]))
