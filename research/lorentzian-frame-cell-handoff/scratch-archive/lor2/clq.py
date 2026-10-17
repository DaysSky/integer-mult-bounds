import numpy as np, sys, time
rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 0)
A = np.load(sys.argv[1]); n = A.shape[0]
POP = np.array([bin(i).count('1') for i in range(256)], dtype=np.int32)
def pc(rows):  # popcount of each row (2D uint8)
    return POP[rows].sum(-1)
def unpack(b): return np.flatnonzero(np.unpackbits(b, count=n))
def greedy(start=None, sample=400, temp=0.0):
    C = []
    cand = np.full(A.shape[1], 255, dtype=np.uint8)
    # mask tail bits
    tail = A.shape[1]*8 - n
    if tail: cand[-1] &= (0xFF << tail) & 0xFF
    if start is not None:
        for s in start:
            C.append(s); cand &= A[s]
    while True:
        idx = unpack(cand)
        if len(idx) == 0: break
        S = idx if len(idx) <= sample else rng.choice(idx, sample, replace=False)
        sc = pc(A[S] & cand)
        if temp > 0:
            w = np.exp((sc - sc.max())/temp); v = S[rng.choice(len(S), p=w/w.sum())]
        else:
            v = S[np.argmax(sc + rng.random(len(S)))]
        C.append(int(v)); cand &= A[v]
    return C
def improve(C, iters=2000):
    # (1,1)-swaps / plateau search: vertices with exactly one conflict in C
    C = list(C)
    Cset = set(C)
    best = list(C)
    tabu = {}
    for it in range(iters):
        Cb = np.zeros(A.shape[1], dtype=np.uint8)
        # count conflicts: for each vertex, number of C members not adjacent
        Ab = np.unpackbits(A[C], axis=1, count=n)  # |C| x n
        conf = len(C) - Ab.sum(0)
        conf[C] = 99
        add = np.flatnonzero(conf == 0)
        if len(add):
            v = int(rng.choice(add)); C.append(v); Cset.add(v)
            if len(C) > len(best): best = list(C)
            continue
        one = np.flatnonzero(conf == 1)
        one = [u for u in one if tabu.get(int(u), -1) < it]
        if not one: break
        u = int(rng.choice(one))
        # find its conflict
        nb = Ab[:, u]
        j = int(np.flatnonzero(nb == 0)[0]); w = C[j]
        C[j] = u; Cset.discard(w); Cset.add(u); tabu[w] = it + 7
    return best
if __name__ == '__main__':
    best = []
    t0 = time.time()
    for r in range(int(sys.argv[3]) if len(sys.argv) > 3 else 10):
        C = greedy(temp=float(sys.argv[4]) if len(sys.argv) > 4 else 0.0)
        C2 = improve(C, 3000)
        print('run', r, 'greedy', len(C), 'improved', len(C2), 'time %.0f' % (time.time()-t0), flush=True)
        if len(C2) > len(best):
            best = C2; np.save(sys.argv[1].replace('adj', 'best'), np.array(best))
    print('best', len(best))
