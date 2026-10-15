"""Exact nine-stage bit price of a local word (generic window h), following the hub's #463/#510 template as replayed
for PR589/P111: global profile = (replicas * stages) x local histogram + idle remainders after whole hosting of the
helper residuals; c = root of  sum_r z_r (r/(mW)) (m/r)^q + 32 m (sum z) m^q / (1e16 W) = 1,  m = 1 + L(h-1),
W = live = 2 K v T (+ banks).  Idle slots per port copy: skel.idle_slots(K, a) with a = h - 1, two copies per port.
Hosting: each helper of width w (= h - its start dim) is hosted once per stage; a slot of capacity c hosting widths
summing to u leaves one paid child of rank c - u (none if 0).  The hosting optimum over slot fillings is found by
exact enumeration of per-slot-type filling counts (uniform width) with the cost evaluated at the root (fixed point)."""
from mpmath import mp, mpf, findroot
from fractions import Fraction as Fr
import itertools, sys
mp.dps = 40

def idle_slots(K, a, split=True):
    sl = []
    if K >= 1 and 2 * K - 2 > 0: sl.append(a * (2 * K - 2))
    for p in range(1, K):
        sl += [2 * p * a, a] if split else [(2 * p + 1) * a]
        if 2 * K - 2 * p - 2 > 0: sl.append(a * (2 * K - 2 * p - 2))
    return sl

def root(prof, m, W, env=True):
    tot = sum(prof.values())
    def F(q):
        s = sum(mpf(r) * z / (m * W) * (mpf(m) / r) ** q for r, z in prof.items() if r < m)
        s += sum(mpf(r) * z / (m * W) for r, z in prof.items() if r >= m) * 0   # rank >= m children cost nothing
        if env: s += 32 * m * mpf(tot) / (mpf(10) ** 16 * W) * mpf(m) ** q
        return s - 1
    lo, hi = mpf(0), mpf('0.05')
    if F(lo) >= 0: return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if F(mid) >= 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2

def host(slot_counts, nres, w, q, m):
    """uniform width w: choose for each slot type c how many slots host j residuals (0..c//w) to host nres residuals,
    minimising sum of f(c - j w) with f(r) = r ((m/r)^q - 1) (f(0) = 0).  Greedy by marginal saving is exact here
    because for a fixed slot type the savings are taken best-first and slot types are independent (separable convex
    knapsack over unit 'host one more' moves is not convex in general, so we do an exact DP over slot types)."""
    f = lambda r: mpf(0) if r <= 0 else mpf(r) * ((mpf(m) / r) ** q - 1)
    types = sorted(slot_counts)
    # options per slot: j hosted, cost f(c - j w); per type, total hosted t with n slots: best is to fill slots as
    # evenly or as unevenly as is cheapest -- enumerate (number of slots at each j) is large; use DP over residual count
    # with per-type best cost g_c(t) computed by inner DP over slots of that type using fill levels.
    INF = None
    best = {0: (mpf(0), {})}
    for c in types:
        n = slot_counts[c]; J = c // w
        # per-type: hosting t residuals in n slots; cost = sum over slots f(c - j_i w); since f is concave-ish in hosted
        # amount, optimal fills slots fully except at most one partial (exchange argument checked numerically below)
        g = {}
        for t in range(0, min(nres, n * J) + 1):
            full, rem = divmod(t, J) if J else (0, 0)
            if J == 0:
                if t == 0: g[0] = (n * f(c), {c: n})
                continue
            if full > n or (full == n and rem): continue
            cost = full * f(c - J * w) + (f(c - rem * w) if rem else 0) + (n - full - (1 if rem else 0)) * f(c)
            prof = {}
            for r, k in ((c - J * w, full), (c - rem * w, 1 if rem else 0), (c, n - full - (1 if rem else 0))):
                if k and r > 0: prof[r] = prof.get(r, 0) + k
            g[t] = (cost, prof)
        nb = {}
        for h0, (c0, p0) in best.items():
            for t, (c1, p1) in g.items():
                if h0 + t > nres: continue
                tot = c0 + c1
                if (h0 + t) not in nb or tot < nb[h0 + t][0]:
                    pp = dict(p0)
                    for r, k in p1.items(): pp[r] = pp.get(r, 0) + k
                    nb[h0 + t] = (tot, pp)
        best = nb
    if nres not in best: return None
    return best[nres][1]

def host_greedy(slot_counts, nres, w, q, m):
    """fill slot types fully in decreasing per-residual saving, one partial slot at the end (concave f)"""
    f = lambda r: mpf(0) if r <= 0 else mpf(r) * ((mpf(m) / r) ** q - 1)
    order = []
    for c, n in slot_counts.items():
        J = c // w
        if J: order.append(((f(c) - f(c - J * w)) / J, c, n, J))
    order.sort(reverse=True)
    rem = {c: n for c, n in slot_counts.items()}
    left = nres
    prof = {}
    for sav, c, n, J in order:
        if left <= 0: break
        full = min(n, left // J)
        left -= full * J
        rem[c] -= full
        if c - J * w > 0 and full: prof[c - J * w] = prof.get(c - J * w, 0) + full
        if left and rem[c] and left < J:
            rem[c] -= 1
            prof[c - left * w] = prof.get(c - left * w, 0) + 1
            left = 0
    if left > 0: return None
    for c, n in rem.items():
        if n: prof[c] = prof.get(c, 0) + n
    return prof

HOST = 'greedy'
def price(local, v, h, R, K=4, T=32, w=None, start_dims=None):
    """local: {rank: count} per local word; returns (c, global profile, details)."""
    L = 2 * K + 1; a = h - 1; m = 1 + L * a; w = h if w is None else w
    slots = {}
    for c in idle_slots(K, a):
        slots[c] = slots.get(c, 0) + 2 * v
    nres = R * L                                     # residuals per replica
    W = 2 * K * v * T
    cap = sum(n * (c // w) for c, n in slots.items())
    if nres > cap: return None, None, dict(error='hosting wall', cap=cap, nres=nres)
    q = mpf('0.0017')
    for _ in range(30):
        rem = host_greedy(slots, nres, w, q, m) if HOST == 'greedy' else host(slots, nres, w, q, m)
        prof = {}
        for r, z in local.items(): prof[r] = prof.get(r, 0) + z * T * L
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
        q2 = root(prof, m, W)
        if q2 is None: return None, prof, dict(error='no root')
        if abs(q2 - q) < mpf(10) ** -30: break
        q = q2
    return q2, prof, dict(m=m, W=W, rem_per_replica=rem, mass=sum(r * z for r, z in prof.items()), deficit=m * W - sum(r * z for r, z in prof.items()))

if __name__ == '__main__':
    import pricer as _p
    p111 = {1: 1321, 2: 1342, 3: 80, 4: 47, 5: 102, 6: 10, 7: 18}
    c, prof, d = price(p111, 111, 8, 439)
    print('P111 c =', mp.nstr(c, 25), 'published 0.001733052823330162099157', d['rem_per_replica'], 'deficit', d['deficit'])
    r420 = {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}
    c, prof, d = price(r420, 120, 8, 420)
    print('R420 c =', mp.nstr(c, 25), 'published 0.001653826988146798944268', d['rem_per_replica'], 'deficit', d['deficit'])
