import pickle, random, collections, itertools, sys
frames, comp_lists, kinds = pickle.load(open('../i13a/compat13.pkl', 'rb'))
part = [tuple(sorted(f)) for f in pickle.load(open('../i13a/pg23_partition.pkl', 'rb'))]
by_line = collections.defaultdict(list)
for i, q in enumerate(frames):
    for l in q: by_line[l].append(i)
def covers(lines, cap):
    lines = set(lines)
    if not lines: yield []; return
    u = min(lines)
    for j in by_line[u]:
        q = set(frames[j])
        if q <= lines:
            for rest in covers(lines - q, cap): yield [j] + rest
random.seed(0)
for k in (2, 3, 4, 5, 6, 8):
    cnt = collections.Counter()
    for trial in range(200 if k < 6 else 60):
        sel = random.sample(part, k)
        freed = [l for f in sel for l in f]
        n = sum(1 for _ in itertools.islice(covers(freed, 0), 1000))
        cnt[min(n, 1000)] += 1
    print('k=%d: #exact covers of freed lines (dist over random frame subsets):' % k, sorted(cnt.items())[:12], flush=True)
