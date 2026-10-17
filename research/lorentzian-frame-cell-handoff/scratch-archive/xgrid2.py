import sys
sys.path.insert(0,'.')
from fractions import Fraction as Fr
from skel import X
for h,x in [(10,Fr(1,3)),(12,Fr(1,5)),(16,Fr(7,100)),(13,Fr(3,7)),(11,Fr(1,2)),(8,Fr(57,100))]:
    best=None
    for s in (3,5,7,9):
        r=float(X(s,h,1,x)['hi'])
        if best is None or r>best[0]: best=(r,s)
    print(h,float(x),best,flush=True)
