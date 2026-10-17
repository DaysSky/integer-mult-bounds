"""E8: 4-covers of R(t) by line-perp sections R(t) cap u-perp (u any line != t): users per section (lines in
span(t,u)), private-set sizes and whether each private set spans its section's flat."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
import numpy as np
V = e8.V; GI = e8.GI; t = 0; R = e8.HYP[t]
pc = lambda m: bin(m).count('1')
LA = e8.LA
sec = {u: R & e8.HYP[u] for u in range(V) if u != t}
def users(u):
    A = np.vstack([LA[t], LA[u]]); r = np.linalg.matrix_rank(A)
    return sum(1 for z in range(V) if np.linalg.matrix_rank(np.vstack([A, LA[z]])) == r)
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
print('E8 4-covers by sections:', len(covers), flush=True)
stat = collections.Counter(); uc = {}
for cv in covers:
    key = []
    for u in cv:
        if u not in uc: uc[u] = users(u)
        others = 0
        for w in cv:
            if w != u: others |= sec[w]
        P = sec[u] & ~others
        key.append((uc[u], pc(sec[u]), pc(P), 'span' if (P and e8.dim(P) == e8.dim(sec[u])) else ('empty' if not P else 'proper')))
    stat[tuple(sorted(key))] += 1
for k, n in stat.most_common(15): print('   ', n, k)
