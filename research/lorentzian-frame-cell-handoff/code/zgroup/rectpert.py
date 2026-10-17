"""Per-target feasibility: is R(t) a mod-2 sum of family demands d with d inside t-perp?  Also the minimum number of
demands per target by greedy/elimination (upper bound).  usage: rectpert.py FAMILIES"""
import sys, itertools, collections
exec(open('rectcover.py').read().split("pairs = [")[0])
def Kset(h, S): return [P(a, b) for a, b in itertools.combinations(S, 2)] + [T(a, b, h) for a, b in itertools.combinations(S, 2)]
def Lset(S): return [P(a, b) for a, b in itertools.combinations(S, 2)] + [T(*c) for c in itertools.combinations(S, 3)]
fams = sys.argv[1].split(',')
dem = set()
for h in range(11):
    rest = [i for i in range(11) if i != h]
    for k in (2, 3, 4, 5, 6, 7, 8):
        if 'K%d' % k in fams:
            for S in itertools.combinations(rest, k): dem.add(sum(1 << u for u in Kset(h, S)))
for k in (3, 4, 5, 6, 7, 8):
    if 'L%d' % k in fams:
        for S in itertools.combinations(range(11), k): dem.add(sum(1 << u for u in Lset(S)))
dem = list(dem)
ok = 0; ranks = collections.Counter()
for t in range(V):
    Rt = OM[t]
    ds = [d for d in dem if d & ~Rt == 0]
    basis = {}
    for d in ds:
        x = d
        while x:
            p = x.bit_length() - 1
            if p in basis: x ^= basis[p]
            else: basis[p] = x; break
    x = Rt
    while x:
        p = x.bit_length() - 1
        if p in basis: x ^= basis[p]
        else: break
    ok += (x == 0); ranks[(g.kind[t], len(ds), len(basis), x == 0)] += 1
print('families', fams, 'targets with R(t) in span:', ok, 'of', V)
for k, c in sorted(ranks.items()): print('  (kind, #demands inside t-perp, span rank, feasible):', k, c)
