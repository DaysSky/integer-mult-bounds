"""Per-frame mate-correction system.  Frame {0,1,2,3}; D6 for each pair {a,b} with d-cell = the other pair.
User a of D6{a,b} receives correction m[a,(a,b)] ⊆ d-cell; symmetric D6s force m[a,.] == m[b,.].
Requirement: for each target t and each mate e: e lies in exactly one (odd) of m[t,(t,f)], f ∉ {t,e}.
Enumerate all choices of the set S of asymmetric D6s (size 0..6) and report the minimum |S| and all minimal S."""
import itertools
F = [0, 1, 2, 3]
pairs = [tuple(sorted(p)) for p in itertools.combinations(F, 2)]
dcell = {p: tuple(x for x in F if x not in p) for p in pairs}
def subsets(c): return [frozenset(s) for k in range(3) for s in itertools.combinations(c, k)]
def solvable(asym):
    # variables: for symmetric D6 one subset; for asymmetric, one subset per user
    keys = []
    for p in pairs:
        if p in asym: keys += [(p, p[0]), (p, p[1])]
        else: keys.append((p, None))
    doms = [subsets(dcell[k[0]]) for k in keys]
    for choice in itertools.product(*doms):
        m = {}
        for (p, u), s in zip(keys, choice):
            if u is None: m[(p, p[0])] = s; m[(p, p[1])] = s
            else: m[(p, u)] = s
        ok = True
        for t in F:
            for e in F:
                if e == t: continue
                cnt = sum(1 for f in F if f not in (t, e) and e in m[(tuple(sorted((t, f))), t)])
                if cnt % 2 != 1: ok = False; break
            if not ok: break
        if ok: return m
    return None
for k in range(7):
    sols = [S for S in itertools.combinations(pairs, k) if solvable(set(S))]
    if sols:
        print('minimum number of asymmetric D6s per frame:', k, '; minimal sets:', sols)
        print('example corrections:', {str(kk): sorted(v) for kk, v in solvable(set(sols[0])).items()})
        break
    print('k =', k, ': no solution')
