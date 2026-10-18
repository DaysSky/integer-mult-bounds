"""For optimal per-block configs (shipped P): which lines are the extras, how do the taus' residuals look, and do the
missing lines pair up into cells (so that one helper could carry a cell combination)."""
import sys,pickle,collections
sys.path.insert(0,'.')
from fastb import *
P=[10,15,51,53,56,66,72,89,111]
opt=pickle.load(open('opt_ship.pkl','rb'))
for B in (0,1,3,5):
    bk=Blk(B,P)
    cellsB=[c for c in G.cells if G.cblk[c]==B]
    cnt=collections.Counter()
    for flb,perm,rs,c in opt[B][1][:3000]:
        # recompute extras list
        Pset=bk.Pset
        fkline={H:cc[(flb>>bk.cells.index(cc))&1] for H,cc in zip(bk.Hs,perm)}
        fkc={H:(0 if fkline[H] in Pset else 1<<fkline[H]) for H in bk.Hs}
        rcv=dict(bk.rcv0)
        for p,r in zip(bk.taus,rs):
            for i,H in enumerate(bk.zzp[p]): rcv[H]=p if (r>>i)&1 else (H[0] if H[1]==p else H[1])
        for p in bk.taus:
            if not any(rcv[H]==p for H in bk.zzp[p]): rcv[bk.zzp[p][0]]=p
        cont={H:fkc[H] for H in bk.Hs}; others=[1<<x for x in bk.freed]; miss=[]
        for p in bk.taus:
            mine=[H for H in bk.zzp[p] if rcv[H]==p]; Np=bk.Np0[p]
            for H in mine[1:]: Np^=cont[H]
            des=mine[0]; need_=Np^cont[des]; basis=[]
            for H in bk.Hs:
                if H!=des: addb(basis,cont[H])
            for o in others: addb(basis,o)
            r=reduce_(need_,basis); miss.append(tuple(bits(r)))
        allm=sorted(set(x for m in miss for x in m))
        pairs=[c for c in cellsB if c[0] in allm and c[1] in allm]
        cnt[(tuple(miss),tuple(pairs))]+=1
    print('B',B,'taus',bk.taus,'distinct residual patterns',len(cnt))
    for k,n in cnt.most_common(4): print('   ',n,'residuals per tau',k[0],'missing pairs that are cells',k[1])
