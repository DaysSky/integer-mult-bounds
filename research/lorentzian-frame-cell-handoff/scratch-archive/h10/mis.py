import numpy as np, sys
from ortools.sat.python import cp_model
Y=int(sys.argv[1]); TL=float(sys.argv[2])
V=np.load('pool_y%d.npy'%Y); A=np.load('adj_y%d.npy'%Y)
n=len(V)
m=cp_model.CpModel(); x=[m.NewBoolVar('x%d'%i) for i in range(n)]
iu,ju=np.nonzero(np.triu(~A,1))
for i,j in zip(iu,ju): m.AddBoolOr([x[i].Not(),x[j].Not()])
m.Maximize(sum(x))
s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=TL; s.parameters.num_workers=8
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s2): super().__init__()
    def on_solution_callback(s2): print('  sol',int(s2.ObjectiveValue()),'bound',int(s2.BestObjectiveBound()),'%.0fs'%s2.WallTime(),flush=True)
st=s.Solve(m,CB())
sel=[i for i in range(n) if s.Value(x[i])]
print('status',s.StatusName(st),'best',len(sel),'bound',s.BestObjectiveBound())
Vs=V[sel]; print('by y',{int(y):int((np.abs(Vs[:,-1])==y).sum()) for y in range(Y+1)})
np.save('best_y%d.npy'%Y,Vs)
