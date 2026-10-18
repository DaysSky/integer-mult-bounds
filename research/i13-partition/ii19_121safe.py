"""THE ROOM-SAFE RE-SLOT (the user's SS1601 'no keep pushing'!!; the recursion insight SS1616-1619!!).

THE PROBLEM: the naive cumulative slots produce the GIANT TRANSITIVE COMPONENTS (the
per-dim read graphs' closures merge targets via the shared pieces + the co-reads: the
(165, 102)-rooms FAIL the perp-existence!!).  THE COMPOSITE FIX RECURSES (the composites'
own builds hit the same merge at the src-side!!).  THE E8'S SOLUTION: THE JOINT ROOM-FLAG
(the co-read sets ARE the D4 structures: the perp-safety BY CONSTRUCTION!!).

THE MEASUREMENT: THE ROOM-AWARE RE-SLOT: assign the pieces to the dims such that the
per-dim components stay PERP-SAFE (each component's pieces' union ⊆ the COMMON PERP of
the component's targets!!):
- the greedy: the pieces sorted by the user-count desc; for each piece: try the dims
  (>= the piece's span!!): the placement at d: the incremental per-dim component check:
  the piece's users' components at d: the merged component: the union + the piece ⊆
  the merged targets' common perp?!  IF NO SAFE DIM: THE PIECE IS ROOM-UNSAFE -> the
  composite fallback (the per-target merge registers: the R cost!!).
- THE OUTPUT: the unplaced/unsafe counts, the perp-safe rooms' statistics, the R_struct
  (pool + the composites + the carriers + 9!!), the demand, the (c)-hist, THE PRICE (do
  the SS1594 crossings survive the room-safe redesign?!).
"""
import sys, time, itertools
from collections import Counter
import numpy as np
from mpmath import mp
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
mp.dps = 40

FRONTIER = 0.001744386
V, H = 121, 9
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# the system [the sweep's code!!]
roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                roots.append(v)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
d8 = {}
for r in list(roots) + half: d8[canon(r)] = np.array(r)
AL = list(d8.values())
L = np.array([list(al) + [0, 0] for al in AL] + [[0.0] * 8 + [1.0, 1.0]])
FORM = np.zeros((10, 10)); FORM[:8, :8] = np.eye(8); FORM[8, 9] = FORM[9, 8] = 1.0
G = L @ FORM @ L.T
PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)
jlines = [[s for s in range(V) if (PERP[t] >> s) & 1] for t in range(V)]
_sr = {}
def span_rank(ids):
    key = tuple(sorted(ids))
    if key not in _sr:
        _sr[key] = int(np.linalg.matrix_rank(L[list(key)])) if key else 0
    return _sr[key]

pair_count = Counter(); pair_junks = {}
for ti, jl in enumerate(jlines):
    for a, b in itertools.combinations(sorted(jl), 2):
        pair_count[(a, b)] += 1
        pair_junks.setdefault((a, b), []).append(ti)
top = [(c, k) for k, c in pair_count.items() if c >= 4]

def jumps(ch):
    ch = sorted(set(ch))
    return [b - a for a, b in zip(ch, ch[1:])]

log('TH | the re-slot: unsafe/fallback | the safe rooms | R_struct dem R_hon | LM | coarse | fine')
for TH in (8, 16, 24):
    covered = [set() for _ in range(V)]; assigned = [[] for _ in range(V)]
    pool = []; pool_users = []
    while True:
        best = None
        for (c, (a, b)) in top:
            users = [ti for ti in pair_junks[(a, b)] if a not in covered[ti] and b not in covered[ti]]
            if len(users) < 2:
                continue
            common = None
            for ti in users:
                unc = set(jlines[ti]) - covered[ti]
                common = unc if common is None else (common & unc)
            if common is None or len(common) < 2:
                continue
            piece = frozenset(common)
            real_users = [ti for ti in users if piece <= set(jlines[ti]) - covered[ti]]
            k = len(piece); u = len(real_users)
            if u < 2:
                continue
            saving = k * u - (k + u)
            if saving <= 0:
                continue
            if best is None or saving > best[0]:
                best = (saving, piece, real_users)
        if best is None or best[0] < TH:
            break
        _, piece, real_users = best
        pool.append(piece); pool_users.append(real_users)
        for ti in real_users:
            covered[ti] |= set(piece); assigned[ti].append(len(pool) - 1)
    leftovers = [sorted(set(jlines[ti]) - covered[ti]) for ti in range(V)]
    pranks = [span_rank(sorted(p)) for p in pool]
    # ============ THE ROOM-AWARE RE-SLOT ============
    # the state: per dim d: the components (the union-find over ('t', t) and ('p', p)!!) +
    # per component: the targets' common perp mask + the pieces' union lines.
    # the greedy: the pieces by the user-count desc; the placement: the dim d >= span:
    # the check: the piece's users' components at d MERGE (via the piece!!) -> the merged
    # component's (union + the piece) ⊆ the merged targets' common perp?!  + the target's
    # cumulative rank check (rank(cum_d + piece) <= d!!)!!
    comp = {d: {} for d in range(2, 9)}          # dim -> node -> (root, perp-mask, union-lines)
    dsu = {d: {} for d in range(2, 9)}
    cperp = {d: {} for d in range(2, 9)}         # dim -> root -> the targets' common perp
    clines = {d: {} for d in range(2, 9)}        # dim -> root -> the pieces' union lines
    cum = {t: {d: [] for d in range(2, 9)} for t in range(V)}   # the targets' cumulative unions
    tgt_slot = {}
    def find(d, x):
        while dsu[d][x] != x:
            dsu[d][x] = dsu[d][dsu[d][x]]; x = dsu[d][x]
        return x
    def comp_of(d, t):
        r = find(d, ('t', t))
        return cperp[d][r], clines[d][r]
    # init: every target is its own component at every dim:
    for d in range(2, 9):
        for t in range(V):
            dsu[d][('t', t)] = ('t', t)
            cperp[d][('t', t)] = PERP[t]
            clines[d][('t', t)] = set()
    unsafe = 0; fallback_reads = 0
    order = sorted(range(len(pool)), key=lambda p: -len(pool_users[p]))
    for p in order:
        r = pranks[p]; lines = set(pool[p])
        placed = False
        for d in range(max(2, r), 9):
            # the merged component check: the piece joins its users' components at d:
            roots_u = {}
            ok = True
            for t in pool_users[p]:
                ru = find(d, ('t', t))
                roots_u[ru] = True
            # the merged common perp + the merged lines:
            mp_ = None; ml = set()
            for ru in roots_u:
                pp = cperp[d][ru]
                mp_ = pp if mp_ is None else (mp_ & pp)
                ml |= clines[d][ru]
            ml = ml | lines
            if not all((mp_ >> s) & 1 for s in ml):
                continue    # the perp fails at this dim!!
            # the cumulative rank check for each user:
            fits = True
            for t in pool_users[p]:
                if span_rank(cum[t][d] + sorted(lines)) > d:
                    fits = False
                    break
            if not fits:
                continue
            # PLACE: merge the components + the piece:
            rl = list(roots_u)
            big = rl[0]
            for ru in rl[1:]:
                dsu[d][ru] = big
                cperp[d][big] &= cperp[d][ru]
                clines[d][big] |= clines[d][ru]
            clines[d][big] |= lines
            dsu[d][('p', p)] = big
            for t in pool_users[p]:
                for d2 in range(d, 9):
                    cum[t][d2] = cum[t][d2] + sorted(lines)
                tgt_slot[(t, p)] = d
            placed = True
            break
        if not placed:
            unsafe += 1
            fallback_reads += len(pool_users[p])   # the per-target composite fallback!!
    # the tails (the same cumulative at the dims >= the span!!):
    tail_slot = {}
    for t in range(V):
        if not leftovers[t]:
            continue
        sp = span_rank(leftovers[t])
        for d in range(max(2, sp), 9):
            if span_rank(cum[t][d] + leftovers[t]) <= d:
                tail_slot[t] = d
                for d2 in range(d, 9):
                    cum[t][d2] = cum[t][d2] + leftovers[t]
                break
    # the composites' fallback: the unsafe pieces -> the per-target merges (the R cost!!)
    # THE R: the pool + the unsafe (the per-target composite registers: ONE per (t, unsafe-piece-read)!!)
    # honest simplification: the fallback composites: one per (t, p) for the unsafe p's reads!!
    n_fb = fallback_reads
    R_struct = len(pool) + n_fb + sum(1 for lo in leftovers if lo) + 9
    demand = len(tgt_slot) + len(tail_slot) + n_fb
    R_hon = max(R_struct, -(-demand // 9))
    slack = R_hon - R_struct
    # ============ THE (c)-HIST ============
    hist = Counter()
    piece_reads = {}
    for (t, p), s in tgt_slot.items():
        piece_reads.setdefault(p, set()).add(s)
    for p in range(len(pool)):
        ch = [0, pranks[p]] + sorted(piece_reads.get(p, set())) + [H]
        for j in jumps(ch):
            hist[j] += 1
    src_slots = {}
    for p in range(len(pool)):
        d_build = None
        # the piece's build frame: the span; the sources' slots: the span dim!!
        for s in pool[p]:
            src_slots.setdefault(s, set()).add(pranks[p])
    tail_span_of = {}
    for t in range(V):
        if leftovers[t]:
            sp_t = span_rank(leftovers[t])
            for s in leftovers[t]:
                tail_span_of.setdefault(s, set()).add(sp_t)
    for s in range(V):
        ch = [1] + sorted(src_slots.get(s, set()) | tail_span_of.get(s, set())) + [H]
        for j in jumps(ch):
            hist[j] += 1
    tgt_dims = {}
    for (t, p), s in tgt_slot.items():
        tgt_dims.setdefault(t, set()).add(s)
    for t in range(V):
        if t in tail_slot:
            tgt_dims.setdefault(t, set()).add(tail_slot[t])
        for j in jumps([0] + sorted(tgt_dims.get(t, set())) + [8]):
            hist[j] += 1
    hist[8] += 8; hist[1] += 8; hist[9] += 1   # the gathers
    hist[8] += 8; hist[9] += 1                  # the copies (cst = 73!!)
    for t in range(V):
        if not leftovers[t]:
            continue
        sp = span_rank(leftovers[t])
        s = tail_slot.get(t)
        ch = {0, sp, H}
        if s is not None and s > sp:
            ch.add(s)
        for j in jumps(sorted(ch)):
            hist[j] += 1
    # the fallback composites' chains (the piece-like: {2, 1x6, 1}!!): the honest coarse/fine bracket!!
    LM = sum(r * z * np.log(73.0 / r) for r, z in hist.items() if r < 73)
    ident = 9 * R_hon + 73 + 2 * V * 8
    outs = []
    for tag, js in (('coarse', [8, 1]), ('fine', [2, 1, 1, 1, 1, 1, 1, 1])):
        h2 = Counter(hist)
        for _ in range(slack + n_fb):        # the slack + the fallback composites!!
            for j in js:
                h2[j] += 1
        mass = sum(r * z for r, z in h2.items())
        assert mass == ident, (TH, tag, mass, ident)
        c, prof, dd = pprice(dict(h2), V, H, R_hon)
        outs.append('%s %s' % (tag, 'NO-ROOT' if c is None else '%+.2f%%' % ((float(c) / FRONTIER - 1) * 100)))
    log('TH=%d | unsafe %d (the fallback reads %d!!) | R_str %d dem %d R_hon %d (slack %d) | LM %.0f | %s'
        % (TH, unsafe, n_fb, R_struct, demand, R_hon, slack, LM, ' | '.join(outs)))
log('DONE')
