"""First-frame layer (reach lemma) for a union in-chain frame design.  Every cell {u,f} (f in M(u); 2 registers if
reciprocal, else 1) sends each register to ONE first frame F = span(u, f, y) of rank 3; a line u in the part A_S of
section S = {t,e}-perp can only be delivered if some cell {u,f} inside S has a chosen frame inside S (y _|_ t, e).
CP-SAT: choose y's per cell (<= #registers) to maximise covered (section, line) incidences.
usage: lframe1.py system.json parts.json [timelimit]"""
import sys, json, collections, time
import numpy as np
from lgeo import *
from ortools.sat.python import cp_model
sysm = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
parts = {tuple(int(x) for x in k.split(',')): int(v, 16) for k, v in json.load(open(sys.argv[2])).items()}
TL = float(sys.argv[3]) if len(sys.argv) > 3 else 300
M = {s: [x for x in bits(sysm[s]) if x != s] for s in range(V)}
O = (np.array(G) == 0); np.fill_diagonal(O, False)
cells = {}
for u in range(V):
    for f in M[u]:
        c = (min(u, f), max(u, f))
        cells[c] = cells.get(c, 0) + 1          # registers: one per line using the cell
# candidate y for cell c: rank-3 span with nondegenerate frame (skip y in cell); use all other lines (rank check)
def cand_y(c):
    u, f = c
    return [y for y in range(V) if y not in c and rank((1 << u) | (1 << f) | (1 << y)) == 3]
M_ = cp_model.CpModel()
z = {}
for c, nreg in cells.items():
    ys = cand_y(c)
    for y in ys: z[(c, y)] = M_.NewBoolVar('')
    M_.Add(sum(z[(c, y)] for y in ys) <= nreg)
cov = []; ninc = 0; nopt0 = 0
for (t, e), A in parts.items():
    for u in bits(A):
        ninc += 1
        lits = []
        for f in M[u]:
            if not (O[f, t] and O[f, e]): continue
            c = (min(u, f), max(u, f))
            lits += [z[(c, y)] for y in range(V) if (c, y) in z and O[y, t] and O[y, e]]
        if not lits: nopt0 += 1; continue
        w = M_.NewBoolVar(''); M_.AddBoolOr(lits).OnlyEnforceIf(w); cov.append(w)
print('incidences', ninc, 'with no candidate at all', nopt0, 'cells', len(cells), 'vars', len(z), flush=True)
M_.Maximize(sum(cov))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 2
st = sv.Solve(M_)
print('status', sv.StatusName(st), 'covered', int(sv.ObjectiveValue()), 'of', ninc, 'bound', int(sv.BestObjectiveBound()), flush=True)
