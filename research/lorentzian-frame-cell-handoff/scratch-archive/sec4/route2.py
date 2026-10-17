"""Diagnostic for stage-0 routing: same structure as route.py but coverage is SOFT (maximise covered (t,s) pairs over
the 8 rep targets) and the per-cell / per-section counts may exceed |P| / |Q| with a penalty.  Modes:
  sym=1  Z15 orbit equality (as route.py);  sym=0 no symmetry (coverage over all 120 targets)
  slack=0 exact counts (route.py), slack=1 allow extras."""
import sys, collections, json
from common import *
from ortools.sat.python import cp_model
sym = int(sys.argv[1]); slack = int(sys.argv[2]); tl = float(sys.argv[3])
D4 = load_d4()
inner = {W: [P for P in planes if P & ~W == 0] for W in D4}
Wperp = {W: perpmask(W) for W in D4}
outer = {W: [Q for Q in planes if Q & ~Wperp[W] == 0] for W in D4}
useful = [W for W in D4 if inner[W] and outer[W]]
M = cp_model.CpModel()
yv = {}; zv = {}
for W in useful:
    for P in inner[W]: yv[(P, W)] = M.NewBoolVar('')
    for Q in outer[W]: zv[(W, Q)] = M.NewBoolVar('')
if sym:
    for (P, W), v in list(yv.items()): M.Add(v == yv[(act(P), act(W))])
    for (W, Q), v in list(zv.items()): M.Add(v == zv[(act(W), act(Q))])
ycnt = collections.defaultdict(list); zcnt = collections.defaultdict(list)
for (P, W), v in yv.items(): ycnt[P].append(v)
for (W, Q), v in zv.items(): zcnt[Q].append(v)
extra = []
for P in planes:
    if slack: e = M.NewIntVar(0, 6, ''); extra.append(e); M.Add(sum(ycnt[P]) == pc(P) + e)
    else: M.Add(sum(ycnt[P]) == pc(P))
for Q in planes:
    if slack: e = M.NewIntVar(0, 6, ''); extra.append(e); M.Add(sum(zcnt[Q]) == pc(Q) + e)
    else: M.Add(sum(zcnt[Q]) == pc(Q))
for W in useful:
    M.Add(sum(yv[(P, W)] for P in inner[W]) == sum(zv[(W, Q)] for Q in outer[W]))
tgts = reps if sym else list(range(V))
cov = []
for t in tgts:
    mine = [Q for Q in planes if Q >> t & 1]
    for s in e8.bits(e8.HYP[t]):
        terms = []
        for Q in mine:
            for W in useful:
                if (W, Q) not in zv or not (W >> s & 1): continue
                for P in inner[W]:
                    if P >> s & 1:
                        a = M.NewBoolVar(''); M.AddImplication(a, yv[(P, W)]); M.AddImplication(a, zv[(W, Q)])
                        terms.append(a)
        c = M.NewBoolVar(''); M.AddBoolOr(terms).OnlyEnforceIf(c); cov.append(c)
M.Maximize(100 * sum(cov) - (sum(extra) if extra else 0))
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M)
print('sym', sym, 'slack', slack, 'status', sol.StatusName(r), 'covered', sum(sol.Value(c) for c in cov), 'of', len(cov),
      'extras', sum(sol.Value(e) for e in extra) if extra else 0, 'bound', sol.BestObjectiveBound(), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    Y = [(hex(P), hex(W)) for (P, W), v in yv.items() if sol.Value(v)]
    Z = [(hex(W), hex(Q)) for (W, Q), v in zv.items() if sol.Value(v)]
    json.dump({'Y': Y, 'Z': Z}, open('routing_s%d_k%d.json' % (sym, slack), 'w'))
