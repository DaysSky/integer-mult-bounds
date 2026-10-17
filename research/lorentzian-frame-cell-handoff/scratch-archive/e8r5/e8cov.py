"""E8 4-covers of R(t) by rank-5 flats (D5 = A3-perp x3 + A5 = Z-perp, Z = t x A2), for all targets t.
Saves covers.pkl: {t: [(X1, X2, X3, Z), ...]} (frame masks) plus A3 list."""
import sys, itertools, collections, pickle, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; HYP = e8.HYP; bits = e8.bits
pc = lambda m: bin(m).count('1')
def pm(m):
    r = e8.FULL
    for s in bits(m): r &= HYP[s]
    return r
t0 = time.time()
A3 = set(); Zs = collections.defaultdict(set)
for t in range(V):
    for a, b in itertools.combinations([x for x in range(V) if x != t], 2):
        F, r = e8.closure((1 << t) | (1 << a) | (1 << b))
        if r != 3: continue
        if pc(F) == 6: A3.add(F)
        elif pc(F) == 4:
            # t must be the A1 factor: t _|_ the other 3 lines
            o = [x for x in bits(F) if x != t]
            if all(e8.GI[t][x] == 0 for x in o): Zs[t].add(F)
A3 = sorted(A3); print('A3s', len(A3), 'Z per line', len(Zs[0]), time.time() - t0, flush=True)
A3of = collections.defaultdict(list)
for X in A3:
    for s in bits(X): A3of[s].append(X)
covers = {}
for t in range(V):
    R = HYP[t] & ~(1 << t)
    Xs = A3of[t]; P = {X: pm(X) & R for X in Xs}
    Zp = {Z: pm(Z) & R for Z in Zs[t]}
    out = []
    for i, X1 in enumerate(Xs):
        for j in range(i + 1, len(Xs)):
            X2 = Xs[j]
            if X1 & X2 != 1 << t: continue
            U12 = P[X1] | P[X2]
            for k in range(j + 1, len(Xs)):
                X3 = Xs[k]
                if X3 & X1 != 1 << t or X3 & X2 != 1 << t: continue
                rem = R & ~(U12 | P[X3])
                for Z, PZ in Zp.items():
                    if rem & ~PZ == 0: out.append((X1, X2, X3, Z))
    covers[t] = out
    if t < 2: print('t', t, 'covers', len(out), time.time() - t0, flush=True)
print('covers per line', collections.Counter(len(v) for v in covers.values()), flush=True)
pickle.dump(dict(A3=A3, covers=covers), open('covers.pkl', 'wb'))
