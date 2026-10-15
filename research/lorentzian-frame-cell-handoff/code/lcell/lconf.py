"""Pairwise read conflicts: cells C, C' conflict if EVERY minimal unserved set of C meets EVERY minimal unserved set
of C' (so both cannot be relieved by in-chain reads, each target having one read).  The minimum vertex cover of the
conflict graph is a lower bound on sum j_C (a cover-free pair would both read-relieve).  Prints certificates.
usage: lconf.py SYSTEM.json"""
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
opts = {}
for C in cells:
    s, a = list(bits(C)); os_ = 0; oa_ = 0
    for c in co[s]:
        if c != C: os_ |= pm(c)
    for c in co[a]:
        if c != C: oa_ |= pm(c)
    PC = pm(C); Fs = PC & ~os_; Fa = PC & ~oa_; D = Fs & Fa; S = Fs & ~Fa; A = Fa & ~Fs
    if not (D | S | A): continue
    nps = sorted(set(pm(closure(C | (1 << x))) for x in range(V) if not C >> x & 1))
    ms = set()
    for q1 in nps:
        for q2 in nps:
            ms.add((D & ~q1) | (S & ~(q1 | q2)) | (A & ~q1))
            ms.add((D & ~q1) | (S & ~q1) | (A & ~(q1 | q2)))
            ms.add((D & ~(q1 & q2)) | (S & ~q1) | (A & ~q2))
    if 0 in ms: continue
    ms = sorted(ms, key=pc_); keep = []
    for m in ms:
        if not any(k & m == k for k in keep): keep.append(m)
    opts[C] = keep
cl = list(opts); edges = []
for i in range(len(cl)):
    for j in range(i + 1, len(cl)):
        A_, B_ = opts[cl[i]], opts[cl[j]]
        ua = 0
        for m in A_: ua |= m
        ub = 0
        for m in B_: ub |= m
        if not ua & ub: continue
        if all(all(a & b for b in B_) for a in A_): edges.append((cl[i], cl[j]))
print(sys.argv[1], 'bottleneck cells', len(cl), 'conflict pairs', len(edges), flush=True)
for C, D_ in edges[:5]:
    print('  certificate:', sorted(bits(C)), 'opts', [sorted(bits(m)) for m in opts[C]][:6], '| vs', sorted(bits(D_)),
          'opts', [sorted(bits(m)) for m in opts[D_]][:6], flush=True)
M = cp_model.CpModel(); x = {C: M.NewBoolVar('') for C in cl}
for C, D_ in edges: M.AddBoolOr([x[C], x[D_]])
M.Minimize(sum(x.values())); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 60; st = sv.Solve(M)
print('min vertex cover of pairwise conflicts (lower bound on sum j):', int(sv.ObjectiveValue()), sv.StatusName(st), flush=True)
