import numpy as np, pickle, random, math, sys, time, collections
q=sys.argv[1]
T=pickle.load(open('../flag/table_q%s.pkl'%q,'rb')); cost=T['cost'].astype(np.int32); isWT=T['isWT']
acts=pickle.load(open('../flag/acts_q%s.pkl'%q,'rb'))
N=cost.shape[0]; g=pickle.load(open('bh.pkl','rb')); phys=g['phys']; ses=g['sessions']
V=182; nb=[[] for _ in range(V)]; sv=[[] for _ in range(V)]
for u,v in phys: nb[u].append(v); nb[v].append(u)
for s,t in ses: sv[s].append(t); sv[t].append(s)
rng=random.Random(int(sys.argv[2])); P=4.0
phi=[0]*V
def local(v,c,phi):
    return sum(int(cost[c,phi[u]]) for u in nb[v]), sum(0 if isWT[c,phi[w]] else 1 for w in sv[v])
e=sum(int(cost[phi[u],phi[v]]) for u,v in phys); viol=sum(1 for s,t in ses if not isWT[phi[s],phi[t]])
best=None; Tmp=3.0; steps=int(float(sys.argv[3])); t0=time.time()
def ball(v,r):
    S={v}; fr=[v]
    for _ in range(r):
        fr=[y for x in fr for y in nb[x] if y not in S]; S.update(fr)
    return S
for it in range(steps):
    if rng.random()<0.1:
        S=ball(rng.randrange(V),rng.choice([1,1,2,2,3])); a=acts[rng.randrange(len(acts))]
        new={v:int(a[phi[v]]) for v in S}
        de=0; dv=0
        for v in S:
            for u in nb[v]:
                if u not in S: de+=int(cost[new[v],phi[u]])-int(cost[phi[v],phi[u]])
            for w in sv[v]:
                if w not in S: dv+=(0 if isWT[new[v],phi[w]] else 1)-(0 if isWT[phi[v],phi[w]] else 1)
        d=de+P*dv
        if d<=0 or rng.random()<math.exp(-d/Tmp):
            for v in S: phi[v]=new[v]
            e+=de; viol+=dv
    else:
        v=rng.randrange(V); r=rng.random()
        if r<0.5: newc=phi[rng.choice(nb[v])]
        elif r<0.8 and sv[v]:
            w=sv[v][rng.randrange(len(sv[v]))]; cands=np.nonzero(isWT[phi[w]])[0]; newc=int(cands[rng.randrange(len(cands))])
        else: newc=rng.randrange(N)
        if newc==phi[v]: continue
        e0,v0=local(v,phi[v],phi); e1,v1=local(v,newc,phi)
        d=(e1-e0)+P*(v1-v0)
        if d<=0 or rng.random()<math.exp(-d/Tmp):
            phi[v]=newc; e+=e1-e0; viol+=v1-v0
    if viol==0 and (best is None or e<best[0]):
        best=(e,list(phi))
        if e<330: print('feasible',e,'it',it,round(time.time()-t0,1),flush=True)
    if it%30000==0: Tmp=max(0.03,Tmp*0.985); P=min(30,P*1.005)
print('seed',sys.argv[2],'best',best[0] if best else None)
if best: pickle.dump(best,open('best2_%s_%s.pkl'%(q,sys.argv[2]),'wb'))
