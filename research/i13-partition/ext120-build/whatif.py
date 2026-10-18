import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price
from mpmath import mpf
from collections import Counter
P111 = mpf('0.001733052823330162099157')
def pct(H, R, v=120, h=8):
    c, _, d = price(dict(H), v, h, R)
    return None if c is None else round(float((c / P111 - 1) * 100), 3)
def hist(roles, cst=72):
    H = Counter({8: 9})
    for n, steps in roles:
        for s in steps: H[s] += n
    return H
base = [(120, (1,2,2,1,1)), (120, (2,5)), (96, (1,1,2,2,1,1)), (96, (2,2,2,2)), (84, (1,1,2,2,2)), (84, (2,2,2,1,1)), (60, (1,1,4,1,1))]
def R_of(roles): return sum(n for n, s in roles[2:])
print('base', pct(hist(base), 420))
variants = {
 'src skip tperp (1,2,2,2)': [(120,(1,2,2,2))] + base[1:],
 'src (1,2,3,2)?': [(120,(1,2,3,1,1))] + base[1:],
 'tgt (7)': [base[0], (120,(7,))] + base[2:],
 'hlp all (2,2,2,2)': base[:2] + [(420,(2,2,2,2))],
 'hlp all (2,2,4)': base[:2] + [(420,(2,2,4))],
 'hlp all (4,4)': base[:2] + [(420,(4,4))],
 'hlp all (8)': base[:2] + [(420,(8,))],
 'hlp 1,1 prefixes -> 2': base[:2] + [(96,(2,2,2,1,1)), (96,(2,2,2,2)), (84,(2,2,2,2)), (84,(2,2,2,1,1)), (60,(2,4,1,1))],
 'hlp 1,1 suffix -> 2': base[:2] + [(96,(1,1,2,2,2)), (96,(2,2,2,2)), (84,(1,1,2,2,2)), (84,(2,2,2,2)), (60,(1,1,4,2))],
}
for k, r in variants.items():
    print(k, pct(hist(r), R_of(r)))
for drop in (60, 120, 180, 240):
    r = base[:2] + [(96,(1,1,2,2,1,1)), (96,(2,2,2,2)), (84,(1,1,2,2,2)), (84,(2,2,2,1,1)), (60,(1,1,4,1,1))]
    # drop helpers proportionally from the (1,1,2,2,1,1) and (2,2,2,1,1)
    rr = base[:2] + [(max(0,96-drop//2),(1,1,2,2,1,1)), (96,(2,2,2,2)), (84,(1,1,2,2,2)), (max(0,84-drop//2),(2,2,2,1,1)), (60,(1,1,4,1,1))]
    print('drop', drop, R_of(rr), pct(hist(rr), R_of(rr)))
