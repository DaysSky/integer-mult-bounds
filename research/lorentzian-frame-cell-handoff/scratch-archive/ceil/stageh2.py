from fractions import Fraction as Q
import ceiling as C
WORD = {1: 2412, 2: 418, 3: 432, 4: 142, 5: 82, 8: 8}
noncopy = {r: n for r, n in WORD.items() if r != 8}
mass_nc = sum(r * n for r, n in noncopy.items())
data = 1792
helper_mass_per = Q(mass_nc - data, 492)
base = C.ceiling(WORD, 73, 896, 9, 64, grid=Q(1, 10**12))[1]
mix = {r: Q(n * r, mass_nc) for r, n in noncopy.items()}   # mass fraction by rank
def hist(data_mode, h, hmode):
    loc = {}
    def addmass(mass, mode):
        if mode == 'unit': loc[1] = loc.get(1, 0) + mass
        elif mode == 'rank2': loc[2] = loc.get(2, 0) + mass / 2
        else:
            for r, f in mix.items(): loc[r] = loc.get(r, 0) + mass * f / r
    addmass(data, data_mode); addmass(helper_mass_per * h, hmode); loc[8] = loc.get(8, 0) + 8
    return loc
for dm, hm in (('unit', 'mix'), ('mix', 'unit'), ('unit', 'unit'), ('rank2', 'rank2')):
    out = []
    for h in (492, 224, 112, 0):
        loc = hist(dm, h, hm); lm = sum(r * n for r, n in loc.items())
        best = None
        for s in (7, 9, 11):
            m = 1 + 8 * s; K = (s - 1) // 2; fam = 2 * K * 112
            if lm > (m - 1) * Q(fam, s) + 64: continue
            a = C.ceiling(loc, m, fam, s, 64, grid=Q(1, 10**12))[1]
            if best is None or a > best[0]: best = (a, s)
        out.append('h%d: x%.2f (s%d)' % (h, float(best[0] / base), best[1]) if best else 'h%d: infeasible' % h)
    print('data %-5s helpers %-5s | ' % (dm, hm) + ' | '.join(out), flush=True)
