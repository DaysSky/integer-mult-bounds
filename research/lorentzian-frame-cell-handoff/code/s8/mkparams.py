"""write a gen_p4 parameter file from a choice (per-block (flb, perm, rs)) + extras, on top of P111's keeper plan"""
import sys,pickle,json
sys.path.insert(0,'.')
from bld import *
P=[10,15,51,53,56,66,72,89,111]
prm=json.load(open(R+'/data/punct.json')); sel0={int(k):v for k,v in prm['receivers'].items()}
def write(choice,extras,out,note):
    fl,assign,sel=make_params(P,choice,rcvbase=sel0)
    dcellof,keepline,home,qhostD6,zz=gen_p3.derive(G,sol,fl)
    dual=set(home.values())
    nd=sorted(c for c in G.cells if c not in dual)
    d=dict(note=note,punctured=P,nodeopt=2000,node_seed=0,
           receivers={str(p):sel[p] for p in sorted(sel)},
           freeline=[[list(c),fl.get(c,0)] for c in nd],
           thirds=[[list(H),list(assign[H])] for H in sorted(zz)],
           extras={str(B):[x if isinstance(x,int) else list(x) for x in extras[B]] for B in sorted(extras)})
    json.dump(d,open(out,'w'),separators=(',',':'))
if __name__=='__main__':
    res=pickle.load(open(sys.argv[1],'rb'))[int(sys.argv[2])]
    write(res[3],res[4],sys.argv[3],sys.argv[4])
