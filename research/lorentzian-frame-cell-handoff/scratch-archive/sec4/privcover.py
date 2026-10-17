"""Combinatorial screen (cell-routed middle, no in-chain help): for each design section Q, the union of its users'
private lines must be covered by <= |Q| supports, each = design cells inside a node X = Q-perp ∩ Q'-perp (Q' another
design section) or a single design cell inside Q-perp.  Exact min set cover by brute force over support subsets."""
import itertools
from common import *
Qp = {Q: perpmask(Q) for Q in planes}
def cellcov(X):
    m = 0
    for P in planes:
        if P & ~X == 0: m |= P
    return m
stat = collections.Counter(); worst = []
seen = set()
for Q in planes:
    c = min(act_k for act_k in orbit(Q))
    if c in seen: continue
    seen.add(c)
    U = e8.bits(Q); need = 0
    for t in U:
        mine = [F for F in planes if F >> t & 1]
        secs = {F: Qp[F] & e8.HYP[t] for F in mine}
        oth = 0
        for F in mine:
            if F != Q: oth |= secs[F]
        need |= secs[Q] & ~oth
    sup = set()
    for Q2 in planes:
        if Q2 != Q:
            s_ = cellcov(Qp[Q] & Qp[Q2]) & need
            if s_: sup.add(s_)
    for P in planes:
        if P & ~Qp[Q] == 0 and P & need: sup.add(P & need)
    sup = sorted(sup, key=lambda m: -pc(m))
    # keep only maximal supports
    maxi = [s for s in sup if not any(s != o and s & ~o == 0 for o in sup)]
    best = None
    for k in range(1, 6):
        for combo in itertools.combinations(maxi, k):
            u = 0
            for s in combo: u |= s
            if u == need: best = k; break
        if best: break
    stat[(pc(Q), pc(need), best)] += 1
    print('section', 'pair' if pc(Q) == 2 else 'A2', 'users', len(U), 'private lines (union)', pc(need),
          'max support covers', max(pc(s) for s in maxi), 'min #supports', best, flush=True)
print(stat)
