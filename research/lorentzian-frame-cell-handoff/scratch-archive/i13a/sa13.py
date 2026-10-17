"""How aligned can an I_{13,1} good-frame partition be?  Score = number of compatible (unordered) frame pairs in the
partition (strict alignment = all C(91,2) = 4095 pairs).  Start: PG(2,3) partition.  Moves: pick 2-3 frames, free
their 8-12 lines, re-cover the freed lines with good frames inside them (exhaustive over exact covers of the freed set),
accept by simulated annealing.  Reports the best score and the frame-mate fraction (alignment of demands)."""
import sys, pickle, itertools, random, numpy as np, time, collections
frames, comp_lists, kinds = pickle.load(open('compat13.pkl', 'rb'))
fidx = {tuple(sorted(q)): i for i, q in enumerate(frames)}
part = [fidx[tuple(sorted(f))] for f in pickle.load(open('pg23_partition.pkl', 'rb'))]
nf = len(frames)
def comp(a, b):
    arr = comp_lists[a]; k = np.searchsorted(arr, b); return k < len(arr) and arr[k] == b
by_line = collections.defaultdict(list)
for i, q in enumerate(frames):
    for l in q: by_line[l].append(i)
def score(P):
    return sum(comp(a, b) for a, b in itertools.combinations(P, 2))
def contrib(f, P):
    return sum(comp(f, b) for b in P if b != f)
def covers(lines):
    """all exact covers of a small line set by good frames inside it"""
    lines = set(lines)
    if not lines: yield []; return
    u = min(lines)
    for j in by_line[u]:
        q = set(frames[j])
        if q <= lines:
            for rest in covers(lines - q): yield [j] + rest
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
P = list(part); cur = score(P); best = cur; bestP = list(P)
print('PG(2,3) partition: compatible pairs %d / 4095' % cur, flush=True)
T0 = 3.0; t0 = time.time(); iters = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
for it in range(iters):
    k = random.choice((2, 2, 3))
    sel = random.sample(range(len(P)), k)
    freed = [l for i in sel for l in frames[P[i]]]
    others = [P[i] for i in range(len(P)) if i not in sel]
    old = sum(contrib(P[i], others) for i in sel) + sum(comp(P[a], P[b]) for a, b in itertools.combinations(sel, 2))
    opts = list(itertools.islice(covers(freed), 400))
    if len(opts) <= 1: continue
    new_c = random.choice(opts)
    new = sum(contrib(j, others) for j in new_c) + sum(comp(a, b) for a, b in itertools.combinations(new_c, 2))
    T = T0 * (1 - it / iters) + 0.05
    if new >= old or random.random() < np.exp((new - old) / T):
        P = others + new_c; cur += new - old
        if cur > best: best = cur; bestP = list(P)
    if it % 2000 == 0: print('it %d cur %d best %d (%.0fs)' % (it, cur, best, time.time() - t0), flush=True)
print('best compatible pairs %d / 4095' % best)
pickle.dump([frames[i] for i in bestP], open('sa13_best.pkl', 'wb'))
