"""THE R420 WORD ANATOMY v4 — THE SEMANTICS VERIFICATION (the last ground-truth piece!!).

THE SS1454 FIXES: (a) the helpers' FINAL contents are 0 BY DESIGN (the C-phase reverses
the builds!!) -> snapshot the contents AT THE READ TIME!!; (b) the B-srcs include THE
SOURCES (register 3 < v!!): the sources are dirt-free (the bit s IS the x-value!!);
(c) the precedence bug (the '==' vs '%') -> the big-gate dests DO match the ret!!

THE SEMANTICS (the gcheck-exact): the target's x-delivery =
XOR(the scatter's gather-contents) ^ XOR(the B-read contents at the B-time) == {t}
(the single bit t!!!) — the B-reads (the sources + the helper running-sums!) XOR out
perp(t) leaving {t}.  THE VERIFICATION per target: THE CHECK.
Plus: the D-srcs vs the (B-srcs + the scatter-ret): the dirt-doubling structure!!
"""
import gzip, json
from collections import Counter, defaultdict
import numpy as np

path = '/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz'
w = json.loads(gzip.open(path, 'rt').read())
h, v, R = w['h'], w['v'], w['R']
print('THE R420 WORD: h=%d v=%d R=%d (rho %.2f)' % (h, v, R, R / v))
L = np.array(w['lines'], dtype=float)
G = L @ L.T
fr = w['frames']
def span_rank(idxs):
    if not idxs:
        return 0
    return int(np.linalg.matrix_rank(L[list(idxs)]))
dims = [span_rank(F) for F in fr]
nreg = 2 * v + R
ret = w['ret']
MASK = (1 << v) - 1

# ============ THE REPLAY WITH THE SNAPSHOTS ============
cur = list(w['start'])
val = [1 << i for i in range(nreg)]
def xorinto(d, s):
    val[d] ^= val[s]
def replay(gates):
    for F, d, srcs in gates:
        for r in [d] + list(srcs):
            cur[r] = F
        for s in srcs:
            val[d] ^= val[s]
# the D: record the pre-reads (the dirt-doubling!!)
d_srcs = defaultdict(set)
for F, d, srcs in w['D']:
    for s in srcs:
        d_srcs[d - v].add(s)
    replay([(F, d, srcs)])
# the A!!
replay(w['A'])
# THE SCATTER SNAPSHOT: the gathers' contents at the scatter!!
scat_content = {}
for t in range(v):
    acc = 0
    for k in w['scatter'][t]:
        acc ^= val[ret[k]] & MASK
    scat_content[t] = acc
# THE B: the srcs' contents AT THE B-TIME!!
b_reads = defaultdict(list)
b_frames = defaultdict(list)
for F, d, srcs in w['B']:
    if v <= d < 2 * v:
        for s in srcs:
            b_reads[d - v].append(s)
            b_frames[d - v].append((F, s))
        replay([(F, d, srcs)])
    else:
        replay([(F, d, srcs)])
replay(w['C'])

def bits(x):
    out = set()
    while x:
        b = x & -x
        out.add(b.bit_length() - 1)
        x ^= b
    return out

# ============ THE SEMANTICS VERIFICATION ============
print('\n=== THE SEMANTICS VERIFICATION (per target!!) ===')
ok = 0
bad = []
for t in range(v):
    tot = scat_content[t]
    for s in b_reads[t]:
        tot ^= val[s] if False else 0   # placeholder (the val has moved on!!)
    # hmm: the B-time contents were NOT snapshotted!! redo below!!
    pass
# THE FIX: recompute with the proper snapshots!!
cur = list(w['start'])
val = [1 << i for i in range(nreg)]
replay(w['D'])
replay(w['A'])
scat_content = {}
for t in range(v):
    acc = 0
    for k in w['scatter'][t]:
        acc ^= val[ret[k]] & MASK
    scat_content[t] = acc
# the B with the snapshots!!
bsnap = defaultdict(list)
for F, d, srcs in w['B']:
    if v <= d < 2 * v:
        for s in srcs:
            bsnap[d - v].append((s, val[s] & MASK))
    replay([(F, d, srcs)])
ok = 0
baddiff = Counter()
for t in range(v):
    tot = scat_content[t]
    for s, c in bsnap[t]:
        tot ^= c
    want = 1 << t
    if tot == want:
        ok += 1
    else:
        baddiff[len(bits(tot))] += 1
print('the targets: %d/%d where scatter ^ B-reads == {t} EXACTLY' % (ok, v))
if baddiff:
    print('the failures (the delivered sizes): %s' % dict(sorted(baddiff.items())))
# the read anatomy: the src classes (the sources vs the helpers!!)
srccount = Counter()
for t in range(v):
    srcs = [s for s, _ in bsnap[t]]
    srccount[('src' if all(s < v for s in srcs) else 'mixed' if any(s < v for s in srcs) else 'helper', len(srcs))] += 1
print('the read classes (the src-type, the count): %s' % dict(sorted(srccount.items())))
# the per-target read sizes (the contents!!)
csize = Counter()
for t in range(v):
    csize[(len(bits(scat_content[t])), len([1 for s, c in bsnap[t] if c]))] += 1
print('the (scatter-size, nonzero-read-count) classes: %s' % dict(sorted(csize.items())))
# the delivered content sizes per read!!
rsize = Counter()
for t in range(v):
    for s, c in bsnap[t]:
        rsize[('src' if s < v else 'helper', len(bits(c)))] += 1
print('the read content sizes by class: %s' % dict(sorted(rsize.items())))

# ============ THE DIRT STRUCTURE ============
print('\n=== THE DIRT-DOUBLING STRUCTURE ===')
dd = Counter()
for t in range(v):
    bset = set(s for s, _ in bsnap[t] if s >= 2 * v)
    rset = set(ret[k] for k in w['scatter'][t])
    dset = d_srcs[t]
    dd[(len(dset), len(dset & (bset | rset)), len(dset - (bset | rset)))] += 1
print('the D-srcs (count, covered-by-B/scatter, extra): %s' % dict(sorted(dd.items())))
print('DONE')
