"""Interval lemma (proven): if d pairs are untouched during g consecutive stages b1..b2-1 (no local on them, no
transform at boundaries b1+1..b2-1 involving them), then g - [b1 == 0] <= 2(K - d).  Proof: their rows are frozen,
Phi(b1) <= Phi_D + 2(K - d), Phi(b2) >= Phi_D, and Phi drops by exactly one per local except the first.
Filter the candidate (sequence, split) options with it."""
import json, sys
K, s = 4, 9
def stretches(sq, sp):
    out = []   # (pair, alpha, beta) in levels
    for r in range(K):
        actv = [j for j in range(s) if sq[j] == r]; lv = 0
        cuts = sorted(b for (q, b) in sp if q == r)
        for j in actv + [s]:
            if j > lv:
                pts = [lv] + [x for x in cuts if lv < x < j] + [j]
                out += [(r, pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
            lv = j + 1
    return out
def interval_ok(sq, sp):
    st = stretches(sq, sp)
    for b1 in range(s):
        for b2 in range(b1 + 1, s + 1):
            d = len({r for (r, a, b) in st if a <= b1 and b2 <= b})
            if (b2 - b1) - (1 if b1 == 0 else 0) > 2 * (K - d): return False
    return True
for fn in sys.argv[1:]:
    rows = json.load(open(fn))
    keep = []
    for row in rows:
        if len(row) == 3:      # (v, sq, L)
            v, sq, L = row
            L2 = [o for o in L if interval_ok(sq, [tuple(e) for e in o[1]])]
            if L2: keep.append((max(o[0] for o in L2), sq, L2))
        else:                  # (v, sq, sp, sl)
            v, sq, sp, sl = row
            if interval_ok(sq, [tuple(e) for e in sp]): keep.append(row)
    keep.sort(key=lambda r: -r[0])
    print(fn, len(rows), '->', len(keep), 'after interval lemma; best', keep[0][0] if keep else None, keep[0][1] if keep else '')
    json.dump(keep, open(fn.replace('.json', '_iv.json'), 'w'))
