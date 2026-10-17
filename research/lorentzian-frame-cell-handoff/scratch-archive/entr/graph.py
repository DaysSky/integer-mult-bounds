"""Helper read graph of P111-tuned: for each helper, who reads it (helpers / sources / targets / scatter), its first-act
frame, and for helper readers whether their chain already stops at h's first-act frame."""
import gzip, json, sys
from collections import Counter, defaultdict
import numpy as np
w = json.load(gzip.open('/home/user/integer-mult-bounds/research/e8-bit-p111-tuned/tune/bitE8mut-p111-tuned.json.gz', 'rt'))
v = w['v']; R = w['R']; n = 2 * v + R
Lm = np.array(w['lines'], dtype=float)
fd = [int(np.linalg.matrix_rank(Lm[f])) if f else 0 for f in w['frames']]
FR = [frozenset(f) for f in w['frames']]
kind = lambda r: 'x' if r < v else ('y' if r < 2 * v else 'h')
readers = defaultdict(list)       # h -> list of (sec, idx, dest, frame)
chain = defaultdict(list)         # register -> list of frames visited (in order, distinct)
first = {}
gates = [(sec, k, g) for sec in ('A', 'B') for k, g in enumerate(w[sec])]
for sec, k, (f, d, srcs) in gates:
    for r in [d] + srcs:
        if not chain[r] or chain[r][-1] != f: chain[r].append(f)
    for s in srcs:
        if kind(s) == 'h': readers[s].append((sec, k, d, f))
    for r in [d] + srcs:
        if kind(r) == 'h' and r not in first: first[r] = (sec, k, f)
ret = set(w['ret'])
cnt = Counter()
cands = []
for h in range(2 * v, n):
    rd = readers[h]
    kinds = Counter(kind(d) for _, _, d, _ in rd)
    tread = kinds['y'] > 0 or h in ret
    xs = kinds['x']
    cnt[('target-read' if tread else ('source-read' if xs else 'helper-only'))] += 1
    if not tread:
        cands.append(h)
print('helper classes', dict(cnt))
# for helper-only (incl source-read) helpers: first-act frame dim, number of distinct readers, readers whose chain has
# h's first frame (or a frame containing it) as their FIRST stop
stat = Counter(); good = []
for h in cands:
    sec, k, f0 = first[h]
    E = f0
    rd = readers[h]
    dests = sorted({d for _, _, d, _ in rd})
    ok = True; extra = 0
    for g in dests:
        cg = chain[g]
        # frames of g before (and at) its first read of h; does g's first frame contain E's lines?
        g0 = cg[0]
        if not (FR[E] <= FR[g0] or E == g0):
            extra += 1
    stat[(fd[E], len(dests), extra)] += 1
    good.append((h, fd[E], len(dests), extra))
for key in sorted(stat): print('first-dim %d readers %d readers-needing-extra-stop %d : %d helpers' % (key + (stat[key],)))
json.dump(good, open('cands.json', 'w'))
