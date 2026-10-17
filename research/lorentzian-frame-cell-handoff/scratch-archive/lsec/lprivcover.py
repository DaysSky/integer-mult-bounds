"""Private-line screen for an I_{11,1} design (raw mode cg=0 or cell mode cg=1): for each section-orbit rep Q, min
number of supports (lines of Q-perp ∩ Q'-perp for design Q' != Q, or [cg=0] single lines / cells) covering the union
of its users' private lines; compare with |Q|."""
import sys, json, itertools
from lcommon import *
DES = sys.argv[1]; cg = int(sys.argv[2])
planes = [int(h, 16) for h in json.load(open(DES))['planes']]
Qp = {Q: perpmask(Q) for Q in planes}
through = collections.defaultdict(list)
for F in planes:
    for s in bits(F): through[s].append(F)
def cellcov(X):
    m = 0
    for P in planes:
        if P & ~X == 0: m |= P
    return m
seen = set(); res = collections.Counter()
for Q in planes:
    c = canon_mask(Q)
    if c in seen: continue
    seen.add(c)
    need = 0
    for t in bits(Q):
        mine = through[t]; oth = 0
        for F in mine:
            if F != Q: oth |= Qp[F] & HYP[t]
        need |= (Qp[Q] & HYP[t]) & ~oth
    sup = set()
    for Q2 in planes:
        if Q2 == Q: continue
        X = Qp[Q] & Qp[Q2]
        s_ = (cellcov(X) if cg else X) & need
        if s_: sup.add(s_)
    for P in planes:
        if P & ~Qp[Q] == 0 and P & need: sup.add(P & need)
    maxi = [s for s in sup if not any(s != o and s & ~o == 0 for o in sup)]
    best = None
    for k in range(1, 5):
        for combo in itertools.combinations(maxi, k):
            u = 0
            for s in combo: u |= s
            if u == need: best = k; break
        if best: break
    res[(pc(Q), pc(need), max((pc(s) for s in maxi), default=0), best)] += 1
    print('section users', pc(Q), 'private union', pc(need), 'largest support', max((pc(s) for s in maxi), default=0), '#maximal supports', len(maxi), 'min cover', best, flush=True)
print(res)
