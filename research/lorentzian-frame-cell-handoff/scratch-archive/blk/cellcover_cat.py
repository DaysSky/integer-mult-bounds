# Cell-respecting 3-covers by catalogue (sound for SAT answers only): sample maximal cell unions of rank <= 9 inside
# R_live(t) (random greedy), close them, keep legal ones (rank <= 8, or rank 9 and nondegenerate), then pick <= 3
# catalogue entries covering every cell (pysat, cardinality).  A "no cover" answer only says the catalogue failed.
import sys, pickle, itertools, random, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, nondegenerate
from pysat.solvers import Cadical153
from pysat.card import CardEnc
part = pickle.load(open(sys.argv[1], 'rb')); OUT = sys.argv[2]; CH, NCH = int(sys.argv[3]), int(sys.argv[4])
NS = int(sys.argv[5]) if len(sys.argv) > 5 else 4000
frames = [tuple(f) for b in part[0] for f in b]; punct = set(part[1])
live = [u for u in range(V) if u not in punct]
ORDER = [u for u in live if g.kind[u] == 'T'] + [u for u in live if g.kind[u] == 'P']
LA = g.L.astype(float)
def rank(ls): return int(np.linalg.matrix_rank(LA[list(ls)], 1e-9)) if ls else 0
res = {}
TL = ORDER[CH::NCH] if CH >= 0 else [int(x) for x in sys.argv[6].split(',')]
for t in TL:
    rnd = random.Random(t)
    Rs = set(u for u in bits(g.HYP[t]) if u not in punct)
    cells = []                                      # each cell: tuple of lines (pairs; quads offer 3 pairings)
    quadalts = []
    for f in frames:
        inn = tuple(u for u in f if u in Rs)
        if len(inn) == 2: cells.append(inn)
        elif len(inn) == 4: quadalts.append(inn)
        elif len(inn) == 3: cells += [(u,) for u in inn]
    # quads: use the whole quad as one unit (a pairing choice only helps; whole quad is the strict version)
    units = cells + quadalts
    best = None; cat = {}
    for it in range(NS):
        order = list(range(len(units))); rnd.shuffle(order)
        S = []; ls = []
        for i in order:
            cand = ls + list(units[i])
            if rank(cand) <= 9: S.append(i); ls = cand
        m = closure(sum(1 << u for u in ls))
        if rank(ls) == 9 and not nondegenerate(m): continue
        cover = frozenset(i for i in range(len(units)) if all((m >> u) & 1 for u in units[i]))
        cat[cover] = m
    entries = list(cat)
    # remove dominated entries
    entries.sort(key=len, reverse=True)
    keep = []
    for e in entries:
        if not any(e <= k for k in keep): keep.append(e)
    s = Cadical153(); var = {i: i + 1 for i in range(len(keep))}
    top = len(keep)
    for u in range(len(units)):
        cl = [var[i] for i, e in enumerate(keep) if u in e]
        if not cl: break
        s.add_clause(cl)
    else:
        card = CardEnc.atmost(lits=list(var.values()), bound=3, top_id=top)
        for c in card.clauses: s.add_clause(c)
        ok = s.solve()
        if ok:
            m_ = set(l for l in s.get_model() if l > 0)
            chosen = [keep[i] for i in range(len(keep)) if var[i] in m_]
            res[t] = ('SAT', [sorted(set(u for i in e for u in units[i])) for e in chosen])
        else: res[t] = ('catalogue-fail', len(keep))
        print('t', t, g.kind[t], res[t][0], 'catalogue', len(keep), flush=True)
        s.delete(); continue
    res[t] = ('catalogue-fail(uncovered unit)', len(keep))
    print('t', t, g.kind[t], res[t][0], flush=True)
from collections import Counter
print('summary', Counter((g.kind[t], v[0]) for t, v in res.items()))
pickle.dump(res, open(OUT, 'wb'))
