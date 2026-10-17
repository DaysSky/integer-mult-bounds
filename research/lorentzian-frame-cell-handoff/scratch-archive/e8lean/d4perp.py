"""E8: all D4 subsystems; for each plane Q through t (orthogonal pair / A2): how many D4s lie in Q-perp; for the
4-section all-proper covers of R(t), whether R(t) can be covered by D4s inside the 4 sections (needed for a
cells->quads->sections design), and the minimum number of D4s per section needed."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; GI = e8.GI
pc = lambda m: bin(m).count('1')
# all D4s: closures of 4 mutually orthogonal lines with 12 lines
D4 = set()
orth = [set(e8.ORTH[a]) for a in range(V)]
for a in range(V):
    for b in orth[a]:
        if b <= a: continue
        for c in orth[a] & orth[b]:
            if c <= b: continue
            for d in orth[a] & orth[b] & orth[c]:
                if d <= c: continue
                F, r = e8.closure((1 << a) | (1 << b) | (1 << c) | (1 << d))
                if pc(F) == 12: D4.add(F)
D4 = sorted(D4)
print('D4 subsystems:', len(D4))
def perpmask(F):
    m = (1 << V) - 1
    for s in e8.bits(F): m &= e8.HYP[s]
    return m
t = 0; R = e8.HYP[t]
planes = set()
for u in range(V):
    if u != t: planes.add(e8.closure((1 << t) | (1 << u))[0])
inside = {}
for Q in planes:
    P = perpmask(Q)
    inside[Q] = [W for W in D4 if W & ~P == 0]
print('D4s inside a section, by plane size:', collections.Counter((pc(Q), len(v)) for Q, v in inside.items()))
# can each section's lines be covered by its inner D4s?  (union of inner D4 lines vs section lines)
for Q in list(planes)[:0]: pass
cov = collections.Counter()
for Q, ws in inside.items():
    m = 0
    for W in ws: m |= W
    cov[(pc(Q), pc(perpmask(Q) & R), pc(m))] += 1
print('(plane size, section lines, lines covered by inner D4s):', dict(cov))
