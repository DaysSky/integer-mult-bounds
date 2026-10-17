exec(open('pen5gen.py').read().split("best=1e9")[0])
sh=[((0, 1, 8, 9, 10, 11), (2, 3, 4, 5, 6, 7)), ((2, 3, 8, 9, 10, 11), (0, 1, 4, 5, 6, 7)), ((0, 1, 4, 5, 6, 7), (2, 3, 8, 9, 10, 11)), ((2, 3, 4, 5, 6, 7), (0, 1, 8, 9, 10, 11))]
# class A = halves 0,1 (lines 0-3). Require within A exact (=N), within B,C = 0 (automatic: uncovered)
W2=W.copy()
for i in range(12):
    for j in range(12):
        if hid[L[i]]!=hid[L[j]] and cls[hid[L[i]]]==cls[hid[L[j]]]:
            W2[i,j]=1.0
            if cls[hid[L[i]]]!=cls[0]: T[i,j]=0.0
W=W2
res=[fit(sh,800) for _ in range(6)]
print('residual with designated-class within exact:',min(res))
# also check: within entries of classes B,C uncovered by these shapes
cov=np.zeros((12,12))
for S,Q in sh: cov[np.ix_(list(Q),list(S))]=1
print('covered within entries per class:', {c:int(sum(cov[i,j] for i in range(12) for j in range(12) if hid[L[i]]!=hid[L[j]] and cls[hid[L[i]]]==cls[hid[L[j]]]==c)) for c in set(cls.values())})
