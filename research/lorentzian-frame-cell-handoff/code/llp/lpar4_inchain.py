"""4-section parity tops through t (sections = plane perps through t) with defect |D| <= MAXD, D = xor of the 4 section
indicators ^ R(t), that are IN-CHAIN capable: all defect lines lie in one of the 4 sections.  Exhaustive (vectorised
pair-xor matching with numpy popcount).  Also records the model-A per-target cost lower bound with S0 read in-chain
by all its users (2/u0 if its need has full closure, 1/u0 if proper) + 3 delivered sections (kappa_ex + u - 1)/u.
usage: lpar4_inchain.py MAXD"""
import sys, itertools, collections
import numpy as np
from lgeo import *
MAXD = int(sys.argv[1]) if len(sys.argv) > 1 else 3
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
def words(m): return [(m >> (64 * w)) & ((1 << 64) - 1) for w in range(4)]
for kind in ('P', 'T'):
    t = next(s for s in range(V) if KIND[s] == kind)
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    Sm = [pm(p) for p in pl]; ty = [ptype(p) for p in pl]
    pairs = list(itertools.combinations(range(len(pl)), 2))
    X = np.array([words(Sm[i] ^ Sm[j]) for i, j in pairs], dtype=np.uint64)
    Rw = np.array(words(R), dtype=np.uint64)
    st = collections.Counter(); seen = set()
    for a in range(len(pairs)):
        Y = X[a] ^ Rw
        cnt = np.bitwise_count(X[a + 1:] ^ Y).sum(axis=1)
        for b in np.nonzero(cnt <= MAXD)[0]:
            b = a + 1 + int(b)
            q = set(pairs[a]) | set(pairs[b])
            if len(q) < 4: continue
            q = tuple(sorted(q))
            if q in seen: continue
            seen.add(q)
            D = Sm[q[0]] ^ Sm[q[1]] ^ Sm[q[2]] ^ Sm[q[3]] ^ R
            inside = [m for m in q if D & ~Sm[m] == 0]
            if not inside and pc(D) > 0: 
                st[('NOT in-chain', tuple(sorted(ty[m] for m in q)), pc(D))] += 1
                continue
            st[('in-chain', tuple(sorted(ty[m] for m in q)), pc(D), tuple(sorted(ty[m] for m in inside)), rank(D) if D else 0)] += 1
    print(kind, 'rep', t, 'planes', len(pl), 'pairs', len(pairs), flush=True)
    for k_, v in sorted(st.items()): print('  ', k_, v, flush=True)
