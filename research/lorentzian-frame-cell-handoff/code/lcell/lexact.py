"""EXACT read-assignment version of the refined free-top cell screen (tightens lscore_ind's pool counting).
For every cell C = {s,a} (2 registers): each stream pattern (s+a,s) / (s+a,a) / (s,a) and each pair of rank-3
closure nodes (N1,N2) (all closures, degenerate included) leaves a set U of forced targets unserved; each target
in U must read C in-chain, and a target has ONE rank-2 in-chain read.  Variables: per cell either one minimal
option U (its targets all read C) or an extra register (j_C = 1, treated as resolving the cell: relaxation).
Constraint: every target reads <= 1 cell.  min sum j_C  ->  R >= 440 + defects + sum j_C for THIS system
(valid relaxation: per-cell options are independent except through the reads).
usage: lexact.py SYSTEM.json [timelimit]"""
import sys, os, json
os.environ['GRP'] = '11'
from lbase import *
from ortools.sat.python import cp_model
pc_ = lambda m: bin(m).count('1')
P = {}
def pm(m):
    if m not in P: P[m] = perp(m)
    return P[m]
fn = sys.argv[1]; tl = float(sys.argv[2]) if len(sys.argv) > 2 else 600
cov = {int(k): v for k, v in json.load(open(fn)).items()}
defects = sum(1 for a in range(V) for b in bits(cov[a]) if not cov[b] >> a & 1)
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
co = {s: [C for C in cells if C >> s & 1] for s in range(V)}
opts = {}; free = 0; rmin = {}
for C in cells:
    s, a = list(bits(C)); os_ = 0; oa_ = 0
    for c in co[s]:
        if c != C: os_ |= pm(c)
    for c in co[a]:
        if c != C: oa_ |= pm(c)
    PC = pm(C); Fs = PC & ~os_; Fa = PC & ~oa_; D = Fs & Fa; S = Fs & ~Fa; A = Fa & ~Fs
    if not (D | S | A): free += 1; continue
    nps = sorted(set(pm(closure(C | (1 << x))) for x in range(V) if not C >> x & 1))
    ms = set()
    for q1 in nps:
        for q2 in nps:
            ms.add((D & ~q1) | (S & ~(q1 | q2)) | (A & ~q1))
            ms.add((D & ~q1) | (S & ~q1) | (A & ~(q1 | q2)))
            ms.add((D & ~(q1 & q2)) | (S & ~q1) | (A & ~q2))
    if 0 in ms: free += 1; continue
    ms = sorted(ms, key=pc_); keep = []
    for m in ms:
        if not any(k & m == k for k in keep): keep.append(m)
    opts[C] = keep; rmin[C] = pc_(keep[0])
print(fn, 'cells', len(cells), 'free', free, 'bottleneck cells', len(opts), 'defects', defects,
      'sum r_min', sum(rmin.values()), 'options', sum(len(v) for v in opts.values()), flush=True)
if os.environ.get('J0') == '1':   # j = 0 feasibility only: disjoint options => size <= r_min + slack
    slack = V - sum(rmin.values()); print('J0 test, slack', slack, flush=True)
    opts = {C: [m for m in ks if pc_(m) <= rmin[C] + slack] for C, ks in opts.items()}
    print('reduced options', sum(len(v) for v in opts.values()), flush=True)
M = cp_model.CpModel(); J = {}; Y = {}; reads = {t: [] for t in range(V)}
for C, ks in opts.items():
    J[C] = M.NewBoolVar(''); ys = []
    for i, m in enumerate(ks):
        y = M.NewBoolVar(''); Y[C, i] = y; ys.append(y)
        for t in bits(m): reads[t].append(y)
    M.Add(sum(ys) + J[C] == 1)
for t, lst in reads.items():
    if len(lst) > 1: M.Add(sum(lst) <= 1)
M.Add(sum(pc_(opts[C][i]) * y for (C, i), y in Y.items()) <= V)   # redundant knapsack cut (disjoint reads)
M.Minimize(sum(J.values()))
if os.environ.get('J0') == '1': M.Add(sum(J.values()) == 0)
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = tl; sv.parameters.num_workers = 2
st = sv.Solve(M)
print('status', sv.StatusName(st), 'sum_j', sv.ObjectiveValue(), 'bound', sv.BestObjectiveBound(),
      '-> R_lb_exact >=', 440 + defects + int(sv.BestObjectiveBound() + 0.999), '(incumbent', 440 + defects + int(sv.ObjectiveValue()), ')', flush=True)
