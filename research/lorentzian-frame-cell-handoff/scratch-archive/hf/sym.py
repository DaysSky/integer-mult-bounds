"""Symmetry group of the 112-port complex unit: signed coordinate permutations preserving the
Hamming tetrads, acting on lines (with orientation sign) and linearly on 9-bit labels."""
from e8 import *
import itertools
TETS=sorted(set(TET))
TSET=set(frozenset(t) for t in TETS)
line_of={}
for t in range(V):
    line_of[tuple(Rr[t])]=(t,1); line_of[tuple(-Rr[t])]=(t,-1)
def perm_ok(pi):  # pi: list, coordinate m -> pi[m]
    return all(frozenset(pi[m] for m in T) in TSET for T in TETS)
def act(pi,eps):
    """returns (perm on lines, sign per line) for x -> (eps * x) permuted: y[pi[m]] = eps[m]*x[m]"""
    pl=[0]*V; sg=[0]*V
    for t in range(V):
        y=[0]*8
        for m in range(8): y[pi[m]]=eps[m]*int(Rr[t,m])
        u,s=line_of[tuple(y)]; pl[t]=u; sg[t]=s
    return pl,sg
def f2solve_matrix(pl):
    """find 9x9 F2 matrix A (as list of column images of basis bits) with A p_t = p_{pl[t]} for all t"""
    # pick 9 independent ports
    idx=[];B=[]
    for t in range(V):
        if len(basis(B+[P[t]]))>len(B): B.append(P[t]); idx.append(t)
        if len(B)==9: break
    # express each unit vector e_j as combination of chosen ports, image = same combination of images
    import itertools
    # Gaussian elimination over F2: build map from span
    rows=[(P[t],P[pl[t]]) for t in idx]
    # reduce to find for each bit j the combination
    img={}
    # solve: represent arbitrary x as xor of subset of P[idx]
    piv={}
    for a,b in rows:
        x,y=a,b
        while x:
            h=x.bit_length()-1
            if h in piv: x^=piv[h][0]; y^=piv[h][1]
            else: piv[h]=(x,y); break
    def apply(x):
        y=0
        while x:
            h=x.bit_length()-1; x^=piv[h][0]; y^=piv[h][1]
        return y
    A=lambda x: apply(x)
    ok=all(apply(P[t])==P[pl[t]] for t in range(V))
    return apply, ok
def group_elements(limit=None):
    perms=[pi for pi in itertools.permutations(range(8)) if perm_ok(pi)]
    return perms
if __name__=='__main__':
    perms=group_elements(); print('tetrad-preserving permutations:',len(perms))
    eps=[1]*8
    bad=0
    for pi in perms[:50]:
        pl,sg=act(pi,eps); A,ok=f2solve_matrix(pl); bad+= (not ok)
        # check N equivariance up to signs
        okN=all(abs(N[pl[t],pl[s]]*sg[t]*sg[s]-N[t,s])<1e-12 for t in range(0,V,7) for s in range(V))
        if not okN: print('N not equivariant'); break
    print('label-linear failures among 50:',bad)
    for m in range(8):
        e=[1]*8; e[m]=-1; pl,sg=act(list(range(8)),e); A,ok=f2solve_matrix(pl)
        print('sign flip',m,'linear on labels:',ok, 'fixes lines:',sum(pl[t]==t for t in range(V)))
