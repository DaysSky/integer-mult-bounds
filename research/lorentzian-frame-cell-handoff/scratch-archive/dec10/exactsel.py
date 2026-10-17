"""Exact best use of deficient codewords: choose disjoint index roles; constraints n_i . m_j = delta_ij for specified
vectors; completion exists if specified m's independent, n's independent and the cross constraints hold (dual
completion lemma).  Then evaluate exact cost by a completion that keeps them (try many completions)."""
import sys, itertools, random, numpy as np
from bestdec import f2_solve_basis, inv2, rk, A
B = np.load(sys.argv[1]) % 2
Ub, piv = f2_solve_basis(B); w = len(Ub); Wc = B[:, piv] % 2
span = lambda idx: np.linalg.matrix_rank(A[idx]) if len(idx) else 0
defS = []; defT = []
for bits in itertools.product((0, 1), repeat=w):
    m = np.array(bits, np.uint8)
    if not m.any(): continue
    P = np.nonzero((m @ Ub) % 2)[0]; Q = np.nonzero((Wc @ m) % 2)[0]
    if span(P) <= 7: defS.append(m)
    if span(Q) <= 7: defT.append(m)
print('dot products n.m (rows T-deficient, cols S-deficient):'); print(np.array([[int(n @ m % 2) for m in defS] for n in defT]))
def indep(vs): return len(vs) == 0 or len(f2_solve_basis(np.array(vs))[0]) == len(vs)
best = None; rng = random.Random(0)
# roles: each S-deficient m -> own piece or paired with a T-deficient n (same piece) or unused; each n similarly
for rs in itertools.product(range(-1, len(defT) + 1), repeat=len(defS)):   # -1 unused, k<len(defT): paired with n_k, len(defT): own piece
    used_n_pair = [r for r in rs if 0 <= r < len(defT)]
    if len(set(used_n_pair)) < len(used_n_pair): continue
    for rt in itertools.product((0, 1), repeat=len(defT)):                # 1 = use n as own piece (if not paired)
        pieces = []   # (m or None, n or None)
        for i, r in enumerate(rs):
            if r == -1: continue
            pieces.append((defS[i], defT[r] if r < len(defT) else None))
        for k, u in enumerate(rt):
            if u and k not in used_n_pair: pieces.append((None, defT[k]))
        ms = [p[0] for p in pieces if p[0] is not None]; ns = [p[1] for p in pieces if p[1] is not None]
        if not indep(ms) or not indep(ns): continue
        ok = True
        for a, (ma, na) in enumerate(pieces):
            for b, (mb, nb) in enumerate(pieces):
                if na is not None and mb is not None:
                    if int(na @ mb % 2) != (1 if a == b else 0): ok = False
        if not ok: continue
        # complete: random search for M with given columns/dual rows
        for trial in range(400):
            M = np.zeros((w, w), np.uint8); fixed_cols = {}; fixed_rows = {}
            for j, (m, n) in enumerate(pieces):
                if m is not None: fixed_cols[j] = m
                if n is not None: fixed_rows[j] = n
            for j in range(w):
                M[:, j] = fixed_cols[j] if j in fixed_cols else np.array([rng.randint(0, 1) for _ in range(w)])
            # enforce dual rows: for j in fixed_rows we need (M^-1)[j,:] = n_j  <=>  n_j . M[:, i] = delta_ij ; repair free columns
            Mi = inv2(M)
            if Mi is None: continue
            if all((Mi[j] == n).all() for j, n in fixed_rows.items()):
                cost = sum(rk(np.nonzero((Wc @ Mi[j]) % 2)[0], np.nonzero((M[:, j] @ Ub) % 2)[0]) for j in range(w))
                if best is None or cost < best[0]: best = (cost, len(pieces)); print('cost', cost, 'using', len(pieces), 'deficient roles', flush=True)
                break
print('best', best)
