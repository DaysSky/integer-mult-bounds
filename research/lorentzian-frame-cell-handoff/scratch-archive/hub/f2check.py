import sys, pickle, itertools, random
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
def vec(x):
    m = 0
    for i in g.supp[x]: m |= 1 << i
    if g.kind[x] == 'T': m |= 1 << 11
    return m
vv = [vec(x) for x in range(V)]
dot = lambda a, b: bin(a & b).count('1') & 1
# 1. orthogonality <-> F2 dot = 0
ok = all((G[i, j] == 0) == (dot(vv[i], vv[j]) == 0) for i in range(V) for j in range(V) if i != j)
print('distinct-line orthogonality == F2 dot 0:', ok, '| distinct vectors:', len(set(vv)))
# 2. good frames == orthogonal 4-sets with vector sum 0
good = set(tuple(sorted(q)) for q in pickle.load(open('../part/good4.pkl', 'rb')))
quads = pickle.load(open('../part/quads.pkl', 'rb'))
z = set(tuple(sorted(q)) for q in quads if vv[q[0]] ^ vv[q[1]] ^ vv[q[2]] ^ vv[q[3]] == 0)
print('good frames == zero-sum orthogonal 4-sets:', z == good, len(z), len(good))
# 3. identity N(V) = sum_{w in D*} N(V+w)
def span(gens):
    S = {0}
    for x in gens: S |= {s ^ x for s in S}
    return S
def N(Vs): return sum(1 << l for l in range(V) if all(dot(vv[l], u) == 0 for u in Vs))
rng = random.Random(1); bad = 0
for _ in range(300):
    gens = [rng.randrange(1, 1 << 12) for _ in range(rng.randint(1, 3))]
    Vs = span(gens)
    while True:
        a, b = rng.randrange(1, 1 << 12), rng.randrange(1, 1 << 12)
        if len(span(gens + [a, b])) == 4 * len(Vs): break
    lhs = N(Vs); rhs = N(span(gens + [a])) ^ N(span(gens + [b])) ^ N(span(gens + [a ^ b]))
    bad += lhs != rhs
print('identity N(V) = N(V+a)+N(V+b)+N(V+a+b) failures:', bad, '/ 300')
pickle.dump(vv, open('vv.pkl', 'wb'))
