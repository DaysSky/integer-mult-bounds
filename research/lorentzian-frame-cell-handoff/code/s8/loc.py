"""Block-local exact replica of gen_p3.build's helper accounting (mini-nodes, extras iteration, block-node junk)."""
import os,sys,random,json,itertools
R='/home/user/integer-mult-bounds/research/e8-bit-p111'
sys.path.insert(0,R+'/code'); sys.path.insert(0,R+'/../e8-bit-carrier-skeleton/code/skeleton')
import gen_p3,e8
from geom import Geom
from planio import load_plan
from gen import span_add
V=e8.V
G=Geom(); sol=load_plan(R+'/data/plan-l3.json')
dcellof,kl0,home,qhostD6,zz=gen_p3.derive(G,sol)
dualcells=set(home.values())
ExF={H:gen_p3.ex_part(G,sol,G.d6quads[H][0],H)^gen_p3.ex_part(G,sol,G.d6quads[H][1],H) for H in G.cells}
NDC={b:[c for c in G.cells if c not in dualcells and G.cblk[c]==b] for b in range(10)}   # 6 non-dual cells per block
ZZB={b:sorted(H for H in zz if G.cblk[H]==b) for b in range(10)}                          # 6 zz D6s per block
ELIG=[p for p in range(V) if gen_p3.eligible(G,sol,dcellof,kl0,qhostD6,zz,p)[0]]
bits=e8.bits

def express_ok(target,vecs):
    b=[]
    for v in vecs: span_add(b,v)
    r=target
    for _ in range(2):
        for bv in b:
            pass
    # reduce
    basis=[]
    for v in vecs:
        for pb,bv in basis:
            if v>>pb&1: v^=bv
        if v:
            basis.append((v.bit_length()-1,v)); basis.sort(key=lambda z:-z[0])
    for pb,bv in basis:
        if r>>pb&1: r^=bv
    return r

def block_cost(B,P,fl,perm,rcvsel,verbose=False):
    """B: supplying block. fl: dict cell->0/1 for NDC[B]; perm: list of 6 cells (NDC[B] order) assigned to ZZB[comp(B)];
    rcvsel: p->1..3 for taus p in comp(B). Returns (extras, newjunk) for block B (mini-node of B, block node of B)."""
    Pset=set(P); live=((1<<V)-1)&~sum(1<<s for s in Pset)
    cb=G.comp[B]
    Hs=ZZB[cb]; thirds=dict(zip(Hs,perm))
    def kline(c):            # keepline of a cell
        if c in fl: return c[fl[c]]
        return kl0[c] if c in dualcells else None
    fkline={H:kline(thirds[H]) for H in Hs}
    fkcont={H:(1<<fkline[H]) if fkline[H] not in Pset else 0 for H in Hs}
    # receivers for zz D6s of block cb
    rcv={H:sol['rcv'][H] for H in Hs}
    taus=[p for p in sorted(P) if G.blk[p]==cb]
    zzp={}
    for p in taus:
        f=G.phi[p]; zzp[p]=sorted(H for H in zz if G.phi[H[0]]==f)
        if p in rcvsel:
            for i,H in enumerate(zzp[p]):
                rcv[H]=p if (rcvsel[p]>>i)&1 else (H[0] if H[1]==p else H[1])
        if not any(rcv[H]==p for H in zzp[p]): rcv[zzp[p][0]]=p
    Ex={H:ExF[H]&live for H in G.cells}
    freed=[]
    for q in P:
        if G.blk[q]==B:
            s=kl0[dcellof[q]]
            if s not in Pset: freed.append(s)
    extras=[]
    for it in range(20):
        # wires: fks (dedupe by register = by H's thirds cell), extras, freed
        cont={('fk',thirds[H]):fkcont[H] for H in Hs}
        for s in extras: cont[('x',s)]=1<<s
        for s in freed: cont[('s',s)]=1<<s
        wires=sorted(set(('fk',thirds[H]) for H in Hs))+[('x',s) for s in extras]+[('s',s) for s in freed]
        missing=set(); finalfk={}
        plan=[]
        for p in taus:
            Hp=qhostD6[p]; lp=kl0[dcellof[p]]
            Np=(e8.HYP[p]&live)^(1<<lp)^Ex[Hp]
            for H in zzp[p]: Np^=Ex[H]
            mine=[H for H in zzp[p] if rcv[H]==p]
            des=('fk',thirds[mine[0]])
            for H in mine[1:]: Np^=cont[('fk',thirds[H])]
            plan.append((p,des,Np))
        for p,des,Np in plan:
            need_=Np^cont[des]
            r=express_ok(need_,[cont[w] for w in wires if w!=des])
            if r: missing|=set(bits(r)); continue
            cont[des]^=need_
        if not missing: break
        extras=sorted(set(extras)|missing)
    else:
        return None
    # block node of B: targets u live in cb; srcw = keepers (sources) of dual cells in B with live keepline
    srcl=[kl0[c] for c in G.cells if c in dualcells and G.cblk[c]==B and kl0[c] not in Pset]
    pos={l:k for k,l in enumerate(srcl)}
    us=[t for t in bits(live) if G.blk[t]==cb]
    rowsN=[]
    for u in us:
        C=dcellof[u]; acc=e8.HYP[u]&live
        if kl0[C] not in Pset: acc^=1<<kl0[C]
        for x in G.phi[u]:
            if x==u: continue
            H=tuple(sorted((u,x)))
            if H==qhostD6[u]: acc^=Ex[H]
            elif H in thirds and rcv[H]==u: acc^=cont[('fk',thirds[H])]^Ex[H]
            else: acc^=Ex[H]
        if acc & ~(G.blocks[B]&live): return None
        r=0
        for l in bits(acc):
            if l not in pos: return None
            r|=1<<pos[l]
        rowsN.append(r)
    avail=[s for s in extras if s in pos]
    bs=[]; nj=0
    for r in rowsN:
        if not span_add(bs,r):
            nj+=1
            rr=r|(1<<(len(srcl)+nj-1))
            assert span_add(bs,rr)
    newjunk=max(0,nj-len(avail))
    return len(extras),newjunk

def total(P,FL,PERM,RS):
    tot=0; per={}
    for B in range(10):
        c=block_cost(B,P,FL[B],PERM[B],RS)
        if c is None: return None,None
        per[B]=c; tot+=sum(c)
    return 429+tot,per
