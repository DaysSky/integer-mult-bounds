"""Eisenstein structure on the skeleton's E8 lines: a fixed-point-free order-3 Weyl element omega (product of the four
A2 rotations of an A2^4 subsystem); its line orbits = 40 Eisenstein A2 planes.  Saves eis8.pkl."""
import sys, itertools, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
import numpy as np
L = np.array(e8.LINES, dtype=np.int64); V = e8.V
n2 = int(L[0] @ L[0]); assert all(int(x @ x) == n2 for x in L)
G = L @ L.T
def refl(r):
    return lambda x: x - 2 * (x @ r) * r // n2
# A2^4: greedy
def find_a2s():
    for a in range(V):
        for b in range(V):
            if G[a, b] != -n2 // 2 and G[a, b] != n2 // 2: continue
            chosen = [(a, b)]
            used = {a, b}
            def ok(c):
                return all(G[c, x] == 0 for p in chosen for x in p)
            def rec():
                if len(chosen) == 4: return True
                for c in range(V):
                    if not ok(c): continue
                    for d in range(c + 1, V):
                        if abs(G[c, d]) == n2 // 2 and ok(d):
                            chosen.append((c, d))
                            if rec(): return True
                            chosen.pop()
                return False
            if rec(): return chosen
    return None
A = find_a2s(); print('A2^4 generators', A)
def omega(x):
    for (a, b) in A:
        x = refl(L[a])(refl(L[b])(x))
    return x
line_of = {}
for i, x in enumerate(L):
    line_of[tuple(x)] = i; line_of[tuple(-x)] = i
perm = [line_of[tuple(omega(L[i]))] for i in range(V)]
assert sorted(perm) == list(range(V))
assert all(perm[perm[perm[i]]] == i for i in range(V)) and all(perm[i] != i for i in range(V))
planes = sorted(set(tuple(sorted({i, perm[i], perm[perm[i]]})) for i in range(V)))
print('Eisenstein planes', len(planes))
assert all(abs(G[p[0], p[1]]) == n2 // 2 and abs(G[p[0], p[2]]) == n2 // 2 and abs(G[p[1], p[2]]) == n2 // 2 for p in planes)
pm = [sum(1 << i for i in p) for p in planes]
orth = [[j for j in range(40) if all(G[a, b] == 0 for a in planes[i] for b in planes[j])] for i in range(40)]
print('orthogonal Eisenstein planes per plane', collections.Counter(len(o) for o in orth))
# relation of non-orthogonal pairs
rel = collections.Counter()
for i in range(40):
    for j in range(i + 1, 40):
        rel[tuple(sorted(collections.Counter(int(abs(G[a, b])) for a in planes[i] for b in planes[j]).items()))] += 1
print('pair types', rel)
pickle.dump(dict(planes=planes, pm=pm, perm=perm, orth=orth, A=A), open('eis8.pkl', 'wb'))
