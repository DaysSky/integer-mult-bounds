"""Cell bottleneck screen with SOURCE frames from partition P1 and TOP frames from P2 = g(P1), g random in W(E8).
Counts cells C (source side) for which no first node N ⊋ C lies in a C-containing top-D6 of every doubly forced target
(=> C needs a 3rd register in any middle, under the frame-architecture assumptions)."""
import sys, json, random, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
import numpy as np
V = e8.V; pc = lambda m: bin(m).count('1')
L = np.array(e8.LINES, dtype=np.int64); n2 = int(L[0] @ L[0])
line_of = {}
for i, x in enumerate(L): line_of[tuple(x)] = i; line_of[tuple(-x)] = i
def refl_perm(r):
    return [line_of[tuple(L[i] - 2 * (L[i] @ L[r]) * L[r] // n2)] for i in range(V)]
RP = [refl_perm(r) for r in range(V)]
def perp(mask):
    m = (1 << V) - 1
    for s in e8.bits(mask): m &= e8.HYP[s]
    return m
cells1 = [int(h, 16) for h in json.load(open('../sec4/r420cells.json'))['planes']]
def maskperm(m, p):
    r = 0
    for s in e8.bits(m): r |= 1 << p[s]
    return r
CL = {}
def closure(m):
    if m not in CL: CL[m] = e8.closure(m)[0]
    return CL[m]
def bad(src_cells, top_cells):
    cells_of = {s: [C for C in src_cells if C >> s & 1] for s in range(V)}
    D6s_of = {t: [perp(C) for C in top_cells if C >> t & 1] for t in range(V)}
    nb = 0; Tsz = collections.Counter()
    for C in src_cells:
        s, e = e8.bits(C); T = []
        for t in range(V):
            if not (e8.HYP[t] >> s & 1 and e8.HYP[t] >> e & 1): continue
            Ds = D6s_of[t]
            rs = [(D, c) for D in Ds for c in cells_of[s] if c & ~D == 0]
            re = [(D, c) for D in Ds for c in cells_of[e] if c & ~D == 0]
            if rs and re and all(c == C for _, c in rs) and all(c == C for _, c in re):
                T.append([D for D, _ in rs])
        Tsz[len(T)] += 1
        if not T: continue
        ok = False
        for x in range(V):
            if C >> x & 1: continue
            N = closure(C | (1 << x))
            if all(any(N & ~D == 0 for D in Ds) for Ds in T): ok = True; break
        if not ok: nb += 1
    return nb, dict(Tsz)
print('identity:', bad(cells1, cells1), flush=True)
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 20):
    p = list(range(V))
    for _ in range(random.randint(1, 40)):
        q = RP[random.randrange(V)]; p = [q[i] for i in p]
    cells2 = [maskperm(C, p) for C in cells1]
    same = len(set(cells2) & set(cells1))
    print('trial', trial, 'shared cells', same, 'bad, |T| histogram:', bad(cells1, cells2), flush=True)
