"""Local search over the top choice with the real builder as the objective (R of build_a3g.py, PIECES=paar).
Proposals: for a random target, an alternative defect-1 triple ranked by its marginal content cost (a3_left2-style
demands, shared demands free).  A proposal is accepted if the rebuilt R does not increase (ties accepted with
probability ACC).  usage: ls_tops.py CHOICE.pkl OUT.pkl ITERS [SEED]"""
import sys, os, pickle, random, subprocess, collections, re, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lmid'))
from lw import V, g, bits
from fastcl import fclosure
HYP = g.HYP; pc = lambda m: bin(m).count('1')
CH, OUT, IT = sys.argv[1], sys.argv[2], int(sys.argv[3])
SEED = int(sys.argv[4]) if len(sys.argv) > 4 else 1
ACC = float(os.environ.get('ACC', '0.3'))
rng = random.Random(SEED)
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
PM = {}
def pm(m):
    r = PM.get(m)
    if r is None:
        r = (1 << V) - 1
        for s in bits(m): r &= HYP[s]
        PM[m] = r
    return r
def a3type(tr):
    a, b, c, d = tr
    tris = [Q for Q in (a, b, c) if pc(Q) == 3]; pairs = [Q for Q in (a, b, c) if pc(Q) == 2]
    if len(tris) == 2 and len(pairs) == 1 and d >= 0 and pairs[0] >> d & 1:
        A3 = fclosure(tris[0] | tris[1])
        if pc(A3) == 6 and A3 >> d & 1: return (A3, tris[0], tris[1], pairs[0], d)
    return None
def demands_of(tr):
    v = a3type(tr)
    if v is None: return [(pm(Q), pm(Q)) for Q in tr[:3]]
    A3, Q1, Q2, P, d = v; Bp = pm(A3)
    return [(Bp, Bp), (pm(Q1), pm(Q1) & ~Bp), (pm(Q2), pm(Q2) & ~Bp), (pm(P), pm(P) & ~Bp)]
TR = pickle.load(open('a3_triples.pkl', 'rb'))
choice = pickle.load(open(CH, 'rb'))
TMP = OUT + '.tmp.pkl'
def evalR(ch):
    pickle.dump(ch, open(TMP, 'wb'))
    env = dict(os.environ, PIECES='paar', HOP='0', MP='0', EVAL='1')
    out = subprocess.run([sys.executable, 'build_a3g.py', TMP, '/dev/null'], capture_output=True, text=True, env=env).stdout
    m = re.search(r"'R': (\d+)", out)
    return int(m.group(1)) if m else 10 ** 9
curR = evalR(choice); best = (curR, dict(choice))
log('start R', curR)
for it in range(IT):
    use = collections.Counter()
    for t, tr in choice.items():
        for K in demands_of(tr): use[K] += 1
    t = rng.randrange(V)
    own = demands_of(choice[t])
    def marg(tr):
        return sum(pc(K[1]) for K in demands_of(tr) if use[K] - (1 if K in own else 0) == 0)
    cands = sorted(range(len(TR[t])), key=lambda k: marg(TR[t][k]))[:8]
    k = rng.choice(cands)
    if tuple(TR[t][k]) == tuple(choice[t]): continue
    new = dict(choice); new[t] = TR[t][k]
    R = evalR(new)
    if R < curR or (R == curR and rng.random() < ACC):
        choice, curR = new, R
        if R < best[0]: best = (R, dict(new)); pickle.dump(new, open(OUT, 'wb'))
        log('it', it, 'accept t', t, 'R', R, '| best', best[0])
log('done best R', best[0])
pickle.dump(best[1], open(OUT, 'wb'))
