"""Local search: good-frame partition (4 punctured lines) minimising odd (E-set, frame) intersections.
Move: remove k random frames (+ the punctured lines), re-cover their lines exactly by good frames (DFS, random order),
accept if the odd count does not increase (or with SA probability)."""
import sys, pickle, random, time, math, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
good = pickle.load(open('good4.pkl', 'rb')); n = len(good); F = np.array(good)
orth = (G == 0); np.fill_diagonal(orth, False)
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
S = np.zeros((n, V), dtype=np.uint8)
for k, (a, b) in enumerate(pairs):
    o = [c for c in range(4) if c not in (a, b)]
    E = orth[F[:, a]] & orth[F[:, b]] & ~orth[F[:, o[0]]] & ~orth[F[:, o[1]]]
    S |= (E.astype(np.uint8) << k)
POP = np.array([bin(i).count('1') for i in range(64)])
def w(i, j):
    a = S[i, F[j, 0]] ^ S[i, F[j, 1]] ^ S[i, F[j, 2]] ^ S[i, F[j, 3]]
    b = S[j, F[i, 0]] ^ S[j, F[i, 1]] ^ S[j, F[i, 2]] ^ S[j, F[i, 3]]
    return POP[a] + POP[b]
def cost_of(fr): return sum(w(a, b) for x, a in enumerate(fr) for b in fr[x + 1:])
byline = [[] for _ in range(V)]
for i, q in enumerate(good):
    for x in q: byline[x].append(i)
idx = {tuple(sorted(q)): i for i, q in enumerate(good)}
sol, pun = pickle.load(open(sys.argv[1], 'rb'))
fr = [idx[tuple(sorted(q))] for q in sol]; pun = list(pun)
seed = int(sys.argv[2]); T = float(sys.argv[3]); rng = random.Random(seed)
cur = cost_of(fr); best = (cur, list(fr), list(pun)); t0 = time.time(); it = 0
print('start odd', cur, flush=True)
def recover(lines, rest, budget_p):
    """exact cover of 'lines' by good frames inside 'lines', allowing budget_p punctures (P parity kept by caller)"""
    lines = set(lines); out = []; pu = []
    def rec():
        if not lines: return True
        x = min(lines, key=lambda u: len(byline[u]))
        cands = [i for i in byline[x] if all(y in lines for y in good[i])]
        rng.shuffle(cands)
        for i in cands[:6]:
            for y in good[i]: lines.discard(y)
            out.append(i)
            if rec(): return True
            out.pop()
            for y in good[i]: lines.add(y)
        if len(pu) < budget_p:
            lines.discard(x); pu.append(x)
            if rec(): return True
            pu.pop(); lines.add(x)
        return False
    ok = rec()
    return (out, pu) if ok else None
temp = 2.0
while time.time() - t0 < T:
    it += 1
    k = rng.choice([2, 3, 3, 4])
    rem = rng.sample(range(len(fr)), k)
    lines = [y for r in rem for y in good[fr[r]]] + pun
    rest = [fr[r] for r in range(len(fr)) if r not in rem]
    res = recover(lines, rest, len(pun))
    if res is None: continue
    nf, np_ = res
    # P-parity: punctured P count must keep total live P even
    if sum(1 for u in np_ if g.kind[u] == 'P') % 2 != 1: continue
    new = rest + nf
    delta = sum(w(a, b) for a in nf for b in rest) + sum(w(a, b) for x, a in enumerate(nf) for b in nf[x + 1:]) \
        - sum(w(fr[r], b) for r in rem for b in rest) - sum(w(fr[r], fr[s]) for x, r in enumerate(rem) for s in rem[x + 1:])
    if delta <= 0 or rng.random() < math.exp(-delta / temp):
        fr, pun, cur = new, np_, cur + delta
        if cur < best[0]:
            best = (cur, list(fr), list(pun)); print('it', it, 'odd', cur, round(time.time() - t0), flush=True)
            pickle.dump(([good[i] for i in fr], pun), open('minodd_%d.pkl' % seed, 'wb'))
    temp = max(0.3, 2.0 * (1 - (time.time() - t0) / T))
print('best odd', best[0], 'its', it)
