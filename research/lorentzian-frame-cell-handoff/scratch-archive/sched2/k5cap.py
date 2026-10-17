import sys
sys.argv = ['x']
exec(open('kbound.py').read().split('def vecs(K):')[0])
def parts(n, k, mx):
    if k == 0:
        if n == 0: yield ()
        return
    for x in range(min(n - (k - 1), mx), 0, -1):
        for rest in parts(n - x, k - 1, x): yield (x,) + rest
K = int(sys.argv[1]) if len(sys.argv) > 1 else 5
for K, Ns, mx in ((5, (12, 13, 14), 10),):
    s = 2 * K + 1; tot = (K - 1) * s
    for N in Ns:
        best = None; n = 0
        for pt in parts(tot, N, mx):
            n += 1
            q = ub(K, pt)
            if best is None or q > best[0]: best = (q, pt)
        print('K', K, 'stretches', N, 'rigorous max %+.3f%%' % float((best[0] / ref - 1) * 100), best[1], 'multisets', n, flush=True)
