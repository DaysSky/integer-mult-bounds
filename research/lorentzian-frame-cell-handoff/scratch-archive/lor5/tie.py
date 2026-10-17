import sys, re, subprocess, os
from fractions import Fraction as Fr
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SP + '/lor2/hub')
import est_model as E
CAL = {(s, m): E.calibration(s, m) for s in ('bit', 'complex') for m in ('abs', 'rel')}
REF = {'bit': 1.7331e-3, 'complex': 1.5987e-3}
def val(side, h, x, rho, m):
    b = E.estimate(side, h, x, Fr(rho).limit_denominator(1000), m)
    return b[1] * CAL[(side, m)] if b else 0
def tie(side, h, x, m):
    ref = val(side, 8 if side == 'bit' else 9, Fr(63, 111) if side == 'bit' else Fr(64, 112), Fr(439, 111) if side == 'bit' else Fr(496, 112), m)
    lo, hi = 0.25, 12.0
    if val(side, h, x, hi, m) >= ref: return '>12'
    if val(side, h, x, lo, m) < ref: return '<.25'
    for _ in range(40):
        mid = (lo + hi) / 2
        if val(side, h, x, mid, m) >= ref: lo = mid
        else: hi = mid
    return '%.2f' % lo
for p in sys.argv[1:]:
    c = subprocess.run([sys.executable, SP + '/lor3/costs.py', p], capture_output=True, text=True).stdout
    mb = re.search(r'BIT: rank P = (\d+) totals (\d+) cst = (\d+) x = ([\d.]+) window (\d+)', c)
    mc = re.search(r'COMPLEX: c = (\d+) cst = (\d+) x = ([\d.]+) binary window (\d+)', c)
    import json; v = len(json.load(open(p))['R'])
    out = [os.path.basename(p), 'v=%d' % v]
    if mb:
        x, h = Fr(int(mb.group(3)), v), int(mb.group(5))
        out += ['BIT x=%.4f h=%d tie-rho abs %s rel %s' % (x, h, tie('bit', h, x, 'abs'), tie('bit', h, x, 'rel'))]
    if mc:
        x, h = Fr(int(mc.group(2)), v), int(mc.group(4))
        out += ['| CX x=%.4f h=%d tie-rho abs %s rel %s' % (x, h, tie('complex', h, x, 'abs'), tie('complex', h, x, 'rel'))]
    print(' '.join(out), flush=True)
