"""Maximum edge-disjoint K4 packing of K11 (star-D4 blocks need all 6 P lines of a 4-set), then hubs h (not in F4)
so that the star T-lines T(h|F4) are pairwise disjoint.  Exact small search."""
import itertools, sys
pts = range(11)
quads = list(itertools.combinations(pts, 4))
best = []
def edges(q): return set(itertools.combinations(q, 2))
def rec(start, used, chosen):
    global best
    if len(chosen) > len(best): best = list(chosen); print('packing', len(best), best, flush=True)
    if len(best) >= 8: return True
    # bound: remaining edges / 6
    if len(chosen) + (55 - len(used)) // 6 <= len(best): return False
    for i in range(start, len(quads)):
        q = quads[i]; e = edges(q)
        if e & used: continue
        chosen.append(q)
        if rec(i + 1, used | e, chosen): return True
        chosen.pop()
    return False
rec(0, set(), [])
print('max packing found', len(best))
# hubs
def tl(h, q): return {tuple(sorted((h,) + p)) for p in itertools.combinations(q, 2)}
sol = None
def hrec(k, used, hubs):
    global sol
    if k == len(best): sol = list(hubs); return True
    q = best[k]
    for h in pts:
        if h in q: continue
        t = tl(h, q)
        if t & used: continue
        hubs.append(h)
        if hrec(k + 1, used | t, hubs): return True
        hubs.pop()
    return False
hrec(0, set(), [])
print('hubs', sol)
import pickle; pickle.dump((best, sol), open('k4pack.pkl', 'wb'))
