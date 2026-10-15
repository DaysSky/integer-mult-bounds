"""Independent (no cross-cell memo) refined free-top scorer for ANY system (symmetric or not).
Optionally NOREADS=1.  Recomputes every cell from scratch with all closure nodes."""
import sys, os, json
os.environ['GRP'] = '11'
from lbase import *
pc_ = lambda m: bin(m).count('1')
P = {}
def pm(m):
    if m not in P: P[m] = perp(m)
    return P[m]
for fn in sys.argv[1:]:
    cov = {int(k): v for k, v in json.load(open(fn)).items()}
    defects = sum(1 for a in range(V) for b in bits(cov[a]) if not cov[b] >> a & 1)
    cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
    co = {s: [C for C in cells if C >> s & 1] for s in range(V)}
    rs = []
    for C in cells:
        s, a = list(bits(C)); os_ = 0; oa_ = 0
        for c in co[s]:
            if c != C: os_ |= pm(c)
        for c in co[a]:
            if c != C: oa_ |= pm(c)
        PC = pm(C); Fs = PC & ~os_; Fa = PC & ~oa_; D = Fs & Fa; S = Fs & ~Fa; A = Fa & ~Fs
        if not (D | S | A): rs.append(0); continue
        nps = list(set(pm(closure(C | (1 << x))) for x in range(V) if not C >> x & 1))
        best = None
        for q1 in nps:
            for q2 in nps:
                u = min(pc_(D & ~q1) + pc_(S & ~(q1 | q2)) + pc_(A & ~q1), pc_(D & ~q1) + pc_(S & ~q1) + pc_(A & ~(q1 | q2)),
                        pc_(D & ~(q1 & q2)) + pc_(S & ~q1) + pc_(A & ~q2))
                if best is None or u < best: best = u
                if best == 0: break
            if best == 0: break
        rs.append(best)
    free0 = sum(1 for r in rs if r == 0); pool = 0 if os.environ.get('NOREADS') == '1' else V; cnt = 0
    for r in sorted(r for r in rs if r > 0):
        if pool >= r: pool -= r; cnt += 1
    j = len(cells) - free0 - cnt
    print(fn, 'cells', len(cells), 'defects', defects, 'reader demand', sum(rs), 'sum_j', j, 'R_lb', 440 + defects + j,
          ' (no-read R_lb', 440 + defects + sum(1 for r in rs if r > 0), ')', flush=True)
