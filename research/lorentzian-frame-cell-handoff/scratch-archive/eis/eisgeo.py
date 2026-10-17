"""Eisenstein E8 geometry: 40 K-lines, flats, closure table, pairing costs."""
import numpy as np, pickle, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry798 import geometry
from fractions import Fraction

P = 1000003
def rank_mod(M):
    M = [[int(x) % P for x in r] for r in M]
    if not M: return 0
    rows, cols = len(M), len(M[0]); r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c]), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], P - 2, P)
        M[r] = [x * inv % P for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % P for a, b in zip(M[i], M[r])]
        r += 1
        if r == rows: break
    return r

def build():
    reps, images, adjacent, pairs, orbits = geometry()
    V = [np.array([r, j], dtype=np.int64) for r, j in zip(reps, images)]
    n = 40
    nonorth = adjacent  # masks of nonorthogonal lines
    orth = [((1 << n) - 1) ^ adjacent[i] ^ (1 << i) for i in range(n)]
    # flats by closure
    def span_rows(mask):
        rows = [V[t][k] for t in range(n) if mask >> t & 1 for k in range(2)]
        return rows
    def closure(mask):
        rows = span_rows(mask)
        rk = rank_mod(rows) if rows else 0
        out = mask
        for t in range(n):
            if not mask >> t & 1:
                if rank_mod(rows + [V[t][0], V[t][1]]) == rk:
                    out |= 1 << t
        return out, rk
    flats = {0: 0}; flat_list = [0]; flat_rank = [0]
    frontier = [0]
    nxt = {}
    while frontier:
        new = []
        for f in frontier:
            for t in range(n):
                if f >> t & 1:
                    nxt[(f, t)] = f; continue
                g, rk = closure(f | 1 << t)
                if g not in flats:
                    flats[g] = len(flat_list); flat_list.append(g); flat_rank.append(rk // 2); new.append(g)
                nxt[(f, t)] = g
        frontier = new
    nf = len(flat_list)
    table = np.zeros((nf, n), dtype=np.int32)
    for (f, t), g in nxt.items():
        table[flats[f], t] = flats[g]
    # pairing cost between flats
    bases = []
    for f in flat_list:
        rows = span_rows(f)
        # pick independent rows
        basis = []
        for r in rows:
            if rank_mod(basis + [r]) > len(basis):
                basis.append(r)
        bases.append(np.array(basis, dtype=np.int64).reshape(-1, 8))
    cost = np.zeros((nf, nf), dtype=np.int8)
    for a in range(nf):
        for b in range(a, nf):
            if len(bases[a]) == 0 or len(bases[b]) == 0:
                c = 0
            else:
                G = bases[a] @ bases[b].T
                c = rank_mod(G.tolist())
                assert c % 2 == 0
                c //= 2
            cost[a, b] = cost[b, a] = c
    return dict(n=n, V=V, nonorth=nonorth, orth=orth, flat_list=flat_list, flat_rank=flat_rank,
                table=table, cost=cost)

if __name__ == '__main__':
    d = build()
    from collections import Counter
    print('flats', len(d['flat_list']), Counter((d['flat_rank'][i], bin(f).count('1')) for i, f in enumerate(d['flat_list'])))
    pickle.dump(d, open('eis.pkl', 'wb'))
