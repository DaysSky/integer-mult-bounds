"""Minimum number of D5 flats (perps of A3s through t) covering R(t) in E8; count and classify the 5-covers."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; GI = e8.GI; t = 0; P = e8.HYP[t]
pc = lambda m: bin(m).count('1')
def perpmask(F):
    m = (1 << V) - 1
    for s in e8.bits(F): m &= e8.HYP[s]
    return m
X6 = set()
for a in range(1, V):
    for b in range(a + 1, V):
        F, d = e8.closure((1 << t) | (1 << a) | (1 << b))
        if d == 3 and pc(F) == 6: X6.add(F)
X6 = sorted(X6); c = [perpmask(F) & P for F in X6]
by_line = collections.defaultdict(list)
for i, m in enumerate(c):
    for s in e8.bits(m): by_line[s].append(i)
def count(k, limit=10**7):
    found = set()
    def rec(unc, kk, chosen):
        if unc == 0: found.add(tuple(sorted(chosen))); return
        if kk == 0 or pc(unc) > 20 * kk: return
        s = (unc & -unc).bit_length() - 1
        for i in by_line[s]:
            rec(unc & ~c[i], kk - 1, chosen + [i])
            if len(found) > limit: return
    rec(P, k, [])
    return found
for k in (4, 5):
    f = count(k)
    print('covers of R(t) by %d D5s: %d' % (k, len(f)), flush=True)
    if f:
        prof = collections.Counter()
        for cv in list(f)[:20000]:
            mm = collections.Counter(sum(1 for i in cv if c[i] >> s & 1) for s in e8.bits(P))
            inter = tuple(sorted(pc(X6[a] & X6[b]) for a, b in itertools.combinations(cv, 2)))
            prof[(tuple(sorted(mm.items())), inter)] += 1
        for kk, n in prof.most_common(8): print('   multiplicity', kk[0], ' A3 pairwise intersections', kk[1], n)
        break
