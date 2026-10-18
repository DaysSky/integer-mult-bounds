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

## The copy bound at cst=72 (nat108b/c)

With the 9-gather W-solve scatter the B-phase must deliver all of perp(t) (63 lines) to every target.
- `../ii19_nat108b_covers.py`: the 8,821 line-spanned hyperplanes of a line's perp; two cover at most 52 of
  the 63 lines; the only covering triples are the 315 D4 4-frame triples (sections of size 30, root normals).
  So a line with 3 pure copies has them at the 3 cells of a D4 4-frame.
- `../ii19_nat108c_cellsides.py`: in all 1,200 cells checked, the 16 targets reachable only through the cell
  have common perp equal to the cell and need 2 sides. Two copies of the cell sum need a third register, so
  every cell holds at least 3 registers: 540 registers, R >= 420 (less a handful from targets reading at cells).
- At R420 shapes: R=420 -4.6%, 405 -2.6%, 360 +3.6%, 345 +5.9%, 274 +18.2%. The +17-42% class needs
  R ~ 174-274, below the bound.
