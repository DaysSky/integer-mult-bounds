import sys
sys.path.insert(0, '.')
import importlib.util
spec = importlib.util.spec_from_file_location('r4', 'r420i13.py')
src = open('r420i13.py').read().split('for R in (1092')[0]
ns = {}; exec(compile(src, 'r420i13', 'exec'), ns)
price = ns['price']; P111 = ns['Q'].P111
for R in (1274, 1500, 1750, 2000, 2300, 2600):
    row = []
    for fr in (0, 0.25, 0.5, 0.75, 1.0):
        for e in (2, 4):
            if fr == 0 and e == 4: continue
            c = price(R, int(fr * R), e)
            row.append('%s/e%d:%s' % (fr, e, ('%+.1f' % float((c / P111 - 1) * 100)) if c else 'wall'))
    print('R=%d  ' % R + '  '.join(row), flush=True)
