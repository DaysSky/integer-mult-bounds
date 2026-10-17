"""Root-like line systems at window h = 9: norm-2 vectors in R^{8,1}, pairwise products in {0, +-1}, lines up to sign.
Claim: at most 127 lines (E8's 120 is the largest found).  Two steps, both exact:

(1) Frame-free systems have <= 119 lines.  The Gram mod 2 is alternating of F2-rank <= 8, so the lines map to vectors
    x_a of a symplectic F2^8 with B(x_a, x_b) = 1 iff a, b are non-orthogonal (twins allowed).  Lines whose images lie
    in one Lagrangian are mutually orthogonal.  Double counting over the 2295 Lagrangians (135 through each nonzero
    vector, all through 0) gives v <= 119 - 16 m(0) when no Lagrangian holds 8 lines.  Checked by enumeration below.
(2) Systems with an orthogonal 8-frame e_1..e_8.  Any other line has x_i = <u, e_i> in {0, +-1}, support k >= 4 and an
    n-part gamma with gamma^2 = k/2 - 2 (n spans E^perp, norm -1).  Products are rational only inside a class:
      A: k in {4, 6};  B: k in {4, 5, 8} (k5-k8 pairs are parity-incompatible: B1 = {4, 5}, B2 = {4, 8});
      C: k in {4, 7};  Euclidean: k = 4 only (<= 8 + 112 = 120).
    Same-support sign patterns of a k > 4 class form a diameter <= 3 code (Kleitman: 2k).  Support families must meet
    parity conditions.  Exact maxima of the resulting support weights (CP-SAT / exhaustive) bound every class.
"""
import itertools
from ortools.sat.python import cp_model

# ---------- (1) Lagrangian count on symplectic F2^8 ----------
def lagrangian_check():
    n = 8
    def B(x, y):   # standard symplectic form, pairs (0,1), (2,3), (4,5), (6,7); vectors as ints
        s = 0
        for i in range(0, n, 2):
            s ^= (((x >> i) & 1) & ((y >> (i + 1)) & 1)) ^ (((x >> (i + 1)) & 1) & ((y >> i) & 1))
        return s
    # enumerate Lagrangians as sets of 16 vectors via reduced spanning sets
    seen = set(); stack = [frozenset([0])]
    lag = set()
    def closure(S, v):
        return frozenset(S | {s ^ v for s in S})
    frontier = [frozenset([0])]
    for d in range(4):
        nxt = set()
        for S in frontier:
            for v in range(1, 256):
                if v in S: continue
                if all(B(v, s) == 0 for s in S): nxt.add(closure(S, v))
        frontier = nxt
    L = frontier
    through = [0] * 256
    for S in L:
        for v in S: through[v] += 1
    assert len(L) == 2295 and through[0] == 2295 and all(through[v] == 135 for v in range(1, 256))
    # max lines with no Lagrangian holding >= 8 (fractional double count): m0 + sum m <= m0 + (7 - m0) * 2295 / 135
    return len(L), max(m0 + (7 - m0) * 2295 // 135 for m0 in range(8))

# ---------- (2) frame classes, support level ----------
P = range(8)
S4 = [frozenset(c) for c in itertools.combinations(P, 4)]
def support_max(k, ck, kk_ok, k4_ok, kill_inside=False):
    """max sum_T (8 - kill_T) y_T + ck sum_S z_S over parity-compatible families with >= 1 k-support."""
    Sk = [frozenset(c) for c in itertools.combinations(P, k)]
    m = cp_model.CpModel()
    y = {T: m.NewBoolVar('') for T in S4}; z = {S: m.NewBoolVar('') for S in Sk}
    for a, b in itertools.combinations(S4, 2):
        if len(a & b) % 2: m.AddBoolOr([y[a].Not(), y[b].Not()])
    for a, b in itertools.combinations(Sk, 2):
        if not kk_ok(a, b): m.AddBoolOr([z[a].Not(), z[b].Not()])
    for T in S4:
        for S in Sk:
            if not k4_ok(T, S): m.AddBoolOr([y[T].Not(), z[S].Not()])
    kill = {T: m.NewBoolVar('') for T in S4}
    if kill_inside:
        for T in S4:
            for S in Sk:
                if T <= S: m.AddBoolOr([y[T].Not(), z[S].Not(), kill[T]])
    else:
        for T in S4: m.Add(kill[T] == 0)
    m.Add(sum(z.values()) >= 1)
    m.Maximize(sum(8 * y[T] - kill[T] for T in S4) + ck * sum(z.values()))
    s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = 1200
    r = s.Solve(m); assert s.StatusName(r) == 'OPTIMAL'
    return int(s.ObjectiveValue())

if __name__ == '__main__':
    nl, ff = lagrangian_check()
    print('(1) Lagrangians of Sp(8,2): %d (135 through each nonzero vector); frame-free systems <= %d lines' % (nl, ff))
    even = lambda a, b: len(a & b) % 2 == 0
    A = support_max(6, 12, even, even)
    B1 = support_max(5, 10, lambda a, b: len(a & b) % 2 == 1, even, kill_inside=True)
    C = support_max(7, 14, lambda a, b: a == b, lambda T, S: T <= S)
    # B2: k8 lines (x; 2), x in {+-1}^8, pairwise distance 1..3 (<= 16); each kills one k4 class on every support
    B2 = 7 * 14 + 16
    print('(2) frame systems: Euclidean <= 120;  A (k4,k6) <= %d;  B1 (k4,k5) <= %d;  B2 (k4,k8) <= %d;  C (k4,k7) <= %d'
          % (8 + A, 8 + B1, 8 + B2, 8 + C))
    print('=> root-like systems in R^{8,1}: at most %d lines' % max(ff, 120, 8 + A, 8 + B1, 8 + B2, 8 + C))
