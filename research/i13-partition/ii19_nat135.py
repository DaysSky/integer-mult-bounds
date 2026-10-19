"""nat135: THE SHAPE-ROUTE TRADE-MAP (the one-climb vs the sharing balance).

The parametrized hist-model at v=111 (cst=63):
- the sources: the k-frame ladders: 1 -> d1 -> ... -> 8 (k steps): the mass 7 (dim 1 -> 8)
  spread over k ranks; the reads: the ~19 each (the sharing (the r434's!!) if k >= 2
  (the shared ladders!), the dup-cost if k = 1: the source read at ~19 distinct perp-frames
  -> ~19 dup-copies!! (the R-explosion))
- the wires: the m-frame builds: 0 -> ... -> 8: the mass 8 over m ranks; the wires
  private (2-3 per target: the r434's own!!) - no dup-cost
- the targets: {7} fixed; the totals: {7, 1}; the copy: 9 x rank 7
The R(k, m) = 225 (the wires) + 9 + the sources' dup-cost(k) + the wires' dup-ish(m)
The price at each (k, m) via the F-inspection (the honest root).
"""
import os, sys
import mpmath as mp
mp.mp.dps = 40
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import idle_slots, host_greedy

v, h, K, T = 111, 8, 4, 32
L = 2*K+1; a = h-1; m_ = 1+L*a; w = h
slots = {}
for c in idle_slots(K, a):
    slots[c] = slots.get(c, 0) + 2*v
W = 2*K*v*T

def F_of(hist, R, q):
    nres = R*L
    rem = host_greedy(slots, nres, w, q, m_)
    prof = {}
    for r, z in hist.items(): prof[r] = prof.get(r, 0) + z*T*L
    for r, z in rem.items(): prof[r] = prof.get(r, 0) + z*T
    tot = sum(prof.values())
    s = sum(mp.mpf(r)*z/(m_*W)*(mp.mpf(m_)/r)**q for r, z in prof.items() if r < m_)
    s += 32*m_*mp.mpf(tot)/(mp.mpf(10)**16 * W)*mp.mpf(m_)**q
    return s - 1

def root_of(hist, R):
    lo, hi = mp.mpf(0), mp.mpf('0.05')
    if F_of(hist, R, lo) >= 0: return None
    for _ in range(60):
        mid = (lo+hi)/2
        if F_of(hist, R, mid) >= 0: hi = mid
        else: lo = mid
    return (lo+hi)/2

P111 = mp.mpf('0.001733052823330162099157')
cst = 63

def model(k, m):
    """k: the sources' ladder-length (1 = the one-climb (the dup-cost!!)); m: the wires' build-length.
    Returns (R, hist)."""
    # the sources: the mass 7 over k steps; the dup-cost: k=1: the ~19 reads at the
    # distinct perps -> the dup-copies ~19-1 = 18 extra per source?! -> the honest model:
    # k=1: R_src_dups = 111 * 18; k>=2: 0 (the shared ladders)
    src_dups = 111 * 18 if k == 1 else (111 * 5 if k == 2 else 0)
    R = 225 + 9 + src_dups
    # the hist: the sources: the mass 7 over k steps (the ranks ~ 7/k each!!):
    hist = {}
    if k == 1:
        hist[6] = hist.get(6, 0) + 111   # 1 -> 7 (the rank 6!!!) then 7 -> 8
        hist[1] = hist.get(1, 0) + 111
    elif k == 2:
        hist[3] = hist.get(3, 0) + 111  # 1 -> 4 -> 7-ish
        hist[2] = hist.get(2, 0) + 111
        hist[1] = hist.get(1, 0) + 111
    elif k == 3:
        hist[2] = hist.get(2, 0) + 111*2
        hist[1] = hist.get(1, 0) + 111*2
    else:  # k = 5 (the r434-ish)
        hist[1] = hist.get(1, 0) + 111*4
        hist[2] = hist.get(2, 0) + 111*1
        hist[1] = hist.get(1, 0) + 111*1
    # the wires: the mass 8 over m steps
    if m == 1:
        hist[7] = hist.get(7, 0) + 225
        hist[1] = hist.get(1, 0) + 225
    elif m == 2:
        hist[4] = hist.get(4, 0) + 225
        hist[3] = hist.get(3, 0) + 225
        hist[1] = hist.get(1, 0) + 225
    elif m == 3:
        hist[2] = hist.get(2, 0) + 225*2
        hist[1] = hist.get(1, 0) + 225*2
    else:  # m = 4+ (the r434-ish)
        hist[2] = hist.get(2, 0) + 225*3
        hist[1] = hist.get(1, 0) + 225*3
    # the targets: {7}
    hist[7] = hist.get(7, 0) + 111
    # the totals: {7, 1} + the copy: 9 x 7
    hist[7] = hist.get(7, 0) + 9
    hist[1] = hist.get(1, 0) + 9
    hist[7] = hist.get(7, 0) + 9   # the copy_ranks
    # the mass check
    mass = sum(r*c for r, c in hist.items())
    ident = 8*R + cst + 2*v*7
    return R, hist, mass, ident

print('k  m   R     mass/ident   price')
for k in (1, 2, 3, 5):
    for m in (1, 2, 3, 4):
        R, hist, mass, ident = model(k, m)
        if mass != ident:
            print('%-2d %-2d  %-5d %s/%s  MASS-MISMATCH' % (k, m, R, mass, ident))
            continue
        q = root_of(hist, R)
        if q is None:
            print('%-2d %-2d  %-5d %s/%s  NO-ROOT' % (k, m, R, mass, ident))
        else:
            print('%-2d %-2d  %-5d %s/%s  %s (%+.2f%%)' % (k, m, R, mass, ident,
                  mp.nstr(q, 8), float((q-P111)/P111)*100))
