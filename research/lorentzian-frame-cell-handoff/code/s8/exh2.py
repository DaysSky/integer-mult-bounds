import sys,itertools,json,time,pickle
sys.path.insert(0,'/tmp/claude-0/-home-user-integer-mult-bounds/45552e66-7196-5fbb-857a-ded5e6dbacae/scratchpad/p111s')
from loc import *
from multiprocessing import Pool
P=sorted(int(x) for x in sys.argv[1].split(','))
BL=[int(x) for x in sys.argv[2].split(',')]
def solveB(B):
    cb=G.comp[B]; taus=[p for p in P if G.blk[p]==cb]
    best=None; opt=[]
    cells=NDC[B]
    for flb in range(64):
        fl={c:(flb>>i)&1 for i,c in enumerate(cells)}
        for perm in itertools.permutations(cells):
            for rs in itertools.product((1,2,3),repeat=len(taus)):
                c=block_cost(B,P,fl,list(perm),dict(zip(taus,rs)))
                if c is None: continue
                s=sum(c)
                if best is None or s<best: best=s; opt=[]
                if s==best: opt.append((flb,perm,rs,c))
    return B,best,opt
if __name__=='__main__':
    out={}
    with Pool(4) as pool:
        for B,best,opt in pool.imap_unordered(solveB,BL):
            print(B,best,len(opt),flush=True); out[B]=(best,opt)
    pickle.dump(out,open(sys.argv[3],'wb'))
