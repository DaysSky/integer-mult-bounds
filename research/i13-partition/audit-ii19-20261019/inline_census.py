"""Census: which private B-wires of the r434 word could be inlined into their target (the target reads the wire's
inputs itself in phase B).  A wire W is inlinable when every register it absorbs is dying after that gate (no
later A/B gate touches it) and the frames of W's gates form a flag together with the target's other read frames."""
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
_sub = {}
def sub(a, b):          # frame a subset of frame b
    if (a, b) not in _sub:
        _sub[(a, b)] = len(rref(FR[a] + FR[b])) == len(FR[b]) if FR[a] else True
    return _sub[(a, b)]
gates = [('A', i, g) for i, g in enumerate(W['A'])] + [('B', i, g) for i, g in enumerate(W['B'])]
touch = defaultdict(list)                     # register -> positions in the A+B sequence
for pos, (ph, i, (F, d, srcs)) in enumerate(gates):
    for r in [d] + srcs: touch[r].append(pos)
is_target = lambda r: v <= r < 2 * v
wire_of = defaultdict(list); tgt_frames = defaultdict(list)
for pos, (ph, i, (F, d, srcs)) in enumerate(gates):
    if ph == 'B' and is_target(d):
        for s in srcs:
            if s >= 2 * v: wire_of[d].append((s, F, pos))
            else: tgt_frames[d].append(F)
stats = Counter(); per_target = Counter()
for t in range(v, 2 * v):
    ok_here = 0
    for wreg, Fread, rpos in wire_of[t]:
        ins = [(pos, F, srcs) for pos, (ph, i, (F, d, srcs)) in enumerate(gates) if d == wreg and pos < rpos]
        dying = all(touch[x][-1] == pos for pos, F, srcs in ins for x in srcs)
        frames = sorted({F for pos, F, srcs in ins} | set(tgt_frames[t]), key=lambda f: len(FR[f]))
        flag = all(sub(a, b) for a, b in zip(frames, frames[1:]))
        stats[(dying, flag)] += 1
        if dying and flag: ok_here += 1
    per_target[min(ok_here, 2)] += 1
print('wires: (all inputs dying, flag-compatible with target reads) ->', dict(stats))
print('targets by number of fully inlinable wires:', dict(per_target))
