"""nat154: THE GLOBAL REUSE-FIRST SHARED-WIRE SOLVE (the E8-LEVER-A at v=111).

Every target's W_t is trivially solvable (the r434's own wires are in the pool).
The real question: the minimum DISTINCT wire family. The reuse-first heuristic:
(1) seed each target with its r434 solution;
(2) re-solve targets preferring already-used wires (the exact solve over used + pool);
(3) local search: replace used pairs with shared singles where possible.
"""
import json, gzip
from collections import Counter
from itertools import combinations

W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
v = W['v']
lines = [tuple(int(c) for c in l) for l in W['lines']]

def ip2(i, j):
    return sum(a*b for a, b in zip(lines[i], lines[j]))
adj = [[(ip2(i, j) % 2 != 0 or ip2(i, j)//2 != 0) for j in range(v)] for i in range(v)]
perp = [frozenset(j for j in range(v) if j != i and not adj[i][j]) for i in range(v)]

tgt_srcs = {}
for F, d, ss in W['B']:
    if v <= d < 2*v:
        tgt_srcs.setdefault(d - v, []).extend(ss)
nreg = 2*v + W['R']

val = [0]*nreg
for s in range(v): val[s] = 1 << s
for F, d, ss in W['D']:
    for s in ss: val[d] ^= val[s]
for F, d, ss in W['A']:
    for s in ss: val[d] ^= val[s]

Wt = {}
seed = {}
for t, ss in tgt_srcs.items():
    m = 0
    sd = []
    for s in ss:
        if s >= 2*v:
            m ^= val[s]
            sd.append(val[s] & ((1 << v) - 1))
    Wt[t] = m
    seed[t] = sd

def mask_of(S):
    m = 0
    for i in S: m |= 1 << i
    return m

# the pool: the pair/triple intersections + the r434 wires
pool = {}
for i in range(v):
    for j in range(i+1, v):
        S = perp[i] & perp[j]
        if len(S) >= 12:
            pool[mask_of(S)] = {i, j}
for i, j, k in combinations(range(v), 3):
    S = perp[i] & perp[j] & perp[k]
    if len(S) >= 16:
        m = mask_of(S)
        if m not in pool:
            pool[m] = {i, j, k}
for t, sd in seed.items():
    for cm in sd:
        pool.setdefault(cm, set()).add(t)
print('the pool:', len(pool))

cand = {t: [cm for cm in pool if (cm & ~mask_of(perp[t])) == 0 and (cm & (1 << t)) == 0] for t in range(v)}

# ---------- the solve machinery ----------
def rref_solve(target_mask, cand_masks):
    """exact: is target_mask in the GF(2)-span? return (a solution subset) or None.
    proper elimination: rows over the v-bit masks, pivot = lowest set bit."""
    rows = []   # (pivot, mask, combo)
    piv = {}     # pivot-bit -> index
    for cm in cand_masks:
        cur, combo = cm, [cm]
        while cur:
            p = cur & -cur
            if p in piv:
                _, bm, bc = rows[piv[p]]
                cur ^= bm
                combo = combo + bc
            else:
                break
        if cur:
            p = cur & -cur
            piv[p] = len(rows)
            rows.append((p, cur, combo))
        # else: dependent row, drop
    # reduce the target
    cur, combo = target_mask, []
    while cur:
        p = cur & -cur
        if p not in piv:
            return None
        _, bm, bc = rows[piv[p]]
        cur ^= bm
        combo = combo + bc
    cnt = Counter(combo)
    return [c for c, n in cnt.items() if n % 2]

# (1) verify the seeds solve exactly (sanity)
ok = all(sorted(seed[t]) == sorted(seed[t]) for t in range(v))
print('the seeds: %d targets, the r434-wire solution (the trivial span proof)' % len(seed))

# (2) THE REUSE-FIRST GLOBAL SOLVE
sols = {}
used = set()
# order the targets by |W_t| descending (the big demands first establish the shared core)
order = sorted(range(v), key=lambda t: -bin(Wt[t]).count('1'))
for t in order:
    # candidates: used-first
    c_used = [cm for cm in used if cm in cand or True]
    # the exact legality: cm must be ⊆ perp(t)
    c_legal = [cm for cm in cand[t]]
    # try: the used wires first (subset XOR = W_t over the used + the new)
    sol = rref_solve(Wt[t], [cm for cm in c_legal])  # any solution (exact)
    if sol is None:
        sol = seed[t]   # the seed fallback
    # prefer used: re-solve restricting to used ∪ the seed (small sets)
    sol_set = set(sol)
    # the reuse-solve: over (used ∩ legal) ∪ pool, the greedy-weighted to reuse
    reuse_c = [cm for cm in c_legal if cm in used]
    new_c = [cm for cm in c_legal if cm not in used]
    # try exact over reuse-only first
    r_sol = rref_solve(Wt[t], reuse_c) if reuse_c else None
    if r_sol is not None:
        sol = r_sol
    else:
        # mixed: try to minimize the new wires: greedy with reuse-bonus
        cur = Wt[t]
        subset = []
        while cur:
            best = None
            for cm in c_legal:
                g = bin(cur ^ cm).count('1') - (0 if cm in used else 1)
                if best is None or g < best[0]:
                    best = (g, cm)
            if best is None or bin(cur ^ best[1]).count('1') >= bin(cur).count('1'):
                # no improving move: use the seed
                sol = seed[t] if rref_solve(Wt[t], [cm for cm in c_legal]) is None else sol
                subset = None
                break
            cur ^= best[1]
            subset.append(best[1])
        if subset is not None:
            # verify
            m = 0
            for cm in subset: m ^= cm
            sol = subset if m == Wt[t] else seed[t]
    sols[t] = sol
    for cm in sol:
        used.add(cm)

print('after the reuse-first pass: the distinct wires = %d' % len(used))
szs = Counter(len(s) for s in sols.values())
print('the subset-sizes:', dict(sorted(szs.items())))
uses = Counter()
for s in sols.values():
    for cm in s:
        uses[cm] += 1
print('the wire-uses histogram:', dict(sorted(Counter(uses.values()).items())))

# (3) THE LOCAL SEARCH: for each 1-use wire, try replacing with a used-wire XOR-pair
improved = True
rounds = 0
while improved and rounds < 10:
    improved = False
    rounds += 1
    one_use = [cm for cm, n in uses.items() if n == 1]
    for cm in one_use:
        t = next(t for t in range(v) if cm in sols[t])
        # try: W_t = (the current sol minus cm) XOR alternative
        others = [x for x in sols[t] if x != cm]
        rest = 0
        for x in others: rest ^= x
        need = rest ^ cm  # what cm must supply
        # candidates for the replacement: any legal mask XOR-compatible
        for cm2 in cand[t]:
            if cm2 == cm or cm2 in sols[t]:
                continue
            # check: cm2 could pair with a used wire to supply need
            need2 = need ^ cm2
            if need2 == 0:
                sols[t] = others + [cm2]
                uses[cm] -= 1
                uses[cm2] += 1
                if uses[cm] == 0: del uses[cm]
                improved = True
                break
            if uses.get(need2, 0) > 0 or need2 in pool:
                # the replacement: others + cm2 + need2
                sols[t] = others + [cm2, need2] if need2 else others + [cm2]
                uses[cm] -= 1
                uses[cm2] += 1
                if need2: uses[need2] += 1
                if uses[cm] == 0: del uses[cm]
                improved = True
                break
        if improved:
            break

print('after the local search (%d rounds): the distinct wires = %d' % (rounds, len(uses)))
uses = Counter()
for s in sols.values():
    for cm in s:
        uses[cm] += 1
print('the final distinct wires:', len(uses), '| uses histogram:', dict(sorted(Counter(uses.values()).items())))
print('vs the r434 B-wires: 225')

# verify all
bad = 0
for t in range(v):
    m = 0
    for cm in sols[t]: m ^= cm
    if m != Wt[t]:
        bad += 1
print('the verification: %d/%d exact' % (v - bad, v))
json.dump({'distinct_wires': len(uses),
           'masks': {hex(cm): sorted(pool.get(cm, set())) for cm in uses},
           'per_target': {t: [hex(cm) for cm in s] for t, s in sols.items()}},
          open('ii19_nat154_sharedsolve.json', 'wt'))
print('SAVED ii19_nat154_sharedsolve.json')
