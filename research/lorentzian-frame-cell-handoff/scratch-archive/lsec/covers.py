"""Valid 4-section covers of R(t) for each H55 line rep: sections = planes through t (pairs, A2s); section of plane Q
for t = R(t) ∩ Q-perp; cover R(t); every private set nonempty and non-spanning (proper).  Saves covers.pkl."""
from lcommon import *
pairs, a2 = planes_all()
print('pairs', len(pairs), 'A2 planes', len(a2), 'A2 sizes', collections.Counter(pc(F) for F in a2), 'line reps', line_reps, [g.kind[s] + str(g.supp[s]) for s in line_reps], flush=True)
res = {}
for t in line_reps:
    R = HYP[t]
    thr = [F for F in pairs if F >> t & 1] + [F for F in a2 if F >> t & 1]
    sec = {F: perpmask(F) & R for F in thr}
    by_line = collections.defaultdict(list)
    for F, m in sec.items():
        for s in bits(m): by_line[s].append(F)
    mx = max(pc(m) for m in sec.values())
    covers = []
    def rec(unc, k, chosen):
        if unc == 0:
            if len(chosen) == 4: covers.append(tuple(sorted(chosen)))
            return
        if k == 0 or pc(unc) > mx * k: return
        s = (unc & -unc).bit_length() - 1
        for F in by_line[s]:
            if F in chosen: continue
            rec(unc & ~sec[F], k - 1, chosen + [F])
    rec(R, 4, [])
    covers = sorted(set(covers))
    good = []; types = collections.Counter()
    for cv in covers:
        ok = True; key = []
        for F in cv:
            oth = 0
            for H in cv:
                if H != F: oth |= sec[H]
            P = sec[F] & ~oth
            if not P or g.dim(P) == g.dim(sec[F]): ok = False; break
            key.append((pc(F), pc(sec[F]), pc(P)))
        if ok: good.append(cv); types[tuple(sorted(key))] += 1
    res[t] = good
    print('rep', g.kind[t], g.supp[t], 'readers', pc(R), 'planes through t', len(thr), '4-covers', len(covers), 'all-proper', len(good), flush=True)
    for k, n in types.most_common(6): print('     ', n, k)
pickle.dump(res, open('covers.pkl', 'wb'))
