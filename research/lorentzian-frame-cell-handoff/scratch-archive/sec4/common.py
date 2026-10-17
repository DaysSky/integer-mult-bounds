"""Shared E8 data for the 4-section search: lines, Z15 action, design planes, D4s, incidences."""
import sys, json, itertools, collections, pickle, os
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; GI = e8.GI
pc = lambda m: bin(m).count('1')
HERE = os.path.dirname(os.path.abspath(__file__))
perm = json.load(open(os.path.join(HERE, 'coxeter.json')))['perm']
planes = [int(h, 16) for h in json.load(open(os.environ.get('DESIGN', os.path.join(HERE, 'design.json'))))['planes']]
def act(mask):
    m = 0
    for s in e8.bits(mask): m |= 1 << perm[s]
    return m
def perpmask(F):
    m = (1 << V) - 1
    for s in e8.bits(F): m &= e8.HYP[s]
    return m
def load_d4():
    p = os.path.join(HERE, 'd4.pkl')
    if os.path.exists(p): return pickle.load(open(p, 'rb'))
    orth = [set(e8.ORTH[a]) for a in range(V)]
    D4 = set()
    for a in range(V):
        for b in orth[a]:
            if b <= a: continue
            for c in orth[a] & orth[b]:
                if c <= b: continue
                for d in orth[a] & orth[b] & orth[c]:
                    if d <= c: continue
                    F, r = e8.closure((1 << a) | (1 << b) | (1 << c) | (1 << d))
                    if pc(F) == 12: D4.add(F)
    D4 = sorted(D4)
    pickle.dump(D4, open(p, 'wb'))
    return D4
def orbit(x):
    o = [x]; y = act(x)
    while y != x: o.append(y); y = act(y)
    return o
line_rep = {}
for s in range(V):
    if s in line_rep: continue
    x = s; k = 0
    while True:
        line_rep[x] = (s, k)   # x = c^k (s)
        x = perm[x]; k += 1
        if x == s: break
reps = sorted(set(r for r, k in line_rep.values()))
