"""Optimise the parts of the M11 triangle top (lttri_design_z11.json) for minimum node waste (exact node model).
Per T line A (nodes n = (A,B,C,E)): f_A(n) = A2(B)+A2(C)+P(E) is forced; single-crossing pairs give full A-fibres
at their node; for each doubly-crossing pair and each a in A choose which of the 2 nodes delivers T(a,pair) (odd
count = 1); own A2(A) at an odd subset (1 or 3) of the 4 nodes; one in-chain node.  Node waste = m - d with
d = dim span(delivered parts), m = s if the rank-<=RHO vectors of S span S else s+1 (lower bound; upper 2s-g also
reported).  Simulated annealing over the discrete choices.  usage: lttri_opt.py RHO minutes seed"""
import sys, json, itertools, random, math, time, collections
from lgeo import *
RHO = int(sys.argv[1]); MIN = float(sys.argv[2]); random.seed(int(sys.argv[3])); t0 = time.time()
sol = [tuple(tuple(T) for T in node) for node in json.load(open('lttri_design_z11.json'))]
def Ln(k, pts): return IDX[(k, tuple(sorted(pts)))]
def A2(T): return sum(1 << Ln('P', p) for p in itertools.combinations(T, 2))
nodes_of = collections.defaultdict(list)
for ni, node in enumerate(sol):
    for T in node: nodes_of[T].append(ni)
lines = sorted(nodes_of)
info = {}
for A in lines:
    D = [x for x in range(11) if x not in A]; nis = nodes_of[A]
    base = {}; fib = {}
    for ni in nis:
        B, C = [T for T in sol[ni] if T != A]; E = tuple(x for x in D if x not in B and x not in C)
        base[ni] = A2(B) | A2(C) | (1 << Ln('P', E))
    single = collections.defaultdict(int); dbl = []
    for p in itertools.combinations(D, 2):
        opts = []
        for ni in nis:
            B, C = [T for T in sol[ni] if T != A]
            if (p[0] in B and p[1] in C) or (p[0] in C and p[1] in B): opts.append(ni)
        if len(opts) == 1:
            for a in A: single[opts[0]] |= 1 << Ln('T', (a,) + p)
        else:
            dbl.append((p, opts))
    info[A] = dict(nis=nis, base=base, single=single, dbl=dbl, a2=A2(A))
# state
st = {}
for A in lines:
    I = info[A]
    st[A] = dict(dch={(p, a): random.choice(opts) for p, opts in I['dbl'] for a in A},
                 own=random.choice([[n] for n in I['nis']] + [list(c) for c in itertools.combinations(I['nis'], 3)]),
                 inch=random.choice(I['nis']))
def part(A, ni):
    I = info[A]; S = st[A]; m = I['base'][ni] | I['single'][ni]
    if ni in S['own']: m |= I['a2']
    for (p, a), n in S['dch'].items():
        if n == ni: m |= 1 << Ln('T', (a,) + p)
    return m
RK = {}
def srank(v):
    if v not in RK: RK[v] = rank(v)
    return RK[v]
def basis(vs):
    b = []
    for v in vs:
        for x in b:
            if v ^ x < v: v ^= x
        if v: b.append(v); b.sort(reverse=True)
    return b
def node_cost(ni):
    users = sol[ni]
    ps = {X: part(X, ni) for X in users}
    deliv = [ps[X] for X in users if st[X]['inch'] != ni]
    B = basis(list(ps.values())); s = len(B); d = len(basis(deliv))
    span = [0]
    for b in B: span = span + [v ^ b for v in span]
    g = len(basis([v for v in span if v and srank(v) <= RHO]))
    return (s if g == s else s + 1) - d, (s if g == s else 2 * s - g) - d
cost = {ni: node_cost(ni) for ni in range(len(sol))}
cur = sum(c[0] for c in cost.values()); best = cur
print('[%4.0fs] init waste %d (upper %d)' % (time.time() - t0, cur, sum(c[1] for c in cost.values())), flush=True)
it = 0
while time.time() - t0 < MIN * 60:
    it += 1
    A = random.choice(lines); I = info[A]; S = st[A]
    r = random.random()
    if r < 0.6 and I['dbl']:
        p, opts = random.choice(I['dbl']); a = random.choice(A); key = (p, a); old = ('d', key, S['dch'][key])
        S['dch'][key] = random.choice([o for o in opts if o != S['dch'][key]]); touched = set(opts)
    elif r < 0.8:
        old = ('o', None, S['own']); S['own'] = random.choice([[n] for n in I['nis']] + [list(c) for c in itertools.combinations(I['nis'], 3)]); touched = set(I['nis'])
    else:
        old = ('i', None, S['inch']); S['inch'] = random.choice(I['nis']); touched = {old[2], S['inch']}
    newc = {ni: node_cost(ni) for ni in touched}
    delta = sum(newc[ni][0] - cost[ni][0] for ni in touched)
    T = 2.0 * (0.02) ** ((time.time() - t0) / (MIN * 60))
    if delta <= 0 or random.random() < math.exp(-delta / T):
        for ni in touched: cost[ni] = newc[ni]
        cur += delta
        if cur < best:
            best = cur
            if it % 50 == 0 or best < 150: print('[%4.0fs] it %d waste %d (upper %d)' % (time.time() - t0, it, best, sum(c[1] for c in cost.values())), flush=True)
    else:
        kind, key, val = old
        if kind == 'd': S['dch'][key] = val
        elif kind == 'o': S['own'] = val
        else: S['inch'] = val
print('[%4.0fs] done: best waste %d, final %d (upper %d), iterations %d; node waste histogram %s' % (time.time() - t0, best, cur, sum(c[1] for c in cost.values()), it,
      sorted(collections.Counter(c[0] for c in cost.values()).items())), flush=True)
