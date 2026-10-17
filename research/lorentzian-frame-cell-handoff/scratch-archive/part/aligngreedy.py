# Randomised greedy: largest family of pairwise disjoint, pairwise compatible good frames (aligned partition with
# the uncovered lines punctured).  Heuristic lower bound on the coverage of an aligned partition.
import pickle, random, numpy as np, time, sys
good = pickle.load(open('good4.pkl', 'rb')); comp = pickle.load(open('compat.pkl', 'rb')); n = len(good)
print('loaded', flush=True); compset = [set(c.tolist()) for c in comp]; print('sets built', flush=True)
byline = {}
for i, q in enumerate(good):
    for x in q: byline.setdefault(x, []).append(i)
rng = random.Random(int(sys.argv[1])); best = 0; t0 = time.time()
while time.time() - t0 < float(sys.argv[2]):
    order = list(range(n)); rng.shuffle(order)
    chosen = []; used = set(); allowed = None
    for i in order:
        if used & set(good[i]): continue
        if allowed is not None and i not in allowed: continue
        chosen.append(i); used |= set(good[i])
        allowed = compset[i] if allowed is None else (allowed & compset[i])
        if not allowed: break
    if len(used) > best:
        best = len(used); print('covered', best, 'frames', len(chosen), 'punctured', 220 - best, '%.0fs' % (time.time() - t0), flush=True)
