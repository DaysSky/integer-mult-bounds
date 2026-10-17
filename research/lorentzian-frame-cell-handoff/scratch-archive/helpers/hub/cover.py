"""#595 section D cover numbers for candidate units (source end; the terminal end is the same geometry for these
self-dual line systems).

For a source s, the readers T(s) are the lines orthogonal to s.  A register crossing from <u_s> into <u_s, w> serves the
readers in w^perp, a 'hyperplane section' of T(s).  The cover number is the least number of proper sections covering T(s).
  * lower bound 2 <=> rank_Q T(s) = h - 1 (then no single proper section covers T(s));            exact
  * upper bound 2 <=> two subsets of T(s), each of rank <= h - 2, with union T(s) (certificate);   exact check
    (the witnesses are found by sampling hyperplanes through h - 2 random readers plus structured functionals;
    a found pair is re-checked exactly)
  * the best single section found (a LOWER bound on the largest section; sampled, not exhaustive)
#595's single-cut floors (d_geometry.single_cut_bounds): sink-only R >= (c - 1) v - floor(v / leftover), strict
R >= max(c v - 2 v, 0).  With cover number 2 the strict floor is 0 and the sink-only floor is at most v.
Control: E8 bit (cover number 3, best pair union 52 of 63: #595 D1).
Usage: python cover.py REPO_ROOT unit[,unit...] [samples] [--json out]     unit in {E8, T<h>, L<n>}
"""
import itertools
import sys

import numpy as np

sys.dont_write_bytecode = True
import units as U                       # noqa: E402


def load(name):
    if name == 'E8':
        L = U.roots_E8(); G = U.gram_doubled(L); return L, G, [0]
    if name.startswith('T'):
        L, G, _ = U.triple_family(int(name[1:])); return L, G, [0]
    if name.startswith('L'):
        n = int(name[1:])
        L, G, _ = U.lorentz_family(n)
        from math import comb
        return L, G, [0, comb(n, 3)]                # one triple-type and one pair-type source
    raise ValueError(name)


def sections_for(L, G, s, h, samples, rng):
    T = np.nonzero(G[s] == 0)[0]
    T = T[T != s]
    X = L[T].astype(float)
    rT = U.rank_q(L[T].tolist())
    secs = set()
    # structured functionals: coordinate patterns c with c . t = 0
    n = L.shape[1]
    cands = []
    for i in range(n):
        e = np.zeros(n); e[i] = 1; cands.append(e)
    for i, j in itertools.combinations(range(n), 2):
        for sg in (1, -1):
            e = np.zeros(n); e[i] = 1; e[j] = sg; cands.append(e)
    for i, j, k in itertools.combinations(range(n), 3):
        for sg in itertools.product((1, -1), repeat=2):
            e = np.zeros(n); e[i] = 1; e[j] = sg[0]; e[k] = sg[1]; cands.append(e)
    for i, j in itertools.combinations(range(n), 2):   # triple family: 1 off {i, j}, -2 on {i, j} (two-class sections)
        e = np.ones(n); e[i] = e[j] = -2; cands.append(e)
    for i in range(n - 1):
        for wgt in (1, 2, 3):
            e = np.ones(n); e[-1] = wgt; e[i] -= 1; cands.append(e)
            e = np.ones(n); e[-1] = wgt; e[i] += 1; cands.append(e)
    for c in cands:
        m = np.abs(X @ c) < 1e-9
        if 0 < m.sum() < len(T):
            secs.add(tuple(np.nonzero(m)[0]))
    # random hyperplanes of span(T) through h - 2 readers
    for _ in range(samples):
        idx = rng.choice(len(T), rT - 1, replace=False)
        M = X[idx]
        if np.linalg.matrix_rank(M) < rT - 1:
            continue
        # normal of the hyperplane inside span(T): project onto span(T) via SVD of X
        _, _, Vt = np.linalg.svd(np.vstack([M, np.zeros((0, n))]))
        null = Vt[rT - 1:]                      # functionals vanishing on M
        # choose a functional that does not vanish on all of T
        best = None
        for c in null:
            m = np.abs(X @ c) < 1e-7
            if m.sum() < len(T):
                best = m; break
        if best is not None:
            secs.add(tuple(np.nonzero(best)[0]))
    return T, rT, secs


def run(name, samples=20000, seed=1):
    L, G, srcs = load(name)
    h = U.rank_q(G.tolist())
    rng = np.random.default_rng(seed)
    out = []
    for s in srcs:
        T, rT, secs = sections_for(L, G, s, h, samples, rng)
        # exact check of every kept section: rank <= h - 2 (a proper section)
        secs = [S for S in secs if U.rank_q(L[T[list(S)]].tolist()) <= h - 2]
        masks = [sum(1 << int(k) for k in S) for S in secs]
        full = (1 << len(T)) - 1
        best1 = max(len(S) for S in secs)
        order = sorted(range(len(masks)), key=lambda i: -len(secs[i]))
        bestpair, cover2 = 0, None
        for a in range(len(order)):
            ma = masks[order[a]]
            for b in range(a, len(order)):
                u = bin(ma | masks[order[b]]).count('1')
                if u > bestpair:
                    bestpair = u
                    if u == len(T):
                        cover2 = (secs[order[a]], secs[order[b]])
                        break
            if cover2:
                break
        lb = 2 if rT == h - 1 else 1
        res = dict(unit=name, source=int(s), readers=len(T), rank_readers=rT, h=h, cover_lb=lb,
                   cover_ub=2 if cover2 else None, best_section_found=best1, best_pair_union=bestpair,
                   n_sections=len(secs))
        if not cover2:                           # look for a 3-cover among the largest sections
            top = order[:400]
            found = None
            for a in range(len(top)):
                for b in range(a, len(top)):
                    rest = full & ~(masks[top[a]] | masks[top[b]])
                    for c in range(len(masks)):
                        if rest & ~masks[c] == 0:
                            found = (secs[top[a]], secs[top[b]], secs[c]); break
                    if found:
                        break
                if found:
                    break
            if found:
                assert set().union(*found) == set(range(len(T)))
                res['cover_ub'] = 3
                res['cover3_sizes'] = tuple(len(x) for x in found)
        if cover2:
            A, B = cover2
            assert U.rank_q(L[T[list(A)]].tolist()) <= h - 2 and U.rank_q(L[T[list(B)]].tolist()) <= h - 2
            assert set(A) | set(B) == set(range(len(T)))
            res['cover2_sizes'] = (len(A), len(B))
        print(res, flush=True)
        out.append(res)
    return out


if __name__ == '__main__':
    import json
    allres = []
    for u in sys.argv[2].split(','):
        allres += run(u, int(sys.argv[3]) if len(sys.argv) > 3 else 20000)
    if '--json' in sys.argv:
        json.dump(allres, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1, default=str)
