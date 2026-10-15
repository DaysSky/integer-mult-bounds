"""I_{11,1} data for the 4-section port: lines (55 P + 165 T), Gram, perps, planes (orthogonal pairs, A2 closures),
symmetry group H55 = {x -> a x + b mod 11, a in QR} acting on coordinates."""
import sys, os, itertools, collections, pickle
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lword'))
from geom import Geom
g = Geom(11); V = g.V; G = g.G
pc = lambda m: bin(m).count('1')
bits = g.bits
HYP = g.HYP
QR = [1, 3, 4, 5, 9]
GROUP = [(a, b) for a in (QR if os.environ.get('GRP', '55') == '55' else [1]) for b in range(11)]
def line_img(s, a, b):
    k, sp = g.kind[s], g.supp[s]
    img = tuple(sorted((a * i + b) % 11 for i in sp))
    return g.idx[(k, img)]
PERMS = [[line_img(s, a, b) for s in range(V)] for (a, b) in GROUP]
def act(mask, p):
    m = 0
    for s in bits(mask): m |= 1 << p[s]
    return m
def orbit_mask(mask):
    return sorted(set(act(mask, p) for p in PERMS))
def canon_mask(mask): return min(act(mask, p) for p in PERMS)
def perpmask(F):
    m = (1 << V) - 1
    for s in bits(F): m &= HYP[s]
    return m
HERE = os.path.dirname(os.path.abspath(__file__))
def planes_all():
    p = os.path.join(HERE, 'planes.pkl')
    if os.path.exists(p): return pickle.load(open(p, 'rb'))
    pairs, a2 = set(), set()
    for s in range(V):
        for u in range(s + 1, V):
            if G[s, u] == 0: pairs.add((1 << s) | (1 << u))
            else:
                F, r = g.closure((1 << s) | (1 << u))
                if r == 2: a2.add(F)
    out = (sorted(pairs), sorted(a2))
    pickle.dump(out, open(p, 'wb')); return out
line_reps = sorted(set(min(p[s] for p in PERMS) for s in range(V)))
import numpy as _np
_ND = {}
def nondeg_span(mask):
    """True iff the span of the lines in mask is a nondegenerate subspace (Gram det of a basis != 0)."""
    if mask in _ND: return _ND[mask]
    B = []
    for i in bits(mask):
        if _np.linalg.matrix_rank(g.LA[B + [i]]) > len(B): B.append(i)
    Gm = _np.array([[G[a, b] for b in B] for a in B], dtype=float)
    r = abs(round(_np.linalg.det(Gm))) > 0 if B else True
    _ND[mask] = r; return r
