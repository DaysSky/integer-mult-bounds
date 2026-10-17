"""Dual-guided search for minrank-11 line sets that improve the clique + minrank-11 hitting LP.
Given dual weights y_L on flat orbits (from the current LP), a family orbit of Y improves the LP iff
  score(Y) = sum_L y_L * Pr_sigma[sigma(Y) meets L]  <  11        (sigma uniform in S11).
Search: start from a random 10-clique Q, greedily add lines that keep the Monte-Carlo score low until the
minrank reaches 11 (SAT), then shrink.  Prints candidates with their estimated scores; saves them to mr11_cg_SEED.pkl
for the certified LP.  usage: colgen.py DUALS.pkl NTRIALS SEED NSAMPLE"""
import sys, pickle, random, numpy as np, time
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/'
sys.path.insert(0, D); sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
from mrlib import mr_le10, C10
duals = pickle.load(open(sys.argv[1], 'rb'))      # list of (y, line-index tuple of the flat rep)
NT, seed, NS = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); rnd = random.Random(seed)
LINES = {tuple(sorted(g.supp[x])): x for x in range(V)}
perms = [np.random.default_rng(seed * 7919 + k).permutation(11) for k in range(NS)]
img = np.zeros((NS, V), dtype=np.int32)              # img[k, x] = line index of sigma_k(x)
for k, p in enumerate(perms):
    for x in range(V): img[k, x] = LINES[tuple(sorted(int(p[i]) for i in g.supp[x]))]
FL = [(y, np.isin(np.arange(V), np.array(cl))) for y, cl in duals]
def score(Y):
    I = img[:, list(Y)]                               # NS x |Y| images
    return sum(y * float(fm[I].any(axis=1).mean()) for y, fm in FL)
out = []; t0 = time.time()
for trial in range(NT):
    Q = list(rnd.choice(C10)); Y = list(Q)
    while mr_le10(Y, Q):
        cand = rnd.sample([x for x in range(V) if x not in Y], 40)
        best = min(cand, key=lambda x: score(Y + [x])); Y.append(best)
        if len(Y) > 60: break
    if mr_le10(Y, Q): continue
    for x in sorted([z for z in Y if z not in Q], key=lambda z: -score(Y) + score([w for w in Y if w != z])):
        Y2 = [z for z in Y if z != x]
        if not mr_le10(Y2, Q): Y = Y2
    sc = score(Y); out.append((tuple(sorted(Y)), tuple(sorted(Q)), sc))
    print('trial %d |Y| %d score %.3f (improving if < 11)  %.0fs' % (trial, len(Y), sc, time.time() - t0), flush=True)
    pickle.dump([(a, b) for a, b, c in out], open(D + 'mr11_cg_%d.pkl' % seed, 'wb'))
