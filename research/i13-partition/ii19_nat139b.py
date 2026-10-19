"""nat139b: THE TPERP-REFRAME - minimal in-place (no reorder, no split).

Per target-dest B-gate, in the ORIGINAL order: re-aim to final[t] iff
(1) it is a pure wire gate (no source srcs),
(2) its position is after the target's last gate at a frame with dim < 7,
(3) every wire's A-end frame is a subspace of final[t] (the content law already
    gives the lines; the frame-containment checked per gate).
Everything else untouched: the z-gates, the source-parts, the order.
Then: the hist replay + the mass + the adapter + gcheck + the price.
"""
import json, gzip, os, sys, copy
import mpmath as mp
from fractions import Fraction
from collections import Counter

mp.mp.dps = 40
W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
v = W['v']; R = W['R']; nreg = 2*v+R
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


def sub(a, b):
    if a == b: return True
    if dims[a] > dims[b]: return False
    bb = bases[b]
    for row in bases[a]:
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


# the targets' last low-frame gate (dim < 7)
last_low = {}
for i, (F, d, ss) in enumerate(B):
    if v <= d < 2*v and dims[F] < 7:
        last_low[d] = i
# the wires' A-end frames (the replay)
curA = list(start)
for F, d, ss in D:
    for p in [d] + list(ss): curA[p] = F
for F, d, ss in A:
    for p in [d] + list(ss): curA[p] = F

B2 = []
n_aim = 0
for i, (F, d, ss) in enumerate(B):
    if (v <= d < 2*v and not ss  # hmm - a gate with no srcs? keep anyway
            or True):
        pass
    if v <= d < 2*v and ss and all(s >= 2*v for s in ss) and i > last_low.get(d, -1) and all(sub(curA[s], final[d]) for s in ss):
        B2.append((final[d], d, list(ss)))
        n_aim += 1
    else:
        B2.append((F, d, list(ss)))
print('the re-aimed gates: %d of %d' % (n_aim, len(B)))

# THE HIST + the mass (the full replay)
hist = {}
cur2 = list(start)
def climb(r, F):
    assert cur2[r] == F or (dims[cur2[r]] < dims[F] and sub(cur2[r], F)), ('climb fail', r, cur2[r], F)
    if cur2[r] != F:
        hist[dims[F] - dims[cur2[r]]] = hist.get(dims[F] - dims[cur2[r]], 0) + 1
        cur2[r] = F

for F, d, ss in D:
    climb(d, F)
    for s in ss: climb(s, F)
for F, d, ss in A:
    climb(d, F)
    for s in ss: climb(s, F)
rf = []
for q in W['ret']:
    rf.append(cur2[q])
    hist[dims[cur2[q]]] = hist.get(dims[cur2[q]], 0) + 1
cst = sum(dims[f] for f in rf)
for F, d, ss in B2:
    climb(d, F)
    for s in ss: climb(s, F)
for F, d, ss in C:
    climb(d, F)
    for s in ss: climb(s, F)
for r in range(nreg):
    climb(r, final[r])
mass = sum(k*n for k, n in hist.items())
ident = 8*R + cst + 2*v*7
print('the hist:', dict(sorted(hist.items())))
print('the mass: %d | the identity: %d | cst %d' % (mass, ident, cst))
assert mass == ident, 'MASS-MISMATCH'
# THE PRICE
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
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
assert F_of(hist, R, lo) < 0
for _ in range(60):
    mid = (lo+hi)/2
    if F_of(hist, R, mid) >= 0: hi = mid
    else: lo = mid
q = (lo+hi)/2
P111 = mp.mpf('0.001733052823330162099157')
print('THE REFRAME PRICE: %s (%+.2f%%)' % (mp.nstr(q, 8), float((q-P111)/P111)*100))

# THE WORD + GCHECK
W2 = dict(W)
W2['B'] = B2
W2['ret_frames'] = rf
W2['frames_full'] = None
W2.pop('frames_full', None)
# the adapter convention: frames as vector lists + ret_frames
W2['frames'] = [[list(lines[i]) for i in F] for F in W['frames']]
json.dump(W2, gzip.open('/tmp/r434-reframed.json.gz', 'wt'))
print('SAVED /tmp/r434-reframed.json.gz')
