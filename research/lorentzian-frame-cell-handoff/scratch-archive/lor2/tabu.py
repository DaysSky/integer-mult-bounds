"""Tabu search for maximum clique (MN/TS style) on a packed-bitset graph."""
import numpy as np, sys, time
def run(A, n, seed, iters, init=None, log=None, L=None, tt=10):
    rng = np.random.default_rng(seed)
    nonadj = lambda v: 1 - np.unpackbits(A[v], count=n).astype(np.int32)
    conf = np.zeros(n, dtype=np.int32)
    inC = np.zeros(n, dtype=bool)
    C = []
    def add(v):
        nonlocal conf
        na = nonadj(v); na[v] = 0
        conf += na; inC[v] = True; C.append(v)
    def drop(v):
        nonlocal conf
        na = nonadj(v); na[v] = 0
        conf -= na; inC[v] = False; C.remove(v)
    if init is not None:
        for v in init: add(int(v))
    best = list(C); tabu = np.full(n, -1, dtype=np.int64)
    t0 = time.time()
    for it in range(iters):
        free = (~inC) & (conf == 0) & (tabu < it)
        PA = np.flatnonzero(free)
        if len(PA):
            # choose add maximizing future PA size approx: random among
            v = int(rng.choice(PA)); add(v)
        else:
            OM = np.flatnonzero((~inC) & (conf == 1) & (tabu < it))
            if len(OM) and rng.random() < 0.9:
                u = int(rng.choice(OM))
                row = np.unpackbits(A[u], count=n)
                Cw = [w for w in C if not row[w]]
                w = Cw[0]
                drop(w); add(u); tabu[w] = it + tt + rng.integers(0, 5)
            else:
                if not C: continue
                w = C[int(rng.integers(len(C)))]
                drop(w); tabu[w] = it + 7
        if len(C) > len(best):
            best = list(C)
            if log: print('  it', it, 'size', len(best), '%.0fs' % (time.time()-t0), flush=True)
    return best
if __name__ == '__main__':
    A = np.load(sys.argv[1]); n = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != '-' else None
    if n is None:
        n = A.shape[1]*8
        cand = sys.argv[1].replace('adj', 'cand'); n = len(np.load(cand))
    seed = int(sys.argv[3]); iters = int(sys.argv[4])
    init = None
    if len(sys.argv) > 5:
        init = np.load(sys.argv[5])
    b = run(A, n, seed, iters, init=init, log=True)
    out = sys.argv[1].replace('adj', 'tabu%d' % seed)
    np.save(out, np.array(b)); print('final', len(b), out)
