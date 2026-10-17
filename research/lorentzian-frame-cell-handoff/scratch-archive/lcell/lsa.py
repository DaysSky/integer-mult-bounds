"""Local search over Z11-invariant good-frame source systems minimising the free-top counting bound
R_lb = 440 + defects + sum_j_lb (doubly forced k_C with nondegenerate rank-3 nodes, <= 220 cell readers).
Fast scoring with bitmask caches.  Start from a json system; moves = change one rep's frame."""
import sys, os, json, random, math, pickle
os.environ['GRP'] = '11'
from lbase import *
fr = goodframes()
covers = {a: [F & ~(1 << a) for F in fr if F >> a & 1] for a in range(V)}
rep_of = {a: min(p[a] for p in PERMS) for a in range(V)}
reps = sorted(set(rep_of.values()))
pmap = {a: next(p for p in PERMS if p[rep_of[a]] == a) for a in range(V)}
PERP = {}
def perpm(m):
    if m not in PERP: PERP[m] = perp(m)
    return PERP[m]
NODEP = {}
def node_perps(C):
    """perps (target masks) of nondegenerate rank-3 nodes closure(C + x)"""
    if C not in NODEP:
        ps = set()
        for x in range(V):
            if C >> x & 1: continue
            N = closure(C | (1 << x))
            if nondeg_span(N): ps.add(perpm(N))
        NODEP[C] = list(ps)
    return NODEP[C]
def system(choice):
    return {a: act(covers[rep_of[a]][choice[rep_of[a]]], pmap[a]) for a in range(V)}
def score(choice):
    cov = system(choice)
    defects = sum(1 for a in range(V) for b in bits(cov[a]) if not cov[b] >> a & 1)
    cells = set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a]))
    cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
    ks = []; memo = {}
    for C in cells:
        s, a = list(bits(C))
        others = 0
        for c in cells_of[s] + cells_of[a]:
            if c != C: others |= perpm(c)
        T = perpm(C) & ~others
        if not T: ks.append(0); continue
        nT = bin(T).count('1')
        best = max([bin(T & q).count('1') for q in node_perps(C)] + [0])
        ks.append(nT - best)
    free0 = sum(1 for k in ks if k == 0); pool = V; cnt = 0
    for k in sorted(k for k in ks if k > 0):
        if pool >= k: pool -= k; cnt += 1
    jlb = len(cells) - free0 - cnt
    return 440 + defects + jlb, defects, jlb
start = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
choice = {r: covers[r].index(start[r]) for r in reps}
iters = int(sys.argv[2]); seed = int(sys.argv[3]); random.seed(seed); T0 = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0
cur = score(choice); best = cur; bestc = dict(choice)
print('start', cur, flush=True)
for it in range(iters):
    r = random.choice(reps); old = choice[r]
    choice[r] = random.randrange(len(covers[r]))
    new = score(choice)
    T = T0 * (1 - it / iters) + 0.05
    if new[0] <= cur[0] or random.random() < math.exp((cur[0] - new[0]) / T):
        cur = new
        if new[0] < best[0]:
            best = new; bestc = dict(choice)
            json.dump({str(a): v for a, v in system(bestc).items()}, open('lsa_best_%d.json' % seed, 'w'))
            print('it', it, 'best', best, flush=True)
    else:
        choice[r] = old
print('final best', best, flush=True)
