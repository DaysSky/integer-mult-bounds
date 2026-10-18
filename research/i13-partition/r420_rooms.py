"""THE R420's ACTUAL JOINT STRUCTURE (the ground truth for the 121-line build's flag design!!).

THE QUESTIONS (per the SS1732 rejection 'climb not nested (reg 0)' — the sources'/targets'/pieces'
chains!!!):
(0) THE FRAMES' ENCODING: the line-index lists (the SS1446 discovery!!) vs the vector bases?! —
    and the TRUE DIMS (the rref dims vs the line-counts!!)
(1) THE SOURCES' CHAINS: the A-gates' frames per source — the dims' sequences (the nested flags!!)
(2) THE PIECES' READ-ROOMS: the B-srcs' frames per helper — the per-piece dim-chains (the shared
    rooms: how many users per room-frame?! the dims?!)
(3) THE TARGETS' CHAINS: the per-target B-frames' dims (the one-per-dim structure!!)
(4) THE D-GATES' DIRT: the per-target srcs-count (the indicator-doubling!!)
(5) THE A-GATES' BUILD PATTERNS: the dests' build-frames (the incremental running sums?! the
    srcs: the sources vs the earlier helpers!!)
"""
import gzip, json
from collections import Counter, defaultdict

path = 'research/e8-bit-r420/data/bitE8mut-r420.json.gz'
w = json.load(gzip.open(path, 'rt'))
h, v, R = w['h'], w['v'], w['R']
print('R420: h=%d v=%d R=%d' % (h, v, R))
print('the keys: %s' % sorted(w.keys()))
print('the form: %s' % str(w.get('form'))[:120])
nreg = 2 * v + R
print('nreg = %d' % nreg)

# ============ (0) THE FRAMES' ENCODING + THE TRUE DIMS ============
fr = w['frames']
print('\n(0) the frames: %d' % len(fr))
kinds = Counter()
for k, F in enumerate(fr):
    if not F:
        kinds['empty'] += 1
    elif isinstance(F[0], (int, float)):
        kinds['FLAT (index-list!!) len %d' % len(F)] += 1
    elif isinstance(F[0], list):
        kinds['NESTED (vector rows!!) len %d' % len(F)] += 1
    else:
        kinds['?? %s' % type(F[0]).__name__] += 1
print('  the kinds histogram: %s' % dict(sorted(kinds.items())[:40]))
for k in [0, 1, 2, 3, 4, 121, 122, 123, 124, 200, 300, len(fr) - 2, len(fr) - 1]:
    if 0 <= k < len(fr):
        print('  frame %d: %s' % (k, str(fr[k])[:150]))

# the TRUE dims: if the frames are the line-index lists: the dims = the ranks of the lines' spans!!
L = w['lines']
import numpy as np
Ln = np.array(L, dtype=float)
print('  the lines: %d x %s' % (len(L), Ln.shape))
def frame_dim(F):
    if not F:
        return 0
    if isinstance(F[0], (int, float)):
        M = Ln[[int(x) for x in F]]
        return int(np.linalg.matrix_rank(M))
    M = np.array(F, dtype=float)
    return int(np.linalg.matrix_rank(M))
dims = [frame_dim(F) for F in fr]
print('  THE TRUE DIMS histogram: %s' % dict(sorted(Counter(dims).items())))
fdim = dims

# ============ (1) THE SOURCES' CHAINS (the A-gates!!) ============
A = w['A']
print('\n(1) the A-gates: %d' % len(A))
src_kind = Counter()
for F, d, srcs in A:
    ks = Counter(('src' if s < v else 'helper') for s in srcs)
    src_kind['%d srcs, %d helper-srcs' % (ks['src'], ks['helper'])] += 1
print('  the srcs-kind histogram (the first 20): %s' % dict(sorted(src_kind.items(), key=lambda kv: -kv[1])[:20]))
# the per-source chains: the dims of the frames of the gates where s is a src!!
srch = defaultdict(list)
for gi, (F, d, srcs) in enumerate(A):
    for s in srcs:
        if s < v:
            srch[s].append(fdim[F])
print('  the sources in A: %d' % len(srch))
ex = sorted(srch.keys())[:6]
for s in ex:
    print('    the source %d: the A-frames dims %s' % (s, srch[s]))
lens = Counter(len(x) for x in srch.values())
print('  the per-source A-gate count: %s' % dict(sorted(lens.items())))
nonnested = 0
for s, ds in srch.items():
    if any(ds[i] >= ds[i + 1] for i in range(len(ds) - 1)):
        nonnested += 1
print('  THE SOURCES WITH NON-INCREASING DIM SEQUENCES: %d' % nonnested)

# ============ (2) THE PIECES' READ-ROOMS (the B-srcs!!) ============
B = w['B']
print('\n(2) the B-gates: %d' % len(B))
tdest = sum(1 for F, d, srcs in B if v <= d < 2 * v)
print('  the target-dest gates: %d | the z-dest gates: %d' % (tdest, len(B) - tdest))
rooms = defaultdict(list)
for F, d, srcs in B:
    for s in srcs:
        if s >= 2 * v:
            rooms[s].append(fdim[F])
print('  the helpers read in B: %d' % len(rooms))
exh = sorted(rooms.keys())[:6]
for q in exh:
    print('    the helper %d: the read-frames dims %s' % (q, rooms[q]))
percnt = Counter(len(x) for x in rooms.values())
print('  the per-helper read-count: %s' % dict(sorted(percnt.items())))
# the same-dim collisions (the one-frame-per-dim!!): the dims with the repeats!!
coll = sum(1 for q, ds in rooms.items() if any(c > 1 for c in Counter(ds).values()))
print('  THE HELPERS WITH THE SAME-DIM REPEATS (the collisions?!): %d' % coll)

# ============ (3) THE TARGETS' CHAINS (the per-target B-frames!!) ============
tch = defaultdict(list)
for F, d, srcs in B:
    if v <= d < 2 * v:
        tch[d - v].append(fdim[F])
print('\n(3) the targets reading in B: %d' % len(tch))
for t in sorted(tch.keys())[:6]:
    print('    the target %d: the B-frames dims %s' % (t, tch[t]))
tnn = sum(1 for t, ds in tch.items() if any(ds[i] >= ds[i + 1] for i in range(len(ds) - 1)))
print('  THE TARGETS WITH NON-INCREASING B-DIM SEQUENCES: %d' % tnn)
tcnt = Counter(len(x) for x in tch.values())
print('  the per-target B-gate count: %s' % dict(sorted(tcnt.items())[:15]))

# ============ (4) THE D-GATES' DIRT ============
D = w['D']
print('\n(4) the D-gates: %d' % len(D))
dcnt = Counter(len(srcs) for F, d, srcs in D)
print('  the D srcs-count: %s' % dict(sorted(dcnt.items())[:15]))

# ============ (5) THE SCATTER + RET ============
print('\n(5) the ret: %d | the scatter: %d' % (len(w['ret']), len(w['scatter'])))
scnt = Counter(len(x) for x in w['scatter'])
print('  the scatter-list sizes: %s' % dict(sorted(scnt.items())[:15]))
print('  the ret: %s' % w['ret'][:12])
print('  the ret_frames dims: %s' % [fdim[f] for f in w['ret_frames']])

# ============ (6) THE FINAL/START ============
st, fi = w['start'], w['final']
print('\n(6) the start dims (the first 5 + the targets): %s | %s' % ([fdim[f] for f in st[:5]], [fdim[f] for f in st[v:v + 5]]))
print('    the final dims (the sources + the targets + the helpers): %s | %s | %s' % (
    [fdim[f] for f in fi[:5]], [fdim[f] for f in fi[v:v + 5]], [fdim[f] for f in fi[2 * v:2 * v + 5]]))
