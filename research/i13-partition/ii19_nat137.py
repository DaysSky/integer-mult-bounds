"""nat137: THE LAST RESTRUCTURE CENSUS - kill the tiny quads.

The sources' rank-1-2 mass comes from their dim-1/2 visits (the tiny quads).
Restructure: the mid-pieces (dim>=4 spans) built directly from sources at their
own frames; the tiny quads eliminated. THE DUP-COUNT per source = the distinct
mid-frames among its direct readers (the incomparable-frame dups).
The price at the resulting (R, hist) if under the 444 wall.
"""
import json, gzip, os, sys
import mpmath as mp
from collections import Counter
from fractions import Fraction

mp.mp.dps = 40
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))

W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
v = W['v']; R = W['R']; nreg = 2*v+R
lines = W['lines']
A = W['A']; B = W['B']; D = W['D']


def rref_int(rows):
    m = [list(map(Fraction, r)) for r in rows]
    r = 0
    for c in range(len(m[0]) if m else 0):
        p = None
        for i in range(r, len(m)):
            if m[i][c]:
                p = i; break
        if p is None: continue
        m[r], m[p] = m[p], m[r]
        for i in range(len(m)):
            if i != r and m[i][c]:
                f = m[i][c]/m[r][c]
                m[i] = [(a - f*b) for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]


# the intermediates: the A-dests that are read later by A or B (the helpers minus the B-wires)
read_after = set()
for F, d, ss in A:
    read_after.update(ss)
for F, d, ss in B:
    read_after.update(s for s in ss if s >= 2*v)
inter = [d for F, d, ss in A if d in read_after and d >= 2*v]
inter = sorted(set(inter))
print('the intermediates: %d' % len(inter))

# the content masks (the replay)
val = [0]*nreg
for s in range(v):
    val[s] = 1 << s
for F, d, ss in D:
    for s in ss:
        val[d] ^= val[s]
for F, d, ss in A:
    for s in ss:
        val[d] ^= val[s]
mask_of = lambda x: x & ((1 << v) - 1)

# the direct-source readers of each intermediate + the span of its content
direct = {}
spans = {}
for F, d, ss in A:
    if d in inter:
        direct.setdefault(d, set()).update(s for s in ss if s < v)
        m = mask_of(val[d])
        spans[d] = len(rref_int([lines[i] for i in range(v) if (m >> i) & 1]))
span_hist = Counter(spans.values())
print('the intermediates\' content-SPANS:', dict(sorted(span_hist.items())))

# the flattened source-sets (iterative: the A-gates are in DAG order)
flatsrc = {}
for F, d, ss in A:
    out = set()
    for s in ss:
        if s < v:
            out.add(s)
        elif s in flatsrc:
            out.update(flatsrc[s])
        # the unbuilt srcs (wires read early for y-dirt) contribute nothing
    if d in inter:
        prev = flatsrc.get(d, set())
        prev |= out
        flatsrc[d] = prev

# THE RESTRUCTURE: the mid-pieces (span >= 4) built directly from sources;
# the tiny quads (span <= 3) eliminated. Per source: the distinct mid-frames
# among its direct readers (the mid-pieces' frames = their content-spans).
mids = [q for q in inter if spans[q] >= 4]
tinies = [q for q in inter if spans[q] < 4]
print('the mid-pieces (span>=4): %d | the tiny quads: %d' % (len(mids), len(tinies)))
src_frames = {}
for q in mids:
    fs = flatsrc.get(q, set())
    for s in fs:
        src_frames.setdefault(s, set()).add(q)  # the reader = the mid-piece (its frame = its span)
dup_count = 0
dup_hist = Counter()
for s, rws in src_frames.items():
    k = len(rws)
    dup_hist[k] += 1
    dup_count += k - 1
print('the sources\' mid-reader counts:', dict(sorted(dup_hist.items())))
print('THE DUP-COUNT (the extra registers): %d' % dup_count)
R_new = len(mids) + 225 + 9 + dup_count
print('R_new = %d (mids %d + wires 225 + totals 9 + dups %d)' % (R_new, len(mids), dup_count))
print('THE WALL: 444 -> %s' % ('UNDER' if R_new <= 444 else 'OVER - DEAD'))
