"""Simulated annealing over I_{11,1} good-frame partitions (<= 4 punctured lines) minimising misalignment = number of
odd (E-set, frame) pairs + odd (Q, frame) pairs.  Move: remove k random frames (k = 2..4), re-cover their lines plus
the punctured lines by a random exact cover with good frames (allowing up to 4 punctures).
usage: misalign_sa.py START.pkl ITERS SEED"""
import sys, random, itertools, pickle, math, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
frames_all = pickle.load(open('halfglobal_11.pkl', 'rb'))['frames']
OM = [0] * V
for i in range(V):
    for j in range(V):
        if i != j and G[i, j] == 0: OM[i] |= 1 << j
FM = {f: sum(1 << u for u in f) for f in frames_all}
byline = collections.defaultdict(list)
for f in frames_all:
    for u in f: byline[u].append(f)
EQ = {}
def eq(f):
    if f not in EQ:
        out = []
        for t, e in itertools.combinations(f, 2):
            k, l = [x for x in f if x not in (t, e)]
            out.append(OM[t] & OM[e] & ~OM[k] & ~OM[l] & ~(1 << k) & ~(1 << l))
        out.append(OM[f[0]] & OM[f[1]] & OM[f[2]] & OM[f[3]])
        EQ[f] = out
    return EQ[f]
def pc(x): return bin(x).count('1') & 1
def pair_cost(f1, f2, live):
    m2 = FM[f2]; m1 = FM[f1]
    return sum(pc(E & live & m2) for E in eq(f1)) + sum(pc(E & live & m1) for E in eq(f2))
def total(part, pun):
    live = ((1 << V) - 1) & ~sum(1 << u for u in pun)
    return sum(pair_cost(a, b, live) for a, b in itertools.combinations(part, 2))
def recover(lines, rng, maxpun):
    """random exact cover of 'lines' (set) by good frames inside it, leaving <= maxpun uncovered"""
    lines = set(lines); out = []
    order = sorted(lines); rng.shuffle(order)
    def rec(rem, acc, pun):
        if not rem: return acc, pun
        u = min(rem, key=lambda x: len([f for f in byline[x] if set(f) <= rem]))
        cands = [f for f in byline[u] if set(f) <= rem]; rng.shuffle(cands)
        for f in cands[:6]:
            r = rec(rem - set(f), acc + [f], pun)
            if r: return r
        if len(pun) < maxpun:
            return rec(rem - {u}, acc, pun + [u])
        return None
    return rec(lines, [], [])
start, iters, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
part, pun = pickle.load(open(start, 'rb')); part = [tuple(sorted(f)) for f in part]
rng = random.Random(seed)
cur = total(part, pun); best = cur; print('start misalignment', cur, flush=True)
T0 = float(sys.argv[4]) if len(sys.argv) > 4 else 30.0
for it in range(iters):
    T = T0 * (1 - it / iters) + 0.5
    k = rng.choice([2, 2, 3, 3, 4])
    rm = rng.sample(range(len(part)), k)
    lines = set(u for i in rm for u in part[i]) | set(pun)
    r = recover(lines, rng, 4)
    if not r: continue
    newf, newp = r
    if len(newp) > 4: continue
    cand = [f for i, f in enumerate(part) if i not in rm] + newf
    c = total(cand, newp)
    if c <= cur or rng.random() < math.exp((cur - c) / T):
        part, pun, cur = cand, newp, c
        if c < best:
            best = c; pickle.dump((part, pun), open('misalign_best_%d.pkl' % seed, 'wb'))
    if it % 200 == 0: print('it', it, 'cur', cur, 'best', best, 'T %.1f' % T, flush=True)
print('best', best)
