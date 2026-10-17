"""Helper-deletion experiment: remove k helpers from the canonical word's chains and re-solve mixing by ALS."""
import sys, time, numpy as np, random
from geo import *
from framenet import FrameNet
k = int(sys.argv[1]); seed = int(sys.argv[2]); sweeps = int(sys.argv[3]); mode = sys.argv[4] if len(sys.argv) > 4 else 'random'
c = load(); v = c['v']; F = c['frames']; n = 2 * v + c['R']
V = np.zeros((n, v))
for s in range(v): V[s, s] = 1
for part in ('A', 'B'):
    for e in c[part]:
        if e[0] == 'add': V[e[1]] += e[3] / e[4] * V[e[2]]
        else: V[e[1]] *= e[2] / e[3]
Mdf = V[v:2 * v].copy()
chains = [[] for _ in range(n)]
def visit(r, f):
    fb = tuple(basis(F[f]))
    if not chains[r] or chains[r][-1][1] != fb: chains[r].append((len(fb), fb))
for r in range(n): visit(r, c['start'][r])
for part in ('A', 'B'):
    for e in c[part]:
        for r in ([e[1], e[2]] if e[0] == 'add' else [e[1]]): visit(r, e[-1])
helpers = list(range(2 * v, n))
rng = random.Random(seed)
if mode == 'random':
    dele = set(rng.sample(helpers, k))
elif mode == 'fewgates':
    # delete helpers with the fewest gates first
    cnt = {h: 0 for h in helpers}
    for part in ('A', 'B'):
        for e in c[part]:
            for r in ([e[1], e[2]] if e[0] == 'add' else [e[1]]):
                if r in cnt: cnt[r] += 1
    dele = set(sorted(helpers, key=lambda h: (cnt[h], rng.random()))[:k])
regs = []
for r in range(n):
    if r in dele: continue
    t = 'X' if r < v else ('Y' if r < 2 * v else 'H')
    ch = [(d, f) for d, f in chains[r] if d > 0 or t != 'X']
    regs.append({'type': t, 'port': (r if r < v else (r - v if r < 2 * v else None)), 'chain': ch})
fn = FrameNet(regs, Mdf, v)
print('k', k, 'mode', mode, 'seed', seed, 'registers', len(regs), flush=True)
t0 = time.time()
res = fn.solve(sweeps=sweeps, verbose=True, seed=seed)
print('FINAL k', k, 'residual', res, 'min sv', fn.min_abs_det(), '%.0fs' % (time.time() - t0), flush=True)
