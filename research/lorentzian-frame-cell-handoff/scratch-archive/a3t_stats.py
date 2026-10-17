"""BUILD (telescoped A3 blocks): block target t (A3 block B, triangles Q1,Q2 through t, opposite o) reads along its
chain 0 -> B-perp -> Q1-perp -> t-perp:  sigma(B-perp) at B-perp (ONE register read by all 6 block targets),
sigma(E_Q1) at Q1-perp (E_Q = Q-perp minus B-perp, shared by the triangle's users), and at t-perp the deliveries
sigma(E_Q2), sigma(E_pair) plus the PURE source of o (mutual opposites).  Parity: B-perp lies in all three sections.
Leftover targets: full plane sections + keeper (or provider source) as in build_a3b.py.
Middle: demands (host frame F, content Y), hierarchical shared flat pieces inside contents, line values broadcast
along exact minimum chain covers (read-only, consumed at chain ends).  usage: build_a3t.py CHOICE.pkl OUT.json.gz"""
import sys, os, pickle, collections, itertools, time, heapq
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid'); sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lbuild')
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
block_of = {t: v for t, v in block_of.items() if len(bl_members[v[0]]) == 6}
blocks = sorted({v[0] for v in block_of.values()})
left = [t for t in range(V) if t not in block_of]
log('complete A3 blocks', len(blocks), '| block targets', len(block_of), '| leftover', len(left))
# ---- providers (pure sources): block opposites (mutual); then leftovers' defects if free
provider = {}
for t, (A3, Q1, Q2, P, o) in block_of.items(): provider[o] = t
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
    for Q in (Q1, Q2): trusers[Q].append(t)
for t in sorted(block_of):
    A3, Q1, Q2, P, o = block_of[t]
    Q = min((Q1, Q2), key=lambda Q: readers[Q])
    inchainQ[t] = Q; readers[Q] += 1
Bperp = {A3: pm(A3) for A3 in blocks}
for A3 in blocks: demand[dkey(Bperp[A3], Bperp[A3])] += 1                      # read-only shared register
for Q, us in trusers.items():
    A3 = block_of[us[0]][0]
    E = pm(Q) & ~Bperp[A3]
    demand[dkey(pm(Q), E)] += max(1, len(us) - readers[Q])
pair_users = collections.defaultdict(list)
for t, (A3, Q1, Q2, P, o) in block_of.items(): pair_users[P].append(t)
for P, us in pair_users.items():
    A3 = block_of[us[0]][0]
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
topset = set(demand); log('top demands', len(demand), '| copies', sum(demand.values()), '| content lines', sum(pc(k[1]) for k in demand))
# ---- hierarchical pieces inside contents
children = collections.defaultdict(list); covered = collections.defaultdict(int)
frontier = list(demand); level = 0
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
dlist = sorted(demand, key=lambda k: (lw.dim(k[0]), pc(k[1])))
STAT = collections.defaultdict(collections.Counter)
# ---- line broadcast chains over host frames
uses_at = collections.defaultdict(lambda: collections.defaultdict(list))   # u -> frame -> [demands]
for D in dlist:
    for u in bits(content[D] & ~covered[D]): uses_at[u][D[0]].append(D)
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
    regs = {}; take = collections.Counter()
    for D in dlist:
        F, Y = D
        ins = [r for (u, r) in consume[D]]
        for C in children[D]: ins.append(regs[C][take[C]]); take[C] += 1
        tv = covered[D]
        for (u, r) in consume[D]: tv |= 1 << u
        nh0 = w.nh
        res, dd = frame_alg(w, F, ins, [tv] * demand[D], 'flat')
        if final:
            lev = 'top' if D in topset else 'piece'
            STAT[lev]['n'] += 1; STAT[lev]['k'] += demand[D]; STAT[lev]['s_lines'] += len(consume[D]); STAT[lev]['s_child'] += len(children[D])
            STAT[lev]['new'] += w.nh - nh0; STAT[lev]['dead'] += len(dd); STAT[lev]['bcast'] += len(bcast[D])
            STAT[lev]['content'] += pc(Y)
        regs[D] = [res[k] for k in range(demand[D])]; dead += dd
        if bcast[D]:
            for r in regs[D]: w.gate(F, r, list(bcast[D]))
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
    def reg_of(D, k): return regs[D][k]
    # phase B, in-chain reads first (registers still at their host frames)
    deliv = collections.defaultdict(list); used_idx = collections.Counter()
    for D in dlist: used_idx[D] = take[D]           # registers already consumed as children
    def next_reg(D):
        k = used_idx[D]; used_idx[D] += 1; return regs[D][k]
    rd_reg = {}
    for D in dlist:
        if used_idx[D] < len(regs[D]): rd_reg[D] = regs[D][used_idx[D]]
    for t in range(V):
        if t in block_of:
            A3, Q1, Q2, P, o = block_of[t]
            Bp = Bperp[A3]
            w.gate(Bp, V + t, [rd_reg[(Bp, Bp)]])
            Qi = inchainQ[t]
            DQ = (pm(Qi), pm(Qi) & ~Bp)
            w.gate(DQ[0], V + t, [rd_reg[DQ]])
        else:
            d = choice[t][3]
            if d >= 0 and srcdef.get(t) != d: w.gate(1 << d, V + t, [keeper[d]])
            if t in lin:
                Q = lin[t]; Dq = (pm(Q), pm(Q)); w.gate(Dq[0], V + t, [rd_reg[Dq]])
    # deliveries
    for A3 in blocks: used_idx[(Bperp[A3], Bperp[A3])] += 1     # the read-only register is not delivered
    for t in range(V):
        if t in block_of:
            A3, Q1, Q2, P, o = block_of[t]; Bp = Bperp[A3]
            Qo = Q2 if inchainQ[t] == Q1 else Q1
            regs_t = [next_reg((pm(Qo), pm(Qo) & ~Bp)), next_reg((pm(P), pm(P) & ~Bp)), o]
        else:
            regs_t = [next_reg((pm(Q), pm(Q))) for Q in choice[t][:3] if lin.get(t) != Q]
            if t in srcdef: regs_t.append(srcdef[t])
        w.gate(HYP[t], V + t, regs_t)
    for t in range(V): assert w.xpart(V + t) == HYP[t], ('target content', t)
    w.finish()
    return w, [], dict(after_top=nh_top, R=w.nh)
w, missing, _ = build([], False)
log('pass 1: helpers before totals', w.nh, '| feeder lines', len(missing))
w, _, stats = build(missing, True)
scatter = [[i for i in range(11) if g.binlabel(t) >> i & 1] for t in range(V)]
print({k: dict(v) for k, v in STAT.items()})
log('EMITTED', OUT, stats, '| roles', dict(collections.Counter(w.role.values())))
