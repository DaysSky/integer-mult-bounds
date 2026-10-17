"""E8: geometry of the 4-section covers of R(t) with all-proper private sets.  For each cover type, the Gram matrix of
{t, u1..u4} (u = section partners) and the planes span(t,u) (2 or 3 lines); also whether the 4 planes' lines are
mutually orthogonal across planes, and how many 4-section covers use only A2 planes."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
import numpy as np
V = e8.V; GI = e8.GI; t = 0; R = e8.HYP[t]
pc = lambda m: bin(m).count('1')
LA = e8.LA
sec = {u: R & e8.HYP[u] for u in range(V) if u != t}
by_line = collections.defaultdict(list)
for u, m in sec.items():
    for s in e8.bits(m): by_line[s].append(u)
mx = max(pc(m) for m in sec.values())
covers = set()
def rec(unc, k, chosen):
    if unc == 0: covers.add(tuple(sorted(chosen))); return
    if k == 0 or pc(unc) > mx * k: return
    s = (unc & -unc).bit_length() - 1
    for u in by_line[s]:
        if u in chosen: continue
        rec(unc & ~sec[u], k - 1, chosen + [u])
rec(R, 4, [])
def plane(u):
    F, d = e8.closure((1 << t) | (1 << u)); return F
stat = collections.Counter(); ex = {}
for cv in covers:
    planes = [plane(u) for u in cv]
    kinds = tuple(sorted(pc(P) for P in planes))
    # private sets proper?
    props = []
    for u in cv:
        others = 0
        for w in cv:
            if w != u: others |= sec[w]
        P = sec[u] & ~others
        props.append(P and e8.dim(P) < e8.dim(sec[u]))
    if not all(props): continue
    # partner Gram (abs inner products of the planes' non-t lines)
    nont = [ [s for s in e8.bits(P) if s != t] for P in planes]
    cross = tuple(sorted(tuple(sorted(abs(int(GI[a, b])) for a in A for b in B)) for A, B in itertools.combinations(nont, 2)))
    key = (kinds, cross)
    stat[key] += 1; ex.setdefault(key, cv)
for k, n in stat.most_common(12): print(n, 'plane sizes', k[0], ' cross |<a,b>| patterns', k[1])
print('all-A2 all-proper covers:', sum(n for k, n in stat.items() if k[0] == (3, 3, 3, 3)))
