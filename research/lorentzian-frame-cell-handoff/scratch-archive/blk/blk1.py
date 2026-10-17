# Layer anatomy of a star block and an octet block.
import sys, pickle, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V, nondegenerate, closure, dim
HYP = g.HYP
exec(open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/f2lib.py').read())
def anat(name, fs):
    Wv = span([vv[x] for q in fs for x in q]); Wd = len(Wv).bit_length() - 1
    wl = [lineof[x] for x in Wv if x in lineof]
    NW = N(Wv)
    pi = {vv[fs[0][0]] ^ vv[x] for x in fs[0][1:]}
    for q in fs: assert {vv[q[0]] ^ vv[x] for x in q[1:]} == pi
    hyps = set()
    gens = list(Wv - {0})
    for a, b, c in itertools.combinations(gens, 3):
        S = frozenset(span([a, b, c]))
        if len(S) == 8: hyps.add(S)
    print(name, '| frames', len(fs), '| dim W', Wd, '| W lines', len(wl), '| N(W)', bin(NW).count('1'),
          '| real pm(W)', bin(pm(sum(1 << x for x in wl))).count('1'), '| hyperplanes', len(hyps))
    tot = 0
    for S in sorted(hyps, key=lambda S: -len([x for x in S if x in lineof])):
        L = N(S) & ~NW
        lin = [lineof[x] for x in S if x in lineof]
        realF = pm(sum(1 << x for x in lin))
        cells = [(x, y) for q in fs for x, y in itertools.combinations(q, 2) if vv[x] in S and vv[y] in S]
        frame = any(set(vv[x] for x in q) <= S for q in fs)
        tot += bin(L).count('1')
        print('   V: lines %d %s cells %d frame %s | layer %d | outside real pm(V) %d | rank pm(V) %d nd %s | pi in V %s' % (
            len(lin), ''.join(sorted(g.kind[x] for x in lin)), len(cells), frame, bin(L).count('1'),
            bin(L & ~realF).count('1'), dim(realF), nondegenerate(realF), pi <= S))
    print('   layer total', tot)
P, T = g.P, g.T
h, F4 = 0, [1, 2, 3, 4]
star = []
for (p, q), (r, s) in (((1, 2), (3, 4)), ((1, 3), (2, 4)), ((1, 4), (2, 3))):
    star.append((P(p, q), P(r, s), T(h, p, q), T(h, r, s)))
anat('star(0;1234)', star)
A, B, C = (0, 1), (2, 3), (4, 5)
trans = [(A[i], B[j], C[k]) for i in range(2) for j in range(2) for k in range(2)]
f0 = tuple(T(*x) for x in trans if (sum(1 for z in x if z in (1, 3, 5)) % 2) == 0)
f1 = tuple(T(*x) for x in trans if (sum(1 for z in x if z in (1, 3, 5)) % 2) == 1)
anat('octet(01|23|45)', [f0, f1])
