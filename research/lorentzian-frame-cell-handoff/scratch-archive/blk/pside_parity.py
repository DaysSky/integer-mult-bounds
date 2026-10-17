# Enumerate P sides (6 complete stars on the unique packing + 3 two-frame stars + 3 single PPTT frames + 1 punctured
# P edge e0) with hubs and no T conflicts; keep those whose mod-4 odd-lambda set O has exactly 6 points (one lone frame).
import itertools, pickle, sys, random
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
out = []; LIMIT = int(sys.argv[1])
def odd_set(starhubs, singles_h, e0):
    par = [0] * 11
    for h in starhubs: par[h] ^= 1
    for h in singles_h: par[h] ^= 1
    return frozenset([p for p in e0 if par[p]] + [p for p in range(11) if p not in e0 and not par[p]])
def rec_hubs(i, usedT, hubsel):
    if len(out) >= LIMIT: return
    if i == 6:
        rec2(0, set(), usedT, [], hubsel); return
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
        for e0 in rem:
            rec1([e for e in rem if e != e0], usedT, chosen, [], hubsel, e0)
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
        O = odd_set(hubsel, [h for h, _, _ in singles], e0)
        if len(O) == 6: out.append((list(hubsel), list(chosen), list(singles), [e0], O))
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
print('P sides with |O| = 6 found:', len(out))
for o in out[:5]: print(o[0], [x[0] for x in o[1]], [(h, sorted(a), sorted(b)) for h, a, b in o[2]], sorted(o[3][0]), sorted(o[4]))
pickle.dump(out, open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/psides_O6.pkl', 'wb'))
