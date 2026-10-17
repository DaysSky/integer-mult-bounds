"""Per target t: covers E7(t) subset of F6 u a1 u a2 with F6 a shareable section (D6 or E6) and a1,a2 any sections.
Level-6 register model cost per target: needer flat F6 shared by s targets costs 2/s; a dedicated section shared by k
targets (k <= #lines in its perp) costs (k+1)/k per output (lower bound with full sharing)."""
import sys, collections, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V
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
secs = list(level[6])
share = {m: e8.popcount(e8.perp(m)) for m in secs}
nlines = {m: e8.popcount(m) for m in secs}
best = {}
for F6 in secs:
    if share[F6] < 2: continue
    rest = H & ~F6
    cands = [m for m in secs if m != F6 and (m & rest)]
    # need a1 | a2 >= rest
    for i, a1 in enumerate(cands):
        r1 = rest & ~a1
        if r1 == 0:
            continue  # single section covers rest (impossible for E8 but check)
        for a2 in cands[i+1:]:
            if (r1 & ~a2) == 0:
                key = (nlines[F6], share[F6], tuple(sorted([(nlines[a1], share[a1]), (nlines[a2], share[a2])])))
                cost = 2.0 / share[F6] + sum((k + 1.0) / k for k in (share[a1], share[a2]))
                best[key] = cost
for key, cost in sorted(best.items(), key=lambda kv: kv[1]):
    print('F6 (lines %d, shared %d)  dedicated %s  -> per-target level-6 registers >= %.3f  (x120 = %.0f)' % (key[0], key[1], key[2], cost, 120 * cost))
