"""Stage 1: local search over E8 cover choices (one 4-cover per target) maximising the number of targets t that have a
potential host: an in-chain A3 X in t's cover and a co-user b in X whose cover also contains X, with a common part
A (excl_t | excl_b <= A <= (excl_t|flex_t) & (excl_b|flex_b)).  Saves e8covsel_<seed>.json {t: cover index}."""
import sys, random, pickle, json, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; HYP = e8.HYP; bits = e8.bits
def pm(m):
    r = e8.FULL
    for s in bits(m): r &= HYP[s]
    return r
seed = int(sys.argv[1]); ITERS = int(sys.argv[2]); random.seed(seed); t0 = time.time()
cov = pickle.load(open('covers.pkl', 'rb'))['covers']
PM = {}
def pmc(F):
    if F not in PM: PM[F] = pm(F)
    return PM[F]
INFO = {}
def info(t, ci):
    key = (t, ci)
    if key in INFO: return INFO[key]
    Xs, Z = cov[t][ci]; R = HYP[t] & ~(1 << t)
    sets = [pmc(Y) & R for Y in Xs] + [pmc(Z) & R]
    d = {}
    for i, X in enumerate(Xs):
        excl = sets[i]
        for j, S in enumerate(sets):
            if j != i: excl &= ~S
        d[X] = (excl, sets[i] & ~excl)
    INFO[key] = d; return d
choice = [random.randrange(len(cov[t])) for t in range(V)]
def hosted(t):
    dt = info(t, choice[t])
    for X, (et, ft) in dt.items():
        for b in bits(X):
            if b == t: continue
            db = info(b, choice[b])
            if X not in db: continue
            eb, fb = db[X]
            if (et | eb) & ~((et | ft) & (eb | fb)) == 0: return True
    return False
def score(): return sum(hosted(t) for t in range(V))
cur = score(); best = cur; bestc = list(choice)
print('init hosted', cur, flush=True)
import math
for it in range(ITERS):
    T = 1.5 * (0.02 / 1.5) ** (it / ITERS)
    un = [x for x in range(V) if not hosted(x)]
    if un and random.random() < 0.7:
        t0_ = random.choice(un)
        Xs = cov[t0_][choice[t0_]][0]
        t = random.choice([t0_] + [b for X in Xs for b in bits(X) if b != t0_])
    else:
        t = random.randrange(V)
    old = choice[t]
    choice[t] = random.randrange(len(cov[t]))
    new = score()
    if new >= cur or random.random() < math.exp((new - cur) / T):
        cur = new
        if cur > best: best = cur; bestc = list(choice); print('[%4.0fs] it %d hosted %d' % (time.time() - t0, it, best), flush=True)
    else: choice[t] = old
    if best == V: break
json.dump(bestc, open('e8covsel_%d.json' % seed, 'w'))
print('best hosted', best, flush=True)
