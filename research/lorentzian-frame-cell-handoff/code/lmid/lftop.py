"""Frame top with routable totals + private correction, for a frame-cell system.
Target t with its own good frame Phi_t = {t, e1, e2, e3} (system cov[t], first 3 mates) has the exact F2 identity
    R(t) = sum_i tot(S_i) + x_e1 + x_e2 + x_e3,     S_i = {t, e_i}-perp      (verified here line by line)
Split tot(S_i) = tot_r(S_i) + tot_u(S_i) (routable = some system cell of u inside S_i).  tot_r(S_i) is user-independent
(shared by t and e_i).  Correction c(t) = sum_i tot_u(S_i) + mates (as an F2 set).  Reports |c(t)| and whether c(t)
fits routably in ONE extra plane section of t (or with the in-chain cell read), i.e. the 4-section frame top.
usage: lftop.py SYSTEM.json"""
import sys, os, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ['GRP'] = '11'
from lbase import V, bits, HYP, closure, perp, g
pc = lambda m: bin(m).count('1')
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
co = {s: [C for C in cells if C >> s & 1] for s in range(V)}
def routable(S):
    m = 0
    for u in bits(S):
        if any(C & ~S == 0 for C in co[u]): m |= 1 << u
    return m
RT = {}
def rt(S):
    if S not in RT: RT[S] = routable(S)
    return RT[S]
stats = collections.Counter(); csz = []; fit = collections.Counter(); bad = []
for t in range(V):
    mates = [e for e in bits(cov[t]) if e != t]
    assert len(mates) == 3, (t, mates)
    secs = [HYP[t] & HYP[e] for e in mates]
    par = 0
    for S in secs: par ^= S
    for e in mates: par ^= 1 << e
    assert par == HYP[t], ('parity identity fails', t)
    c = 0
    for e in mates: c ^= 1 << e
    for S in secs: c ^= S & ~rt(S)
    csz.append(pc(c))
    # one extra plane section of t covering c routably, optionally with an in-chain cell read inside it
    ok = False; okcell = False
    for e in range(V):
        if e == t: continue
        Q = closure((1 << t) | (1 << e)); S = perp(Q)
        r = rt(S)
        if c & ~r == 0: ok = True; break
        miss = c & ~r
        if pc(miss) <= 2:
            for C in cells:
                if C & ~S == 0 and C & ~HYP[t] == 0 and miss & ~C == 0: okcell = True; break
    fit['one section' if ok else ('section + cell read' if okcell else 'NO')] += 1
    if not ok and not okcell: bad.append(t)
print('parity identity verified for all', V, 'targets')
print('|c(t)| distribution:', sorted(collections.Counter(csz).items()))
print('correction fits:', dict(fit), 'bad targets', bad[:20])
