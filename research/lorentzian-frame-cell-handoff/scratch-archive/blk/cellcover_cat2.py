# Catalogue cover with quads split by one of their 3 pairings (the exact cell-respecting rule); sound for SAT only.
import sys, pickle, itertools, random, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, nondegenerate
from pysat.solvers import Cadical153
from pysat.card import CardEnc
part = pickle.load(open(sys.argv[1], 'rb')); OUT = sys.argv[2]; NS = int(sys.argv[3]); TL = [int(x) for x in sys.argv[4].split(',')]
frames = [tuple(f) for b in part[0] for f in b]; punct = set(part[1])
LA = g.L.astype(float)
def rank(ls): return int(np.linalg.matrix_rank(LA[list(ls)], 1e-9)) if ls else 0
res = {}
for t in TL:
    rnd = random.Random(1000 + t)
    Rs = set(u for u in bits(g.HYP[t]) if u not in punct)
    pairs = []; quads = []
    for f in frames:
        inn = tuple(u for u in f if u in Rs)
        if len(inn) == 2: pairs.append(inn)
        elif len(inn) == 4: quads.append(inn)
        elif len(inn) == 3: pairs += [(u,) for u in inn]
    qpairs = [[((q[0], q[1]), (q[2], q[3])), ((q[0], q[2]), (q[1], q[3])), ((q[0], q[3]), (q[1], q[2]))] for q in quads]
    allp = list(pairs) + sorted(set(p for qp in qpairs for pr in qp for p in pr))
    pidx = {p: i for i, p in enumerate(allp)}
    cat = {}
    for it in range(NS):
        units = list(pairs) + [p for qp in qpairs for p in qp[rnd.randrange(3)]]
        rnd.shuffle(units); ls = []
        for u_ in units:
            cand = ls + list(u_)
            if rank(cand) <= 9: ls = cand
        m = closure(sum(1 << u for u in ls))
        if rank(ls) == 9 and not nondegenerate(m): continue
        cover = frozenset(i for i, p in enumerate(allp) if all((m >> u) & 1 for u in p))
        cat[cover] = m
    keep = []
    for e in sorted(cat, key=len, reverse=True):
        if not any(e <= k for k in keep): keep.append(e)
    s = Cadical153(); nv = len(keep)
    cov = {}
    for i in range(len(allp)):
        nv += 1; cov[i] = nv
        lits = [k + 1 for k, e in enumerate(keep) if i in e]
        s.add_clause([-cov[i]] + lits)
    for p in pairs: s.add_clause([cov[pidx[p]]])
    for qp in qpairs:
        zs = []
        for pr in qp:
            nv += 1; z = nv; zs.append(z)
            for p in pr: s.add_clause([-z, cov[pidx[p]]])
        s.add_clause(zs)
    card = CardEnc.atmost(lits=list(range(1, len(keep) + 1)), bound=3, top_id=nv)
    for c in card.clauses: s.add_clause(c)
    ok = s.solve()
    res[t] = ('SAT' if ok else 'catalogue-fail', len(keep))
    print('t', t, g.kind[t], res[t][0], 'catalogue', len(keep), flush=True)
    s.delete()
from collections import Counter
print('summary', Counter(v[0] for v in res.values()))
pickle.dump(res, open(OUT, 'wb'))
