"""(hierarchical-piece variant)  BUILD an I_{11,1} word on a PARITY top of plane sections (A3/TT*-type triples, defect <= 1).
Step 2: CP-SAT picks one triple per target (from a3_triples.pkl) minimising #distinct planes + #distinct defect lines.
Step 3: every used plane Q gives one section sum sigma(Q-perp) (identical for all its users) assembled by a shared-
piece middle (flats inside sections, reused across sections; exact lw.frame_alg), copied once per delivery.  Targets:
chain 0 -> {d} (read the keeper copy of the defect line, shared by all targets with that defect) -> t-perp (read the 3
section deliveries).  Decoder totals as lmid/build3.py.  usage: build_a3.py OUT.json.gz [TL_seconds]"""
import sys, os, pickle, collections, itertools, time, heapq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lmid'))
import lw
from lw import V, g, bits, LWord, frame_alg, FULL, nondegenerate
from fastcl import fclosure
from ortools.sat.python import cp_model
HYP = g.HYP
pc = lambda m: bin(m).count('1')
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
OUT = sys.argv[1]; TL = float(sys.argv[2]) if len(sys.argv) > 2 else 300
TR = pickle.load(open('a3_triples.pkl', 'rb'))
PM = {}
def pm(m):
    r = PM.get(m)
    if r is None:
        r = FULL
        for s in bits(m): r &= HYP[s]
        PM[m] = r
    return r
# ---- step 2: selection (cached in a3_choice.pkl)
CH = os.environ.get('CHOICE', 'a3_choice.pkl')
planes = sorted({Q for t in TR for tr in TR[t] for Q in tr[:3]})
pid = {Q: i for i, Q in enumerate(planes)}
if os.path.exists(CH): choice = pickle.load(open(CH, 'rb'))
else: choice = None
INCH = int(os.environ.get('INCHAIN', '0'))
if choice is None:
    # Z11-equivariant selection: choose a triple per orbit representative, rotate
    nn = 11
    def img_line(s0, perm): return g.idx[(g.kind[s0], tuple(sorted(perm[i] for i in g.supp[s0])))]
    rot = [img_line(s0, [(i + 1) % nn for i in range(nn)]) for s0 in range(V)]
    rotp = [list(range(V))]
    for k in range(1, nn): rotp.append([rot[x] for x in rotp[-1]])
    def rotm(m, k):
        r = 0
        for s0 in bits(m): r |= 1 << rotp[k % nn][s0]
        return r
    orb = {}; reps = []
    for s0 in range(V):
        if s0 in orb: continue
        reps.append(s0); x0 = s0
        for k in range(nn): orb[x0] = (len(reps) - 1, k); x0 = rot[x0]
    porb = {}
    def plane_orbit(Q):
        r = porb.get(Q)
        if r is None:
            r = min(rotm(Q, k) for k in range(nn)); porb[Q] = r
        return r
    M = cp_model.CpModel(); yo = {}; do = {}; X = {}; bonus = []
    def yvar(O):
        if O not in yo: yo[O] = M.NewBoolVar('')
        return yo[O]
    def dvar(D):
        if D not in do: do[D] = M.NewBoolVar('')
        return do[D]
    for r in reps:
        xs = []
        for k, (a, b, c, d) in enumerate(TR[r]):
            x = M.NewBoolVar(''); X[(r, k)] = x; xs.append(x)
            for Q in (a, b, c): M.AddImplication(x, yvar(plane_orbit(Q)))
            if d >= 0: M.AddImplication(x, dvar(min(rotp[k2][d] for k2 in range(nn))))
            if INCH and d >= 0 and any(pm(Q) >> d & 1 for Q in (a, b, c)): bonus.append(x)
        M.AddExactlyOne(xs)
    M.Minimize(sum(yo.values()) + sum(do.values()) - sum(bonus) * (1.0 / nn))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
    st = sv.Solve(M); assert st in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    log('Z11 selection', sv.StatusName(st), '| plane orbits', sum(sv.Value(v) for v in yo.values()), '| defect orbits',
        sum(sv.Value(v) for v in do.values()), '| bound', sv.BestObjectiveBound())
    choice = {}
    for t in range(V):
        o, k = orb[t]; r = reps[o]
        kk = next(k2 for k2 in range(len(TR[r])) if sv.Value(X[(r, k2)]))
        a, b, c, d = TR[r][kk]
        choice[t] = (rotm(a, k), rotm(b, k), rotm(c, k), rotp[k][d] if d >= 0 else -1)
    pickle.dump(choice, open(CH, 'wb'))
used = sorted({Q for t in choice for Q in choice[t][:3]}, key=pc)
defects = sorted({choice[t][3] for t in choice if choice[t][3] >= 0})
log('selection', '| distinct planes', len(used), '| distinct defect lines', len(defects))
users = collections.defaultdict(list)
for t in range(V):
    a, b, c, d = choice[t]
    for Q in (a, b, c): users[Q].append(t)
    tot = pm(a) ^ pm(b) ^ pm(c) ^ ((1 << d) if d >= 0 else 0)
    assert tot == HYP[t], ('parity triple wrong', t)
log('users per section', dict(collections.Counter(len(users[Q]) for Q in used)))
SEC = {Q: pm(Q) for Q in used}
inchain = {}                                  # t -> plane Q whose section holds t's defect (read in-chain)
for t in range(V):
    a, b, c, d = choice[t]
    if INCH and d >= 0:
        for Q in (a, b, c):
            if pm(Q) >> d & 1: inchain[t] = Q; break
ncopy = {}
for Q in used:
    readers = sum(1 for t in users[Q] if inchain.get(t) == Q)
    ncopy[Q] = max(1, len(users[Q]) - readers)
log('in-chain readers', len(inchain), '| section copies', sum(ncopy.values()), 'vs users', sum(len(users[Q]) for Q in used))
# ---- step 3a: HIERARCHICAL shared pieces.  demands: flat -> copies needed
demand = collections.Counter({SEC[Q]: ncopy[Q] for Q in used})
children = collections.defaultdict(list)        # flat -> [child flats used inside it]
covered = collections.defaultdict(int)
level = 0; frontier = list(demand)
while frontier:
    where = collections.defaultdict(list)
    fs = sorted(set(frontier), key=pc)
    for F in fs:
        L = bits(F); cands = set()
        for a, b in itertools.combinations(L, 2):
            Xf = fclosure((1 << a) | (1 << b))
            if Xf & ~F == 0 and Xf != F: cands.add(Xf)
        if int(os.environ.get('TRIPLES', '1')) and len(L) <= 30:
            for a, b, c in itertools.combinations(L, 3):
                Xf = fclosure((1 << a) | (1 << b) | (1 << c))
                if pc(Xf) >= 4 and Xf & ~F == 0 and Xf != F: cands.add(Xf)
        for Xf in cands: where[Xf].append(F)
    # hyperplane cuts F & x-perp (flats), credited to every demand containing them
    if int(os.environ.get('HCUT', '0')) and level == 0:
        fsset = fs
        for F in fs:
            for x in range(V):
                Xc = F & HYP[x]
                if pc(Xc) < 3 or Xc == F: continue
                if Xc in where: continue
                cont = [G for G in fsset if Xc & ~G == 0]
                if len(cont) >= 2: where[Xc] = cont
    # intersections of demands
    for F, G in itertools.combinations(fs, 2):
        I = F & G
        if pc(I) >= 3:
            Xf = fclosure(I)
            if Xf & ~F == 0 and Xf & ~G == 0 and Xf != F and Xf != G:
                if F not in where[Xf]: where[Xf].append(F)
                if G not in where[Xf]: where[Xf].append(G)
    good = {Xf: w for Xf, w in where.items() if nondegenerate(Xf)}
    heap = [(-(len(w) - 1) * (pc(Xf) - 1), Xf) for Xf, w in good.items()]; heapq.heapify(heap)
    newf = []
    while heap:
        negs, Xf = heapq.heappop(heap)
        uses = [F for F in good[Xf] if covered[F] & Xf == 0]
        sc = (len(uses) - 1) * (pc(Xf) - 1)
        if sc <= 0: continue
        if sc < -negs: heapq.heappush(heap, (-sc, Xf)); continue
        for F in uses: covered[F] |= Xf; children[F].append(Xf)
        demand[Xf] += len(uses); newf.append(Xf)
    log('level', level, '| demands', len(fs), '| new pieces', len(newf), '| sizes', dict(collections.Counter(pc(x) for x in newf)))
    frontier = newf; level += 1
    if level > 6: break
flats = sorted(demand, key=lambda F: (lw.dim(F), pc(F)))
log('flats to assemble', len(flats), '| total copies', sum(demand.values()), '| uncovered line arrivals', sum(pc(F & ~covered[F]) for F in flats))
D10 = []
for i in range(11):
    m = 0
    for a, b in itertools.combinations([j for j in range(11) if j != i], 2): m |= (1 << g.P(a, b)) | (1 << g.T(a, b, i))
    D10.append(m)
def build(FEED, final):
    w = LWord(); dead = []
    keeper = {}
    for d in defects:                       # keeper copies first, while sources are untouched at {d}
        h = w.helper('keeper'); w.gate(1 << d, h, [d]); keeper[d] = h
    for s in FEED:
        h = w.helper('feeder'); w.gate(1 << s, h, [s]); dead.append(h)
    need = collections.defaultdict(list)
    for F in flats:
        for u in bits(F & ~covered[F]): need[u].append(F)
    carrier = {}
    for u in range(V):
        for idx, F in enumerate(need[u]):
            if idx == 0: carrier[(u, F)] = u
            else:
                h = w.helper('carrier'); w.gate(1 << u, h, [u]); carrier[(u, F)] = h
    regs = {}; take = collections.Counter()
    for F in flats:
        ins = [carrier[(u, F)] for u in bits(F & ~covered[F])]
        for C in children[F]: ins.append(regs[C][take[C]]); take[C] += 1
        res, dd = frame_alg(w, F, ins, [F] * demand[F], 'flat')
        regs[F] = [res[k] for k in range(demand[F])]; dead += dd
    deliv = collections.defaultdict(list); secreg = {}
    for Q in used:
        S = SEC[Q]; secreg[Q] = regs[S][take[S]]
        for t in users[Q]:
            if inchain.get(t) == Q: continue
            deliv[t].append(regs[S][take[S]]); take[S] += 1
    nh_top = w.nh
    red = {}
    for r in dead:
        vec = w.xpart(r); comb = {r}
        while vec:
            hb = vec.bit_length() - 1
            if hb in red: vec ^= red[hb][0]; comb = comb ^ red[hb][1]
            else: red[hb] = (vec, comb); break
    missing = []; totals = []
    for i in range(11):
        x = D10[i]; comb = set()
        while x:
            hb = x.bit_length() - 1
            if hb not in red: missing.append(hb); red[hb] = (1 << hb, {('feed', hb)})
            x ^= red[hb][0]; comb ^= red[hb][1]
        if final:
            assert not any(isinstance(c, tuple) for c in comb)
            h = w.helper('total'); w.gate(FULL, h, sorted(comb)); totals.append(h)
    if not final: return w, sorted(set(missing)), None
    w.ret = totals; w.phase = 'B'
    for t in range(V):
        d = choice[t][3]
        if d >= 0: w.gate(1 << d, V + t, [keeper[d]])
        if t in inchain:
            Q = inchain[t]; w.gate(SEC[Q], V + t, [secreg[Q]])
    for t in range(V): w.gate(HYP[t], V + t, deliv[t])
    for t in range(V): assert w.xpart(V + t) == HYP[t], ('target content', t)
    w.finish()
    return w, [], dict(after_top=nh_top, R=w.nh)
w, missing, _ = build([], False)
log('pass 1: helpers before totals', w.nh, '| feeder lines', len(missing))
w, _, stats = build(missing, True)
scatter = [[i for i in range(11) if g.binlabel(t) >> i & 1] for t in range(V)]
w.emit(scatter, [FULL] * 11, OUT)
log('EMITTED', OUT, stats, '| roles', dict(collections.Counter(w.role.values())))
