"""E8: cover number of R(t) (the 63 lines of t-perp = E7) by flats of rank <= r inside t-perp, r = 5 (and 4).
Enumerate all flats of t-perp up to rank r by BFS closure; exact set-cover by bitset search (greedy + exhaustive
k = 3, 4)."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; t = 0
P = e8.HYP[t]; Pl = e8.bits(P)
pc = lambda m: bin(m).count('1')
flats = {0: 0}; fr = [0]; maxr = int(sys.argv[1]) if len(sys.argv) > 1 else 5
while fr:
    nf = []
    for F in fr:
        if flats[F] >= maxr: continue
        for s in Pl:
            if F >> s & 1: continue
            Fc, d = e8.closure(F | (1 << s))
            if Fc not in flats: flats[Fc] = d; nf.append(Fc)
    fr = nf
byr = collections.Counter(flats.values())
print('flats of t-perp by rank:', dict(sorted(byr.items())))
top = [F for F, d in flats.items() if d == maxr]
print('rank-%d flats by #lines:' % maxr, dict(sorted(collections.Counter(pc(F) for F in top).items())))
# maximal ones only (by lines), dedupe dominated
top.sort(key=pc, reverse=True)
full = P
# k=3 and k=4 exhaustive with pruning: need sum of sizes >= 63
sizes = [pc(F) for F in top]
best = None
for k in (3, 4):
    found = 0
    if sum(sizes[:k]) < 63: print('k=%d impossible by sizes' % k); continue
    # exhaustive over combinations with branch on uncovered line
    def rec(cov, start, left, chosen):
        global found
        if cov == full:
            found += 1; return True
        if left == 0: return False
        # pick lowest uncovered line; must be covered by some chosen flat
        s = (full & ~cov) & -(full & ~cov)
        for i, F in enumerate(top):
            if F & s:
                if rec(cov | F, 0, left - 1, chosen + [i]): return True
        return False
    ok = rec(0, 0, k, [])
    print('cover by %d rank-<=%d flats:' % (k, maxr), 'YES' if ok else 'NO', flush=True)
