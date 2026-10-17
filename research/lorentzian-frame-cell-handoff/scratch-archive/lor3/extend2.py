"""Rigid greedy extension (abstract real vectors) of an odd-or-zero system in w^perp of I_{n,1}.
Classes of L = w^perp cap Z^{n,1} mod 2L <-> parity vectors (x mod 2, y mod 2) with even total parity.
Bbar(a,b) = <a,b> mod 2 via representatives.  New class c may join with any real vector r in w^perp orthogonal to all
existing r_b with Bbar(c,b) = 0 (same class included), nonisotropic."""
import json, sys, itertools, math, numpy as np
d = json.load(open(sys.argv[1])); n = d['n']; t = d['t']; blocks = d['blocks']
eta = np.diag([1.0]*n + [-1.0]); w = np.array([1.0]*n + [float(t)])
def expand(orbit):
    cmb, y = orbit
    vecs = set()
    perms = [set(itertools.permutations(c)) for c in cmb]
    for pr in itertools.product(*perms):
        x = tuple(a for blk in pr for a in blk); vecs.add(x + (y,))
    return vecs
V = []
for orb in d['orbits']:
    vs = expand(orb)
    seen = set()
    for v in vs:
        if tuple(-a for a in v) in seen: continue
        seen.add(v); V.append(np.array(v, dtype=float))
V = np.array(V); print('base lines', len(V), flush=True)
ip = lambda A, B: A @ eta @ B.T
par = lambda v: tuple(int(round(a)) % 2 for a in v)
# class representatives: parity vectors with even total; representative integer vector in L with that parity
reps = {}
rng_vals = range(-2, 3)
for x in itertools.product((0, 1), repeat=n):
    for y in (0, 1):
        if (sum(x) + y) % 2: continue
        reps[tuple(x) + (y,)] = None
# find integer representatives: solve small search: choose y in {y0, y0+2, ...}, x = parity + 2k with sum x = t*y
def find_rep(p):
    xp = np.array(p[:n]); yp = p[n]
    for y in range(yp - 4, yp + 5, 2):
        need = t*y - xp.sum()   # must be even; adjust by adding +-2 to coordinates
        if need % 2: continue
        x = xp.copy().astype(int); k = need // 2
        i = 0
        while k != 0:
            x[i % n] += 2 if k > 0 else -2; k += -1 if k > 0 else 1; i += 1
        return np.array(list(x) + [y], dtype=float)
for p in reps: reps[p] = find_rep(p)
classes = [p for p in reps if any(p)]
R = list(V); S = [par(v) for v in V]
assert len(set(S)) == len(S), 'base has repeated classes'
# basis of w^perp (in metric eta): vectors u with u . eta . w = 0
Wp = np.linalg.svd((eta @ w)[None, :])[2][1:]
def bbar(p, q): return int(round(reps[p] @ eta @ reps[q])) % 2
def bbar_vec(p, r): return int(round(reps[p] @ eta @ r)) % 2   # r integer for base lines; for added lines use class rep
cls_of = {}
for i, s in enumerate(S): cls_of[i] = s
added = 0; changed = True
while changed:
    changed = False
    inS = set(S)
    for c in classes:
        if c in inS: continue
        cons = [R[i] for i in range(len(R)) if S[i] == c or bbar(c, S[i]) == 0]
        A = np.array(cons) @ eta @ Wp.T          # constraints on coefficients in w^perp basis
        if len(A) == 0: continue
        s = np.linalg.svd(A, compute_uv=False)
        rk = (s > 1e-9 * s[0]).sum()
        if rk >= Wp.shape[0]: continue
        null = np.linalg.svd(A)[2][rk:]
        for k in range(10):
            coef = null[k] if k < len(null) else np.random.default_rng(k).standard_normal(len(null)) @ null
            r = coef @ Wp
            if abs(r @ eta @ r) > 1e-6 * (r @ r):
                R.append(r); S.append(c); added += 1; changed = True; inS.add(c)
                break
print('final', len(S), 'added', added)
json.dump(dict(eta=eta.tolist(), R=[list(map(float, r)) for r in R], S=[list(s) for s in S]), open(sys.argv[1].replace('best', 'ext'), 'w'))
