"""Census (rescheduled inlining): a private wire W of target t is eliminated if t reads W's inputs itself in
phase B, each at the input's frame at scatter time.  Conditions: every input X of W is unchanged from W's read
of it to the scatter; X's scatter-time frame lies inside t-perp; and those frames, together with t's other read
frames, form one flag (t's chain).  Reports per-target eliminable wires (at most one wire per target can share
the target's chain unless both fit the same flag)."""
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
def is_flag(fs):
    fs = sorted(set(fs), key=lambda f: len(FR[f]))
    return all(sub(a, b) for a, b in zip(fs, fs[1:])) and len({len(FR[f]) for f in fs}) == len(fs)
A, B = W['A'], W['B']
# frames and last-write positions through phase A (the scatter follows A)
cur = list(W['start']); lastw = defaultdict(lambda: -1)
for F, d, srcs in W['D']:
    for r in [d] + srcs: cur[r] = F
for pos, (F, d, srcs) in enumerate(A):
    for r in [d] + srcs: cur[r] = F
    lastw[d] = pos
at_scatter = list(cur)
# wires: B-read helpers of each target; their build gates (in A or B)
reads = defaultdict(list)
for F, d, srcs in B:
    if v <= d < 2 * v: reads[d].append((F, srcs))
builds = defaultdict(list)
for pos, (F, d, srcs) in enumerate(A): builds[d].append(('A', pos, F, srcs))
for pos, (F, d, srcs) in enumerate(B):
    if not (v <= d < 2 * v): builds[d].append(('B', pos, F, srcs))
stats = Counter(); elim = Counter()
for t in range(v, 2 * v):
    tperp = W['final'][t]
    other = [F for F, srcs in reads[t] if not any(s >= 2 * v for s in srcs)]   # frames of t's source reads
    wires = [s for F, srcs in reads[t] for s in srcs if s >= 2 * v]
    ok_frames = []
    for Wr in wires:
        bl = builds[Wr]
        if any(ph == 'B' for ph, *_ in bl): stats['wire built in B'] += 1; ok_frames.append(None); continue
        fx = []; good = True
        for ph, pos, F, srcs in bl:
            for X in srcs:
                if lastw[X] > pos: good = False; break           # X changed after W read it
                fX = at_scatter[X]
                if not sub(fX, tperp): good = False; break
                fx.append(fX)
            if not good: break
        if not good: stats['input changed or outside t-perp'] += 1; ok_frames.append(None); continue
        if not is_flag(fx + other + [tperp]): stats['frames not a flag'] += 1; ok_frames.append(None); continue
        stats['eliminable'] += 1; ok_frames.append(fx)
    # can two wires be eliminated together? (their frames + t's must form one flag)
    good = [f for f in ok_frames if f is not None]
    if len(good) == 2 and is_flag(good[0] + good[1] + other + [tperp]): elim[2] += 1
    elif good: elim[1] += 1
    else: elim[0] += 1
print('wires:', dict(stats))
print('targets by eliminable wires:', dict(sorted(elim.items())), '-> helpers saved:', elim[1] + 2 * elim[2])
