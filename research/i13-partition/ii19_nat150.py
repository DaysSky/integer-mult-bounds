"""nat150: THE NODE-SEED SWEEP - the never-swept build parameter.

gen_p4's node-realization seed shapes the DAG (the same plan, the same R,
a different delivery graph -> a different hist -> a different price).
The r434 was built at node_seed=0 only. Sweep node_seed 1..N:
params.json (the census-optimal plan) + node_seed -> gen_p4 -> tune -> hist -> price.
"""
import json, gzip, os, sys, subprocess, copy
import mpmath as mp

mp.mp.dps = 40
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
sys.path.insert(0, os.path.join('..', 'e8-bit-p111-tuned', 'tune'))
sys.path.insert(0, os.path.join('..', 'e8-bit-p111-tuned'))

HUB = os.path.abspath('../e8-bit-p111-r434/code')
PRM = os.path.abspath('../e8-bit-p111-r434/data/params.json')
P111 = mp.mpf('0.001733052823330162099157')
N = int(os.environ.get('N', '12'))

import wlib

results = []
for seed in range(1, N+1):
    # (1) build with the node_seed
    out = '/tmp/r434-nodeseed-%d.json.gz' % seed
    r = subprocess.run(['/Users/dayssky/.venv/bin/python', '-I', 'gen_p4.py', 'data/plan-l3.json', PRM, out],
                       cwd=HUB, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        print('seed %d: BUILD FAIL: %s' % (seed, r.stderr[-200:]))
        continue
    # patch: gen_p4 ignores node_seed from CLI - inject via the params copy
    prm2 = '/tmp/params-nodeseed-%d.json' % seed
    P = json.load(open(PRM))
    P['node_seed'] = seed
    json.dump(P, open(prm2, 'wt'))
    r = subprocess.run(['/Users/dayssky/.venv/bin/python', '-I', 'gen_p4.py', 'data/plan-l3.json', prm2, out],
                       cwd=HUB, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        print('seed %d: BUILD FAIL: %s' % (seed, r.stderr[-200:]))
        continue
    try:
        W = json.load(gzip.open(out, 'rt'))
    except Exception as e:
        print('seed %d: LOAD FAIL %s' % (seed, e))
        continue
    R = W['R']
    # (2) tune
    import tune
    Tn = tune.Tuner(W, a=0.001733)
    for _ in range(8):
        n = 0
        for ch in "TSF":
            for sec in "AB":
                V = Tn.view(sec)
                ap = (tune.transport_sweep(V, verbose=False) if ch == "T" else
                      tune.steinberg_sweep(V, verbose=False) if ch == "S" else
                      tune.transport_sweep(V, verbose=False, allow_move=False))
                n += len(ap)
        if not n:
            break
    Wt = Tn.word()
    hist = wlib.paid(Wt)
    # (3) the price
    sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
    from pricer import idle_slots, host_greedy
    K, T = 4, 32
    L = 2*K+1; a = 7; m_ = 1+L*a; w = 8
    v = Wt['v']
    slots = {}
    for c in idle_slots(K, a):
        slots[c] = slots.get(c, 0) + 2*v
    WW = 2*K*v*T

    def F_of(q):
        nres = R*L
        rem = host_greedy(slots, nres, w, q, m_)
        prof = {}
        for rr, z in hist.items(): prof[rr] = prof.get(rr, 0) + z*T*L
        for rr, z in rem.items(): prof[rr] = prof.get(rr, 0) + z*T
        tot = sum(prof.values())
        s = sum(mp.mpf(rr)*z/(m_*WW)*(mp.mpf(m_)/rr)**q for rr, z in prof.items() if rr < m_)
        s += 32*m_*mp.mpf(tot)/(mp.mpf(10)**16 * WW)*mp.mpf(m_)**q
        return s - 1

    lo, hi = mp.mpf(0), mp.mpf('0.05')
    if F_of(lo) >= 0:
        print('seed %d: R=%d NO-ROOT hist=%s' % (seed, R, dict(sorted(hist.items()))))
        continue
    for _ in range(60):
        mid = (lo+hi)/2
        if F_of(mid) >= 0: hi = mid
        else: lo = mid
    q = (lo+hi)/2
    pc = float((q-P111)/P111)*100
    print('seed %-3d R=%-4d hist=%-58s %s (%+.2f%%)' % (seed, R, dict(sorted(hist.items())), mp.nstr(q, 8), pc))
    results.append((pc, seed, R, dict(hist)))
    json.dump(Wt, gzip.open('/tmp/r434-nodeseed-%d-tuned.json.gz' % seed, 'wt'))

results.sort(reverse=True)
print()
print('THE BEST:', results[:3] if results else 'none')
json.dump([{'seed': s, 'R': R, 'price_pct': pc, 'hist': h} for pc, s, R, h in results],
          open('ii19_nat150_nodeseed.json', 'wt'), default=str)
print('SAVED ii19_nat150_nodeseed.json')
