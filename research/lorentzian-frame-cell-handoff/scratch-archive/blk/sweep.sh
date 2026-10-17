#!/bin/bash
# EVAL-mode sweep of build_blk.py options on blkpartA.pkl (R estimate = helpers + feeders + 11 totals)
cd /home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lbuild
for PAIR in 0 1 2; do for PCH in 0 1; do for QM in 0 1; do for SEEDL in 0 1; do for MP in 0 1; do for PF in none max; do
  env EVAL=1 PAIR=$PAIR PCHAIN=$PCH QMERGE=$QM QALL=$QM PIECES=paar HOP=0 MP=$MP SEEDL=$SEEDL PFRAME=$PF \
    timeout 900 python3 build_blk.py blkpartA.pkl /dev/null 2>/dev/null | grep EVAL | sed "s/^/PAIR=$PAIR PCH=$PCH QM=$QM SEEDL=$SEEDL MP=$MP PF=$PF /"
done; done; done; done; done; done
