"""Build an I_{11,1} bit word on a frame-cell source system, ONE-LEVEL middle:
   line {s} -> system cell C -> node N (pp-closed flat of system cells, inside the section) -> section S -> t-perp.
Top: fewest plane sections per target covering R(t) by routable lines; one delivered register per (target, section).
Exact F2 algebra at every frame (lw.frame_alg).  Decoder totals tot_i = sum over D10(i) hosted at FULL on dead
registers (+ line-level feeder copies where the dead span is short; found in a first emission pass).
usage: build3.py SYSTEM.json OUT.json.gz"""
import sys, os, json, time, collections, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lw
from lw import V, g, bits, closure, dim, nondegenerate, LWord, frame_alg, FULL
from ortools.sat.python import cp_model
HYP = g.HYP
pc = lambda m: bin(m).count('1')
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
SYS, OUT = sys.argv[1], sys.argv[2]
cov = {int(k): v for k, v in json.load(open(SYS)).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
PM = {}
def pm(m):
    r = PM.get(m)
    if r is None:
        r = FULL
        for s in bits(m): r &= HYP[s]
        PM[m] = r
    return r
def pp(m): return pm(pm(m))
RT = {}
def RTm(S): return routable(S)
def routable(S):
    r = RT.get(S)
    if r is None:
        r = 0
        for u in bits(S):
            if any(C & ~S == 0 for C in cells_of[u]): r |= 1 << u
        RT[S] = r
    return r

# ---------------- top (cached)
TOPF = SYS.replace('.json', '') + '.top.json'
INCHAIN = []        # (t, S): t reads in-chain the delivered full part on S
if os.environ.get('TOPP'):
    parts = []
    tp = json.load(open(os.environ['TOPP']))
    for t, S, P, mode, Q in tp:
        if mode == 'in': INCHAIN.append((t, int(S, 16)))
        else: parts.append((t, int(S, 16), int(P, 16)))
elif os.path.exists(TOPF):
    parts = [(t, int(S, 16), int(P, 16)) for t, S, P in json.load(open(TOPF))]
else:
    parts = []
    for t in range(V):
        R = HYP[t]
        planes = sorted(set(closure((1 << t) | (1 << e)) for e in range(V) if e != t))
        secs = [pm(Q) for Q in planes]          # perp of a plane: always nondegenerate
        rout = [routable(S) & R for S in secs]
        M = cp_model.CpModel(); x = [M.NewBoolVar('') for _ in secs]
        for u in bits(R): M.AddBoolOr([x[i] for i in range(len(secs)) if rout[i] >> u & 1])
        M.Minimize(sum(x)); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 20; sv.parameters.num_workers = 4
        st = sv.Solve(M); assert st in (cp_model.OPTIMAL, cp_model.FEASIBLE)
        chosen = [i for i in range(len(secs)) if sv.Value(x[i])]
        asg = collections.defaultdict(int)
        for u in bits(R):
            i = max([i for i in chosen if rout[i] >> u & 1], key=lambda i: pc(rout[i]))
            asg[i] |= 1 << u
        for i, m in asg.items(): parts.append((t, secs[i], m))
    json.dump([(t, hex(S), hex(P)) for t, S, P in parts], open(TOPF, 'w'))
log('top: parts', len(parts), 'per target', dict(collections.Counter(collections.Counter(p[0] for p in parts).values())))

# ---------------- middle design
CIN = {}
def cin(S):
    r = CIN.get(S)
    if r is None: r = [C for C in cells if C & ~S == 0]; CIN[S] = r
    return r
NODE = {}   # N -> (ok, covered-lines mask, cells inside list)  (cells restricted to the section's cells)
def node_info(N, Scells):
    r = NODE.get(N)
    if r is None:
        ins = [C for C in Scells if C & ~N == 0]
        cm = 0
        for C in ins: cm |= C
        r = (nondegenerate(N), cm, ins); NODE[N] = r
    return r
import random, math
random.seed(int(os.environ.get('SEED', '1')))
HUBS = []
for p_ in range(11):
    oth = [i for i in range(11) if i != p_]
    for sz in (4, 5, 6):
        for A_ in itertools.combinations(oth, sz):
            m = 0
            for i, j in itertools.combinations(A_, 2): m |= (1 << g.P(i, j)) | (1 << g.T(i, j, p_))
            HUBS.append(closure(m))
# candidate nodes per part
CAND = []
for pi, (t, S, P) in enumerate(parts):
    Sc = cin(S)
    cand = [C for C in Sc if C & P]
    nodes = set([S])
    for C in cand: nodes.add(C); nodes.add(pp(C))
    for C, D in itertools.combinations(cand, 2): nodes.add(pp(C | D))
    for Hh in HUBS:
        if Hh & ~S == 0: nodes.add(Hh)
    lst = []
    for N in nodes:
        if N & ~S: continue
        ok, cm, ins = node_info(N, Sc)
        if ok and cm & P: lst.append((N, cm & P, [C for C in ins if C & P]))
    CAND.append(lst)
log('candidates built; avg per part', sum(map(len, CAND)) / len(CAND))
# ---- state
LK = collections.defaultdict(collections.Counter)   # (C,N) -> multiset of projection masks
cell_out = collections.Counter(); node_in = collections.Counter(); node_outn = collections.Counter()
line_cells = collections.defaultdict(collections.Counter)   # s -> Counter of cells needing s (with multiplicity)
def sdim(cnt):
    red = {}; d = 0
    for v0 in cnt:
        v1 = v0
        while v1:
            hb = v1.bit_length() - 1
            if hb in red: v1 ^= red[hb]
            else: red[hb] = v1; d += 1; break
    return d
def ccost(x): return max(0, x - 2)
def ncost(o, i): return max(0, o - i)
COVER = [None] * len(parts)
def apply(pi, cover, sign):
    """add (sign=+1) or remove (-1) a part's cover; returns cost delta"""
    delta = 0
    for N, L, usecell in cover:
        per = collections.defaultdict(int)
        for u, C in usecell.items(): per[C] |= 1 << u
        before_n = ncost(node_outn[N], node_in[N])
        for C, m in per.items():
            key = (C, N)
            d0 = sdim(LK[key])
            if sign > 0: LK[key][m] += 1
            else:
                LK[key][m] -= 1
                if LK[key][m] == 0: del LK[key][m]
            d1 = sdim(LK[key])
            if d1 != d0:
                bc = ccost(cell_out[C]); cell_out[C] += d1 - d0; delta += ccost(cell_out[C]) - bc
                node_in[N] += d1 - d0
            for s_ in bits(m & C):
                bl = len(line_cells[s_])
                line_cells[s_][C] += sign
                if line_cells[s_][C] == 0: del line_cells[s_][C]
                delta += max(0, len(line_cells[s_]) - 1) - max(0, bl - 1)
        node_outn[N] += sign
        delta += ncost(node_outn[N], node_in[N]) - before_n
    return delta
def gen_cover(pi, temp_rand):
    t, S, P = parts[pi]; U = P; cover = []
    cands = CAND[pi]
    while U:
        scored = []
        for N, cm, ins in cands:
            cl = U & cm
            if not cl: continue
            usecell = {}
            for u in bits(cl):
                cs = [C for C in ins if C >> u & 1]
                cs.sort(key=lambda C: (0 if (C, N) in LK else 1, cell_out[C]))
                usecell[u] = cs[0]
            newc = set(C for C in usecell.values() if (C, N) not in LK)
            est = sum(1 for C in newc if cell_out[C] >= 2) + (0 if node_in[N] + len(newc) > node_outn[N] else 1)
            scored.append((pc(cl) / (est + 0.3) * (1 + temp_rand * random.random()), N, cl, usecell))
        scored.sort(key=lambda z: -z[0])
        _, N, cl, usecell = scored[0]
        cover.append((N, cl, usecell)); U &= ~cl
    return cover
cost = 0
for pi in range(len(parts)):
    COVER[pi] = gen_cover(pi, 0.0); cost += apply(pi, COVER[pi], +1)
log('initial cost (extra registers beyond sources):', cost)
ITERS = int(os.environ.get('ITERS', '20000')); T0 = float(os.environ.get('T0', '2.0'))
best = cost; bestC = list(COVER)
for it in range(ITERS):
    pi = random.randrange(len(parts))
    old = COVER[pi]
    d1 = apply(pi, old, -1)
    newc = gen_cover(pi, 1.0)
    d2 = apply(pi, newc, +1)
    T = T0 * (1 - it / ITERS) + 0.01
    if d1 + d2 <= 0 or random.random() < math.exp(-(d1 + d2) / T):
        COVER[pi] = newc; cost += d1 + d2
        if cost < best: best = cost; bestC = list(COVER)
    else:
        apply(pi, newc, -1); apply(pi, old, +1)
    if it % 2000 == 0: log('SA it', it, 'cost', cost, 'best', best)
# rebuild best
links = collections.defaultdict(int); node_out = []
for pi in range(len(parts)):
    for N, cl, usecell in bestC[pi]:
        for u, C in usecell.items(): links[(C, N)] |= 1 << u
        node_out.append((pi, N, cl, usecell))
log('SA best cost', best)
log('middle design: node outputs', len(node_out), 'distinct nodes', len(set(o[1] for o in node_out)), 'links', len(links))
proj = collections.defaultdict(set)
for pi, N, cl, usecell in node_out:
    per = collections.defaultdict(int)
    for u, C in usecell.items(): per[C] |= 1 << u
    for C, m in per.items(): proj[(C, N)].add(m)
def span_basis(vecs):
    red = {}; out = []
    for v0 in sorted(vecs):
        v1 = v0
        while v1:
            hb = v1.bit_length() - 1
            if hb in red: v1 ^= red[hb]
            else: red[hb] = v1; out.append(v0); break
    return out
D10 = []
for i in range(11):
    m = 0
    for a, b in itertools.combinations([j for j in range(11) if j != i], 2): m |= (1 << g.P(a, b)) | (1 << g.T(a, b, i))
    D10.append(m)

def emit(FEED, final):
    w = LWord()
    need = collections.defaultdict(set)
    for (C, N) in links:
        for b in span_basis(proj[(C, N)]):
            for s in bits(b): need[s].add(C)
    branch = {}
    feed_regs = []
    for s in FEED:
        h = w.helper('feeder'); w.gate(1 << s, h, [s]); feed_regs.append(h)
    for s in range(V):
        cs = sorted(need[s])
        if not cs: continue
        branch[(s, cs[0])] = s
        for C in cs[1:]:
            h = w.helper('carrier'); w.gate(1 << s, h, [s]); branch[(s, C)] = h
    dead = list(feed_regs)
    by_cell = collections.defaultdict(list)
    for (C, N) in links: by_cell[C].append(N)
    link_regs = collections.defaultdict(list)
    for C, Ns in by_cell.items():
        ins = [branch[(s, C)] for s in bits(C) if (s, C) in branch]
        outs, tags = [], []
        for N in Ns:
            for b in span_basis(proj[(C, N)]): outs.append(b); tags.append(N)
        res, dd = frame_alg(w, C, ins, outs, 'cell')
        for k, r in res.items(): link_regs[(C, tags[k])].append(r)
        dead += dd
    nh_cells = w.nh
    outs_by_node = collections.defaultdict(list)
    for pi, N, cl, usecell in node_out: outs_by_node[N].append((pi, cl))
    ins_by_node = collections.defaultdict(list)
    for (C, N), regs in link_regs.items(): ins_by_node[N] += regs
    node_regs = {}
    for N in sorted(outs_by_node, key=dim):
        lst = outs_by_node[N]
        res, dd = frame_alg(w, N, ins_by_node[N], [cl for pi, cl in lst], 'node')
        for k, r in res.items(): node_regs[(lst[k][0], N)] = r
        dead += dd
    nh_nodes = w.nh
    by_sec = collections.defaultdict(list)
    for pi, (t, S, P) in enumerate(parts): by_sec[S].append(pi)
    ins_by_sec = collections.defaultdict(list)
    for (pi, N), r in node_regs.items(): ins_by_sec[parts[pi][1]].append(r)
    deliv = {}
    for S, pis in by_sec.items():
        res, dd = frame_alg(w, S, ins_by_sec[S], [parts[pi][2] for pi in pis], 'section')
        for k, r in res.items(): deliv[pis[k]] = r
        dead += dd
    nh_secs = w.nh
    # totals
    red = {}
    for r in dead:
        vec = w.xpart(r); comb = 1 << len(red) if False else None
        comb = {r}
        while vec:
            hb = vec.bit_length() - 1
            if hb in red: vec ^= red[hb][0]; comb = comb ^ red[hb][1]
            else: red[hb] = (vec, comb); break
    missing = []; totals = []
    for i in range(11):
        x = D10[i]; comb = set()
        while x:
            hb = x.bit_length() - 1
            if hb not in red:
                missing.append(hb)
                red[hb] = (1 << hb, {('feed', hb)})     # pretend a feeder exists (pass 1)
            x ^= red[hb][0]; comb ^= red[hb][1]
        if final:
            assert not any(isinstance(c, tuple) for c in comb)
            h = w.helper('total'); w.gate(FULL, h, sorted(comb)); totals.append(h)
    if not final: return w, sorted(set(missing)), None
    w.ret = totals
    w.phase = 'B'
    full_at = {}
    for pi, (t, S, P) in enumerate(parts):
        if P == RTm(S): full_at.setdefault(S, pi)
    for t, S in INCHAIN:
        pi = full_at[S]
        w.gate(S, V + t, [deliv[pi]])          # in-chain read of the co-user's full delivery
    by_t = collections.defaultdict(list)
    for pi, (t, S, P) in enumerate(parts): by_t[t].append(deliv[pi])
    for t in range(V): w.gate(HYP[t], V + t, by_t[t])
    for t in range(V): assert w.xpart(V + t) == HYP[t], ('target content', t)
    w.finish()
    stats = dict(carriers_and_feeders=nh_cells, after_nodes=nh_nodes, after_sections=nh_secs, R=w.nh)
    return w, [], stats

w, missing, _ = emit([], False)
log('pass 1: R(before totals) =', w.nh, 'feeder lines needed', len(missing))
w, _, stats = emit(missing, True)
scatter = [[i for i in range(11) if g.binlabel(t) >> i & 1] for t in range(V)]
w.emit(scatter, [FULL] * 11, OUT)
Hh = w.histogram([11] * 11)
log('EMITTED', OUT, stats, 'histogram', dict(sorted(Hh.items())))
log('roles', dict(collections.Counter(w.role.values())))
