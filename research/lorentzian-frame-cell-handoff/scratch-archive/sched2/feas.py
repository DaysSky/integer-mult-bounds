"""Feasibility of a junction-only (split-free) schedule for a given pair sequence with UNCOUPLED junction transforms
diag(A, B), A, B in SL2(Z) with entries in [-E, E].  BFS by stage with exact rank pruning (every local after the first
lowers rank(XX) + rank(YY) by exactly one) and state dedupe.  Prints one witness per feasible F/R pattern found.
usage: feas.py 'seq' E [maxpat]"""
import sys, itertools, json
K = None
def rank_int(rows):
    A = [list(r) for r in rows]; r = 0
    cols = len(A[0]) if A else 0
    for c in range(cols):
        piv = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if piv is None: continue
        A[r], A[piv] = A[piv], A[r]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f, g = A[i][c], A[r][c]
                A[i] = [g * x - f * y for x, y in zip(A[i], A[r])]
        r += 1
    return r
def pot(M, K):
    XX = [[M[2 * i][2 * j] for j in range(K)] for i in range(K)]
    YY = [[M[2 * i + 1][2 * j + 1] for j in range(K)] for i in range(K)]
    return rank_int(XX) + rank_int(YY)
def loc(M, p, rev):
    M = [list(r) for r in M]
    if rev: M[2 * p] = [x - y for x, y in zip(M[2 * p], M[2 * p + 1])]
    else: M[2 * p + 1] = [x + y for x, y in zip(M[2 * p + 1], M[2 * p])]
    return M
def junc(M, p, q, A, B):
    M = [list(r) for r in M]
    xp, xq, yp, yq = M[2 * p], M[2 * q], M[2 * p + 1], M[2 * q + 1]
    M[2 * p] = [A[0][0] * a + A[0][1] * b for a, b in zip(xp, xq)]
    M[2 * q] = [A[1][0] * a + A[1][1] * b for a, b in zip(xp, xq)]
    M[2 * p + 1] = [B[0][0] * a + B[0][1] * b for a, b in zip(yp, yq)]
    M[2 * q + 1] = [B[1][0] * a + B[1][1] * b for a, b in zip(yp, yq)]
    return M
def feasible(seq, E, pats=None, limit_states=200000):
    K = max(seq) + 1; s = len(seq); n = 2 * K
    SL = [((a, b), (c, d)) for a in range(-E, E + 1) for b in range(-E, E + 1) for c in range(-E, E + 1)
          for d in range(-E, E + 1) if a * d - b * c == 1]
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    found = []
    for fr in (pats or itertools.product((False, True), repeat=s)):
        if fr[0]: continue                       # first local F (R is the mirror)
        layer = {json.dumps(loc(I, seq[0], fr[0])): (loc(I, seq[0], fr[0]), [])}
        P = 2 * K; ok = True
        for b in range(1, s):
            nl = {}
            for key, (M, wit) in layer.items():
                if seq[b] == seq[b - 1]:
                    opts = [(M, None)]
                else:
                    opts = [(junc(M, seq[b - 1], seq[b], A, B), (A, B)) for A in SL for B in SL]
                for M1, j in opts:
                    M2 = loc(M1, seq[b], fr[b])
                    if pot(M2, K) != P - 1: continue
                    k2 = json.dumps(M2)
                    if k2 not in nl: nl[k2] = (M2, wit + [j])
                if len(nl) > limit_states: break
            P -= 1; layer = nl
            if not layer: ok = False; break
        if ok and layer:
            M, wit = next(iter(layer.values()))
            found.append((''.join('R' if f else 'F' for f in fr), wit, M))
            return found
    return found
if __name__ == '__main__':
    seq = json.loads(sys.argv[1]); E = int(sys.argv[2])
    f = feasible(seq, E)
    print(seq, 'E', E, 'feasible' if f else 'none found', f[0][0] if f else '', f[0][1] if f else '', flush=True)
