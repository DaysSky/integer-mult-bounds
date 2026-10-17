"""Exact linear budget at the frontier: c >= q* iff sum_children z_r * r((m/r)^q* - 1) <= m W - mass.
With all residuals hosted, mW - mass = T(8v - 9 cst).  Costs in units of T: local child x 9, idle remainder x 1."""
import math
QSTAR = 0.001734473240795253742474   # E1 frontier
def cost(r, m, q=QSTAR):
    return 0.0 if r <= 0 or r >= m else r * ((m / r) ** q - 1)
def slots(h, K=4):
    a = h - 1; sl = []
    if 2*K-2 > 0: sl.append(a*(2*K-2))
    for p in range(1, K):
        sl += [2*p*a, a]
        if 2*K-2*p-2 > 0: sl.append(a*(2*K-2*p-2))
    return sl
if __name__ == '__main__':
    for h in (8, 11, 13):
        m = 1 + 9*(h-1)
        print('h', h, 'm', m, 'slots', slots(h))
        print('  cost(r)*9:', ' '.join('%d:%.4f' % (r, 9*cost(r, m)) for r in range(1, h+1)))
        print('  per-unit-mass 9cost/r:', ' '.join('%d:%.4f' % (r, 9*cost(r, m)/r) for r in range(1, h+1)))
        idle = 2*sum(cost(c, m) for c in slots(h))
        print('  idle per line (unhosted):', round(idle, 4))
