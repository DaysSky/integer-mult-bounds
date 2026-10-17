"""Coxeter element of W(E8) acting on the 120 lines: simple roots from a generic linear functional, product of the 8
simple reflections; save the permutation (cycle type should be 30^4)."""
import sys, json, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
import numpy as np
V = e8.V
roots = [np.array(r) for r in e8.ALL]
w = np.array([1.0, 2.1, 3.3, 4.7, 5.2, 6.9, 7.4, 8.15]) * np.array([1, 1.01, 0.99, 1.02, 0.98, 1.03, 0.97, 1.0])
pos = [r for r in roots if r @ w > 0]
posset = {tuple(r) for r in pos}
simple = []
for r in pos:
    dec = any(tuple(r - s) in posset for s in pos if not np.array_equal(s, r))
    if not dec: simple.append(r)
print('simple roots:', len(simple))
L = np.array(e8.LINES, dtype=float)
key = {}
for i, r in enumerate(e8.LINES):
    key[tuple(int(x) for x in r)] = i; key[tuple(-int(x) for x in r)] = i
def refl_perm(r):
    r = np.array(r, dtype=float); rr = r @ r
    return [key[tuple(int(round(z)) for z in (L[i] - 2 * (L[i] @ r) / rr * r))] for i in range(V)]
p = list(range(V))
for s in simple:
    q = refl_perm(s); p = [q[p[i]] for i in range(V)]
def cycles(p):
    seen = [False] * V; c = []
    for i in range(V):
        if seen[i]: continue
        n = 0; j = i
        while not seen[j]: seen[j] = True; j = p[j]; n += 1
        c.append(n)
    return collections.Counter(c)
print('cycle type on lines:', cycles(p))
json.dump({'perm': p}, open('coxeter.json', 'w'))
