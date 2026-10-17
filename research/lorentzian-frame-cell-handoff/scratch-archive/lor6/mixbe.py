"""Mixed population break-even for I_{11,1}: C frame-0 helpers (carriers/proxies; chain 0 -> 11 in kc steps, width 11)
plus H entrance-ranked hubs (enter at rank e, climb to 11 in kh steps, width 11 - e).  Sources ks=2, targets kt=3,
11 copies of rank 10.  Uses pricer.price with per-helper widths via a mixed hosting (greedy by width)."""
import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer
from pricer import idle_slots, root
from mpmath import mp, mpf
P111 = mp.mpf('0.001733427039589844')
v, h, cst, K, T = 220, 11, 110, 4, 32
L = 2*K + 1; a = h - 1; m = 1 + L*a; W = 2*K*v*T
def split(total, k):
    b, r = divmod(total, k); return [b + 1]*r + [b]*(k - r)
def local(C, kc, H, e, kh, ks=2, kt=3):
    Hs = {}
    def add(r, z):
        if z: Hs[r] = Hs.get(r, 0) + z
    for p in split(10, ks): add(p, v)
    for p in split(10, kt): add(p, v)
    for p in split(11, kc): add(p, C)
    for p in split(11 - e, kh): add(p, H)
    add(10, 11)
    return Hs
def price_mixed(loc, widths):
    """widths: list of (width, count) residuals per replica (each helper hosted once per stage: count*L residuals).
    Hosting: greedy best-fit, wide residuals first, into idle slots; leftover slot capacity becomes paid children;
    unhosted residuals -> no root (hosting wall)."""
    slots = []
    for c in idle_slots(K, a):
        slots += [c] * (2 * v)
    slots.sort(reverse=True)
    free = slots[:]
    res = []
    for w, cnt in sorted(widths, reverse=True): res += [w] * (cnt * L)
    import heapq
    # best-fit decreasing using a sorted list of free capacities
    import bisect
    free.sort()
    for w in res:
        i = bisect.bisect_left(free, w)
        if i == len(free): return None
        c = free.pop(i)
        if c - w > 0: bisect.insort(free, c - w)
    rem = {}
    for c in free: rem[c] = rem.get(c, 0) + 1
    prof = {}
    for r, z in loc.items(): prof[r] = prof.get(r, 0) + z * T * L
    for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
    return root(prof, m, W)
def ok(C, kc, H, e, kh):
    c = price_mixed(local(C, kc, H, e, kh), [(11, C), (11 - e, H)])
    return c is not None and c >= P111
# calibration: pure frame-0 population against pricer.price
if __name__ == "__main__": c1 = price_mixed(local(700, 3, 0, 0, 1), [(11, 700)])
if __name__ == "__main__": c2, _, _ = pricer.price(local(700, 3, 0, 0, 1), v, h, 700)
if __name__ == "__main__": print("calibration C=700 kc=3: bestfit %s vs pricer %s' % (mp.nstr(c1, 10) if c1 else None, mp.nstr(c2, 10) if c2 else None))
if __name__ == "__main__":
  pass
for kc in ([] if __name__ != "__main__" else (3, 4)):
    for C in (426, 500, 600):
        row = []
        for e, kh in ((5, 1), (5, 2), (7, 1), (7, 2), (9, 1)):
            if not ok(C, kc, 0, e, kh): row.append('C alone fails'); continue
            lo, hi = 0, 4000
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if ok(C, kc, mid, e, kh): lo = mid
                else: hi = mid
            row.append('e%d/k%d: H<=%d' % (e, kh, lo))
        print('C=%d (kc=%d):' % (C, kc), ' | '.join(row), flush=True)

if __name__ == "__main__": print("--- long carrier chains: sources ks, targets kt, carriers C=440 (kc), nodes e/kh')
for ks, kt, kc in ([] if __name__ != "__main__" else ((3, 2, 5), (4, 2, 5), (4, 2, 6), (5, 3, 6))):
    row = []
    for e, kh in ((5, 1), (6, 1), (7, 1), (8, 1), (9, 1)):
        def okk(H):
            c = price_mixed(local(440, kc, H, e, kh, ks=ks, kt=kt), [(11, 440), (11 - e, H)])
            return c is not None and c >= P111
        if not okk(0): row.append('C fails'); continue
        lo, hi = 0, 5000
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if okk(mid): lo = mid
            else: hi = mid
        row.append('e%d: H<=%d' % (e, lo))
    print('ks=%d kt=%d kc=%d:' % (ks, kt, kc), ' | '.join(row), flush=True)
