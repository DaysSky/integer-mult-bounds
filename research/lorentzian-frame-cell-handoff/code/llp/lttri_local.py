"""Local zero-waste test for every M11 triangle node with three delivered users.  At node (A,B,C,E) a transversal
tau = T(a,b,c) lies in user X's part iff X takes the crossing pair it defines for X here: forced if that pair crosses
only at this node among X's 4 nodes, free otherwise.  Zero waste needs rank(P(E) + own-A2 terms + XOR of the three
transversal sets) <= 7, which (rank count: P(E) 1 + T 1 + coordinate directions) requires the XOR set to avoid
varying in at least one direction fully, i.e. to contain no line with some coordinate value v in some block
(A, B or C).  For each node and each (block, value) we check by brute force over the free memberships of the
9 transversals having that value whether all their counts can be made even.  If no (block, value) works, the node
needs >= 1 extra register whenever all three users are delivered.  usage: lttri_local.py"""
import json, itertools, collections
sol = [tuple(tuple(T) for T in node) for node in json.load(open('lttri_design_z11.json'))]
nodes_of = collections.defaultdict(list)
for ni, node in enumerate(sol):
    for T in node: nodes_of[T].append(ni)
def mult(X, pair):
    """number of X's nodes where pair crosses"""
    k = 0
    for nj in nodes_of[X]:
        B, C = [T for T in sol[nj] if T != X]
        if (pair[0] in B and pair[1] in C) or (pair[0] in C and pair[1] in B): k += 1
    return k
ok_nodes = 0; hist = collections.Counter()
for ni, (A, B, C) in enumerate(sol):
    feasible_any = False
    for blk_i, blk in enumerate((A, B, C)):
        for v in blk:
            good = True
            # transversals with coordinate v in block blk
            others = [T for T in (A, B, C) if T != blk]
            for y in others[0]:
                for z in others[1]:
                    tau = {blk_i: v}
                    pts = (v, y, z)
                    # membership for each user X: the pair is tau minus X's own coordinate
                    forced = 0; free = 0
                    for X in (A, B, C):
                        pair = tuple(sorted(p for p in pts if p not in X))
                        if mult(X, pair) == 1: forced += 1
                        else: free += 1
                    # can count be even? count = forced + (#free chosen); free can add 0..free
                    if not any((forced + f) % 2 == 0 for f in range(free + 1)): good = False; break
                if not good: break
            if good: feasible_any = True
    hist[feasible_any] += 1
print('triangle nodes where some (block, value) can be made even (necessary for zero waste with 3 delivered):', dict(hist))
