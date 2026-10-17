"""best_*.json (Young-orbit form) -> explicit line list {eta, R, S} in R^{n,1}."""
import json, sys, itertools
from sympy.utilities.iterables import multiset_permutations
src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src)); n = d['n']; blocks = d['blocks']
lines = {}
for cmb, y in d["orbits"]:

    per = [list(multiset_permutations(sorted(c))) for c in cmb]
    for parts in itertools.product(*per):
        x = [a for p in parts for a in p]
        v = tuple(x + [y]); nv = tuple(-a for a in v)
        lines[max(v, nv)] = 1
R = [list(map(float, v)) for v in sorted(lines)]
eta = [[(1.0 if i == j and i < n else (-1.0 if i == j else 0.0)) for j in range(n + 1)] for i in range(n + 1)]
json.dump(dict(eta=eta, R=R, S=[[int(a) for a in r] for r in R]), open(dst, 'w'))
print(src, '->', len(R), 'lines (expected', d['lines'], ')')
