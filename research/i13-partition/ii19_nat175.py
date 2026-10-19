"""nat175: THE ONE-GATE RE-EMISSION DESIGN CENSUS at the 121.
The breakthrough construction: the dup-count measured 0 (nat174!!) -- the 121's
consumers' frames are nested -- the one-gate builds (the pieces at their content-spans,
the wires at theirs) are LEGAL and dup-free.
THE DESIGN INPUTS (this census):
(1) the per-gate-type frame-dims: which frames each helper-class is built/read at TODAY;
(2) the pieces' content-spans: the dim-4/5 closure candidates for their one-gates;
(3) the wires' content-spans: the dim-6 candidates;
(4) the srcs per helper: the source-counts + the src-types (sources vs helpers!!);
(5) the one-gate design's chain-legality: the srcs' climb-paths.
"""
import json
from collections import Counter, defaultdict

w = json.load(open('ii19_own_word4.json'))
v = w['v']
nreg = 2 * v + w['R']
LCDIM = {0: 0, 1: 1, 2: 2, 3: 3, 12: 4, 13: 5, 30: 6, 64: 8, 120: 8, 121: 9}
dims = [LCDIM[len(fr)] for fr in w['frames']]
lines = [tuple(int(c) for c in l) for l in w['lines']]

# (1) the helper-classes
a_dest = defaultdict(list)
for F, d, ss in w['A']:
    a_dest[d].append((F, ss))
b_wires = set()
for F, d, ss in w['B']:
    for s in ss:
        if s >= 2 * v:
            b_wires.add(s)
b_touched = set(d for F, d, ss in w['B'] if v <= d < 2 * v)  # the targets' dest-gates
all_helpers = set(a_dest.keys())
pieces = sorted(all_helpers - b_wires)
wires = sorted(b_wires & all_helpers)
print('the A-built helpers: %d | the pieces (not B-read): %d | the wires (B-read): %d' % (
    len(all_helpers), len(pieces), len(wires)))

# the build-frames' dims (per class)
pc = Counter(dims[F] for d in pieces for F, ss in a_dest[d])
wc = Counter(dims[F] for d in wires for F, ss in a_dest[d])
print('the pieces\' build-frame dims:', dict(sorted(pc.items())))
print('the wires\' build-frame dims:', dict(sorted(wc.items())))

# the gates per helper (the chain-lengths today!)
pg = Counter(len(a_dest[d]) for d in pieces)
wg = Counter(len(a_dest[d]) for d in wires)
print('the gates-per-piece:', dict(sorted(pg.items())))
print('the gates-per-wire:', dict(sorted(wg.items())))

# (2)+(3) the content-spans: each helper's delivered x-content (the replay!)
val = [0] * nreg
for s in range(v):
    val[s] = 1 << s
for F, d, ss in w['D']:
    for s in ss:
        val[d] ^= val[s]
# the A-phase replay in topological order (the emission order!)
import heapq
order = []
indeg = Counter()
succ = defaultdict(list)
srcmap = {}
for d in all_helpers:
    for F, ss in a_dest[d]:
        pass
# simple: replay in the A-list order (own8's emission is already topological!)
for F, d, ss in w['A']:
    for s in ss:
        val[d] ^= val[s]

def span_dim(mask):
    ls = [i for i in range(v) if (mask >> i) & 1]
    if not ls:
        return 0
    M = [list(lines[i]) for i in ls]
    import itertools
    r = 0
    for col in range(9):
        piv = next((i for i in range(r, len(M)) if M[i][col]), None)
        if piv is not None:
            M[r], M[piv] = M[piv], M[r]
            for i in range(len(M)):
                if i != r and M[i][col]:
                    M[i] = [(a ^ b) for a, b in zip(M[i], M[r])]
            r += 1
    return r

psd = Counter()
for d in pieces:
    m = val[d] & ((1 << v) - 1)
    psd[span_dim(m)] += 1
wsd = Counter()
for d in wires:
    m = val[d] & ((1 << v) - 1)
    wsd[span_dim(m)] += 1
print('the pieces\' content-span dims:', dict(sorted(psd.items())))
print('the wires\' content-span dims:', dict(sorted(wsd.items())))

# (4) the srcs: the source-counts + the helper-srcs
psrc = Counter()
phsrc = Counter()
for d in pieces:
    n_s = sum(1 for F, ss in a_dest[d] for s in ss if s < v)
    n_h = sum(1 for F, ss in a_dest[d] for s in ss if s >= 2 * v)
    psrc[n_s] += 1
    if n_h:
        phsrc[n_h] += 1
print('the pieces\' SOURCE-counts (total across their gates):', dict(sorted(psrc.items())))
print('the pieces\' helper-src-counts:', dict(sorted(phsrc.items())))
wsrc = Counter()
whsrc = Counter()
for d in wires:
    n_s = sum(1 for F, ss in a_dest[d] for s in ss if s < v)
    n_h = sum(1 for F, ss in a_dest[d] for s in ss if s >= 2 * v)
    wsrc[n_s] += 1
    if n_h:
        whsrc[n_h] += 1
print('the wires\' SOURCE-counts:', dict(sorted(wsrc.items())))
print('the wires\' helper-src-counts:', dict(sorted(whsrc.items())))
