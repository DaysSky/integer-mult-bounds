"""Per-cell r_C (refined, free top) by cell type: inside a fully shared frame vs not, symmetric vs defect."""
import sys, os, json, collections
os.environ['GRP'] = '11'
from lbase import *
import lscore2 as L
for fn in sys.argv[1:]:
    cov = {int(k): v for k, v in json.load(open(fn)).items()}
    full = {a: all((cov[b] | (1 << b)) == (cov[a] | (1 << a)) for b in bits(cov[a])) for a in range(V)}
    cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
    cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
    stat = collections.Counter(); memo = {}
    for C in cells:
        s, a = list(bits(C))
        sym = (cov[s] >> a & 1) and (cov[a] >> s & 1)
        typ = ('sym' if sym else 'def', 'full' if (full[s] and full[a] and (cov[s] | 1 << s) == (cov[a] | 1 << a)) else 'mixed', ''.join(sorted(g.kind[x] for x in (s, a))))
        os_ = 0; oa_ = 0
        for c in cells_of[s]:
            if c != C: os_ |= L.perpm(c)
        for c in cells_of[a]:
            if c != C: oa_ |= L.perpm(c)
        PC = L.perpm(C); Fs = PC & ~os_; Fa = PC & ~oa_
        D = Fs & Fa; S = Fs & ~Fa; A = Fa & ~Fs
        nps = L.node_perps(C); best = None
        for q1 in nps:
            for q2 in nps:
                u1 = L.pc_(D & ~q1) + L.pc_(S & ~(q1 | q2)) + L.pc_(A & ~q1)
                u2 = L.pc_(D & ~q1) + L.pc_(S & ~q1) + L.pc_(A & ~(q1 | q2))
                u3 = L.pc_(D & ~(q1 & q2)) + L.pc_(S & ~q1) + L.pc_(A & ~q2)
                u = min(u1, u2, u3)
                if best is None or u < best: best = u
                if best == 0: break
            if best == 0: break
        stat[typ + ('r=%d' % best, 'D%d S%d A%d' % (L.pc_(D), L.pc_(S), L.pc_(A)))] += 1
    print(fn)
    for k, v in sorted(stat.items()): print('  ', k, v)
