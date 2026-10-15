"""Broadcaster/collector word builder (demand-driven), I_{11,1} frame-cell system.
 - Broadcasters: registers carrying ONE line x_u, never modified, climbing a nested chain of frames that starts at a
   system cell C of u.  (First broadcaster of u = the source register, others = carriers copied at {u}.)
 - Collectors: one delivery register per part (t, S, P); it climbs a nested chain of nodes inside S and at each node
   reads (XORs in) broadcasters present there.  A read of u at node N is free if some broadcaster of u (from a cell
   C inside N) has a chain comparable with N (N is inserted); otherwise a new broadcaster (+1 register) is created.
 - Phase A: all collector reads (in rank order), then broadcasters climb to FULL and host the 11 decoder totals.
 - Phase B: each target reads its deliveries at t-perp.
usage: bc2.py SYSTEM.json OUT.json.gz"""
import sys, os, json, time, collections, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lw import V, g, bits, closure, dim, nondegenerate, LWord, FULL
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
ND = {}
def ok(N):
    r = ND.get(N)
    if r is None: r = nondegenerate(N); ND[N] = r
    return r
parts = [(t, int(S, 16), int(P, 16)) for t, S, P in json.load(open(SYS.replace('.json', '') + '.top.json'))]
log('parts', len(parts))
HUBS = []
for p_ in range(11):
    oth = [i for i in range(11) if i != p_]
    for sz in (3, 4, 5, 6, 7):
        for A_ in itertools.combinations(oth, sz):
            m = 0
            for i, j in itertools.combinations(A_, 2): m |= (1 << g.P(i, j)) | (1 << g.T(i, j, p_))
            HUBS.append(closure(m))
HUBS = sorted(set(HUBS))
# broadcasters: list of [line, cell, chain(list of frames, nested)]
BC = []
by_lc = collections.defaultdict(list)        # (u, C) -> broadcaster ids
def comparable(chain, N):
    return all((F & ~N == 0) or (N & ~F == 0) for F in chain)
def find_bc(u, N):
    """a broadcaster of u (cell inside N) whose chain admits N; returns id or None"""
    best = None
    for C in cells_of[u]:
        if C & ~N: continue
        for b in by_lc[(u, C)]:
            if N in BC[b][2] or comparable(BC[b][2], N):
                return b
        if best is None: best = C
    return None
def cell_for(u, N):
    cs = [C for C in cells_of[u] if C & ~N == 0]
    return cs[0] if cs else None
reads = []          # (part index, node, [broadcaster ids])
part_chain = {}
for pi, (t, S, P) in enumerate(parts):
    Sc = [C for C in cells if C & ~S == 0 and C & P]
    cand = set([S])
    for C in Sc: cand.add(pp(C))
    for C, D in itertools.combinations(Sc, 2): cand.add(pp(C | D))
    for Hh in HUBS:
        if Hh & ~S == 0 and Hh & P: cand.add(Hh)
    cand = [N for N in cand if N & ~S == 0 and ok(N)]
    # covered lines per node
    cvr = {}
    for N in cand:
        m = 0
        for C in Sc:
            if C & ~N == 0: m |= C
        cvr[N] = m & P
    chain = []; left = P
    while left:
        best = None
        for N in cand:
            if not all((F & ~N == 0) or (N & ~F == 0) for F in chain): continue
            cl = cvr[N] & left
            if not cl: continue
            free = 0; new = 0
            for u in bits(cl):
                if find_bc(u, N) is not None: free += 1
                else: new += 1
            sc = (free + 0.35 * new, -dim(N))
            if best is None or sc > best[0]: best = (sc, N, cl)
        assert best is not None, ('stuck', pi)
        _, N, cl = best
        ids = []
        for u in bits(cl):
            b = find_bc(u, N)
            if b is None:
                C = cell_for(u, N)
                b = len(BC); BC.append([u, C, [C]]); by_lc[(u, C)].append(b)
            if N not in BC[b][2]:
                BC[b][2].append(N); BC[b][2].sort(key=dim)
            ids.append(b)
        reads.append((pi, N, ids)); chain.append(N); left &= ~cl
    part_chain[pi] = sorted(chain, key=dim)
    if pi % 100 == 0: log('part', pi, 'broadcasters', len(BC), 'reads', len(reads))
nbc = collections.Counter(b[0] for b in BC)
log('design: broadcasters', len(BC), 'lines without broadcaster', sum(1 for u in range(V) if nbc[u] == 0),
    'deliveries', len(parts), 'reads', len(reads))
# verify chains nested
for b in BC:
    ch = b[2]
    for x, y in zip(ch, ch[1:]): assert x & ~y == 0 and dim(y) > dim(x), 'broadcaster chain not nested'
# ---------------- emission
w = LWord()
reg_of = {}
first = {}
for bid, (u, C, ch) in enumerate(BC):
    if u not in first: first[u] = bid; reg_of[bid] = u
for bid, (u, C, ch) in enumerate(BC):
    if bid in reg_of: continue
    h = w.helper('carrier'); w.gate(1 << u, h, [u]); reg_of[bid] = h
# lines with no broadcaster still need a dead copy for the totals: use the source register itself
deliv = {}
for pi in range(len(parts)): deliv[pi] = w.helper('collector')
order = sorted(range(len(reads)), key=lambda k: dim(reads[k][1]))
for k in order:
    pi, N, ids = reads[k]
    w.gate(N, deliv[pi], [reg_of[b] for b in ids])
log('collector reads done; helpers', w.nh)
for pi, (t, S, P) in enumerate(parts): assert w.xpart(deliv[pi]) == P, ('delivery content', pi)
# decoder totals at FULL on broadcasters (one broadcaster per line as source; hosts are distinct broadcasters)
D10 = []
for i in range(11):
    m = 0
    for a, b in itertools.combinations([j for j in range(11) if j != i], 2): m |= (1 << g.P(a, b)) | (1 << g.T(a, b, i))
    D10.append(m)
regs_of_line = collections.defaultdict(list)
for bid, (u, C, ch) in enumerate(BC): regs_of_line[u].append(reg_of[bid])
for u in range(V):
    if not regs_of_line[u]: regs_of_line[u].append(u)
used_host = set(); totals = []
for i in range(11):
    host = None
    for u in bits(D10[i]):
        for r in regs_of_line[u][1:]:
            if r not in used_host: host = (u, r); break
        if host: break
    if host is None:
        h = w.helper('total'); w.gate(FULL, h, [regs_of_line[u][0] for u in bits(D10[i])]); totals.append(h)
    else:
        u0, r0 = host; used_host.add(r0)
        w.gate(FULL, r0, [regs_of_line[u][0] for u in bits(D10[i]) if u != u0]); totals.append(r0)
    assert w.xpart(totals[-1]) == D10[i]
w.ret = totals
w.phase = 'B'
by_t = collections.defaultdict(list)
for pi, (t, S, P) in enumerate(parts): by_t[t].append(deliv[pi])
for t in range(V): w.gate(HYP[t], V + t, by_t[t])
for t in range(V): assert w.xpart(V + t) == HYP[t]
w.finish()
scatter = [[i for i in range(11) if g.binlabel(t) >> i & 1] for t in range(V)]
w.emit(scatter, [FULL] * 11, OUT)
Hh = w.histogram([11] * 11)
log('EMITTED', OUT, 'R =', w.nh, 'roles', dict(collections.Counter(w.role.values())), 'histogram', dict(sorted(Hh.items())))
