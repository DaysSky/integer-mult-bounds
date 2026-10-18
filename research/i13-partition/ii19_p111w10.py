"""THE P111-WORD v10 (ii19_p111w10.py) — THE LEGAL-RE-SOLVE (THE B-PIN-FILTERED POOLS!!!)

THE v9-DIAGNOSIS (the measured!!!): the w8's 92-illegal-climbs ALL-in-the-B (the 70-sources +
the 22-helpers: the star-builds took them to the dim-7 W_i (the A-tail!!) -> the R420's-B
re-reads them at the dim-2-cells (THE DOWN-CLIMBS!!!)).  THE ROOT-CAUSE: the w6's-POOLS
filtered on cur[r] ⊆ W_i (the climb-up ✓!!) but NOT on the B-pins!!!

THE FIX (THE LEGAL-POOLS!!!):
  (1) THE B-PIN-FILTER: r ∈ POOL[si] iff r ∉ THE-PROJECTED-B-SRCS (the pin-set!!)
      — a star-src-register's chain: ... -> W_si (7!!) -> [the later-reads: ONLY-THE-FULL (8!!)!!]
  (2) THE FREE-SOURCES (the un-pinned!!): the mini-F = ANY-frame ⊇ cur0[u] ∧ ⊆ W_si
      (the star-internal D4/D6 (the cell ⊆ the D4 (the R420's-own-ladder!!!))!!)
  (3) THE PINNED-SOURCES (the B-srcs!!): the mini-F == cur0[u] FORCED (the FREE-read!!)
      -> the mini's climb: cur0[u] -> W_si: THE LUCKY-CELLS (cur0[u] ⊆ W_si!!!)
  (4) THE RE-SOLVE (the w6's-machinery + THE WEIGHTED-RESIDUES (the legal-minis-first!!))

THIS-SCRIPT (the measure + the re-solve!!): (0) the base-replay + THE PIN-MAP;
(1) THE LEGAL-POOLS (the sizes + the span-sufficiency!!); (2) THE RE-SOLVE (the conflict-free!!
(the exclusive!!) + the residues); (3) THE RESIDUES'-LEGALITY-MEASURE (the free vs the
pinned-lucky!!); (4) THE SAVE (the sol2-JSON (the w11's-rebuild!!!)).
"""
import gzip, json, random, time
from collections import Counter
from fractions import Fraction

W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

RM = [1, 8, 20, 24, 45, 63, 82, 89, 102]          # the sol.json's-puncture (the w6's!!)
kept = [i for i in range(120) if i not in RM]
old2new = {o: n for n, o in enumerate(kept)}
V, H = 111, 8
lines = W['lines']
v0 = W['v']
frames0 = W['frames']
nreg0 = len(W['start'])
R0 = W['R']

def iph(a, b): return sum(x * y for x, y in zip(a, b)) / 2
def basis_of(idx_list):
    rr = [[Fraction(z) for z in lines[i]] for i in idx_list]
    bas = []
    for row in rr:
        y = list(row)
        for b in bas:
            p = next((c for c in range(8) if b[c] != 0), None)
            if p is not None and y[p] != 0:
                f = y[p] / b[p]
                y = [a2 - f * c for a2, c in zip(y, b)]
        p = next((c for c in range(8) if y[c] != 0), None)
        if p is not None: bas.append(y)
    return bas
FBAS = [basis_of(f) if f else [] for f in frames0]
FDIM = [len(b) for b in FBAS]
def in_W(fbas, wbas):
    for y in fbas:
        z = list(y)
        for b in wbas:
            p = next((c for c in range(8) if b[c] != 0), None)
            if p is not None and z[p] != 0:
                f = z[p] / b[p]
                z = [a2 - f * c for a2, c in zip(z, b)]
        if any(z[c] != 0 for c in range(8)):
            return False
    return True

# ============ (0) THE BASE-REPLAY + THE PIN-MAP ============
val = [1 << r for r in range(nreg0)]
cur = list(W['start'])
for F, d, srcs in W['D']:
    for s in srcs: val[d] ^= val[s]
for gi, (F, d, srcs) in enumerate(W['A']):
    x = 0
    for s in srcs: x ^= val[s]
    val[d] ^= x
    for s in srcs:
        if FDIM[cur[s]] < FDIM[F] or not in_W(FBAS[cur[s]], FBAS[F]):
            cur[s] = F
    cur[d] = F
log('(0) the base-replay done!!')
CONT_OLD = {}
for r in range(nreg0):
    c = 0
    for b in range(v0):
        if (val[r] >> b) & 1:
            c |= 1 << b
    CONT_OLD[r] = c
CONT = {}
for r in range(nreg0):
    proj = 0
    for b in range(v0):
        if (CONT_OLD[r] >> b) & 1 and b in old2new:
            proj |= 1 << old2new[b]
    CONT[r] = proj

# THE PIN-MAP (the projected-B's srcs (the kept-registers-read-in-the-B!!)!!)
def map_reg(r):
    if r < v0:
        return old2new.get(r)
    if r < 2 * v0:
        return old2new.get(r - v0)          # the target-src (never!! (the B: no-target-srcs!!))
    return r - 18
B_PIN = set()                                 # the OLD-indices (the kept!!)
B_GATE_N = 0
for F, d, srcs in W['B']:
    nd_ok = (d < v0 and d in old2new) or (v0 <= d < 2 * v0 and (d - v0) in old2new)
    if not nd_ok:
        continue                              # the dropped-dests (the pruned-gates!!)
    for s in srcs:
        if s < 2 * v0:
            if s in old2new: B_PIN.add(s)     # the kept-source-read (the PIN!!)
        else:
            B_PIN.add(s)                      # the helper-read (the map: h-18 ✓!!)
    B_GATE_N += 1
log('    THE PIN-MAP: %d registers (the sources %d | the helpers %d!!) | the B-gates %d' % (
    len(B_PIN), sum(1 for r in B_PIN if r < v0), sum(1 for r in B_PIN if r >= 2 * v0), B_GATE_N))
log('    the sources-A-frames: %s (the cur0-dims!!)' % dict(sorted(
    Counter(FDIM[cur[s]] for s in range(v0)).items())))
log('    the helpers-A-frames: %s' % dict(sorted(
    Counter(FDIM[cur[h]] for h in range(2 * v0, nreg0) if cur[h]).items())))

# the stars + the W_i!!
STARS, WiB = [], []
for L in RM:
    s_new = 0
    for u in kept:
        if iph(lines[L], lines[u]) == 0:
            s_new |= 1 << old2new[u]
    STARS.append(s_new)
    WiB.append(basis_of([u for u in range(120) if u != L and iph(lines[L], lines[u]) == 0]))
log('    the stars: %s' % [bin(s).count('1') for s in STARS])

# ============ (1) THE LEGAL-POOLS (the B-pin-filtered!!!) ============
POOLS_OLD = [[r for r in range(nreg0) if cur[r] and FDIM[cur[r]] <= 7
              and in_W(FBAS[cur[r]], WiB[si]) and CONT[r]] for si in range(9)]
POOLS = [[r for r in POOLS_OLD[si] if r not in B_PIN] for si in range(9)]
log('(1) THE LEGAL-POOLS: %s (the unfiltered: %s!!) (the pin-filter removed %s!!)' % (
    [len(p) for p in POOLS], [len(p) for p in POOLS_OLD],
    [len(POOLS_OLD[si]) - len(POOLS[si]) for si in range(9)]))
# the pools'-span-sufficiency (the star ∈ the span?!)
for si in range(9):
    piv = {}
    for r in POOLS[si]:
        x = CONT[r]
        while x:
            p = (x & -x).bit_length() - 1
            if p in piv: x ^= piv[p]
            else: piv[p] = x; break
    z = STARS[si]
    while z:
        p = (z & -z).bit_length() - 1
        if p in piv: z ^= piv[p]
        else: break
    log('    the star %d: the pool %d -> the rank %d | the star-in-the-span: %s' % (
        si, len(POOLS[si]), len(piv), z == 0))

# ============ (2) THE RE-SOLVE (the conflict-free (the exclusive!!)) ============
def solve_one(si, exclude, pool):
    s = STARS[si]
    pp = [r for r in pool if r not in exclude and CONT[r]]
    piv = {}
    for r in pp:
        x = CONT[r]
        chain = 1 << r
        while x:
            p = (x & -x).bit_length() - 1
            if p in piv:
                x2, m2 = piv[p]
                x ^= x2; chain ^= m2
            else:
                piv[p] = (x, chain); break
    x = s; chain = 0
    while x:
        p = (x & -x).bit_length() - 1
        if p in piv:
            x2, m2 = piv[p]
            x ^= x2; chain ^= m2
        else:
            break
    return [r for r in pp if (chain >> r) & 1], x

rng = random.Random(11111)
best = None
for trial in range(3000):
    order = list(range(9)); rng.shuffle(order)
    used = set()
    sols_t = {}; minis_t = []
    for si in order:
        sol, res = solve_one(si, used, POOLS[si])
        if sol is not None and res == 0:
            sols_t[si] = sol
            used.update(sol)
            continue
        # THE PARTIAL (the residue -> the minis!!)
        pool = [r for r in POOLS[si] if r not in used and CONT[r]]
        piv = {}
        for r in pool:
            x = CONT[r]; chain = 1 << r
            while x:
                p = (x & -x).bit_length() - 1
                if p in piv:
                    x2, m2 = piv[p]; x ^= x2; chain ^= m2
                else:
                    piv[p] = (x, chain); break
        x = STARS[si]; chain = 0
        while x:
            p = (x & -x).bit_length() - 1
            if p in piv:
                x2, m2 = piv[p]; x ^= x2; chain ^= m2
            else:
                break
        sol_partial = [r for r in pool if (chain >> r) & 1]
        resid = x
        sols_t[si] = sol_partial
        used.update(sol_partial)
        minis_t.extend((si, i) for i in range(V) if (resid >> i) & 1)
    if best is None or len(minis_t) < len(best[0]):
        best = (minis_t, sols_t, order)
        log('    the trial %d: THE MINIS %d (the order %s!!)' % (trial, len(minis_t), order[:3]))
        if not minis_t:
            break
minis, final_sols, best_order = best
log('(2) THE RE-SOLVE: THE MINIS %d (the R = %d (the +9-rets +9-mimics!!))' % (
    len(minis), R0 + len(minis) + 9 + 9))
# THE VERIFICATION (the algebra!!)
for si in range(9):
    x = 0
    for r in final_sols[si]: x ^= CONT[r]
    for u in [u2 for (s2, u2) in minis if s2 == si]: x ^= 1 << u
    assert x == STARS[si], 'THE SOL-VERIFICATION at %d!!' % si
log('    the sol-verification: ALL 9 PASS ✓ (the sols-sizes %s!!)' % (
    [len(final_sols[si]) for si in range(9)]))

# ============ (3) THE RESIDUES'-LEGALITY-MEASURE (the minis'-deliverability!!) ============
# the mini (si, u): the u's-OLD-index + the pin-status + the cell-luck!!
free_ok = 0; pin_lucky = 0; pin_dead = 0
for si, u in minis:
    u_old = kept[u]
    pinned = u_old in B_PIN
    lucky = in_W(FBAS[cur[u_old]], WiB[si])   # the cell ⊆ W_si!!
    # the free: the star-internal-F ⊇ the cell (the D4-parent-route!!): the F-candidates!!
    f_cand = [fi for fi in range(len(frames0)) if FDIM[fi] >= 2 and FDIM[fi] <= 6
              and in_W(FBAS[fi], WiB[si]) and in_W(FBAS[cur[u_old]], FBAS[fi])]
    if pinned:
        if lucky: pin_lucky += 1
        elif f_cand: pin_lucky += 1           # hmm — the pinned: the F == cur0 FORCED!!!
        else: pin_dead += 1
    else:
        if f_cand or lucky: free_ok += 1
        else: pin_dead += 1
log('(3) THE MINIS %d: the free-ok %d | the pinned-lucky %d | THE DEAD %d!!' % (
    len(minis), free_ok, pin_lucky, pin_dead))
# THE DETAIL (the per-mini!!):
for si, u in sorted(minis):
    u_old = kept[u]
    pinned = u_old in B_PIN
    lucky = in_W(FBAS[cur[u_old]], WiB[si])
    f_cand_n = sum(1 for fi in range(len(frames0)) if 2 <= FDIM[fi] <= 6
                   and in_W(FBAS[fi], WiB[si]) and in_W(FBAS[cur[u_old]], FBAS[fi]))
    log('    the mini (star %d, u %d (old %d!!)): the pinned %s | the cell-dim %d | the lucky %s '
        '| the star-internal-F-cands %d' % (si, u, u_old, pinned, FDIM[cur[u_old]], lucky, f_cand_n))

# ============ (4) THE SAVE ============
json.dump(dict(rm=RM, sols={si: final_sols[si] for si in range(9)},
               minis=[[si, u] for si, u in minis]), open('ii19_p111_sol2.json', 'wt'))
log('(4) THE SAVE: ii19_p111_sol2.json (the w11\'s-rebuild!!!)')
log('DONE — THE v10-LEGAL-RE-SOLVE!!')
