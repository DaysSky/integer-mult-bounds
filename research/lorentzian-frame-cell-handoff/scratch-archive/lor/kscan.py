import sys
sys.path.insert(0,'/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price
from mpmath import mp
import price_a3reach as A
P111t = mp.mpf('0.001733427039589844'); E1 = mp.mpf('0.001734473240795253742474')
for K in (3,4,5,6,7):
    out=[]
    for R in (700,750,800,900,1000):
        c=price(A.hist(5,R),220,11,R,K=K)[0]
        out.append('R%d %s'%(R, ('%+.2f%%'%float((c/P111t-1)*100)) if c else 'none'))
    print('K',K,' '.join(out),flush=True)
