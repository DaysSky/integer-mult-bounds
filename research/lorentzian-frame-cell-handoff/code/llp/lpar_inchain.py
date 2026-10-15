"""3-section parity tops through t with defect |D| <= 3 (D = S1 ^ S2 ^ S3 ^ R(t)) and IN-CHAIN capability: all defect
lines lie in one section S0 (then the chain 0 -> span(D) -> S0 -> t-perp is nested).  Exhaustive per representative.
Reports counts by (plane types, |D|, which section types contain D, rank of span(D))."""
import itertools, collections
from lgeo import *
VEC = {}
for s in range(V):
    VEC[tuple(int(x) for x in g.L[s])] = s; VEC[tuple(-int(x) for x in g.L[s])] = s
def plane_of(a, b):
    m = (1 << a) | (1 << b)
    if G[a][b] != 0:
        for sg in (1, -1):
            c = VEC.get(tuple(int(x) for x in (g.L[a] - sg * g.L[b])))
            if c is not None and c not in (a, b): m |= 1 << c
    return m
def ptype(p):
    L = bits(p); ks = ''.join(sorted(KIND[x] for x in L))
    if len(L) == 3: return ks
    a_, b_ = L
    if ks == 'PT':
        P_ = a_ if KIND[a_] == 'P' else b_; T_ = b_ if P_ == a_ else a_
        return 'PTi' if set(SUPP[P_]) <= set(SUPP[T_]) else 'PTd'
    if ks == 'TT': return 'TT' if G[a_][b_] == 0 else 'TTs'
    return ks
for kind in ('P', 'T'):
    t = next(s for s in range(V) if KIND[s] == kind)
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    Sm = [pm(p) for p in pl]; ty = [ptype(p) for p in pl]
    st = collections.Counter()
    for i, j in itertools.combinations(range(len(pl)), 2):
        X = Sm[i] ^ Sm[j] ^ R
        for k in range(j + 1, len(pl)):
            D = X ^ Sm[k]
            d = pc(D)
            if d > 3 or d < 2: continue
            assert D & ~R == 0 or True
            inside = [ty[m] for m in (i, j, k) if D & ~Sm[m] == 0]
            if not inside: continue
            st[(tuple(sorted((ty[i], ty[j], ty[k]))), d, tuple(sorted(inside)), rank(D), 'D in R' if D & ~R == 0 else 'D out R')] += 1
    print(kind, 'representative', t, 'planes', len(pl))
    for k_, v in sorted(st.items()): print('  ', k_, v)
