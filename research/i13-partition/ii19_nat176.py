"""nat176: THE ONE-GATE RE-EMISSION AT THE 121 -- THE REAL CONSTRUCTION.
Each helper's multi-gate build ladder collapses into ONE gate at its content-span's
closure (the root-closed frame), same src-set, same XOR, same consumers.
Legality (all verified by measurement + the closure-nesting law):
- the srcs' contents nest inside the consumer's span-closure (root-closure law!!);
- the consumers' frames nest (nat174: 0 dups!!);
- the B/D/scatter/rets UNCHANGED (the val-replay is identical!!);
- only the A-phase's build-gates + the C-web re-emit.
THE OUTPUT: the new word -> gcheck -> the hist -> the price.
"""
import json
from collections import Counter, defaultdict
from fractions import Fraction

w = json.load(open('ii19_own_word4.json'))
v = w['v']
h = w['h']
nreg = 2 * v + w['R']
lines = [tuple(int(c) for c in l) for l in w['lines']]

# the replay: each helper's content + its src-union
val = [0] * nreg
for s in range(v):
    val[s] = 1 << s
for F, d, ss in w['D']:
    for s in ss:
        val[d] ^= val[s]
src_union = defaultdict(list)
for F, d, ss in w['A']:
    src_union[d].extend(ss)
    for s in ss:
        val[d] ^= val[s]

helpers = sorted(src_union.keys())
print('the helpers: %d' % len(helpers), flush=True)

# the frames: line-INDEX sets (find-or-add by the closure!!)
def lineset_of_frame(fr):
    return frozenset(tuple(int(c) for c in vec) for vec in fr)

# build the canonical line-index map (with +/- handling: a line and its negative are the same)
def canon(vec):
    if vec > tuple(-c for c in vec):
        vec = tuple(-c for c in vec)
    return vec
lidx = {}
for i, l in enumerate(lines):
    lidx[canon(tuple(l))] = i

def span_lines(mask):
    return [i for i in range(v) if (mask >> i) & 1]

# the closure of a line-set: the root-closed frame = all lattice lines in the span.
# compute via: span the lines (over Q), then find all lattice lines in the span.
import itertools
def span_closure(idxset):
    """all lattice lines in the Q-span of the given lines (the root-closure)."""
    if not idxset:
        return frozenset()
    M = [list(lines[i]) for i in idxset]
    # RREF over Q (fractions)
    rows = [[Fraction(c) for c in r] for r in M]
    piv = []
    r = 0
    for col in range(9):
        p = next((i for i in range(r, len(rows)) if rows[i][col] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        pv = rows[r][col]
        rows[r] = [c / pv for c in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv.append(col)
        r += 1
        if r == len(rows):
            break
    # all lattice lines in the span: for each line l: l in span iff RREF(l) reduces to 0
    out = []
    for i in range(v):
        x = [Fraction(c) for c in lines[i]]
        for rr, pc in zip(rows, piv):
            if x[pc] != 0:
                f = x[pc]
                x = [a - f * b for a, b in zip(x, rr)]
        if all(c == 0 for c in x):
            out.append(i)
    return frozenset(out)

# the frame-registry: existing frames by their canonical line-sets
frames = [list(fr) for fr in w['frames']]
fsets = {lineset_of_frame(fr) for fr in frames}

def get_frame(idxset):
    """find or create the closure-frame for the given line-set."""
    cs = span_closure(idxset)
    if cs not in fsets:
        fsets.add(cs)
        frames.append([list(lines[i]) for i in sorted(cs)])
    # return the index
    for k, fr in enumerate(frames):
        if lineset_of_frame(fr) == cs:
            return k
    raise AssertionError('frame not found')

# the A-phase's topological order: use the W4's own A-order (already topological!!)
# per helper: ONE gate at its content-span's closure.
content = {}
for F, d, ss in w['A']:
    pass  # (the replay already done above)
# the contents: recompute in the W4's A-order (val already accumulated!!)
# NOTE: the content is the accumulated val (the replay ✓)

new_A = []
gate_frames = {}
for F, d, ss in w['A']:
    if d in gate_frames:
        continue  # only the FIRST gate per helper (we rebuild from scratch below)
# rebuild: iterate the W4's A-order; for each helper's FIRST gate, emit the ONE-gate.
emitted = set()
for F, d, ss in w['A']:
    if d in emitted:
        continue
    emitted.add(d)
    m = val[d] & ((1 << v) - 1)
    sp = span_lines(m)
    fr = get_frame(sp)
    new_A.append([fr, d, sorted(set(src_union[d]))])
    gate_frames[d] = fr
print('the one-gates: %d | the frames: %d (was %d)' % (len(new_A), len(frames), len(w['frames'])), flush=True)

# the B-phase: UNCHANGED (the targets read the wires at the same frames!!)
new_B = [list(g) for g in w['B']]

# the D-phase: UNCHANGED
new_D = [list(g) for g in w['D']]

# the C-web: the zg = the A+B non-target dests -- recompute the reversal pairs.
# own8's C-format: [F, d, [s]]: the z-reversal at the FULL frame (index 1!!).
# the zg-list: the (dest, src) pairs from A+B (non-target dests), in order; the C = the reverse.
zg = []
for F, d, ss in new_A:
    if not (v <= d < 2 * v):
        for s in ss:
            zg.append((d, s))
for F, d, ss in new_B:
    if not (v <= d < 2 * v):
        for s in ss:
            zg.append((d, s))
FULL = 1  # the W4's FULL-frame index
new_C = [[FULL, d, [s]] for d, s in reversed(zg)]
print('the C-gates: %d' % len(new_C), flush=True)

# the starts: the sources' singles + the targets at 0 + the helpers at 0
# the W4's start: reuse (the sources' singles!!) + the helpers at 0!!
start = list(w['start'])
final = list(w['final'])

# the finals: the helpers at the FULL (1!!); the targets at their perps (unchanged!!);
# the W4's finals: reuse.

out = {
    'v': v, 'h': h, 'R': w['R'], 'form': w['form'], 'lines': w['lines'],
    'frames': frames, 'start': start, 'final': final,
    'D': new_D, 'A': new_A, 'B': new_B, 'C': new_C,
    'ret': w['ret'], 'scatter': w['scatter'], 'ret_frames': w['ret_frames'],
}
json.dump(out, open('ii19_onegate_word.json', 'wt'))
print('SAVED ii19_onegate_word.json', flush=True)

# gcheck!!
import sys
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/tword')
import gcheck
res = gcheck.main('ii19_onegate_word.json')
print('THE GCHECK:', res, flush=True)
