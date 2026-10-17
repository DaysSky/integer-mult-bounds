"""Randomised most-constrained-line greedy for an aligned good-frame partition of I_{13,1}.
State: allowed[j] = frame j disjoint from chosen lines and compatible with every chosen frame.  Pick the uncovered line
with the fewest allowed frames; choose among them (randomised by score = |allowed after|) .  Report max lines covered."""
import sys, pickle, numpy as np, time
frames, comp_lists, kinds = pickle.load(open('compat13.pkl', 'rb'))
F = np.array(frames); nf = len(F); V = 364
t0 = time.time()
C = np.zeros((nf, (nf + 7) // 8), dtype=np.uint8)
for i, js in enumerate(comp_lists):
    row = np.zeros(nf, dtype=bool); row[js] = True; C[i] = np.packbits(row)
print('compat matrix built %.0fs' % (time.time() - t0), flush=True)
member = np.zeros((V, nf), dtype=bool)
for j in range(nf):
    for u in F[j]: member[u, j] = True
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
best = 0; best_sol = None
runs = int(sys.argv[2]) if len(sys.argv) > 2 else 20
for run in range(runs):
    allowed = np.ones(nf, dtype=bool); covered = np.zeros(V, dtype=bool); chosen = []
    while True:
        unc = np.nonzero(~covered)[0]
        if len(unc) == 0: break
        cnt = (member[unc] & allowed).sum(1)
        if cnt.min() == 0: break
        u = unc[np.argmin(cnt + rng.random(len(cnt)) * 0.5)]
        opts = np.nonzero(member[u] & allowed)[0]
        if len(opts) > 40: opts = rng.choice(opts, 40, replace=False)
        scores = []
        for j in opts:
            a2 = allowed & np.unpackbits(C[j])[:nf].astype(bool)
            scores.append(a2.sum())
        scores = np.array(scores, float) * (1 + 0.1 * rng.random(len(scores)))
        j = opts[int(np.argmax(scores))]
        chosen.append(j); covered[F[j]] = True
        allowed &= np.unpackbits(C[j])[:nf].astype(bool)
        allowed[member[F[j]].any(0)] = False
    ncov = int(covered.sum())
    if ncov > best: best = ncov; best_sol = list(chosen)
    print('run %d: frames %d covered %d / 364 (best %d) %.0fs' % (run, len(chosen), ncov, best, time.time() - t0), flush=True)
    if ncov == V:
        print('ALIGNED PARTITION FOUND'); break
pickle.dump(best_sol, open('greedy13_best.pkl', 'wb'))
