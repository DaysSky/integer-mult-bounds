"""Anatomy of the I_{13,1} alignment obstruction.
(1) E-set sizes per cell type (parity) for PPTT and TTTT frames.
(2) After f0: the most constrained line, its allowed frames, and for each, the lines killed (no allowed frame left)."""
import sys, pickle, numpy as np, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V; G = g.G
frames, comp_lists, kinds = pickle.load(open('compat13.pkl', 'rb'))
F = np.array(frames); nf = len(F)
orth = (G == 0); np.fill_diagonal(orth, False)
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
def esets(q):
    out = []
    for a, b in pairs:
        o = [c for c in range(4) if c not in (a, b)]
        E = orth[q[a]] & orth[q[b]] & ~orth[q[o[0]]] & ~orth[q[o[1]]]
        out.append(((g.kind[q[a]] + g.kind[q[b]]), int(E.sum())))
    return out
for typ in ('PPTT', 'TTTT'):
    i0 = next(i for i in range(nf) if kinds[i] == typ)
    print(typ, [g.supp[x] for x in F[i0]], 'E-set (cell kinds, size):', esets(F[i0]))
C = np.zeros((nf, nf), dtype=bool)
for i, js in enumerate(comp_lists): C[i, js] = True
member = np.zeros((V, nf), dtype=bool)
for j in range(nf): member[F[j], j] = True
f0 = next(i for i in range(nf) if kinds[i] == 'PPTT')
allowed = C[f0] & ~member[F[f0]].any(0)
covered = np.zeros(V, dtype=bool); covered[F[f0]] = True
unc = np.nonzero(~covered)[0]; cnt = (member[unc] & allowed).sum(1)
order = np.argsort(cnt)
print('lines with fewest allowed frames after f0:')
for k in order[:8]:
    u = unc[k]; print('  ', g.kind[u], g.supp[u], 'allowed', cnt[k])
dist = collections.Counter(cnt.tolist()); print('distribution (allowed count: #lines), smallest:', sorted(dist.items())[:10])
u = unc[order[0]]
for j in np.nonzero(member[u] & allowed)[0]:
    a2 = allowed & C[j] & ~member[F[j]].any(0)
    cov2 = covered.copy(); cov2[F[j]] = True
    unc2 = np.nonzero(~cov2)[0]; c2 = (member[unc2] & a2).sum(1)
    dead = unc2[c2 == 0]
    print(' option frame', [(g.kind[x], g.supp[x]) for x in F[j]], '-> killed lines', len(dead), [(g.kind[x], g.supp[x]) for x in dead[:10]])
