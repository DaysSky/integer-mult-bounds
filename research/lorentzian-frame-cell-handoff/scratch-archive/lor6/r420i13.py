"""Price an R420-analogue on I_{13,1} (v 364, h 13, 13 totals at rank 12): per-role chains scaled from R420.
R420 roles (E8): sources line->cell->D4->D6->t-perp->full {1:3,2:2}; targets 0->cell->t-perp {2:1,5:1};
helpers {1:960,2:1080,4:60}/420.  I13: sources {1:3,2:1,7:1}; targets {2:1,10:1}; helpers per helper
{1:2.286,2:1.571,4:0.143,7:1}.  Variants: a fraction of helpers entrance-ranked (start at their first frame, rank e)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/lor6')
import i13ent as Q
from mpmath import mp
import bisect
from pricer import idle_slots, root
h, v, cst = 13, 364, 156
K, T, L = 4, 32, 9
def price(R, n_ent=0, e=2):
    a = h - 1; m = 1 + L*a; W = 2*K*v*T
    loc = {}
    def add(r, z):
        if z: loc[r] = loc.get(r, 0) + z
    add(1, 3*v); add(2, 1*v); add(7, 1*v)               # sources
    add(2, v); add(10, v)                                # targets
    n0 = R - n_ent
    add(1, round(2.286*n0)); add(2, round(1.571*n0)); add(4, round(0.143*n0)); add(7, n0)
    # entrance-ranked helpers: drop their first climb(s) worth e units: assume they start at rank e (drop e rank-1/2 children)
    if n_ent:
        # their chain: e -> 4 -> 11 -> 12 -> 13 approx: climbs (4-e), 7, 1, 1
        add(4 - e, n_ent) if e < 4 else None
        add(7, n_ent); add(1, 2*n_ent)
    q, r = divmod(cst, 12); add(12, q); add(r, 1 if r else 0)
    free = sorted(c for c in idle_slots(K, a) for _ in range(2*v))
    res = sorted([h]*(n0*L) + [h - e]*(n_ent*L), reverse=True)
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
for R in (1092, 1150, 1200, 1274):
    c = price(R)
    print('R=%d frame-0: %s' % (R, ('%+.2f%%' % float((c / Q.P111 - 1)*100)) if c else 'wall'), flush=True)
for n_ent, e in ((546, 2), (546, 4), (910, 2), (910, 4)):
    c = price(1274, n_ent, e)
    print('R=1274 with %d helpers entering at rank %d: %s' % (n_ent, e, ('%+.2f%%' % float((c / Q.P111 - 1)*100)) if c else 'wall'), flush=True)
