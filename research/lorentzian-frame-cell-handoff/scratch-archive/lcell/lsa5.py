"""Z11 local search for a source system that ADMITS the own-frame top (every u in R(t) has a source cell inside one
of t's own 3 sections), objective = 1000*no_route + defects.  Then report the frame-top screen.
usage: lsa5.py START.json iters seed T0 tag"""
import sys, os, json, random, math
os.environ['GRP'] = '11'
import lsa3
from lbase import V, bits, HYP, act
covers, reps, rep_of, pmap, perpm = lsa3.covers, lsa3.reps, lsa3.rep_of, lsa3.pmap, lsa3.perpm
def system(choice): return {a: act(covers[rep_of[a]][choice[rep_of[a]]], pmap[a]) for a in range(V)}
def score(choice):
    cov = system(choice)
    defects = sum(1 for a in range(V) for b in bits(cov[a]) if not cov[b] >> a & 1)
    cells = set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a]))
    cells_of = {s: [] for s in range(V)}
    for C in cells:
        for s in bits(C): cells_of[s].append(C)
    nr = 0
    for t in reps:                      # Z11: count on reps, x11
        own = [perpm((1 << t) | (1 << f)) for f in bits(cov[t])]
        for u in bits(HYP[t]):
            if not any(c & ~S == 0 for S in own for c in cells_of[u]): nr += 1
    return 1000 * nr + defects, nr * 11, defects
start = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
choice = {r: covers[r].index(start[r]) for r in reps}
iters, seed, T0, tag = int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
random.seed(seed); cur = score(choice); best = cur; print('start', cur, flush=True)
for it in range(iters):
    r = random.choice(reps); old = choice[r]; choice[r] = random.randrange(len(covers[r]))
    new = score(choice); T = T0 * (1 - it / iters) + 0.5
    if new[0] <= cur[0] or random.random() < math.exp((cur[0] - new[0]) / T):
        cur = new
        if new[0] < best[0]:
            best = new; json.dump({str(a): v for a, v in system(choice).items()}, open('lsa5_best_%s.json' % tag, 'w'))
            print('it', it, 'best', best, flush=True)
    else: choice[r] = old
print('final best', best, flush=True)
