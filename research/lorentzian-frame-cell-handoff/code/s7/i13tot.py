from maxh import maxH
h, v = 13, 364
cst = [12]*13
for src in ([12], [1,11], [2,10], [1,2,9]):
    for tg in ([12], [2,10], [1,2,9]):
        row = []
        for gp in ([1,12], [2,11], [1,1,11], [2,3,8], [1,2,10], [1,2,3,7], [4,9], [2,2,9], [1,1,2,9], [3,10], [6,7]):
            M = maxH(h, v, cst, src, tg, [], gp, ge=0)
            row.append('%s:%.2f' % ('-'.join(map(str, gp)), M / v if M else -1))
        print('src', src, 'tgt', tg, ' '.join(row), flush=True)
