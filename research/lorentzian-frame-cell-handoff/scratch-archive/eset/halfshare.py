"""Sharing of E-set halves: for each sign half (and, for comparison, each E-set), the number of lines in the perp of
its span (sections that could contain it) and the number of E-sets of the partition that contain it as a subset.
Usage: halfshare.py e8 | i11 | i13"""
import sys, pickle, collections, itertools, numpy as np
exec(open('ehalves.py').read().split("orth = lambda")[0].replace("mode = sys.argv[1]", "mode = sys.argv[1]"))
orth = lambda a, b: a != b and GI[a, b] == 0
rk = lambda S: int(np.linalg.matrix_rank(LA[sorted(S)])) if S else 0
def perp_lines(S):
    B = LA[sorted(S)]
    # lines u with <u, s> = 0 for all s in S (form via GI on lines: use GI rows)
    return [u for u in live if all(GI[u, s] == 0 and u != s for s in S)]
Es = []; halves = []
for f in frames:
    for t, e in itertools.combinations(f, 2):
        k, l = [x for x in f if x not in (t, e)]
        E = frozenset(u for u in live if orth(u, t) and orth(u, e) and not orth(u, k) and not orth(u, l))
        Es.append(E)
        halves.append(frozenset(u for u in E if GI[u, k] == GI[u, l])); halves.append(frozenset(u for u in E if GI[u, k] == -GI[u, l]))
st = collections.Counter()
for H in halves:
    pl = len(perp_lines(H)); cont = sum(1 for E in Es if H <= E)
    st[(len(H), rk(H), pl, cont)] += 1
print(mode, '(|half|, rank, #lines perp to half, #E-sets containing half): count')
for k_, c in sorted(st.items()): print('  ', k_, c)
print('distinct halves', len(set(halves)), 'of', len(halves))
