"""Parallel ('level') schedules over F_2.  A level program is a list of levels, each a tuple of distinct pairs that run a
local (F or R) at that level.  At the boundary before level b the pairs at level b are those active at b-1 and at b
(idle pairs excluded: no splits); any transform diag(A, B), A, B in GL(F_2), on their X and Y registers is allowed.
Potential pruning: rk(XX) + rk(YY) starts at 2K, ends at 0, each local changes it by <= 1 and the locals of level 0
cannot lower it, so level 0 must hold exactly one local and every later local must lower it by exactly one (locals of
one level act on distinct pairs and commute; their joint drop must equal their number).
usage: levelp.py 'levels-json'   e.g. '[[0],[0,1],[1],[0]]'"""
import sys, json, itertools
from feasp import rank_p
def gl(n):
    out = []
    for bits in itertools.product((0, 1), repeat=n * n):
        M = [bits[i * n:(i + 1) * n] for i in range(n)]
        if rank_p(M, 2) == n: out.append(tuple(map(tuple, M)))
    return out
GL = {1: gl(1), 2: gl(2), 3: gl(3)}
def run(levels, witness=False, maxset=3):
    K = 1 + max(max(l) for l in levels); n = 2 * K
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
    assert len(levels[0]) == 1
    I = tuple(tuple(int(i == j) for j in range(n)) for i in range(n))
    layer = {loc(I, levels[0][0], False): None}; P = 2 * K; hist = [layer]
    for b in range(1, len(levels)):
        S = sorted(set(levels[b - 1]) | set(levels[b]))
        if len(S) > maxset: return 'skip'
        nl = {}
        for M in layer:
            opts = [M] if len(S) == 1 else [tr(M, S, A, B) for A in GL[len(S)] for B in GL[len(S)]]
            for M1 in opts:
                for revs in itertools.product((False, True), repeat=len(levels[b])):
                    M2 = M1
                    for q, rv in zip(levels[b], revs): M2 = loc(M2, q, rv)
                    if M2 in nl: continue
                    if pot(M2) != P - len(levels[b]): continue
                    nl[M2] = (M, revs)
        P -= len(levels[b]); layer = nl; hist.append(layer)
        if not layer: return False
    return True
if __name__ == '__main__':
    lv = json.loads(sys.argv[1])
    print(lv, run(lv))
