"""Hyperplane-ended (HPE) Lorentzian word: the r434 frontier embedded in II_{1,9} (P111 lines + special of norm
-2, h=9) with its whole helper network inside the hyperplane U = sp^perp = E8.  Every helper ends at U and the
cleanup C runs at U (word key 'hyperplane_end'); only sources (-> full_9) and targets (-> t^perp + <sp>) step into
the special direction, each by one rank-1 climb.  Checked by gcheck_hpe.py (gcheck + that one extension).
usage: hpe_lorentz.py OUT.json"""
import json, os, sys
from _common import I13
W = json.load(open(os.path.join(I13, 'ii19_pub2_p111-r434.json')))
v, h, R = W['v'], W['h'], W['R']; nreg = 2 * v + R
sp = [0] * 8 + [1]
frames = [[x + [0] for x in F] for F in W['frames']]
dims_full = [k for k, F in enumerate(W['frames']) if len(F) and k == W['final'][0]]
U = W['final'][0]                                   # the r434 full frame: now the 8-dim hyperplane E8 = sp^perp
FULL9 = len(frames); frames.append([x + [0] for x in W['frames'][U]] + [sp])
SPF = len(frames); frames.append([sp])
tperp9 = {}
for t in range(v):
    f = W['final'][v + t]
    if f not in tperp9: tperp9[f] = len(frames); frames.append([x + [0] for x in W['frames'][f]] + [sp])
rm = lambda r: r if r < v else (r + 1 if r < 2 * v else r + 2)
V2 = v + 1; SPS, SPT = v, 2 * V2 - 1; N2 = 2 * V2 + R
start = [None] * N2; final = [None] * N2
for r in range(nreg):
    start[rm(r)] = W['start'][r]
    if r < v: final[rm(r)] = FULL9
    elif r < 2 * v: final[rm(r)] = tperp9[W['final'][r]]
    else: final[rm(r)] = U
start[SPS], final[SPS] = SPF, FULL9
start[SPT], final[SPT] = 0, U
g = lambda gl: [[F, rm(d), [rm(s) for s in srcs]] for F, d, srcs in gl]
num = [row + [0] for row in W['form']['num']] + [[0] * 8 + [-2 * W['form']['den']]]
word = dict(format='bitGen/1+mut+hpe', h=h + 1, v=V2, R=R, hyperplane_end=U,
            form=dict(num=num, den=W['form']['den']), lines=[l + [0] for l in W['lines']] + [sp],
            frames=frames, start=start, final=final, D=g(W['D']), A=g(W['A']), B=g(W['B']), C=g(W['C']),
            ret=[rm(q) for q in W['ret']] + [SPS], ret_frames=W['ret_frames'] + [SPF],
            scatter=[list(s) for s in W['scatter']] + [[len(W['ret'])]],
            note='r434 in II_{1,9}: helpers and cleanup in U = sp^perp (hyperplane_end); special = orthogonal singleton')
json.dump(word, open(sys.argv[1], 'w')); print('wrote', sys.argv[1], 'U =', U)
