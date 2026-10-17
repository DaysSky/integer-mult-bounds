import numpy as np, sys, time
def ip(A, B):
    # A: (n,10), B: (m,10) doubled E8 coords + (p,q)
    e = (A[:, :8] @ B[:, :8].T) // 4
    u = np.outer(A[:, 8], B[:, 9]) + np.outer(A[:, 9], B[:, 8])
    return e + u
def build(L, blk=2000):
    n = len(L)
    nb = (n + 7)//8
    adj = np.zeros((n, nb), dtype=np.uint8)
    for i in range(0, n, blk):
        G = ip(L[i:i+blk], L)
        ok = (G == 0) | (G % 2 != 0)
        for r in range(G.shape[0]):
            ok[r, i + r] = False
        adj[i:i+blk] = np.packbits(ok, axis=1)
    return adj
if __name__ == '__main__':
    L = np.load(sys.argv[1])
    t = time.time(); A = build(L); print('built', A.shape, time.time()-t)
    np.save(sys.argv[1].replace('cand', 'adj'), A)
    deg = np.unpackbits(A, axis=1, count=len(L)).sum(1)
    print('deg min/mean/max', deg.min(), deg.mean(), deg.max())
