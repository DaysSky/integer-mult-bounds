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
