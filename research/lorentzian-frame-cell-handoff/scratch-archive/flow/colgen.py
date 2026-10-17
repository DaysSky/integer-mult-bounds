"""Max fractional undirected multicommodity flow by column generation (paths), with certified dual bound."""
import numpy as np, time
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.csgraph import dijkstra
from motif import topology

def max_flow_cg(c, rho, iters=500, tol=1e-7, verbose=True):
    nV, edges = topology(c)
    G = len(c.gates); W = len(c.wires); E = len(edges)
    ea = np.array([a for a, b, w in edges]); eb = np.array([b for a, b, w in edges])
    # adjacency: map (u,v) -> list of edge ids; for dijkstra use min weight per vertex pair (parallel edges)
    src = np.array([G + 2 * k for k in range(W)]); dst = np.array([G + 2 * rho[k] + 1 for k in range(W)])
    paths = []  # (commodity, edge ids)
    y = np.zeros(E); z = np.zeros(W)
    best_dual = float('inf'); val = 0.0
    for it in range(iters):
        # pricing with lengths y (choose cheapest parallel edge)
        wts = y + 1e-12
        order = np.lexsort((wts, np.minimum(ea, eb), np.maximum(ea, eb)))
        key = np.minimum(ea, eb) * nV + np.maximum(ea, eb)
        ks = key[order]; first = np.ones(len(ks), dtype=bool); first[1:] = ks[1:] != ks[:-1]
        sel = order[first]
        M = coo_matrix((wts[sel], (ea[sel], eb[sel])), shape=(nV, nV)).tocsr()
        pairmin = {int(key[e]): int(e) for e in sel}
        dist, pred = dijkstra(M, directed=False, indices=src, return_predecessors=True)
        # dual bound: scale y so that every commodity distance >= 1 ... valid upper bound = sum y / min_w dist_w (if y>0)
        d = dist[np.arange(W), dst]
        if np.all(d > 0) and y.sum() > 0:
            best_dual = min(best_dual, y.sum() / d.min())
        added = 0
        for k in range(W):
            if d[k] < 1 - z[k] - tol or not paths:
                # reconstruct
                v = dst[k]; ep = []
                while v != src[k]:
                    u = pred[k, v]
                    ep.append(pairmin[int(min(u, v) * nV + max(u, v))]); v = u
                paths.append((k, ep)); added += 1
        if added == 0 and it > 0:
            break
        # master LP
        P = len(paths)
        rows, cols = [], []
        for j, (k, ep) in enumerate(paths):
            rows.extend(ep); cols.extend([j] * len(ep))
        Ae = coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(E, P))
        Ac = coo_matrix((np.ones(P), ([k for k, ep in paths], list(range(P)))), shape=(W, P))
        from scipy.sparse import vstack
        A = vstack([Ae, Ac]).tocsr()
        b = np.concatenate([np.ones(E), np.ones(W)])
        res = linprog(-np.ones(P), A_ub=A, b_ub=b, bounds=(0, None), method='highs')
        val = -res.fun
        duals = -res.ineqlin.marginals
        y = np.maximum(duals[:E], 0); z = np.maximum(duals[E:], 0)
        if verbose and (it % 5 == 0):
            print('  it', it, 'paths', P, 'primal', round(val, 6), 'dual bound', round(best_dual, 6) if best_dual < 1e18 else None, flush=True)
    return val, best_dual, W, E, y
