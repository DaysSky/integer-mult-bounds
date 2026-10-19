"""Census on the r434: helpers X read exactly once (outside C) whose reader Y could absorb X's inputs at the
read frame G.  Input u qualifies when u is not written between X's gate and the read, u's frame at the read
is inside G, and u's next frame after the read (next gate frame or final) contains G."""
import json, os
from collections import Counter, defaultdict
from fractions import Fraction as Fr
from _common import I13
W = json.load(open(os.path.join(I13, 'ii19_pub2_p111-r434.json')))
v, h, R = W['v'], W['h'], W['R']; nreg = 2 * v + R
def rref(vs):
    m = [[Fr(x) for x in r] for r in vs]; rk = 0
    for c in range(h):
        p = next((i for i in range(rk, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[rk], m[p] = m[p], m[rk]; iv = 1 / m[rk][c]; m[rk] = [x * iv for x in m[rk]]
        for i in range(len(m)):
            if i != rk and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[rk])]
        rk += 1
    return m[:rk]
FR = [rref(F) if F else [] for F in W['frames']]
_s = {}
def sub(a, b):
    if a == b or not FR[a]: return True
    if (a, b) not in _s: _s[(a, b)] = len(rref(FR[a] + FR[b])) == len(FR[b])
    return _s[(a, b)]
seq = [('D', g) for g in W['D']] + [('A', g) for g in W['A']] + [('B', g) for g in W['B']]
# frame of every register after each gate position, and write positions
frame_at = []; cur = list(W['start'])
writes = defaultdict(list); reads = defaultdict(list); visits = defaultdict(list)
for pos, (ph, (F, d, srcs)) in enumerate(seq):
    for r in [d] + srcs:
        if cur[r] != F: visits[r].append((pos, F)); cur[r] = F
    writes[d].append(pos)
    if ph != "D":
        for s in srcs: reads[s].append((pos, d, F))
def frame_before(r, pos):           # frame of r just before gate pos
    f = W['start'][r]
    for p, F in visits[r]:
        if p < pos: f = F
        else: break
    return f
def next_frame_after(r, pos):
    for p, F in visits[r]:
        if p > pos: return F
    return W['final'][r]
TOT = set(W['ret'])
stats = Counter(); good = []
for X in range(2 * v, nreg):
    if X in TOT: continue
    rd = reads[X]
    if len(rd) != 1: stats['reads=%d' % min(len(rd), 4)] += 1; continue
    tpos, Y, G = rd[0]
    ins = [(pos, srcs) for pos, (ph, (F, d, srcs)) in enumerate(seq) if d == X and ph != 'D']
    ok = True; k = 0
    for pos, srcs in ins:
        for u in srcs:
            k += 1
            if any(pos < p < tpos for p in writes[u]): ok = False; break
            if not sub(frame_before(u, tpos), G): ok = False; break
            if not sub(G, next_frame_after(u, tpos)): ok = False; break
        if not ok: break
    stats['inlinable' if ok else 'blocked'] += 1
    if not ok: stats['blocked_reader_'+('target' if v <= Y < 2*v else 'helper')] += 1
    if ok: good.append((X, Y, k))
print('helpers (non-total):', sum(stats.values()), dict(stats))
print('inlinable: %d; inputs per inlinable helper: %s; reader kinds: %s' % (
    len(good), dict(sorted(Counter(k for _, _, k in good).items())),
    dict(Counter('target' if v <= Y < 2 * v else 'helper' for _, Y, _ in good))))
