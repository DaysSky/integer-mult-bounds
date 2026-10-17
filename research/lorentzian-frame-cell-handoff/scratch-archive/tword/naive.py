"""Pipeline validation word for T_h: centre decoder (h totals at C_i = span{t_T : T contains i}), naive reads (one copy
register per (target, reader) pair, the paper's side-wire structure).  Correct by construction, deliberately inefficient."""
import sys, json, gzip
from tfam import TFam
from gword import GWord
h = int(sys.argv[1]); out = sys.argv[2]
f = TFam(h); S = f.S; v = f.v
w = GWord(f)
# ---- phase A: totals.  For each point i a total register at C_i; each line T contributes to its 3 totals through
# copies taken at the line's own frame (the source stays at its start frame during A and B).
Ci = [f.span_lines([s for s in range(v) if i in f.trip[s]]) for i in range(h)]
tot = []
for i in range(h):
    r = w.helper('total%d' % i); tot.append(r)
    for s in range(v):
        if i not in f.trip[s]: continue
        c = w.helper('tcopy')
        w.gate(f.line_space[s], c, [s])          # c = x_s at <t_s>
        w.gate(Ci[i], r, [c])                    # total += x_s at C_i
w.ret = tot
w.phase = 'B'
scatter = [[k for k in range(h) if k in f.trip[t]] for t in range(v)]
# ---- phase B: reads.  y_t += x_s for every reader s, through a fresh copy at <t_s>, delivered at t-perp
for t in range(v):
    P = f.tperp(t)
    for s in f.readers(t):
        c = w.helper('rcopy')
        w.gate(f.line_space[s], c, [s])
        w.gate(P, v + t, [c])
w.finish()
word = w.build(scatter, Ci)
json.dump(word, gzip.open(out, 'wt'))
print('h', h, 'v', v, 'R', w.nh, 'gates A/B', len(word['A']), len(word['B']))
