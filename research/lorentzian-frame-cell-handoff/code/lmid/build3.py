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
if os.path.exists(TOPF):
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
links = collections.defaultdict(int)     # (C, N) -> lines of C used at N
node_out = []                            # (part index, N, lines mask, {u: C})
for pi, (t, S, P) in enumerate(parts):
    Sc = cin(S)
    cand = [C for C in Sc if C & P]
    nodes = set()
    for C in cand: nodes.add(C); nodes.add(pp(C))
    for C, D in itertools.combinations(cand, 2): nodes.add(pp(C | D))
    nodes = [N for N in nodes if N & ~S == 0]
    infos = []
    for N in nodes:
        ok, cm, ins = node_info(N, Sc)
        if ok and cm & P: infos.append((N, cm, ins))
    U = P
    while U:
        top = sorted(infos, key=lambda z: -pc(U & z[1]))[:24]
        best = None
        for N, cm, ins in top:
            cl = U & cm
            if not cl: continue
            usecell = {}
            for u in bits(cl):
                cs = [C for C in ins if C >> u & 1]
                cs.sort(key=lambda C: 0 if (C, N) in links else 1)
                usecell[u] = cs[0]
            newl = len(set(C for C in usecell.values() if (C, N) not in links))
            score = pc(cl) / (1.0 + newl)
            if best is None or score > best[0]: best = (score, N, cl, usecell)
        assert best is not None, ('uncoverable', pi)
        _, N, cl, usecell = best
        for u, C in usecell.items(): links[(C, N)] |= 1 << u
        node_out.append((pi, N, cl, usecell)); U &= ~cl
    if pi % 100 == 0: log('design part', pi, 'node outputs so far', len(node_out), 'links', len(links))
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
