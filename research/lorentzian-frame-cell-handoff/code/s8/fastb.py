"""Fast exact block-local cost (same accounting as loc.block_cost / gen_p3.build), precomputed per (B, P)."""
import sys,itertools
sys.path.insert(0,'/tmp/claude-0/-home-user-integer-mult-bounds/45552e66-7196-5fbb-857a-ded5e6dbacae/scratchpad/p111s')
from loc import *
def reduce_(r,basis):
    for pb,bv in basis:
        if r>>pb&1: r^=bv
    return r
def addb(basis,v):
    v=reduce_(v,basis)
    if v: basis.append((v.bit_length()-1,v)); basis.sort(key=lambda z:-z[0]); return True
    return False
class Blk:
    def __init__(s,B,P):
        s.B=B; s.P=sorted(P); Pset=set(P); s.Pset=Pset
        s.live=live=((1<<V)-1)&~sum(1<<q for q in Pset)
        cb=G.comp[B]; s.cb=cb
        s.Hs=ZZB[cb]; s.cells=NDC[B]
        s.taus=[p for p in s.P if G.blk[p]==cb]
        Ex={H:ExF[H]&live for H in G.cells}; s.Ex=Ex
        s.freed=[kl0[dcellof[q]] for q in s.P if G.blk[q]==B and kl0[dcellof[q]] not in Pset]
        s.zzp={p:sorted(H for H in zz if G.phi[H[0]]==G.phi[p]) for p in s.taus}
        s.Np0={}
        for p in s.taus:
            Hp=qhostD6[p]; lp=kl0[dcellof[p]]
            Np=(e8.HYP[p]&live)^(1<<lp)^Ex[Hp]
            for H in s.zzp[p]: Np^=Ex[H]
            s.Np0[p]=Np
        s.srcl=[kl0[c] for c in G.cells if c in dualcells and G.cblk[c]==B and kl0[c] not in Pset]
        s.pos={l:k for k,l in enumerate(s.srcl)}
        s.us=[t for t in bits(live) if G.blk[t]==cb]
        s.base={}; s.uzz={}
        for u in s.us:
            C=dcellof[u]; acc=e8.HYP[u]&live
            if kl0[C] not in Pset: acc^=1<<kl0[C]
            zl=[]
            for x in G.phi[u]:
                if x==u: continue
                H=tuple(sorted((u,x))); acc^=Ex[H]
                if H in s.Hs: zl.append(H)
            s.base[u]=acc; s.uzz[u]=zl
        s.rcv0={H:sol['rcv'][H] for H in s.Hs}
    def cost(s,flb,perm,rs):
        Pset=s.Pset
        fkline={}
        for H,c in zip(s.Hs,perm):
            i=s.cells.index(c); fkline[H]=c[(flb>>i)&1]
        fkc={H:(0 if fkline[H] in Pset else 1<<fkline[H]) for H in s.Hs}
        rcv=dict(s.rcv0)
        for p,r in zip(s.taus,rs):
            for i,H in enumerate(s.zzp[p]):
                rcv[H]=p if (r>>i)&1 else (H[0] if H[1]==p else H[1])
        for p in s.taus:
            if not any(rcv[H]==p for H in s.zzp[p]): rcv[s.zzp[p][0]]=p
        extras=[]
        for it in range(20):
            cont={H:fkc[H] for H in s.Hs}
            others=[1<<x for x in extras]+[1<<x for x in s.freed]
            missing=0; plan=[]
            for p in s.taus:
                mine=[H for H in s.zzp[p] if rcv[H]==p]
                Np=s.Np0[p]
                for H in mine[1:]: Np^=cont[H]
                plan.append((mine[0],Np))
            for des,Np in plan:
                need_=Np^cont[des]
                basis=[]
                for H in s.Hs:
                    if H!=des: addb(basis,cont[H])
                for o in others: addb(basis,o)
                r=reduce_(need_,basis)
                if r: missing|=r; continue
                cont[des]^=need_
            if not missing: break
            extras=sorted(set(extras)|set(bits(missing)))
        else: return None
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
        avail=sum(1 for x in extras if x in s.pos)
        bs=[]; nj=0
        for r in rows:
            if not span_add(bs,r):
                nj+=1; assert span_add(bs,r|(1<<(len(s.srcl)+nj-1)))
        return len(extras),max(0,nj-avail)
