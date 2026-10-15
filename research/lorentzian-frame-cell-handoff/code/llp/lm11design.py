"""Combined M11 top: T lines use the S(4,5,11) triangle design (lttri_design_z11.json); each P line P(E) uses one
parallel class {B1,B2,B3} of the derived affine plane at E (one of the 4 triangle nodes over E, chosen
Z11-equivariantly by CLASS index): nodes A2(Bi) + P(E) (i = 1..3) and {P(E), T(B1), T(B2), T(B3)}.  Checks every cover
geometrically and writes a one-cover-per-line pool (r8covers format) + sel json for lr8mkdet.py.
usage: lm11design.py CLASS out.pkl"""
import sys, json, pickle, itertools, collections
from lgeo import *
CL = int(sys.argv[1]); out = sys.argv[2]
sol = [tuple(tuple(T) for T in node) for node in json.load(open('lttri_design_z11.json'))]
def Ln(k, pts): return IDX[(k, tuple(sorted(pts)))]
def frame(lines):
    """pp-closure of the first three (rank-3) lines; all given lines must lie in it"""
    m = 0
    for s in lines[:3]: m |= 1 << s
    assert rank(m) == 3, lines
    F = pp(m)
    for s in lines: assert F >> s & 1, ('line outside frame', lines)
    return F
covers = {}
byT = collections.defaultdict(list); byE = collections.defaultdict(list)
for node in sol:
    E = tuple(x for x in range(11) if x not in set(itertools.chain(*node)))
    byE[E].append(node)
    F = frame([Ln('T', T) for T in node])
    for T in node: byT[T].append(F)
for T, Fs in byT.items(): covers[Ln('T', T)] = tuple(sorted(Fs))
rot = lambda pts, k: tuple(sorted((x + k) % 11 for x in pts))
# equivariant class choice: for each E orbit under Z11 pick the CL-th node (sorted) at the orbit representative
done = {}
for E in sorted(byE):
    if E in done: continue
    nodes = sorted(byE[E]); base = nodes[CL % len(nodes)]
    for k in range(11):
        Ek = rot(E, k)
        if Ek in done: continue
        nk = tuple(sorted(rot(T, k) for T in base))
        assert nk in [tuple(sorted(x)) for x in byE[Ek]], 'design not Z11 invariant?'
        done[Ek] = nk
for E, node in done.items():
    t = Ln('P', E)
    Fs = [frame([t] + [Ln('P', p) for p in itertools.combinations(B, 2)]) for B in node]
    Fs.append(frame([t] + [Ln('T', B) for B in node]))
    covers[t] = tuple(sorted(Fs))
ok = 0
for t, c in covers.items():
    U = 0
    for F in c: assert F >> t & 1; U |= pm(F)
    assert U & HYP[t] == HYP[t], ('not a cover', t)
    ok += 1
print('all %d covers verified' % ok)
users = collections.Counter(F for c in covers.values() for F in c)
print('nodes', len(users), 'users per node', sorted(collections.Counter(users.values()).items()))
pickle.dump({t: [c] for t, c in covers.items()}, open(out, 'wb'))
reps = [0, 1, 2, 3, 4, 55, 56, 57, 58, 59, 60, 61, 62, 65, 66, 67, 68, 69, 74, 75]
json.dump({str(r): 0 for r in reps}, open(out.replace('.pkl', '_sel.json'), 'w'))
