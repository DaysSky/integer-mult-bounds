import sys
from fractions import Fraction as Q
import ceiling as C
WORD = {1: 2412, 2: 418, 3: 432, 4: 142, 5: 82, 8: 8}
noncopy = {r: n for r, n in WORD.items() if r != 8}
mass_nc = sum(r * n for r, n in noncopy.items())   # 5522
data = 1792
helper_mass_per = Q(mass_nc - data, 492)
base = C.ceiling(WORD, 73, 896, 9, 64, grid=Q(1, 10**12))[1]
print('baseline a', float(base))
for h in (492, 300, 224, 150, 112, 56, 0):
    scale = (data + helper_mass_per * h) / mass_nc
    local = {r: n * scale for r, n in noncopy.items()}; local[8] = 8
    lm = sum(r * n for r, n in local.items())
    row = []
    for s in (5, 7, 9, 11, 13):
        m = 1 + 8 * s; K = (s - 1) // 2; fam = 2 * K * 112
        cover = (m - 1) * Q(fam, s) + 64
        if lm > cover:
            row.append('s%d: infeasible (local %.0f > cover %.0f)' % (s, float(lm), float(cover))); continue
        try:
            a = C.ceiling(local, m, fam, s, 64, grid=Q(1, 10**12))[1]
            row.append('s%d: x%.2f' % (s, float(a / base)))
        except Exception as e:
            row.append('s%d: err %s' % (s, str(e)[:30]))
    print('helpers %3d local mass %.0f | ' % (h, float(lm)) + ' | '.join(row), flush=True)
