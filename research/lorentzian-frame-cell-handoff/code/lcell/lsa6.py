"""[lsa6: defect-repair moves] NON-SYMMETRIC local search (each line picks its own good frame) on the refined free-top bound R_lb2.
Reuses lsa3's cached per-cell r_C.  usage: lsa4.py START.json iters seed T0 tag"""
import sys, os, json, random, math
os.environ['GRP'] = '11'
import lsa3
from lbase import V, bits
covers = lsa3.covers
def score(cov):
    defects = sum(1 for a in range(V) for b in bits(cov[a]) if not cov[b] >> a & 1)
    cells = set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a]))
    cells_of = {s: [] for s in range(V)}
    for C in cells:
        for s in bits(C): cells_of[s].append(C)
    rs = []
    for C in cells:
        s, a = list(bits(C))
        os_ = 0
        for c in cells_of[s]:
            if c != C: os_ |= lsa3.perpm(c)
        oa_ = 0
        for c in cells_of[a]:
            if c != C: oa_ |= lsa3.perpm(c)
        rs.append(lsa3.r_cell(C, os_, oa_))
    free0 = sum(1 for r in rs if r == 0); pool = 0 if os.environ.get('NOREADS') == '1' else int(os.environ.get('POOL', V)); cnt = 0
    for r in sorted(r for r in rs if r > 0):
        if pool >= r: pool -= r; cnt += 1
    jlb = len(cells) - free0 - cnt
    return 440 + defects + jlb, defects, jlb
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
iters, seed, T0, tag, K = int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5], 8
random.seed(seed)
cur = score(cov); best = cur; print('start', cur, flush=True)
for it in range(iters):
    defects = [(a, b) for a in range(V) for b in bits(cov[a]) if not cov[b] >> a & 1]
    if defects and random.random() < 0.5:
        a, b = random.choice(defects)
        if random.random() < 0.5:
            x = b; cands = [c for c in covers[b] if c >> a & 1]
        else:
            x = a; cands = [c for c in covers[a] if not c >> b & 1]
        random.shuffle(cands); cands = cands[:K]
        old = cov[x]; bestc = None
        for c in cands:
            cov[x] = c; sc = score(cov)
            if bestc is None or sc[0] < bestc[0]: bestc = (sc[0], c, sc)
        cov[x] = old
        if bestc is None: continue
        new = bestc[2]; T = T0 * (1 - it / iters) + 0.05
        if new[0] <= cur[0] or random.random() < math.exp((cur[0] - new[0]) / T):
            cov[x] = bestc[1]; cur = new
    else:
        x = random.randrange(V); old = cov[x]; cov[x] = random.choice(covers[x])
        new = score(cov); T = T0 * (1 - it / iters) + 0.05
        if new[0] <= cur[0] or random.random() < math.exp((cur[0] - new[0]) / T): cur = new
        else: cov[x] = old
    if cur[0] < best[0]:
        best = cur; json.dump({str(k): v for k, v in cov.items()}, open('lsa6_best_%s.json' % tag, 'w'))
        print('it', it, 'best', best, flush=True)
    if it % 500 == 0: print('it', it, 'cur', cur, flush=True)
print('final best', best, flush=True)
