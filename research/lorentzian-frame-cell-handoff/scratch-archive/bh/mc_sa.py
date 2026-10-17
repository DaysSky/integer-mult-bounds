import random, math, pickle, sys
g=pickle.load(open('bh.pkl','rb')); E=g['phys']; S=g['sessions']; V=182
nb=[[] for _ in range(V)]; sv=[[] for _ in range(V)]
for u,v in E: nb[u].append(v); nb[v].append(u)
for s,t in S: sv[s].append(t); sv[t].append(s)
rng=random.Random(int(sys.argv[1])); K=int(sys.argv[2])
lab=[rng.randrange(K) for _ in range(V)]
e=sum(lab[u]!=lab[v] for u,v in E); viol=sum(lab[s]==lab[t] for s,t in S)
P=2.0; Tm=2.0; best=None
for it in range(int(float(sys.argv[3]))):
    v=rng.randrange(V); new=lab[rng.choice(nb[v])] if rng.random()<0.7 else rng.randrange(K)
    if new==lab[v]: continue
    de=sum((new!=lab[u])-(lab[v]!=lab[u]) for u in nb[v]); dv=sum((new==lab[w])-(lab[v]==lab[w]) for w in sv[v])
    d=de+P*dv
    if d<=0 or rng.random()<math.exp(-d/Tm):
        lab[v]=new; e+=de; viol+=dv
        if viol==0 and (best is None or e<best): best=e
    if it%20000==0: Tm=max(0.03,Tm*0.98); P=min(20,P*1.01)
print('K',K,'seed',sys.argv[1],'best multicut',best)
