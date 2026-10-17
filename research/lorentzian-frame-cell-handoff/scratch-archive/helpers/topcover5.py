"""Option B: target t reads at level 6 a register whose content lies in a 5-dim flat G5 (no level-6 partner needed);
the remaining readers E7(t) minus G5 must be covered by 2 dedicated sections a1, a2 (6-dim flats in t^perp)."""
import sys, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
t = 0
H = e8.HYP[t]; Hl = e8.bits(H)
level = {1: {1 << s for s in Hl}}
for d in range(2, 7):
    nxt = set()
    for m in level[d-1]:
        for s in Hl:
            if m >> s & 1: continue
            cm, k = e8.closure(m | (1 << s))
            if k == d: nxt.add(cm)
    level[d] = nxt
secs = list(level[6]); share = {m: e8.popcount(e8.perp(m)) for m in secs}
G5s = list(level[5])
# max number of lines in a 5-dim flat inside t^perp
mx = max(e8.popcount(g) for g in G5s)
print('5-dim flats', len(G5s), 'max lines', mx, collections.Counter(e8.popcount(g) for g in G5s))
found = collections.Counter()
# for efficiency: only G5 with many lines
for G5 in sorted(G5s, key=lambda g: -e8.popcount(g))[:3000]:
    rest = H & ~G5
    cands = [m for m in secs if (m & rest)]
    big = [m for m in cands if e8.popcount(m & rest) * 2 >= e8.popcount(rest)]
    ok = False
    for a1 in big:
        r1 = rest & ~a1
        for a2 in cands:
            if r1 & ~a2 == 0:
                found[(e8.popcount(G5), e8.popcount(a1), share[a1], e8.popcount(a2), share[a2])] += 1
                ok = True
print('covers found (G5 lines, a1 lines, a1 share, a2 lines, a2 share):', dict(found) if found else 'NONE')
