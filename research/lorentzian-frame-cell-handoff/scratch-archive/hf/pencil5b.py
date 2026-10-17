from pencil5 import *
import sys
dS,dQ=4,4
B=blocks(dS,dQ)
for target in [4,5]:
    m=cp_model.CpModel(); x=[m.NewBoolVar('') for _ in B]
    cover={}
    for b,(S,Q) in enumerate(B):
        for t in Q:
            for s in S: cover.setdefault((t,s),[]).append(b)
    for t in L:
        for s in L:
            if t==s or hid[t]==hid[s]: continue
            terms=[x[b] for b in cover.get((t,s),[])]
            if cls[hid[t]]!=cls[hid[s]]: m.Add(sum(terms)==1)
            else: m.Add(sum(terms)<=1)
    m.Add(sum(x)<=target)
    sv=cp_model.CpSolver(); sv.parameters.max_time_in_seconds=600; sv.parameters.num_workers=8
    r=sv.Solve(m); print('level5 blocks<=',target,':',sv.StatusName(r),flush=True)
    if sv.StatusName(r) in ('FEASIBLE','OPTIMAL'):
        for b in range(len(B)):
            if sv.Value(x[b]): S,Q=B[b]; print('   S',S,'Q',Q)
        break
