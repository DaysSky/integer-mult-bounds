# Exhaustive P-side feasibility for B = 25 configurations.  P lines lie only in PPTT (star) frames.
# Given complete stars on a K4 packing K (|K| = s3), count the maximum number of 2-frame stars (4-cycle F4 using two
# matchings of leftover edges) that are edge-disjoint, then singles; T-line conflicts (T(h,e)) are checked with hubs.
import itertools, sys
X = 10
pack6 = [(0, 1, 2, 3), (0, 4, 5, 6), (0, 7, 8, 9), (1, 4, 7, X), (2, 5, 8, X), (3, 6, 9, X)]
E = lambda b: [frozenset(e) for e in itertools.combinations(sorted(b), 2)]
def tl(h, e): return frozenset((h,) + tuple(e))
def solve(K, s2_needed, s1_needed, pP):
    used = set(e for b in K for e in E(b))
    left = [frozenset(e) for e in itertools.combinations(range(11), 2) if frozenset(e) not in used]
    # 2-frame star candidates: (F4, two matchings) with 4 leftover edges; hub h not in F4
    c2 = []
    for F4 in itertools.combinations(range(11), 4):
        p, q, r, s = F4
        ms = [(frozenset((p, q)), frozenset((r, s))), (frozenset((p, r)), frozenset((q, s))), (frozenset((p, s)), frozenset((q, r)))]
        for m1, m2 in itertools.combinations(ms, 2):
            es = list(m1) + list(m2)
            if all(e in left for e in es): c2.append((F4, tuple(es)))
    c1 = [(e1, e2) for e1, e2 in itertools.combinations(left, 2) if not e1 & e2]
    # complete-star hubs: choose hubs for K; then 2-stars, singles; all T lines distinct; exactly pP edges left over
    best = [None]
    Klist = list(K)
    def hubs_K(i, usedT, hubsel):
        if i == len(Klist):
            pick2(0, set(), usedT, [], hubsel); return best[0] is not None
        F4 = Klist[i]
        for h in range(11):
            if h in F4: continue
            ts = [tl(h, e) for e in E(F4)]
            if any(t in usedT for t in ts): continue
            if hubs_K(i + 1, usedT | set(ts), hubsel + [h]): return True
        return False
    def pick2(start, usedE, usedT, chosen, hubsel):
        if best[0] is not None: return
        if len(chosen) == s2_needed:
            pick1(set(usedE), usedT, chosen, [], hubsel); return
        for j in range(start, len(c2)):
            F4, es = c2[j]
            if any(e in usedE for e in es): continue
            for h in range(11):
                if h in F4: continue
                ts = [tl(h, e) for e in es]
                if any(t in usedT for t in ts): continue
                pick2(j + 1, usedE | set(es), usedT | set(ts), chosen + [(h, F4, es)], hubsel)
                if best[0] is not None: return
    def pick1(usedE, usedT, chosen, singles, hubsel, punct=()):
        if best[0] is not None: return
        rem = [e for e in left if e not in usedE and e not in punct]
        if not rem:
            if len(singles) == s1_needed and len(punct) == pP: best[0] = (hubsel, chosen, singles, list(punct))
            return
        e1 = rem[0]
        if len(punct) < pP:                                   # e1 punctured
            pick1(usedE, usedT, chosen, singles, hubsel, punct + (e1,))
            if best[0] is not None: return
        if len(singles) < s1_needed:                          # e1 in a single frame with some disjoint e2 and hub h
            for e2 in rem[1:]:
                if e1 & e2: continue
                for h in range(11):
                    if h in e1 or h in e2: continue
                    t1, t2 = tl(h, e1), tl(h, e2)
                    if t1 in usedT or t2 in usedT: continue
                    pick1(usedE | {e1, e2}, usedT | {t1, t2}, chosen, singles + [(h, e1, e2)], hubsel, punct)
                    if best[0] is not None: return
    hubs_K(0, set(), [])
    return best[0], len(c2)

import pickle
allsol = []
r, n2 = solve(pack6, 3, 3, 1)
print('s3=6 s2=3 s1=3 pP=1:', 'FEASIBLE' if r else 'INFEASIBLE', r)
pickle.dump(r, open('pside633.pkl', 'wb'))
