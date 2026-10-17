import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V, nondegenerate, closure, dim
HYP = g.HYP
exec(open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/f2lib.py').read())
P, T = g.P, g.T
def name(u): return ('P' if g.kind[u] == 'P' else 'T') + ''.join('%x' % i for i in g.supp[u])
def show(fs, label):
    Wv = span([vv[x] for q in fs for x in q]); NW = N(Wv)
    pi = {vv[fs[0][0]] ^ vv[x] for x in fs[0][1:]}
    hyps = set()
    for a, b, c in itertools.combinations(list(Wv - {0}), 3):
        S = frozenset(span([a, b, c]))
        if len(S) == 8 and not pi <= S: hyps.add(S)
    print(label, 'Q =', sorted(name(u) for u in bits(NW)))
    for S in hyps:
        lin = sorted(name(lineof[x]) for x in S if x in lineof)
        L = N(S) & ~NW
        print('  V', lin, '\n     layer(%d)' % bin(L).count('1'), sorted(name(u) for u in bits(L)))
h = 0
star = [(P(a, b), P(c, d), T(h, a, b), T(h, c, d)) for (a, b), (c, d) in (((1, 2), (3, 4)), ((1, 3), (2, 4)), ((1, 4), (2, 3)))]
show(star, 'STAR (0;1234)')
A, B_, C = (0, 1), (2, 3), (4, 5)
trans = [(A[i], B_[j], C[k]) for i in range(2) for j in range(2) for k in range(2)]
f0 = tuple(T(*x) for x in trans if (sum(1 for z in x if z in (1, 3, 5)) % 2) == 0)
f1 = tuple(T(*x) for x in trans if (sum(1 for z in x if z in (1, 3, 5)) % 2) == 1)
show([f0, f1], 'OCTET (01|23|45)')
