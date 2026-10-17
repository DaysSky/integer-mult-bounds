"""Rigorous necessary test over F_p: an integer split-free schedule (junction transforms products of integer adds, so
in SL2(Z)) reduces mod p to an F_p schedule with junctions in SL2(F_p) whose middle product is anti-diagonal with
invertible blocks.  Over F_p the potential rk(XX) + rk(YY) starts at 2K, ends at 0, changes by <= 1 per local, and the
first local cannot lower it, so every later local lowers it by exactly one.  Exhaustive BFS (no truncation).
usage: feasp.py p 'seq' [pattern|all]"""
import sys, itertools, json
def rank_p(rows, p):
    A = [list(r) for r in rows]; r = 0
    for c in range(len(A[0]) if A else 0):
        piv = next((i for i in range(r, len(A)) if A[i][c] % p), None)
        if piv is None: continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [x * inv % p for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        r += 1
    return r
def make(p, K):
    n = 2 * K
    SL = [((a, b), (c, d)) for a in range(p) for b in range(p) for c in range(p) for d in range(p) if (a * d - b * c) % p == 1]
    def pot(M):
        return rank_p([[M[2 * i][2 * j] for j in range(K)] for i in range(K)], p) + \
               rank_p([[M[2 * i + 1][2 * j + 1] for j in range(K)] for i in range(K)], p)
    def loc(M, q, rev):
        M = list(M)
        if rev: M[2 * q] = tuple((x - y) % p for x, y in zip(M[2 * q], M[2 * q + 1]))
        else: M[2 * q + 1] = tuple((x + y) % p for x, y in zip(M[2 * q + 1], M[2 * q]))
        return tuple(M)
    def junc(M, a, b, A, B):
        M = list(M); xa, xb, ya, yb = M[2 * a], M[2 * b], M[2 * a + 1], M[2 * b + 1]
        M[2 * a] = tuple((A[0][0] * u + A[0][1] * w) % p for u, w in zip(xa, xb))
        M[2 * b] = tuple((A[1][0] * u + A[1][1] * w) % p for u, w in zip(xa, xb))
        M[2 * a + 1] = tuple((B[0][0] * u + B[0][1] * w) % p for u, w in zip(ya, yb))
        M[2 * b + 1] = tuple((B[1][0] * u + B[1][1] * w) % p for u, w in zip(ya, yb))
        return tuple(M)
    return SL, pot, loc, junc
def feasible_p(seq, p, pats=None, want_witness=True):
    K = max(seq) + 1; s = len(seq); n = 2 * K
    SL, pot, loc, junc = make(p, K)
    I = tuple(tuple(int(i == j) for j in range(n)) for i in range(n))
    res = []
    for fr in (pats or itertools.product((False, True), repeat=s)):
        if fr[0]: continue
        layer = {loc(I, seq[0], fr[0]): []}
        P = 2 * K
        for b in range(1, s):
            nl = {}
            for M, wit in layer.items():
                opts = [(M, None)] if seq[b] == seq[b - 1] else \
                       [(junc(M, seq[b - 1], seq[b], A, B), (A, B)) for A in SL for B in SL]
                for M1, j in opts:
                    M2 = loc(M1, seq[b], fr[b])
                    if M2 in nl: continue
                    if pot(M2) != P - 1: continue
                    nl[M2] = wit + [j]
            P -= 1; layer = nl
            if not layer: break
        if layer:
            res.append((''.join('R' if f else 'F' for f in fr), next(iter(layer.items()))))
            if want_witness: return res
    return res
if __name__ == '__main__':
    p = int(sys.argv[1]); seq = json.loads(sys.argv[2])
    f = feasible_p(seq, p)
    print(seq, 'p', p, 'FEASIBLE ' + f[0][0] if f else 'INFEASIBLE (all patterns)', flush=True)
