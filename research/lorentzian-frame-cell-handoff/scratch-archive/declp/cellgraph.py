"""Aligned cell graphs for I_{11,1}.  A cell graph H is a set of orthogonal line pairs.  Target t can assemble its
need t-perp from pair cells inside t-perp up to one single line per ODD component of H[t-perp]
(a component of even size has an odd-degree spanning subgraph; an odd one needs a single).
E8's R420 cell graph (30 disjoint K4) leaves exactly 1 odd component per target (its own frame).
Search: simulated annealing over H (start: the good-frame partition of blkpartA), cost
  sum_t oddcomp(H[t-perp]) + LAM * |H|.   usage: cellgraph.py LAM STEPS SEED [T0]"""
import sys, random, pickle, math, time
import numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
G = g.G
LAM, STEPS, seed = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); T0 = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
rnd = random.Random(seed)
perp = [[s for s in range(V) if s != t and G[t, s] == 0] for t in range(V)]
inperp = [set(p) for p in perp]
pairs = [(a, b) for a in range(V) for b in range(a + 1, V) if G[a, b] == 0]
users = {e: [t for t in range(V) if e[0] in inperp[t] and e[1] in inperp[t]] for e in pairs}
part = pickle.load(open('/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lbuild/blkpartA.pkl', 'rb'))
H = set()
for blk in part[0]:
    for fr in blk:
        for a, b in __import__('itertools').combinations(sorted(fr), 2):
            if G[a, b] == 0: H.add((a, b))
adj = {s: set() for s in range(V)}
for a, b in H: adj[a].add(b); adj[b].add(a)
def oddcomp(t):
    P = inperp[t]; seen = set(); odd = 0
    for s in perp[t]:
        if s in seen: continue
        stack = [s]; seen.add(s); n = 0
        while stack:
            u = stack.pop(); n += 1
            for w in adj[u]:
                if w in P and w not in seen: seen.add(w); stack.append(w)
        odd += n & 1
    return odd
oc = [oddcomp(t) for t in range(V)]
cur = sum(oc) + LAM * len(H); best = cur; bestH = set(H)
print('start: |H| %d, odd components total %d (per target %.2f), cost %.1f' % (len(H), sum(oc), sum(oc) / V, cur), flush=True)
t0 = time.time()
for step in range(STEPS):
    T = T0 * (1 - step / STEPS) + 1e-3
    if rnd.random() < 0.5 and H:
        e = rnd.choice(tuple(H)); add = False
    else:
        e = rnd.choice(pairs); add = e not in H
        if not add: continue
    a, b = e
    if add: adj[a].add(b); adj[b].add(a)
    else: adj[a].discard(b); adj[b].discard(a)
    aff = users[e]; new = {t: oddcomp(t) for t in aff}
    delta = sum(new[t] - oc[t] for t in aff) + (LAM if add else -LAM)
    if delta <= 0 or rnd.random() < math.exp(-delta / T):
        for t in aff: oc[t] = new[t]
        if add: H.add(e)
        else: H.discard(e)
        cur += delta
        if cur < best: best = cur; bestH = set(H)
    else:
        if add: adj[a].discard(b); adj[b].discard(a)
        else: adj[a].add(b); adj[b].add(a)
    if step % 20000 == 0:
        deg = [len(adj[s]) for s in range(V)]
        print('step %d T %.3f |H| %d odd total %d (per target %.2f, max %d) mean degree %.2f cost %.1f best %.1f  %.0fs' % (
            step, T, len(H), sum(oc), sum(oc) / V, max(oc), sum(deg) / V, cur, best, time.time() - t0), flush=True)
pickle.dump(sorted(bestH), open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/cellgraph_%s_%d.pkl' % (LAM, seed), 'wb'))
print('done best cost %.1f' % best, flush=True)
