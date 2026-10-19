"""Where a wide-margin II19 win would have to come from (exact pricer; shapes are models, not words).
(1) one-climb ceiling vs R/v; (2) even k-climb shapes vs R/v; (3) an idealized 3-climb middle at known
E8-class densities; (4) the 'no bridge split' idle-slot scope rule on the frontier and on II19-112."""
import _common  # noqa: F401  (puts the pricer on sys.path)
import pricer
from _common import FRONTIER, pct, transplant, W4T, COPY_W4T, R434

def split(D, k):
    k = min(k, D); b, e = divmod(D, k); return [b + 1] * e + [b] * (k - e)
def shape(v, h, R, ks, kt, kh, copies):
    hist = {}
    for k, n in ((ks, v), (kt, v)):
        for r in split(h - 1, k): hist[r] = hist.get(r, 0) + n
    for r in split(h, kh): hist[r] = hist.get(r, 0) + R
    for r, z in copies.items(): hist[r] = hist.get(r, 0) + z
    return hist
SYS = (('E8/P111   h=8 cst 63', 111, 8, {7: 9}), ('II19-112  h=9 cst 64', 112, 9, {7: 8, 8: 1}))

print('(1)+(2) even k climbs per register (sources, targets, helpers), vs R/v')
for nm, v, h, cop in SYS:
    print(' ', nm)
    for rr in (1.0, 2.0, 3.0, 3.9):
        R = int(rr * v)
        print('    R/v %.1f  ' % rr + '  '.join('k=%d %+6.1f%%' % (k, pct(shape(v, h, R, k, k, k, cop), v, h, R)[0])
                                            for k in (1, 2, 3, 4, 5)))
print('\n(3) idealized middle: targets 2 climbs, sources and helpers 3 climbs')
for nm, v, h, cop in SYS:
    print('  %-22s' % nm + '  '.join('R/v %.2f %+6.1f%%' % (rr, pct(shape(v, h, int(rr * v), 3, 2, 3, cop), v, h, int(rr * v))[0])
                                   for rr in (3.25, 3.5, 3.9)))
print('\n(4) idle-slot scope rule "no bridge split" (pricer slots patched locally)')
orig = pricer.idle_slots
w112 = transplant(W4T, COPY_W4T, 112, 9, 437, {7: 8, 8: 1})
for nm, hist, v, h, R in (('r434 frontier', R434, 111, 8, 434), ('II19-112 (W4 shape)', w112, 112, 9, 437)):
    a = pct(hist, v, h, R)[0]
    pricer.idle_slots = lambda K, aa, split=True: orig(K, aa, split=False)
    try:
        b = pct(hist, v, h, R)[0]
    finally:
        pricer.idle_slots = orig
    print('  %-20s as priced %+6.2f%%   no bridge split %+6.2f%%' % (nm, a, b))
