"""New L3 plans (planL3 CP-SAT model, random objectives) screened for punctured words with fewer extra helpers.
Per plan: eligible lines, affinely independent puncture sets, a lower bound per P (forced junk + ceil(missing/2) per
supplying block), then sampled keeper plans (gen_p4 accounting) on the most promising P."""
import sys, itertools, random, time, json, pickle
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/45552e66-7196-5fbb-857a-ded5e6dbacae/scratchpad/plans')
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-r420/discovery')
import pcensus as pc
from planL3 import build_model, extract
from ortools.sat.python import cp_model
G, V, e8 = pc.G, pc.V, pc.e8
BROW = [sum((int(e8.GI[t, b]) & 1) << b for b in range(V)) for t in range(V)]
pairs = [(0, 1), (2, 4), (3, 5), (6, 9), (7, 8)]


def affine_ok(P):
    basis = []
    for v in [(1 << V) | BROW[p] for p in P]:
        for b in basis:
            v = min(v, v ^ b)
        if v:
            basis.append(v)
    return len(basis) == 9


def lb_block(B, P):
    bk = pc.Block(B, P)
    k_in = sum(1 for p in P if G.blk[p] == B); k_out = sum(1 for p in P if G.blk[p] == G.comp[B])
    junk = max(0, k_in - k_out)       # outputs 12-k_out over inputs 12-k_in
    if not bk.taus:
        return junk
    U = 0
    for p in bk.taus:
        U |= bk.Np0[p]
    need = set(pc.bits(U))
    cov = max(len(need & (set(bk.freed) | set(ch))) for ch in itertools.product(*[list(c) for c in bk.cells]))
    miss = len(need) - cov
    return max(junk, (miss + 1) // 2)


def sample_block(B, P, n, rng):
    bk = pc.Block(B, P); best = None
    for _ in range(n):
        flb = rng.randrange(64); perm = bk.cells[:]; rng.shuffle(perm); rs = [rng.choice((1, 2, 3)) for _ in bk.taus]
        try:
            r = bk.cost_new(flb, perm, rs, bound=None if best is None else best[0])
        except AssertionError:
            continue
        if r is not None and (best is None or r[0] < best[0]):
            best = (r[0], flb, perm, rs, r[1], r[2])
            if best[0] == 0:
                break
    return best


def evaluate_plan(sol, log, nsample=1500):
    pc.setplan(sol)
    byframe = {}
    for p in pc.ELIG:
        byframe.setdefault(G.phi[p], []).append(p)
    cands = []
    for fs in itertools.combinations(sorted(byframe), 9) if len(byframe) >= 9 else []:
        for P in itertools.product(*(byframe[f] for f in fs)):
            if affine_ok(P):
                cands.append(tuple(sorted(P)))
    log('eligible', len(pc.ELIG), 'frames', len(byframe), 'affine-OK P', len(cands))
    if not cands:
        return None
    lbs = []
    cache = {}
    for P in cands:
        tot = 0
        for B in range(10):
            key = (B, tuple(p for p in P if G.blk[p] in (B, G.comp[B])))
            if key not in cache:
                cache[key] = lb_block(B, list(key[1]))
            tot += cache[key]
        lbs.append((tot, P))
    lbs.sort()
    log('LB distribution (best 5):', [t for t, _ in lbs[:5]], 'P', lbs[0][1])
    rng = random.Random(0); res = []
    for lb, P in lbs[:4]:
        if lb >= 5:
            break
        tot = 0; per = {}
        for B in range(10):
            s = sample_block(B, list(P), nsample, rng)
            if s is None:
                tot = None; break
            per[B] = s; tot += s[0]
        log('  P', P, 'LB', lb, 'sampled UB', tot)
        res.append((tot, lb, P, per))
    return res


if __name__ == '__main__':
    seed0, n = int(sys.argv[1]), int(sys.argv[2])
    out = []
    t0 = time.time()
    log = lambda *a: print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
    for seed in range(seed0, seed0 + n):
        rng = random.Random(seed)
        M, Vv = build_model(G, rank_mode="strong")
        obj = [rng.randrange(-3, 4) * b for b in Vv["X"].values()] + [rng.randrange(-3, 4) * b for b in Vv["rcv"].values()]
        M.Maximize(sum(obj))
        S = cp_model.CpSolver(); S.parameters.max_time_in_seconds = 20.0; S.parameters.num_workers = 2
        S.parameters.random_seed = seed
        r = S.Solve(M)
        if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            log('seed', seed, 'status', S.StatusName(r)); continue
        sol = extract(S, Vv)
        log('seed', seed, 'plan solved')
        res = evaluate_plan(sol, log)
        out.append((seed, sol, res))
        pickle.dump(out, open('plansearch_%d.pkl' % seed0, 'wb'))
