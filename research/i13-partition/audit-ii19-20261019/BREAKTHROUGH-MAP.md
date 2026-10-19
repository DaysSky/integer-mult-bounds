# II19 breakthrough map (2026-10-19): what a wide-margin win would need

This is a follow-up to `AUDIT.md`, prepared for DaysSky with assistance from Claude.

- **Question:** is there any lever that could make an II19 (Lorentzian) bit word beat the frontier
  (r434, c = 0.0017444) by a wide margin?
- **Method:** the exact pricer only. Histograms marked "model" are shapes, not words.
- **Short answer:** I found no such lever in the current format, and §4 explains why II19 structurally
  trails its h = 8 parent. A wide margin needs a class of middle that nobody has exhibited, even for E8.

## 0. Framing: the bit side does not bind κ

`docs/research/current-status.md`: the selected κ = 0.001672660 is complex-bound. The bit supplier
"remains #589 on #555". A bit-side win of any size (II19 or E8) is headroom for the bit side only. It
moves κ only together with complex-side progress.

## 1. Where the price is lost (verified)

**Fixed by (v, h, cst).** The profile mass T·L·(cst + 2K·a·v) and the deficit 32(8v − 9cst) are both
fixed by (v, h, cst), independent of R (`audit_pricer.py`). A word therefore only chooses how that fixed
mass splits into ranks: c ≈ deficit / Σ r·z_r·ln(m/r).

**86% of the ln-mass is local climbs (`audit_anatomy.py`).** By role:

| role | r434 frontier | record W4 |
|---|---|---|
| targets | 2 climbs (2,5), 4 B-reads | 2–3 climbs |
| sources | 5 climbs (1,2,2,1,1) | 5 climbs (1,2,2,2,1) |
| helpers | 434 helpers, 4–6 rank-1/2 climbs each | same anatomy |

In the r434 the helpers account for 74% of all climbs.

## 2. What a wide margin requires (model, `audit_breakthrough.py`)

Shapes give every source, target and helper k even climbs.

| II19-112 (h=9, cst 64) | k=1 | k=2 | k=3 | k=4 |
|---|---|---|---|---|
| R/v 1.0 | +95% | +65% | +51% | +42% |
| R/v 2.0 | +68% | +38% | +25% | +17% |
| R/v 3.0 | +46% | +18% | +6% | −1% |
| R/v 3.9 | +30% | +4% | −7% | −13% |

The r434 behaves like k = 4 at R/v 3.9. A **+25% II19 word** needs about **R/v ≈ 2 with ≤ 3 climbs per
register**, or about R/v ≈ 3 with 2 climbs. That means halving the helper count and the helper ladder
length of every known E8-class middle together.

## 3. Why the E8-type middle resists that

- **Cell bottleneck (handoff):** R ≥ 390 = 3.25v for E8 in the frame-cell class.
- **Reach decay.** A source's x_s can leave its register only at frames on its single chain.
  - In E8 the lines ⊥ s number 63. Any 2-dim frame through s keeps at most 36 of them (E6).
  - So at least 27 targets per source must be reached through registers whose first frame is ⟨s⟩.
  - Each register has one dim-1 frame. Every source therefore needs dedicated relays, and the relays'
    reach decays again at each step.
  - This compounding is what drives the 200 A-DAG intermediates and R ≈ 3.5–3.9v.
- **Private slices.**
  - perp(t) is E7, and covering its 63 lines with hyperplane slices takes 3: the D6 slices of a Fano
    line in an orthogonal 7-frame; two E6-type slices cover at most 57.
  - Each slice beyond the target's own needs a register at t^⊥, which only t can read there.
  - Hence ~2 wires per target, as the r434 has (225 wires ≈ 2v).
  - At h = 9 the special line adds one dimension but no reach: frames S ⊕ ⟨special⟩ hold the same E8
    lines.
- **Idealized middle at those densities** (targets 2 climbs, sources and helpers 3; model):

  | system | R/v 3.25 | R/v 3.50 | R/v 3.90 |
  |---|---|---|---|
  | II19-112 | +3.6% | −0.2% | −5.6% |
  | E8/P111 | +20.1% | +15.7% | +9.4% |

These are a mechanism and counting bounds, not an impossibility theorem. They place every E8-type
II19 middle at about a tie at best.

## 4. Why II19 trails its h = 8 parent at equal middle quality

- At the same middle, II19 sits 16–17 points below E8: h = 9 raises the fixed mass by a factor of 8/7
  and the window from m = 64 to 73.
- The Lorentzian lift has to add a dimension. The handoff proves that no Lorentzian form keeps E8's or
  P111's orthogonality pattern at h = 8.
- Twins of E8 lines at higher levels are pairwise non-orthogonal ((α,n)·(β,n) = α·β − 2n² ≠ 0). That
  forces an identity decoder block of 120, so richer Lorentzian systems pay in the decoder.
- Any middle improvement transfers from E8 to II19 at this discount. An II19 win of +W% needs an E8
  middle worth about +(W + 17)%.

## 5. Levers ranked by II19 effect (model unless stated)

| lever | II19-112 effect | status |
|---|---|---|
| decoder correction (`AUDIT.md` E1) | −23% → −14.6% | verified decoder; word not built (R ≤ 448) |
| idealized 3-climb middle at R/v 3.25 | → +3.6% | no such middle known |
| idle slots without bridge split (format-limits A.7 rule) | +5.2 points | pipeline scope change; also lifts r434 by +6.2% |
| double-star decoder copied at the cut | +10 points | format extension; in bitE8/1 each copy costs 7 |
| stage count | ≤ +1.8 points at R ≤ 2.29v | checked; not a lever |
| signature | 0 | price-invisible (`AUDIT.md` E3) |

## Open next questions

1. **A middle class with slow reach decay.**
   - Screen systems for lines whose perps nest along short flags (D_n-like reach), using a valid decoder
     bound rather than rank(B0).
   - First step: compute max-lines-in-subspace profiles alongside the `audit_nonorth_lb.py` decoder bounds.
   - Blocker: so far slow-reach systems (D_n) have x > 1 with standard decoders.
2. **E8 lever A** (a middle better than R420 per incidence).
   - It is the only route that moves both E8 and II19.
   - The handoff already ranks it first.
3. **Complex side.** It binds κ, so it has the larger payoff for the program's headline number.
