"""Generalised block cost: extras may be single lines (extra carriers) or cell sums x_a + x_b of a cell of B (cell-sum
helpers, gen_p4).  cost = max(|E|, junk directions needed) with E minimal (exact search over candidate extras)."""
import sys,itertools
sys.path.insert(0,'/tmp/claude-0/-home-user-integer-mult-bounds/45552e66-7196-5fbb-857a-ded5e6dbacae/scratchpad/p111s')
from fastb import *
class BlkG(Blk):
    def __init__(s,B,P):
        Blk.__init__(s,B,P)
        s.cellsB=[c for c in G.cells if G.cblk[c]==B and c[0] not in s.Pset and c[1] not in s.Pset]
    def setup(s,flb,perm,rs):
        Pset=s.Pset; fkline={}
        for H,c in zip(s.Hs,perm):
            i=s.cells.index(c); fkline[H]=c[(flb>>i)&1]
        fkc={H:(0 if fkline[H] in Pset else 1<<fkline[H]) for H in s.Hs}
        rcv=dict(s.rcv0)
        for p,r in zip(s.taus,rs):
            for i,H in enumerate(s.zzp[p]):
                rcv[H]=p if (r>>i)&1 else (H[0] if H[1]==p else H[1])
        for p in s.taus:
            if not any(rcv[H]==p for H in s.zzp[p]): rcv[s.zzp[p][0]]=p
        return fkc,rcv
    def sim(s,fkc,rcv,E):
        """mini-node with extra vectors E (ints); returns missing mask (0 = success)"""
        cont={H:fkc[H] for H in s.Hs}
        others=list(E)+[1<<x for x in s.freed]
        missing=0; plan=[]
        for p in s.taus:
            mine=[H for H in s.zzp[p] if rcv[H]==p]
            Np=s.Np0[p]
            for H in mine[1:]: Np^=cont[H]
            plan.append((mine[0],Np))
        for des,Np in plan:
            need_=Np^cont[des]; basis=[]
            for H in s.Hs:
                if H!=des: addb(basis,cont[H])
            for o in others: addb(basis,o)
            r=reduce_(need_,basis)
            if r: missing|=r; continue
            cont[des]^=need_
        return missing,cont
    def junk(s,cont,rcv):
        rows=[]
        for u in s.us:
            acc=s.base[u]
            for H in s.uzz[u]:
                if rcv[H]==u: acc^=cont[H]
            if acc & ~(G.blocks[s.B]&s.live): return None
            r=0
            for l in bits(acc):
                if l not in s.pos: return None
                r|=1<<s.pos[l]
            rows.append(r)
        bs=[]; nj=0
        for r in rows:
            if not span_add(bs,r):
                nj+=1; assert span_add(bs,r|(1<<(len(s.srcl)+nj-1)))
        return nj
    def single(s,fkc,rcv):
        extras=[]
        for it in range(20):
            m,cont=s.sim(fkc,rcv,[1<<x for x in extras])
            if not m: return extras,cont
            extras=sorted(set(extras)|set(bits(m)))
        return None,None
    def gcost(s,flb,perm,rs,bound=None):
        """returns (cost, E as list of line tuples, nj) or None if cost >= bound"""
        fkc,rcv=s.setup(flb,perm,rs)
        ext,cont=s.single(fkc,rcv)
        if ext is None: return None
        nj=s.junk(cont,rcv)
        if nj is None: return None
        M=set(ext)
        lb=max(nj,(len(M)+1)//2)
        if bound is not None and lb>=bound: return None
        best=(max(len(M),nj),[(x,) for x in sorted(M)])
        cands=[(x,) for x in sorted(M)]+[c for c in s.cellsB if c[0] in M or c[1] in M]
        for k in range((len(M)+1)//2,len(M)):
            if max(k,nj)>=best[0]: break
            found=None
            for comb in itertools.combinations(cands,k):
                cov=set(l for c in comb for l in c)
                if not M<=cov: continue
                E=[sum(1<<l for l in c) for c in comb]
                m,_=s.sim(fkc,rcv,E)
                if not m: found=list(comb); break
            if found is not None: best=(max(k,nj),found); break
        if bound is not None and best[0]>=bound: return None
        return best[0],best[1],nj
