import pickle, numpy as np
from sympy.combinatorics import Permutation, PermutationGroup
gens = [Permutation(g) for g in pickle.load(open('eis_gens.pkl','rb'))]
G = PermutationGroup(gens)
elems = np.array([g.array_form for g in G.generate_schreier_sims()], dtype=np.int8)
print('elements', len(elems))
np.save('eis_elems.npy', elems)
def key(a): return a.tobytes()
idx = {key(e): i for i, e in enumerate(elems)}
def compose(a, b):  # (a*b)(x) = b(a(x)) sympy convention: apply a then b
    return b[a]
def inv(a):
    r = np.empty_like(a); r[a] = np.arange(len(a), dtype=a.dtype); return r
out = {}
def orbit_sizes(H):
    return sorted(len(o) for o in H.orbits())
for p in (2, 3, 5):
    S = G.sylow_subgroup(p)
    Sset = set(key(np.array(g.array_form, dtype=np.int8)) for g in S.generate_schreier_sims())
    Sg = [np.array(g.array_form, dtype=np.int8) for g in S.generators]
    Nel = [e for e in elems if all(key(compose(compose(inv(e), s), e)) in Sset for s in Sg)]
    N = PermutationGroup([Permutation(list(map(int, e))) for e in Nel[:60]] + list(S.generators))
    print('syl%d' % p, S.order(), orbit_sizes(S), '| normalizer', len(Nel), N.order(), orbit_sizes(N), flush=True)
    out['syl%d' % p] = [list(map(int, g.array_form)) for g in S.generators]
    out['nsyl%d' % p] = [list(map(int, e)) for e in Nel]
St = G.stabilizer(0)
print('stab(line)', St.order(), orbit_sizes(St))
pickle.dump(out, open('subgroups.pkl', 'wb'))
