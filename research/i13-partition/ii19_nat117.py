"""THE nat117: THE PLAN-SPACE SCAN (the >8% breakthrough hunt!!)
THE KNOB: gen_p4.plan_thirds (the seed-driven freeline/thirds draws (the published word: ONE seed-552 draw (the
  params-p111.json's frozen plan!!!)))
THE SCAN: N seeds -> the draws -> gen_p4.make (the in-process (the auto-closing extras!!)) -> the R-census!!
"""
import json, os, sys, random
sys.path.insert(0, os.path.join('..', 'e8-bit-p111', 'code'))
sys.path.insert(0, os.path.join('..', 'e8-bit-carrier-skeleton', 'code', 'skeleton'))
sys.path.insert(0, os.path.join('..', 'e8-bit-p111-r434', 'code'))
import gen_p4
from geom import Geom
from planio import load_plan

log = print
PLAN = os.path.join('..', 'e8-bit-p111', 'data', 'plan-l3.json')
PRM0 = json.load(open(os.path.join('..', 'e8-bit-p111-r434', 'data', 'params-p111.json')))

G = Geom()
sol = load_plan(PLAN)
log('the setup: G + sol loaded (the sol keys: %s)' % sorted(sol.keys()))

def make_with_seed(seed):
    fl, assign = gen_p4.plan_thirds(G, sol, random.Random(seed))
    if fl == 'failed':
        return None, ('the draw failed: %s' % assign)
    prm = dict(PRM0)
    prm['freeline'] = [[list(c), b] for c, b in fl.items()]
    prm['thirds'] = [[list(H), list(c)] for H, c in assign.items()]
    prm['extras'] = {}  # the auto-closing (the make()'s loop!!)
    try:
        (W, word), extras = gen_p4.make(PLAN, prm)
    except Exception as ex:
        return None, ('the make error: %s' % str(ex)[:120])
    return word, None

log('(1) THE CONTROL (the published plan (the params-p111.json!!)):')
sys.path.insert(0, os.path.join('..', 'e8-bit-p111-r434', 'code'))
import importlib
r = None
try:
    (W, word), extras = gen_p4.make(PLAN, PRM0)
    log('  the control: R = %d (the stats %s)' % (word['R'], word['stats']))
except Exception as ex:
    log('  the control error: %s' % str(ex)[:200])

log('(2) THE SEED-SCAN (the R-census!!):')
results = []
N = int(os.environ.get('N', '30'))
for seed in range(N):
    word, err = make_with_seed(seed)
    if err:
        log('  seed %3d: %s' % (seed, err)); continue
    R = word['R']
    results.append((R, seed, word['stats'].get('extra_carriers', -1), word['stats'].get('junk_wires', -1)))
    log('  seed %3d: R = %4d | %s' % (seed, R, word['stats']))

results.sort()
log('(3) THE R-CENSUS (the sorted!!): %s' % results[:12])
json.dump(results, open('ii19_nat117_planscan.json', 'wt'))
log('SAVED ii19_nat117_planscan.json')
