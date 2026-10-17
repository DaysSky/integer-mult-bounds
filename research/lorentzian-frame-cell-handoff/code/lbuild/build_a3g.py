"""BUILD (telescoped A3 blocks, general residual pieces via genpieces.py): block target t (A3 block B, triangles Q1,Q2 through t, opposite o) reads along its
chain 0 -> B-perp -> Q1-perp -> t-perp:  sigma(B-perp) at B-perp (ONE register read by all 6 block targets),
sigma(E_Q1) at Q1-perp (E_Q = Q-perp minus B-perp, shared by the triangle's users), and at t-perp the deliveries
sigma(E_Q2), sigma(E_pair) plus the PURE source of o (mutual opposites).  Parity: B-perp lies in all three sections.
Leftover targets: full plane sections + keeper (or provider source) as in build_a3b.py.
Middle: demands (host frame F, content Y), hierarchical shared flat pieces inside contents, line values broadcast
along exact minimum chain covers (read-only, consumed at chain ends).  usage: build_a3t.py CHOICE.pkl OUT.json.gz"""
import sys, os, pickle, collections, itertools, time, heapq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lmid'))
import lw
from lw import V, g, bits, LWord, frame_alg, FULL, nondegenerate
from fastcl import fclosure
HYP = g.HYP; G = g.G
pc = lambda m: bin(m).count('1')
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
CHF, OUT = sys.argv[1], sys.argv[2]
choice = pickle.load(open(CHF, 'rb'))
PM = {}
def pm(m):
    r = PM.get(m)
    if r is None:
        r = FULL
        for s in bits(m): r &= HYP[s]
        PM[m] = r
    return r
# ---- classify targets: block (A3 triple with defect = opposite inside the A3) vs leftover
block_of = {}
for t, (a, b, c, d) in choice.items():
    tris = [Q for Q in (a, b, c) if pc(Q) == 3]
    pairs = [Q for Q in (a, b, c) if pc(Q) == 2]
    if len(tris) == 2 and len(pairs) == 1 and d >= 0 and pairs[0] >> d & 1:
        A3 = fclosure(tris[0] | tris[1])
        if pc(A3) == 6 and A3 >> d & 1: block_of[t] = (A3, tris[0], tris[1], pairs[0], d)
# blocks must be complete (all 6 lines are block targets of the same A3) for the shared B-perp read
bl_members = collections.defaultdict(list)
for t, (A3, *_r) in block_of.items(): bl_members[A3].append(t)
ALLA3 = os.environ.get('ALLA3', '1') == '1'
if not ALLA3: block_of = {t: v for t, v in block_of.items() if len(bl_members[v[0]]) == 6}
blocks = sorted({v[0] for v in block_of.values()})
left = [t for t in range(V) if t not in block_of]
log('complete A3 blocks', len(blocks), '| block targets', len(block_of), '| leftover', len(left))
# ---- providers (pure sources): block opposites (mutual); then leftovers' defects if free
provider = {}
for t, (A3, Q1, Q2, P, o) in block_of.items():
    if o in block_of and block_of[o][4] == t: provider[o] = t          # mutual opposites
for t, (A3, Q1, Q2, P, o) in block_of.items():
    if o not in provider: provider[o] = t
for t in left:
    d = choice[t][3]
    if d >= 0 and d not in provider: provider[d] = t
srcdef = {t: d for d, t in provider.items()}
# ---- demands
demand = collections.Counter(); content = {}
def dkey(F, Y): content[(F, Y)] = Y; return (F, Y)
inchainQ = {}                                       # block target -> triangle read in-chain
readers = collections.Counter(); trusers = collections.defaultdict(list)
for t, (A3, Q1, Q2, P, o) in block_of.items():
    for Q in (Q1, Q2): trusers[(Q, A3)].append(t)
for t in sorted(block_of):
    A3, Q1, Q2, P, o = block_of[t]
    Q = min((Q1, Q2), key=lambda Q: (readers[(Q, A3)] > 0 and len(trusers[(Q, A3)]) - readers[(Q, A3)] <= 1, readers[(Q, A3)]))
    inchainQ[t] = Q; readers[(Q, A3)] += 1
Bperp = {A3: pm(A3) for A3 in blocks}
# optional deeper shared in-chain level: A3s grouped under a rank-4 frame F4 share sigma(F4-perp)
Bkey = {A3: (Bperp[A3], Bperp[A3]) for A3 in blocks}; Gkey = {}
if os.environ.get('HIER', '0') == '1':
    MINU = int(os.environ.get('HIERMIN', '2'))
    cand = collections.defaultdict(set)
    MAXR = int(os.environ.get('HIERRANK', '6'))
    for A, B in itertools.combinations(blocks, 2):
        F4 = fclosure(A | B)
        if lw.dim(F4) <= MAXR: cand[F4] |= {A, B}
    for F4 in list(cand):
        cand[F4] = {A for A in blocks if A & ~F4 == 0}
    good = {}
    for F4, As in cand.items():
        if len(As) < MINU: continue
        G = pm(F4)
        if G and nondegenerate(G) and all(G != Bperp[A] for A in As): good[F4] = (G, As)
    assigned = {}
    while True:
        best = None
        for F4, (G, As) in good.items():
            fr = [A for A in As if A not in assigned]
            if len(fr) < MINU: continue
            sc = (len(fr) - 1) * pc(G)
            if best is None or sc > best[0]: best = (sc, F4, G, fr)
        if best is None: break
        sc, F4, G, fr = best
        for A in fr: assigned[A] = G
    for A3, G in assigned.items():
        Gkey[A3] = (G, G); Bkey[A3] = (Bperp[A3], Bperp[A3] & ~G)
    log('HIER: A3s grouped', len(assigned), 'of', len(blocks), '| groups', len(set(assigned.values())),
        '| shared lines saved', sum(pc(G) for G in assigned.values()) - sum(pc(G) for G in set(assigned.values())))
for A3 in blocks:
    demand[dkey(*Bkey[A3])] += 1                                               # read-only shared register
    if A3 in Gkey: demand[dkey(*Gkey[A3])] = 1
for (Q, A3), us in trusers.items():
    E = pm(Q) & ~Bperp[A3]
    demand[dkey(pm(Q), E)] += max(1, len(us) - readers[(Q, A3)])
pair_users = collections.defaultdict(list)
for t, (A3, Q1, Q2, P, o) in block_of.items(): pair_users[(P, A3)].append(t)
for (P, A3), us in pair_users.items():
    demand[dkey(pm(P), pm(P) & ~Bperp[A3])] += len(us)
# leftovers: full sections, in-chain read if their defect is source-provided
luser = collections.defaultdict(list)
for t in left:
    for Q in choice[t][:3]: luser[Q].append(t)
lin = {}
lreaders = collections.Counter()
for t in left:
    if t in srcdef:
        Q = max(choice[t][:3], key=lambda Q: len(luser[Q]) - lreaders[Q])
        if len(luser[Q]) - lreaders[Q] >= 2: lin[t] = Q; lreaders[Q] += 1
for Q, us in luser.items():
    demand[dkey(pm(Q), pm(Q))] += max(1, len(us) - lreaders[Q])
TOPSET = set(demand)
log('top demands', len(demand), '| copies', sum(demand.values()), '| content lines', sum(pc(k[1]) for k in demand))
# ---- hierarchical pieces inside contents
children = collections.defaultdict(list); covered = collections.defaultdict(int)
frontier = list(demand); level = 0
if os.environ.get('PIECES') == 'paar':
    from paarpieces import paar_pieces
    TOPS0 = list(demand)
    seeds = None
    if os.environ.get('SEEDW') == '1':
        seeds = set()
        for A3 in blocks:
            Z = set()
            for u in bits(A3): Z |= set(g.supp[u])
            if len(Z) != 5: continue
            W = [i for i in range(11) if i not in Z]; Zl = sorted(Z)
            blk = []
            blk.append(sum(1 << g.P(x, y) for x, y in itertools.combinations(W, 2)))
            blk.append(sum(1 << g.T(x, y, z) for x, y, z in itertools.combinations(W, 3)))
            for z in Zl:
                blk.append(sum(1 << g.T(z, x, y) for x, y in itertools.combinations(W, 2)))
                blk.append(sum(1 << g.P(z, x) for x in W))
            for z1, z2 in itertools.combinations(Zl, 2):
                blk.append(sum(1 << g.T(z1, z2, x) for x in W))
            seeds.update(blk)
        seeds = sorted(seeds, key=lambda B: -pc(B))
    children, covered = paar_pieces(demand, content, log, seeds=seeds)
    if os.environ.get('MP', '1') == '1':
        from paarpieces import mp_refine
        children, covered = mp_refine(TOPS0, demand, content, children, covered, log)
    frontier = []
elif os.environ.get('GEN', '1') == '1':
    from genpieces import find_pieces
    children, covered = find_pieces(demand, content, log, minsize=int(os.environ.get('MINSIZE', '3')))
    frontier = []
while frontier:
    where = collections.defaultdict(list)
    fs = sorted(set(frontier), key=lambda k: pc(k[1]))
    for D in fs:
        Y = content[D]; L = bits(Y); cands = set()
        for a, b in itertools.combinations(L, 2):
            X = fclosure((1 << a) | (1 << b))
            if X & ~Y == 0 and X != Y: cands.add(X)
        if len(L) <= 30:
            for a, b, c in itertools.combinations(L, 3):
                X = fclosure((1 << a) | (1 << b) | (1 << c))
                if pc(X) >= 4 and X & ~Y == 0 and X != Y: cands.add(X)
        for X in cands: where[X].append(D)
    for D1, D2 in itertools.combinations(fs, 2):
        I = content[D1] & content[D2]
        if pc(I) >= 3:
            X = fclosure(I)
            if X & ~content[D1] == 0 and X & ~content[D2] == 0 and X != content[D1] and X != content[D2]:
                if D1 not in where[X]: where[X].append(D1)
                if D2 not in where[X]: where[X].append(D2)
    good = {X: w for X, w in where.items() if nondegenerate(X)}
    heap = [(-(len(w) - 1) * (pc(X) - 1), X) for X, w in good.items()]; heapq.heapify(heap)
    newf = []
    while heap:
        negs, X = heapq.heappop(heap)
        uses = [D for D in good[X] if covered[D] & X == 0]
        sc = (len(uses) - 1) * (pc(X) - 1)
        if sc <= 0: continue
        if sc < -negs: heapq.heappush(heap, (-sc, X)); continue
        K = dkey(X, X)
        for D in uses: covered[D] |= X; children[D].append(K)
        demand[K] += len(uses); newf.append(K)
    log('level', level, '| demands', len(fs), '| new pieces', len(newf))
    frontier = newf; level += 1
    if level > 6: break
HOP = os.environ.get('HOP', '0') == '1'
hops = {}                     # parent -> nested chain of children received at their own frames (no copy)
hopparents = collections.defaultdict(list)
if HOP:
    for D, ch in children.items():
        if not ch: continue
        cs = sorted(set(ch), key=lambda C: (lw.dim(C[0]), pc(C[1])))
        best = {}
        for i, C in enumerate(cs):
            b = (pc(C[1]), [C])
            for Cp in cs[:i]:
                if Cp[0] & ~C[0] == 0 and lw.dim(Cp[0]) < lw.dim(C[0]):
                    v = best[Cp]
                    if v[0] + pc(C[1]) > b[0]: b = (v[0] + pc(C[1]), v[1] + [C])
            best[C] = b
        chain = max(best.values(), key=lambda v: v[0])[1]
        if chain[-1][0] & ~D[0] == 0:
            hops[D] = chain
            for C in chain: hopparents[C].append(D)
    topkeys = set(k for k in demand if k not in content or True)
    for C, ps in hopparents.items():
        nonhop = demand[C] - len(ps)
        demand[C] = max(nonhop, 1)
    log('hops: parents with hop chains', len(hops), '| hop receptions', sum(len(v) for v in hops.values()),
        '| copies now', sum(demand.values()))
# ---- optional multi-output quad merges (qmerge.py)
quads = []; qparts = collections.defaultdict(list)
if os.environ.get('QMERGE') == '1':
    import qmerge
    QSET = list(demand) if os.environ.get('QALL') == '1' else list(TOPSET)
    quads, qterms = qmerge.plan(QSET, children, covered, content, lambda K: K[0], log, strict=[D for D in QSET if D not in TOPSET])
    for D in QSET:
        children[D] = [t[1] for t in qterms[D] if t[0] == 'P']
        qparts[D] = [(t[1], t[2]) for t in qterms[D] if t[0] == 'Q']
        cv = 0
        for C in children[D]: cv ^= content[C]
        for (i, v) in qparts[D]: cv ^= v
        assert all(t[0] in 'PQ' or True for t in qterms[D])
        covered[D] = cv
    for i, (X, inp, inl, outs) in enumerate(quads):
        children[('Q', i)] = list(inp)
QKEYS = [('Q', i) for i in range(len(quads))]
QFR = {('Q', i): quads[i][0] for i in range(len(quads))}
dlist = sorted(demand, key=lambda k: (lw.dim(k[0]), pc(k[1])))
# ---- assembly frame of each demand: its closure, or (PFRAME=max) the largest frame inside all its parents' frames
GFR = {D: D[0] for D in dlist}
if os.environ.get('PFRAME') == 'max':
    par = collections.defaultdict(list)
    for P, cs in children.items():
        for C in cs: par[C].append(P)
    for D in reversed(dlist):
        if D in TOPSET or not par[D]: continue
        M = FULL
        for P in par[D]: M &= GFR[P]
        if M != D[0] and M & D[0] == D[0] and nondegenerate(M): GFR[D] = M
    log('PFRAME=max: enlarged frames', sum(1 for D in dlist if GFR[D] != D[0]))
    dlist = sorted(demand, key=lambda k: (lw.dim(GFR[k]), pc(k[1])))
if quads:
    for q in QKEYS: GFR[q] = QFR[q]
    def _ord(K):
        if K in QFR: return (lw.dim(QFR[K]), 1, 0)
        return (lw.dim(GFR[K]), 2 if K in TOPSET else 0, pc(K[1]))
    dlist = sorted(list(demand) + QKEYS, key=_ord)
    # topological order (children and quads before their users), ties by _ord
    preds = collections.defaultdict(set)
    for P in dlist:
        for C in children[P]: preds[P].add(C)
        for (i, v) in qparts.get(P, []): preds[P].add(('Q', i))
    rank_ = {K: k for k, K in enumerate(dlist)}
    indeg = {K: len(preds[K]) for K in dlist}
    succ = collections.defaultdict(list)
    for P in dlist:
        for C in preds[P]: succ[C].append(P)
    ready = [(rank_[K], K) for K in dlist if indeg[K] == 0]; heapq.heapify(ready); out = []
    while ready:
        _, K = heapq.heappop(ready); out.append(K)
        for P in succ[K]:
            indeg[P] -= 1
            if indeg[P] == 0: heapq.heappush(ready, (rank_[P], P))
    assert len(out) == len(dlist), 'cycle in piece/quad DAG'
    dlist = out
# ---- line broadcast chains over host frames
uses_at = collections.defaultdict(lambda: collections.defaultdict(list))   # u -> frame -> [demands]
for D in dlist:
    if D in QFR:
        for u in quads[D[1]][2]: uses_at[u][QFR[D]].append(D)
        continue
    assert (content[D] ^ covered[D]) & ~GFR[D] == 0, 'residual lines outside frame'
    for u in bits(content[D] ^ covered[D]): uses_at[u][GFR[D]].append(D)
def chain_cover(frames):
    frames = sorted(set(frames), key=lambda F: (lw.dim(F), pc(F))); n0 = len(frames)
    adj = [[j for j in range(n0) if j != i and frames[i] & ~frames[j] == 0 and lw.dim(frames[i]) < lw.dim(frames[j])] for i in range(n0)]
    match_r = [-1] * n0
    def aug(i, seen):
        for j in adj[i]:
            if j in seen: continue
            seen.add(j)
            if match_r[j] < 0 or aug(match_r[j], seen): match_r[j] = i; return True
        return False
    for i in range(n0): aug(i, set())
    nxt = [-1] * n0
    for j in range(n0):
        if match_r[j] >= 0: nxt[match_r[j]] = j
    out = []
    for j in range(n0):
        if match_r[j] < 0:
            ch = [frames[j]]; k = j
            while nxt[k] >= 0: k = nxt[k]; ch.append(frames[k])
            out.append(ch)
    return out
lch = {u: chain_cover(list(uses_at[u])) for u in range(V)}
log('line uses', sum(len(D) for u in range(V) for D in uses_at[u].values()), '| frames', sum(len(uses_at[u]) for u in range(V)), '| chains', sum(len(c) for c in lch.values()))
# ---- optional piece broadcasting (PCHAIN=1): a piece register is read-only along a minimum chain cover of its
# parents' frames and consumed by the chain's last parent; one register per chain (master or copy), not per use
PCH = os.environ.get('PCHAIN') == '1'
prole = {}; pmaster = {}
if PCH:
    pidx = {D: k for k, D in enumerate(dlist)}
    pparents = collections.defaultdict(list)
    for P in dlist:
        hs = set(hops.get(P, []))
        for C in children[P]:
            if C in TOPSET or C in hs: continue
            pparents[C].append(P)
    nch = 0; nuse = 0
    for C, Ps in pparents.items():
        byF = collections.defaultdict(list)
        for P in Ps: byF[GFR[P]].append(P)
        seqs = []
        for ch in chain_cover(list(byF)):
            seq = []
            for F in ch: seq += sorted(byF[F], key=pidx.get)
            seqs.append(seq)
        pmaster[C] = max(range(len(seqs)), key=lambda k: pidx[seqs[k][0]])
        for k, seq in enumerate(seqs):
            for j, P in enumerate(seq):
                assert pidx[P] > pidx[C]
                prole[(P, C)] = (k, j == 0, j == len(seq) - 1)
        nch += len(seqs); nuse += len(Ps)
    log('PCHAIN: pieces', len(pparents), '| uses', nuse, '| chains', nch, '| copies saved', nuse - nch)
D10 = []
for i in range(11):
    m = 0
    for a, b in itertools.combinations([j for j in range(11) if j != i], 2): m |= (1 << g.P(a, b)) | (1 << g.T(a, b, i))
    D10.append(m)
def build(FEED, final):
    w = LWord(); dead = []
    kneed = sorted({choice[t][3] for t in left if choice[t][3] >= 0 and srcdef.get(t) != choice[t][3]})
    keeper = {}
    for d in kneed:
        h = w.helper('keeper'); w.gate(1 << d, h, [d]); keeper[d] = h
    bkeeper = {}
    for t, v in block_of.items():
        if srcdef.get(t) != v[4]:
            h = w.helper('keeper'); w.gate(1 << v[4], h, [v[4]]); bkeeper[t] = h
    for s in FEED:
        h = w.helper('feeder'); w.gate(1 << s, h, [s]); dead.append(h)
    bcast = collections.defaultdict(list); consume = collections.defaultdict(list)   # demand -> regs / (u, reg)
    for u in range(V):
        chs = lch[u]
        if not chs: continue
        src_i = None
        if u in provider:
            t = provider[u]
            ins = [i for i, ch in enumerate(chs) if all(F & ~HYP[t] == 0 for F in ch)]
            src_i = max(ins, key=lambda i: len(chs[i])) if ins else None
        else:
            src_i = max(range(len(chs)), key=lambda i: len(chs[i]))
        for i, ch in enumerate(chs):
            if i == src_i: r = u
            else:
                r = w.helper('carrier'); w.gate(1 << u, r, [u])
            pure = (r == u and u in provider)
            for j, F in enumerate(ch):
                Ds = uses_at[u][F]
                last = (j == len(ch) - 1) and not pure
                for k, D in enumerate(Ds):
                    if last and k == len(Ds) - 1: consume[D].append((u, r))
                    else: bcast[D].append(r)
    regs = {}; take = collections.Counter(); asm = {}
    LAZY = os.environ.get('LAZY', '1') == '1'
    pool = collections.defaultdict(list); master = {}; reused = set()
    uses_left = collections.Counter()
    for D in dlist:
        for C in children[D]:
            if C not in set(hops.get(D, [])): uses_left[C] += 1
    qout = {}
    creg = {}
    def chain_reg(P, C, F):
        k, first, last = prole[(P, C)]
        if first:
            if k == pmaster[C]: r = master[C]
            else:
                r = None; lst = pool.get(content[C], [])
                for k2, x in enumerate(lst):
                    if w.cur[x] & ~F == 0 and w.xpart(x) == content[C]:
                        r = x; del lst[k2]; reused.add(x); break
                if r is None:
                    r = w.helper('copy'); w.gate(GFR[C], r, [master[C]])
            creg[(C, k)] = r
        return creg[(C, k)], last
    for D in dlist:
        if D in QFR:
            i = D[1]; F = QFR[D]; X, inp, inl, outs = quads[i]
            ins = [r for (u, r) in consume[D]]
            bpc = {}
            for C in children[D]:
                if PCH:
                    r, last = chain_reg(D, C, F)
                    if last: ins.append(r)
                    else: bpc[C] = r
                    continue
                r = None; lst = pool.get(content[C], [])
                for k2, x in enumerate(lst):
                    if w.cur[x] & ~F == 0 and w.xpart(x) == content[C]:
                        r = x; del lst[k2]; reused.add(x); break
                uses_left[C] -= 1
                if r is None:
                    if uses_left[C] == 0: r = master[C]
                    else:
                        r = w.helper('copy'); w.gate(GFR[C], r, [master[C]])
                elif uses_left[C] == 0:
                    dead.append(master[C]); pool[content[C]].append(master[C])
                ins.append(r)
            bl = {u: r for (u, r) in [(w.xpart(r).bit_length() - 1, r) for r in bcast[D]]}
            targets = []
            for (Dt, v, tt) in outs:
                bpart = 0
                for t in tt:
                    if t[0] == 'L' and t[1] in bl: bpart |= 1 << t[1]
                    if t[0] == 'P' and t[1] in bpc: bpart ^= content[t[1]]
                targets.append(v ^ bpart)
            res, dd = frame_alg(w, F, ins, targets, 'quad')
            for k2, (Dt, v, tt) in enumerate(outs):
                r = res[k2]
                need = [bl[t[1]] for t in tt if t[0] == 'L' and t[1] in bl] + [bpc[t[1]] for t in tt if t[0] == 'P' and t[1] in bpc]
                if need: w.gate(F, r, need)
                assert w.xpart(r) == v
                qout[(i, Dt)] = r
            dead += dd
            for x in dd: pool[w.xpart(x)].append(x)
            continue
        F, Y = GFR[D], D[1]
        ins = [r for (u, r) in consume[D]]
        for (i, v) in qparts.get(D, []): ins.append(qout[(i, D)])
        hset = set(hops.get(D, []))
        bpc = []; bvec = 0
        for C in children[D]:
            if C in hset: continue
            if PCH and C not in TOPSET:
                r, last = chain_reg(D, C, F)
                if last: ins.append(r)
                else: bpc.append(r); bvec ^= content[C]
                continue
            if LAZY and C not in TOPSET:
                r = None; lst = pool.get(content[C], [])
                for i, x in enumerate(lst):
                    if w.cur[x] & ~F == 0 and w.xpart(x) == content[C]:
                        r = x; del lst[i]; reused.add(x); break
                uses_left[C] -= 1
                if r is None:
                    if uses_left[C] == 0: r = master[C]
                    else:
                        r = w.helper('copy'); w.gate(GFR[C], r, [master[C]])
                elif uses_left[C] == 0:
                    dead.append(master[C]); pool[content[C]].append(master[C])
                ins.append(r)
            else:
                ins.append(regs[C][take[C]]); take[C] += 1
        if D in asm: ins.append(asm[D])
        tv = covered[D]
        for (u, r) in consume[D]: tv ^= 1 << u
        tv ^= bvec
        nout = 1 if (LAZY and D not in TOPSET) else demand[D]
        if ins:
            res, dd = frame_alg(w, F, ins, [tv] * nout, 'flat')
        else:
            assert tv == 0
            res = {k: w.helper('empty@flat') for k in range(nout)}; dd = []
        regs[D] = [res[k] for k in range(nout)]; dead += dd
        if bpc:
            for r in regs[D]: w.gate(F, r, list(bpc))
        if LAZY and D not in TOPSET: master[D] = res[0]
        for x in dd: pool[w.xpart(x)].append(x)
        if bcast[D]:
            for r in regs[D]: w.gate(F, r, list(bcast[D]))
        # hop receptions: parents' assemblers read this piece at its own frame, before any copy of it climbs
        for P in hopparents.get(D, []):
            if P not in asm: asm[P] = w.helper('assembler')
            w.gate(F, asm[P], [regs[D][-1]])
    nh_top = w.nh
    dead = [r for r in dead if r not in reused]
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
    def reg_of(D, k): return regs[D][k]
    # phase B, in-chain reads first (registers still at their host frames)
    deliv = collections.defaultdict(list); used_idx = collections.Counter()
    for D in dlist: used_idx[D] = take[D]           # registers already consumed as children
    def next_reg(D):
        k = used_idx[D]; used_idx[D] += 1; return regs[D][k]
    rd_reg = {}
    for D in dlist:
        if D in regs and used_idx[D] < len(regs[D]): rd_reg[D] = regs[D][used_idx[D]]
    for t in range(V):
        if t in block_of:
            A3, Q1, Q2, P, o = block_of[t]
            Bp = Bperp[A3]
            if A3 in Gkey: w.gate(Gkey[A3][0], V + t, [rd_reg[Gkey[A3]]])
            w.gate(Bp, V + t, [rd_reg[Bkey[A3]]])
            Qi = inchainQ[t]
            DQ = (pm(Qi), pm(Qi) & ~Bp)
            w.gate(DQ[0], V + t, [rd_reg[DQ]])
        else:
            d = choice[t][3]
            if d >= 0 and srcdef.get(t) != d: w.gate(1 << d, V + t, [keeper[d]])
            if t in lin:
                Q = lin[t]; Dq = (pm(Q), pm(Q)); w.gate(Dq[0], V + t, [rd_reg[Dq]])
    # deliveries
    for A3 in blocks: used_idx[Bkey[A3]] += 1                   # the read-only registers are not delivered
    for K in set(Gkey.values()): used_idx[K] += 1
    for t in range(V):
        if t in block_of:
            A3, Q1, Q2, P, o = block_of[t]; Bp = Bperp[A3]
            Qo = Q2 if inchainQ[t] == Q1 else Q1
            regs_t = [next_reg((pm(Qo), pm(Qo) & ~Bp)), next_reg((pm(P), pm(P) & ~Bp)), o if srcdef.get(t) == o else bkeeper[t]]
        else:
            regs_t = [next_reg((pm(Q), pm(Q))) for Q in choice[t][:3] if lin.get(t) != Q]
            if t in srcdef: regs_t.append(srcdef[t])
        w.gate(HYP[t], V + t, regs_t)
    for t in range(V): assert w.xpart(V + t) == HYP[t], ('target content', t)
    w.finish()
    return w, [], dict(after_top=nh_top, R=w.nh)
w, missing, _ = build([], False)
log('pass 1: helpers before totals', w.nh, '| feeder lines', len(missing))
if os.environ.get('EVAL') == '1':
    print("EVAL {'R': %d}" % (w.nh + len(missing) + 11)); sys.exit(0)
w, _, stats = build(missing, True)
scatter = [[i for i in range(11) if g.binlabel(t) >> i & 1] for t in range(V)]
w.emit(scatter, [FULL] * 11, OUT)
log('EMITTED', OUT, stats, '| roles', dict(collections.Counter(w.role.values())))
