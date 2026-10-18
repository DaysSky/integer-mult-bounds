"""nat128: THE BIG-JUMP FEASIBILITY CENSUS (the partial restructure's reach).

For each helper q (built in A, read in B/C): its consumers'-chain structure. A helper's
build-gates can big-jump (0 -> high -> 8) iff every participant in every build-gate
permits it: the srcs' chains must not be pinned by OTHER small-frame consumers, and the
dest's own next-readers must be at >= the jumped frames. Backward reachability: process
the DAG backward from the finals; a gate can big-jump iff all its srcs are 'free' at
that point (their remaining consumers all permit high frames). The reachable mass
fraction -> the mixed hist -> the price.
"""
import json, gzip, os, sys
import mpmath as mp
from collections import Counter
from fractions import Fraction

mp.mp.dps = 40
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price

W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
v = W['v']; R = W['R']; nreg = 2 * v + R; NF = len(W['frames'])
lines = W['lines']; final = W['final']; start = W['start']
RET = set(W['ret'])


def rref_int(rows):
    m = [list(map(Fraction, r)) for r in rows]
    r = 0
    for c in range(len(m[0]) if m else 0):
        p = None
        for i in range(r, len(m)):
            if m[i][c]:
                p = i; break
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        for i in range(len(m)):
            if i != r and m[i][c]:
                f = m[i][c] / m[r][c]
                m[i] = [(a - f * b) for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]


bases = [rref_int([lines[i] for i in W['frames'][F]]) for F in range(NF)]
dims = [len(b) for b in bases]


def contains(b, row):
    row = list(row)
    for br in b:
        c = next((i for i, x in enumerate(row) if x), None)
        if c is None:
            break
        bc = next((i for i, x in enumerate(br) if x), None)
        if bc == c:
            f = row[c] / br[c]
            row = [(a - f * bb) for a, bb in zip(row, br)]
    return all(x == 0 for x in row)


sub = [[False] * NF for _ in range(NF)]
for a in range(NF):
    sub[a][a] = True
    if not bases[a]:
        for b in range(NF):
            sub[a][b] = True
        continue
    for b in range(NF):
        if b == a or dims[b] < dims[a] or dims[b] == 0:
            continue
        sub[a][b] = all(contains(bases[b], row) for row in bases[a])
print('the containment matrix done', flush=True)

D = W['D']; A = W['A']; B = W['B']; C = W['C']

# the full gate sequence with the participants
seq = ([('A', i, g) for i, g in enumerate(A)] + [('B', i, g) for i, g in enumerate(B)])
NG = len(seq)
events = [[] for _ in range(nreg)]   # per register: its (gate-idx, frame) in the D+A+B order
for k, (ph, gi, (F, d, ss)) in enumerate(seq):
    for p in [d] + list(ss):
        events[p].append((k, F))

# THE BACKWARD BIG-JUMP: bound[p] as in nat125, but the candidate choice PREFERS the
# highest-dim frame that is ALSO >= the gate's ORIGINAL frame (the content-safe growth)
# -> identical to nat125 (the merge). THE NEW FREEDOM: the gate's frame may move to a
# frame NOT containing the original (only containing the CONTENTS!) - the content-span!
# The content of a src at gate k: its delivered lines so far. Compute via the replay.
val = [0] * nreg
for s in range(v):
    val[s] = 1 << s
for q in range(2 * v, nreg):
    val[q] = 1 << (q + v) if False else 0
# the replay: D then A then B, tracking each participant's content at each gate
cont_at = [None] * NG   # per gate: {p: content-mask}
cur_val = [x for x in val]
curm = list(start)
for k, (ph, gi, (F, d, ss)) in enumerate(seq):
    if ph == 'A':
        pass
    cont_at[k] = {p: (cur_val[p] & ((1 << v) - 1)) for p in [d] + list(ss)}
    for s in ss:
        cur_val[d] ^= cur_val[s]
    for p in [d] + list(ss):
        curm[p] = F

# the content-span dim per (gate, participant)
def cdim(mask):
    ls = [i for i in range(v) if (mask >> i) & 1]
    if not ls:
        return 0
    return len(rref_int([lines[i] for i in ls]))


# the backward big-jump pass: candidates = frames containing the CONTENTS (not necessarily F!)
bound = list(final)
hist = Counter()
raised = 0
for k in range(NG - 1, -1, -1):
    ph, gi, (F, d, ss) = seq[k]
    parts = [d] + list(ss)
    if any(p in RET for p in parts):
        for p in parts:
            bound[p] = F
        continue
    # the contents at this gate
    cmax = max(cdim(cont_at[k][p]) for p in parts)
    # the candidates: G with dims[G] > max(dims[F], cmax), G \u2286 bound[p] \u2200p,
    # and the content-lines \u2288 G's inF: check each content-line's span \u2286 G
    cands = []
    for G in range(NF):
        if dims[G] <= max(dims[F], cmax):
            continue
        if not all(sub[G][bound[p]] for p in parts):
            continue
        # the content check: every content-line's span must sit inside G
        ok = True
        for p in parts:
            ls = [i for i in range(v) if (cont_at[k][p] >> i) & 1]
            for i in ls:
                if not contains(bases[G], lines[i]):
                    ok = False; break
            if not ok:
                break
        if ok:
            cands.append(G)
    if cands:
        best = max(cands, key=lambda G: dims[G])
        seq[k] = (ph, gi, [best, d, ss])
        F = best
        raised += 1
    for p in parts:
        bound[p] = F
print('the big-jump pass: %d gates raised (of %d)' % (raised, NG), flush=True)

for ph, gi, (F, d, ss) in seq:
    if ph == 'A': A[gi] = [F, d, ss]
    else: B[gi] = [F, d, ss]

# the hist + the price
curm = list(start)
for gates in (D, A, B):
    for F, d, ss in gates:
        for p in [d] + list(ss):
            r0 = dims[F] - dims[curm[p]]
            if r0 > 0:
                hist[r0] += 1
            assert r0 > 0 or curm[p] == F, ('the down-climb!', p)
            curm[p] = F
rf = [curm[q] for q in W['ret']]
cst = sum(dims[f] for f in rf)
for f in rf:
    hist[dims[f]] += 1
for F, d, ss in C:
    for p in [d] + list(ss):
        r0 = dims[F] - dims[curm[p]]
        if r0 > 0:
            hist[r0] += 1
        curm[p] = F
for r in range(nreg):
    r0 = dims[final[r]] - dims[curm[r]]
    if r0 > 0:
        hist[r0] += 1
mass = sum(k * c for k, c in hist.items())
ident = 8 * R + cst + 2 * v * 7
print('the big-jump hist:', dict(sorted(hist.items())), 'mass', mass, 'identity', ident)
assert mass == ident
P111 = mp.mpf('0.001733052823330162099157')
c, prof, d = price(dict(hist), v, 8, R)
print('THE BIG-JUMP PRICE: %s (%+.4f%%)' % (mp.nstr(c, 20) if c else 'NO-ROOT', float((c - P111) / P111) * 100 if c else 0))

# the word + gcheck
W2 = dict(W)
W2['A'] = A; W2['B'] = B
W2['form'] = {'num': [[1 if i == j else 0 for j in range(8)] for i in range(8)], 'den': 2}
cur2 = list(start)
for F, d, ss in W2['D'] + W2['A']:
    cur2[d] = F
    for s in ss:
        cur2[s] = F
W2['ret_frames'] = [cur2[q] for q in W2['ret']]
W2['frames'] = [[list(W2['lines'][i]) for i in F] for F in W2['frames']]
json.dump(W2, open('/tmp/r434-bigjump.json', 'wt'))
print('running gcheck...', flush=True)
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
import gcheck
out = gcheck.main('/tmp/r434-bigjump.json', do_price=True)
for k in ('status', 'R', 'cst', 'local_histogram', 'bit_c_nine_stage', 'vs_P111_percent'):
    print('gcheck %s: %s' % (k, out.get(k)))
