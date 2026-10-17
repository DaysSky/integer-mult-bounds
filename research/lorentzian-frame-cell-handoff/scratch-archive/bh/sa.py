import numpy as np, pickle, random, math, sys, time, collections
T=pickle.load(open('../flag/table_q%s.pkl'%sys.argv[1],'rb')); cost=T['cost'].astype(np.int32); isWT=T['isWT']
N=cost.shape[0]
g=pickle.load(open('bh.pkl','rb')); phys=g['phys']; ses=g['sessions']
print('identity row costs',collections.Counter(cost[0].tolist()), 'wT count', int(isWT[0].sum()))
V=182; nb=[[] for _ in range(V)]; sv=[[] for _ in range(V)]
for u,v in phys: nb[u].append(v); nb[v].append(u)
for s,t in ses: sv[s].append(t); sv[t].append(s)
rng=random.Random(int(sys.argv[2])); P=4.0
phi=[rng.randrange(N) for _ in range(V)]
def energy(phi):
    e=sum(cost[phi[u],phi[v]] for u,v in phys); viol=sum(1 for s,t in ses if not isWT[phi[s],phi[t]])
    return e,viol
e,viol=energy(phi); best=None
Tmp=3.0; steps=int(float(sys.argv[3])); t0=time.time()
for it in range(steps):
    v=rng.randrange(V)
    r=rng.random()
    if r<0.5 and nb[v]: new=phi[rng.choice(nb[v])]          # copy a neighbour's chamber
    elif r<0.75 and sv[v]:                                    # a chamber at wT from a session partner
        w=sv[v][rng.randrange(len(sv[v]))]; cands=np.nonzero(isWT[phi[w]])[0]; new=int(cands[rng.randrange(len(cands))])
    else: new=rng.randrange(N)
    old=phi[v]
    if new==old: continue
    de=sum(int(cost[new,phi[u]])-int(cost[old,phi[u]]) for u in nb[v])
    dv=sum((0 if isWT[new,phi[w]] else 1)-(0 if isWT[old,phi[w]] else 1) for w in sv[v])
    d=de+P*dv
    if d<=0 or rng.random()<math.exp(-d/Tmp):
        phi[v]=new; e+=de; viol+=dv
        if viol==0 and (best is None or e<best[0]):
            best=(e,list(phi)); print('feasible cost',e,'it',it,round(time.time()-t0,1),flush=True)
    if it%20000==0:
        Tmp=max(0.05,Tmp*0.97); P=min(40,P*1.01)
    if it%200000==0: print('it',it,'e',e,'viol',viol,'T',round(Tmp,3),'P',round(P,2),flush=True)
print('best',best[0] if best else None, 'target < 314')
if best: pickle.dump(best,open('best_%s_%s.pkl'%(sys.argv[1],sys.argv[2]),'wb'))
