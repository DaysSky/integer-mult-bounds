"""Per-block profile scan: other blocks fixed at a base choice, block B runs over its optimal configs; score = exact
local paid profile -> fee proxy (tune.fee_table at a = 0.00174).  Writes the scored list."""
import sys,pickle,json,random,collections,math
sys.path.insert(0,'.')
sys.path.insert(0,'/tmp/claude-0/-home-user-integer-mult-bounds/45552e66-7196-5fbb-857a-ded5e6dbacae/scratchpad/pkg/code')
from bld import *
import gen_p4
P=[10,15,51,53,56,66,72,89,111]
prm=json.load(open(R+'/data/punct.json')); sel0={int(k):v for k,v in prm['receivers'].items()}
gopt=pickle.load(open('gopt_ship.pkl','rb'))
base=pickle.load(open('sampg_1.pkl','rb'))[0]     # best sampled config as the base
B=int(sys.argv[1]); cap=int(sys.argv[2])
a=0.00174; fee=lambda k: k*math.expm1(a*math.log(64/k))
gen_p4.NODEOPT[0]=1
cands=gopt[B][1]
rng=random.Random(B)
idx=list(range(len(cands))) if len(cands)<=cap else rng.sample(range(len(cands)),cap)
out=[]
for i in idx:
    flb,perm,rs,E,nj=cands[i]
    choice=dict(base[3]); choice[B]=(flb,perm,rs)
    extras=dict(base[4]); extras[B]=[x[0] if len(x)==1 else list(x) for x in E]
    fl,assign,sel=make_params(P,choice,rcvbase=sel0)
    r=gen_p4.build(G,sol,P,fl,assign,extras=extras,verbose=False,rcvsel=sel)
    if r[0]=='missing': continue
    w=r[1]
    if w['R']!=434: continue
    H=wlib.paid(w)
    out.append((sum(fee(k)*n for k,n in H.items()),dict(H),i))
out.sort()
pickle.dump(out,open('blkprof_%d.pkl'%B,'wb'))
print(B,'scanned',len(out),'best',out[0],'worst',out[-1][:2],flush=True)
