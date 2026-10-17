import numpy as np, itertools, pickle, sys, time
from bld import all_chambers, matinv
q=int(sys.argv[1]); n=4
C=all_chambers(n,q); N=len(C); A=np.array(C); Ainv=np.array([matinv(c,q) for c in C])
def detk(M):  # batched det of k x k (k<=4) mod q via cofactor
    k=M.shape[-1]
    if k==1: return M[...,0,0]
    if k==2: return M[...,0,0]*M[...,1,1]-M[...,0,1]*M[...,1,0]
    s=0
    for c in range(k):
        minor=np.delete(M[...,1:,:],c,axis=-1)
        s=s+((-1)**c)*M[...,0,c]*detk(minor)
    return s
def rank_batch(M):  # M: (N,r,c) mod q
    r,c=M.shape[1:]; rk=np.zeros(M.shape[0],dtype=np.int8)
    for t in range(1,min(r,c)+1):
        nz=np.zeros(M.shape[0],dtype=bool)
        for rows in itertools.combinations(range(r),t):
            for cols in itertools.combinations(range(c),t):
                sub=M[:,list(rows)][:,:,list(cols)]
                nz|=(detk(sub)%q)!=0
        rk[nz]=t
    return rk
perm_index={p:i for i,p in enumerate(itertools.permutations(range(n)))}
W=np.zeros((N,N),dtype=np.int16)
t0=time.time()
for a in range(N):
    M=np.einsum('ab,nbc->nac',A[a],Ainv)%q
    R=np.zeros((n+1,n+1,N),dtype=np.int8)
    for i in range(1,n+1):
        for j in range(n):
            R[i,j]=rank_batch(M[:,:i,j:])
    w=np.zeros((N,n),dtype=np.int8)
    for i in range(n):
        inc=(R[i+1,:n]-R[i,:n])==1   # (n_j, N)
        w[:,i]=np.max(np.where(inc,np.arange(n)[:,None],-1),axis=0)
    W[a]=[perm_index[tuple(x)] for x in w]
    if a%200==0: print(a,round(time.time()-t0,1),flush=True)
perms=list(perm_index)
def rl(p):
    seen=set(); cyc=0
    for i in range(n):
        if i in seen: continue
        cyc+=1; j=i
        while j not in seen: seen.add(j); j=p[j]
    return n-cyc
cost=np.array([rl(p) for p in perms],dtype=np.int8)[W]
wT=perm_index[(2,3,0,1)]
pickle.dump(dict(W=W,cost=cost,isWT=(W==wT),perms=perms),open('table_q%d.pkl'%q,'wb'))
print('done',time.time()-t0)
