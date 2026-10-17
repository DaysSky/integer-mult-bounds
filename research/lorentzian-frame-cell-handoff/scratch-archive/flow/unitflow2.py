import sys, time
from unitflow import build
from units import UNITS
from colgen import max_flow_cg
for name in sys.argv[1:]:
    R = UNITS[name]; c, rho, totals, side = build(R); v, h = R.shape
    t0 = time.time()
    val, dual, W, E, y = max_flow_cg(c, rho)
    print(name, 'v', v, 'W', W, 'edges', E, 'F* in [%.6f, %.6f]' % (val, dual), 'W-F* <=', round(W - val, 6), '%.0fs' % (time.time() - t0), flush=True)
