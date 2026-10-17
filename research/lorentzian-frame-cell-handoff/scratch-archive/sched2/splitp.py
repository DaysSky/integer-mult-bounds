"""General schedule search over F_2 with optional SPLITS.  At time b (between stages b-1 and b) the pairs at level b
are p_{b-1}, p_b and any idle pairs Z_b we choose to split at level b; any transform diag(A, B), A, B in GL(F_2) on the
X and Y registers of those pairs is allowed (legal: all at a common level).  Potential pruning as in feasp.py.
State = (matrix, split record).  Reports feasible split choices and slot multisets.
usage: splitp.py 'seq' maxsplits"""
import sys, json, itertools
from feasp import rank_p
p = 2
def gl(n):
    out = []
    for bits in itertools.product((0, 1), repeat=n * n):
        M = [bits[i * n:(i + 1) * n] for i in range(n)]
        if rank_p(M, 2) == n: out.append(tuple(map(tuple, M)))
    return out
GL = {1: gl(1), 2: gl(2), 3: gl(3)}
def run(seq, maxs):
    K = max(seq) + 1; s = len(seq); n = 2 * K
    def pot(M):
        return rank_p([[M[2 * i][2 * j] for j in range(K)] for i in range(K)], 2) + \
               rank_p([[M[2 * i + 1][2 * j + 1] for j in range(K)] for i in range(K)], 2)
    def loc(M, q, rev):
        M = list(M)
        if rev: M[2 * q] = tuple((x + y) % 2 for x, y in zip(M[2 * q], M[2 * q + 1]))
        else: M[2 * q + 1] = tuple((x + y) % 2 for x, y in zip(M[2 * q + 1], M[2 * q]))
        return tuple(M)
    def tr(M, prs, A, B):
        M = list(M); xs = [M[2 * r] for r in prs]; ys = [M[2 * r + 1] for r in prs]
        for i, r in enumerate(prs):
            M[2 * r] = tuple(sum(A[i][k] * xs[k][c] for k in range(len(prs))) % 2 for c in range(n))
            M[2 * r + 1] = tuple(sum(B[i][k] * ys[k][c] for k in range(len(prs))) % 2 for c in range(n))
        return tuple(M)
    act = {r: [j for j in range(s) if seq[j] == r] for r in range(K)}
    def idle_at(r, b):          # r idle across level b strictly inside its idle interval
        last = max([j for j in act[r] if j < b], default=-1); nxt = min([j for j in act[r] if j >= b], default=s)
        return (last + 1) < b < nxt
    I = tuple(tuple(int(i == j) for j in range(n)) for i in range(n))
    layer = {(loc(I, seq[0], False), ()): None}
    P = 2 * K; hist = [layer]
    for b in range(1, s):
        nl = {}
        a, c = seq[b - 1], seq[b]
        base = [a] if a == c else [a, c]
        for (M, splits), _ in layer.items():
            idle = [r for r in range(K) if r not in base and idle_at(r, b)]
            for k in range(0, min(maxs - len(splits), len(idle), 1) + 1):
                for Z in itertools.combinations(idle, k):
                    prs = base + list(Z)
                    if len(prs) == 1: opts = [M]
                    else: opts = [tr(M, prs, A, B) for A in GL[len(prs)] for B in GL[len(prs)]]
                    sp2 = splits + tuple((r, b) for r in Z)
                    for M1 in opts:
                        for rev in (False, True):
                            M2 = loc(M1, c, rev)
                            key = (M2, sp2)
                            if key in nl: continue
                            if pot(M2) != P - 1: continue
                            nl[key] = ((M, splits), rev)
        P -= 1; layer = nl; hist.append(layer)
        if not layer: return []
    return sorted({sp for (M, sp) in layer})
def slots(seq, splits, a=7):
    K = max(seq) + 1; s = len(seq); out = []
    for r in range(K):
        actv = [j for j in range(s) if seq[j] == r]; lv = 0
        cuts = sorted(b for (q, b) in splits if q == r)
        bounds = []
        for j in actv + [s]:
            if j > lv:
                pts = [lv] + [x for x in cuts if lv < x < j] + [j]
                out += [(pts[i + 1] - pts[i]) * a for i in range(len(pts) - 1)]
            lv = j + 1
    return tuple(sorted(out, reverse=True))
if __name__ == '__main__':
    seq = json.loads(sys.argv[1]); maxs = int(sys.argv[2])
    res = run(seq, maxs)
    print(seq, 'feasible split sets:', len(res))
    for sp in res[:20]: print('  splits', sp, 'slots', slots(seq, sp))
