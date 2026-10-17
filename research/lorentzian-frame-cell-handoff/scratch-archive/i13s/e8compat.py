import sys, itertools, numpy as np, collections
sys.path.insert(0, '../e8cal'); import e8
V = e8.V; orth = (e8.GI == 0); np.fill_diagonal(orth, False)
fr = []
for a in range(V):
    for b, c, d in itertools.combinations([x for x in range(a + 1, V) if orth[a, x]], 3):
        if orth[b, c] and orth[b, d] and orth[c, d]: fr.append((a, b, c, d))
def good(q):
    for t in q:
        es = [e for e in q if e != t]
        for l in range(V):
            if l in q or not orth[t, l]: continue
            if sum(orth[l, e] for e in es) % 2 == 0: return False
    return True
F = np.array([q for q in fr if good(q)]); nf = len(F)
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
S = np.zeros((nf, V), dtype=np.uint8)
for k, (a, b) in enumerate(pairs):
    o = [c for c in range(4) if c not in (a, b)]
    E = orth[F[:, a]] & orth[F[:, b]] & ~orth[F[:, o[0]]] & ~orth[F[:, o[1]]]
    S |= (E.astype(np.uint8) << k)
member = np.zeros((nf, V), dtype=bool); member[np.arange(nf)[:, None], F] = True
i = 0; s = S[i]
x = s[F[:, 0]] ^ s[F[:, 1]] ^ s[F[:, 2]] ^ s[F[:, 3]]
y = S[:, F[i, 0]] ^ S[:, F[i, 1]] ^ S[:, F[i, 2]] ^ S[:, F[i, 3]]
disj = ~member[:, F[i]].any(1)
ok = (x == 0) & (y == 0) & disj
print('E8 good frames', nf, 'disjoint from f0', disj.sum(), 'compatible', ok.sum(), 'fraction %.3f' % (ok.sum() / disj.sum()))
