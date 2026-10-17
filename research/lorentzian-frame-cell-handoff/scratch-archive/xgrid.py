import sys
sys.path.insert(0,'.')
from fractions import Fraction as Fr
from skel import X
for h,k in [(9,1),(8,1),(6,1),(4,1),(3,1),(2,1)]:
  for x in [Fr(57,100),Fr(3,10),Fr(1,10),Fr(0)]:
    best=None
    for s in (3,5,7,9,11,13,17,21):
      try:
        r=float(X(s,h,k,x)['hi'])
      except Exception as e:
        r=None
      if r and (best is None or r>best[0]): best=(r,s)
    print(h,k,float(x),best)
