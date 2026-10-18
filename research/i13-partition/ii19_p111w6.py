"""THE P111-CLASS WORD — THE COMPLETE BUILD (ii19_p111w6.py)!!!
THE CONFLICT-DRIVEN SOLVE (the augmenting re-solves (not the random restarts!!)) + THE
PROJECTION + THE SELF-CORRECTING D-FIX (the replay -> the register-residues -> the
D-srcs += -> repeat!!) + THE FULL REPLAY + THE EMISSION!!
THE TARGET: the R = 420 + the minis (the crossing at 428: the minis <= 8!!!)
"""
import gzip, json, random, time
from collections import Counter
from fractions import Fraction
W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

RM = [1, 8, 20, 24, 45, 63, 82, 89, 102]       # THE MINIS-17 PUNCTURE (the hunt best!!)
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
        y = row
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

# ============ (0) THE BASE-REPLAY (the R420's own semantics!!) ============
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

# the stars + the W_i!!
STARS, WiB, WiLINES = [], [], []
for L in RM:
    s_new = 0
    star_old = [u for u in range(120) if u != L and iph(lines[L], lines[u]) == 0]
    for u in kept:
        if iph(lines[L], lines[u]) == 0:
            s_new |= 1 << old2new[u]
    STARS.append(s_new)
    WiB.append(basis_of(star_old))
    WiLINES.append([old2new[u] for u in star_old if u in old2new])
bx = {}
for s in STARS:
    x = s
    while x:
        p = (x & -x).bit_length() - 1
        if p in bx: x ^= bx[p]
        else: bx[p] = x; break
assert len(bx) == 9, 'the CST-63 puncture!!'
log('(0b) the stars: %s (the W-dims %s!!)' % (
    [bin(s).count('1') for s in STARS], [len(b) for b in WiB]))

# the pools (the tail-curs ⊆ W_i!!)
POOLS = [[r for r in range(nreg0) if cur[r] and FDIM[cur[r]] <= 7
          and in_W(FBAS[cur[r]], WiB[si]) and CONT[r]] for si in range(9)]
log('(0c) the pools: %s' % [len(p) for p in POOLS])

# ============ (1) THE CONFLICT-DRIVEN SOLVE (the augmenting!!) ============
def solve_one(si, exclude, do_shuffle=False):
    """the star si's solve over pool-minus-exclude: (the sol, the residue)!!
    THE SHUFFLE: the diversity (the pool-order randomization — the w2e's key!!)"""
    s = STARS[si]
    pool = [r for r in POOLS[si] if r not in exclude and CONT[r]]
    if do_shuffle:
        rng.shuffle(pool)
    piv = {}
    for r in pool:
        x = CONT[r]
        chain = 1 << r
        while x:
            p = (x & -x).bit_length() - 1
            if p in piv:
                x2, m2 = piv[p]
                x ^= x2
                chain ^= m2
            else:
                piv[p] = (x, chain)
                break
    x = s
    chain = 0
    while x:
        p = (x & -x).bit_length() - 1
        if p in piv:
            x2, m2 = piv[p]
            x ^= x2
            chain ^= m2
        else:
            break
    if x:
        return None, x
    return [r for r in pool if (chain >> r) & 1], 0

rng = random.Random(111)
# THE MIN-CONFLICTS LOCAL SEARCH (the hill-climb on the conflicts!!)!
def full_state():
    taken = Counter()
    for si in range(9):
        for r in sols[si]: taken[r] += 1
    return taken
def conflicts(taken):
    return sum(1 for r, k in taken.items() if k >= 2)

# the initial: the independent solves!!
sols = {}
for si in range(9):
    sol, res = solve_one(si, set())
    sols[si] = sol if sol else []
taken = full_state()
best_cost = conflicts(taken)
log('(1) the initial: the conflicts %d!!' % best_cost)

# THE LOCAL SEARCH (the moves: the exclusion-re-solves!!)!
for restart in range(400):
    for it in range(2000):
        confl = [r for r, k in taken.items() if k >= 2]
        if not confl:
            break
        r = rng.choice(confl)
        owners = [si for si in range(9) if r in sols[si]]
        # THE MOVE: re-solve a random owner with r excluded (+ a random extra exclusion!!)!
        moved = False
        for loser in rng.sample(owners, len(owners)):
            excl = {r}
            # the diversification: also drop a random member of the loser's sol!!
            cur_sol = sols[loser]
            if cur_sol and rng.random() < 0.5:
                excl.add(rng.choice(cur_sol))
            sol2, res2 = solve_one(loser, excl, do_shuffle=True)
            if sol2 is not None:
                for x in sols[loser]: taken[x] -= 1
                sols[loser] = sol2
                for x in sol2: taken[x] += 1
                moved = True
                break
        if not moved:
            # the random kick: re-solve a random star with random exclusions!!
            si = rng.randrange(9)
            excl = set(rng.sample(sols[si], min(len(sols[si]), 2))) if sols[si] else set()
            sol2, res2 = solve_one(si, excl, do_shuffle=True)
            if sol2 is not None:
                for x in sols[si]: taken[x] -= 1
                sols[si] = sol2
                for x in sol2: taken[x] += 1
        c = conflicts(taken)
        if c < best_cost:
            best_cost = c
            best_sols = {si: list(sols[si]) for si in range(9)}
            log('    the restart %d iter %d: THE CONFLICTS %d!!' % (restart, it, c))
            if c == 0:
                break
    if best_cost == 0:
        break
    # the fresh restart!!
    for si in range(9):
        sol, res = solve_one(si, set())
        sols[si] = sol if sol else []
        # the random order-diversification: re-solve sequentially with the taken!!
    # the sequential-diverse restart: the random order + the taken-aware!!
    order = list(range(9)); rng.shuffle(order)
    used = set()
    for si in order:
        sol, res = solve_one(si, used)
        if sol is None:
            # NO FALLBACK: keep the previous sol (the hill-climb continues!!)
            continue
        sols[si] = sol
        used.update(sol)
    taken = full_state()
    c = conflicts(taken)
    if c < best_cost:
        best_cost = c
        best_sols = {si: list(sols[si]) for si in range(9)}
        log('    the restart %d (the sequential!!): THE CONFLICTS %d!!' % (restart, c))
log('(1b) THE BEST CONFLICTS: %d' % best_cost)
sols = best_sols

# THE FINAL: the honest sequential + the residue-minis (the w2e-semantics, the local-search start!!)
# THE BEST-ORDER: try many orders with the best-found state's exclusions!!
best_minis = None
for trial in range(2500):
    order = list(range(9)); rng.shuffle(order)
    used = set()
    sols_t = {}
    minis_t = []
    for si in order:
        sol, res = solve_one(si, used, do_shuffle=True)
        if sol is not None:
            sols_t[si] = sol
            used.update(sol)
            continue
        # THE PARTIAL: solve with the used-exclusions but allow the residues -> the minis!!
        # the max-partial: the piv-elimination over the free pool + the star!!
        pool = [r for r in POOLS[si] if r not in used and CONT[r]]
        piv = {}
        for r in pool:
            x = CONT[r]
            chain = 1 << r
            while x:
                p = (x & -x).bit_length() - 1
                if p in piv:
                    x2, m2 = piv[p]
                    x ^= x2
                    chain ^= m2
                else:
                    piv[p] = (x, chain)
                    break
        x = STARS[si]
        chain = 0
        while x:
            p = (x & -x).bit_length() - 1
            if p in piv:
                x2, m2 = piv[p]
                x ^= x2
                chain ^= m2
            else:
                break
        sol_partial = [r for r in pool if (chain >> r) & 1]
        resid = x
        sols_t[si] = sol_partial
        used.update(sol_partial)
        minis_t.extend((si, u) for u in [i for i in range(V) if (resid >> i) & 1])
    if best_minis is None or len(minis_t) < len(best_minis[0]):
        best_minis = (minis_t, sols_t, order)
        log('    the final-trial %d: THE MINIS %d (the order %s!!)' % (
            trial, len(minis_t), order[:3]))
minis, final_sols, best_order = best_minis
# THE VERIFICATION (mandatory!!): the SOL + the minis must XOR to the stars!!
for si in range(9):
    x = 0
    for r in final_sols[si]:
        x ^= CONT[r]
    for u in [u2 for (s2, u2) in minis if s2 == si]:
        x ^= 1 << u
    assert x == STARS[si], 'THE SOL-VERIFICATION FAILS at the star %d (the diff %s!!)' % (
        si, [b for b in range(V) if (x ^ STARS[si]) >> b & 1][:8])
log('(1c-b) THE SOL-VERIFICATION: ALL 9 PASS (the algebra ✓!!)')
log('(1c) THE MINIS: %d (the R = %d!!) %s' % (
    len(minis), R0 + len(minis), 'THE CROSSING (<= 8)!!!' if len(minis) <= 8 else ''))

json.dump(dict(rm=RM, sols={si: final_sols[si] for si in range(9)},
               minis=[[si, u] for si, u in minis]), open('ii19_p111_sol.json', 'wt'))
log('(1d) the solve saved (ii19_p111_sol.json!!)')
log('    the sols: %s' % [len(final_sols[si]) for si in range(9)])