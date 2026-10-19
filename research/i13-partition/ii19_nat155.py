"""nat155: THE 121's SHARED-CONTENT MINIMUM (the E8-LEVER-A's Lorentzian application).

The W4 (v=121, R=472, gcheck-PASSING) has 283 B-wires already shared (129 used 2x, 24 used 3-6x).
The crossing zone needs R <= 280 (the -192). The shared-content minimum:
(1) the pool: the perp-intersection contents (the pair/triple shared ⊥-sets) + the W4's own wires;
(2) the reuse-first global solve on the W4's B-parities;
(3) the verdict: the recomposed B-wire family + the recomposed R + the price at the band.
"""
import json
from collections import Counter
from itertools import combinations

W = json.load(open('ii19_own_word4.json'))
v = W['v']
print('the W4: v=%d, R=%d' % (v, W['R']))
lines = [tuple(int(c) for c in l) for l in W['lines']]
print('the lines: %d, the dims: %d' % (len(lines), len(lines[0])))

n = len(lines[0])

# the form: (x,y)/2 - the W4's form: check
print('the form:', W.get('form', '?') if not isinstance(W.get('form'), dict) else 'dict')

def ip2(i, j):
    return sum(a*b for a, b in zip(lines[i], lines[j]))

adj = [[(ip2(i, j) % 2 != 0 or ip2(i, j)//2 != 0) for j in range(v)] for i in range(v)]
perp = [frozenset(j for j in range(v) if j != i and not adj[i][j]) for i in range(v)]
print('the perp-size census:', dict(sorted(Counter(len(p) for p in perp).items())))

# the W4's B-parities
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
    m, sd = 0, []
    for s in ss:
        if s >= 2*v:
            m ^= val[s]
            sd.append(val[s] & ((1 << v) - 1))
    Wt[t] = m
    seed[t] = sd
print('the per-target |W_t| census:', dict(sorted(Counter(bin(m).count('1') for m in Wt.values()).items())))
print('the seeds: %d targets' % len(seed))

def mask_of(S):
    m = 0
    for i in S: m |= 1 << i
    return m

# THE POOL
pool = {}
cnt2 = 0
for i, j in combinations(range(v), 2):
    S = perp[i] & perp[j]
    if len(S) >= 14:
        m = mask_of(S)
        if m not in pool:
            pool[m] = {i, j}
            cnt2 += 1
print('the pair-contents (>=14 lines): %d' % cnt2)
cnt3 = 0
for i, j, k in combinations(range(v), 3):
    S = perp[i] & perp[j] & perp[k]
    if len(S) >= 18:
        m = mask_of(S)
        if m not in pool:
            pool[m] = {i, j, k}
            cnt3 += 1
print('the triple-contents (>=18 lines): %d' % cnt3)
for t, sd in seed.items():
    for cm in sd:
        pool.setdefault(cm, set()).add(t)
print('the pool total:', len(pool))

cand = {t: [cm for cm in pool if (cm & ~mask_of(perp[t])) == 0 and (cm & (1 << t)) == 0] for t in range(v)}
print('the per-target candidate counts:', dict(sorted(Counter(len(c) for c in cand.values()).items())))

# THE REUSE-FIRST SOLVE (the nat154-machinery)
def rref_solve(target_mask, cand_masks):
    rows, piv = [], {}
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
    cur, combo = target_mask, []
    while cur:
        p = cur & -cur
        if p not in piv:
            return None
        _, bm, bc = rows[piv[p]]
        cur ^= bm
        combo = combo + bc
    cnt = Counter(combo)
    return [c for c, nn in cnt.items() if nn % 2]

sols = {}
used = set()
order = sorted(range(v), key=lambda t: -bin(Wt[t]).count('1'))
nsolve = 0
for t in order:
    c_legal = cand[t]
    reuse_c = [cm for cm in c_legal if cm in used]
    sol = rref_solve(Wt[t], reuse_c) if reuse_c else None
    if sol is None:
        # the mixed greedy with the reuse-bonus
        cur = Wt[t]
        subset = []
        okflag = True
        while cur:
            best = None
            for cm in c_legal:
                g = bin(cur ^ cm).count('1') - (0.5 if cm in used else 0)
                if best is None or g < best[0]:
                    best = (g, cm)
            if best is None or bin(cur ^ best[1]).count('1') >= bin(cur).count('1'):
                okflag = False
                break
            cur ^= best[1]
            subset.append(best[1])
        if okflag and cur == 0:
            sol = subset
        else:
            sol = seed[t]
    else:
        nsolve += 1
    sols[t] = sol
    for cm in sol:
        used.add(cm)

uses = Counter()
for s in sols.values():
    for cm in s:
        uses[cm] += 1
print('the reuse-exact hits: %d' % nsolve)
print('THE RECOMPOSED B-WIRES: %d (vs the W4 actual: 283)' % len(uses))
print('the uses histogram:', dict(sorted(Counter(uses.values()).items())))

# the verification
bad = 0
for t in range(v):
    m = 0
    for cm in sols[t]: m ^= cm
    if m != Wt[t]:
        bad += 1
print('the verification: %d/%d exact' % (v - bad, v))

# THE R-ACCOUNT: the W4's R minus the B-side delta + the A-side's proportional delta
delta_b = 283 - len(uses)
# the A-side: the wires' builds (the intermediates): the naive proportion: the R ~ the R - delta_b - (the A-side's shares)
# the honest: report the B-side delta + the band
print()
print('THE B-SIDE DELTA: %d wires' % delta_b)
for aa in [1.0, 0.75, 0.5, 0.25]:
    r_new = W['R'] - delta_b - int(delta_b * aa)
    print('  at the A-proportion %.2f: R ~ %d' % (aa, r_new))

json.dump({'recomposed_wires': len(uses),
           'masks': {hex(cm): sorted(pool.get(cm, set())) for cm in uses},
           'per_target': {t: [hex(cm) for cm in s] for t, s in sols.items()}},
          open('ii19_nat155_shared121.json', 'wt'))
print('SAVED ii19_nat155_shared121.json')
