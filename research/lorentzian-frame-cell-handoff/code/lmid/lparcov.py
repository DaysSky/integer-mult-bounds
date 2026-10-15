"""Parity covers of R(t) by ROUTABLE section totals: find the fewest plane sections S_i (planes through t) with
sum_i 1[rt(S_i)] = 1[R(t)] over F2 (every line of R(t) in an odd number of the rt(S_i)).  Then every section's content
is its full routable total -- identical for all users of the section (shareable, free in-chain reads).
usage: lparcov.py SYSTEM.json [ntargets]"""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lw import V, g, bits, closure, FULL
from ortools.sat.python import cp_model
HYP = g.HYP
pc = lambda m: bin(m).count('1')
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
NT = int(sys.argv[2]) if len(sys.argv) > 2 else V
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
def pm(m):
    r = FULL
    for s in bits(m): r &= HYP[s]
    return r
def rt(S):
    r = 0
    for u in bits(S):
        if any(C & ~S == 0 for C in cells_of[u]): r |= 1 << u
    return r
res = collections.Counter(); out = {}
for t in range(NT):
    planes = sorted(set(closure((1 << t) | (1 << e)) for e in range(V) if e != t))
    secs = [pm(Q) for Q in planes]; rts = [rt(S) for S in secs]
    M = cp_model.CpModel(); x = [M.NewBoolVar('') for _ in secs]
    for u in bits(HYP[t]):
        terms = [x[i] for i in range(len(secs)) if rts[i] >> u & 1]
        M.AddBoolXOr(terms + [M.NewConstant(0)])      # XOR of terms == 1  (BoolXOr enforces odd parity)
    M.Minimize(sum(x)); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 60; sv.parameters.num_workers = 4
    st = sv.Solve(M)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        k = int(sv.ObjectiveValue()); chosen = [hex(secs[i]) for i in range(len(secs)) if sv.Value(x[i])]
        out[t] = chosen
    else: k = None
    res[(g.kind[t], k, sv.StatusName(st))] += 1
    print(t, g.kind[t], 'min parity cover', k, sv.StatusName(st), 'bound', sv.BestObjectiveBound(), flush=True)
print(sorted(res.items(), key=str))
json.dump(out, open('lparcov_%s.json' % os.path.basename(sys.argv[1]).split('.')[0], 'w'))
