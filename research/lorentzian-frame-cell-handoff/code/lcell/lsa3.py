"""Fast local search on the refined free-top cell bound R_lb2 (valid relaxation; see lscore2) over Z11 good-frame
systems, with per-cell context caching (r_C depends only on C and the other cells of its two lines).
usage: lsa3.py START.json iters seed T0 [tag]"""
import sys, os, json, random, math
os.environ['GRP'] = '11'
from lbase import *
fr = goodframes()
covers = {a: [F & ~(1 << a) for F in fr if F >> a & 1] for a in range(V)}
rep_of = {a: min(p[a] for p in PERMS) for a in range(V)}
reps = sorted(set(rep_of.values()))
pmap = {a: next(p for p in PERMS if p[rep_of[a]] == a) for a in range(V)}
PERP = {}
def perpm(m):
    if m not in PERP: PERP[m] = perp(m)
    return PERP[m]
NODE = {}
def node_perps(C):
    if C not in NODE:
        ps = set()
        for x in range(V):
            if not C >> x & 1: ps.add(perpm(closure(C | (1 << x))))
        NODE[C] = sorted(ps, key=lambda q: -bin(q).count('1'))
    return NODE[C]
pc_ = lambda m: bin(m).count('1')
RC = {}
def r_cell(C, os_, oa_):
    key = (C, os_, oa_)
    if key in RC: return RC[key]
    PC = perpm(C); Fs = PC & ~os_; Fa = PC & ~oa_
    D = Fs & Fa; S = Fs & ~Fa; A = Fa & ~Fs
    best = None
    if not (D | S | A): best = 0
    else:
        nps = node_perps(C)
        for q1 in nps:
            d1 = pc_(D & ~q1); s1 = pc_(S & ~q1); a1 = pc_(A & ~q1)
            if best is not None and d1 >= best: continue
            for q2 in nps:
                u = min(d1 + pc_(S & ~(q1 | q2)) + a1, d1 + s1 + pc_(A & ~(q1 | q2)), pc_(D & ~(q1 & q2)) + s1 + pc_(A & ~q2))
                if best is None or u < best: best = u
                if best == 0: break
            if best == 0: break
    RC[key] = best; return best
def system(choice):
    return {a: act(covers[rep_of[a]][choice[rep_of[a]]], pmap[a]) for a in range(V)}
def score(choice):
    cov = system(choice)
    defects = sum(1 for a in range(V) for b in bits(cov[a]) if not cov[b] >> a & 1)
    cells = set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a]))
    cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
    ops = {s: 0 for s in range(V)}
    rs = []
    for C in cells:
        s, a = list(bits(C))
        os_ = 0
        for c in cells_of[s]:
            if c != C: os_ |= perpm(c)
        oa_ = 0
        for c in cells_of[a]:
            if c != C: oa_ |= perpm(c)
        rs.append(r_cell(C, os_, oa_))
    free0 = sum(1 for r in rs if r == 0); pool = V; cnt = 0
    for r in sorted(r for r in rs if r > 0):
        if pool >= r: pool -= r; cnt += 1
    jlb = len(cells) - free0 - cnt
    return 440 + defects + jlb, defects, jlb
if __name__ == '__main__':
    start = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
    choice = {r: covers[r].index(start[r]) for r in reps}
    iters, seed, T0 = int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]); tag = sys.argv[5] if len(sys.argv) > 5 else str(seed)
    random.seed(seed)
    cur = score(choice); best = cur
    print('start', cur, flush=True)
    for it in range(iters):
        r = random.choice(reps); old = choice[r]; choice[r] = random.randrange(len(covers[r]))
        new = score(choice); T = T0 * (1 - it / iters) + 0.05
        if new[0] <= cur[0] or random.random() < math.exp((cur[0] - new[0]) / T):
            cur = new
            if new[0] < best[0]:
                best = new
                json.dump({str(a): v for a, v in system(choice).items()}, open('lsa3_best_%s.json' % tag, 'w'))
                print('it', it, 'best', best, flush=True)
        else: choice[r] = old
        if it % 200 == 0: print('it', it, 'cur', cur, 'cache', len(RC), flush=True)
    print('final best', best, flush=True)
