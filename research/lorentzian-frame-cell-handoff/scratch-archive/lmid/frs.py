"""Frame-routable source-system search (own-frame top, R420 mechanism).
State: each line a picks a good 4-frame F(a) containing a.  Arcs a->b for b in F(a)\\{a}; cells = {a,b} for all arcs.
Sections = perp(C) for every cell C that is an arc of some line (own-frame top sections {t,e}-perp).
Unroutable pair (S, u): u in S but no system cell inside S contains u.  Objective = U + lam * defects
(defect = arc a->b with a not in F(b)).  Incremental: cnt[S][u] = #cells inside S containing u.
usage: frs.py START(json|random) iters seed lam T0 tag"""
import sys, os, json, random, math, time, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ['GRP'] = '11'
from lbase import V, bits, HYP, goodframes
pc = lambda m: bin(m).count('1')
START, ITERS, SEED, LAM, T0, TAG = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
random.seed(SEED)
FR = goodframes()
frames_of = collections.defaultdict(list)
for F in FR:
    for s in bits(F): frames_of[s].append(F)
PERP = {}
def perp2(C):
    r = PERP.get(C)
    if r is None:
        a, b = bits(C); r = HYP[a] & HYP[b]; PERP[C] = r
    return r
if START == 'random':
    F = {a: random.choice(frames_of[a]) for a in range(V)}
else:
    F = {int(k): v for k, v in json.load(open(START)).items()}
    for a in range(V):
        if F[a] not in FR:   # system may contain non-frame masks (extra branches); snap to a frame containing a
            F[a] = max(frames_of[a], key=lambda X: pc(X & F[a]))
# ---- derived state
arc_cnt = collections.Counter()      # cell -> number of arcs creating it (1 or 2)
sec_cnt = collections.Counter()      # section-cell -> number of arcs making it a section (same as arc_cnt)
cnt = {}                             # section cell C -> dict u -> #cells inside perp(C) containing u
U = 0
cells = set()
def cells_inside(S):
    return [D for D in cells if D & ~S == 0]
def add_cell(D):
    """cell D appears: update every section containing it"""
    global U
    for C, cu in cnt.items():
        S = perp2(C)
        if D & ~S == 0:
            for u in bits(D):
                if cu[u] == 0: U -= 1
                cu[u] += 1
def rem_cell(D):
    global U
    for C, cu in cnt.items():
        S = perp2(C)
        if D & ~S == 0:
            for u in bits(D):
                cu[u] -= 1
                if cu[u] == 0: U += 1
def add_section(C):
    global U
    S = perp2(C); cu = collections.Counter()
    for D in cells:
        if D & ~S == 0:
            for u in bits(D): cu[u] += 1
    for u in bits(S):
        if cu[u] == 0: U += 1
    cu_full = collections.defaultdict(int, cu)
    cnt[C] = cu_full
def rem_section(C):
    global U
    S = perp2(C); cu = cnt.pop(C)
    for u in bits(S):
        if cu[u] == 0: U -= 1
def arcs_of(a): return [(1 << a) | (1 << b) for b in bits(F[a]) if b != a]
def defects():
    return sum(1 for a in range(V) for b in bits(F[a]) if b != a and not F[b] >> a & 1)
# build
for a in range(V):
    for C in arcs_of(a): arc_cnt[C] += 1
cells = set(arc_cnt)
for C in cells: add_section(C)
DEF = defects()
def obj(): return U + LAM * DEF
print('start U', U, 'defects', DEF, 'cells', len(cells), 'obj', obj(), flush=True)
def set_frame(a, newF):
    """change F[a]; maintain arc_cnt, cells, sections, U, DEF"""
    global DEF
    old = arcs_of(a)
    # defects involving a: arcs a->b and b->a
    def local_def():
        d = 0
        for b in bits(F[a]):
            if b != a and not F[b] >> a & 1: d += 1
        for b in range(V):
            if b != a and F[b] >> a & 1 and not F[a] >> b & 1: d += 1
        return d
    DEF -= local_def()
    for C in old:
        arc_cnt[C] -= 1
        if arc_cnt[C] == 0:
            del arc_cnt[C]; cells.discard(C); rem_section(C); rem_cell(C)
    F[a] = newF
    for C in arcs_of(a):
        if arc_cnt[C] == 0:
            cells.add(C); add_cell(C); add_section(C)
        arc_cnt[C] += 1
    DEF += local_def()
best = obj(); bestF = dict(F); t0 = time.time()
for it in range(ITERS):
    # focus: pick a line involved in an unroutable pair half of the time
    if random.random() < 0.6 and U > 0:
        C = random.choice([C for C, cu in cnt.items() if any(cu[u] == 0 for u in bits(perp2(C)))])
        S = perp2(C)
        u = random.choice([u for u in bits(S) if cnt[C][u] == 0])
        a = u if random.random() < 0.7 else random.choice(bits(C))
    else:
        a = random.randrange(V)
    oldF = F[a]; o0 = obj()
    cand = random.sample(frames_of[a], min(12, len(frames_of[a])))
    bestc = None
    for X in cand:
        if X == oldF: continue
        set_frame(a, X); v = obj()
        if bestc is None or v < bestc[0]: bestc = (v, X)
        set_frame(a, oldF)
    if bestc is None: continue
    T = T0 * (1 - it / ITERS) + 0.05
    if bestc[0] <= o0 or random.random() < math.exp((o0 - bestc[0]) / T):
        set_frame(a, bestc[1])
        if obj() < best:
            best = obj(); bestF = dict(F)
            json.dump({str(k): v for k, v in bestF.items()}, open('frs_best_%s.json' % TAG, 'w'))
    if it % 200 == 0:
        print('it', it, 'U', U, 'def', DEF, 'obj', obj(), 'best', best, '%.0fs' % (time.time() - t0), flush=True)
print('final best', best, flush=True)
