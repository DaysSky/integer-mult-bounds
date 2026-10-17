import sys, pickle, random, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V
good = pickle.load(open('good4.pkl', 'rb'))
inc = collections.defaultdict(list)
for i, q in enumerate(good):
    for u in q: inc[u].append(i)
best = None
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
for it in range(400):
    free = set(range(V)); chosen = []
    while True:
        # pick the free line with fewest available frames
        cand = None
        for u in free:
            av = [i for i in inc[u] if all(x in free for x in good[i])]
            if not av: continue
            if cand is None or len(av) < cand[0] or (len(av) == cand[0] and rng.random() < 0.3): cand = (len(av), u, av)
        if cand is None: break
        i = rng.choice(cand[2]); chosen.append(good[i]); free -= set(good[i])
    if best is None or len(free) < len(best[1]): best = (chosen, sorted(free)); print(it, 'uncovered', len(free), flush=True)
    if len(free) <= 4: break
pickle.dump(best, open('greedypart.pkl', 'wb'))
print('frames', len(best[0]), 'uncovered', [(g.kind[u], g.supp[u]) for u in best[1]])
