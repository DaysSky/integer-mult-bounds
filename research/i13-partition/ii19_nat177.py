"""nat177: THE MAX-SHAPE EMISSION AT THE 121 -- the one-gate builds + the max-legal reads.
Design (all legality verified):
(1) each helper: ONE A-gate at its content-span's closure (the 472 one-gates,
    the ranks 4-9 -- the {2,2}-ladders gone);
(2) the read-frames: the maximal legal -- the consumer reads the src at the
    highest frame with (the src's content in F) and (F in the consumer's backward bound)
    -- the common-ancestor reaming (the dup-free incomparability bridge!!);
(3) the chains monotone by construction; the B/D/scatter/rets unchanged;
(4) the C-web re-emitted from the new A.
Output: the word -> gcheck -> the hist -> the price.
"""
import json
from collections import Counter, defaultdict
from fractions import Fraction

w = json.load(open('ii19_own_word4.json'))
v, h = w['v'], w['h']
nreg = 2*v + w['R']
lines = [tuple(int(c) for c in l) for l in w['lines']]

def canon(vec):
    vec = tuple(vec)
    return vec if vec > tuple(-c for c in vec) else tuple(-c for c in vec)
cvec = [canon(l) for l in lines]
cidx = {cv: i for i, cv in enumerate(cvec)}

frames = [list(fr) for fr in w['frames']]
fsets = [frozenset(canon(vec) for vec in fr) for fr in frames]
fkey = {fs: k for k, fs in enumerate(fsets)}

def span_closure(idxset):
    if not idxset: return frozenset()
    rows = [[Fraction(c) for c in lines[i]] for i in idxset]
    piv = []; r = 0
    for col in range(9):
        p = next((i for i in range(r, len(rows)) if rows[i][col] != 0), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        pv = rows[r][col]
        rows[r] = [c/pv for c in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [a - f*b for a, b in zip(rows[i], rows[r])]
        piv.append(col); r += 1
        if r == len(rows): break
    out = set()
    for i in range(v):
        x = [Fraction(c) for c in lines[i]]
        for rr, pc in zip(rows, piv):
            if x[pc] != 0:
                f = x[pc]
                x = [a - f*b for a, b in zip(x, rr)]
        if all(c == 0 for c in x): out.add(cvec[i])
    return frozenset(out)

def get_frame(idxset):
    key = span_closure(idxset)
    if key not in fkey:
        fkey[key] = len(frames)
        frames.append([list(lines[cidx[cv]]) for cv in sorted(key, key=lambda t: cidx[t])])
        fsets.append(key)
    return fkey[key]

# the replay + the src-unions + the contents
val = [0]*nreg
for s in range(v): val[s] = 1 << s
for F, d, ss in w['D']:
    for s in ss: val[d] ^= val[s]
src_union = defaultdict(list)
for F, d, ss in w['A']:
    src_union[d].extend(ss)
    for s in ss: val[d] ^= val[s]

helpers = set(src_union.keys())
content = {d: val[d] & ((1 << v) - 1) for d in helpers}
span_frame = {}
for d in helpers:
    sp = [i for i in range(v) if (content[d] >> i) & 1]
    span_frame[d] = get_frame(sp)
print('the helpers %d | the frames %d' % (len(helpers), len(frames)), flush=True)

# the consumers (A-side: helper-reads; B-side: the targets -- frames UNCHANGED for B!!)
consA = defaultdict(set)
for d, ss in src_union.items():
    for s in ss:
        if s in helpers: consA[s].add(d)
bReads = defaultdict(list)   # wire -> list of (B-frame)
for F, d, ss in w['B']:
    for s in ss:
        if s in helpers: bReads[s].append(F)

# THE BACKWARD BOUNDS: the consumer's bound at the read = the highest frame
# its chain can be at -- computed by the LAST gate's frame (the final bounds) + backward.
# the gate-list per helper-consumer (the one-gate frames + the B-frames for the wires)
gates_of = defaultdict(list)   # helper -> [(frame, is_B)]
for d in helpers:
    gates_of[d].append((span_frame[d], False))
for s, Fs in bReads.items():
    for F in Fs:
        gates_of[s].append((F, True))
# the finals: all helpers end at the FULL (dim-9!!) -- the last bound = FULL(=1)
FULL = 1

# the backward pass: process the gates in reverse topological order.
# the topological order: the W4's A-order (the srcs built first) + the B at the end.
order = [d for F, d, ss in w['A'] if d in helpers]
seen = set(); topo = []
for d in order:
    if d not in seen:
        seen.add(d); topo.append(d)
# the bounds: bound[d] = the max frame the helper d's position may be at, given its later gates.
# process each helper's gates LAST-to-FIRST: after its last gate (the final: FULL).
bounds = {}
for d in helpers:
    gs = gates_of[d]
    # the bound for the LAST gate = FULL; each earlier gate's bound = the next gate's frame
    bnd = FULL
    bs = []
    for F, isB in reversed(gs):
        bs.append(bnd)
        bnd = F
    bounds[d] = list(reversed(bs))   # bounds[i] = the bound for gates_of[d][i]

# THE READ-FRAMES: the consumer reads the src s at the highest legal F:
# content(s) subseteq F subseteq the consumer's bound at that read.
# the reads happen at the consumer's one-gate (frame = span_frame[consumer]) -- already MAX for the srcs!
# so the src's read-frame = span_frame[consumer] (already maximal given the consumer's position!!)
# the legality: span_frame[s] subseteq span_frame[consumer]?? -- by the closure-nesting law (the content-nesting).
bad = 0
for d in helpers:
    for s in src_union[d]:
        if not (fsets[span_frame[s]] <= fsets[span_frame[d]]):
            bad += 1
print('the src-nesting violations (content outside the consumer span): %d' % bad, flush=True)

# the B-frames for the wires: the wires climb span_frame[w] -> the B-frames: the nesting check
badB = 0
for s, Fs in bReads.items():
    for F in Fs:
        if not (fsets[span_frame[s]] <= fsets[F]):
            badB += 1
print('the B-frame nesting violations: %d' % badB, flush=True)

if bad or badB:
    print('THE DESIGN ILLEGAL -- stopping before emission')
    json.dump({'bad': bad, 'badB': badB}, open('ii19_nat177_illegal.json', 'wt'))
    raise SystemExit(1)

# THE EMISSION: the A-phase = the one-gates in the topological order
new_A = [[span_frame[d], d, sorted(set(src_union[d]))] for d in topo]
new_B = [list(g) for g in w['B']]
new_D = [list(g) for g in w['D']]
zg = []
for F, d, ss in new_A:
    if not (v <= d < 2*v):
        for s in ss: zg.append((d, s))
for F, d, ss in new_B:
    if not (v <= d < 2*v):
        for s in ss: zg.append((d, s))
new_C = [[FULL, d, [s]] for d, s in reversed(zg)]
print('the A: %d | the C: %d' % (len(new_A), len(new_C)), flush=True)

out = dict(w)
out['frames'] = frames
out['A'] = new_A; out['B'] = new_B; out['D'] = new_D; out['C'] = new_C
json.dump(out, open('ii19_maxshape_word.json', 'wt'))
print('SAVED ii19_maxshape_word.json', flush=True)

import sys
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/tword')
import gcheck
res = gcheck.main('ii19_maxshape_word.json')
print('THE GCHECK:', res, flush=True)
