"""THE V2-TRIAL-v2 (ii19_p111w20.py) — THE CELL-GATES'-THE-EARLY-MOVE (THE ORDER-FIX!!!)

THE W19'-s-CONFLICTS (75/155!!): the readers-at-509 vs the-the-srcs'-cells-at-510 — THE FIX:
THE SRCS'-CELL-GATES-MOVE-EARLY (the ~222 (the ~the-singleton-reads'-THE-AFTER!!!)) (their
ONLY-upstream: the PURE-sources (the 1<<u-NEVER-WRITTEN-IN-A!!!)) -> the 155-builds-THE-AFTER
(the ~222+-class (the ~the-cells (the ~the-FREE-reads!!!))) -> THE READERS (the ~the-509 (the
~the-UNTOUCHED!!!)) ✓✓✓ THE NO-CYCLE (the ~the-the-srcs'-the-the-THE-NO-UPSTREAM!!!)

THE 11-NO-CELL-SRCS: their builds-STAY (the ~the-144-moved (the ~the-HIST: {1: −288, 2: +144}
(the ~the-+1.0%-class (the ~the-the-THE-LESS (the ~the-the-the-THE-STILL-THE-ABOVE (the ~the-
THE-FRONTIER-BY-~+1.6%!!!)))))
"""
import json, time
from collections import Counter, defaultdict
from fractions import Fraction

w = json.load(open('ii19_pub2_p111-r434.json', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

V, H = w['v'], w['h']
nreg = len(w['start'])

def rref(rows, n):
    m = [[Fraction(x) for x in r] for r in rows]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]
dims = [len(rref(F, H)) for F in w['frames']]

cur = list(w['start'])
chain = defaultdict(list)
for F, d, srcs in w['D'] + w['A']:
    for r in [d] + srcs:
        if cur[r] != F and dims[F] >= dims[cur[r]]:
            cur[r] = F; chain[r].append(F)
T155 = set(h for h in range(2 * V, nreg) if tuple(dims[f] for f in chain[h]) == (1, 2, 4, 6))
builds = {}
for gi, (F, d, srcs) in enumerate(w['A']):
    if d in T155 and d not in builds:
        builds[d] = (gi, F, tuple(srcs))
src_cell = {}
for gi, (F, d, srcs) in enumerate(w['A']):
    if dims[F] == 2:
        for s in srcs:
            if s < V and s not in src_cell:
                src_cell[s] = (gi, F)
log('(0) the 155: %d | the no-cell-srcs: %d' % (
    len(builds), sum(1 for d, b in builds.items() if b[2][0] not in src_cell)))
MOBILE = {d: b for d, b in builds.items() if b[2][0] in src_cell}
FIXED = {d: b for d, b in builds.items() if b[2][0] not in src_cell}
log('    THE MOBILE: %d | THE FIXED (the-stays!!): %d' % (len(MOBILE), len(FIXED)))

# the singleton-reads'-the-LAST-position (the u/w-singleton-reads (the builds-at-the-singletons!!)!!)
sing_last = defaultdict(int)
for gi, (F, d, srcs) in enumerate(w['A']):
    if dims[F] == 1:
        for s in srcs:
            sing_last[s] = max(sing_last[s], gi)
# the moved-cell-gates (the MOBILE-srcs'-cell-gates!!) + the partners!!
move_cell = {}
for d, (gi, F, srcs) in MOBILE.items():
    s = srcs[0]
    move_cell[src_cell[s][0]] = s
# the partners: the cell-gates'-srcs (the 2-src-pair-gates!!)
partners = {}
for gi, (F, d, srcs) in enumerate(w['A']):
    if gi in move_cell:
        partners[gi] = tuple(srcs)
# the constraint: the moved-cell-gates AFTER ALL their srcs'-singleton-reads!!
cell_after = {}
for gi in move_cell:
    m = max(sing_last.get(s, 0) for s in partners[gi])
    cell_after[gi] = m
    assert gi > m, 'the cell-gate %d before the singleton-reads %d?!' % (gi, m)
log('(1) the moved-cell-gates: %d (the all-after-their-singleton-reads ✓!!)' % len(move_cell))

# (2) THE NEW-ORDER: the keys!!!
A2 = [[F, d, list(srcs)] for F, d, srcs in w['A']]
moved_cell_set = set(move_cell)
mobile_ids = set(MOBILE)
key = []
for gi, (F, d, srcs) in enumerate(A2):
    if gi in moved_cell_set:
        key.append(-1)                 # the cell-gates: the FIRST (the ~just-after-the-singleton-reads (the stable!!))
    elif d in mobile_ids:
        s = srcs[0]
        key.append(src_cell[s][0])     # the moved-builds: after-their-cell-gate!!
    else:
        key.append(gi)
# the ORDER: the stable-3-pass: (i) the cell-gates-first (the -1-keys (the their-own-relative-order!!)); (ii) the rest (the stable-by-key)!!
order = sorted(range(len(A2)), key=lambda i: ((0 if key[i] == -1 else 1), key[i], i))
A2 = [A2[i] for i in order]
# the build-frames: the singleton -> the cell!!!
n_ref = 0
for gi, (F, d, srcs) in enumerate(A2):
    if d in mobile_ids and dims[F] == 1:
        s = srcs[0]
        A2[gi][0] = src_cell[s][1]
        n_ref += 1
log('(2) the moves: the cell-gates %d-first | the builds-reframed %d (the cells!!)' % (
    len(moved_cell_set), n_ref))

# (3) THE REPLAY (the gcheck-exact!!)
fr = [rref(F, H) for F in w['frames']]
_sub = {}
def sub(a, b):
    if (a, b) not in _sub:
        _sub[(a, b)] = len(rref(list(fr[a]) + list(fr[b]), H)) == dims[b]
    return _sub[(a, b)]
cur = list(w['start'])
val = [1 << r for r in range(nreg)]
bad_climbs = []
hist = Counter()
def climb(r, F, phase, gi):
    if cur[r] == F: return
    if not (sub(cur[r], F) and dims[F] > dims[cur[r]]):
        bad_climbs.append((phase, gi, r, cur[r], F, dims[cur[r]], dims[F]))
    hist[dims[F] - dims[cur[r]]] += 1
    cur[r] = F
def run(gates, phase):
    for gi, (F, d, srcs) in enumerate(gates):
        for r in [d] + srcs: climb(r, F, phase, gi)
        for s in srcs: val[d] ^= val[s]
run(w['D'], 'D')
run(A2, 'A')
for t in range(V):
    for k in w['scatter'][t]: val[V + t] ^= val[w['ret'][k]]
run(w['B'], 'B')
run(w['C'], 'C')
for r in range(nreg): climb(r, w['final'][r], 'FINAL', -1)
for f in w['ret_frames']:
    hist[dims[f]] += 1
bad = [r for r in range(nreg)
       if val[r] != ((1 << r) ^ (1 << (r - V)) if V <= r < 2 * V else 1 << r)]
log('(3) THE REPLAY: bad-vals %d/%d | illegal-climbs %d' % (len(bad), nreg, len(bad_climbs)))
log('    THE NEW-HIST: %s (the mass %d!!)' % (dict(sorted(hist.items())),
    sum(k * n for k, n in hist.items())))
for b in bad[:5]: log('    !!! reg %d' % b)
for b in bad_climbs[:8]:
    log('    !!! [%s] gate %d reg %d: %d(d%d) -> %d(d%d)' % (b[0], b[1], b[2], b[3], b[5], b[4], b[6]))

word = dict(w)
word['A'] = A2
json.dump(word, open('ii19_r434_v2.json', 'w'))
log('(4) EMITTED (ii19_r434_v2.json)')
log('DONE — THE V2-TRIAL-v2!!!')
