import pickle, sys
from e8 import *
from ortools.sat.python import cp_model
singles,pairs=pickle.load(open('lev3cands.pkl','rb'))
minpair=int(sys.argv[1]); minsing=int(sys.argv[2]); tl=float(sys.argv[3])
P2=[(p,q) for p,q in pairs if len(q)>=minpair]
S1=[(s,q) for s,q in singles if len(q)>=minsing]
print('pairs',len(P2),'singles',len(S1),flush=True)
m=cp_model.CpModel()
x=[m.NewBoolVar('') for _ in P2]; y=[m.NewBoolVar('') for _ in S1]
cov={}
for i,((s,s2),q) in enumerate(P2):
    for t in q: cov.setdefault((t,s),[]).append(x[i]); cov.setdefault((t,s2),[]).append(x[i])
for i,(s,q) in enumerate(S1):
    for t in q: cov.setdefault((t,s),[]).append(y[i])
miss=0
for t in range(V):
    for s in range(V):
        if LEG[t,s]:
            terms=cov.get((t,s),[])
            if not terms: miss+=1; continue
            m.Add(sum(terms)==1)
print('uncoverable entries',miss,flush=True)
m.Minimize(sum(x)+sum(y))
sv=cp_model.CpSolver(); sv.parameters.max_time_in_seconds=tl; sv.parameters.num_workers=8
r=sv.Solve(m); print(sv.StatusName(r), 'obj', sv.ObjectiveValue() if r in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None, 'bound', sv.BestObjectiveBound(),flush=True)
if r in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    np_=sum(sv.Value(v) for v in x); ns=sum(sv.Value(v) for v in y); print('pairs used',np_,'singles used',ns)
    sol=([P2[i] for i in range(len(P2)) if sv.Value(x[i])],[S1[i] for i in range(len(S1)) if sv.Value(y[i])])
    pickle.dump(sol,open(f'lev3sol_{minpair}_{minsing}.pkl','wb'))
