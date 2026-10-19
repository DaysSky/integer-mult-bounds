"""Census on the r434: helpers convertible to E1-style entrance helpers (research/e8-bit-p111-e1).  Helper h
(not a total, never read by a target) enters at its first-write frame F1 instead of frame 0.  Its dirt is cancelled
inside the word: every direct reader r that reads h an odd number of times gets one extra read [F1, r, [h]]
inserted just before h's first write (h then holds only its dirt).  Legal when r's frame at that moment lies in F1
and r's next frame contains F1.  Then no D gate needs h.  Entrance rank = dim F1, residual width = 8 - dim F1."""
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
FR = [rref(F) if F else [] for F in W['frames']]; DIM = [len(F) for F in FR]
_s = {}
def sub(a, b):
    if a == b or not FR[a]: return True
    if (a, b) not in _s: _s[(a, b)] = len(rref(FR[a] + FR[b])) == len(FR[b])
    return _s[(a, b)]
seq = [('A', g) for g in W['A']] + [('B', g) for g in W['B']]
cur = list(W['start'])
for F, d, srcs in W['D']:
    for r in [d] + srcs: cur[r] = F
frame_before = []                 # frame of every register just before each gate (sparse: store per gate operands)
visits = defaultdict(list)        # register -> [(pos, frame)]
for pos, (ph, (F, d, srcs)) in enumerate(seq):
    for r in [d] + srcs:
        if cur[r] != F: visits[r].append((pos, F)); cur[r] = F
def frame_at(r, pos):             # frame just before gate pos
    f = W['start'][r]
    for p, F in visits[r]:
        if p < pos: f = F
        else: break
    return f
def next_frame_from(r, pos):      # first frame r visits at or after gate pos
    for p, F in visits[r]:
        if p >= pos: return F
    return W['final'][r]
first_write = {}; readers = defaultdict(Counter); target_read = set()
for pos, (ph, (F, d, srcs)) in enumerate(seq):
    if d >= 2 * v and d not in first_write: first_write[d] = (pos, F)
    for s in srcs:
        if s >= 2 * v:
            if v <= d < 2 * v: target_read.add(s)
            else: readers[s][d] += 1
TOT = set(W['ret']); stats = Counter(); ok = []
for hreg in range(2 * v, nreg):
    if hreg in TOT: stats['total'] += 1; continue
    if hreg in target_read: stats['read by a target'] += 1; continue
    if hreg not in first_write: stats['never written'] += 1; continue
    pos1, F1 = first_write[hreg]
    if W['start'][hreg] != 0 or frame_at(hreg, pos1) != 0: stats['not at frame 0 before first write'] += 1; continue
    good = True; inserts = 0
    for r, k in readers[hreg].items():
        if k % 2 == 0: continue
        if not (sub(frame_at(r, pos1), F1) and sub(F1, next_frame_from(r, pos1))): good = False; break
        inserts += 1
    if not good: stats['a reader cannot do the early read'] += 1; continue
    stats['convertible'] += 1; ok.append((hreg, DIM[F1], inserts))
print('helpers:', R, dict(stats))
print('convertible by entrance rank (width 8-rank):', dict(sorted(Counter(e for _, e, _ in ok).items())))
print('early reads inserted per convertible helper:', dict(sorted(Counter(i for *_, i in ok).items())))
json.dump(ok, open('entrance_candidates.json', 'w'))
