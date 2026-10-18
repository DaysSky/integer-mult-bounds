"""Exact per-block minimum of (extra carriers + new junk wires) for every subset S of eligible lines of a complementary
block pair, over freeline (64) x thirds permutation (720) x receivers (3^k); fastb.Blk (validated against gen_p3.build
through loc.block_cost).  Resumes from census.pkl."""
import sys,itertools,time,pickle,os
sys.path.insert(0,'/tmp/claude-0/-home-user-integer-mult-bounds/45552e66-7196-5fbb-857a-ded5e6dbacae/scratchpad/p111s')
from fastb import *
from multiprocessing import Pool
EL=[p for p in ELIG if p>=8]
pairs=[(0,1),(2,4),(3,5),(6,9),(7,8)]
jobs=[]
for X,Y in pairs:
    el=[p for p in EL if G.blk[p] in (X,Y)]
    for k in range(len(el)+1):
        for S in itertools.combinations(el,k):
            for B in (X,Y): jobs.append((B,S))
def solve(job):
    B,S=job; bk=Blk(B,list(S)); best=None; nopt=0
    for flb in range(64):
        for perm in itertools.permutations(bk.cells):
            for rs in itertools.product((1,2,3),repeat=len(bk.taus)):
                c=bk.cost(flb,perm,rs)
                if c is None: continue
                s=sum(c)
                if best is None or s<best[0]: best=(s,c,flb,perm,rs); nopt=0
                if s==best[0]: nopt+=1
                if best[0]==0 and not bk.taus: return job,best,nopt
    return job,best,nopt
if __name__=='__main__':
    out=pickle.load(open('census.pkl','rb')) if os.path.exists('census.pkl') else {}
    todo=[j for j in jobs if j not in out]
    todo.sort(key=lambda j:-len([p for p in j[1] if G.blk[p]==G.comp[j[0]]]))   # heavy jobs first
    print('done',len(out),'todo',len(todo),flush=True); t=time.time()
    with Pool(4) as pool:
        for job,best,nopt in pool.imap_unordered(solve,todo):
            out[job]=(best,nopt)
            print(job,best[:2] if best else None,nopt,'%.0fs'%(time.time()-t),flush=True)
            pickle.dump(out,open('census.pkl','wb'))
