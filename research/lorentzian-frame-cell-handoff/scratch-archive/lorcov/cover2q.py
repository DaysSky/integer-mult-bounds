"""Exact char-0 cover test via the kernel K of quadratic forms on span R(s) vanishing on the readers R(s).
cover 1 iff rank R(s) <= h-2.  K = 0 => cover >= 3 (certified by full column rank mod a prime).
K != 0: exact rational basis of K; a member of rank 2 that is indefinite (or rank 1) factors over R into l1*l2
=> cover 2.  For dim K = 1 this is decisive; for dim K > 1 we additionally search K's members of rank <= 2 by
exact elimination on pencils of basis pairs and report 'K>1 undecided' if none found."""
import json, sys, itertools, collections
import numpy as np
from fractions import Fraction as Fr

def rank_mod(M, p):
    M = [[x % p for x in row] for row in M]; r = 0; ncol = len(M[0]) if M else 0
    for c in range(ncol):
        piv = next((i for i in range(r, len(M)) if M[i][c]), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]; inv = pow(M[r][c], p - 2, p); M[r] = [x * inv % p for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r

def nullspace_Q(M, ncol):
    A = [[Fr(x) for x in row] for row in M]; piv = []; r = 0
    for c in range(ncol):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]; inv = 1 / A[r][c]; A[r] = [x * inv for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]; A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv.append(c); r += 1
    free = [c for c in range(ncol) if c not in piv]; basis = []
    for fc in free:
        v = [Fr(0)] * ncol; v[fc] = Fr(1)
        for i, pc in enumerate(piv): v[pc] = -A[i][fc]
        basis.append(v)
    return basis

def qrank(rows):
    return np.linalg.matrix_rank(np.array(rows, dtype=float), tol=1e-8) if len(rows) else 0

def sym_from(vec, mons, d):
    S = np.zeros((d, d))
    for (i, j), c in zip(mons, vec):
        if i == j: S[i, i] = float(c)
        else: S[i, j] = S[j, i] = float(c) / 2
    return S

def analyse(path):
    d0 = json.load(open(path)); eta = np.array(d0['eta']); R = np.array(d0['R'])
    Gf = R @ eta @ R.T; v = len(R)
    INTG = np.allclose(Gf, np.rint(Gf))
    G = np.rint(Gf).astype(np.int64) if INTG else Gf
    ZZ = np.abs(Gf) < 1e-9
    # labels modulo the radical: for degenerate forms use Gram rank as window; work in coordinates of R itself
    h = np.linalg.matrix_rank(Gf, tol=1e-8)
    Ri = np.rint(R * 6).astype(np.int64)
    out = collections.Counter(); kd = collections.Counter(); per = collections.defaultdict(collections.Counter)
    for s in range(v):
        rd = [t for t in range(v) if t != s and ZZ[s, t]]
        # rank in the label space = rank of the Gram block of readers against all lines (kills the radical)
        Yg = G[rd]                                        # reader -> functional on lines
        d = qrank(Yg)
        key = (round(float(Gf[s, s]), 4), len(rd))
        if d <= h - 2:
            out[1] += 1; per[key][1] += 1; continue
        # coordinates: choose d columns of Yg (i.e. d lines) on which readers are independent
        cols = []
        for j in range(v):
            if qrank(Yg[:, cols + [j]]) > len(cols): cols.append(j)
            if len(cols) == d: break
        mons = list(itertools.combinations_with_replacement(range(d), 2))
        if INTG:
            Yc = [[int(Yg[i, j]) for j in cols] for i in range(len(rd))]
            M = [[y[i] * y[j] for (i, j) in mons] for y in Yc]
            rk = rank_mod(M, 1000003); kdim = len(mons) - rk
            if kdim > 0:
                rk2 = rank_mod(M, 998244353); kdim = len(mons) - max(rk, rk2)
        else:
            Yc = [[float(Yg[i, j]) for j in cols] for i in range(len(rd))]
            M = [[y[i] * y[j] for (i, j) in mons] for y in Yc]
            kdim = len(mons) - qrank(M)
            if kdim > 0:
                out['float K>0 (unresolved)'] += 1; per[key]['float K>0'] += 1; kd[kdim] += 1; continue
        kd[kdim] += 1
        if kdim == 0:
            out['>=3'] += 1; per[key]['>=3'] += 1; continue
        K = nullspace_Q(M, len(mons))
        res = 'K>1 undecided'
        mats = [sym_from(k, mons, d) for k in K]
        for S in mats:
            ev = np.linalg.eigvalsh(S); nz = ev[np.abs(ev) > 1e-9]
            if len(nz) == 1 or (len(nz) == 2 and nz[0] * nz[1] < 0):
                res = 2; break
        if res != 2 and len(K) == 1:
            res = '>=3'
        if res != 2 and len(K) > 1:
            # pencils a*S1 + S2: rank <= 2 requires all 3x3 minors to vanish; scan exact roots of det of 3x3 minors
            for S1, S2 in itertools.combinations(mats, 2):
                for ii in itertools.combinations(range(d), 3):
                    A = S1[np.ix_(ii, ii)]; B = S2[np.ix_(ii, ii)]
                    # det(aA + B) cubic in a; roots
                    cs = np.polyfit(np.arange(4.0), [np.linalg.det(a * A + B) for a in range(4)], 3)
                    for a in np.roots(cs):
                        if abs(a.imag) > 1e-9: continue
                        S = a.real * S1 + S2; ev = np.linalg.eigvalsh(S); nz = ev[np.abs(ev) > 1e-7]
                        if len(nz) == 2 and nz[0] * nz[1] < 0:
                            res = 2; break
                    if res == 2: break
                    break   # one minor triple is enough to generate candidate a's
                if res == 2: break
        out[res] += 1; per[key][res] += 1
    print(path, 'v', v, 'h', h, 'dim K', dict(kd), 'cover', dict(out), flush=True)
    for k, c in sorted(per.items()):
        print('   source (norm %s, readers %d):' % k, dict(c), flush=True)

for p in sys.argv[1:]:
    analyse(p)
