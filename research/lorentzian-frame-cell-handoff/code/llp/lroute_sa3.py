"""Stage-2 local search on a routable system: minimise the lmatch3 register estimate directly (slow evaluation,
~2 s), by single-line cover changes restricted to moves that keep weak routability (U) from increasing.
usage: lroute_sa3.py init.json minutes OPTS(good|all) seed -> lroute3_best_<seed>.json"""
import sys, json, random, time, pickle, subprocess, io, contextlib, runpy
from lgeo import *
INIT, MIN, OPTS, seed = sys.argv[1], float(sys.argv[2]), sys.argv[3], int(sys.argv[4])
random.seed(seed)
cov = pickle.load(open('covers3.pkl', 'rb'))
opts = [[ms for ms, gd in cov[t] if gd or OPTS == 'all'] for t in range(V)]
cur = {int(k): v for k, v in json.load(open(INIT)).items()}
def evaluate(sysm):
    json.dump(sysm, open('_tmp_eval_%d.json' % seed, 'w'))
    out = subprocess.run([sys.executable, 'lmatch3.py', '_tmp_eval_%d.json' % seed], capture_output=True, text=True).stdout
    line = [l for l in out.splitlines() if 'model-A registers' in l][0]
    return int(line.split('=')[1].split('->')[0]), out
best, out = evaluate(cur); print('init', best, flush=True)
t0 = time.time(); it = 0
while time.time() - t0 < MIN * 60:
    it += 1
    s = random.randrange(V); ms = random.choice(opts[s])
    new = dict(cur); new[s] = sum(1 << x for x in ms) | (1 << s)
    c, o = evaluate(new)
    if c <= best:
        if c < best: print('[%4.0fs] it %d  %d -> %d' % (time.time() - t0, it, best, c), flush=True)
        best, cur, out = c, new, o
json.dump(cur, open('lroute3_best_%d.json' % seed, 'w'))
print(out)
