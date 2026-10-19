"""nat138: THE TARGETS' B-CHAIN CENSUS + THE TPERP-REFRAME.

(1) The per-target B-gate frames (the targets' ladders + their hist contribution).
(2) The direct-source-reads in B (the per-source target-counts).
(3) The TPERP-reframe: the B-gates re-aimed at the targets' TPERP frames -
    the wires: 6->7 (rank 1); the sources: their extra TPERP visits ->
    THE DUP-COUNT (the per-source distinct TPERPs among its B-readers).
(4) The hist + the price at the reframe.
"""
import json, gzip, os, sys
import mpmath as mp
from collections import Counter

mp.mp.dps = 40
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))

W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
v = W['v']; R = W['R']; nreg = 2*v+R
A = W['A']; B = W['B']; D = W['D']
dims = [len(r) for r in W['frames_full']] if 'frames_full' in W else None
# the frame dims via the frames' line-sets (from the adapter convention: line-index lists)
lines = W['lines']
from fractions import Fraction

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

fdim = {}
for F in range(len(W['frames'])):
    fdim[F] = len(rref_int([lines[i] for i in W['frames'][F]]))

# (1) the targets' B-chains
chains = {}
for F, d, ss in B:
    chains.setdefault(d, []).append(F)
tgt_frames = {d: sorted(set(F for F in Fs if F != chains[d][0] or True)) for d, Fs in chains.items()}
tgt_hist = Counter()
for d, Fs in chains.items():
    cur = 0
    for F in Fs:
        f0 = fdim[F]
        if f0 > cur:
            tgt_hist[f0 - cur] += 1
            cur = f0
    # the final: the TPERP (dim 7)
    if 7 > cur:
        tgt_hist[7 - cur] += 1
print('the targets\' B-chain hist contribution:', dict(sorted(tgt_hist.items())))
cnt = Counter(len(Fs) for d, Fs in chains.items())
print('the per-target B-gate counts:', dict(sorted(cnt.items())))

# (2) the direct-source-reads in B
src_B = {}
for F, d, ss in B:
    for s in ss:
        if s < v:
            src_B.setdefault(s, set()).add(d)
src_B_counts = Counter(len(ts) for s, ts in src_B.items())
print('the sources\' direct-B-reader (target) counts:', dict(sorted(src_B_counts.items())))
tot_direct = sum(len(ts) for s, ts in src_B.items())
print('the total direct source-read-events in B: %d' % sum(1 for F, d, ss in B for s in ss if s < v))

# (3) the dup-count: per source, its direct-B-targets are ALREADY distinct targets;
# the reframe: each source visits each reader-target's TPERP: the dup-count =
# sum over sources of (distinct TPERPs - 1)  [the first visit rides the chain]
dups = sum(max(0, len(ts) - 1) for s, ts in src_B.items())
print('THE DUP-COUNT (the sources\' extra TPERP visits): %d' % dups)

# (4) the hist + the price at the reframe:
# the targets: {7} (111 rank-7 climbs!) - all their mass at rank 7
# the sources: {1: 555, 2: 111} (the r434's own ladders) + the dups: the dup-copies
#   climb 1 -> TPERP (rank 6!) then TPERP -> 8 (rank 1): {6, 1} each
# the wires: {1: 450, 6: 225} (the nat136 model: the builds at 6, the B 6->7, the C 7->8)
# the totals: {7: 9, 1: 9} + the copy {7: 9}
hist = {}
hist[7] = 111 + 9 + 9
hist[1] = 555 + 450 + 9 + dups      # the sources' ladders + the wires + the totals + the dup-copies' final
hist[2] = 111
hist[6] = 225 + dups                # the wires' builds + the dup-copies' TPERP climbs
R_new = 225 + 9 + dups
mass = sum(r*c for r, c in hist.items())
ident = 8*R_new + 63 + 2*111*7
print('the reframe hist:', dict(sorted(hist.items())), '| mass', mass, '| identity', ident)
if mass != ident:
    print('MASS-MISMATCH - refine the model')
else:
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
    if F_of(hist, R_new, lo) >= 0:
        print('NO-ROOT')
    else:
        for _ in range(60):
            mid = (lo+hi)/2
            if F_of(hist, R_new, mid) >= 0: hi = mid
            else: lo = mid
        q = (lo+hi)/2
        P111 = mp.mpf('0.001733052823330162099157')
        print('R_new = %d | THE REFRAME PRICE: %s (%+.2f%%)' % (R_new, mp.nstr(q, 8), float((q-P111)/P111)*100))
