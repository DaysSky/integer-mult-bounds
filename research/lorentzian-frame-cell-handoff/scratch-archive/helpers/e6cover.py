import sys, collections, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; GI = e8.GI
t = 0
H = e8.HYP[t]
# an A2 through t: a line u with <t,u> = +-1, third line = t-u or t+u
u = [s for s in range(V) if abs(GI[t, s]) == 1][0]
A2 = e8.closure((1 << t) | (1 << u))[0]
E6 = e8.perp(A2)
print('A2 lines', e8.bits(A2), 'E6 lines', e8.popcount(E6), 'inside t^perp', E6 & ~H == 0)
rest = H & ~E6
print('readers outside E6:', e8.popcount(rest))
# all hyperplane sections of t^perp (6-dim flats), from sections2 growth
Hl = e8.bits(H)
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
# pairs of sections covering 'rest'
cov = [(m & rest) for m in secs]
best = collections.Counter()
pairs = []
for i in range(len(secs)):
    ci = cov[i]
    if e8.popcount(ci) < 14: continue
    for j in range(i+1, len(secs)):
        if (ci | cov[j]) == rest:
            key = tuple(sorted([(e8.popcount(secs[i]), e8.popcount(e8.perp(secs[i]))), (e8.popcount(secs[j]), e8.popcount(e8.perp(secs[j])))]))
            best[key] += 1
            pairs.append((i, j))
print('number of section pairs covering the 27:', len(pairs))
print('types (lines, sharing) of covering pairs:', dict(best))
