"""Screen small-window units: v label lines (char-0 Gram), F2 decoder fitting orthogonality.
Exact F2 minrank by SAT (asymmetric allowed), lower bound from a max pairwise-non-orthogonal clique."""
import itertools, sys, time, math
import numpy as np
import networkx as nx
sys.path.insert(0, '../lor2/hub')
from minrank_sat import build
from pysat.solvers import Cadical153

def gauss_norm(v):
    # canonical representative of the line spanned by v (entries complex with int parts)
    for z in v:
        if z != 0:
            break
    # scale by unit so first nonzero has positive real part and nonneg imag (Gaussian units)
    for u in (1, -1, 1j, -1j):
        w = tuple(complex(u*a) for a in v)
        f = next(c for c in w if c != 0)
        if f.real > 0 and f.imag >= 0:
            return w
    raise ValueError

def dedupe_lines(vecs, form, field='real'):
    seen = {}
    for v in vecs:
        v = tuple(v)
        if all(a == 0 for a in v):
            continue
        g = None
        if field == 'real':
            g = math.gcd(*[int(a) for a in v])
            w = tuple(int(a)//g for a in v)
            f = next(a for a in w if a != 0)
            if f < 0: w = tuple(-a for a in w)
        else:
            w = gauss_norm(v)  # (no gcd reduction; caller gives primitive-ish)
        seen[w] = 1
    L = list(seen)
    M = np.array(form)
    out = []
    for w in L:
        a = np.array(w)
        n = a @ M @ a
        if abs(n) > 1e-9:
            out.append(w)
    return out

def gram(lines, form):
    A = np.array(lines)
    return A @ np.array(form) @ A.T

def screen(name, lines, form, cmax=None, tlimit=120, verbose=True):
    G = gram(lines, form)
    v = len(lines)
    h = np.linalg.matrix_rank(np.array(lines, dtype=complex))
    off = [(S, T) for S in range(v) for T in range(S+1, v) if abs(G[S, T]) > 1e-9]
    # clique of pairwise non-orthogonal lines
    Gr = nx.Graph(); Gr.add_nodes_from(range(v)); Gr.add_edges_from(off)
    cl, _ = nx.max_weight_clique(Gr, weight=None) if v <= 80 else (max(nx.find_cliques(Gr), key=len), None)
    deg = [sum(1 for T in range(v) if T != S and abs(G[S, T]) < 1e-9) for S in range(v)]
    res = dict(name=name, v=v, h=int(h), omega_nonorth=len(cl), orth_deg=(min(deg), max(deg)))
    lo = len(cl)
    best = None
    cmax = cmax or v
    for c in range(lo, cmax+1):
        f = build(v, off, c, False, cl if len(cl) == c else None)
        if c * h >= v:
            res['note'] = 'minrank >= %d (proxy x >= 1)' % c
            break
        s = Cadical153(bootstrap_with=f.cl)
        import threading
        tm = threading.Timer(tlimit, lambda: s.interrupt()); tm.start()
        r = s.solve_limited(expect_interrupt=True)
        tm.cancel()
        if r is True:
            best = c; break
        if r is None:
            res['note'] = 'c=%d timeout' % c
            break
    res['minrank'] = best
    res['x_proxy'] = (best * h / v) if best else None
    if verbose:
        print(res, flush=True)
    return res

if __name__ == '__main__':
    pass
