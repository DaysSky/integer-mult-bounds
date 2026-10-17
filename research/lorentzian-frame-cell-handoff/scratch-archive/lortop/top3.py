"""Top-level per-target register cost (same model as helpers/topcover.py for E8): target t's readers R(t) are covered
by three sections R(t) cap u^perp (u a line).  Section shared by the lines of the plane <t,u>: 2 if u perp t, 3 if
<t,u> = +-1 (A2), more if the plane holds more lines (counted exactly).  The target's own chain passes the needer
section F (cost 2/s), the other two are dedicated deliveries (cost (k+1)/k).  Union covers and parity covers
(every reader in an odd number of sections) are both enumerated exhaustively over unordered line triples."""
import json, sys, itertools, collections
import numpy as np
def run(path, reps=None):
    d = json.load(open(path)); eta = np.array(d['eta']); R = np.array(d['R']); v = len(R)
    G = R @ eta @ R.T
    Z = np.abs(G) < 1e-9
    rank = lambda A: np.linalg.matrix_rank(A, tol=1e-8)
    # orbit representatives: one per (norm, #readers) class unless given
    if reps is None:
        seen = {}; reps = []
        for t in range(v):
            k = (round(G[t, t], 4), int(Z[t].sum()))
            if k not in seen: seen[k] = t; reps.append(t)
    out = []
    for t in reps:
        rd = [s for s in range(v) if s != t and Z[t, s]]
        idx = {s: i for i, s in enumerate(rd)}; full = (1 << len(rd)) - 1
        M = {}; share = {}
        for u in range(v):
            if u == t: continue
            m = 0
            for s in rd:
                if s != u and Z[u, s]: m |= 1 << idx[s]
            M[u] = m
            # lines in the plane <t,u>
            P = np.vstack([G[t], G[u]])          # functional coordinates (works with radical too)
            r2 = rank(P)
            share[u] = sum(1 for z in range(v) if rank(np.vstack([P, G[z]])) == r2)
        us = sorted(M)
        best = {'union': None, 'parity': None}
        hist = {'union': collections.Counter(), 'parity': collections.Counter()}
        cost = lambda s: 2.0 / s
        ded = lambda k: (k + 1.0) / k
        for a, b, c in itertools.combinations(us, 3):
            ma, mb, mc = M[a], M[b], M[c]
            for kind, ok in (('union', (ma | mb | mc) == full), ('parity', (ma ^ mb ^ mc) == full)):
                if not ok: continue
                trip = (share[a], share[b], share[c])
                cst = min(cost(trip[i]) + sum(ded(trip[j]) for j in range(3) if j != i) for i in range(3))
                hist[kind][tuple(sorted(trip))] += 1
                if best[kind] is None or cst < best[kind][0]: best[kind] = (round(cst, 4), tuple(sorted(trip)))
        out.append(dict(t=t, norm=round(float(G[t, t]), 4), readers=len(rd), best=best,
                        hist={k: {str(kk): vv for kk, vv in h.items()} for k, h in hist.items()}))
        print(path, json.dumps(out[-1]), flush=True)
for p in sys.argv[1:]:
    run(p)
