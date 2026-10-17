import pickle, random, sys, time
import numpy as np
d=pickle.load(open('e8f.pkl','rb')); comp=d['comp']; n=comp.shape[0]
nb=[0]*n
for i in range(n):
    m=0
    for j in np.nonzero(comp[i])[0]: m|=1<<int(j)
    nb[i]=m
def bits(x):
    out=[]
    while x:
        b=x&-x; out.append(b.bit_length()-1); x^=b
    return out
def greedy(seed_set, rng):
    C=list(seed_set); P=(1<<n)-1
    for c in C: P&=nb[c]
    while P:
        cand=bits(P)
        # pick vertex maximizing remaining candidates (sample)
        sample=rng.sample(cand,min(40,len(cand)))
        best=max(sample,key=lambda v:bin(P&nb[v]).count('1'))
        C.append(best); P&=nb[best]
    return C
rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 0)
best=[]; t0=time.time()
while time.time()-t0<float(sys.argv[2]) if len(sys.argv)>2 else 60:
    C=greedy([rng.randrange(n)],rng)
    # local search: drop k random, regrow
    for it in range(200):
        k=rng.randint(1,3)
        keep=rng.sample(C,max(1,len(C)-k))
        C2=greedy(keep,rng)
        if len(C2)>=len(C): C=C2
    if len(C)>len(best):
        best=C; print(len(best),round(time.time()-t0,1),flush=True)
pickle.dump(best,open('best_clique_%s.pkl'%(sys.argv[1] if len(sys.argv)>1 else 0),'wb'))
print('final',len(best))
