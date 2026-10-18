import sys,itertools,pickle,time
sys.path.insert(0,'/tmp/claude-0/-home-user-integer-mult-bounds/45552e66-7196-5fbb-857a-ded5e6dbacae/scratchpad/p111s')
from fastg import *
from multiprocessing import Pool
P=sorted(int(x) for x in sys.argv[1].split(','))
def solveB(B):
    bk=BlkG(B,P); best=None; opt=[]
    for flb in range(64):
        for perm in itertools.permutations(bk.cells):
            for rs in itertools.product((1,2,3),repeat=len(bk.taus)):
                r=bk.gcost(flb,perm,rs,bound=None if best is None else best+1)
                if r is None: continue
                if best is None or r[0]<best: best=r[0]; opt=[]
                if r[0]==best and len(opt)<200000: opt.append((flb,perm,rs,r[1],r[2]))
    return B,best,opt
if __name__=='__main__':
    BL=[int(x) for x in sys.argv[2].split(',')]
    out={}; t=time.time()
    with Pool(4) as pool:
        for B,best,opt in pool.imap_unordered(solveB,BL):
            out[B]=(best,opt); print(B,'best',best,'n',len(opt),'example',opt[0] if opt else None,'%.0fs'%(time.time()-t),flush=True)
    pickle.dump(out,open(sys.argv[3],'wb'))
