import sys,itertools
sys.path.insert(0,'.')
from loc import *
P=[10,15,51,53,56,66,72,89,111]
Pset=set(P); live=((1<<V)-1)&~sum(1<<q for q in P)
exq=lambda q,H: gen_p3.ex_part(G,sol,q,H)&live
for p in P:
    B=G.comp[G.blk[p]]; Bm=G.blocks[B]&live
    Hp=qhostD6[p]; lp=kl0[dcellof[p]]
    zzp=sorted(H for H in zz if G.phi[H[0]]==G.phi[p])
    Np=(e8.HYP[p]&live)^(1<<lp)^ExF[Hp]&live
    for H in zzp: Np^=ExF[H]&live
    opts=[]
    Ds=[Hp]+zzp
    for sub in itertools.product((0,1,2),repeat=3):
        N2=Np
        for H,s in zip(Ds,sub):
            q1,q2=G.d6quads[H]
            if s==1: N2^=exq(q2,H)      # use o1 alone (ex1) instead of E = ex1+ex2
            if s==2: N2^=exq(q1,H)      # use o2 alone
        inB = N2 & ~Bm == 0
        opts.append((sub,inB,bin(N2).count('1'),bin(N2&~Bm).count('1')))
    print(p,'B',B,'base |Np|',bin(Np).count('1'),'outside',bin(Np&~Bm).count('1'),'| options in B:',[(o[0],o[2]) for o in opts if o[1]])
