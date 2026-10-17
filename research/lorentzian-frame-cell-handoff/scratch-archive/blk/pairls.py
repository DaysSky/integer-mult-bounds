# First-improvement local search over per-frame pairings for build_hubm.py (best-known options), EVAL objective.
import subprocess, os, random, re, json, sys
env0 = dict(os.environ, PCHAIN='1', QMERGE='1', QALL='1', PIECES='paar', HOP='0', MP='1', EVAL='1')
def R(p):
    e = dict(env0, PAIRS=','.join(map(str, p)))
    out = subprocess.run([sys.executable, 'build_hubm.py', 'blkpartA.pkl', '/dev/null'], env=e, capture_output=True, text=True).stdout
    m = re.search(r"EVAL \{'R': (\d+)\}", out)
    return int(m.group(1)) if m else 10 ** 9
best = [1] * 54; bR = R(best); print('start', bR, flush=True)
rnd = random.Random(1); improved = True; sweep = 0
while improved:
    improved = False; sweep += 1
    order = list(range(54)); rnd.shuffle(order)
    for i in order:
        for alt in (0, 1, 2):
            if alt == best[i]: continue
            p = list(best); p[i] = alt; r = R(p)
            if r < bR:
                best, bR, improved = p, r, True
                print('sweep', sweep, 'frame', i, '->', alt, 'R', bR, flush=True)
                json.dump(dict(R=bR, pairs=best), open('pairls_best.json', 'w'))
                break
print('local optimum', bR, best, flush=True)
