from e8 import *
import itertools, sys
from ortools.sat.python import cp_model
key=next(iter(PEN)); H=halves_of(key); L=[x for h in H for x in h]
hid={t:a for a,h in enumerate(H) for t in h}
cls={}  # class of half: same tetrad
for a,h in enumerate(H): cls[a]=TET[h[0]]
def spanok(lines,d): return len(basis([P[x] for x in lines]))<=d
def blocks(dS,dQ):
    out=[]
    opts=[]  # per half: (S-part, Q-part)
    for a,(x,y) in enumerate(H):
        o=[((),())]+[(s,()) for s in [(x,),(y,),(x,y)]]+[((),q) for q in [(x,),(y,),(x,y)]]
        opts.append(o)
    for combo in itertools.product(*opts):
        S=[x for s,q in combo for x in s]; Q=[x for s,q in combo for x in q]
        if not S or not Q: continue
        if spanok(S,dS) and spanok(Q,dQ): out.append((tuple(S),tuple(Q)))
    return out
def solve(dS,dQ,tl=120):
    B=blocks(dS,dQ)
    m=cp_model.CpModel(); x=[m.NewBoolVar('') for _ in B]
    cover={}
    for b,(S,Q) in enumerate(B):
        for t in Q:
            for s in S: cover.setdefault((t,s),[]).append(b)
    within=[]
    for t in L:
        for s in L:
            if t==s or hid[t]==hid[s]: continue
            terms=[x[b] for b in cover.get((t,s),[])]
            if cls[hid[t]]!=cls[hid[s]]: m.Add(sum(terms)==1)
            else:
                m.Add(sum(terms)<=1); within.append(sum(terms))
    m.Minimize(sum(x)*1000 - sum(within))
    sv=cp_model.CpSolver(); sv.parameters.max_time_in_seconds=tl; sv.parameters.num_workers=8
    r=sv.Solve(m)
    ch=[B[b] for b in range(len(B)) if sv.Value(x[b])]
    w=sum(sv.Value(e) for e in within)
    return sv.StatusName(r), len(B), len(ch), w, ch
if __name__=="__main__":
    for lev,(dS,dQ) in {5:(4,4),4:(3,5),6:(5,3),3:(2,6)}.items():
       st,nb,k,w,ch=solve(dS,dQ)
       print(f'level {lev}: status {st} candidates {nb} min blocks {k} within-covered {w}/24 ', flush=True)
       for S,Q in ch: print('   S halves',sorted(set(hid[s] for s in S)),len(S),' Q halves',sorted(set(hid[t] for t in Q)),len(Q))
