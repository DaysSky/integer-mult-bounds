import sys, numpy as np
sys.path.insert(0,'.')
from geo import *
K0=list(range(8)); live=[T for T in range(NL) if T not in K0]; n=len(live)
Gl=G[np.ix_(live,live)]; U=U9[live]%2
F2gram=(U@U.T)%2            # complex label form; =1 on Q-orthogonal pairs (and diagonal)
A=[[1 if G[live[i],f]!=0 else 0 for i in range(n)] for f in K0]
A=np.array(A).T              # n x 8 membership
B=(A@A.T)%2
diag_ok=all(B[i,i]==1 for i in range(n))
viol=sum(1 for i in range(n) for j in range(n) if i!=j and F2gram[i,j]==1 and B[i,j]!=0)
print('F2 frame decoder: diag ok',diag_ok,'pattern violations',viol)
# rows identical classes
rows={}
for i in range(n): rows.setdefault(B[i].tobytes(),[]).append(i)
print('distinct rows',len(rows),'class sizes',sorted(set(len(v) for v in rows.values())))
