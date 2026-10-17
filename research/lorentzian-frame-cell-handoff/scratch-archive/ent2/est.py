import sys
sys.path.insert(0,'/home/user/integer-mult-bounds/research/e8-bit-p111-e1/code')
import price_e1 as PE
from mpmath import mpf
ref = mpf('0.001733427039589844')
base = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
for n7, d1 in [(1,1),(10,10),(50,50),(100,100),(200,200),(285,285),(438,438)]:
    loc=dict(base); loc[1]-=d1
    out=PE.price(loc,439,n7)
    if out is None: print(n7,'infeasible'); continue
    c,rem,o=out
    print('n7 %d: c %.15f %+.3f%% rem %s opt %s'%(n7,float(c),float((c/ref-1)*100),rem,o),flush=True)
