"""8-bank scalar model of the B_K template (research/e8-early-reset-kernel/bit_global.py: small()).
Rows z[2p] = X_p, z[2p+1] = Y_p.  local(p, F): Y_p += X_p ; local(p, R): X_p -= Y_p ;
bridge(d, s, c): X_d += c X_s, Y_s -= c Y_d ; exchange: (X_j, Y_j) -> (Y_j, -X_j).
Question: keep the nine locals of the shipped recipe, put bridges ONLY at the start (all pairs at level -1) and at
the end (all at level 8), and still compose to the identity.  Then no bridge sits on an idle stretch (no split)."""
import itertools, numpy as np, sys
K = 4
def I8(): return np.eye(2 * K, dtype=np.int64)
def op_local(p, rev):
    M = I8()
    if rev: M[2 * p, 2 * p + 1] = -1          # X_p -= Y_p
    else: M[2 * p + 1, 2 * p] = 1             # Y_p += X_p
    return M
def op_bridge(d, s, c):
    M = I8(); M[2 * d, 2 * s] += c; M[2 * s + 1, 2 * d + 1] -= c
    return M
def op_exchange():
    M = np.zeros((2 * K, 2 * K), dtype=np.int64)
    for j in range(K):
        M[2 * j, 2 * j + 1] = 1; M[2 * j + 1, 2 * j] = -1
    return M
def compose(ops):          # ops applied in order; state z -> M z (row ops act as left multiplication)
    T = I8()
    for M in ops: T = M @ T
    return T
shipped_locals = [(0, False), (0, True), (0, False), (1, True), (1, False), (2, True), (2, False), (3, True), (3, False)]
# sanity: shipped recipe = identity
def shipped():
    ops = [op_local(0, False)]
    for j in range(K):
        ops.append(op_local(j, True))
        if j < K - 1: ops.append(op_bridge(j, j + 1, 1))
        ops.append(op_local(j, False))
        if j < K - 1: ops.append(op_bridge(j, j + 1, -1))
    for j in reversed(range(K - 1)): ops.append(op_bridge(j + 1, j, 1))
    ops.append(op_exchange())
    return compose(ops)
assert (shipped() == I8()).all(), shipped()
Mloc = compose([op_local(p, r) for p, r in shipped_locals])
E = op_exchange()
bridges = [(d, s, c) for d in range(K) for s in range(K) if d != s for c in (1, -1)]
# search B_end . Mloc . B_start = E^-1 with short bridge words on each side (meet in the middle on B_start side)
Einv = np.round(np.linalg.inv(E)).astype(np.int64)
maxlen = int(sys.argv[1]) if len(sys.argv) > 1 else 3
def words(n):
    for L in range(n + 1):
        for w in itertools.product(range(len(bridges)), repeat=L):
            yield w
def mat(w):
    return compose([op_bridge(*bridges[i]) for i in w])
# B_end = Einv . B_start^-1 . Mloc^-1 must be a bridge word: tabulate end words
endtab = {}
for w in words(maxlen):
    endtab.setdefault(mat(w).tobytes(), w)
Mi = np.round(np.linalg.inv(Mloc)).astype(np.int64)
found = 0
for w in words(maxlen):
    Bs = mat(w); Bsi = np.round(np.linalg.inv(Bs)).astype(np.int64)
    need = Einv @ Mi @ Bsi
    if need.tobytes() in endtab:
        found += 1
        print('start', [bridges[i] for i in w], 'end', [bridges[i] for i in endtab[need.tobytes()]])
        if found >= 5: break
print('solutions found (up to 5):', found, 'with words up to length', maxlen)
