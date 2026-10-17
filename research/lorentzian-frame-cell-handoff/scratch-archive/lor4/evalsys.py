"""Evaluate an orbit-form Lorentzian system: expand, exact bit/complex x (lor3/costs.py), hub helper-model value
(#620 est_model, fixed calibration) at rho = 2, 3, 3.95, and closed-line cover histogram."""
import json, sys, subprocess, re, os
from fractions import Fraction as Fr
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SP + '/lor2/hub'); sys.argv_save = sys.argv[:]
import est_model as E
CAL = {s: E.calibration(s, 'abs') for s in ('bit', 'complex')}
CALR = {s: E.calibration(s, 'rel') for s in ('bit', 'complex')}
def run(p):
    base = os.path.basename(p).replace('best_', 'sys_')
    out = os.path.join(os.path.dirname(os.path.abspath(p)), base)
    subprocess.run([sys.executable, SP + '/lorcov/expand.py', p, out], check=True, capture_output=True)
    c = subprocess.run([sys.executable, SP + '/lor3/costs.py', out], capture_output=True, text=True).stdout
    mb = re.search(r'BIT: rank P = (\d+) totals (\d+) cst = (\d+) x = ([\d.]+) window (\d+)', c)
    mc = re.search(r'COMPLEX: c = (\d+) cst = (\d+) x = ([\d.]+) binary window (\d+)', c)
    d = json.load(open(out)); v = len(d['R'])
    res = dict(sys=base, v=v)
    if mb:
        cst, hb = int(mb.group(3)), int(mb.group(5))
        res['bit'] = dict(rankP=int(mb.group(1)), cst=cst, x=round(cst / v, 4), h=hb,
                          model={rho: ['%.2e' % (E.estimate('bit', hb, Fr(cst, v), Fr(rho).limit_denominator(100), m)[1] * (CAL if m == 'abs' else CALR)['bit'])
                                       for m in ('abs', 'rel')] for rho in (2, 3, 3.95)} if hb >= 2 and Fr(cst, v) < 1 else None)
    if mc:
        cst, hb = int(mc.group(2)), int(mc.group(4))
        res['complex'] = dict(c=int(mc.group(1)), cst=cst, x=round(cst / v, 4), h=hb,
                              model={rho: ['%.2e' % (E.estimate('complex', hb, Fr(cst, v), Fr(rho).limit_denominator(100), m)[1] * (CAL if m == 'abs' else CALR)['complex'])
                                           for m in ('abs', 'rel')] for rho in (2, 3, 3.95)} if hb >= 2 and Fr(cst, v) < 1 else None)
    lc = subprocess.run([sys.executable, SP + '/lorcov/linecover.py', out], capture_output=True, text=True).stdout
    m = re.search(r'line cover (\{.*\})', lc); res['line_cover'] = m.group(1) if m else lc[-200:]
    print(json.dumps(res), flush=True)
for p in sys.argv[1:]:
    try:
        run(p)
    except Exception as e:
        print(json.dumps(dict(sys=p, error=repr(e))), flush=True)
