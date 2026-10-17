"""BUILD an I_{11,1} word on a PARITY top of plane sections (A3/TT*-type triples, defect <= 1).
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
# ---- step 2: selection
planes = sorted({Q for t in TR for tr in TR[t] for Q in tr[:3]})
pid = {Q: i for i, Q in enumerate(planes)}
M = cp_model.CpModel()
y = [M.NewBoolVar('') for _ in planes]
dv = [M.NewBoolVar('') for _ in range(V)]
X = {}
for t in range(V):
    xs = []
    for k, (a, b, c, d) in enumerate(TR[t]):
        x = M.NewBoolVar(''); X[(t, k)] = x; xs.append(x)
        for Q in (a, b, c): M.AddImplication(x, y[pid[Q]])
        if d >= 0: M.AddImplication(x, dv[d])
    assert xs, ('no triple for target', t)
    M.AddExactlyOne(xs)
M.Minimize(sum(y) + sum(dv))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
st = sv.Solve(M)
assert st in (cp_model.OPTIMAL, cp_model.FEASIBLE)
choice = {}
for t in range(V):
    for k in range(len(TR[t])):
        if sv.Value(X[(t, k)]): choice[t] = TR[t][k]
used = sorted({Q for t in choice for Q in choice[t][:3]}, key=pc)
defects = sorted({choice[t][3] for t in choice if choice[t][3] >= 0})
log('selection', sv.StatusName(st), '| distinct planes', len(used), '| distinct defect lines', len(defects),
    '| objective', sv.ObjectiveValue(), 'bound', sv.BestObjectiveBound())
users = collections.defaultdict(list)
for t in range(V):
    a, b, c, d = choice[t]
    for Q in (a, b, c): users[Q].append(t)
    tot = pm(a) ^ pm(b) ^ pm(c) ^ ((1 << d) if d >= 0 else 0)
    assert tot == HYP[t], ('parity triple wrong', t)
log('users per section', dict(collections.Counter(len(users[Q]) for Q in used)))
SEC = {Q: pm(Q) for Q in used}
# ---- step 3a: shared pieces inside sections (each section = one atom)
where = collections.defaultdict(list)
for Q in used:
    L = bits(SEC[Q]); cands = set()
    for a, b in itertools.combinations(L, 2):
        Xf = fclosure((1 << a) | (1 << b))
        if Xf & ~SEC[Q] == 0: cands.add(Xf)
    if int(os.environ.get('TRIPLES', '1')):
        for a, b, c in itertools.combinations(L, 3):
            Xf = fclosure((1 << a) | (1 << b) | (1 << c))
            if pc(Xf) >= 4 and Xf & ~SEC[Q] == 0: cands.add(Xf)
    for Xf in cands: where[Xf].append(Q)
good = {Xf: w for Xf, w in where.items() if nondegenerate(Xf)}
covered = collections.defaultdict(int); chosen = []
heap = [(-(len(w) - 1) * (pc(Xf) - 1), Xf) for Xf, w in good.items()]; heapq.heapify(heap)
while heap:
    negs, Xf = heapq.heappop(heap)
    uses = [Q for Q in good[Xf] if covered[Q] & Xf == 0]
    sc = (len(uses) - 1) * (pc(Xf) - 1)
    if sc <= 0: continue
    if sc < -negs: heapq.heappush(heap, (-sc, Xf)); continue
    for Q in uses: covered[Q] |= Xf
    chosen.append((Xf, uses))
log('pieces', len(chosen), '| uses', sum(len(u) for _, u in chosen), '| sizes', dict(collections.Counter(pc(Xf) for Xf, _ in chosen)),
    '| section lines total', sum(pc(SEC[Q]) for Q in used), '| covered by pieces', sum(pc(covered[Q]) for Q in used))
piece_at = collections.defaultdict(list)
for pi, (Xf, uses) in enumerate(chosen):
    for Q in uses: piece_at[Q].append(pi)
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
    for pi, (Xf, uses) in enumerate(chosen):
        for u in bits(Xf): need[u].append(('P', pi))
    for Q in used:
        for u in bits(SEC[Q] & ~covered[Q]): need[u].append(('S', Q))
    carrier = {}
    for u in range(V):
        for idx, dest in enumerate(need[u]):
            if idx == 0: carrier[(u, dest)] = u
            else:
                h = w.helper('carrier'); w.gate(1 << u, h, [u]); carrier[(u, dest)] = h
    piece_regs = {}
    for pi, (Xf, uses) in enumerate(chosen):
        res, dd = frame_alg(w, Xf, [carrier[(u, ('P', pi))] for u in bits(Xf)], [Xf] * len(uses), 'piece')
        piece_regs[pi] = [res[k] for k in range(len(uses))]; dead += dd
    take = collections.Counter(); deliv = collections.defaultdict(list)
    for Q in used:
        S = SEC[Q]
        ins = [carrier[(u, ('S', Q))] for u in bits(S & ~covered[Q])]
        for pi in piece_at[Q]: ins.append(piece_regs[pi][take[pi]]); take[pi] += 1
        res, dd = frame_alg(w, S, ins, [S] * len(users[Q]), 'section')
        for k, t in enumerate(users[Q]): deliv[t].append(res[k])
        dead += dd
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
