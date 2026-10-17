import sys
sys.path.insert(0,'.')
import est_model as E
from fractions import Fraction as Fr
for side in ('bit','complex'):
    for mode in ('abs','rel'):
        cal=E.calibration(side,mode)
        ref=E.BIT if side=='bit' else E.CX
        e8=E.estimate(side,ref['h'],ref['x'],Fr(ref['R'],ref['v']),mode)
        print(side,mode,'cal %.3f'%cal,'E8 a_cal %.3e'%(e8[1]*cal))
        for h,x in [(10,Fr(11*10,330)),(10,Fr(110,250)),(10,Fr(110,220)),(11,Fr(1,2)),(13,Fr(3,7)),(8,Fr(3,10)),(6,Fr(4,10)),(4,Fr(1,2))]:
            row=[]
            for rho in [2,3,4,6,10]:
                b=E.estimate(side,h,x,Fr(rho),mode)
                row.append('%.2e'%(b[1]*cal) if b else '-')
            print('  h=%d x=%.3f'%(h,float(x)),' rho2..10:',row)
