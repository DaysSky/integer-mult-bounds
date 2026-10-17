"""Column-generation loop for the decoder lower bound: alternate the certified LP (declp4.py, which saves duals.pkl)
with the dual-guided minrank-11 search (colgen.py), adding improving families each round.
usage: cgloop.py ROUNDS NX"""
import subprocess, sys, pickle, os
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/'
ROUNDS, NX = int(sys.argv[1]), int(sys.argv[2])
for k in range(ROUNDS):
    out = subprocess.run([sys.executable, D + 'declp4.py', str(NX), '1.0', '6'], capture_output=True, text=True, cwd=D)
    lines = [l for l in out.stdout.splitlines() if 'CERTIFIED' in l or 'saved' in l or 'weight' in l]
    print('=== round %d (NX = %d)' % (k, NX), flush=True)
    for l in lines[-14:]: print('  ', l, flush=True)
    if out.returncode != 0:
        print(out.stderr[-2000:], flush=True); break
    cg = subprocess.run([sys.executable, D + 'colgen.py', D + 'duals.pkl', '30', str(100 + k), '4000'], capture_output=True, text=True, cwd=D)
    sc = [float(l.split('score ')[1].split()[0]) for l in cg.stdout.splitlines() if 'score' in l]
    print('   colgen: %d candidates, best score %.3f, improving %d' % (len(sc), min(sc) if sc else 99, sum(s < 11 for s in sc)), flush=True)
    if not any(s < 10.999 for s in sc):
        print('   no improving column found; stopping the loop', flush=True); break
    NX += 30
