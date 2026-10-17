import sys
sys.path.insert(0, '.')
from lclosed import *
def L(S):
    S = set(S); U = 0
    for s in range(V):
        if set(SUPP[s]) <= S: U |= 1 << s
    return U
L7 = L(range(4, 11))
lv = closed_sets(L7, 5)
for k in (2, 3, 4):
    print('kappa_%d(L7)' % k, kappa(L7, lv[k], tl=120), flush=True)
print('kappa_5(L7)', kappa(L7, lv[5], tl=300), flush=True)
L5 = L(range(6, 11))
print('L5 lines', pc(L5))
for k in (2, 3, 4): print('kappa_%d(L5)' % k, kappa(L5, [S for S in lv[k] if S & L5], tl=60), flush=True)
L3 = L(range(8, 11)); print('kappa_2(L3)', kappa(L3, [S for S in lv[2] if S & L3]))
A3 = 0
for s in range(V):
    if KIND[s] == 'P' and set(SUPP[s]) <= {7, 8, 9, 10}: A3 |= 1 << s
print('kappa_2(A3)', kappa(A3, [S for S in lv[2] if S & A3]))
