"""Refined per-cell screen (free top) including SINGLY forced targets: a 2-register cell C={s,a} emits 2 streams with
contents (s+a, s), (s+a, a) or (s, a) to nodes N1, N2 (nondegenerate rank-3 closures).  Target groups: D (doubly
forced: needs s and a via C), S (needs s via C only), A (needs a via C only).  A node serves t iff N ⊂ t-perp.
r_C = min over configurations of #forced targets left unserved (they must read C in-chain).  Counting with <= 220
readers -> sum j_C lower bound.  R_lb = 440 + defects + sum_j_lb."""
import sys, os, json
os.environ['GRP'] = '11'
from lbase import *
PERP = {}
def perpm(m):
    if m not in PERP: PERP[m] = perp(m)
    return PERP[m]
pc_ = lambda m: bin(m).count('1')
def node_perps(C):
    ps = set()
    for x in range(V):
        if C >> x & 1: continue
        N = closure(C | (1 << x))
        ps.add(perpm(N))   # degenerate closures kept: a general nondegenerate frame F ⊋ C has line span ⊇ some closure(C+x), so served(F) ⊂ served(closure) (relaxation)
    return list(ps)
def score2(cov):
    defects = sum(1 for a in range(V) for b in bits(cov[a]) if not cov[b] >> a & 1)
    cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
    cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
    rs = []; memo = {}
    for C in cells:
        key = min(act(C, p) for p in PERMS)
        if key in memo: rs.append(memo[key]); continue
        s, a = list(bits(C))
        os_ = 0; oa_ = 0
        for c in cells_of[s]:
            if c != C: os_ |= perpm(c)
        for c in cells_of[a]:
            if c != C: oa_ |= perpm(c)
        PC = perpm(C)
        Fs = PC & ~os_          # targets for which s can come only via C
        Fa = PC & ~oa_
        D = Fs & Fa; S = Fs & ~Fa; A = Fa & ~Fs
        nps = node_perps(C)
        best = None
        for q1 in nps:
            # sum stream at q1 serves D,S,A within q1; second stream single s or a at q2
            d1 = D & q1; s1 = S & q1; a1 = A & q1
            for q2 in nps:
                # (sum@q1, s@q2): D served by q1 only; S by q1|q2; A by q1
                u1 = pc_(D & ~q1) + pc_(S & ~(q1 | q2)) + pc_(A & ~q1)
                u2 = pc_(D & ~q1) + pc_(S & ~q1) + pc_(A & ~(q1 | q2))
                # (s@q1, a@q2): D needs both; S by q1; A by q2
                u3 = pc_(D & ~(q1 & q2)) + pc_(S & ~q1) + pc_(A & ~q2)
                u = min(u1, u2, u3)
                if best is None or u < best: best = u
                if best == 0: break
            if best == 0: break
        if best is None: best = pc_(D | S | A)
        memo[key] = best; rs.append(best)
    free0 = sum(1 for r in rs if r == 0); pool = V; cnt = 0
    for r in sorted(r for r in rs if r > 0):
        if pool >= r: pool -= r; cnt += 1
    jlb = len(cells) - free0 - cnt
    return 440 + defects + jlb, defects, jlb
if __name__ == '__main__':
    for fn in sys.argv[1:]:
        cov = {int(k): v for k, v in json.load(open(fn)).items()}
        print(fn, 'R_lb2, defects, sum_j_lb2 =', score2(cov), flush=True)
