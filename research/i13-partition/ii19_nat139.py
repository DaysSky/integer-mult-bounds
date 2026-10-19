"""nat139: THE TARGETS' TPERP-REFRAME SURGERY (the first positive shape move).

gcheck B-rules: the target-dest gates are frame-free (the 'pass' branch);
the z-gates (non-target dests) are H4-order-pinned but independent.
Per target: split the mixed gates (source-parts / wire-parts); order the low gates
(source-parts + double-reader wire-parts, ascending), then re-aim the
SINGLE-reader wire-parts at final[t] (the TPERP, dim 7) - legal since every
frame in the target's chain nests inside its TPERP, and the wire climbs
A-end -> 7 (rank <= 6... requires sub(cur[w], TPERP): check per gate).
The z-gates stay in place (their H4 order).
"""
import json, gzip, os, sys, copy
import mpmath as mp
from fractions import Fraction
from collections import Counter

mp.mp.dps = 40
W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
v = W['v']; R = W['R']; nreg = 2*v+R; h = 8
lines = W['lines']
D, A, B, C = W['D'], W['A'], W['B'], W['C']
start = W['start']; final = W['final']


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


bases = [rref_int([lines[i] for i in W['frames'][F]]) for F in range(len(W['frames']))]
dims = [len(b) for b in bases]
fr_cache = {}
line_sets = [set(W['frames'][F]) for F in range(len(W['frames']))]


def sub(a, b):
    if a == b: return True
    if dims[a] > dims[b]: return False
    if a not in fr_cache:
        fr_cache[a] = rref_int([lines[i] for i in W['frames'][a]])
    bb = bases[b]
    for row in fr_cache[a]:
        r_ = list(row)
        for br in bb:
            c = next((i for i, x in enumerate(r_) if x), None)
            if c is None: break
            bc = next((i for i, x in enumerate(br) if x), None)
            if bc == c:
                f = r_[c]/br[c]
                r_ = [(x - f*y) for x, y in zip(r_, br)]
        if any(x != 0 for x in r_): return False
    return True


# the wires' reader-counts (the B-srcs >= 2v, target-dest gates only)
wire_readers = Counter()
for F, d, ss in B:
    if v <= d < 2*v:
        for s in ss:
            if s >= 2*v:
                wire_readers[s] += 1
single = {q for q, n in wire_readers.items() if n == 1}
print('the wires: %d | single-reader: %d | multi-reader: %d' % (len(wire_readers), len(single), len(wire_readers)-len(single)))

# the A-end positions (the replay: D + A)
cur = list(start)
for F, d, ss in D:
    cur[d] = F
    for s in ss: cur[s] = F
for F, d, ss in A:
    for p in [d] + list(ss): cur[p] = F

# the content masks (for the content-law check)
val = [0]*nreg
for s in range(v): val[s] = 1 << s
for F, d, ss in D:
    for s in ss: val[d] ^= val[s]
for F, d, ss in A:
    for s in ss: val[d] ^= val[s]

# THE SURGERY: split + sort + re-aim
B_new = []
zkeep = []     # the z-gates in order
tpf = final    # the targets' TPERP frames
n_aim = 0
n_keep = 0
for F, d, ss in B:
    if not (v <= d < 2*v):
        zkeep.append((F, d, list(ss)))
        continue
    srcs = [s for s in ss if s < v]
    ws = [s for s in ss if s >= 2*v]
    # split: the source-part keeps F; the wire-part candidate: final[d]
    if srcs and ws:
        B_new.append((F, d, srcs))
        B_new.append((F, d, ws))   # placeholder - re-aimed in the per-target pass below
    elif ws:
        B_new.append((F, d, ws))   # placeholder
    else:
        B_new.append((F, d, srcs))
    n_keep += 1

# the per-target pass: collect the target-gates, sort, re-aim the single-reader wire-parts
by_tgt = {}
for F, d, ss in B_new:
    by_tgt.setdefault(d, []).append((F, ss))
B_out = []
for F, d, ss in B:
    if not (v <= d < 2*v):
        B_out.append((F, d, ss))
        continue
# rebuild: interleave - simplest legal order: for each target, its gates in the original
# order but with the single-reader wire-parts moved last + re-aimed
final_B = []
i = 0
tgt_queues = {}
for F, d, ss in B:
    if not (v <= d < 2*v):
        final_B.append((F, d, list(ss)))
        continue
    tgt_queues.setdefault(d, []).append((F, ss))
# process the targets' queues (the z-gates already emitted in order above!)
# PROBLEM: the z-gates must stay interleaved... they were emitted first - WRONG ORDER!
# Actually the z-gates' H4 order is their own relative order; the target-gates can be
# anywhere. Rebuild: the z-gates in their original relative order, then the target-gates.
B_final = []
tgt_gates = []
for F, d, ss in B:
    if v <= d < 2*v:
        tgt_gates.append((F, d, list(ss)))
    else:
        B_final.append((F, d, list(ss)))
# split the target-gates
split_gates = []
for F, d, ss in tgt_gates:
    srcs = [s for s in ss if s < v]
    ws = [s for s in ss if s >= 2*v]
    if srcs: split_gates.append((F, d, srcs, 'src'))
    if ws: split_gates.append((F, d, ws, 'wire'))
# per target: the low gates ascending, then the re-aimed single-reader wire-parts
per = {}
for F, d, ss, kind in split_gates:
    per.setdefault(d, []).append((F, ss, kind))
reordered = []
for d, gs in per.items():
    lows = [(F, ss) for F, ss, k in gs if not (k == 'wire' and all(w in single for w in ss))]
    highs = [(F, ss) for F, ss, k in gs if (k == 'wire' and all(w in single for w in ss))]
    lows.sort(key=lambda x: dims[x[0]])
    tpf_d = final[d]
    for F, ss in lows:
        reordered.append((F, d, ss))
    for F, ss in highs:
        ok = all(sub(cur[w], tpf_d) for w in ss)
        if ok:
            reordered.append((tpf_d, d, ss))
            n_aim += 1
        else:
            reordered.append((F, d, ss))
            n_keep += 1
B_final.extend(reordered)
print('the re-aimed wire-parts: %d | kept: %d' % (n_aim, n_keep))
print('the B-gates: %d -> %d' % (len(B), len(B_final)))

# THE HIST + the mass
hist = {}
cur2 = list(start)
def climb(r, F):
    if cur2[r] == F: return
    global error
    assert dims[cur2[r]] < dims[F] and sub(cur2[r], F), ('climb fail', r, cur2[r], F)
    hist[dims[F] - dims[cur2[r]]] = hist.get(dims[F] - dims[cur2[r]], 0) + 1
    cur2[r] = F

for F, d, ss in D:
    climb(d, F)
    for s in ss: climb(s, F)
for F, d, ss in A:
    climb(d, F)
    for s in ss: climb(s, F)
for k, q in enumerate(W['ret']):
    rf = cur2[q]          # the totals' A-end frames (the replay positions!)
    for c in [dims[rf]]: hist[c] = hist.get(c, 0) + 1
for F, d, ss in B_final:
    climb(d, F)
    for s in ss: climb(s, F)
for F, d, ss in C:
    climb(d, F)
    for s in ss: climb(s, F)
for r in range(nreg):
    climb(r, final[r])
mass = sum(k*n for k, n in hist.items())
ident = 8*R + sum(dims[W['ret_frames'][k]] for k in range(len(W['ret']))) + 2*v*7
print('the hist:', dict(sorted(hist.items())), '| mass', mass, '| identity', ident)
if mass == ident:
    print('MASS-TRUE')
    json.dump({'B': B_final, 'hist': hist}, open('ii19_nat139_result.json', 'wt'))
