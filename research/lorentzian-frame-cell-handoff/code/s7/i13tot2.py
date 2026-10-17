from maxh import maxH
h, v = 13, 364
cst = [12]*13
for src in ([12],):
    for tg in ([12], [11,1], [10,2], [10,1,1]):
        row = []
        for gp in ([11,1,1], [12,1], [10,2,1], [10,1,1,1], [2,9,1,1], [1,10,1,1], [1,1,9,1,1], [4,7,1,1], [6,5,1,1], [11,2], [10,3], [8,5]):
            M = maxH(h, v, cst, src, tg, [], gp, ge=0)
            row.append('%s:%.2f' % ('-'.join(map(str, gp)), M / v if M else -1))
        print('src', src, 'tgt', tg, ' '.join(row), flush=True)
