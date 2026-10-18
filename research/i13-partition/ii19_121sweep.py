"""THE THRESHOLD SWEEP — THE UNEXPLORED REDESIGN DIMENSION (the user's SS1566: 'whatever it takes. keep pushing the frontier'!!).

THE SS1568 READ SETTLED THE ARRIVAL LAW: the slots.py L237-242: the demand = THE
TARGET-SIDE B-READS ONLY (the pieces assigned + the tail reads!!) <= 9 x R_struct —
THE AGGREGATE FORM (the E8 precedent: the R420's ~3,000 B-reads vs 8x420 = 3,360: the
89.3% utilization — THE SAME LAW!!!); the A-src-reads + the gathers' 521 reads DO NOT
COUNT (the audit's scope question ANSWERED!!).  R_honest = max(R_struct, ceil(demand/9)).

THE LEVER NEVER EXPLORED: THE PIECE ECONOMY'S THRESHOLD — the greedy stops at saving >=
4 (MY ARBITRARY SS1423-ERA CHOICE!!!).  THE SWEEP: TH in {6, 5, 4, 3, 2}: the COARSER
economy (TH=6/5): FEWER, BIGGER pieces -> FEWER reads -> R DROPS -> THE PRICE RISES (the
lower R = the lower mass = the better c: the SS1536 R-grid trend!!) AND THE HIST
COARSENS (the bigger spans + the heavier tails -> THE LM DROPS -> THE PRICE RISES
FURTHER!!); the FINER (TH=3/2): the opposite.  FOR EACH TH: the packings (the honest
feasibility: the unplaced + the conflicts!!) + THE (b)-MODEL HIST (the SS1551 code!!) +
THE PRICE at the honest R (the consistent pairing: the hist at the R_struct + THE SLACK
REGISTERS' BRACKET (the coarse {8,1} / the fine piece-like: the R_honest - R_struct!!)).

THE HONEST CAVEATS: (1) the coarse hist vs the REAL-WORD precedent (the R420 climbs
FINE: {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}: the rank-8 ONLY the copies!!); (2) the
nesting failure (121/121: SS1515!!) REMAINS the build blocker; (3) the payoff is
BIT-side only (the selected κ is COMPLEX-bound!!).
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

# the system [the slots.py code!!]
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

log('TH | pool carriers R_struct demand R_hon slack | unplaced conflicts | LM | coarse-slack | fine-slack')
for TH in (4, 5, 6, 7, 8, 10, 12, 16, 24):
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
    carriers = sum(1 for lo in leftovers if lo)
    pranks = [span_rank(sorted(p)) for p in pool]
    # the target-side packing [the slots.py!!]
    tgt_slot = {}; unplaced = 0
    for ti in range(V):
        items = [(pid, pranks[pid]) for pid in assigned[ti]]
        if leftovers[ti]:
            items.append((-1, span_rank(leftovers[ti])))
        items.sort(key=lambda x: -x[1])
        slot_unions = {d: [] for d in range(2, 9)}
        for pid, r in items:
            lines = sorted(pool[pid]) if pid >= 0 else leftovers[ti]
            okd = None
            for d in range(max(2, r), 9):
                if span_rank(slot_unions[d] + lines) <= d:
                    okd = d
                    break
            if okd is None:
                unplaced += 1
            else:
                slot_unions[okd] = slot_unions[okd] + lines
                tgt_slot[(ti, pid)] = okd
    # the source-side [the slots.py!!]
    src_pieces = {s: [] for s in range(V)}
    for pid, p in enumerate(pool):
        for s in p:
            src_pieces[s].append(pid)
    src_assign = {}; conflicts = 0
    for s in range(V):
        used = set()
        for pid in sorted(src_pieces[s], key=lambda q: -pranks[q]):
            d = None
            for cand in range(max(2, pranks[pid]), 9):
                if cand not in used:
                    d = cand
                    break
            if d is None:
                conflicts += 1
            else:
                used.add(d); src_assign[(s, pid)] = d
    # THE (b)-MODEL HIST [the SS1551 code!!]
    hist = Counter()
    piece_reads = {}
    for (t, p), s in tgt_slot.items():
        if p >= 0:
            piece_reads.setdefault(p, set()).add(s)
    for p in range(len(pool)):
        for j in jumps([0, pranks[p]] + sorted(piece_reads.get(p, set())) + [H]):
            hist[j] += 1
    src_slots = {}
    for (s, p), slot in src_assign.items():
        src_slots.setdefault(s, set()).add(slot)
    # THE (c)-CORRECTION (the gcheck re-read SS1589!!): the gate rule — ALL the operands
    # (the dest AND the srcs!!) climb to the gate's frame, and EVERY climb is priced
    # (the hist!!)!!  THE TAIL-BUILDS' SOURCE-CLIMBS: the carriers' leftover lines must
    # climb to the tail's span (dim 5-8!!) BEFORE FULL (a source at FULL (dim 9!!)
    # cannot feed a dim-8 build: the ⊆ rule!!) — THE SOURCES' CHAINS MUST INCLUDE THE
    # TAIL-SPAN FRAMES (the SS1551 (b)-model MISSED them!!).  The sources' total mass
    # is FIXED (8 each — the identity!!): the DISTRIBUTION coarsens (the LM rises!!)
    # -> the honest price is LOWER than every SS1572/SS1575 number!!
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
        for j in jumps([0] + sorted(tgt_dims.get(t, set())) + [8]):
            hist[j] += 1
    hist[8] += 8; hist[1] += 8; hist[9] += 1   # the gathers (the even 0->8->9 x8; the odd 0->9!!)
    hist[8] += 8; hist[9] += 1                  # the copies (the MEASURED cst=73!!)
    for t in range(V):
        if not leftovers[t]:
            continue
        sp = span_rank(leftovers[t])
        s = tgt_slot.get((t, -1))
        ch = {0, sp, H}
        if s is not None and s > sp:
            ch.add(s)
        for j in jumps(sorted(ch)):
            hist[j] += 1
    R_struct = len(pool) + carriers + 9
    demand = sum(len(assigned[ti]) + (1 if leftovers[ti] else 0) for ti in range(V))
    R_hon = max(R_struct, -(-demand // 9))
    slack = R_hon - R_struct
    LM = sum(r * z * np.log(73.0 / r) for r, z in hist.items() if r < 73)
    ident = 9 * R_hon + 73 + 2 * V * 8
    outs = []
    for tag, js in (('coarse', [8, 1]), ('fine', [2, 1, 1, 1, 1, 1, 1, 1])):
        h2 = Counter(hist)
        for _ in range(slack):
            for j in js:
                h2[j] += 1
        mass = sum(r * z for r, z in h2.items())
        assert mass == ident, (TH, tag, mass, ident)
        c, prof, d = pprice(dict(h2), V, H, R_hon)
        outs.append('%s %s' % (tag, 'NO-ROOT' if c is None else '%+.2f%%' % ((float(c) / FRONTIER - 1) * 100)))
    print('TH=%d | %d pool, %d carr, R_str %d, dem %d, R_hon %d (slack %d) | unpl %d, conf %d | LM %.0f | %s'
          % (TH, len(pool), carriers, R_struct, demand, R_hon, slack, unplaced, conflicts, LM, ' | '.join(outs)), flush=True)
print('DONE')
