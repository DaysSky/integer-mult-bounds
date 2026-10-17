"""Window-w decoders for full E8 (120 lines): B = sum_j Q_j x P_j over F2 with B_tt = 1 and B_ts = 0 on non-orthogonal
pairs.  Piece j has sources P_j inside A_j and readers Q_j inside C_j; its drop cost is at most the pairing rank
rk(A_j x C_j) = dim A_j - dim(A_j n C_j^perp) (Theorem C of #446 is a lower bound and a single copy meets it).
A template fixes (A_j, C_j); SAT decides whether labels exist.  Template cost < 72 would beat the window-9 floor."""
import sys, itertools, numpy as np, random, time
sys.path.insert(0, '../newunit')
from smallsys import roots, gram
from pysat.solvers import Cadical153
from pysat.formula import IDPool
R, sc = roots('E8'); G, A = gram(R, sc); v = len(G); A = A.astype(float)
NON = [[s for s in range(v) if s != t and G[t, s] != 0] for t in range(v)]
def lines_in(subspace_basis):
    """lines inside span(basis) (basis rows, real)."""
    Bm = np.array(subspace_basis, float); r = np.linalg.matrix_rank(Bm)
    return [t for t in range(v) if np.linalg.matrix_rank(np.vstack([Bm, A[t]])) == r]
def perp_lines(z):   # lines orthogonal to vector z
    return [t for t in range(v) if abs(A[t] @ z) < 1e-9]
def pairing_rank(Aset, Cset):
    if not Aset or not Cset: return 0
    return int(np.linalg.matrix_rank(A[Aset] @ A[Cset].T))
def solve(pieces, timeout=600):
    """pieces: list of (Aset, Cset).  Returns labels or None."""
    pool = IDPool(); cl = []
    p = {}; q = {}
    for j, (As, Cs) in enumerate(pieces):
        for s in As: p[j, s] = pool.id(('p', j, s))
        for t in Cs: q[j, t] = pool.id(('q', j, t))
    def AND(a, b):
        x = pool.id(('and', a, b)); cl.extend([[-x, a], [-x, b], [x, -a, -b]]); return x
    def xor_eq(lits, val):
        if not lits:
            if val: cl.append([]) 
            return
        acc = lits[0]
        for l in lits[1:]:
            x = pool.id(('x', acc, l)); cl.extend([[-x, acc, l], [-x, -acc, -l], [x, -acc, l], [x, acc, -l]]); acc = x
        cl.append([acc] if val else [-acc])
    for t in range(v):
        for s in [t] + NON[t]:
            lits = [AND(q[j, t], p[j, s]) for j in range(len(pieces)) if (j, t) in q and (j, s) in p]
            xor_eq(lits, 1 if s == t else 0)
    if any(len(c) == 0 for c in cl): return None
    S = Cadical153(bootstrap_with=cl)
    ok = S.solve()
    if not ok: return False
    m = set(l for l in S.get_model() if l > 0)
    P = [[s for s in As if p[j, s] in m] for j, (As, Cs) in enumerate(pieces)]
    Q = [[t for t in Cs if q[j, t] in m] for j, (As, Cs) in enumerate(pieces)]
    return P, Q
ALL = list(range(v))
if __name__ == '__main__':
    mode = sys.argv[1]; seed = int(sys.argv[2]); random.seed(seed)
    if mode == 'stars':      # 10 pieces: sources in z_j-perp, readers anywhere (cost 7 each = 70)
        Z = random.sample(range(v), 10); pieces = [(perp_lines(A[z]), ALL) for z in Z]
    elif mode == 'rstars':   # readers in z_j-perp, sources anywhere
        Z = random.sample(range(v), 10); pieces = [(ALL, perp_lines(A[z])) for z in Z]
    elif mode == 'mixed':    # 5 + 5
        Z = random.sample(range(v), 10); pieces = [(perp_lines(A[z]), ALL) for z in Z[:5]] + [(ALL, perp_lines(A[z])) for z in Z[5:]]
    elif mode == 'b0test':   # control: 9 full pieces (cost 72) must be SAT
        pieces = [(ALL, ALL)] * 9
    elif mode == 'w8':       # control: 8 full pieces must be UNSAT
        pieces = [(ALL, ALL)] * 8
    cost = sum(pairing_rank(a, c) for a, c in pieces)
    t0 = time.time(); r = solve(pieces)
    print(mode, seed, 'pieces', len(pieces), 'template cost', cost, '->', 'SAT' if r else ('UNSAT' if r is False else 'trivially UNSAT'), '%.0fs' % (time.time() - t0), flush=True)
    if r:
        P, Q = r; real = sum(pairing_rank(a, c) for a, c in zip(P, Q))
        print('  realised cost', real, 'piece sizes', [(len(a), len(c)) for a, c in zip(P, Q)])
