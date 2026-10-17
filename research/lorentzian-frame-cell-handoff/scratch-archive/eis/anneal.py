"""Simulated annealing for a cheap fitting F2 decoder on the 40 Eisenstein lines."""
import pickle, random, math, sys, time
d = pickle.load(open('eis.pkl', 'rb'))
n = d['n']; nonorth = d['nonorth']; table = d['table'].tolist(); cost = d['cost'].tolist()
FULL = (1 << n) - 1

def closure(mask):
    f = 0
    while mask:
        b = mask & -mask; t = b.bit_length() - 1; mask ^= b
        f = table[f][t]
    return f

def rowviol(t, row):
    return (0 if row >> t & 1 else 1) + (row & nonorth[t]).bit_count()

def run(nrect, steps, seed, lam0=1.0, lam1=60.0, T0=1.0, T1=0.02, init='rows'):
    rng = random.Random(seed)
    p = [0] * nrect; q = [0] * nrect
    # init: random sparse
    if init == 'rows':
        for t in range(min(n, nrect)):
            p[t] = 1 << t; q[t] = 1 << t
    else:
        for j in range(nrect):
            p[j] = rng.getrandbits(n) & rng.getrandbits(n) & rng.getrandbits(n)
            q[j] = rng.getrandbits(n) & rng.getrandbits(n) & rng.getrandbits(n)
    fp = [closure(x) for x in p]; fq = [closure(x) for x in q]
    rc = [cost[fp[j]][fq[j]] for j in range(nrect)]
    B = [0] * n
    for j in range(nrect):
        m = p[j]
        while m:
            b = m & -m; t = b.bit_length() - 1; m ^= b
            B[t] ^= q[j]
    viol = sum(rowviol(t, B[t]) for t in range(n))
    C = sum(rc)
    best = None
    for step in range(steps):
        fr = step / steps
        lam = lam0 * (lam1 / lam0) ** fr
        T = T0 * (T1 / T0) ** fr
        j = rng.randrange(nrect)
        x = rng.randrange(n)
        if rng.random() < 0.5:
            # flip x in p[j]: row x toggles by q[j]
            newp = p[j] ^ (1 << x)
            nf = closure(newp) if not (newp >> x & 1) else table[fp[j]][x]
            nc = cost[nf][fq[j]]
            old = rowviol(x, B[x]); new = rowviol(x, B[x] ^ q[j])
            dv = new - old; dc = nc - rc[j]
            dE = dc + lam * dv
            if dE <= 0 or rng.random() < math.exp(-dE / T):
                p[j] = newp; fp[j] = nf; rc[j] = nc; B[x] ^= q[j]; viol += dv; C += dc
        else:
            newq = q[j] ^ (1 << x)
            nf = closure(newq) if not (newq >> x & 1) else table[fq[j]][x]
            nc = cost[fp[j]][nf]
            dv = 0
            m = p[j]
            bit = 1 << x
            while m:
                b = m & -m; t = b.bit_length() - 1; m ^= b
                dv += rowviol(t, B[t] ^ bit) - rowviol(t, B[t])
            dc = nc - rc[j]
            dE = dc + lam * dv
            if dE <= 0 or rng.random() < math.exp(-dE / T):
                q[j] = newq; fq[j] = nf; rc[j] = nc; viol += dv; C += dc
                m = p[j]
                while m:
                    b = m & -m; t = b.bit_length() - 1; m ^= b
                    B[t] ^= bit
        if viol == 0 and (best is None or C < best[0]):
            best = (C, list(p), list(q))
    return best, C, viol

if __name__ == '__main__':
    nrect = int(sys.argv[1]); steps = int(sys.argv[2]); seeds = int(sys.argv[3]); init = sys.argv[4] if len(sys.argv) > 4 else 'rows'
    overall = None
    t0 = time.time()
    for s in range(seeds):
        best, C, viol = run(nrect, steps, s, init=init)
        print('seed', s, 'final C', C, 'viol', viol, 'best feasible', best[0] if best else None, 'time %.0f' % (time.time() - t0), flush=True)
        if best and (overall is None or best[0] < overall[0]):
            overall = best
            pickle.dump(overall, open('best_%d.pkl' % nrect, 'wb'))
    print('OVERALL', overall[0] if overall else None)
