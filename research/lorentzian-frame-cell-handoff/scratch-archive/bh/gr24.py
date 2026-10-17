import numpy as np, itertools, random, math, pickle, sys
q=int(sys.argv[1])
# points of Gr(2,4)(F_q) as RREF 2x4
def rref(M):
    M=M.copy()%q; r=0; piv=[]
    for c in range(4):
        p=next((i for i in range(r,2) if M[i,c]),None)
        if p is None: continue
        M[[r,p]]=M[[p,r]]; M[r]=(M[r]*pow(int(M[r,c]),q-2,q))%q
        for i in range(2):
            if i!=r and M[i,c]: M[i]=(M[i]-M[i,c]*M[r])%q
        r+=1
        if r==2: break
    return M if r==2 else None
pts={}
for v in itertools.product(range(q),repeat=8):
    M=rref(np.array(v).reshape(2,4))
    if M is not None: pts[M.tobytes()]=M
P=list(pts.values()); N=len(P); print('Gr(2,4) points',N)
def rank(A):
    A=A.copy()%q; r=0
    for c in range(A.shape[1]):
        p=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if p is None: continue
        A[[r,p]]=A[[p,r]]; A[r]=(A[r]*pow(int(A[r,c]),q-2,q))%q
        for i in range(A.shape[0]):
            if i!=r and A[i,c]: A[i]=(A[i]-A[i,c]*A[r])%q
        r+=1
    return r
D=np.zeros((N,N),dtype=np.int32)
for i in range(N):
    for j in range(N): D[i,j]=rank(np.vstack([P[i],P[j]]))-2   # Grassmann distance
g=pickle.load(open('bh.pkl','rb')); E=g['phys']; S=g['sessions']; V=182
nb=[[] for _ in range(V)]; sv=[[] for _ in range(V)]
for u,v in E: nb[u].append(v); nb[v].append(u)
for s,t in S: sv[s].append(t); sv[t].append(s)
best_all=None
for seed in range(int(sys.argv[2])):
    rng=random.Random(seed); lab=[rng.randrange(N) for _ in range(V)]
    e=sum(D[lab[u],lab[v]] for u,v in E); viol=sum(D[lab[s],lab[t]]!=2 for s,t in S)
    Pn=2.0; Tm=2.0; best=None
    for it in range(int(float(sys.argv[3]))):
        v=rng.randrange(V); r=rng.random()
        if r<0.6: new=lab[rng.choice(nb[v])]
        elif r<0.8 and sv[v]:
            w=rng.choice(sv[v]); c=np.nonzero(D[lab[w]]==2)[0]; new=int(rng.choice(list(c)))
        else: new=rng.randrange(N)
        if new==lab[v]: continue
        de=sum(int(D[new,lab[u]]-D[lab[v],lab[u]]) for u in nb[v]); dv=sum(int(D[new,lab[w]]!=2)-int(D[lab[v],lab[w]]!=2) for w in sv[v])
        d=de+Pn*dv
        if d<=0 or rng.random()<math.exp(-d/Tm):
            lab[v]=new; e+=de; viol+=dv
            if viol==0 and (best is None or e<best): best=e
        if it%20000==0: Tm=max(0.03,Tm*0.98); Pn=min(20,Pn*1.01)
    print('seed',seed,'best',best,flush=True)
    if best is not None and (best_all is None or best<best_all): best_all=best
print('Gr(2,4) relaxation best',best_all,'(bar 314; product 332)')
