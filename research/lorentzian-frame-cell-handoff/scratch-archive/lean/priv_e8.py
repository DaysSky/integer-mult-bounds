"""E8 (= I_{9,1} odd-or-zero lines) check: for a good 4-frame and each section, is the private set covered by two
flats shared with FOREIGN sections (no common target)?  Exhaustive over orthogonal pairs."""
import sys, itertools, collections
sys.path.insert(0, '../lword')
from geom import Geom
import numpy as np
g = Geom(9); V = g.V; G = g.G
print('v', V, 'h', g.h)
perp = [0] * V
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and G[t, s] == 0: m |= 1 << s
    perp[t] = m
pc = lambda m: bin(m).count('1')
def name(s): return g.kind[s] + ''.join('%x' % i for i in g.supp[s])
orth = [set(np.nonzero(G[t] == 0)[0].tolist()) - {t} for t in range(V)]
allsec = [(p, q) for p in range(V) for q in orth[p] if p < q]
frames = []
for a in range(V):
    for b in orth[a]:
        if b <= a: continue
        for c in orth[a] & orth[b]:
            if c <= b: continue
            for d in orth[a] & orth[b] & orth[c]:
                if d <= c: continue
                frames.append((a, b, c, d))
print('orthogonal 4-frames', len(frames), 'readers per line', pc(perp[0]))
seen = set()
for Phi in frames[:3000]:
    key = tuple(sorted(g.kind[x] for x in Phi))
    if key in seen: continue
    seen.add(key)
    for t, y in itertools.combinations(Phi, 2):
        o = [z for z in Phi if z not in (t, y)]
        sig = perp[t] & perp[y]
        P = sig & ~perp[o[0]] & ~perp[o[1]]
        fl = set()
        for (p, q) in allsec:
            if {p, q} & {t, y}: continue
            F = sig & perp[p] & perp[q] & P
            if F: fl.add(F)
        fl = sorted(fl, key=pc, reverse=True)
        keep = []
        for f in fl:
            if not any((f | k) == k for k in keep): keep.append(f)
        best = max([pc(a | b) for a, b in itertools.combinations(keep, 2)] + [pc(keep[0]) if keep else 0])
        print(' frame', [name(x) for x in Phi], 'section', name(t), name(y), 'lines', pc(sig), 'private', pc(P),
              'best foreign 2-cover', best, 'COVERED' if best == pc(P) else '')
