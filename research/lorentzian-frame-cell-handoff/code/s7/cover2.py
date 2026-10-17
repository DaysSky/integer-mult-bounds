from i11geo import *
import itertools
G = g.G
def R(t): return [u for u in range(V) if u != t and G[t,u] == 0]
for t in (g.T(0,1,2), g.P(0,1)):
    Rt = R(t); Rs = set(Rt)
    # 2-covers by line-sections {t,a}^perp, a in R(t)
    best = []
    for a, b in itertools.combinations(Rt, 2):
        miss = [u for u in Rt if u not in (a, b) and G[a,u] != 0 and G[b,u] != 0]
        # a and b themselves: a in R(t); is a in lines({t,b}^perp)? needs a perp b
        if not miss: best.append((a, b, G[a,b]))
    print(g.kind[t], g.supp[t], '|R|', len(Rt), '2-covers by line sections:', len(best))
    from collections import Counter
    print('  types', Counter((g.kind[a], g.kind[b], int(G[a,b])) for a,b,_ in best).most_common(10))
    if best:
        a, b, _ = best[0]; print('  e.g.', g.kind[a], g.supp[a], g.kind[b], g.supp[b])
    # 3-covers count (min uncovered by best 2)
    mm = min(sum(1 for u in Rt if G[a,u] != 0 and G[b,u] != 0 and u not in (a,b)) for a, b in itertools.combinations(Rt, 2))
    print('  min uncovered by 2 line-sections', mm)
