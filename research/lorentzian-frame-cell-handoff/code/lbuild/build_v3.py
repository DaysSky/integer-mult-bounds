"""BUILD v3 (= v2 with fast closure, triple-closure flats enabled by default): same legal frame-section top as build_m11.py, middle with SHARED PIECES.
At each node S the needed lines (union of users' parts) split into ATOMS (same membership pattern over the node's
parts); a nondegenerate flat X inside one atom can arrive as the single register sigma(X) instead of |X| line
carriers.  A piece is assembled once at frame X from line carriers (exact frame_alg) and copied once per further use;
saving (k-1)(|X|-1) for k uses.  Candidates: closures of 2- and 3-subsets inside atoms; greedy by saving, disjoint
inside each atom.  Nodes: frame_alg over piece copies + remaining line carriers.  usage: build_v2.py DET POOL OUT"""
import sys, os, json, pickle, collections, itertools, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lmid'))
import lw
from lw import V, g, bits, dim, LWord, frame_alg, FULL, nondegenerate
from fastcl import fclosure as closure
HYP = g.HYP
pc = lambda m: bin(m).count('1')
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
DET, POOL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
MAXSUB = int(os.environ.get('MAXSUB', '3'))
D = json.load(open(DET)); sel = {int(k): v for k, v in D['sel'].items()}; det = D['det']
cov = pickle.load(open(POOL, 'rb'))
n = 11
def img_line(s, perm): return g.idx[(g.kind[s], tuple(sorted(perm[i] for i in g.supp[s])))]
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
rotp = [list(range(V))]
for k in range(1, n): rotp.append([rot[x] for x in rotp[-1]])
def rotm(m, k):
    r = 0
    for s in bits(m): r |= 1 << rotp[k % n][s]
    return r
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
asg = collections.defaultdict(int)
for key, val in det['assign'].items():
    ri, i, u = map(int, key.split(','))
    if val: asg[(ri, i)] |= 1 << u
PM = {}
def pm(m):
    r = PM.get(m)
    if r is None:
        r = FULL
        for s in bits(m): r &= HYP[s]
        PM[m] = r
    return r
sections, parts, cin = {}, {}, {}
for t in range(V):
    o, k = orb[t]
    Fs = [rotm(F, k) for F in cov[reps[o]][sel[reps[o]]]]
    sections[t] = [pm(F) for F in Fs]; parts[t] = [rotm(asg[(o, j)], k) for j in range(4)]
    cin[t] = det['cin'][o].index(1)
    tot = 0
    for j in range(4):
        assert parts[t][j] & ~sections[t][j] == 0 and tot & parts[t][j] == 0 and nondegenerate(sections[t][j])
        tot |= parts[t][j]
    assert tot == HYP[t]
users = collections.defaultdict(list)
for t in range(V):
    for j in range(4): users[sections[t][j]].append((t, j, parts[t][j], j == cin[t]))
nodes = sorted(users, key=pc)
atoms = {}
for S in nodes:
    pat = collections.defaultdict(int)
    for u in range(V):
        pass
    un = 0
    for (_, _, p, _) in users[S]: un |= p
    for u in bits(un):
        key = tuple(i for i, (_, _, p, _) in enumerate(users[S]) if p >> u & 1)
        pat[key] |= 1 << u
    atoms[S] = list(pat.values())
log('nodes', len(nodes), '| atoms', sum(len(a) for a in atoms.values()), '| needed line-node incidences',
    sum(pc(a) for al in atoms.values() for a in al))
# candidate flats inside atoms
CL = {}
def cl(m):
    r = CL.get(m)
    if r is None: r = closure(m); CL[m] = r
    return r
where = collections.defaultdict(list)    # X -> [(S, atom index)]
for S in nodes:
    for ai, A in enumerate(atoms[S]):
        L = bits(A)
        if len(L) < 2: continue
        cands = set()
        for a, b in itertools.combinations(L, 2):
            X = cl((1 << a) | (1 << b))
            if X & ~A == 0: cands.add(X)
        if MAXSUB >= 3 and len(L) <= int(os.environ.get("MAXATOM", "40")):
            for a, b, c in itertools.combinations(L, 3):
                X = cl((1 << a) | (1 << b) | (1 << c))
                if pc(X) >= 4 and X & ~A == 0: cands.add(X)
        for X in cands: where[X].append((S, ai))
log('candidate flats', len(where))
good = {X: w for X, w in where.items() if nondegenerate(X)}
log('nondegenerate candidates', len(good))
# greedy
covered = collections.defaultdict(int)     # (S, ai) -> lines already covered by chosen pieces
chosen = []                                # (X, [(S, ai)])
order = sorted(good.items(), key=lambda kv: -((len(kv[1]) - 1) * (pc(kv[0]) - 1)))
import heapq
heap = [(-(len(w) - 1) * (pc(X) - 1), X) for X, w in good.items()]
heapq.heapify(heap)
while heap:
    negs, X = heapq.heappop(heap)
    uses = [(S, ai) for (S, ai) in good[X] if covered[(S, ai)] & X == 0]
    sc = (len(uses) - 1) * (pc(X) - 1)
    if sc <= 0: continue
    if sc < -negs:
        heapq.heappush(heap, (-sc, X)); continue
    for su in uses: covered[su] |= X
    chosen.append((X, uses))
saving = sum((len(u) - 1) * (pc(X) - 1) for X, u in chosen)
log('chosen pieces', len(chosen), '| uses', sum(len(u) for _, u in chosen), '| estimated saving', saving,
    '| piece sizes', dict(collections.Counter(pc(X) for X, _ in chosen)))
piece_at = collections.defaultdict(list)    # S -> [piece index]
for pi, (X, uses) in enumerate(chosen):
    for (S, ai) in uses: piece_at[S].append(pi)
D10 = []
for i in range(11):
    m = 0
    for a, b in itertools.combinations([j for j in range(11) if j != i], 2): m |= (1 << g.P(a, b)) | (1 << g.T(a, b, i))
    D10.append(m)
def build(FEED, final):
    w = LWord(); dead = []
    for s in FEED:
        h = w.helper('feeder'); w.gate(1 << s, h, [s]); dead.append(h)
    # line demand: (u, frame) pairs: pieces X need their lines at X; nodes need uncovered lines
    need = collections.defaultdict(list)
    for pi, (X, uses) in enumerate(chosen):
        for u in bits(X): need[u].append(('P', pi))
    for S in nodes:
        cv = 0
        for ai, A in enumerate(atoms[S]): cv |= covered[(S, ai)]
        un = 0
        for (_, _, p, _) in users[S]: un |= p
        for u in bits(un & ~cv): need[u].append(('N', S))
    carrier = {}
    for u in range(V):
        for idx, dest in enumerate(need[u]):
            if idx == 0: carrier[(u, dest)] = u
            else:
                h = w.helper('carrier'); w.gate(1 << u, h, [u]); carrier[(u, dest)] = h
    piece_regs = {}
    for pi, (X, uses) in enumerate(chosen):
        res, dd = frame_alg(w, X, [carrier[(u, ('P', pi))] for u in bits(X)], [X] * len(uses), 'piece')
        piece_regs[pi] = [res[k] for k in range(len(uses))]
        dead += dd
    nh_pieces = w.nh
    take = {pi: 0 for pi in piece_regs}
    deliv = {}; inreg = {}
    for S in nodes:
        us = users[S]
        cv = 0
        for ai, A in enumerate(atoms[S]): cv |= covered[(S, ai)]
        un = 0
        for (_, _, p, _) in us: un |= p
        ins = [carrier[(u, ('N', S))] for u in bits(un & ~cv)]
        for pi in piece_at[S]:
            ins.append(piece_regs[pi][take[pi]]); take[pi] += 1
        dl = [(t, j, p) for (t, j, p, ic) in us if not ic]; icl = [(t, j, p) for (t, j, p, ic) in us if ic]
        res, dd = frame_alg(w, S, ins, [p for (_, _, p) in dl] + [p for (_, _, p) in icl], 'node')
        for k, (t, j, p) in enumerate(dl): deliv[(t, j)] = res[k]
        for k, (t, j, p) in enumerate(icl): inreg[(t, j)] = res[len(dl) + k]
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
        j = cin[t]; w.gate(sections[t][j], V + t, [inreg[(t, j)]])
    for t in range(V):
        w.gate(HYP[t], V + t, [deliv[(t, j)] for j in range(4) if j != cin[t]])
    for t in range(V): assert w.xpart(V + t) == HYP[t], ('target content', t)
    w.finish()
    return w, [], dict(after_pieces=nh_pieces, after_top=nh_top, R=w.nh)
w, missing, _ = build([], False)
log('pass 1: helpers before totals', w.nh, '| feeder lines', len(missing))
w, _, stats = build(missing, True)
scatter = [[i for i in range(11) if g.binlabel(t) >> i & 1] for t in range(V)]
w.emit(scatter, [FULL] * 11, OUT)
log('EMITTED', OUT, stats, '| roles', dict(collections.Counter(w.role.values())))
