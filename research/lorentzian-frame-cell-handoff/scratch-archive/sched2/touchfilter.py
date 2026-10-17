import json
rows = json.load(open('splitlist_K4.json'))
K, s = 4, 9
def ok(sq, sp):
    tau = {r: 99 for r in range(K)}; lam = {r: -1 for r in range(K)}
    for j, p in enumerate(sq):
        tau[p] = min(tau[p], j); lam[p] = max(lam[p], j + 1)
    for b in range(1, s):
        for r in (sq[b - 1], sq[b]):
            if sq[b - 1] != sq[b]: tau[r] = min(tau[r], b); lam[r] = max(lam[r], b)
    for (r, b) in sp: tau[r] = min(tau[r], b); lam[r] = max(lam[r], b)
    ts = sorted(tau.values()); ls = sorted(lam.values(), reverse=True)
    return all(ts[k] <= 2 * k for k in range(K)) and all(s - ls[k] <= 2 * k for k in range(K))
keep = []
for v, sq, L in rows:
    L2 = [o for o in L if ok(sq, [tuple(e) for e in o[1]])]
    if L2: keep.append((max(o[0] for o in L2), sq, L2))
keep.sort(reverse=True)
json.dump(keep, open('splitlist_K4_touch.json', 'w'))
print(len(rows), '->', len(keep), 'sequences after touch-time filter')
for v, sq, L in keep[:20]: print('%+.3f%%' % v, sq, len(L), L[0][1], L[0][2])
