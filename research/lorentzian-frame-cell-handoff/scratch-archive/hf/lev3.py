from e8 import *
import itertools, sys, time
from collections import defaultdict
from ortools.sat.python import cp_model
Nsgn=np.sign(N).astype(int)
RD=[[t for t in range(V) if LEG[t,s]] for s in range(V)]
vecs=list(range(1,512))
# singles: S={s}, b=<p_s>+D (D dim 2 in p_s^perp, modulo p_s), Q = readers orth to D. keep maximal distinct sets
singles=[]
for s in range(V):
    ps=P[s]; perp=[x for x in vecs if dot(x,ps)==0]
    sets=set()
    for x,y in itertools.combinations(perp,2):
        if x^y==ps or x==ps or y==ps: continue
        Q=frozenset(t for t in RD[s] if dot(P[t],x)==0 and dot(P[t],y)==0)
        if len(Q)>=8: sets.add(Q)
    mx=[Q for Q in sets if not any(Q<R for R in sets)]
    singles+= [(s,Q) for Q in mx]
print('singles',len(singles),flush=True)
# pair blocks: S={s,s2}, b=<p_s,p_s2,x>, Q = common readers orth x with proportional rows (2 sign classes)
pairs=[]
for s,s2 in itertools.combinations(range(V),2):
    cr=[t for t in RD[s] if LEG[t,s2]]
    if len(cr)<6: continue
    base=basis([P[s],P[s2]])
    sets=set()
    for x in vecs:
        if x in span(base): continue
        if dot(x,P[s]) or dot(x,P[s2]): pass  # x need not be orth to S; b just must lie in Q-perp; require Q orth x
        for sg in (1,-1):
            Q=frozenset(t for t in cr if dot(P[t],x)==0 and Nsgn[t,s]*Nsgn[t,s2]==sg)
            if len(Q)>=5: sets.add(Q)
    mx=[Q for Q in sets if not any(Q<R for R in sets)]
    pairs+=[((s,s2),Q) for Q in mx]
print('pairs',len(pairs),flush=True)
import pickle; pickle.dump((singles,pairs),open('lev3cands.pkl','wb'))
