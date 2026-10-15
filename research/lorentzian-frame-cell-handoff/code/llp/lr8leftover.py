"""Leftover / independence screen for a rank-8 design with parts (from an exact hosting solution): for each section
frame F, its delivered users' parts: (a) independent? (b) if only one delivered user and its part spans F-perp
(closure rank 8) -> assembly leftover (+1); (c) count in-chain users not hosted (they need own arrivals or a 4th
delivery).  Input: JSON {F_hex: {"deliv": {b: part_hex}, "inchain": [t...]}}.  usage: lr8leftover.py parts.json"""
import sys, json
from lgeo import *
P = json.load(open(sys.argv[1]))
def gf2_rank(vs):
    rows = list(vs); r = 0
    for bit in range(V):
        piv = next((i for i in range(r, len(rows)) if rows[i] >> bit & 1), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> bit & 1: rows[i] ^= rows[r]
        r += 1
    return r
left = dep = single_span = 0
for Fh, d in P.items():
    parts = [int(v, 16) for v in d['deliv'].values()]
    if gf2_rank(parts) < len(parts): dep += 1
    if len(parts) == 1 and rank(pp(parts[0])) == 8: single_span += 1
print('sections', len(P), 'dependent delivered parts', dep, 'single-delivered spanning (leftover +1)', single_span)
