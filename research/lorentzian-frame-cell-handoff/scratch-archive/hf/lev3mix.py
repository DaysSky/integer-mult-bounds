import pickle, sys
from e8 import *
from ortools.sat.python import cp_model
singles,pairs=pickle.load(open('lev3cands.pkl','rb'))
minpair=int(sys.argv[1]); minsing=int(sys.argv[2]); tl=float(sys.argv[3]); cap=int(sys.argv[4]) if len(sys.argv)>4 else None
P2=[(p,q) for p,q in pairs if len(q)>=minpair]
S1=[(s,q) for s,q in singles if len(q)>=minsing]
print('pairs',len(P2),'singles',len(S1),flush=True)
m=cp_model.CpModel()
x=[m.NewBoolVar('') for _ in P2]; y=[m.NewBoolVar('') for _ in S1]
pc={}; sc={}
for i,((s,s2),q) in enumerate(P2):
    for t in q: pc.setdefault((t,s),[]).append(x[i]); pc.setdefault((t,s2),[]).append(x[i])
for i,(s,q) in enumerate(S1):
    for t in q: sc.setdefault((t,s),[]).append(y[i])
for t in range(V):
    for s in range(V):
        if LEG[t,s]:
            P_=pc.get((t,s),[]); S_=sc.get((t,s),[])
            m.Add(sum(P_)+sum(S_)>=1)
            if S_: 
                z=m.NewBoolVar(''); m.AddMaxEquality(z,S_)
                m.Add(sum(P_)<=1+8*z)
            else: m.Add(sum(P_)<=1)
obj=sum(x)+sum(y)
if cap: m.Add(obj<=cap)
m.Minimize(obj)
sv=cp_model.CpSolver(); sv.parameters.max_time_in_seconds=tl; sv.parameters.num_workers=8; sv.parameters.log_search_progress=False
r=sv.Solve(m); print(sv.StatusName(r),'obj',sv.ObjectiveValue() if r in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None,'bound',sv.BestObjectiveBound(),flush=True)
if r in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    print('pairs',sum(sv.Value(v) for v in x),'singles',sum(sv.Value(v) for v in y))
    pickle.dump(([P2[i] for i in range(len(P2)) if sv.Value(x[i])],[S1[i] for i in range(len(S1)) if sv.Value(y[i])]),open(f'lev3mix_{minpair}_{minsing}.pkl','wb'))
