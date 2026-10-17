"""BUILD a verified I_{11,1} bit word on the combined M11 top (llp/lm11design.py + exact Z11 parts lr8det_m11_*.json):
T lines on the 220 S(4,5,11) triangle nodes, P lines on one derived parallel class each.  Every target has 4 sections
(rank-8 frame perps), parts partition R(t), one in-chain section (read at the node in phase B), 3 delivered.
Middle v1 (direct): per node, line carriers (copies of x_u made at {u}) climb straight into the node; exact F2
transform at the node (lw.frame_alg) produces the delivered parts and, if needed, extra registers for in-chain parts.
Decoder totals as in lmid/build3.py.  usage: build_m11.py DET.json POOL.pkl OUT.json.gz"""
import sys, os, json, pickle, collections, itertools, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lmid'))
import lw
from lw import V, g, bits, dim, LWord, frame_alg, FULL
HYP = g.HYP
pc = lambda m: bin(m).count('1')
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
DET, POOL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
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
    sections[t] = [pm(F) for F in Fs]
    parts[t] = [rotm(asg[(o, j)], k) for j in range(4)]
    cin[t] = det['cin'][o].index(1)
    tot = 0
    for j in range(4):
        assert parts[t][j] & ~sections[t][j] == 0 and tot & parts[t][j] == 0
        assert lw.nondegenerate(sections[t][j]), 'degenerate section'
        tot |= parts[t][j]
    assert tot == HYP[t], ('parts do not partition R(t)', t)
log('design loaded: every target has 4 nondegenerate sections whose parts partition R(t)')
users = collections.defaultdict(list)          # section frame -> [(t, j, part, inchain)]
for t in range(V):
    for j in range(4): users[sections[t][j]].append((t, j, parts[t][j], j == cin[t]))
log('distinct nodes', len(users), '| users per node', dict(collections.Counter(len(u) for u in users.values())))
D10 = []
for i in range(11):
    m = 0
    for a, b in itertools.combinations([j for j in range(11) if j != i], 2): m |= (1 << g.P(a, b)) | (1 << g.T(a, b, i))
    D10.append(m)
def build(FEED, final):
    w = LWord(); dead = []
    for s in FEED:
        h = w.helper('feeder'); w.gate(1 << s, h, [s]); dead.append(h)
    # line carriers: one register per (line, node needing it); the source register itself serves its first node
    need = collections.defaultdict(list)
    for S, us in users.items():
        un = 0
        for (t, j, p, ic) in us: un |= p
        for u in bits(un): need[u].append(S)
    carrier = {}
    for u in range(V):
        for idx, S in enumerate(need[u]):
            if idx == 0: carrier[(u, S)] = u
            else:
                h = w.helper('carrier'); w.gate(1 << u, h, [u]); carrier[(u, S)] = h
    deliv = {}; inreg = {}
    for S in sorted(users, key=lambda S: pc(S)):
        us = users[S]; un = 0
        for (t, j, p, ic) in us: un |= p
        ins = [carrier[(u, S)] for u in bits(un)]
        dl = [(t, j, p) for (t, j, p, ic) in us if not ic]
        icl = [(t, j, p) for (t, j, p, ic) in us if ic]
        outs = [p for (t, j, p) in dl] + [p for (t, j, p) in icl]
        res, dd = frame_alg(w, S, ins, outs, 'node')
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
    for t in range(V):                       # in-chain reads first (registers still at the node)
        j = cin[t]; w.gate(sections[t][j], V + t, [inreg[(t, j)]])
    for t in range(V):
        w.gate(HYP[t], V + t, [deliv[(t, j)] for j in range(4) if j != cin[t]])
    for t in range(V): assert w.xpart(V + t) == HYP[t], ('target content', t)
    w.finish()
    return w, [], dict(after_top=nh_top, R=w.nh)
w, missing, _ = build([], False)
log('pass 1: helpers before totals', w.nh, '| feeder lines needed', len(missing))
w, _, stats = build(missing, True)
scatter = [[i for i in range(11) if g.binlabel(t) >> i & 1] for t in range(V)]
w.emit(scatter, [FULL] * 11, OUT)
log('EMITTED', OUT, stats, '| roles', dict(collections.Counter(w.role.values())))
log('histogram', dict(sorted(w.histogram([11] * 11).items())))
