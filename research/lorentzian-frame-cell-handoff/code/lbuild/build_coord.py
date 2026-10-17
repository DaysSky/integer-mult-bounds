"""BUILD (coordinate-aligned top): every read is a full flat sum of a coordinate / star flat, so shared sub-flats
(K_a(U), L(U), A(U)) are large and nest across targets.
  T(abc), S8 = [11] - abc:  HYP = N_a + N_b + N_c,  N_a = K_a(S8) u {P(bc)}  (K_a(S) = {P(xy), T(axy): x,y in S});
     N_a is a closed nondegenerate rank-9 flat inside T(abc)-perp; the three are delivered.
  P(ab), paired with a disjoint P(zw) (mutual opposites):  HYP = A2(abz)-perp + A2(abw)-perp + {P(ab),P(zw)}-perp
     + P(zw) (A3-parity on the P-type A3 on {a,b,z,w}); one triangle section read in-chain (shared by every in-chain
     reader of that triangle, later delivered to a delivered user), the other triangle section and the pair section
     delivered, the opposite's source read pure at t-perp.  The odd P line takes a keeper for its opposite.
Middle as build_a3t.py: hierarchical shared flat pieces inside contents, line values broadcast along exact minimum
chain covers (read-only, consumed at chain ends).  usage: build_coord.py OUT.json.gz [SEED]"""
import sys, os, collections, itertools, time, heapq, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lmid'))
import lw
from lw import V, g, bits, LWord, frame_alg, FULL, nondegenerate
from fastcl import fclosure
HYP = g.HYP
pc = lambda m: bin(m).count('1')
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
OUT = sys.argv[1]
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1
N = 11
PM = {}
def pm(m):
    r = PM.get(m)
    if r is None:
        r = FULL
        for s in bits(m): r &= HYP[s]
        PM[m] = r
    return r
def Kset(a, S):
    m = 0
    for x, y in itertools.combinations(sorted(S), 2): m |= (1 << g.P(x, y)) | (1 << g.T(a, x, y))
    return m
def A2(a, b, c): return (1 << g.P(a, b)) | (1 << g.P(a, c)) | (1 << g.P(b, c))
# ---------------- top ----------------
demand = collections.Counter()
reads = {}                     # t -> dict(inchain=[(F, D)], deliv=[D], src=[s], keep=[s])
# T targets
for t in range(V):
    if g.kind[t] != 'T': continue
    abc = g.supp[t]; S8 = [i for i in range(N) if i not in abc]
    ds = []
    for i in range(3):
        a = abc[i]; b, c = [x for x in abc if x != a]
        Y = Kset(a, S8) | (1 << g.P(b, c))
        assert fclosure(Y) == Y and nondegenerate(Y) and Y & ~HYP[t] == 0
        D = (Y, Y); demand[D] += 1; ds.append(D)
    tot = 0
    for D in ds: tot ^= D[1]
    assert tot == HYP[t]
    reads[t] = dict(inchain=[], deliv=ds, src=[], keep=[])
# P targets: matching into disjoint pairs, then in-chain triangle choice
rng = random.Random(SEED)
Plines = [t for t in range(V) if g.kind[t] == 'P']
def tri_cost(match, choice):
    d = collections.Counter(); i = collections.Counter()
    for t, (Qin, Qdel) in choice.items(): i[Qin] += 1; d[Qdel] += 1
    return sum(d.values()) + sum(1 for Q in i if d[Q] == 0)
def best_choice(match):
    # each P(ab) with partner P(zw): triangles abz, abw; pick in-chain one so in-chain triangles have a delivered user
    opts = {}
    for t, u in match.items():
        a, b = g.supp[t]; z, w = g.supp[u]
        opts[t] = (A2(a, b, z), A2(a, b, w))
    choice = {t: (o[0], o[1]) for t, o in opts.items()}
    cur = tri_cost(match, choice)
    for _ in range(20):
        imp = False
        for t in opts:
            alt = dict(choice); alt[t] = (choice[t][1], choice[t][0])
            c = tri_cost(match, alt)
            if c < cur: choice, cur, imp = alt, c, True
        if not imp: break
    return choice, cur
best = None
for trial in range(300):
    order = Plines[:]; rng.shuffle(order); match = {}; free = set(order)
    for t in order:
        if t not in free: continue
        cand = [u for u in order if u in free and u != t and not set(g.supp[t]) & set(g.supp[u])]
        if not cand: continue
        u = cand[0]; match[t] = u; match[u] = t; free -= {t, u}
    choice, cost = best_choice(match)
    if best is None or (len(free), cost) < best[0]: best = ((len(free), cost), match, choice, set(free))
(_, tcost), match, choice, leftP = best[0], best[1], best[2], best[3]
log('P matching: pairs', len(match) // 2, '| unmatched', len(leftP), '| triangle-section registers', tcost)
keepers_needed = []
for t in Plines:
    if t in match:
        u = match[t]; Qin, Qdel = choice[t]
    else:
        a, b = g.supp[t]
        u = next(x for x in Plines if not set(g.supp[x]) & {a, b})
        z, w = g.supp[u]; Qin, Qdel = A2(a, b, z), A2(a, b, w)
        keepers_needed.append((t, u))
    Pp = (1 << t) | (1 << u)
    Din = (pm(Qin), pm(Qin)); Dd = (pm(Qdel), pm(Qdel)); DP = (pm(Pp), pm(Pp))
    assert (Din[1] ^ Dd[1] ^ DP[1] ^ (1 << u)) == HYP[t], 'P parity'
    reads[t] = dict(inchain=[Din], deliv=[Dd, DP], src=[u] if t in match else [], keep=[] if t in match else [u])
inreaders = collections.Counter(); delusers = collections.Counter()
for t, r in reads.items():
    for D in r['inchain']: inreaders[D] += 1
    for D in r['deliv']: delusers[D] += 1
for D in set(inreaders) | set(delusers):
    if delusers[D] or inreaders[D]:
        demand[D] = max(1, delusers[D])
content = {D: D[1] for D in demand}
for D in demand: assert nondegenerate(D[0]), 'degenerate frame'
log('top demands', len(demand), '| copies', sum(demand.values()), '| content lines', sum(pc(k[1]) for k in demand))
# ---------------- middle: hierarchical pieces ----------------
def dkey(F, Y): content[(F, Y)] = Y; return (F, Y)
children = collections.defaultdict(list); covered = collections.defaultdict(int)
frontier = list(demand); level = 0
if os.environ.get('PIECES') == 'paar':
    from paarpieces import paar_pieces
    children, covered = paar_pieces(demand, content, log)
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
        for X in cands: where[X].append(D)
    for D1, D2 in itertools.combinations(fs, 2):
        I = content[D1] & content[D2]
        if pc(I) >= 3:
            X = fclosure(I)
            if X & ~content[D1] == 0 and X & ~content[D2] == 0 and X != content[D1] and X != content[D2]:
                if D1 not in where[X]: where[X].append(D1)
                if D2 not in where[X]: where[X].append(D2)
    good = {X: w for X, w in where.items() if nondegenerate(X)}
    BYSIZE = os.environ.get('PIECEORDER', 'size') == 'size'
    MINP = int(os.environ.get('MINPIECE', '4'))
    if BYSIZE: good = {X: w for X, w in good.items() if pc(X) >= MINP or level >= 2}
    heap = [((-pc(X), -(len(w) - 1)) if BYSIZE else (-(len(w) - 1) * (pc(X) - 1), -pc(X)), X) for X, w in good.items()]
    heapq.heapify(heap)
    newf = []
    while heap:
        key, X = heapq.heappop(heap)
        uses = [D for D in good[X] if covered[D] & X == 0]
        sc = (len(uses) - 1) * (pc(X) - 1)
        if sc <= 0: continue
        if BYSIZE:
            if len(uses) < len([D for D in good[X]]) and (-pc(X), -(len(uses) - 1)) != key:
                heapq.heappush(heap, ((-pc(X), -(len(uses) - 1)), X)); continue
        elif sc < -key[0]: heapq.heappush(heap, ((-sc, -pc(X)), X)); continue
        K = dkey(X, X)
        for D in uses: covered[D] |= X; children[D].append(K)
        demand[K] += len(uses); newf.append(K)
    log('level', level, '| demands', len(fs), '| new pieces', len(newf), '| piece sizes',
        dict(sorted(collections.Counter(pc(k[1]) for k in newf).items(), reverse=True)[:8]))
    frontier = newf; level += 1
    if level > 8: break
dlist = sorted(demand, key=lambda k: (lw.dim(k[0]), pc(k[1])))
# ---------------- line broadcast chains ----------------
uses_at = collections.defaultdict(lambda: collections.defaultdict(list))
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
log('line uses', sum(len(D) for u in range(V) for D in uses_at[u].values()), '| frames',
    sum(len(uses_at[u]) for u in range(V)), '| chains', sum(len(c) for c in lch.values()))
# pure-source discipline: a source read pure at its opposite's t-perp keeps one chain inside that target's perp
srcreader = {}
for t, r in reads.items():
    for s in r['src']: srcreader[s] = t
D10 = []
for i in range(11):
    m = 0
    for a, b in itertools.combinations([j for j in range(11) if j != i], 2): m |= (1 << g.P(a, b)) | (1 << g.T(a, b, i))
    D10.append(m)
def build(FEED, final):
    w = LWord(); dead = []
    keeper = {}
    for (t, u) in keepers_needed:
        h = w.helper('keeper'); w.gate(1 << u, h, [u]); keeper[t] = h
    for s in FEED:
        h = w.helper('feeder'); w.gate(1 << s, h, [s]); dead.append(h)
    bcast = collections.defaultdict(list); consume = collections.defaultdict(list)
    for u in range(V):
        chs = lch[u]
        if not chs: continue
        if u in srcreader:
            t = srcreader[u]
            ins = [i for i, ch in enumerate(chs) if all(F & ~HYP[t] == 0 for F in ch)]
            src_i = max(ins, key=lambda i: len(chs[i])) if ins else None
        else:
            src_i = max(range(len(chs)), key=lambda i: len(chs[i]))
        for i, ch in enumerate(chs):
            if i == src_i: r = u
            else:
                r = w.helper('carrier'); w.gate(1 << u, r, [u])
            pure = (r == u and u in srcreader)
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
        res, dd = frame_alg(w, F, ins, [tv] * demand[D], 'flat')
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
    used_idx = collections.Counter()
    for D in dlist: used_idx[D] = take[D]
    def next_reg(D):
        k = used_idx[D]; used_idx[D] += 1; return regs[D][k]
    rd_reg = {D: regs[D][used_idx[D]] for D in dlist if used_idx[D] < len(regs[D])}
    for t in range(V):                                   # in-chain reads first
        for D in reads[t]['inchain']: w.gate(D[0], V + t, [rd_reg[D]])
    for t in range(V):
        regs_t = [next_reg(D) for D in reads[t]['deliv']] + list(reads[t]['src']) + [keeper[t] for u in reads[t]['keep']]
        w.gate(HYP[t], V + t, regs_t)
    for t in range(V): assert w.xpart(V + t) == HYP[t], ('target content', t)
    w.finish()
    return w, [], dict(after_top=nh_top, R=w.nh)
w, missing, _ = build([], False)
log('pass 1: helpers before totals', w.nh, '| feeder lines', len(missing))
w, _, stats = build(missing, True)
scatter = [[i for i in range(11) if g.binlabel(t) >> i & 1] for t in range(V)]
w.emit(scatter, [FULL] * 11, OUT)
log('EMITTED', OUT, stats, '| roles', dict(collections.Counter(w.role.values())))
