"""Complex P112 top-level register floor (level h-1 = 8): per target t, readers R(t) covered by its own level-7 frame F7
(shared needer) and dedicated sections at level 8.  Sections = 7-dim subspaces of t^perp (8-dim) in F2^9.
Cost model as for the bit side: shared flat with s users costs (users+1)/users if its content spans the full 7 dims
(needs a merge partner at that flat), users/users = 1 otherwise."""
import itertools, collections
from e8 import P, V, LEG
from geo import dot, basis, span
h = 9
def rank(vs): return len(basis(vs))
R = [[s for s in range(V) if s != t and LEG[t, s]] for t in range(V)]
print('ports', V, 'readers per target', collections.Counter(len(r) for r in R))
def hyperplanes_of(Wbasis):
    """all codim-1 subspaces of span(Wbasis): kernels of nonzero functionals on W"""
    k = len(Wbasis); out = []
    Wset = span(Wbasis)
    for f in range(1, 1 << h):
        # functional x -> dot(f,x) restricted to W must be nonzero on W
        if all(dot(f, w) == 0 for w in Wbasis): continue
        H = frozenset(x for x in Wset if dot(f, x) == 0)
        out.append(H)
    return list(set(out))
t = 0
Tperp = basis([x for x in range(1, 1 << h) if dot(x, P[t]) == 0])
secs = hyperplanes_of(Tperp)
print('sections of t^perp:', len(secs))
def share(S):
    Sb = basis(list(S))
    perpS = [x for x in range(1, 1 << h) if all(dot(x, b) == 0 for b in Sb)]
    return [u for u in range(V) if P[u] in set(perpS)]
Rt = set(R[t])
res = collections.Counter()
for F7 in secs:
    covF = {s for s in Rt if P[s] in F7}
    rest = Rt - covF
    sF = len(share(F7))
    for a1 in secs:
        if a1 == F7: continue
        if all(P[s] in a1 for s in rest):
            k = len(share(a1))
            spanF = rank([P[s] for s in covF]); spanA = rank([P[s] for s in rest])
            costF = (1 if spanF < 7 else 2) / sF
            costA = (k + (1 if spanA >= 7 else 0)) / k
            res[(len(covF), sF, spanF, len(rest), k, spanA, round(costF + costA, 3))] += 1
for key, n in sorted(res.items(), key=lambda kv: kv[0][-1]):
    print('F7 covers %d (shared %d, span %d) | dedicated covers %d (shared %d, span %d) | per-target %.3f  x%d' % (*key, n))
