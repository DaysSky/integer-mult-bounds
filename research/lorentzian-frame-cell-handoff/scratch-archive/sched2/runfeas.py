import json, sys, time
from feas import feasible
K = 4; s = 9
res = json.load(open('seqprice_K4.json'))
def ok(sq):
    for direction in (sq, sq[::-1]):
        first = {}
        for j, p in enumerate(direction): first.setdefault(p, j)
        for k, b in enumerate(sorted(first.values())):
            if b > 2 * k + 1: return False
    return True
E = int(sys.argv[1]); top = int(sys.argv[2])
cands = []
for pct, sl, seqs in res:
    if pct <= 0: break
    for q in seqs:
        if ok(q): cands.append((pct, sl, q))
print(len(cands), 'candidate sequences with positive price', flush=True)
for pct, sl, q in cands[:top]:
    t = time.time()
    f = feasible(q, E)
    print('%+.2f%%' % pct, sl, q, 'FEASIBLE' if f else 'none(E=%d)' % E, f[0][0] if f else '', f[0][1] if f else '',
          '%.0fs' % (time.time() - t), flush=True)
