# Session 8 scripts (lever A on E8; HANDOFF.md section 3j)

These are working copies from the session scratch directory; their `sys.path` lines point there, so adjust the paths
to re-run them. The verified, self-contained versions are in `research/e8-bit-p111-r434/code/`: `census.py` combines
`loc.py`, `fastb.py`, `fastg.py`, `exh*.py`, `census2.py` and `combine.py`, and `gen_p4.py` and `tune434.py` are the
generator and tuner steps.

| script | role |
|---|---|
| `entcensus*.py` | E1-style entrance-conversion census (exact single-column dirt simulation; `ent434.log`: none on R = 434) |
| `loc.py` | block-local replica of gen_p3's helper accounting (validated 41/41 against full builds) |
| `fastb.py` | faster exact replica (2,000/2,000 against `loc.py`) |
| `fastg.py` | cell-sum generalisation, block cost max(\|E\|, junk) |
| `exh.py`, `exh2.py`, `gexh.py` | exhaustive per-block search for the shipped puncture set (gen_p3 / gen_p4 accounting) |
| `census2.py`, `combine.py` | all-subset census and the combination over 17,478 puncture sets |
| `lb.py`, `resid.py` | lower bounds and residual patterns (the cell-pair observation) |
| `o2mod.py` | D6 o1/o2 re-splits for the totals (needs leave the block: ruled out) |
| `bld.py`, `mkparams.py`, `tryg.py`, `samp437.py`, `sampg.py`, `blkprof.py`, `combo.py` | builds, sampling and profile scan |
| `plansearch.py` | screening of new L3 plans (not run yet) |
