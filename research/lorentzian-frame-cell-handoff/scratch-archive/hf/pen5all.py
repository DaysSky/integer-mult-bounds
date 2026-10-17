exec(open('pen5gen.py').read().split("best=1e9")[0])
from ortools.sat.python import cp_model
m=cp_model.CpModel(); x=[m.NewBoolVar('') for _ in maxs]
for i in range(12):
    for j in range(12):
        if W[i,j]>0: m.Add(sum(x[k] for k,(S,Q) in enumerate(maxs) if j in S and i in Q)>=1)
m.Add(sum(x)==4)
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s): super().__init__(); s.sols=[]
    def on_solution_callback(s): s.sols.append([k for k in range(len(maxs)) if s.Value(x[k])])
sv=cp_model.CpSolver(); sv.parameters.enumerate_all_solutions=True; cb=CB(); sv.Solve(m,cb)
from collections import Counter
for sol in cb.sols:
    sh=[maxs[k] for k in sol]
    cov=np.zeros((12,12))
    for S,Q in sh: cov[np.ix_(list(Q),list(S))]+=1
    wc=Counter()
    for i in range(12):
        for j in range(12):
            if hid[L[i]]!=hid[L[j]] and cls[hid[L[i]]]==cls[hid[L[j]]] and cov[i,j]>0: wc[cls[hid[L[i]]]]+=1
    r=min(fit(sh,600) for _ in range(3))
    halves=[(sorted(set(hid[L[i]] for i in S)),sorted(set(hid[L[i]] for i in Q))) for S,Q in sh]
    print('exact' if r<1e-7 else 'inexact', round(r,8), 'within covered per class', dict(wc), halves)
