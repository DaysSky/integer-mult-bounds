import json, sys, time
from feas import feasible
res = json.load(open('seqprice_K4.json'))
def ok(sq):
    for direction in (sq, sq[::-1]):
        first = {}
        for j, p in enumerate(direction): first.setdefault(p, j)
        for k, b in enumerate(sorted(first.values())):
            if b > 2 * k + 1: return False
    return True
def no3(sq):
    return not any(sq[i] == sq[i + 1] == sq[i + 2] for i in range(len(sq) - 2))
E = int(sys.argv[1])
cands = [(pct, sl, q) for pct, sl, seqs in res if pct > 0 for q in seqs if ok(q) and no3(q)]
print(len(cands), 'candidates', flush=True)
for pct, sl, q in cands:
    t = time.time()
    f = feasible(q, E, limit_states=50000)
    print('%+.2f%%' % pct, sl, q, 'FEASIBLE' if f else 'none(E=%d)' % E, f[0][0] if f else '', f[0][1] if f else '',
          '%.0fs' % (time.time() - t), flush=True)
