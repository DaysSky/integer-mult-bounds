"""Generalised nine-stage pricer: L stages, P pairs, arbitrary idle slots per port copy (two copies per port),
same root equation and greedy whole-residual hosting as code/price/pricer.py."""
import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer as P
from mpmath import mpf
def price(local, v, h, R, L, pairs, idle, T=32, w=None):
    a = h - 1; m = 1 + L * a; w = h if w is None else w
    slots = {}
    for c in idle: slots[c] = slots.get(c, 0) + 2 * v
    nres = R * L; W = 2 * pairs * v * T
    cap = sum(n * (c // w) for c, n in slots.items())
    if nres > cap: return None, dict(error='hosting wall', cap=cap, nres=nres)
    q = mpf('0.0017')
    for _ in range(40):
        rem = P.host_greedy(slots, nres, w, q, m)
        prof = {}
        for r, z in local.items(): prof[r] = prof.get(r, 0) + z * T * L
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
        q2 = P.root(prof, m, W)
        if q2 is None: return None, dict(error='no root')
        if abs(q2 - q) < mpf(10) ** -30: break
        q = q2
    return q2, dict(m=m, W=W, rem=rem, deficit=m * W - sum(r * z for r, z in prof.items()))
def triples_idle(pairs, a):
    # pair p active at stages 3p..3p+2 of L = 3*pairs; idle pre 3p*a, post (L-3p-3)*a
    L = 3 * pairs; out = []
    for p in range(pairs):
        if 3 * p > 0: out.append(3 * p * a)
        if L - 3 * p - 3 > 0: out.append((L - 3 * p - 3) * a)
    return L, out
if __name__ == '__main__':
    import mpmath as mp
    ref = mp.mpf('0.001733427039589844')
    tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
    c, d = price(tuned, 111, 8, 439, 9, 4, P.idle_slots(4, 7)); print('control B_K L=9:', mp.nstr(c, 12))
    for pairs in (3, 4, 5, 6):
        L, idle = triples_idle(pairs, 7)
        c, d = price(tuned, 111, 8, 439, L, pairs, idle)
        print('independent triples: pairs %d, L %d, idle %s ->' % (pairs, L, idle), (mp.nstr(c, 10) + '  %+.2f%%' % float((c / ref - 1) * 100)) if c else d)
