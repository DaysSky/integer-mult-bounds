exec(open('pen5gen.py').read().split("best=1e9")[0])
from ortools.sat.python import cp_model
m=cp_model.CpModel(); x=[m.NewBoolVar('') for _ in maxs]
for i in range(12):
    for j in range(12):
        if W[i,j]>0:
            m.Add(sum(x[k] for k,(S,Q) in enumerate(maxs) if j in S and i in Q)>=1)
m.Add(sum(x)==4)
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s): super().__init__(); s.sols=[]
    def on_solution_callback(s): s.sols.append([k for k in range(len(maxs)) if s.Value(x[k])])
sv=cp_model.CpSolver(); sv.parameters.enumerate_all_solutions=True; sv.parameters.max_time_in_seconds=600
cb=CB(); sv.Solve(m,cb); print('4-covers found',len(cb.sols),flush=True)
best=1e9
for sol in cb.sols:
    sh=[maxs[k] for k in sol]
    r=min(fit(sh,400) for _ in range(4))
    best=min(best,r)
    if r<1e-7: print('EXACT 4-term decomposition:',sh); break
print('best residual over all 4-covers',best)
