"""Two pairs A=0, B=1 active in the same stages (n locals each, simultaneous), bridge words between them at every
inter-stage point (no idle split possible).  Is J_n L_n ... J_1 L_1 J_0 anti-diagonal (X->Y, Y->X) for some choice?"""
import itertools, numpy as np, sys
K = 2
def I(): return np.eye(4, dtype=np.int64)
def loc(p, rev):
    M = I()
    if rev: M[2 * p, 2 * p + 1] = -1
    else: M[2 * p + 1, 2 * p] = 1
    return M
def br(d, s, c):
    M = I(); M[2 * d, 2 * s] += c; M[2 * s + 1, 2 * d + 1] -= c; return M
def comp(ops):
    T = I()
    for M in ops: T = M @ T
    return T
X = [0, 2]; Y = [1, 3]
anti = lambda W: not W[np.ix_(X, X)].any() and not W[np.ix_(Y, Y)].any()
n = int(sys.argv[1]); maxj = int(sys.argv[2]); C = [-2, -1, 1, 2]
gens = [(0, 1, c) for c in C] + [(1, 0, c) for c in C]
JW = {}
for L in range(maxj + 1):
    for w in itertools.product(gens, repeat=L):
        M = comp([br(*b) for b in w]); JW.setdefault(M.tobytes(), M)
JW = list(JW.values()); print('junction matrices', len(JW), flush=True)
found = 0
for oA in itertools.product((False, True), repeat=n):
    for oB in itertools.product((False, True), repeat=n):
        Ls = [loc(0, oA[i]) @ loc(1, oB[i]) for i in range(n)]
        def rec(i, T):
            global found
            if i == n:
                for J in JW:
                    W = J @ T
                    if anti(W):
                        found += 1
                        if found <= 3: print('FOUND', oA, oB, W.tolist(), flush=True)
                return
            for J in JW:
                rec(i + 1, Ls[i] @ J @ T)
        rec(0, I())
print('n', n, 'maxj', maxj, 'solutions', found)
