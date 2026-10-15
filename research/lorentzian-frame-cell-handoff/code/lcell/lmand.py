"""Mandatory-reader conflicts (fast valid check of the read pool): for each bottleneck cell C, M_C = intersection of
its minimal unserved sets (targets that MUST read C unless C gets an extra register).  A target lies in M_C for
several cells -> it can read only one of them.  Reports the conflict structure and the exact minimum number of cells
to drop (j) so that every target is mandatory for <= 1 kept cell (a lower bound on lexact's sum j)."""
import sys, os, json
os.environ['GRP'] = '11'
from lbase import *
from ortools.sat.python import cp_model
pc_ = lambda m: bin(m).count('1')
P = {}
def pm(m):
    if m not in P: P[m] = perp(m)
    return P[m]
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
co = {s: [C for C in cells if C >> s & 1] for s in range(V)}
mand = {}
for C in cells:
    s, a = list(bits(C)); os_ = 0; oa_ = 0
    for c in co[s]:
        if c != C: os_ |= pm(c)
    for c in co[a]:
        if c != C: oa_ |= pm(c)
    PC = pm(C); Fs = PC & ~os_; Fa = PC & ~oa_; D = Fs & Fa; S = Fs & ~Fa; A = Fa & ~Fs
    if not (D | S | A): continue
    nps = sorted(set(pm(closure(C | (1 << x))) for x in range(V) if not C >> x & 1))
    inter = None; zero = False
    for q1 in nps:
        for q2 in nps:
            for m in ((D & ~q1) | (S & ~(q1 | q2)) | (A & ~q1), (D & ~q1) | (S & ~q1) | (A & ~(q1 | q2)),
                      (D & ~(q1 & q2)) | (S & ~q1) | (A & ~q2)):
                if m == 0: zero = True; break
                inter = m if inter is None else inter & m
            if zero: break
        if zero: break
    if not zero: mand[C] = inter
by_t = {}
for C, m in mand.items():
    for t in bits(m): by_t.setdefault(t, []).append(C)
conf = {t: cs for t, cs in by_t.items() if len(cs) > 1}
print(sys.argv[1], 'bottleneck cells', len(mand), 'mandatory pairs', sum(pc_(m) for m in mand.values()),
      'targets mandatory for >1 cell', len(conf), 'max', max((len(c) for c in conf.values()), default=0), flush=True)
M = cp_model.CpModel(); keep = {C: M.NewBoolVar('') for C in mand}
for t, cs in conf.items(): M.Add(sum(keep[C] for C in cs) <= 1)
M.Maximize(sum(keep.values()))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 120; st = sv.Solve(M)
print('min cells needing a 3rd register from mandatory conflicts alone:', len(mand) - int(sv.ObjectiveValue()),
      sv.StatusName(st), flush=True)
