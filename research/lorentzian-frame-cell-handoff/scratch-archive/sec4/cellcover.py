"""Support availability: for each target t and s in R(t), can x_s reach t through some design section Q ∋ t via a
node (Q-perp ∩ Q2-perp, Q2 another design section, or a single cell) containing a SOURCE CELL C ∋ s with C inside it?
env DESIGN (sections), CELLS (source cells).  Reports uncovered (t,s) pairs (no slot count can fix those)."""
import os, json, collections
from common import *
Qp = {Q: perpmask(Q) for Q in planes}
CELLS = [int(h, 16) for h in json.load(open(os.environ['CELLS']))['planes']] if os.environ.get('CELLS') else planes
def avail(X):
    m = 0
    for C in CELLS:
        if C & ~X == 0: m |= C
    return m
secav = {}
for Q in planes:
    m = avail(Qp[Q])   # any cell inside Q-perp at all (single-section pre-mixer / single cell)
    mm = 0
    for Q2 in planes:
        if Q2 != Q: mm |= avail(Qp[Q] & Qp[Q2])
    for C in CELLS:
        if C & ~Qp[Q] == 0: mm |= C
    secav[Q] = (m, mm)
unc_multi = 0; unc_any = 0; tot = 0
for t in range(V):
    mine = [Q for Q in planes if Q >> t & 1]
    a_any = 0; a_multi = 0
    for Q in mine: a_any |= secav[Q][0]; a_multi |= secav[Q][1]
    R = e8.HYP[t]
    tot += pc(R); unc_any += pc(R & ~a_any); unc_multi += pc(R & ~a_multi)
print(os.environ.get('DESIGN'), os.environ.get('CELLS'), 'pairs', tot, 'uncovered (any cell in a section perp):', unc_any,
      ' uncovered (multi-section nodes / single cells):', unc_multi)
