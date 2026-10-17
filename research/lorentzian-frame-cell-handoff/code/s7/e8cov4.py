import numpy as np, itertools
from e8geo import e8_roots
L = e8_roots(); n = len(L)
cands = []
for c in itertools.product(range(-2, 3), repeat=8):
    if sum(c) % 2 == 0 and 0 < sum(x*x for x in c) <= 8: cands.append(tuple(2*x for x in c))
for c in itertools.product((-3, -1, 1, 3), repeat=8):
    if sum(x*x for x in c) <= 32 and sum(c) % 4 == 0: cands.append(tuple(c))
Z = np.array(cands); P = (L @ Z.T) == 0
masks = {}
for j in range(Z.shape[0]):
    m = 0
    for i in np.nonzero(P[:, j])[0]: m |= 1 << int(i)
    if bin(m).count('1') >= 20 and m not in masks: masks[m] = j
ms = list(masks); FULL = (1 << n) - 1
pc = lambda m: bin(m).count('1')
print('sets', len(ms), flush=True)
# case A: first = E7 (root perp) - fix one root
r0 = next(m for m in ms if pc(m) == 63)
rest = FULL & ~r0
cand = [m for m in ms if pc(m & rest) >= (pc(rest) + 1) // 2]
print('case E7: uncovered', pc(rest), 'candidates covering >= half', len(cand), flush=True)
found = None
allm = ms
for a in cand:
    need = rest & ~a
    for b in allm:
        if b & need == need: found = (r0, a, b); break
    if found: break
print('case E7 3-cover:', 'FOUND' if found else 'none', flush=True)
# case B: all three of size <= 42 -> need three D7-type (42) sets
d7 = [m for m in ms if pc(m) == 42]
print('D7-type sets', len(d7), flush=True)
fB = None
a = d7[0]   # D7 sets form one orbit under W(E8)? (assume; check sizes only) -- try all a anyway if small
for a in d7:
    rest = FULL & ~a
    c2 = [m for m in d7 if pc(m & rest) >= 39]
    for b in c2:
        need = rest & ~b
        if pc(need) > 42: continue
        for c in d7:
            if c & need == need: fB = (a, b, c); break
        if fB: break
    if fB: break
print('case D7^3 3-cover:', 'FOUND' if fB else 'none', flush=True)
