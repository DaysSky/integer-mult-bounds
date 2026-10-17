"""Does the stage template (K, L = 2K+1) change Lorentzian vs E8 standing?  Generic chains (as i13ent), break-even R/v
against P111-tuned's c at the same template (9-stage 0.0017334270, 11-stage 0.0017109519)."""
import sys, bisect
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots, root
from mpmath import mp
REF = {4: mp.mpf('0.001733427039589844'), 5: mp.mpf('0.001710951900777583975622')}
T = 32
def split(total, k):
    b, r = divmod(total, k); return [b + 1]*r + [b]*(k - r)
def price(K, h, v, cst, C, kc, H, e, kh, ks=2, kt=3):
    L = 2*K + 1; a = h - 1; m = 1 + L*a; W = 2*K*v*T
    loc = {}
    def add(r, z):
        if z: loc[r] = loc.get(r, 0) + z
    for p in split(h - 1, ks): add(p, v)
    for p in split(h - 1, kt): add(p, v)
    for p in split(h, kc): add(p, C)
    if H:
        for p in split(h - e, kh): add(p, H)
    q, r = divmod(cst, h - 1); add(h - 1, q); add(r, 1 if r else 0)
    free = sorted(c for c in idle_slots(K, a) for _ in range(2*v))
    res = sorted([h]*(C*L) + [h - e]*(H*L), reverse=True)
    for w in res:
        i = bisect.bisect_left(free, w)
        if i == len(free): return None
        c = free.pop(i)
        if c > w: bisect.insort(free, c - w)
    rem = {}
    for c in free: rem[c] = rem.get(c, 0) + 1
    prof = {}
    for r_, z in loc.items(): prof[r_] = prof.get(r_, 0) + z*T*L
    for r_, z in rem.items(): prof[r_] = prof.get(r_, 0) + z*T
    return root(prof, m, W)
def be(K, h, v, cst, f, e=4):
    def ok(R):
        H = int(f * R); c = price(K, h, v, cst, R - H, 5, H, e, 2); return c is not None and c >= REF[K]
    lo, hi = 0, 12000
    if not ok(1): return 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid): lo = mid
        else: hi = mid
    return lo
for nm, h, v, cst in (('E8', 8, 120, 72), ('P111', 8, 111, 63), ('I11', 11, 220, 110), ('I13', 13, 364, 156)):
    out = []
    for K in (4, 5):
        for f in (0, 0.25):
            r = be(K, h, v, cst, f); out.append('K%d f%.2f: %.2fv' % (K, f, r / v))
    print(nm, ' | '.join(out), flush=True)
