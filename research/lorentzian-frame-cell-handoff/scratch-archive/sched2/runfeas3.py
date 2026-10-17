import json, sys, time, itertools
from feas import feasible
res = json.load(open('seqprice_K4.json'))
def ok2(sq):
    for direction in (sq, sq[::-1]):
        first = {}
        for j, p in enumerate(direction): first.setdefault(p, j)
        for k, b in enumerate(sorted(first.values())):
            if k >= 1 and b > 2 * k: return False
    return True
def no3(sq): return not any(sq[i] == sq[i + 1] == sq[i + 2] for i in range(len(sq) - 2))
E = int(sys.argv[1]); alt = sys.argv[2] == 'alt'
cands = [(pct, sl, q) for pct, sl, seqs in res if pct > 0 for q in seqs if ok2(q) and no3(q)]
print(len(cands), 'candidates', flush=True)
pats = [tuple(bool(i % 2) for i in range(9))] if alt else None
for pct, sl, q in cands:
    t = time.time()
    f = feasible(q, E, pats=pats, limit_states=400000)
    print('%+.2f%%' % pct, sl, q, 'FEASIBLE' if f else 'none(E=%d,%s)' % (E, sys.argv[2]), f[0][0] if f else '',
          f[0][1] if f else '', '%.0fs' % (time.time() - t), flush=True)
