import numpy as np, pickle, sys, time, random
d=pickle.load(open('e8f.pkl','rb')); L=d['L']; frames=d['frames']; orth=d['orth']
nf=len(frames)
P=[]
for (a,b) in frames:
    P+= [L[a], L[b], L[a]+L[b]]
P=np.array(P)
Om=((P@P.T)//4)%2
Om=Om.astype(np.uint8)
print('Omega built',Om.shape,flush=True)
NV=nf*9
def vinfo(v):
    T=v//9; c=v%9; return T, c//3, c%3
# row of adjacency for vertex v (bool array len NV)
Tidx=np.repeat(np.arange(nf),9); Kidx=np.tile(np.repeat(np.arange(3),3),nf); Lidx=np.tile(np.tile(np.arange(3),3),nf)
def row(v):
    T,i,j=vinfo(v)
    o=orth[T][Tidx]
    c1=Om[3*T+i][3*Tidx+Lidx]   # omega(psi_T, phi_S)
    c2=Om[3*T+j][3*Tidx+Kidx]   # omega(psi_S, phi_T)
    r=o|((c1==1)&(c2==1))
    r[Tidx==T]=False
    return r
rng=random.Random(int(sys.argv[1])); tl=float(sys.argv[2])
cache={}
def R(v):
    if v not in cache:
        if len(cache)>4000: cache.clear()
        cache[v]=row(v)
    return cache[v]
best=[]; t0=time.time()
C=[]; conf=np.zeros(NV,dtype=np.int32)  # number of clique members NOT adjacent
tabu={}
it=0
while time.time()-t0<tl:
    it+=1
    k=len(C)
    free=np.nonzero(conf==0)[0]
    free=free[[v not in C for v in free]] if len(free)<5000 else free
    inC=set(C)
    free=[v for v in free if v not in inC and tabu.get(v,0)<it]
    if free:
        v=rng.choice(free)
        C.append(v); conf+= ~R(v)
        conf[v]-=0
    else:
        one=np.nonzero(conf==1)[0]
        one=[v for v in one if v not in inC and tabu.get(v,0)<it]
        if one and rng.random()<0.9:
            v=rng.choice(one)
            rv=R(v)
            u=[c for c in C if not rv[c]][0]
            C.remove(u); conf-= ~R(u); tabu[u]=it+7
            C.append(v); conf+= ~rv
        else:
            u=rng.choice(C); C.remove(u); conf-= ~R(u); tabu[u]=it+7
    if len(C)>len(best):
        best=list(C); print(len(best),round(time.time()-t0,1),it,flush=True)
pickle.dump(best,open('asym_best_%s.pkl'%sys.argv[1],'wb'))
print('final',len(best))
