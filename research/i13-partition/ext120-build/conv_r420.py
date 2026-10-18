"""Convert the vendored E8 R420 word (bitE8/1+mut: frames as line-index lists, form '<x,y>/2') into the
gcheck.py word format (frames as spanning vectors, form {num, den}, ret_frames from replay)."""
import gzip, json, sys
src = sys.argv[1]; out = sys.argv[2]
w = json.load(gzip.open(src, 'rt'))
assert w['form'] == '<x,y>/2' and w['h'] == 8
h, v = w['h'], w['v']
L = w['lines']
frames = [[list(L[i]) for i in f] for f in w['frames']]
# ret_frames: replay the frame pointers through D and A (climbs only move to the gate frame)
cur = list(w['start'])
for F, d, srcs in w['D'] + w['A']:
    for r in [d] + srcs: cur[r] = F
rf = [cur[q] for q in w['ret']]
o = dict(h=h, v=v, R=w['R'], form=dict(num=[[1 if i == j else 0 for j in range(h)] for i in range(h)], den=2),
         lines=L, frames=frames, start=w['start'], final=w['final'], D=w['D'], A=w['A'], B=w['B'], C=w['C'],
         ret=w['ret'], ret_frames=rf, scatter=w['scatter'])
json.dump(o, open(out, 'w'))
print('ret_frames', rf, 'frames', len(frames))
