"""O^-(8,2) nonsingular points relative to one maximal B-isotropic 4-space W: cosets of W, supports, parallel pairs."""
import itertools, numpy as np
def q(x): return (x[0]*x[1] + x[2]*x[3] + x[4]*x[5] + x[6] + x[6]*x[7] + x[7]) % 2
def B(x, y): return (q(tuple((a + b) % 2 for a, b in zip(x, y))) + q(x) + q(y)) % 2
V = list(itertools.product((0, 1), repeat=8))
pts = [x for x in V if any(x) and q(x) == 1]
idx = {p: i for i, p in enumerate(pts)}
# find a maximal totally isotropic subspace W (dim 4) by greedy search
def span(gens):
    S = {tuple([0] * 8)}
    for g in gens: S |= {tuple((a + b) % 2 for a, b in zip(s, g)) for s in S}
    return S
import random
random.seed(1)
while True:
    gens = []
    for x in random.sample(V, len(V)):
        if not any(x): continue
        if all(B(x, g) == 0 for g in gens) and x not in span(gens): gens.append(x)
        if len(gens) == 4: break
    if len(gens) == 4: break
W = sorted(span(gens)); frame = [w for w in W if q(w) == 1]
print('W size', len(W), 'frame points', len(frame), 'mutually orthogonal', all(B(a, b) == 0 for a in frame for b in frame))
others = [p for p in pts if p not in frame]
sig = lambda p: tuple(B(p, u) for u in frame)
groups = {}
for p in others: groups.setdefault(sig(p), []).append(p)
print('support patterns', len(groups), sorted(sum(s) for s in groups), [len(g) for g in groups.values()])
# parallel supports (disjoint) : B constant?
keys = list(groups)
for a, b in itertools.combinations(keys, 2):
    if sum(a) == 4 and sum(b) == 4 and not any(x & y for x, y in zip(a, b)):
        vals = {B(p, r) for p in groups[a] for r in groups[b]}
        print('parallel pair', a, b, 'B values', vals)
