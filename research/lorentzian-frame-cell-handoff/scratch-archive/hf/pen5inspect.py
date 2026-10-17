exec(open('pen5gen.py').read().split("best=1e9")[0])
sh=[((0, 1, 8, 9, 10, 11), (2, 3, 4, 5, 6, 7)), ((2, 3, 8, 9, 10, 11), (0, 1, 4, 5, 6, 7)), ((0, 1, 4, 5, 6, 7), (2, 3, 8, 9, 10, 11)), ((2, 3, 4, 5, 6, 7), (0, 1, 8, 9, 10, 11))]
def fit2(sh,iters=1500):
    k=len(sh)
    a=[np.zeros(12) for _ in sh]; b=[np.zeros(12) for _ in sh]
    for e,(S,Q) in enumerate(sh): a[e][list(Q)]=rng.standard_normal(len(Q)); b[e][list(S)]=rng.standard_normal(len(S))
    for it in range(iters):
        for e,(S,Q) in enumerate(sh):
            Rm=T-sum(np.outer(a[f],b[f]) for f in range(k) if f!=e)
            Ql=list(Q); Sl=list(S); bb=b[e][Sl]; Wm=W[np.ix_(Ql,Sl)]; Rs=Rm[np.ix_(Ql,Sl)]
            a[e][:]=0; a[e][Ql]=(Wm*Rs*bb).sum(1)/((Wm*bb**2).sum(1)+1e-12)
            aa=a[e][Ql]; b[e][:]=0; b[e][Sl]=(Wm*Rs*aa[:,None]).sum(0)/((Wm*aa[:,None]**2).sum(0)+1e-12)
    M=sum(np.outer(a[f],b[f]) for f in range(k))
    return M
A_lines=[i for i in range(12) if hid[L[i]] in (0,1)]
for rep in range(4):
    M=fit2(sh)
    r=np.sqrt((W*(M-T)**2).sum())
    blk=M[np.ix_(A_lines,A_lines)]; Nb=T[np.ix_(A_lines,A_lines)]*0+N[np.ix_([L[i] for i in A_lines],[L[i] for i in A_lines])]
    print('rep',rep,'cross residual',round(r,10))
    print('  fitted within (class A) / N ratio:\n', np.round(np.where(np.abs(Nb)>0, blk/np.where(Nb==0,1,Nb), 0),4))
