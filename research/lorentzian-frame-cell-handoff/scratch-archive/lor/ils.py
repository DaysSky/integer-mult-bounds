"""Iterated local search max clique on the compatibility graph (swap moves)."""
import numpy as np, random, pickle, sys, time
def ils(compat, iters=200000, seed=0, init=None, verbose=True):
    N = len(compat); rng = random.Random(seed)
    adj = compat
    inC = np.zeros(N, dtype=bool)
    miss = np.zeros(N, dtype=np.int64)   # number of clique members not adjacent (excluding self)
    def add(v):
        inC[v] = True
        miss[:] += ~adj[v]; miss[v] -= 1  # v not adjacent to itself (diag False) -> fix
    def rem(v):
        inC[v] = False
        miss[:] -= ~adj[v]; miss[v] += 1
    # init
    order = list(range(N)); rng.shuffle(order)
    if init is not None:
        for v in init: add(v)
    else:
        for v in order:
            if not inC[v] and miss[v] == 0: add(v)
    best = list(np.nonzero(inC)[0]); tabu = {}
    t0 = time.time()
    for it in range(iters):
        free = np.nonzero((~inC) & (miss == 0))[0]
        if len(free):
            add(int(rng.choice(free)))
        else:
            one = np.nonzero((~inC) & (miss == 1))[0]
            one = [u for u in one if tabu.get(u, -1) < it]
            if one:
                u = rng.choice(one)
                blockers = np.nonzero(inC & ~adj[u])[0]
                w = int(blockers[0])
                rem(w); tabu[w] = it + 7; add(u)
            else:
                # perturb: remove random member
                mem = np.nonzero(inC)[0]
                w = int(rng.choice(mem)); rem(w); tabu[w] = it + 7
        c = int(inC.sum())
        if c > len(best):
            best = list(np.nonzero(inC)[0])
            if verbose: print('  it', it, 'clique', c, '%.0fs' % (time.time() - t0), flush=True)
    return best
if __name__ == '__main__':
    compat = np.load(sys.argv[1]) if sys.argv[1].endswith('.npy') else pickle.load(open(sys.argv[1], 'rb'))['compat']
    best = ils(compat, int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 0)
    print('BEST', len(best))
    pickle.dump(best, open(sys.argv[1] + '.ils.pkl', 'wb'))
