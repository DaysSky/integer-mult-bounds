"""nat136: THE SHAPE-ROUTE CENSUS (the wires' one-gate builds at the shared block-frames).

(1) Per wire: its content's span-dim + the candidate dim-6 frames containing it.
(2) The sources' sharing: per source, its reader-wires; can they share ONE frame
    (the source's single dim-6 visit: the chain 1 -> 6 -> 8: {5, 2})?
(3) The honest hist + the price at the realized shape.
"""
import json, gzip, os, sys
import mpmath as mp
from collections import Counter
from fractions import Fraction

mp.mp.dps = 40
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))

W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
v = W['v']; R = W['R']; nreg = 2*v+R; NF = len(W['frames'])
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


bases = [rref_int([lines[i] for i in W['frames'][F]]) for F in range(NF)]
dims = [len(b) for b in bases]


def contains(b, row):
    row = list(row)
    for br in b:
        c = next((i for i, x in enumerate(row) if x), None)
        if c is None: break
        bc = next((i for i, x in enumerate(br) if x), None)
        if bc == c:
            f = row[c]/br[c]
            row = [(a - f*bb) for a, bb in zip(row, br)]
    return all(x == 0 for x in row)


# the wire contents (the replay)
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

wires = {}
for F, d, ss in B:
    for s in ss:
        if s >= 2*v:
            wires.setdefault(s, set()).update(i for i in range(v) if (mask_of(val[s]) >> i) & 1)
print('the wires: %d' % len(wires), flush=True)

# (1) the content-spans + the dim-6 candidates
dim6 = [G for G in range(NF) if dims[G] == 6]
print('the dim-6 frames: %d' % len(dim6), flush=True)
span_hist = Counter()
cand_hist = Counter()
wire_cands = {}
for q, ls in wires.items():
    ls = sorted(ls)
    sp = len(rref_int([lines[i] for i in ls]))
    span_hist[sp] += 1
    cs = [G for G in dim6 if all(contains(bases[G], lines[i]) for i in ls)]
    cand_hist[min(len(cs), 20)] += 1
    wire_cands[q] = cs
print('the wires\' content-spans:', dict(sorted(span_hist.items())))
print('the dim-6 candidate-counts (capped 20):', dict(sorted(cand_hist.items())))

# (2) the sources' sharing: per source, its reader-wires + their candidate-intersections
readers = {}
for q, ls in wires.items():
    for i in ls:
        readers.setdefault(i, set()).add(q)
share_ok = Counter()
for s, rws in readers.items():
    if len(rws) <= 1:
        share_ok['single'] += 1
        continue
    inter = set(wire_cands[next(iter(rws))])
    for q in rws:
        inter &= set(wire_cands[q])
    if inter:
        share_ok['shared'] += 1
    else:
        share_ok['SPLIT'] += 1
print('the sources\' sharing:', dict(share_ok))
# the honest hist: the sources: the single-visit ({5, 2}) for the shared; the split ones
# need 2+ dim-6 visits: the chains 1 -> 6a -> 8 then the dup/extra visit
n_split = share_ok.get('SPLIT', 0)
n_single = share_ok.get('single', 0)
n_shared = share_ok.get('shared', 0)
print('  => the sources: %d shared (one visit: {5,2}), %d split, %d single' % (n_shared, n_split, n_single))
# the hist: the shared/single sources: {5: 1, 2: 1} each (the mass 7); the split: +1 visit
# (the second dim-6: the rank-0 no-op if nested... the honest: the dup-copy (+1 register!!))
# the wires: one-gate at the dim-6: {6: 1} + the B (6->7: {1}) + the C (7->8: {1})
hist = {}
hist[5] = hist.get(5, 0) + n_shared + n_single + n_split
hist[2] = hist.get(2, 0) + n_shared + n_single + n_split
hist[6] = hist.get(6, 0) + len(wires)
hist[1] = hist.get(1, 0) + len(wires) + len(wires)
# the targets: {7}
hist[7] = hist.get(7, 0) + v
# the totals: {7, 1} + the copy {7}
hist[7] = hist.get(7, 0) + 9
hist[1] = hist.get(1, 0) + 9
hist[7] = hist.get(7, 0) + 9
# the dup-copies for the split sources (each +1 register: {6, 1} + {2}?!: the dup: 0->6->{1}...)
ndup = n_split
R2 = len(wires) + 9 + ndup
hist[6] = hist.get(6, 0) + ndup
hist[1] = hist.get(1, 0) + ndup
hist[2] = hist.get(2, 0) + ndup
mass = sum(r*c for r, c in hist.items())
ident = 8*R2 + 63 + 2*v*7
print('the honest hist:', dict(sorted(hist.items())), 'mass', mass, 'identity', ident)
if mass == ident:
    from pricer import idle_slots, host_greedy
    K, T = 4, 32
    L = 2*K+1; a = 7; m_ = 1+L*a; w = 8
    slots = {}
    for c in idle_slots(K, a):
        slots[c] = slots.get(c, 0) + 2*v
    WW = 2*K*v*T

    def F_of(H, Rr, q):
        nres = Rr*L
        rem = host_greedy(slots, nres, w, q, m_)
        prof = {}
        for r, z in H.items(): prof[r] = prof.get(r, 0) + z*T*L
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z*T
        tot = sum(prof.values())
        s = sum(mp.mpf(r)*z/(m_*WW)*(mp.mpf(m_)/r)**q for r, z in prof.items() if r < m_)
        s += 32*m_*mp.mpf(tot)/(mp.mpf(10)**16 * WW)*mp.mpf(m_)**q
        return s - 1

    lo, hi = mp.mpf(0), mp.mpf('0.05')
    if F_of(hist, R2, lo) >= 0:
        print('NO-ROOT (F(0) >= 0)')
    else:
        for _ in range(60):
            mid = (lo+hi)/2
            if F_of(hist, R2, mid) >= 0: hi = mid
            else: lo = mid
        q = (lo+hi)/2
        P111 = mp.mpf('0.001733052823330162099157')
        print('THE HONEST SHAPE PRICE: %s (%+.2f%%)' % (mp.nstr(q, 8), float((q-P111)/P111)*100))
else:
    print('MASS-MISMATCH: the model needs the dup-structure refined')
