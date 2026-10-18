import sys,pickle,json
sys.path.insert(0,'.')
sys.path.insert(0,'/home/user/integer-mult-bounds/research/e8-bit-p111-r434/code')
from bld import *
import gen_p4, mkparams
P=[10,15,51,53,56,66,72,89,111]
prm=json.load(open(R+'/data/punct.json')); sel0={int(k):v for k,v in prm['receivers'].items()}
gopt=pickle.load(open('gopt_ship.pkl','rb'))
base=pickle.load(open('sampg_1.pkl','rb'))[0]
gen_p4.NODEOPT[0]=1
out=[]
for b1 in (None,'best'):
  for b5 in (None,'best'):
    choice=dict(base[3]); extras=dict(base[4])
    for B,flag in ((1,b1),(5,b5)):
        if flag:
            sc=pickle.load(open('blkprof_%d.pkl'%B,'rb'))
            i=sc[0][2]; flb,perm,rs,E,nj=gopt[B][1][i]
            choice[B]=(flb,perm,rs); extras[B]=[x[0] if len(x)==1 else list(x) for x in E]
    fl,assign,sel=make_params(P,choice,rcvbase=sel0)
    r=gen_p4.build(G,sol,P,fl,assign,extras=extras,verbose=False,rcvsel=sel)
    w=r[1]; H=wlib.paid(w)
    print(b1,b5,w['R'],dict(H),flush=True)
    out.append((b1,b5,dict(H),choice,extras))
pickle.dump(out,open('combo.pkl','wb'))
