# ext120 = E8: the R420 control under gcheck

Scope note (not an II19 result). The "ext120" system of `../ii19_nat69_spec.json` is the E8 root-line
system: 120 lines, closed under reflections, form positive-definite (signature 8,0). It is the same line set
(up to sign) as the hub's E8 R420 word. That word is therefore an existing cst=72 ext120 word.

- `conv_r420.py`: converts `research/subspace16-r420/vendor/e8-bit-r420/data/bitE8mut-r420.json.gz`
  (bitE8/1+mut format) into the gcheck.py format (frames as spanning vectors, form {I, 2}, ret_frames by replay).
- `chains.py WORD.json`: per-role climb patterns of a gcheck-format word.
- `whatif.py`: pricer what-ifs on the R420 role shapes and R.

Reproduce (Python 3, numpy, mpmath):

    python3 conv_r420.py ../../subspace16-r420/vendor/e8-bit-r420/data/bitE8mut-r420.json.gz r420_gc.json
    python3 ../../lorentzian-frame-cell-handoff/code/tword/gcheck.py r420_gc.json --price

Result: PASS, v=120, h=8, R=420, cst=72, hist {1:1320, 2:1440, 4:60, 5:120, 8:9},
c = 0.001653826988146798944268 (-4.571% vs P111 0.001733052823330162099157), the published R420 value.

Observations: at R420 shapes the price crosses P111 near R=370 (R=360 gives +3.6%); each helper is worth
about +0.14%. Any design with the affine 9-gather decoder needs about 3 pure branches per line (two hyperplane
sections of an E7 never cover it), so about 240 carriers. The previous ext120 plan's "free source-fills,
at most 47 dups" assumption is below that bound.

## Open next questions
- This is E8, not the Lorentzian II19 target. Which II19 system to build (the 361-line h=10 system, or the
  240-line 2-class at h=10) is undecided.
