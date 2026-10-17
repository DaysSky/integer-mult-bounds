"""D4-type W in T^perp: W^perp is a D4 containing T, spanned by an orthogonal 4-frame {T,a,b,c}.
lines(W) = lines orthogonal to T,a,b,c.  Keep W with 12 lines (then W is a D4 too)."""
import pickle, itertools, numpy as np
d=pickle.load(open('../k2/e8f.pkl','rb')); G=d['GL']; n=120
Z=(G==0)
res={}
for T in range(n):
    E=[S for S in range(n) if Z[T,S]]
    Ws=set()
    for a,b,c in itertools.combinations(E,3):
        if Z[a,b] and Z[a,c] and Z[b,c]:
            W=frozenset(np.nonzero(Z[T]&Z[a]&Z[b]&Z[c])[0].tolist())
            if len(W)==12: Ws.add(W)
    res[T]=sorted(Ws,key=sorted)
print('per-line counts',sorted(set(len(v) for v in res.values())))
pickle.dump(res,open('subs_D4.pkl','wb'))
