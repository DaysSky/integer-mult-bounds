import numpy as np, sys
A = np.load(sys.argv[1]); n = len(A)
with open(sys.argv[2], 'w') as f:
    f.write('%d\n' % n)
    for i in range(n): f.write(' '.join(map(str, np.nonzero(A[i])[0])) + '\n')
