import sys,pickle,json,random
sys.path.insert(0,'.')
sys.path.insert(0,'/tmp/claude-0/-home-user-integer-mult-bounds/45552e66-7196-5fbb-857a-ded5e6dbacae/scratchpad/pkg/code')
from bld import *
from fastg import BlkG
import gen_p4
from mpmath import mp
E1=mp.mpf('0.001734473240795253742474')
P=[10,15,51,53,56,66,72,89,111]
prm=json.load(open(R+'/data/punct.json')); sel0={int(k):v for k,v in prm['receivers'].items()}
opt=pickle.load(open('opt_ship.pkl','rb'))
want={0:{49,63},3:{29,97}}
choice={}; extras={}
for B in (0,1,3,5):
    bk=BlkG(B,P)
    for flb,perm,rs,c in opt[B][1]:
        fkc,rcv=bk.setup(flb,perm,rs); ext,_=bk.single(fkc,rcv)
        if B not in want or set(ext)==want[B]:
            choice[B]=(flb,perm,rs); extras[B]=[list(want[B])] if B in want else ext; break
print('extras',extras)
fl,assign,sel=make_params(P,choice,rcvbase=sel0)
gen_p4.NODEOPT[0]=1
res=gen_p4.build(G,sol,P,fl,assign,extras=extras,verbose=False,rcvsel=sel)
print(res[0] if res[0]=='missing' else '')
word=res[1]
H,c=evalw(word)
print('R',word['R'],word['stats'],dict(H),'%+.4f%%'%(float(c/E1-1)*100))
