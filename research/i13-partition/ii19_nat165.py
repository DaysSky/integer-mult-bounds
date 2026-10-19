"""nat165: THE CORE-PRESERVED DEEP RE-SOLVE (the B-side's true minimum).

The nat155 greedy (242) discarded the W4's shared core (129x2 + 24x3-6 users!).
The core-preserved re-solve: the W4's shared wires (>=2 users) MANDATORY;
the 130 privates re-solved over (core + pool + the used-set preference) -> the true min.
"""
import json
from collections import Counter, defaultdict

W4 = json.load(open('ii19_own_word4.json'))
v = W4['v']
nreg = 2*v + W4['R']
X = (1 << v) - 1

val = [0]*nreg
for s in range(v): val[s] = 1 << s
for F, d, ss in W4['D']:
    for s in ss: val[d] ^= val[s]
for F, d, ss in W4['A']:
    for s in ss: val[d] ^= val[s]

ret_set = set(W4['ret'])
tgt_srcs = defaultdict(list)
for F, d, ss in W4['B']:
    if v <= d < 2*v:
        tgt_srcs[d - v].extend(ss)

# the W4's actual per-target wire-solutions + the use census
Wt = {}
sol0 = {}
for t, ss in tgt_srcs.items():
    m = 0
    sol = []
    for s in ss:
        if s >= 2*v and s not in ret_set:
            m ^= val[s] & X
            sol.append(val[s] & X)
    Wt[t] = m
    sol0[t] = sol

use0 = Counter()
for sol in sol0.values():
    for cm in sol:
        use0[cm] += 1
core = {cm for cm, k in use0.items() if k >= 2}
priv0 = {cm for cm, k in use0.items() if k == 1}
print('the W4 core (>=2 users): %d | the privates: %d' % (len(core), len(priv0)), flush=True)

# the pool (the nat155's: the perp-intersections + the W4's own wires)
lines = [tuple(int(c) for c in l) for l in W4['lines']]
def ip2(i, j):
    return sum(a*b for a, b in zip(lines[i], lines[j]))
adj = [[(ip2(i, j) % 2 != 0 or ip2(i, j)//2 != 0) for j in range(v)] for i in range(v)]
perp = [frozenset(j for j in range(v) if j != i and not adj[i][j]) for i in range(v)]
def mask_of(S):
    m = 0
    for i in S: m |= 1 << i
    return m
pool = set()
for i in range(v):
    for j in range(i+1, v):
        S = perp[i] & perp[j]
        if len(S) >= 12:
            pool.add(mask_of(S))
pool |= core  # the core always available
print('the pool: %d (incl. the core)' % len(pool), flush=True)

# the re-solve: per target: the residual after the core; then the reuse-first greedy
# over the pool + the privates-as-needed
def rref_sparse(tm, cands):
    """the rref + the kernel-coset sampling for sparsity (the small pools)."""
    rows, piv = [], {}
    for cm in cands:
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
    cur, combo = tm, []
    while cur:
        p = cur & -cur
        if p not in piv:
            return None
        _, bm, bc = rows[piv[p]]
        cur ^= bm
        combo = combo + bc
    cnt = Counter(combo)
    return [c for c, nn in cnt.items() if nn % 2]

used = Counter()
new_sol = {}
for t in range(v):
    # the core's contribution to t: the core-masks ⊆ perp(t) that the W4 itself used for t
    own_core = [cm for cm in sol0[t]]
    # the residual: W_t minus the core-part the W4 delivered via its shared wires
    # strategy: KEEP the W4's core-reads for t; re-solve the private-part
    core_t = [cm for cm in sol0[t] if cm in core]
    priv_t = [cm for cm in sol0[t] if cm in priv0]
    res = 0
    for cm in priv_t:
        res ^= cm
    new_sol[t] = list(core_t)
    if not res:
        for cm in core_t: used[cm] += 1
        continue
    # the re-solve of the residual over (the pool (incl core) + all privates)
    pt = mask_of(perp[t])
    cands = [cm for cm in (pool | priv0) if (cm & ~pt) == 0 and (cm & (1 << t)) == 0]
    # the used-set preference: sort the candidates by (already-used first, bigger first)
    cands.sort(key=lambda cm: (used.get(cm, 0) == 0, -bin(cm).count('1')))
    sol = rref_sparse(res, cands)
    if sol is None:
        sol = priv_t  # the fallback: the W4's own privates
    new_sol[t] = core_t + sol
    for cm in new_sol[t]:
        used[cm] += 1

tot = len(used)
print('THE CORE-PRESERVED FAMILY: %d distinct (vs the W4: %d, vs nat155: 242)' % (
    tot, len(use0)), flush=True)
print('the uses histogram:', dict(sorted(Counter(used.values()).items())))
szs = Counter(len(s) for s in new_sol.values())
print('the per-target read-counts:', dict(sorted(szs.items())))
# the verification
bad = 0
for t in range(v):
    cur = 0
    for cm in new_sol[t]:
        cur ^= cm
    if cur != Wt[t]:
        bad += 1
print('the verification: %d/%d exact' % (v - bad, v))
json.dump({'distinct': tot,
           'masks': {hex(cm): bin(cm) for cm in used},
           'per_target': {t: [hex(cm) for cm in s] for t, s in new_sol.items()}},
          open('ii19_nat165_corefamily.json', 'wt'))
print('SAVED ii19_nat165_corefamily.json')
