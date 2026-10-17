"""Max sets of lines y in Z^w (entries 0,+-1,+-2), y.y = 0 mod 4, pairwise y.y' in {0} U (2+4Z)  (=> G/2 has
even diagonal, zero-or-odd off-diagonal: the E8 'J+Gbar' decoder applies with rank <= 1+w).
Heuristic max clique (greedy + randomized restarts).  usage: clique.py w seconds"""
import itertools, sys, time, numpy as np
w=int(sys.argv[1]); T=float(sys.argv[2]); rng=np.random.default_rng(int(sys.argv[3]) if len(sys.argv)>3 else 0)
cand=set()
def canon(v):
    v=tuple(v)
    for x in v:
        if x!=0: return v if x>0 else tuple(-y for y in v)
for S in itertools.combinations(range(w),4):
    for sg in itertools.product((1,-1),repeat=4):
        v=[0]*w
        for i,s in zip(S,sg): v[i]=s
        cand.add(canon(v))
for i in range(w):
    v=[0]*w; v[i]=2; cand.add(canon(v))
for S in itertools.combinations(range(w),2):
    for sg in itertools.product((2,-2),repeat=2):
        v=[0]*w
        for i,s in zip(S,sg): v[i]=s
        cand.add(canon(v))
if w<=10:
    for S in itertools.combinations(range(w),8):
        for sg in itertools.product((1,-1),repeat=8):
            if sg[0]<0: continue
            v=[0]*w
            for i,s in zip(S,sg): v[i]=s
            cand.add(canon(v))
C=np.array(sorted(cand)); n=len(C)
G=C@C.T
ok=((G==0)|((G%4)==2)); np.fill_diagonal(ok,False)
print('w',w,'candidates',n,'norms',sorted(set(np.diag(G).tolist())),flush=True)
deg=ok.sum(1)
best=[]; t0=time.time(); it=0
while time.time()-t0<T:
    it+=1
    # randomized greedy: pick start, then repeatedly add vertex with max remaining-compatible count (noisy)
    alive=np.ones(n,bool); cl=[]
    v=rng.integers(n)
    while True:
        cl.append(v); alive&=ok[v]; alive[v]=False
        idx=np.nonzero(alive)[0]
        if len(idx)==0: break
        sc=ok[np.ix_(idx,idx)].sum(1)+rng.random(len(idx))*2
        v=idx[np.argmax(sc)]
    if len(cl)>len(best):
        best=cl; Cb=C[best]; r=np.linalg.matrix_rank(Cb.astype(float))
        Gb=(Cb@Cb.T)//2; rk2=np.linalg.matrix_rank(Gb%2) # float rank as proxy; exact F2 below
        M=(Gb%2).astype(np.uint8)
        # exact F2 rank
        A=M.copy(); rr=0
        for c in range(A.shape[1]):
            p=np.nonzero(A[rr:,c])[0]
            if len(p)==0: continue
            p=p[0]+rr; A[[rr,p]]=A[[p,rr]]
            m=A[:,c].copy(); m[rr]=0; A[m==1]^=A[rr]; rr+=1
            if rr==A.shape[0]: break
        c_=rr+1; x=c_*r/len(best)
        print('it',it,'lines',len(best),'rank_Q',r,'F2rank',rr,'c<=',c_,'x<=c*w/v=%.3f'%x,'norm mix',sorted(set(np.diag(Cb@Cb.T).tolist())),round(time.time()-t0,1),flush=True)
np.save('best_w%d.npy'%w,C[best])
