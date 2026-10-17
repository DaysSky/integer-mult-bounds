import numpy as np, itertools, sys
def inv_mod(a,q): return pow(int(a),q-2,q)
def canon(g,q):
    g=g.copy()%q; n=g.shape[0]
    for i in range(n):
        nz=np.nonzero(g[i])[0]; p=nz[0]
        g[i]=(g[i]*inv_mod(g[i,p],q))%q
        for k in range(i+1,n):
            if g[k,p]: g[k]=(g[k]-g[k,p]*g[i])%q
    return g
def matinv(a,q):
    n=a.shape[0]; M=np.concatenate([a%q,np.eye(n,dtype=np.int64)],axis=1)
    for c in range(n):
        r=next(r for r in range(c,n) if M[r,c]%q)
        M[[c,r]]=M[[r,c]]; M[c]=(M[c]*inv_mod(M[c,c],q))%q
        for r in range(n):
            if r!=c and M[r,c]: M[r]=(M[r]-M[r,c]*M[c])%q
    return M[:,n:]
def rank_mod(A,q):
    A=A.copy()%q; r=0; rows,cols=A.shape
    for c in range(cols):
        piv=next((i for i in range(r,rows) if A[i,c]),None)
        if piv is None: continue
        A[[r,piv]]=A[[piv,r]]; A[r]=(A[r]*inv_mod(A[r,c],q))%q
        for i in range(rows):
            if i!=r and A[i,c]: A[i]=(A[i]-A[i,c]*A[r])%q
        r+=1
        if r==rows: break
    return r
def weyl(M,q):
    n=M.shape[0]; w=[None]*n
    R=[[rank_mod(M[:i,j:],q) if i>0 else 0 for j in range(n+1)] for i in range(n+1)]
    for i in range(n):
        # w(i) = max j with R[i+1][j]-R[i][j]==1
        w[i]=max(j for j in range(n) if R[i+1][j]-R[i][j]==1)
    return tuple(w)
def delta(a,b,q): return weyl((a@matinv(b,q))%q,q)
def all_chambers(n,q):
    start=np.eye(n,dtype=np.int64); key=lambda g: canon(g,q).tobytes()
    seen={key(start):canon(start,q)}; frontier=[canon(start,q)]
    gens=[]
    for i in range(n):
        for j in range(n):
            if i!=j:
                E=np.eye(n,dtype=np.int64); E[i,j]=1; gens.append(E)
    while frontier:
        nf=[]
        for g in frontier:
            for E in gens:
                h=canon((g@E)%q,q); k=h.tobytes()
                if k not in seen: seen[k]=h; nf.append(h)
        frontier=nf
    return list(seen.values())
