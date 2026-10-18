import sys,itertools,json,time
sys.path.insert(0,'/tmp/claude-0/-home-user-integer-mult-bounds/45552e66-7196-5fbb-857a-ded5e6dbacae/scratchpad/p111s')
from loc import *
from multiprocessing import Pool
P=sorted(int(x) for x in sys.argv[1].split(','))
def solveB(B):
    cb=G.comp[B]; taus=[p for p in P if G.blk[p]==cb]
    hasp=any(G.blk[p] in (B,cb) for p in P)
    if not hasp: return B,(0,0),None
    best=None; cnt=0; t=time.time(); hist={}
    cells=NDC[B]
    for flb in range(64):
        fl={c:(flb>>i)&1 for i,c in enumerate(cells)}
        for perm in itertools.permutations(cells):
            for rs in itertools.product((1,2,3),repeat=len(taus)):
                rcvsel=dict(zip(taus,rs))
                c=block_cost(B,P,fl,list(perm),rcvsel)
                cnt+=1
                if c is None: continue
                s=sum(c); hist[s]=hist.get(s,0)+1
                if best is None or s<best[0]: best=(s,c,flb,list(perm),rs)
    return B,best,dict(sorted(hist.items()))
if __name__=='__main__':
    with Pool(4) as pool:
        tot=0
        for B,best,hist in pool.imap_unordered(solveB,range(10)):
            print(B,'taus',[p for p in P if G.blk[p]==G.comp[B]],'best',best[:2] if best and best[0] is not None and isinstance(best[0],int) else best,'hist',hist,flush=True)
