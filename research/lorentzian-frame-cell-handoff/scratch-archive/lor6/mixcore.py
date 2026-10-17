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
