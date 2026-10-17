"""[build_blk_pairs.py = build_blk.py + PAIRS (per-frame pairing list) + optional HUBS stage (HUBMODE=hop|read);
 session 6c.  Best: PAIRS from word_blkA4 notes, PCHAIN=1 QMERGE=1 QALL=1 PIECES=paar HOP=0 MP=1 -> R = 3,656.]
BUILD (block top: frames sharing a cell-sum plane share Q at pm(W) and layers L(V) at pm(V); partner sources
accumulate deliveries).  Derived from build_f2hub.py; usage: build_blk.py BLOCKPART.pkl OUT.json.gz (blocks, punctured).
  Partition of the lines into good orthogonal
4-frames Phi = {t,a,b,c} (pairing (t,a),(b,c)) plus punctured lines.  For a good frame, with Q = lines _|_ Phi and
E_xy = lines _|_ x,y (not in Q, not frame lines):  R(t) = Q + E_ta + E_tb + E_tc + a + b + c  (disjoint).
Top registers per frame (6, + Q shared by every frame with the same Q):
  Q      at pm(Phi)   read in-chain by the 4 targets (and by every frame with the same pm, e.g. a star D4 block)
  IN_ta  at pm(t,a)   = E_ta + b + c, read in-chain by t and a;  IN_bc likewise
  X_tb, X_tc, X_ab, X_ac at pm(x,y) = E_xy.
Deliveries (sources accumulate in phase A):  source a reads X_tb at pm(t,b) -> t;  source t reads X_ac -> a;
  source c reads X_ab -> b;  source b reads X_tc -> c.  Final reads:  t: [a, X_tc]  a: [t, X_ab]  b: [c, X_tb]
  c: [b, X_ac].  Target chains: 0 -> pm(Phi) -> pm(t,a) -> t-perp.  Punctured targets: one R(t) register.
Middle as in build_a3g.py (Paar pieces, quad merges, piece chains, line chains).
usage: build_f2hub.py PART.pkl OUT.json.gz   (PART = (frames, punctured), frames as 4-tuples of line indices)"""
import sys, os, pickle, collections, itertools, time, heapq
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid'); sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lbuild')
import lw
from lw import V, g, bits, LWord, frame_alg, FULL, nondegenerate
from fastcl import fclosure
HYP = g.HYP; G = g.G
pc = lambda m: bin(m).count('1')
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
PARTF, OUT = sys.argv[1], sys.argv[2]
part = pickle.load(open(PARTF, 'rb'))
blocks0, punct = [list(b) for b in part[0]], list(part[1])   # blocks: lists of good frames sharing a cell-sum plane
PM = {}
def pm(m):
    r = PM.get(m)
    if r is None:
        r = FULL
        for s in bits(m): r &= HYP[s]
        PM[m] = r
    return r
B2 = lambda x, y: (1 << x) | (1 << y)
def vec(x):
    m = 0
    for i in g.supp[x]: m |= 1 << i
    if g.kind[x] == 'T': m |= 1 << 11
    return m
vv = [vec(x) for x in range(V)]
lineof = {vv[x]: x for x in range(V)}
fdot = lambda a, b: bin(a & b).count('1') & 1
def fspan(gens):
    S = {0}
    for x in gens: S |= {s ^ x for s in S}
    return S
def fN(Vs): return sum(1 << l for l in range(V) if all(fdot(vv[l], u) == 0 for u in Vs))
PAIR = int(os.environ.get('PAIR', '0'))
PAIRS = [int(c) for c in os.environ['PAIRS'].split(',')] if os.environ.get('PAIRS') else None
FR = []; blk_of = {}; BLK = []
for bi, fs in enumerate(blocks0):
    Wv = fspan([vv[x] for q in fs for x in q]); NW = fN(Wv)
    BLK.append(dict(W=Wv, NW=NW, Wlines=sum(1 << lineof[x] for x in Wv if x in lineof)))
    for q in fs:
        q = list(q); t = q[0]; others = q[1:]; a = others[PAIRS[len(FR)] if PAIRS else PAIR]; b, c = [x for x in others if x != a]
        FR.append((t, a, b, c)); blk_of[(t, a, b, c)] = bi
def hyper(Wv, x, y, U):
    """the two hyperplanes of W containing <x,y> other than U (F2 vector sets)"""
    out = []
    xs = [vv[x], vv[y]]
    rest = [w for w in Wv if w not in fspan(xs)]
    seen = set()
    for w in rest:
        S = frozenset(fspan(xs + [w]))
        if S != U and S not in seen: seen.add(S); out.append(S)
    return out
E = {}; LAY = {}; QF = {}
for f in FR:
    t, a, b, c = f; bk = BLK[blk_of[f]]; Wv = bk['W']
    U = frozenset(fspan([vv[t], vv[a], vv[b]])); Ul = B2(t, a) | B2(b, c)
    Q = pm(Ul)
    for x, y in itertools.combinations((t, a, b, c), 2):
        Exy = pm(B2(x, y)) & ~Q & ~Ul
        E[(x, y)] = E[(y, x)] = Exy
        if len(Wv) == 16:
            hs = hyper(Wv, x, y, U); assert len(hs) == 2
            ls = []
            for S in hs:
                Lv = fN(S) & ~bk['NW']; Sl = sum(1 << lineof[w] for w in S if w in lineof)
                assert Lv & ~pm(Sl) == 0, 'layer outside its real frame'
                ls.append((pm(Sl), Lv))
            assert ls[0][1] ^ ls[1][1] == Exy, 'E != L(V) + L(V\')'
            LAY[(x, y)] = LAY[(y, x)] = ls
    QF[f] = pm(bk['Wlines']) if len(Wv) == 16 else Q
    if len(Wv) == 16: assert QF[f] == Q, 'block Q differs from frame Q'
for f in FR:
    t, a, b, c = f
    for x in (t, a, b, c):
        o = [y for y in (t, a, b, c) if y != x]
        acc = 0
        for p in [QF[f], E[(x, o[0])], E[(x, o[1])], E[(x, o[2])], B2(o[0], o[1]) | (1 << o[2])]:
            assert acc & p == 0; acc |= p
        assert acc == HYP[x]
log('blocks', len(BLK), collections.Counter(len(b) for b in blocks0), '| frames', len(FR), '| punctured', len(punct), '| layered sections', len(LAY) // 2)
# ---- top demands
demand = collections.Counter(); content = {}
def dkey(F, Y): content[(F, Y)] = Y; return (F, Y)
topQ = {}; topIN = {}; topX = {}; topL1 = {}
EXPL = os.environ.get('EXPL') == '1'; expl = []
for f in FR:
    t, a, b, c = f
    topQ[f] = dkey(QF[f], QF[f]); demand[topQ[f]] = 1
    for (x, y, p, q) in ((t, a, b, c), (b, c, t, a)):
        if (x, y) in LAY:
            (F1, L1), (F2_, L2) = sorted(LAY[(x, y)], key=lambda z: (lw.dim(z[0]), z[0]))
            topL1[(x, y)] = dkey(F1, L1); demand[topL1[(x, y)]] = 1
            Y = L2 | B2(p, q)
        else:
            Y = E[(x, y)] | B2(p, q)
        topIN[(x, y)] = dkey(pm(B2(x, y)), Y)
        if EXPL and (x, y) in LAY:
            KL2 = dkey(F2_, L2); demand[KL2] += 0
            expl.append((topIN[(x, y)], [KL2], None))
        else:
            demand[topIN[(x, y)]] = 1
    for (x, y) in ((t, b), (t, c), (a, b), (a, c)):
        topX[(x, y)] = dkey(pm(B2(x, y)), E[(x, y)])
        if EXPL and (x, y) in LAY:
            ks = [dkey(Fl, Lv) for (Fl, Lv) in LAY[(x, y)]]
            for k in ks: demand[k] += 0
            expl.append((topX[(x, y)], ks, 'hop'))
        else:
            demand[topX[(x, y)]] = 1
topP = {}
for t in punct:
    topP[t] = dkey(HYP[t], HYP[t]); demand[topP[t]] += 1
acc = {}; deliv = {}
for (t, a, b, c) in FR:
    for (s, x, y, tgt, cons) in ((a, t, b, t, (t, c)), (t, a, c, a, (a, b)), (c, a, b, b, (t, b)), (b, t, c, c, (a, c))):
        acc[s] = (pm(B2(x, y)), topX[(x, y)], tgt)
        deliv[tgt] = (s, topX[cons])
for k in list(demand):
    if demand[k] == 0: demand[k] = 1          # layer pieces (EXPL): placeholder count, reset after Paar
TOPSET = set(demand)
log('top demands', len(demand), '| copies', sum(demand.values()), '| content lines', sum(pc(k[1]) for k in demand))

# ---- HUBS=1: one shared hub frame per consumer (top demand).  At hub Z the consumers with Z strictly inside their
# frame take E n Z; the parked registers are an F2 basis of those rows (chosen among the rows themselves); every user
# reads its combination at Z inside its own chain (hop), so a hub part costs rank(rows) registers, not one copy per
# user.  Residual contents go to the Paar middle; hub basis vectors are new demands at frame Z.
HUBS = os.environ.get('HUBS') == '1'
hubcov = {}; hubkids = {}
if HUBS:
    HMIN = float(os.environ.get('HUBMIN', '3'))
    HMODE = os.environ.get('HUBMODE', 'hop')
    xsrc = {acc[s_][1]: s_ for s_ in acc}; qkeys = set(topQ.values())
    tops_ = list(demand)
    prs = sorted(set((min(x, y), max(x, y)) for f in FR for x, y in itertools.combinations(f, 2)))
    def _perpF(Wm):
        m = FULL
        for s_ in bits(Wm): m &= HYP[s_]
        for p_ in punct: m &= ~(1 << p_)
        return fclosure(m) if m else 0
    candZ = set(); seenW = set()
    W2 = []
    for (a1, b1), (a2, b2) in itertools.combinations(prs, 2):
        Wm = fclosure(B2(a1, b1) | B2(a2, b2))
        if Wm in seenW: continue
        seenW.add(Wm)
        if lw.dim(Wm) > 6 or not nondegenerate(Wm): continue
        Z = _perpF(Wm)
        if Z and nondegenerate(Z): candZ.add(Z); W2.append(Wm)
    if os.environ.get('HUB3', '1') == '1':
        for Wm in W2:
            for (a3, b3) in prs:
                if (Wm >> a3) & 1 and (Wm >> b3) & 1: continue
                W3 = fclosure(Wm | B2(a3, b3))
                if W3 in seenW: continue
                seenW.add(W3)
                if lw.dim(W3) > 7 or not nondegenerate(W3): continue
                Z = _perpF(W3)
                if Z and nondegenerate(Z): candZ.add(Z)
    candZ = sorted(candZ)
    log('HUBS: candidate hub frames', len(candZ))
    def f2basis(rows):
        piv = {}; basis = []
        for x in rows:
            y = x
            while y:
                hb = y.bit_length() - 1
                if hb in piv: y ^= piv[hb]
                else: piv[hb] = y; basis.append(x); break
        return basis
    def express(x, basis):
        # coefficients of x in the basis (basis vectors independent)
        red = []
        for i, b in enumerate(basis):
            v = b; tag = 1 << i
            for (rv, rt) in red:
                if v ^ rv < v and (rv.bit_length() == v.bit_length()): v ^= rv; tag ^= rt
            red.append((v, tag))
        # simple Gaussian elimination with pivots
        piv = {}
        for v, tag in [(b, 1 << i) for i, b in enumerate(basis)]:
            while v:
                hb = v.bit_length() - 1
                if hb in piv: v ^= piv[hb][0]; tag ^= piv[hb][1]
                else: piv[hb] = (v, tag); break
        tag = 0; y = x
        while y:
            hb = y.bit_length() - 1
            assert hb in piv
            y ^= piv[hb][0]; tag ^= piv[hb][1]
        return [basis[i] for i in range(len(basis)) if tag >> i & 1]
    users = {}
    for Z in candZ:
        us = [D for D in tops_ if Z & ~D[0] == 0 and Z != D[0] and D[1] & Z]
        if HMODE == 'read': us = [D for D in us if (D in xsrc and (Z >> xsrc[D]) & 1) or D in qkeys]
        if len(us) >= 2: users[Z] = us
    assigned = set()
    def score(Z):
        rows = [D[1] & Z for D in users[Z] if D not in assigned]
        if len(rows) < 2: return 0.0
        return sum(pc(r) for r in rows) / len(f2basis(rows))
    pq = [(-score(Z), Z) for Z in users]; heapq.heapify(pq)
    nh_ = 0; inc_ = 0
    while pq:
        ns, Z = heapq.heappop(pq)
        sc = score(Z)
        if sc < HMIN: 
            if sc > 0 and pq and sc < -pq[0][0]: heapq.heappush(pq, (-sc, Z))
            if not pq or -pq[0][0] < HMIN: break
            continue
        if pq and sc < -pq[0][0] - 1e-9: heapq.heappush(pq, (-sc, Z)); continue
        us = [D for D in users[Z] if D not in assigned]
        rows = [D[1] & Z for D in us]
        basis = f2basis(rows)
        for D, r in zip(us, rows):
            comb = express(r, basis)
            ks = []
            for b in comb:
                K = (Z, b, 'hub'); content[K] = b; demand[K] = 1; ks.append(K)
            hubkids[D] = ks; hubcov[D] = r; assigned.add(D)
        nh_ += len(basis); inc_ += sum(pc(r) for r in rows)
    log('HUBS: hubs used', len(set(K[0] for ks in hubkids.values() for K in ks)), '| parked registers', nh_,
        '| consumers served', len(assigned), '| incidences', inc_)
    _saved_content = {}
    for D, r in hubcov.items():
        _saved_content[D] = content[D]; content[D] = D[1] ^ r
# ---- hierarchical pieces inside contents
children = collections.defaultdict(list); covered = collections.defaultdict(int)
frontier = list(demand); level = 0
if os.environ.get('PIECES') == 'paar':
    from paarpieces import paar_pieces
    TOPS0 = list(demand)
    seeds = None
    if os.environ.get('SEEDL') == '1':             # block layers (and Q) as seeded pieces
        seeds = set()
        for (x, y), ls in LAY.items():
            for (Fl, Lv) in ls: seeds.add(Lv)
        if os.environ.get('SEEDQ') == '1':
            for f in FR: seeds.add(QF[f])
        seeds = sorted(seeds, key=lambda B: -pc(B))
    elif os.environ.get('SEEDW') == '1':
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
        import paarpieces as _pp; _pp.EXCL = set(hubcov) if HUBS else set()
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
hops = {}
hopparents = collections.defaultdict(list)

if HUBS and os.environ.get('HUBMODE', 'hop') == 'read':
    pass                                         # tops keep the residual; readers take the hub parts at Z
elif HUBS:
    for D, r in hubcov.items():
        content[D] = _saved_content[D]; covered[D] ^= r
        children[D] = list(children[D]) + hubkids[D]
        hops[D] = list(hubkids[D])
        for K in hubkids[D]: hopparents[K].append(D)
if EXPL:
    layer_keys = set(k for (_, ks, _) in expl for k in ks)
    use_cons = collections.Counter(); use_ro = collections.Counter()
    for (D, ks, mode) in expl:
        demand[D] = 1; content[D] = D[1]
        cv = 0
        for k in ks: cv ^= content[k]
        if mode == 'hop':
            kh = max(ks, key=lambda k: (lw.dim(k[0]) < lw.dim(D[0]), pc(k[1])))
            assert kh[0] & ~D[0] == 0 and lw.dim(kh[0]) < lw.dim(D[0])
            hops[D] = [kh]; hopparents[kh].append(D); use_ro[kh] += 1
            children[D] = list(ks)
            for k in ks:
                if k != kh: use_cons[k] += 1
        else:
            children[D] = list(ks); use_cons[ks[0]] += 1
        covered[D] = cv
    l1keys = set(topL1.values())
    for k in layer_keys | l1keys:
        demand[k] = use_cons[k] + (1 if (use_ro[k] or k in l1keys) else 0)
        if demand[k] == 0: demand[k] = 1
    TOPSET = set(TOPSET) | set(e[0] for e in expl) | layer_keys | l1keys
    log('EXPL: explicit X/IN', len(expl), '| layer keys', len(layer_keys), '| hop reads', sum(use_ro.values()),
        '| consumed layer uses', sum(use_cons.values()), '| layer registers', sum(demand[k] for k in layer_keys | l1keys))
HOP = os.environ.get('HOP', '0') == '1'
if False:
    hops = {}                     # parent -> nested chain of children received at their own frames (no copy)
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
    if EXPL:
        _ex = set(e[0] for e in expl) | set(k for e in expl for k in e[1]) | set(topL1.values())
        QSET = [D for D in QSET if D not in _ex]
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
dlist = sorted(demand, key=lambda k: (lw.dim(k[0]), pc(k[1]), len(k)))
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
    if len(out) != len(dlist):
        left_ = [K for K in dlist if indeg[K] > 0]
        # walk predecessors to find a cycle
        K = left_[0]; seen_ = []
        while K not in seen_:
            seen_.append(K); K = next(C for C in preds[K] if indeg.get(C, 0) > 0)
        cyc = seen_[seen_.index(K):]
        def tag(K):
            if K in QFR: return 'QUAD%d' % K[1]
            return ('EXPL' if K in set(e[0] for e in expl) else 'LAYER' if any(K in e[1] for e in expl) else 'TOP' if K in TOPSET else 'piece') + ':%d' % pc(K[1])
        print('CYCLE', [tag(K) for K in cyc])
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
                if not pidx[P] > pidx[C]:
                    print('ORDER P', len(P), lw.dim(P[0]), pc(P[1]), P in TOPSET, 'C', len(C), lw.dim(C[0]), pc(C[1]), C in TOPSET, 'Csub', C[1] & ~P[1] == 0, 'Cframe in P', C[0] & ~P[0] == 0)
                assert pidx[P] > pidx[C]
                prole[(P, C)] = (k, j == 0, j == len(seq) - 1)
        nch += len(seqs); nuse += len(Ps)
    log('PCHAIN: pieces', len(pparents), '| uses', nuse, '| chains', nch, '| copies saved', nuse - nch)
D10 = []
for i in range(11):
    m = 0
    for a, b in itertools.combinations([j for j in range(11) if j != i], 2): m |= (1 << g.P(a, b)) | (1 << g.T(a, b, i))
    D10.append(m)
CDBG = {}
def build(FEED, final):
    w = LWord(); dead = []
    for s in FEED:
        h = w.helper('feeder'); w.gate(1 << s, h, [s]); dead.append(h)
    bcast = collections.defaultdict(list); consume = collections.defaultdict(list)   # demand -> regs / (u, reg)
    for u in range(V):
        chs = lch[u]
        if not chs: continue
        if u in acc:
            AF = acc[u][0]
            if HUBS and acc[u][1] in hubkids and hubkids[acc[u][1]] and os.environ.get('HUBMODE', 'hop') == 'read':
                AF = hubkids[acc[u][1]][0][0]
            ins = [i for i, ch in enumerate(chs) if all(F & ~AF == 0 for F in ch)]
            src_i = max(ins, key=lambda i: len(chs[i])) if ins else None
        else:
            src_i = max(range(len(chs)), key=lambda i: len(chs[i]))
        for i, ch in enumerate(chs):
            if i == src_i: r = u
            else:
                r = w.helper('carrier'); w.gate(1 << u, r, [u])
            pure = (r == u and u in acc)
            CDBG[r] = (u, i, [(lw.dim(F), [('T' if D in TOPSET else 'K' if D[1] == content.get(D) and any(D in v for v in hubkids.values()) else 'p', pc(D[1])) for D in uses_at[u][F]]) for F in ch])
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
            try:
                res, dd = frame_alg(w, F, ins, [tv] * nout, 'flat')
            except AssertionError as e:
                bad = [r for r in ins if w.cur[r] & ~F != 0]
                print('DEBUG D frame dim', lw.dim(F), 'content', pc(D[1]), 'hub' if D in hubcov else '', 'hubpiece' if any(D in v for v in hubkids.values()) else '', 'top' if D in TOPSET else '')
                for C in children[D]:
                    print('   child', len(C), lw.dim(C[0]), pc(C[1]), 'top' if C in TOPSET else '', 'hop' if C in hset else '', 'frame-in' if C[0] & ~F == 0 else 'FRAME-OUT', 'regs', regs.get(C), master.get(C))
                print('   consume', [(u, r) for (u, r) in consume[D]][:10], 'asm', asm.get(D), 'qparts', qparts.get(D))
                for r in bad: print('  chain', CDBG.get(r)); print('  reg', r, w.role.get(r), 'cur dim', lw.dim(w.cur[r]), 'path dims', [lw.dim(x) for x in w.path[r]], 'sub?', w.cur[r] & ~F == 0)
                raise
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
    for s, (F, D, tgt) in acc.items():                              # sources accumulate their X part
        for K in (hubkids.get(D, []) if HUBS else []): w.gate(K[0], s, [regs[K][0]])
        w.gate(F, s, [regs[D][take[D]]])
    nh_top = w.nh
    dead = [r for r in dead if r not in reused]
    red = {}
    for r in dead:
        vec = w.xpart(r); comb = {r}
        while vec:
            hb = vec.bit_length() - 1
            if hb in red: vec ^= red[hb][0]; comb = comb ^ red[hb][1]
            else: red[hb] = (vec, comb); break
    missing = []; totals = []; RETF.clear()
    for i in range(11):
        x = D10[i]; comb = set()
        while x:
            hb = x.bit_length() - 1
            if hb not in red: missing.append(hb); red[hb] = (1 << hb, {('feed', hb)})
            x ^= red[hb][0]; comb ^= red[hb][1]
        if final:
            assert not any(isinstance(c, tuple) for c in comb)
            h = w.helper('total'); F10 = lw.closure(D10[i])
            ok10 = nondegenerate(F10) and all((w.cur[r] & ~F10) == 0 for r in comb)
            Fsel = F10 if (ok10 and os.environ.get('D10RET', '1') == '1') else FULL
            w.gate(Fsel, h, sorted(comb)); totals.append(h); RETF.append(Fsel)
            log('total', i, 'operands', len(comb), 'at D10 frame' if Fsel != FULL else 'at FULL', 'bad operands', sum(1 for r in comb if (w.cur[r] & ~F10) != 0))
    if not final: return w, sorted(set(missing)), None
    w.ret = totals; w.phase = 'B'
    for f in FR:                                                    # in-chain reads (shared registers)
        t, a, b, c = f
        for (x, y) in ((t, a), (b, c)):
            for z in (x, y):
                DQ = topQ[f]
                for K in (hubkids.get(DQ, []) if HUBS else []): w.gate(K[0], V + z, [regs[K][0]])
                w.gate(DQ[0], V + z, [regs[DQ][take[DQ]]])
                if (x, y) in topL1:
                    DL = topL1[(x, y)]; w.gate(DL[0], V + z, [regs[DL][take[DL]]])
                DI = topIN[(x, y)]; w.gate(DI[0], V + z, [regs[DI][take[DI]]])
    for (t, a, b, c) in FR:
        for z in (t, a, b, c):
            s, DX = deliv[z]
            w.gate(HYP[z], V + z, [s, regs[DX][take[DX]]])
    for t in punct:
        w.gate(HYP[t], V + t, [regs[topP[t]][take[topP[t]]]])
    for t in range(V): assert w.xpart(V + t) == HYP[t], ('target content', t)
    w.finish()
    return w, [], dict(after_top=nh_top, R=w.nh)
RETF = []
w, missing, _ = build([], False)
log('pass 1: helpers before totals', w.nh, '| feeder lines', len(missing))
if os.environ.get('EVAL') == '1':
    print("EVAL {'R': %d}" % (w.nh + len(missing) + 11), dict(collections.Counter(w.role.values()))); sys.exit(0)
w, _, stats = build(missing, True)
scatter = [[i for i in range(11) if g.binlabel(t) >> i & 1] for t in range(V)]
w.emit(scatter, list(RETF), OUT)
log('EMITTED', OUT, stats, '| roles', dict(collections.Counter(w.role.values())))
