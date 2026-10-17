"""Residual isometries for E1: PR #443's frame-zero record (the carrier skeleton's data/eleven/residual-isometries.json,
copied unchanged) plus a record for the entrance frame 186 of helper 248 (register 470): entrance basis [33, 77] (frame
186 is spanned by the orthogonal roots 33 and 77), residual basis the first (lexicographic) six live roots that are
mutually orthogonal and orthogonal to both, and the Gauss-Jordan reduction of (rows / 2) to the identity in the
port-route vocabulary (swap / scale / add with exact dyadic scalars).  Deterministic.
usage: make_iso_e1.py WORD.json.gz SKELETON_ISOMETRIES.json OUT.json"""
import gzip, json, sys
from fractions import Fraction

word, skel, out = sys.argv[1:4]
w = json.load(gzip.open(word, 'rt'))
L = w['lines']; dot = lambda a, b: sum(x * y for x, y in zip(a, b))
F, EB = 186, [33, 77]
assert sorted(w['frames'][F]) == EB and w['start'][470] == F and dot(L[33], L[77]) == 0
base = json.load(open(skel))
assert len(base) == 1 and base[0]['frame'] == 0


def frame_of(base):
    def rec(cur, cands):
        if len(cur) == 8: return cur
        for k, c in enumerate(cands):
            r = rec(cur + [c], [d for d in cands[k + 1:] if dot(L[c], L[d]) == 0])
            if r: return r
        return None
    return rec(list(base), [i for i in range(len(L)) if i not in base and all(dot(L[i], L[b]) == 0 for b in base)])


basis = frame_of(EB)
M = [L[i] for i in basis]
Qm = [[Fraction(x, 2) for x in row] for row in M]
ops = []
for c in range(8):
    p = next(r for r in range(c, 8) if Qm[r][c])
    if p != c:
        Qm[c], Qm[p] = Qm[p], Qm[c]; ops.append(['swap', c, p, None])
    if Qm[c][c] != 1:
        s = 1 / Qm[c][c]; Qm[c] = [s * x for x in Qm[c]]; ops.append(['scale', c, None, str(s)])
    for i in range(8):
        if i != c and Qm[i][c]:
            s = -Qm[i][c]; Qm[i] = [x + s * y for x, y in zip(Qm[i], Qm[c])]; ops.append(['add', i, c, str(s)])
assert Qm == [[Fraction(int(i == j)) for j in range(8)] for i in range(8)]
rec = dict(frame=F, entrance_rank=2, denominator=2, entrance_basis=EB, residual_basis=basis[2:],
           orthogonal_rows_numerator=M, gaussian_reduction=ops)
json.dump(base + [rec], open(out, 'w'), separators=(',', ':'))
print('residual isometries: frame 0 (identity) and frame %d: basis %s, %d route factors (%s)' % (
    F, basis, len(ops), ', '.join('%d %s' % (sum(o[0] == k for o in ops), k) for k in ('swap', 'scale', 'add'))))
