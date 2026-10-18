"""Build a P111-family word from explicit per-block (freeline, thirds, receivers) choices; save; exact replay; profile; price."""
import sys,random,json,pickle,gzip
sys.path.insert(0,'/tmp/claude-0/-home-user-integer-mult-bounds/45552e66-7196-5fbb-857a-ded5e6dbacae/scratchpad/p111s')
from loc import *
sys.path.insert(0,'/home/user/integer-mult-bounds/research/e8-bit-p111-tuned/tune')
sys.path.insert(0,'/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import wlib, pricer
from wordkit import save
def make_params(P,choice,seed=552,rcvbase=None):
    """choice: B -> (flb, perm, rs). Others from plan_thirds(seed)."""
    fl,assign=gen_p3.plan_thirds(G,sol,random.Random(seed))
    fl=dict(fl); assign=dict(assign); sel=dict(rcvbase or {})
    for B,(flb,perm,rs) in choice.items():
        cells=NDC[B]
        for i,c in enumerate(cells): fl[c]=(flb>>i)&1
        for H,c in zip(ZZB[G.comp[B]],perm): assign[H]=c
        taus=[p for p in P if G.blk[p]==G.comp[B]]
        sel.update(dict(zip(taus,rs)))
    return fl,assign,sel
def build(P,fl,assign,sel,nodeopt=2000,node_seed=0):
    gen_p3.NODEOPT[0]=nodeopt
    extras={}
    for _ in range(20):
        res=gen_p3.build(G,sol,P,fl,assign,extras=extras,verbose=False,rcvsel=sel,node_seed=node_seed)
        if res[0]=='missing':
            for B,ls in res[1].items(): extras[B]=sorted(set(extras.get(B,[]))|set(ls))
            continue
        return res[1],extras
def evalw(word):
    H=wlib.paid(word)
    c,_,_=pricer.price(H,word['v'],8,word['R'])
    return H,c
if __name__=='__main__':
    pass
