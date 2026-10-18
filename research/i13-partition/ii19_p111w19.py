"""THE V2-TRIAL (ii19_p111w19.py) — THE 155-SINGLETON-BUILDS'-THE-CELL-REFRAME (+1.7270%!!!)

THE MEASURED-FACTS (the w18-decomposition + the w19-timing!!):
  - THE 155-(0,1,2,4,6)-HELPERS: the builds [singleton-u, h, [source-u]] (the FREE-starts!!)
    at the A-head (the positions 1-221!!) | the sources NEVER-written-in-A (the 1<<u-pure!!)
  - THE V2-PRICE (the pricer-direct!!): {1: -310, 2: +155} -> **+1.7270%** (the c-0.001763!!!)

THE EDIT: the per-build: the MOVE to just-after-the-src'-s-first-cell-gate + the F: the
singleton -> THE CELL (the src'-s-cur (the FREE!!!)) -> the h'-s-chain (0,2,4,6) (the +2!!)

THE CHECKS: (a) the moved-builds-vs-their-first-readers (the ORDER!!); (b) the vals (the
sources-pure (the ORDER-INDEPENDENT!!!)); (c) THE CLIMBS (the gcheck-exact!!); (d) THE
GCHECK (the real!!!); (e) THE PRICE (the ~+1.73%-THE-ABOVE-THE-FRONTIER!!!).
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

# (0) THE 155 + their builds + the srcs'-cell-gates + the readers!!
cur = list(w['start'])
chain = defaultdict(list)
for F, d, srcs in w['D'] + w['A']:
    for r in [d] + srcs:
        if cur[r] != F and dims[F] >= dims[cur[r]]:
            cur[r] = F; chain[r].append(F)
T155 = set(h for h in range(2 * V, nreg) if tuple(dims[f] for f in chain[h]) == (1, 2, 4, 6))
log('(0) THE (0,1,2,4,6)-HELPERS: %d' % len(T155))
builds = {}
for gi, (F, d, srcs) in enumerate(w['A']):
    if d in T155 and d not in builds:
        builds[d] = (gi, F, tuple(srcs))
log('    the builds: %d (the positions %d..%d!!)' % (
    len(builds), min(b[0] for b in builds.values()), max(b[0] for b in builds.values())))
# the srcs'-first-cell-gates (the dim-2-gates-reading-the-src!!)
src_cell = {}
for gi, (F, d, srcs) in enumerate(w['A']):
    if dims[F] == 2:
        for s in srcs:
            if s < V and s not in src_cell:
                src_cell[s] = (gi, F)
missing = [d for d, b in builds.items() if b[2][0] not in src_cell]
log('    the srcs-without-cells: %d %s' % (len(missing), missing[:8]))
# the readers (the A/B-gates-reading-h (the first-position!!))
first_read = {}
for gi, (F, d, srcs) in enumerate(w['A']):
    for s in srcs:
        if s in T155 and s not in first_read:
            first_read[s] = gi
for gi, (F, d, srcs) in enumerate(w['B']):
    for s in srcs:
        if s in T155 and s not in first_read:
            first_read[s] = gi
# (a) THE CONFLICT-CHECK: the moved-position (the src'-s-cell + 1) vs the first-reader!!
n_conf = 0
for h, (gi, F, srcs) in builds.items():
    s = srcs[0]
    if s not in src_cell: continue
    move_to = src_cell[s][0]
    fr = first_read.get(h, 10 ** 9)
    if fr < move_to:
        n_conf += 1
        if n_conf <= 5:
            log('    !!! the CONFLICT h=%d: the build %d -> %d BUT the first-reader at %d!!' % (
                h, gi, move_to, fr))
log('(a) THE CONFLICTS: %d/%d' % (n_conf, len(builds)))
assert n_conf == 0, 'THE ORDER-CONFLICT (the deeper-reframe-the-NEEDED!!)'

# (b) THE MOVE + THE REFRAME!!!
A2 = []
moves = []
for gi, (F, d, srcs) in enumerate(w['A']):
    A2.append([F, d, list(srcs)])
for h, (gi, F, srcs) in builds.items():
    s = srcs[0]
    cpos, cF = src_cell[s]
    g = A2[gi]
    assert g[1] == h and g[2] == list(srcs)
    g[0] = cF
    moves.append((gi, cpos))
# the REORDER: the stable-sort-key: the src'-s-cell-pos (the moved-builds) vs the ORIGINAL-positions (the others!!)
key = []
for gi, (F, d, srcs) in enumerate(A2):
    if d in builds:
        key.append(src_cell[srcs[0]][0] + 0.5)   # just-after-the-cell-gate!!
    else:
        key.append(gi)
order = sorted(range(len(A2)), key=lambda i: (key[i], i))
A2 = [A2[i] for i in order]
log('(b) THE MOVE: %d-builds-moved (the reframe-at-their-cells!!)' % len(moves))

# (c) THE CLIMB- + VAL-REPLAY (the gcheck-exact!!)
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
hist[dims[w['ret_frames'][k]]] += 0
for f in w['ret_frames']:
    hist[dims[f]] += 1
bad = [r for r in range(nreg)
       if val[r] != ((1 << r) ^ (1 << (r - V)) if V <= r < 2 * V else 1 << r)]
log('(c) THE REPLAY: bad-vals %d/%d | illegal-climbs %d' % (len(bad), nreg, len(bad_climbs)))
log('    THE NEW-HIST: %s (the mass %d!!)' % (dict(sorted(hist.items())),
    sum(k * n for k, n in hist.items())))
for b in bad[:5]: log('    !!! reg %d' % b)
for b in bad_climbs[:8]:
    log('    !!! [%s] gate %d reg %d: %d(d%d) -> %d(d%d)' % (b[0], b[1], b[2], b[3], b[5], b[4], b[6]))

# (d) THE EMISSION!!!
word = dict(w)
word['A'] = A2
json.dump(word, open('ii19_r434_v2.json', 'w'))
log('(d) EMITTED (ii19_r434_v2.json)')
log('    THE GCHECK: /Users/dayssky/.venv/bin/python '
    'research/lorentzian-frame-cell-handoff/code/tword/gcheck.py '
    'research/i13-partition/ii19_r434_v2.json --price')
log('DONE — THE V2-TRIAL!!!')
