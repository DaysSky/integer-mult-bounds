"""Build an I_{11,1} bit word on a frame-cell source system with a ONE-LEVEL middle:
   line {s} -> cell C (system cell) -> node N (pp-closed flat of system cells, inside the section) -> section S (plane
   section of the target) -> t-perp (delivery read by the target in phase B).
Top: per target the fewest plane sections covering R(t) by routable lines (cell inside the section); R(t) is split into
parts, one delivered register per (target, section).  Nodes chosen greedily per part, sharing (cell -> node) links.
All contents exact over F2 (frame_alg).  Decoder totals tot_i (D10(i), i = 0..10) hosted on dead registers.
usage: build1.py SYSTEM.json OUT.json.gz"""
import sys, os, json, time, collections, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lw
from lw import V, g, bits, closure, dim, nondegenerate, LWord, frame_alg, FULL
from ortools.sat.python import cp_model
HYP = g.HYP
pc = lambda m: bin(m).count('1')
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
OUT = sys.argv[2]
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
def perp_of_plane(Q): return pm(Q)

# ---------------- top: sections + parts
RT = {}
def routable(S):
    r = RT.get(S)
    if r is None:
        r = 0
        for u in bits(S):
            if any(C & ~S == 0 for C in cells_of[u]): r |= 1 << u
        RT[S] = r
    return r
parts = []      # (t, S, linesmask)
for t in range(V):
    R = HYP[t]
    planes = sorted(set(closure((1 << t) | (1 << e)) for e in range(V) if e != t))
    secs = [pm(Q) for Q in planes]
    secs = [S for S in secs if nondegenerate(S)]
    rout = [routable(S) & R for S in secs]
    M = cp_model.CpModel(); x = [M.NewBoolVar('') for _ in secs]
    for u in bits(R):
        M.AddBoolOr([x[i] for i in range(len(secs)) if rout[i] >> u & 1])
    M.Minimize(sum(x)); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 20; sv.parameters.num_workers = 4
    st = sv.Solve(M); assert st in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    chosen = [i for i in range(len(secs)) if sv.Value(x[i])]
    # assign each line to the chosen section with the most routable lines (balanced-ish)
    asg = collections.defaultdict(int)
    for u in bits(R):
        opts = [i for i in chosen if rout[i] >> u & 1]
        i = max(opts, key=lambda i: pc(rout[i]))
        asg[i] |= 1 << u
    for i, m in asg.items(): parts.append((t, secs[i], m))
log('top done: parts', len(parts), 'sections per target', collections.Counter(collections.Counter(p[0] for p in parts).values()))

# ---------------- middle design (greedy shared nodes)
cells_in = {}
def cin(S):
    r = cells_in.get(S)
    if r is None:
        r = [C for C in cells if C & ~S == 0]; cells_in[S] = r
    return r
NODEOK = {}
def node_ok(N):
    r = NODEOK.get(N)
    if r is None: r = nondegenerate(N); NODEOK[N] = r
    return r
links = collections.defaultdict(int)      # (C, N) -> mask of lines of C needed at N
node_out = []                             # (part index, N, lines mask assigned via N, {u: C})
for pi, (t, S, P) in enumerate(parts):
    cand_cells = [C for C in cin(S) if C & P]
    nodes = set()
    for C in cand_cells:
        nodes.add(C)                 # direct: cell itself acts as node
        nodes.add(pp(C))
    for C, D in itertools.combinations(cand_cells, 2):
        nodes.add(pp(C | D))
    nodes = [N for N in nodes if N & ~S == 0 and node_ok(N)]
    U = P; mine = []
    while U:
        best = None
        for N in nodes:
            cov_lines = 0; newlinks = 0; usecell = {}
            for u in bits(U):
                cs = [C for C in cells_of[u] if C & ~N == 0]
                if not cs: continue
                cs.sort(key=lambda C: 0 if (C, N) in links else 1)
                usecell[u] = cs[0]; cov_lines |= 1 << u
            if not cov_lines: continue
            newl = len(set(C for C in usecell.values() if (C, N) not in links))
            score = pc(cov_lines) / (1 + newl)
            if best is None or score > best[0]: best = (score, N, cov_lines, usecell)
        assert best is not None, ('uncoverable part', pi)
        _, N, cl, usecell = best
        for u, C in usecell.items(): links[(C, N)] |= 1 << u
        node_out.append((pi, N, cl, usecell)); U &= ~cl
log('middle design: node outputs', len(node_out), 'distinct nodes', len(set(o[1] for o in node_out)),
    'cell->node links', len(links))

# ---------------- emission
w = LWord()
# line level: branches for each cell needing s
need_cells = collections.defaultdict(set)
for (C, N), m in links.items():
    for s in bits(m): need_cells[s].add(C)
branch = {}                     # (s, C) -> register
for s in range(V):
    cs = sorted(need_cells[s])
    if not cs: continue
    branch[(s, cs[0])] = s
    for C in cs[1:]:
        h = w.helper('carrier'); w.gate(1 << s, h, [s]); branch[(s, C)] = h
log('line level done, helpers', w.nh)
# cell level
link_regs = collections.defaultdict(list)   # (C, N) -> registers carrying a basis of the needed span
dead = []
by_cell = collections.defaultdict(list)
for (C, N), m in links.items(): by_cell[C].append((N, m))
for C, lst in by_cell.items():
    ins = [branch[(s, C)] for s in bits(C) if (s, C) in branch]
    outs = []; tags = []
    for N, m in lst:
        # needed span from C at N: each needed line separately (span of {x_u : u in m})
        for u in bits(m): outs.append(1 << u); tags.append(N)
    res, dd = frame_alg(w, C, ins, outs, 'cell')
    for k, r in res.items(): link_regs[(C, tags[k])].append(r)
    dead += dd
log('cell level done, helpers', w.nh)
# node level
outs_by_node = collections.defaultdict(list)
for pi, N, cl, usecell in node_out: outs_by_node[N].append((pi, cl))
node_regs = {}                               # (pi, N) -> register
ins_by_node = collections.defaultdict(list)
for (C, N), regs in link_regs.items(): ins_by_node[N] += regs
for N in sorted(outs_by_node, key=dim):
    lst = outs_by_node[N]
    ins = ins_by_node[N]
    res, dd = frame_alg(w, N, ins, [cl for pi, cl in lst], 'node')
    for k, r in res.items(): node_regs[(lst[k][0], N)] = r
    dead += dd
log('node level done, helpers', w.nh)
# section level
by_sec = collections.defaultdict(list)
for pi, (t, S, P) in enumerate(parts): by_sec[S].append(pi)
deliv = {}
ins_by_sec = collections.defaultdict(list)
for (pi, N), r in node_regs.items(): ins_by_sec[parts[pi][1]].append(r)
for S, pis in by_sec.items():
    res, dd = frame_alg(w, S, ins_by_sec[S], [parts[pi][2] for pi in pis], 'section')
    for k, r in res.items(): deliv[pis[k]] = r
    dead += dd
log('section level done, helpers', w.nh, 'deliveries', len(deliv), 'dead', len(dead))
# decoder totals: tot_i = sum over D10(i); hosted at FULL on helpers built from dead registers (+ feeders if needed)
D10 = []
for i in range(11):
    m = 0
    for a, b in itertools.combinations([j for j in range(11) if j != i], 2): m |= (1 << g.P(a, b)) | (1 << g.T(a, b, i))
    D10.append(m)
def span_solve(regs, target):
    red = {}
    for r in regs:
        vec = w.xpart(r); tag = 1 << len(red) if False else 0
    basis = []   # (vec, set of regs)
    red = {}
    for r in regs:
        vec = w.xpart(r); comb = {r}
        while vec:
            hb = vec.bit_length() - 1
            if hb in red: vec ^= red[hb][0]; comb ^= red[hb][1]
            else: red[hb] = (vec, comb); break
    x = target; comb = set()
    while x:
        hb = x.bit_length() - 1
        if hb not in red: return None, red
        x ^= red[hb][0]; comb ^= red[hb][1]
    return comb, red
feeders = 0
totals = []
for i in range(11):
    comb, red = span_solve(dead, D10[i])
    while comb is None:
        # add a feeder copy x_s for the highest unresolved line
        x = D10[i]
        while x:
            hb = x.bit_length() - 1
            if hb in red: x ^= red[hb][0]
            else: break
        s = x.bit_length() - 1
        h = w.helper('feeder'); w.gate(1 << s, h, [s]); dead.append(h); feeders += 1
        comb, red = span_solve(dead, D10[i])
    h = w.helper('total'); w.gate(FULL, h, sorted(comb))
    totals.append(h)
w.ret = totals
log('totals hosted; feeders', feeders, 'helpers', w.nh)
# phase B: targets read their deliveries at t-perp
w.phase = 'B'
by_t = collections.defaultdict(list)
for pi, (t, S, P) in enumerate(parts): by_t[t].append(deliv[pi])
for t in range(V):
    w.gate(HYP[t], V + t, by_t[t])
# check contents: each target's B-content = R(t)
for t in range(V):
    assert w.xpart(V + t) == HYP[t], ('target content wrong', t)
w.finish()
scatter = []
for t in range(V):
    lab = g.binlabel(t)
    scatter.append([i for i in range(11) if lab >> i & 1])
ret_frames = [FULL] * 11
w.emit(scatter, ret_frames, OUT)
copy_ranks = [11] * 11
Hh = w.histogram(copy_ranks)
log('EMITTED', OUT, 'R =', w.nh, 'histogram', dict(sorted(Hh.items())))
roles = collections.Counter(w.role.values())
log('helper roles', dict(roles))
