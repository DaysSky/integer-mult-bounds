"""THE GIANT REPAIR SCAN (the user's SS1601 push!!; the SS1628 catastrophe's honest follow-up!!).

THE HONEST GAP: the naive cumulative slots (SS1604!!) have only 9 failing rooms (the
giant transitive components, SS1615!!); my room-safe greedy (SS1628!!) overshoots
(82-87% rejects!!).  THE TRUE OPTIMUM IS BETWEEN.  THE BOUNDED NEXT STEP: THE REPAIR
SCAN — for each failing room's pieces: the SAFE ALTERNATIVE DIMS (the span + the
cumulative rank + the perp-safety at the new dim's components!!):
- (a) the piece's span: d' >= the span;
- (b) the users' cumulative ranks at d': rank(cum_{d'} + piece) <= d';
- (c) the placement at d' merges the users' components at d' -> the merged lines +
      the piece ⊆ the merged targets' common perp (the transitive safety!!).
THE UNREPAIRABLE (no safe d') -> THE COMPOSITES (the per-target fallback: the R cost!!).

THE OUTPUT: per TH: the failing rooms' pieces: the repairable (the safe alternatives'
counts!!) vs the unrepairable; the composites' R cost; the repaired R_struct + the
(c)-hist + THE PRICE BRACKET: DOES ANY REPAIRED CONFIGURATION KEEP THE CROSSINGS?!
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

def find(dsu, x):
    while dsu[x] != x:
        dsu[x] = dsu[dsu[x]]; x = dsu[x]
    return x

log('TH | the failing rooms | the pieces: repairable/unrepairable | the composites R | R_str dem R_hon | the price bracket')
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
    # ============ THE NAIVE CUMULATIVE SLOTS (SS1604!!) ============
    cum = {t: {d: [] for d in range(2, 9)} for t in range(V)}
    tgt_slot = {}
    for ti in range(V):
        items = [(pid, pranks[pid]) for pid in assigned[ti]]
        if leftovers[ti]:
            items.append((-1, span_rank(leftovers[ti])))
        items.sort(key=lambda x: -x[1])
        for pid, r in items:
            lines = sorted(pool[pid]) if pid >= 0 else leftovers[ti]
            for d in range(max(2, r), 9):
                if span_rank(cum[ti][d] + lines) <= d:
                    for d2 in range(d, 9):
                        cum[ti][d2] = cum[ti][d2] + lines
                    tgt_slot[(ti, pid)] = d
                    break
    # ============ THE PER-DIM COMPONENTS (SS1615!!) + THE FAILING ROOMS ============
    fails_at = {d: set() for d in range(2, 9)}   # dim -> the failing rooms' pieces
    for d in range(2, 9):
        reads = [(t, p) for (t, p), dd in tgt_slot.items() if dd == d]
        nodes = {}
        for t, p in reads:
            nodes[('t', t)] = True
            nodes[('p', p) if p >= 0 else ('tail', t)] = True
        dsu = {n: n for n in nodes}
        def uni(a, b):
            ra, rb = find(dsu, a), find(dsu, b)
            if ra != rb:
                dsu[ra] = rb
        for t, p in reads:
            uni(('t', t), ('p', p) if p >= 0 else ('tail', t))
        rooms = {}
        for n in nodes:
            rooms.setdefault(find(dsu, n), []).append(n)
        for r, members in rooms.items():
            ts = [m[1] for m in members if m[0] == 't']
            ps = [m[1] for m in members if m[0] == 'p']
            tls = [m[1] for m in members if m[0] == 'tail']
            cp = PERP[ts[0]]
            for t in ts[1:]:
                cp &= PERP[t]
            ul = set()
            for p in ps:
                ul |= set(pool[p])
            for t in tls:
                ul |= set(leftovers[t])
            if not all((cp >> s) & 1 for s in ul):
                fails_at[d] |= set(ps)    # the failing room's PIECES (the tails: not movable!!)
    # ============ THE REPAIR SCAN ============
    # for each failing piece: the alternative dims d' != d (the span + the cumulative +
    # the merged perp-safety at d'!!).  THE COMPONENTS AT d' (from the naive slots!!).
    comps = {}
    for d in range(2, 9):
        reads = [(t, p) for (t, p), dd in tgt_slot.items() if dd == d]
        nodes = {}
        for t, p in reads:
            nodes[('t', t)] = True
            nodes[('p', p) if p >= 0 else ('tail', t)] = True   # THE SS1609 FIX: the per-target tail nodes!!
        dsu2 = {n: n for n in nodes}
        for t, p in reads:
            ra, rb = find(dsu2, ('t', t)), find(dsu2, ('p', p) if p >= 0 else ('tail', t))
            if ra != rb:
                dsu2[ra] = rb
        comps[d] = dsu2
    cperp = {}; clines = {}
    for d in range(2, 9):
        cperp[d] = {}; clines[d] = {}
        for n in comps[d]:
            r = find(comps[d], n)
            if r not in cperp[d]:
                cperp[d][r] = None; clines[d][r] = set()
        for n in comps[d]:
            r = find(comps[d], n)
            if n[0] == 't':
                cperp[d][r] = PERP[n[1]] if cperp[d][r] is None else (cperp[d][r] & PERP[n[1]])
            elif n[0] == 'p':
                clines[d][r] |= set(pool[n[1]])
            else:
                clines[d][r] |= set(leftovers[n[1]])   # THE TAILS' CONTENTS (the SS1609 fix!!)
    repairable = 0; unrepairable = 0; fb_reads = 0
    alt_hist = Counter()
    for d in range(2, 9):
        for p in sorted(fails_at[d]):
            lines = set(pool[p]); r = pranks[p]
            found = None
            for d2 in range(2, 9):
                if d2 == d or d2 < r:
                    continue
                # (b) the cumulative check at d2:
                ok_c = all(span_rank(cum[t][d2] + sorted(lines)) <= d2 for t in pool_users[p])
                if not ok_c:
                    continue
                # (c) the merged perp-safety at d2: the users' components at d2 + the piece:
                roots_u = set(find(comps[d2], ('t', t)) for t in pool_users[p] if ('t', t) in comps[d2])
                mp_ = None; ml = set()
                for ru in roots_u:
                    pp = cperp[d2].get(ru)
                    if pp is None:
                        continue
                    mp_ = pp if mp_ is None else (mp_ & pp)
                    ml |= clines[d2].get(ru, set())
                if mp_ is None:
                    mp_ = (1 << V) - 1
                ml = ml | lines
                if not all((mp_ >> s) & 1 for s in ml):
                    continue
                found = d2
                break
            if found is not None:
                repairable += 1
                alt_hist[found] += 1
            else:
                unrepairable += 1
                fb_reads += len(pool_users[p])
    # ============ THE REPAIRED R + THE PRICE BRACKET ============
    n_fb = fb_reads
    R_struct = len(pool) + n_fb + sum(1 for lo in leftovers if lo) + 9
    demand = len(tgt_slot) + sum(1 for lo in leftovers if lo) + n_fb
    R_hon = max(R_struct, -(-demand // 9))
    slack = R_hon - R_struct
    # the (c)-hist [the SS1594 model + the unrepairable fallbacks' chains in the bracket!!]
    hist = Counter()
    piece_reads = {}
    for (t, p), s in tgt_slot.items():
        if p >= 0:
            piece_reads.setdefault(p, set()).add(s)
    def jumps(ch):
        ch = sorted(set(ch))
        return [b - a for a, b in zip(ch, ch[1:])]
    for p in range(len(pool)):
        for j in jumps([0, pranks[p]] + sorted(piece_reads.get(p, set())) + [H]):
            hist[j] += 1
    src_slots = {}; tail_span_of = {}
    for p in range(len(pool)):
        for s in pool[p]:
            src_slots.setdefault(s, set()).add(pranks[p])
    for t in range(V):
        if leftovers[t]:
            sp_t = span_rank(leftovers[t])
            for s in leftovers[t]:
                tail_span_of.setdefault(s, set()).add(sp_t)
    for s in range(V):
        for j in jumps([1] + sorted(src_slots.get(s, set()) | tail_span_of.get(s, set())) + [H]):
            hist[j] += 1
    tgt_dims = {}
    for (t, p), s in tgt_slot.items():
        tgt_dims.setdefault(t, set()).add(s)
    for t in range(V):
        if leftovers[t]:
            sp = span_rank(leftovers[t])
            s = tgt_slot.get((t, -1))
            ch = {0, sp, H}
            if s is not None and s > sp:
                ch.add(s)
                tgt_dims.setdefault(t, set()).add(s)
        for j in jumps([0] + sorted(tgt_dims.get(t, set())) + [8]):
            hist[j] += 1
    hist[8] += 8; hist[1] += 8; hist[9] += 1
    hist[8] += 8; hist[9] += 1
    for t in range(V):
        if leftovers[t]:
            sp = span_rank(leftovers[t])
            s = tgt_slot.get((t, -1))
            ch = {0, sp, H}
            if s is not None and s > sp:
                ch.add(s)
            for j in jumps(sorted(ch)):
                hist[j] += 1
    ident = 9 * R_hon + 73 + 2 * V * 8
    outs = []
    for tag, js in (('coarse', [8, 1]), ('fine', [2, 1, 1, 1, 1, 1, 1, 1])):
        h2 = Counter(hist)
        for _ in range(slack + n_fb):
            for j in js:
                h2[j] += 1
        mass = sum(r * z for r, z in h2.items())
        if mass != ident:
            outs.append('%s MASS-OFF(%d vs %d)' % (tag, mass, ident))
            continue
        c, prof, dd = pprice(dict(h2), V, H, R_hon)
        outs.append('%s %s' % (tag, 'NO-ROOT' if c is None else '%+.2f%%' % ((float(c) / FRONTIER - 1) * 100)))
    log('TH=%d | the failing rooms: %s | repairable %d (the alts %s), unrepairable %d (the fb reads %d!!) | R_str %d dem %d R_hon %d | %s'
        % (TH, {d: len(fails_at[d]) for d in range(2, 9) if fails_at[d]}, repairable,
           dict(sorted(alt_hist.items())), unrepairable, n_fb, R_struct, demand, R_hon, ' | '.join(outs)))
log('DONE')
