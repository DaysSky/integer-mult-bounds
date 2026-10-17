import itertools, numpy as np, sys
n=int(sys.argv[1]); L=[]
for i,j in itertools.combinations(range(n),2):
    x=[0]*(n+1); x[i]=1; x[j]=-1; L.append(x)
for t in itertools.combinations(range(n),3):
    x=[0]*(n+1)
    for i in t: x[i]=1
    x[n]=1; L.append(x)
np.save('I%d.npy'%n,np.array(L))
