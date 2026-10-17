import sys
sys.path.insert(0,'.')
from fractions import Fraction as Fr
from skel import X
def best(h,k,x):
    b=None
    for s in (3,5,7,9,11,13,15):
        r=X(s,h,k,x)
        if r is None: continue
        v=float(r['hi'])
        if b is None or v>b[0]: b=(v,s)
    return b
print('E8 bit ref', best(8,1,Fr(3,5)))
print('E8 cx ref', best(9,1,Fr(64,112)))
for h,k,x in [(8,2,Fr(6,10)),(8,2,Fr(1)),(8,2,Fr(12,10)),(8,2,Fr(3,2)),(8,3,Fr(1)),(8,3,Fr(2)),(8,4,Fr(2)),(9,2,Fr(1)),(12,2,Fr(1)),(12,3,Fr(1)),(12,4,Fr(2)),(16,4,Fr(2)),(16,2,Fr(1))]:
    print(h,k,float(x),best(h,k,x),flush=True)
