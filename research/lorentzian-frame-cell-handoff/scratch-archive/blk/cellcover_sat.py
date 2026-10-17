# Exact test of the cell-hub lead: for each live target t, can the lines of R_live(t) be split into 3 groups, each of
# rank <= 9 and with a nondegenerate span when it has rank 9, such that the partition cells (pairs from one partition
# frame inside R(t); for frames with all 4 lines inside, any of the 3 pairings) are never split?
# SAT (CaDiCaL) with lazily added rank clauses; UNSAT is an exact "no cell-respecting 3-cover" certificate.
import sys, pickle, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
from pysat.solvers import Cadical153
part = pickle.load(open(sys.argv[1], 'rb')); targets = [int(a) for a in sys.argv[2:]] if len(sys.argv) > 2 else None
frames = [tuple(f) for b in part[0] for f in b]; punct = set(part[1])
live = [u for u in range(V) if u not in punct]
LA = g.L.astype(float)
rng = np.random.default_rng(11)
def rank(ls): return np.linalg.matrix_rank(LA[list(ls)], 1e-9) if ls else 0
def mask(ls): return sum(1 << u for u in ls)
res = {}
for t in (targets or live):
    R = [u for u in bits(g.HYP[t]) if u not in punct]
    pos = {u: i for i, u in enumerate(R)}
    var = lambda u, c: 3 * pos[u] + c + 1
    nv = 3 * len(R); s = Cadical153()
    for u in R:
        s.add_clause([var(u, c) for c in range(3)])
        for a, b in itertools.combinations(range(3), 2): s.add_clause([-var(u, a), -var(u, b)])
    s.add_clause([var(R[0], 0)])                                    # symmetry: first line in group 0
    for f in frames:
        inn = [u for u in f if u in pos]
        if len(inn) == 2:
            u, v = inn
            for c in range(3): s.add_clause([-var(u, c), var(v, c)]); s.add_clause([var(u, c), -var(v, c)])
        elif len(inn) == 4:
            pairings = [((inn[0], inn[1]), (inn[2], inn[3])), ((inn[0], inn[2]), (inn[1], inn[3])), ((inn[0], inn[3]), (inn[1], inn[2]))]
            ys = []
            for p in pairings:
                nv += 1; y = nv; ys.append(y)
                for (u, v) in p:
                    for c in range(3): s.add_clause([-y, -var(u, c), var(v, c)]); s.add_clause([-y, var(u, c), -var(v, c)])
            s.add_clause(ys)
        elif len(inn) == 3 and t in f: pass                          # own frame: the 3 mates are free singles
        elif len(inn) not in (0,): raise SystemExit('odd intersection %d for t=%d' % (len(inn), t))
    it = 0; status = None
    while True:
        it += 1
        if not s.solve(): status = 'UNSAT'; break
        m = set(l for l in s.get_model() if l > 0)
        groups = [[u for u in R if var(u, c) in m] for c in range(3)]
        bad = False
        for c, G in enumerate(groups):
            if rank(G) >= 10:
                bad = True
                for rep in range(6):                               # several random bases -> forbid each in every group
                    order = list(G); rng.shuffle(order); B = []
                    for u in order:
                        if rank(B + [u]) > len(B): B.append(u)
                        if len(B) == 10: break
                    for cc in range(3): s.add_clause([-var(u, cc) for u in B])
            elif rank(G) == 9:
                cl = closure(mask(G))
                if not nondegenerate(cl):                           # group inside a degenerate hyperplane: forbid
                    bad = True; outside = [u for u in R if not (cl >> u) & 1]
                    for cc in range(3): s.add_clause([var(u, cc) for u in outside])
        if not bad: status = 'SAT'; break
        if it > 60000: status = 'LIMIT'; break
    res[t] = (status, it)
    print('t', t, g.kind[t], status, 'iterations', it, flush=True)
    s.delete()
from collections import Counter
print('summary', Counter((g.kind[t], st) for t, (st, _) in res.items()))
pickle.dump(res, open('cellcover_sat_out.pkl', 'wb'))
