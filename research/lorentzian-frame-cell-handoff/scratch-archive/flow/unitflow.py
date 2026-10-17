"""3-stage swap circuits from root-system units (direct reads + J+B centres); exact fractional flow bound."""
import sys, numpy as np, itertools, time
from motif import Circ, scalar_check, max_flow
from units import UNITS
def decoder(R):
    v, h = R.shape
    G = np.rint(R @ R.T).astype(int)
    assert all(G[i, i] == 2 for i in range(v))
    assert set(np.abs(G[~np.eye(v, dtype=bool)]).tolist()) <= {0, 1}
    # lattice basis: pick h independent roots, express all roots in that basis (integer coords for root lattice)
    basis = []
    for i in range(v):
        if np.linalg.matrix_rank(R[basis + [i]]) > len(basis): basis.append(i)
        if len(basis) == h: break
    B = R[basis]
    coords = np.rint(np.linalg.solve(B.T, R.T).T).astype(int)
    assert np.allclose(coords @ B, R)
    Gb = np.rint(B @ B.T).astype(int) % 2
    Rb = coords % 2
    A1 = (Rb @ Gb) % 2   # reader side
    totals = [(list(range(v)), list(range(v)))]
    for i in range(h):
        Rset = [s for s in range(v) if A1[s, i]]; Aset = [t for t in range(v) if Rb[t, i]]
        if Rset and Aset: totals.append((Rset, Aset))
    C = np.zeros((v, v), dtype=int)
    for Rs, As in totals:
        for s in Rs:
            for t in As: C[s, t] ^= 1
    orth = (G == 0)
    assert all(C[s, s] == 1 for s in range(v)) and not any(C[s, t] for s in range(v) for t in range(v) if s != t and not orth[s, t])
    side = {s: [t for t in range(v) if t != s and orth[s, t] and C[s, t]] for s in range(v)}
    return totals, side, G
def build(R):
    totals, side, G = decoder(R)
    v = len(R)
    c = Circ()
    X = [c.wire(('X', a)) for a in range(v)]
    Y = [c.wire(('Y', a)) for a in range(v)]
    def inv(src, tgt, st, inverse):
        Cw = [c.wire(('C', st, j)) for j in range(len(totals))]
        r_scat = [(tgt[s], Cw[j]) for j, (Rs, As) in enumerate(totals) for s in Rs]
        r_gath = [(Cw[j], src[t]) for j, (Rs, As) in enumerate(totals) for t in As]
        r_side = [(tgt[s], src[t]) for s in range(v) for t in side[s]]
        rows = [r_scat, r_gath, r_scat, r_side, r_gath]
        if inverse: rows = rows[::-1]
        for r in rows:
            for x in r: c.gate([x])
    inv(X, Y, 0, False); inv(Y, X, 1, True); inv(X, Y, 2, False)
    W = len(c.wires); rho = list(range(W))
    for a in range(v): rho[X[a]], rho[Y[a]] = Y[a], X[a]
    return c, rho, totals, side
if __name__ == '__main__':
    for name in sys.argv[1:]:
        R = UNITS[name]
        c, rho, totals, side = build(R)
        v, h = R.shape
        print(name, 'v', v, 'h', h, 'totals', len(totals), 'side/line', len(side[0]), 'W', len(c.wires), 'gates', len(c.gates), 'scalar', scalar_check(c, rho), flush=True)
        t0 = time.time()
        F, res, W, E = max_flow(c, rho, directed=False)
        print('   undirected F*', round(F, 6), 'W-F*', round(W - F, 6), 'edges', E, '%.0fs' % (time.time() - t0), flush=True)
