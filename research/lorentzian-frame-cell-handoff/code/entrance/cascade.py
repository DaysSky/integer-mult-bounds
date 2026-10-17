"""Coordinated frame lifting: merge two consecutive frame segments of one register's chain by lifting every gate of the
lower segment to the next segment's frame; other operands of a lifted gate whose next gate is not above the new frame get
that next gate lifted to the closure of the union (forward cascade).  Hard bounds: D gates fixed (frame 0); the last A gate
of every retained total fixed (COPY rank); every gate below the final frame of each of its registers (targets: t-perp).
Objective: local paid fee sum_moves phi_q(r), phi_q(r) = r((64/r)^q - 1), q fixed.  Greedy best-improvement to a fixed point.
usage: cascade.py IN.json.gz OUT.json.gz [q]"""
import sys, gzip, json, math, copy
from collections import Counter, defaultdict
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-p111-tuned/tune')
import tune as TU

inp, out = sys.argv[1], sys.argv[2]
q = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0017343
w = json.load(gzip.open(inp, 'rt'))
v, R = w['v'], w['R']; n = 2 * v + R
cat = TU.Cat(w)
phi = lambda r: r * math.expm1(q * math.log(64 / r)) if r > 0 else 0.0
FULL = next(i for i, f in enumerate(w['frames']) if len(f) == v)
G = [[sec, list(g)] for sec in ('D', 'A', 'B') for g in w[sec]]   # gate: [sec, [f, d, srcs]]
NG = len(G)
chain = defaultdict(list)
for i, (sec, (f, d, srcs)) in enumerate(G):
    for r in [d] + srcs:
        if not chain[r] or chain[r][-1] != i: chain[r].append(i)
pos = defaultdict(dict)
for r, ch in chain.items():
    for k, i in enumerate(ch): pos[r][i] = k
ret = set(w['ret'])
fixed = set(i for i, (sec, g) in enumerate(G) if sec == 'D')
for r in ret:
    lastA = [i for i in chain[r] if G[i][0] == 'A']
    if lastA: fixed.add(lastA[-1])
final = w['final']; start = w['start']
regs_of = [[g[1]] + g[2] for sec, g in G]
M = lambda f: cat.masks[f]
le = lambda a, b: M(a) & ~M(b) == 0


def reg_cost(r, fr):
    c = 0.0; prev = start[r]
    for i in chain[r] + [None]:
        f = final[r] if i is None else fr[i]
        if f != prev:
            c += phi(cat.dim[f] - cat.dim[prev]); prev = f
    return c


fr = [g[0] for sec, g in G]
cost = {r: reg_cost(r, fr) for r in chain}
total = sum(cost.values())
print('initial local fee %.6f' % total, flush=True)


def cascade(lifts):
    """lifts: dict gate -> new frame (proposed).  Returns dict of all changed gates or None if infeasible."""
    new = dict(lifts); queue = list(lifts)
    while queue:
        i = queue.pop()
        F = new[i]
        if i in fixed and F != fr[i]: return None
        for r in regs_of[i]:
            if not le(F, final[r]): return None
            k = pos[r][i]
            if k + 1 < len(chain[r]):
                j = chain[r][k + 1]
                Fj = new.get(j, fr[j])
                if not le(F, Fj):
                    Fn = cat.closure(M(F) | M(Fj))
                    if j in fixed: return None
                    new[j] = Fn; queue.append(j)
    return new


def delta(new):
    regs = set(r for i in new for r in regs_of[i])
    trial = list(fr)
    for i, F in new.items(): trial[i] = F
    d = 0.0; nc = {}
    for r in regs:
        c = reg_cost(r, trial); nc[r] = c; d += c - cost[r]
    return d, nc


it = 0
while True:
    best = None
    for r, ch in chain.items():
        # segments of r: runs of equal frames along ch
        segs = []
        for i in ch:
            if segs and fr[segs[-1][-1]] == fr[i]: segs[-1].append(i)
            else: segs.append([i])
        for s in range(len(segs) - 1):
            F = fr[segs[s + 1][0]]
            lifts = {i: F for i in segs[s]}
            new = cascade(lifts)
            if new is None: continue
            d, nc = delta(new)
            if d < -1e-12 and (best is None or d < best[0]): best = (d, new, nc)
    if best is None: break
    d, new, nc = best
    for i, F in new.items(): fr[i] = F
    cost.update(nc); total += d; it += 1
    if it % 10 == 0 or it < 10:
        print('it %d: delta %.6f (%d gates) total %.6f' % (it, d, len(new), total), flush=True)
print('final local fee %.6f after %d moves' % (total, it))
# export
for i, (sec, g) in enumerate(G): g[0] = fr[i]
nw = copy.deepcopy(w)
cat.export(nw)
for sec in ('D', 'A', 'B'): nw[sec] = [g for s, g in G if s == sec]
nw['C'] = TU.wlib.rebuild_C(nw)
data = gzip.compress(json.dumps(nw, sort_keys=True, separators=(',', ':')).encode(), compresslevel=9, mtime=0)
data = data[:9] + bytes([255]) + data[10:]
open(out, 'wb').write(data)
import wlib
print('profile', wlib.paid(nw))
