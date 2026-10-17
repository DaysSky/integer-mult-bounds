exec(open('pen5pair.py').read().split("random.seed(2)")[0])
from ortools.sat.python import cp_model
from collections import defaultdict
bySet=defaultdict(list)
for i,(S,Q) in enumerate(shapes): bySet[S].append(i)
for n in (4,5,6):
    m=cp_model.CpModel(); x=[m.NewIntVar(0,2,'') for _ in shapes]
    for q in halves:
        for s in halves:
            if W[q,s]>0: m.Add(sum(x[i] for i,(S,Q) in enumerate(shapes) if s in S and q in Q)>=1)
    for S,ids in bySet.items():
        if len(S)==3:
            used=m.NewBoolVar(''); tot=sum(x[i] for i in ids)
            m.Add(tot>=2).OnlyEnforceIf(used); m.Add(tot==0).OnlyEnforceIf(used.Not())
    m.Add(sum(x)==n)
    class CB(cp_model.CpSolverSolutionCallback):
        def __init__(s): super().__init__(); s.sols=[]
        def on_solution_callback(s):
            sol=[]
            for i in range(len(shapes)):
                sol+= [shapes[i]]*s.Value(x[i])
            s.sols.append(sol)
            if len(s.sols)>=400: s.StopSearch()
    sv=cp_model.CpSolver(); sv.parameters.enumerate_all_solutions=True; sv.parameters.max_time_in_seconds=120
    cb=CB(); sv.Solve(m,cb)
    print('n',n,'covering paired multisets (cap 400):',len(cb.sols),flush=True)
    best=1e9
    for sol in cb.sols:
        r=fit(sol,400,3); best=min(best,r)
        if r<1e-7: print('  EXACT',sol,flush=True); break
    print('  best residual',best,flush=True)
