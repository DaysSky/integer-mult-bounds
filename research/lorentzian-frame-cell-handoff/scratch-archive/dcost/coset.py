# Cheaper retained pieces for the B0 decoder: find >= 12 low-rank line sets in ONE coset of C_11 (row space of B0)
# whose pairwise sums span C_11.  Then B0 = S P with P = those pieces, cost = sum of their frame ranks (vs 110).
import sys, itertools, numpy as np, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
lab = np.array([[(g.binlabel(t) >> i) & 1 for i in range(11)] for t in range(V)], dtype=np.uint8)
C11 = [int(''.join(map(str, lab[:, i][::-1])), 2) for i in range(11)]       # D10 indicators as ints (bit u = line u)
# reduced basis of C_11 for syndrome computation: reduce a vector modulo C_11
piv = {}
for b in C11:
    x = b
    while x:
        hb = x.bit_length() - 1
        if hb in piv: x ^= piv[hb]
        else: piv[hb] = x; break
def red(x):
    while True:
        changed = False
        for hb in sorted(piv, reverse=True):
            if (x >> hb) & 1: x ^= piv[hb]; changed = True
        if not changed: return x
def mask(ls): return sum(1 << u for u in ls)
P = lambda a, b: g.P(a, b); T = lambda a, b, c: g.T(a, b, c)
cands = {}
def add(name, m):
    if m == 0: return
    F = closure(m); r = dim(F)
    if r <= 9 and nondegenerate(F): cands.setdefault(m, (name, r))
pts = range(11)
D10 = [mask([P(a, b) for a, b in itertools.combinations([j for j in pts if j != i], 2)] + [T(a, b, i) for a, b in itertools.combinations([j for j in pts if j != i], 2)]) for i in pts]
for i, j in itertools.combinations(pts, 2):
    add('D10cap%d%d' % (i, j), D10[i] & D10[j]); add('D10minus%d%d' % (i, j), D10[i] & ~D10[j]); add('D10minus%d%d' % (j, i), D10[j] & ~D10[i])
for t in range(V):
    for i in pts:
        if (D10[i] >> t) & 1: add('perpD10', g.HYP[t] & D10[i])
for h in pts:
    for S in itertools.combinations([j for j in pts if j != h], 9):
        add('Kstar9', mask([P(a, b) for a, b in itertools.combinations(S, 2)] + [T(h, a, b) for a, b in itertools.combinations(S, 2)]))
    for S in itertools.combinations([j for j in pts if j != h], 8):
        add('Kstar8', mask([P(a, b) for a, b in itertools.combinations(S, 2)] + [T(h, a, b) for a, b in itertools.combinations(S, 2)]))
for S in itertools.combinations(pts, 8):
    add('L8', mask([P(a, b) for a, b in itertools.combinations(S, 2)] + [T(a, b, c) for a, b, c in itertools.combinations(S, 3)]))
for t in range(V):
    for u in range(t + 1, V):
        if g.G[t, u] == 0: add('plane', g.HYP[t] & g.HYP[u])
print('candidates', len(cands), collections.Counter(v[0].rstrip('0123456789') for v in cands.values()))
by = collections.defaultdict(list)
for m, (nm, r) in cands.items(): by[red(m)].append((r, m, nm))
def span_ok(items):
    # do pairwise sums of items span C_11 ?
    base = items[0][1]; vecs = [base ^ it[1] for it in items[1:]]
    pv = {}
    for x in vecs:
        while x:
            hb = x.bit_length() - 1
            if hb in pv: x ^= pv[hb]
            else: pv[hb] = x; break
    return len(pv) >= 11
best = []
for syn, items in by.items():
    if syn == 0 or len(items) < 12: continue
    items.sort()
    # greedy: cheapest items that increase the span of differences
    chosen = [items[0]]; pv = {}; cost = items[0][0]
    for it in items[1:]:
        x = chosen[0][1] ^ it[1]
        while x:
            hb = x.bit_length() - 1
            if hb in pv: x ^= pv[hb]
            else: pv[hb] = x; break
        if x: chosen.append(it); cost += it[0]
        if len(pv) == 11: break
    if len(pv) == 11: best.append((cost, len(chosen), syn, collections.Counter(c[2].rstrip('0123456789') for c in chosen)))
best.sort()
print('cosets with >= 12 low-rank members:', sum(1 for s, it in by.items() if s and len(it) >= 12), '| spanning ones:', len(best))
for b in best[:10]: print('  cost', b[0], 'pieces', b[1], b[3])
