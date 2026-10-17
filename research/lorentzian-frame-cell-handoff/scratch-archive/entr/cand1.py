"""The entrance-rank-1 candidate(s) in P111-tuned: helper h whose first act is at a rank-1 frame E, read by exactly
one register g (a helper or source) whose chain can sit at E before h is first modified; h's dirt then cancels in g
by an early read g += h at E, so h leaves D and may start at E (width-7 residual)."""
import gzip, json
import numpy as np
from collections import defaultdict
w = json.load(gzip.open('/home/user/integer-mult-bounds/research/e8-bit-p111-tuned/tune/bitE8mut-p111-tuned.json.gz', 'rt'))
v = w['v']; R = w['R']; n = 2 * v + R
Lm = np.array(w['lines'], dtype=float)
fd = [int(np.linalg.matrix_rank(Lm[f])) if f else 0 for f in w['frames']]
FR = [frozenset(f) for f in w['frames']]
kind = lambda r: 'x' if r < v else ('y' if r < 2 * v else 'h')
gates = [(sec, k, g) for sec in ('A', 'B') for k, g in enumerate(w[sec])]
readers = defaultdict(list); writes = defaultdict(list); touches = defaultdict(list)
for idx, (sec, k, (f, d, srcs)) in enumerate(gates):
    writes[d].append((idx, sec, k, f))
    for s in srcs: readers[s].append((idx, sec, k, d, f))
    for r in [d] + srcs: touches[r].append((idx, sec, k, f))
ret = set(w['ret'])
Dset = set(s for g in w['D'] for s in g[2])
for h in range(2 * v, n):
    rd = readers[h]
    if h in ret: continue
    dests = sorted({d for _, _, _, d, _ in rd})
    if len(dests) != 1: continue
    g = dests[0]
    if kind(g) == 'y': continue
    t0 = touches[h][0]; E = t0[3]
    if fd[E] != 1: continue
    # g's frames before/at its first touch
    tg = touches[g]
    g_first = tg[0]
    print('helper h=%d (h%d): first act %s gate %d at frame %d (dim %d, lines %s); reads of h: %s' % (h, h - 2 * v, t0[1], t0[2], E, fd[E], sorted(FR[E]),
          [(s, k, f, fd[f]) for _, s, k, _, f in rd]))
    print('   only reader g=%d (%s): start frame dim %d; first touch %s gate %d at frame %d dim %d lines %s; contains E: %s' % (
          g, kind(g), fd[w['start'][g]], g_first[1], g_first[2], g_first[3], fd[g_first[3]], sorted(FR[g_first[3]]), FR[E] <= FR[g_first[3]]))
    print('   h in D:', h in Dset, '; h writes:', [(s, k, f, fd[f]) for _, s, k, f in writes[h]][:6])
    print('   g touches (first 6):', [(s, k, f, fd[f]) for _, s, k, f in tg[:6]])
