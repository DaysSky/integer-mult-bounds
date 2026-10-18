"""THE FRONTIER LADDER RUNG (ii19_nat67.py) — the rank-preserving extensions!!

THE SYSTEM (nat66!!): the P111 = 8 axes + 91 signed weight-4 + 12 constant-weight-4
(raw-norm-4, the form I/2, THE DECODER RANK 9!!); THE POOL: 568 canonical (the 457
extension candidates!!). THE V-SWEEP'S LADDER (the nat46!!): the 120 (R 470): +13.07%!!
the 125 (490): +19.59%!! the 130 (510): +25.55%!!!
HERE: (1) the greedy extension from the P111 (the pool-lines added (the RANK-GROWTH
MINIMIZED (the sparse-decoder-preserving!!))!!); (2) the rank gates at v = 120/125/130;
(3) the ip-structure checks (the P111-compat!!); (4) THE ECONOMY + THE PRICES!!!
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
import pricer
log = lambda *a: print(*a, file=sys.stderr, flush=True)
price = lambda hist, v, h, R: pricer.price({int(k): int(val) for k, val in hist.items()}, v, h, R)
FC = Fraction(str('0.001744385950814795279853'))

D66 = json.load(open('ii19_nat66_pool.json', 'rt'))
import ast
poolcanon = {tuple(ast.literal_eval(k)): tuple(v) for k, v in D66['pool'].items()}
P111 = [tuple(k) for k in D66['P111']]
log('the pool: %d | the P111: %d' % (len(poolcanon), len(P111)))

def gf2_rank(M):
    M = M.copy(); rr = 0; rows, cols = M.shape
    for c in range(cols):
        p = next((i for i in range(rr, rows) if M[i][c]), None)
        if p is None: continue
        M[[rr, p]] = M[[p, rr]]
        for i in range(rows):
            if i != rr and M[i][c]:
                M[i] ^= M[rr]
        rr += 1
    return rr

def census(lines):
    V = len(lines)
    G = [[sum(a[i] * b[i] for i in range(8)) for b in lines] for a in lines]
    PERP = [set(s for s in range(V) if s != t and G[s][t] == 0) for t in range(V)]
    B0 = np.array([[1 if (s == t or s in PERP[t]) else 0 for s in range(V)] for t in range(V)], dtype=np.uint8)
    return V, PERP, gf2_rank(B0), G

V0, PERP0, RANK0, G0 = census(P111)
log('THE CONTROL: v %d | the perps %s | the rank %d' % (
    V0, dict(sorted(Counter(len(p) for p in PERP0).items())), RANK0))

# (1) THE GREEDY EXTENSION: the pool-lines added one at a time: the RANK-GROWTH
# minimized (the candidates sorted by the rank-delta then by the perp-richness!!)
cands = [tuple(poolcanon[k]) for k in poolcanon if poolcanon[k] not in set(P111)]
log('the extension candidates: %d' % len(cands))
def rank_with(lines, extra):
    V = len(lines) + len(extra)
    Ls = list(lines) + list(extra)
    G = [[sum(a[i] * b[i] for i in range(8)) for b in Ls] for a in Ls]
    PERP = [set(s for s in range(V) if s != t and G[s][t] == 0) for t in range(V)]
    B0 = np.array([[1 if (s == t or s in PERP[t]) else 0 for s in range(V)] for t in range(V)], dtype=np.uint8)
    return gf2_rank(B0), PERP, G

cur = list(P111)
for target in (120, 125, 130):
    while len(cur) < target:
        best = None
        for c in cands:
            if c in cur: continue
            r, PERP, G = rank_with(cur, [c])
            # the ip-compat: the new line vs the current (the norms ±!!): prefer the
            # 0/+-2-ips (the P111-class!!)!!
            ips = Counter(G[i][len(cur)] for i in range(len(cur)))
            if any(k not in (0, 2, -2) for k in ips):
                continue
            key = (r, -len([k for k in ips if k == 0]))
            if best is None or key < best[0]:
                best = (key, c, r)
        if best is None:
            log('    NO more compatible candidates at %d!!' % len(cur))
            break
        cur.append(best[1])
        if len(cur) % 5 == 0 or len(cur) == target:
            log('    v %d: the rank %d' % (len(cur), best[2]))
    V, PERP, RANK, G = census(cur)
    log('(2) THE EXTENSION AT v %d: the perps %s | THE RANK %d' % (
        V, dict(sorted(Counter(len(p) for p in PERP).items())), RANK))
    # (3) THE ECONOMY (the (3,4)-greedy!!)
    def greedy(PERP, V, kmin, umin):
        pair_count = Counter(); pair_users = defaultdict(list)
        for ti, pl in enumerate(PERP):
            for a, b in itertools.combinations(sorted(pl), 2):
                pair_count[(a, b)] += 1; pair_users[(a, b)].append(ti)
        covered = [set() for _ in range(V)]
        pool2 = []
        while True:
            cands2 = []
            for (a, b), c in pair_count.items():
                if c < 2: continue
                users = [ti for ti in pair_users[(a, b)] if a not in covered[ti] and b not in covered[ti]]
                if len(users) < umin: continue
                common = None
                for ti in users:
                    unc = PERP[ti] - covered[ti]
                    common = unc if common is None else (common & unc)
                if common is None or len(common) < kmin: continue
                piece = frozenset(sorted(common)[:kmin])
                real = [ti for ti in users if piece <= PERP[ti] - covered[ti]]
                if len(real) < umin: continue
                saving = len(piece) * len(real) - (len(piece) + len(real))
                if saving <= 0: continue
                cands2.append((saving, piece, real))
            if not cands2: break
            cands2.sort(key=lambda c: c[0], reverse=True)
            for saving, piece, real in cands2[:50]:
                if any(piece <= PERP[ti] - covered[ti] for ti in real):
                    pool2.append((piece, real))
                    for ti in real: covered[ti] |= set(piece)
                    break
            else: break
        left = [PERP[t] - covered[t] for t in range(V)]
        return pool2, left
    pool2, left = greedy(PERP, V, 3, 4)
    RET = max(9, RANK)
    R = len(pool2) + sum(1 for lo in left if lo) + RET
    log('(3) v %d: %d pieces + %d carriers + %d gathers = R %d (R/v %.2f!!)' % (
        V, len(pool2), sum(1 for lo in left if lo), RET, R, R / V))
    # (4) THE PRICE (the frontier's shape (the nat49-style!!))
    hist0 = {1: 1311, 2: 1339, 3: 69, 4: 45, 5: 103, 6: 12, 7: 18}
    base = dict(hist0); base[7] -= 9
    bm = sum(r * c for r, c in base.items())
    cst = 7 * RET
    climb = 8 * R + 2 * V * 7
    acc = Counter()
    for r in sorted(base, key=lambda r: -base[r] * r):
        acc[r] = int(Fraction(climb * (base[r] * r), bm) / r)
    rem = climb - sum(r * c for r, c in acc.items())
    while rem > 0:
        for r in sorted(base, key=lambda r: -base[r]):
            if r <= rem: acc[r] += 1; rem -= r; break
        else:
            acc[max(1, rem)] += 1; rem = 0
    acc[7] += RET
    c = price(dict(acc), V, 8, R)
    if c and c[0] and 1e-4 < float(c[0]) < 1e-2:
        log('(4) v %d: THE FRONTIER-SHAPE PRICE at (v %d, 8, R %d): %+.2f%% vs the FRONTIER!!!' % (
            V, V, R, 100 * (float(c[0]) / float(FC) - 1)))
    else:
        log('(4) v %d: NO-ROOT/spurious' % V)
    json.dump({'lines': [list(l) for l in cur], 'R': R, 'rank': RANK},
              open('ii19_nat67_ext%d.json' % V, 'w'))
log('saved the extension JSONs!!')
