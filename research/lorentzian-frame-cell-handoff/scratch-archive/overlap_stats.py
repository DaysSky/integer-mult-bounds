import sys, pickle, collections, itertools
sys.path.insert(0,'/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid'); sys.path.insert(0,'/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lbuild')
import os
os.environ['GEN']='1'
# reuse build_a3g top construction by exec up to the piece finder
src=open('build_a3g.py').read()
cut=src.index('# ---- hierarchical pieces')
sys.argv=['x','a3_choice_pack.pkl','/dev/null']
exec(compile(src[:cut],'top','exec'))
tops=list(demand)
print('top demands', len(tops))
mx=[]; second=[]
for D in tops:
    ov=sorted((pc(content[D]&content[E]) for E in tops if E!=D), reverse=True)
    mx.append((pc(content[D]), ov[0], ov[1], ov[2]))
import statistics
print('content size median', statistics.median(m[0] for m in mx))
print('best overlap median', statistics.median(m[1] for m in mx), '2nd', statistics.median(m[2] for m in mx), '3rd', statistics.median(m[3] for m in mx))
print('fraction best overlap/content median', statistics.median(m[1]/m[0] for m in mx))
sig=collections.Counter()
for u in range(V):
    s=frozenset(i for i,D in enumerate(tops) if content[D]>>u&1); sig[s]+=1
print('distinct line signatures', len(sig), 'avg demands per line', sum(len(s)*c for s,c in sig.items())/V)
