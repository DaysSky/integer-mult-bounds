import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer as P
from mpmath import mpf, mp
ref = mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
def price_over(local, v, h, R, K, T=32):
    L = 2 * K + 1; a = h - 1; m = 1 + L * a; w = h
    slots = {}
    for c in P.idle_slots(K, a): slots[c] = slots.get(c, 0) + 2 * v
    nres = R * L
    cap = sum(n * (c // w) for c, n in slots.items())
    nh = min(nres, cap); over = nres - nh
    W = 2 * K * v * T
    q = mpf('0.0017')
    for _ in range(40):
        rem = P.host_greedy(slots, nh, w, q, m)
        prof = {}
        for r, z in local.items(): prof[r] = prof.get(r, 0) + z * T * L
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
        # overflow residuals: paid on bank wires as rank-w children, D unchanged -> add as extra children but keep W budget:
        # pressure form sum z g(r) = D; P.root uses sum z r (m/r)^q / (mW) = 1 i.e. mass identity. Add bank wire: W += over*T/(L?)
        prof2 = dict(prof)
        prof2[w] = prof2.get(w, 0) + over * T
        # each bank-wire child adds w to mass and w to the m*W budget (zero net saving): extra W = over*T*w/m
        Wb = W + mpf(over * T * w) / m
        q2 = P.root(prof2, m, Wb, env=False)
        if q2 is None: return None
        if abs(q2 - q) < mpf(10) ** -25: break
        q = q2
    return q2, over, cap
for K in (2, 3, 4, 5):
    r = price_over(tuned, 111, 8, 439, K)
    if r is None: print(K, "no root"); continue
    print(K, 'over', r[1], 'cap', r[2], mp.nstr(r[0], 10), '%+.2f%%' % float((r[0] / ref - 1) * 100))
