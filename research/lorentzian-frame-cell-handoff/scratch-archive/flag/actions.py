import numpy as np, pickle, sys, random
from bld import all_chambers, canon
q=int(sys.argv[1]); n=4
C=all_chambers(n,q); idx={canon(c,q).tobytes():i for i,c in enumerate(C)}
rng=np.random.default_rng(0); acts=[]
for k in range(200):
    h=np.eye(n,dtype=np.int64)
    for _ in range(12):
        E=np.eye(n,dtype=np.int64); i,j=rng.choice(n,2,replace=False); E[i,j]=rng.integers(1,q); h=(h@E)%q
    acts.append(np.array([idx[canon((c@h)%q,q).tobytes()] for c in C],dtype=np.int32))
pickle.dump(acts,open('acts_q%d.pkl'%q,'wb')); print('ok',len(acts))
