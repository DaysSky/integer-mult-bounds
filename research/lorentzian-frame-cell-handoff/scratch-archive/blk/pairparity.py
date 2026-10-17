# Pair-parity filter: Z = e0 + sum_stars K14(hub;F4) + sum_singles K14(hub; endpoints) + sum_punctT K3(triple) (mod 2)
# must be a K_{2,2,2} (one lone frame).  Enumerate P sides (exhaustive generator) and the 280 punctured-triple splits.
import itertools, pickle, sys
X = 10
pack6 = [(0, 1, 2, 3), (0, 4, 5, 6), (0, 7, 8, 9), (1, 4, 7, X), (2, 5, 8, X), (3, 6, 9, X)]
E = lambda b: [frozenset(e) for e in itertools.combinations(sorted(b), 2)]
tl = lambda h, e: frozenset((h,) + tuple(e))
used = set(e for b in pack6 for e in E(b))
left = [frozenset(e) for e in itertools.combinations(range(11), 2) if frozenset(e) not in used]
c2 = []
for F4 in itertools.combinations(range(11), 4):
    p, q, r, s = F4
    ms = [(frozenset((p, q)), frozenset((r, s))), (frozenset((p, r)), frozenset((q, s))), (frozenset((p, s)), frozenset((q, r)))]
    for m1, m2 in itertools.combinations(ms, 2):
        es = list(m1) + list(m2)
        if all(e in left for e in es): c2.append((F4, tuple(es)))
def is_k222(Zs):
    if len(Zs) != 12: return None
    pts = sorted(set(p for e in Zs for p in e))
    if len(pts) != 6: return None
    allp = set(frozenset(e) for e in itertools.combinations(pts, 2))
    miss = allp - Zs
    if len(miss) != 3 or len(set(p for e in miss for p in e)) != 6: return None
    return (tuple(pts), tuple(tuple(sorted(e)) for e in miss))
def splits(pts):
    pts = list(pts)
    if not pts: yield []; return
    a = pts[0]
    for b, c in itertools.combinations(pts[1:], 2):
        rest = [p for p in pts if p not in (a, b, c)]
        for s in splits(rest): yield [(a, b, c)] + s
out = []; LIMIT = int(sys.argv[1]); count = [0]
def xor(S, edges):
    for e in edges: S ^= {frozenset(e)}
    return S
def rec_hubs(i, usedT, hubsel):
    if len(out) >= LIMIT: return
    if i == 6: rec2(0, set(), usedT, [], hubsel); return
    F4 = pack6[i]
    for h in range(11):
        if h in F4: continue
        ts = [tl(h, e) for e in E(F4)]
        if any(t in usedT for t in ts): continue
        rec_hubs(i + 1, usedT | set(ts), hubsel + [h])
def rec2(start, usedE, usedT, chosen, hubsel):
    if len(out) >= LIMIT: return
    if len(chosen) == 3:
        rem = [e for e in left if e not in usedE]
        for e0 in rem: rec1([e for e in rem if e != e0], usedT, chosen, [], hubsel, e0)
        return
    for j in range(start, len(c2)):
        F4, es = c2[j]
        if any(e in usedE for e in es): continue
        for h in range(11):
            if h in F4: continue
            ts = [tl(h, e) for e in es]
            if any(t in usedT for t in ts): continue
            rec2(j + 1, usedE | set(es), usedT | set(ts), chosen + [(h, F4, es)], hubsel)
def rec1(rem, usedT, chosen, singles, hubsel, e0):
    if len(out) >= LIMIT: return
    if not rem:
        count[0] += 1
        Z = set([e0])
        for h, F4 in zip(hubsel, pack6): Z = xor(Z, [(h, v) for v in F4])
        for h, e1, e2 in singles: Z = xor(Z, [(h, v) for v in set(e1) | set(e2)])
        others = [p for p in range(11) if p not in e0]
        for sp in splits(others):
            ts = [frozenset(t) for t in sp]
            if any(t in usedT for t in ts): continue          # punctured T line must still be available
            Z2 = set(Z)
            for t in sp: Z2 = xor(Z2, list(itertools.combinations(t, 2)))
            k = is_k222(Z2)
            if k: out.append((list(hubsel), list(chosen), list(singles), [e0], sp, k)); return
        return
    e1 = rem[0]
    for e2 in rem[1:]:
        if e1 & e2: continue
        for h in range(11):
            if h in e1 or h in e2: continue
            t1, t2 = tl(h, e1), tl(h, e2)
            if t1 in usedT or t2 in usedT: continue
            rec1([e for e in rem if e not in (e1, e2)], usedT | {t1, t2}, chosen, singles + [(h, e1, e2)], hubsel, e0)
rec_hubs(0, set(), [])
print('P sides examined', count[0], '| passing pair-parity with one lone frame:', len(out))
for o in out[:5]: print('hubs', o[0], '| punctT', o[4], '| lone K222 on', o[5])
pickle.dump(out, open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/psides_pp.pkl', 'wb'))
