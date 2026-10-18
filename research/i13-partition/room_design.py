"""Minimum-load demand decomposition over room-subsets (the corrected vocabulary).
Design: each target t reads K pieces: rooms (full, of flats containing t -- shared up to 12x
between the flat's mates) + a private correction Delta_t (subset of R(t), built once, 1 user).
GF(2) semantics: R(t) = XOR of chosen rooms XOR Delta_t.  Greedy: process targets grouped by
flats so mates coordinate on the same rooms (reuse free); each target greedily picks rooms
maximizing |room & N_t| (N_t = remaining need), K-1 rooms, then Delta_t = leftover.
Cost: 49 x #distinct rooms + sum |Delta_t|.  Capacity: 17,056 (E8 reference: 3,000)."""
import pickle, sys, time, collections
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V; HYP = g.HYP; G = g.G
full = (1 << V) - 1
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

frames = pickle.load(open('goodframes13.pkl', 'rb'))
log('good frames', len(frames))
# rooms keyed by their flat; also room masks per target
flat_of_room = {}
rooms_by_t = collections.defaultdict(set)
for F in frames:
    room = full
    for s in [x for x in range(V) if F >> x & 1]: room &= HYP[s]
    flat_of_room[room] = room  # room == perp(flat); flat = perp(room)
    for s in [x for x in range(V) if F >> x & 1]:
        rooms_by_t[s].add(room)
log('distinct rooms', len(flat_of_room), 'per-target mean %.0f' % (sum(len(v) for v in rooms_by_t.values()) / V))

R = {t: HYP[t] & ~(1 << t) for t in range(V)}
K = 4  # pieces per target: K-1 rooms + 1 correction
used_rooms = set()
delta_total = 0
c_t_total = 0
# coordinate: process targets grouped by flats -- build flat groups covering all targets once
# greedy set cover of targets by flats (a flat = the 12 lines of perp(room))
flats = {}
for room in flat_of_room:
    fl = full
    for r in [x for x in range(V) if room >> x & 1]: fl &= HYP[r]
    flats[room] = fl
covered = set()
groups = []
while covered != set(range(V)):
    best, bestn = None, -1
    for room, fl in flats.items():
        n = len({x for x in range(V) if fl >> x & 1} - covered)
        if n > bestn: bestn, best = n, room
    if best is None or bestn == 0: break
    mates = {x for x in range(V) if flats[best] >> x & 1}
    groups.append((best, mates))
    covered |= mates
log('flat groups to cover all targets:', len(groups), 'sizes', [len(m) for _, m in groups][:10])

# per-target greedy room picks with reuse preference
room_uses = collections.Counter()
N = dict(R)
for home_room, mates in groups:
    for t in sorted(mates):
        need = N[t]
        picks = []
        # first: the home room (shared by all mates)
        if home_room & need and home_room not in picks:
            picks.append(home_room); need ^= home_room & need  # remove covered lines (subset)
            need = N[t] & ~home_room  # recompute: home room fully inside R(t)
        # wait: rooms are subsets of R(t); XOR semantics: N ^= room
        need = N[t] ^ (home_room if home_room & ~N[t] == 0 else 0)
        picked = {home_room} if home_room & ~R[t] == 0 else set()
        need = N[t]
        for rm in picked: need ^= rm
        while len(picked) < K - 1 and need:
            best, gain = None, -1
            for rm in rooms_by_t[t]:
                if rm in picked or rm & ~R[t]: continue
                # coverage gain: lines of rm inside need, with reuse bonus
                cov = bin(rm & need).count('1')
                bonus = 8 if rm in used_rooms else 0
                sc = cov * (1 + (0.3 if rm in used_rooms else 0))
                if cov > 0 and sc > gain: gain, best = sc, rm
            if best is None: break
            picked.add(best); need ^= best
        for rm in picked:
            used_rooms.add(rm); room_uses[rm] += 1
        delta = bin(need).count('1')
        delta_total += delta
        c_t_total += len(picked) + (1 if delta else 0)
log('done')
cost_rooms = len(used_rooms) * 49  # mean room size; compute exactly:
cost_rooms_exact = sum(bin(rm).count('1') for rm in used_rooms)
log('distinct rooms used:', len(used_rooms), 'exact content: %d' % cost_rooms_exact)
log('room uses total:', sum(room_uses.values()), 'use histogram:', dict(sorted(collections.Counter(room_uses.values()).items())))
log('delta total (private corrections):', delta_total, 'mean/target %.1f' % (delta_total / V))
TOTAL = cost_rooms_exact + delta_total
log('TOTAL DISTINCT CONTENT: %d  (capacity 17,056; E8 reference 3,000; load %.1f/line vs E8 25)' % (TOTAL, TOTAL / V))
log('sum c_t = %d -> R_identity = %d + dead' % (c_t_total, c_t_total - V))
