# Digest: what has been tried in CrocSwap/integer-mult-bounds (Discussions + local repo)

Prepared 2026-10-14 (read-only; nothing posted, nothing modified). Sources:
- GitHub Discussions: all list pages (`?page=1..7`; page 7 = only pinned #1163), the Ideas category (2 pages), and
  `is:closed` (zero closed discussions). About 130 discussions in total, #1163 to #1753. I fetched about 95 threads
  with WebFetch, which returns a model summary rather than raw text. Numbers below are as the posters reported them.
  None were re-verified here. #1645 and parts of #1166 (after 100k chars) could not be fetched (tool refusal or truncation).
- A few PR pages: #288, #895, #836, #172, #928.
- Local repo `/home/user/integer-mult-bounds` (base bce54fb3): `docs/research/*.md`, `research/*/README*`,
  `research/kappa-nine/*`, `research/format-limits-corrected/README.md`,
  `research/five-port-quadratic-decoder/sources/pr446-PROOF.md`, `research/e8-decoder-floors-and-cold14-notes/`,
  `research/leech-lattice/`, `research/niemeier-lattices/`, and PR-title snapshots in `research/*/OPEN-SNAPSHOT.json`.

Scope tags: **[F]** finite search or census, **[E]** exhaustive within a stated model, **[P]** written proof
(not Lean unless stated), **[L]** Lean-checked, **[R]** relaxation or budget screen (not a construction),
**[C]** claim with no result yet.

Note on PR #928: it is **not** the kappa-nine rank-two question. It is rohanarun's "Standardize agent research:
auto-research.md + mirror of research/" PR, with no mathematical content. The rank-two triple-label question is the local
`research/kappa-nine/` package (Douglas Colkitt) together with `docs/research/block-label-feasibility.md`,
`additive-label-obstruction.md` and `small-block-control.md`.

---------------------------------------------------------------------------------------------------------------------

## 0. The frame everything is measured against (key numbers)

- Selected record: #1094 lineage, conditional κ ≈ 0.0016727. Complex primitive ≈ 0.00167546 (binds), bit ≈ 0.00173343.
  Reaching κ > 0.01 needs both primitive savings a > 1/99 (`docs/research/bottleneck-brief.md`).
- **Format ceiling** (`research/format-limits-corrected/README.md`, PR #595 lineage, [P]+checked). Under the "S2"
  axioms (B_K compressed windows, star copies, whole-residual hosting, pressure identity), every supplier has
  a ≤ X(s, w=h/k, x/k), with x = cst/v. On realised E8 units: bit X* = 6.0005e-3 (111 lines, cst 63) and complex
  X* = 5.1863e-3 (112 ports, cst 64), so **κ ≤ 5.16e-3 inside this format**.
  - X depends only on (s, h/k, x/k). Scaling every rank by label rank k changes nothing. **Rank-k labels help only if
    they lower window/k or copy-cost/(v·k).**
  - Scope multipliers (A.7) if a rule is dropped: copy charge → 0 gives ×6.8 (best s) / ×2.8 (s=9). B_K idle frame
    changes free gives ×1.67–2.15. Batching all idle changes of a copy gives ×1.2–1.55. Bridges unsplit gives ×1.15.
    Window one smaller gives ×1.16. Hosting cannot raise the ceiling.
  - Not covered: non-B_K schedules, non-star decoders (β_j < k·w_in), labels outside the cross-field unit, and
    changes to the pressure identity (children of rank above their frame change, a new outer assembly).
- **Coverage-law relaxation** (#1240, #1328, #1606, [R]). Mass = 72W + 64N, one unpaid coordinate per live family,
  halving guard (idle ranks ≤ 51). Any hosting, owner or idle repacking of the #1094 local word gives κ < 0.0016872:
  the packing headroom is < 0.87% (#1240, #1264, #1648, #1620).
  - Thresholds for a ≥ 1/99 (#1328). Unpaid coordinates per family u* ≈ 2.80, **or** ≥ 3093 families per call,
    **or** paid excess spend ≤ 4.9% of the current amount. Changing the centre charge alone is impossible.
    (u=2, c=0) gives a* ≈ 0.00936 < 1/99, while **(u=3, c=64) gives a* ≈ 0.0110 > 1/99**.
  - Port count (#1606). P104 maximizes the ceiling at ×1.054 (κ < 0.0017788). **1/99 needs V ≥ 1328 ports at cst 64.
    No V ≤ 120 reaches it even at cst = 0.**

---------------------------------------------------------------------------------------------------------------------

## 1. Discussion-by-discussion digest

### 1a. Hubs
| # | Title | Content |
|---|---|---|
| 1163 | Start here | Board protocol, plus seed-track result tables (1337isnot1337: P112 d0=76/77 two-sink witnesses COPY 65, P120 shared-total 61,320 trials with zero exact pairs, S4 three dirty roles needing exactly 8 calls (#1734), P112→P104 adapter cst 56 "knob +5.53%" (#1746), recursive echoes saving 112/144 primitives with prefix row-L1 rising 30→42). woklerx's 17 PRs (#1435–#1456) include joint diagonal capacity 99 (rank-six cover) and an 8-call floor for dihedral commutators. bbMisk #1490: static Gaussian-dyadic gauges C_G ≥ (C0+C1)/2 + 4·N_odd. |
| 1166 | Handoffs | Lean PR540 level model ([L]). #1264 queue census: 30 open complex κ claims on 9–11 local words, all capped < 0.0016873. #1212 rank-8 rigidity chain. #1293 a<D/E diagnostic: ceilings ≈0.00168/0.00174, while the screening extremum 0.0137/0.0161 exceeds 1/99, so D/E alone cannot settle the target. #1303 nine-vs-ten primitive gap closes at exactly 10 with any number of dirty donors (2.3M matrices). Four-SWAP at r=4 lies in {8,10,12} (#1705). Rank-one connector cost 10n+4+p_t (#1739). |
| 1167 | Larger κ: proposals | #1240 packing ceiling (<0.87%; excess spend at a=1/99 is 20.4× budget; would need a ~95% cut or a coverage-law change). tomdif helper-basis screen: 10,428 permanent pair conjugations all frame-infeasible, 2,960 temporary ones feasible but with unchanged paid profile. H6 banked E8² (PR606/1590): needs delivered rank ≥ 0.384 per compensation helper, ≤ 80,558 helpers (L=3). The 1.538× "paper ceiling" ratio is E8² Pauli vs E8. Maximooch: at a=0.00169, ≥99.32% of idle mass must sit above rank 48. |
| 1200 | Workflow feedback | Process notes. The only maths content is the #1240 ceiling and a suggestion to group queue claims by local word. |

### 1b. Decoder / unit geometry (complex P112 / P104 / P120 and E8 lines)
| # | Idea tried | Outcome | Scope |
|---|---|---|---|
| 1210 | Masked root-star decoders with trimmed supports N(α), any number of terms, P112 | The hoped-for bound of 64 is **false** for the family. The frame-hit bound is 784/13 ≈ 60.31, so the window [60.31, 64] for masked mixed-β trimmed stars is **open**. Eight best atoms listed as leads (PR1226). | [E] census + [R] |
| 1241 | A8 simplex 9-term decoder (PR1224) with per-root kernel shifts | P120 sharp cost 72 (PR1248). Matching-frame P112 punctures sharp 71 (PR1304, 945 frames). One-pair punctures sharp 71 (PR1612, 1,080 frames). Together these exhaust all 2,025 orthogonal 8-frames. | [E]+[P] |
| 1267 | Nine symmetric co-star-supported terms, masked P112, cst ≤ 63 | 120 maximal co-stars (pairing rank 7). Full-support case impossible. 40,656 four-direction sets survive necessary conditions, but the fixed candidate [0,1,56,87]/(3,2,2,2) is **impossible** (rank-two crown, PR1320). Other assignments are open. | [P] one candidate + [F] gate |
| 1275 | Masked local deformation at 2G on all 1260 P104 frame-pair punctures | Tangent space = diagonal torus only (PR1292). Masking cannot locally deform. Global P104 and nine masked terms are open. | [P] local, exact mod p |
| 1301 | Further trims of β-7 root-star atoms | Deletion thresholds 20/22, support-loss floor 560, first frame-hit change at 4 deletions with cost unchanged (PR1323). | [F]+[P] |
| 1316 | Free odd rectangle mixed with 1–2 original P112 terms (GL(2,C), GL(3,C)) | COPY ≥ 64 throughout (PR1331, 1375, 1432, 1473). An aligned cancellation totals 70. | [P]+[F] |
| 1330 | Rank-six descendants of cost-7 C/N parents | Relaxation copy bill 60 with a 10-term witness, but 21 diagonals uncovered, so it is not a decoder. A 120 s cover search found nothing; no theorem (PR1347). | [E]+[R] |
| 1360 | All 9-term complex factorizations of the single-odd-entry completion K = 2G + λ e_α e_β^T | COPY ≥ 64 and power ≥ 8·8^q (PR1591). Ten or more terms and shared-copy pricing remain open. | [P]+[F] |
| 1384, 1395, 1411 | Global rank-8 gauge rigidity (E-graph model) beyond #1212 | All P111, type-(4,4) and admissible P104 units are rigid (cst ≥ 63/56). P110/P109/P108 rigid (floors 62/61/60). P107/P106 rigid (59/58) and P105 orbits pass (#1568/#1616/#1650). **Only 8 costly terms are covered. Nine or more is open everywhere.** | [P]+DRUP certificates |
| 1434 | One-column free corrections on 52 odd neighbours, GL(3,C) | COPY 64 retained. Lower envelopes (8,8,0), (6,6,6), (6,6,4). | [P]+[F] |
| 1550 | Fixed triple J=(2,4,5) with singleton correction | COPY64 corroborated, otherwise COPY65 (PR1613 covers all 56 triples). | audit |
| 1555 | Rank-5 rectangular cut completion M+K, joint encoding | B(K) ≥ 14 + rank K (sharp, ranks 1–6), PR1600. | [P]+[F] |
| 1570 | 8-term completions of PR1020's 26-line puncture (pair 48,0) | Minimum 62 (prior decoder 69), 256 optimal classes, independently audited (PR1624/1663). Other cost-6 pairs open. | [E] |
| 1581 | Unrestricted two-factor P112 masked decoders | Released: already covered by #1213/#1212/#1292/#1367. | — |
| 1597 | Masked exactness + one root-linear factor ⇒ all-pairs exactness? | Holds through 26 deletions. A 27-deletion 93-port witness breaks it, but its COPY of 72 gives no saving (PR1609). | [F]+[P] |
| 1606 | Port count / puncture depth p=0..24 on #1094 word | See §0: P104 ×1.054. **1/99 needs V ≥ 1328** (PR1619). Break-even table: V=104 needs cst ≤ 57, V=96 needs ≤ 51, V=82 needs ≤ 41. | [R] |
| 1621 | Scope map of complex E8 decoder lower bounds | Separates PR968/1077 eight-term all-pairs floors, PR845 fixed-reader ninth-term exclusion, and the PR1098 support lemma (PR1626). Advises no more search inside those domains. | consolidation |
| 1622 | Overcomplete exact E8 decoders D Tᵀ = 2RRᵀ | Outside-root-code ranks satisfy s+t ≤ m−8 (sharp). Rank-one residual normal form for 10 terms. Real symmetric decoders stay in the code. Complex symmetric decoders reach residual rank min(n−8, ⌊(m−8)/2⌋) (PR1633). **Unrestricted 10-term support/copy-cost search is open.** | [P]+[F] |
| 1636 | Centre-free E8 side shear: drop the 8 rank-8 centre children, y += (I−RRᵀ)x | Local identity passes on 704 roles. A five-call spectral word (eigenvalues 1, −13) composes exactly. **But inherited cover routing fails** (stage/port block [[1,0],[131/144,1]] ≠ required swap), so it was stopped. "Needs a genuinely different global geometry or a paid intertwiner." | [P] local + [E] obstruction |
| 1639 | Uniform P112 odd-column family and nine-mixed terms | COPY64. With nine nonzero projections, sharp 71 (PR1652). | [P]+[F] |
| 1667 | **D16 / D12 spinor paired-Walsh centres** (new binary dimension 16) | D16: 576-centre factor, COPY bill 7,744 → 6,272 (vs 9,216 full), graded square-zero basis 7,734. D12: 1,024 ports, 32 packets of rank 6, cross-packet compensation unresolved. **Full supplier and cross-packet compensation open**, not admitted. | [F] partial |
| 1691 | Batch coding across k independent P112 demands | Minimum charge is exactly 64·rank(C) in the root-code model. A cheaper two-call decoder would need ≥ 17 active terms, an outside-code factor and ≥ 9 rank units saved (necessary, not sufficient). **Open.** | [P]+[F] |
| 1713 | Fitting-matrix (minrank) of the fixed P112 orthogonality graph over char 2 | **Exactly 9 over every char-2 field**, including nonsymmetric matrices (six 8-cliques XOR argument, PR1744). Credits Leung–Mančinska–Matthews–Ozols–Roy (arXiv:1009.1195). New graphs and other characteristics are not covered. | [P] |
| 1728 | Rational basis shears on the 8-term P104 decoder | 392 one-shear and 71,344 two-shear paths give no new cst-56 basis (only inverse moves). Three or more shears open. | [F] |
| 1737 | Row-masked P112 basis switch (A-dual sources on mask S, any A ∈ GL(2,C)) | COPY ≥ 64 and power ≥ 8·8^θ for every pair, A and S (PR1747). **The arbitrary four-ray source case is open.** | [P]+[F] |
| 1516 | Host the 8 centre paths (the 64N term) on idle coordinates | Obstruction for fixed A/B words: paid mass ≥ hosted + 8·rank(scatter), so 64 stay unhosted (#1643/1664/1684). A two-panel fanout sharing centres across two calls gives 416 → 384 actions, a cap of +3.45%, conditional on eligible invocation pairs (#1748). | [P] conditional + [F] |
| 1587 | Where the one unpaid coordinate per family comes from; **plane ports** (rank-2 port labels) | The unpaid coordinate is the port direction q, forced by the line-port contract (U ≤ v(N−d), argued). Plane ports leave 2 unpaid. A naive plane-port centre costs 224/call against a break-even of ≈163.6/call. Greedy E8-style star search reaches only 9 ports, and one family of 112 planes needs ≥ 30 terms. **No lower bound for plane ports. No good plane decoder found.** | [P] argued + [F] greedy |
| 1596 | Partial integer reblocking of rank-1 children into rank-16 blocks; pairwise rank-1→2 fusion | Needs ≥ 363 of 2,412 (reblocking) or ≥ 722 of 1,206 pairs (fusion). Displacement cap 171. Physical realisation open. | [R] |
| 1693 | Fuse consecutive rank-1 climbs into rank-2 | Max disjoint set 674 < 720 needed for +5%. Too small even before physical costs. | [R] |
| 1659 | Joint A/B/early-cleanup gate-frame reassignment (fixed scalar word) | Every legal reassignment keeps a < 0.00169005 (PR1671). LP duals certify optimality for all 0 ≤ a ≤ 1/32 (PR1686). Ideal per-column blocking would be ×1.62, but every pair has an intervening event. | [E]+LP dual |
| 1674 | Nested contraction of 78 helper ends + 5,413 gate frames | Claim only, no result. | [C] |
| 1723 | How many of 12 late block interfaces must escape PR1429's class for a=1/99 | **At least 8 of 12.** Any 5 retained blocks exclude the target. No admitted replacement exists. | [P] conditional + interval replay |
| 1492 | Cross-block rational mixing among 12 late interfaces | Helper-growth minimum 328 + 56·2^s + 28·3^s + 20·4^s retained (PR1517). | [P] |
| 1618 | Cross-call terminal/entrance fusion on R480 | No read-free terminal or entrance child on any of 704 roles. Spectral variant failed (→ #1636). Other boundary topologies untried. | [E] |
| 1265, 1332, 1339, 1265, 1251, 1258, 1269, 1314 | Owner and idle repacking, helper relocations, dyadic gauges, read fusions, slot optima | All within ±5e-7 κ or zero gain. Optimal idle-axis overlay fails 8-stream composition (#1339). | [E]/[F] |
| 1237, 1335, 1362, 1378, 1470, 1289, 1315 | Frame / endpoint rigidity audits | Restricted helper ends forced (#1378). One-gate 4D→6D replacements chronologically infeasible (#1335). Helper 468 forced to rank 8 after cut 177 (#1362). Count/window-only implication is false (#1289). | [E] |

### 1c. Bit-side register models (abelian and non-abelian group algebras), connectors, shears
| # | Model / idea | Outcome | Scope |
|---|---|---|---|
| 1317 | F2[AGL_d(F2)] paid units I+([g]−1)N, free GL_r(F2) mixing; many targets | Cost conjectured = Σ rank[A_i−I | b_i]. Three noncommuting dim-3 targets cost 9 (#1333). GL2 two swaps cost 6 (#1414). UT3 central commutator costs 8 (#1478). Three swaps cost 9 (#1491). GL3 coordinate variants cost 6/8 (#1495/#1496). 27,308 of 28,224 GL3 pairs exact (#1567). diag(a,b,aba) costs 5 (#1696). AGL2 diag(h,h) costs 8. Four swaps lie in {8,10,12} (#1705), and the J²-layer bound is vacuous (J² = J³) (#1755). **In every resolved case minimum = direct bill.** | [E] small r + [P] |
| 1514 | Fourth dirty register for 3 swaps | The compression lemma reduces to 4 registers. 35 patterns UNSAT (DRUP), so 9 is the minimum. | [E] SAT certificates |
| 1715 | Coordinate-CNOT label saturation | Proved. Four swaps need 10 or 12. Balanced 5+5 ten-call existence is open. | [P] |
| 1569, 1599 | F2[UT3(F2)] targets, all registers, nilpotent couplings | Minimum 4w (PR1573). Sharp separate a/b tariffs for all 8 UT3 targets. | [P] |
| 1647 | F2[UT4(F2)] central targets | One target costs exactly 8. Two targets C ∈ {15,16} for every r (14 excluded at r=2 plus a compression lemma). | [P]+[E] |
| 1738 | D8/UT3 central commutator with a third dirty register | No 7-call word (radius-3 meet). 8 stands. | [E] bounded |
| 1740 | F2[S4], four roles, products of transpositions | No 3-call word for 8 targets. Direct 4. | [E] bounded |
| 1727 | F2[AGL2] target diag(h,h⁻¹,t_x,t_y), four labels | Minimum in 8..10 (q=6,7 excluded). | [E] partial |
| 1700 | Two-relation 15-address four-register word | No diagonal singleton endpoint for the ansatz. | [E] ansatz |
| 1594 | Ternary half-integral rank-one frames uvᵀ/2 (338) + quarter-integral (676); arbitrary rational rank-one frames | **9 calls necessary and sufficient** for 3 identical I3 targets in all three alphabets (PR1604, PR1628, PR1679). "Positive follow-ups need to change target equality or collective topology, not enlarge the rational alphabet." | [P]+[E] |
| 1630 | 11 rank-one calls, 4 lower-triangular targets, fixed-weight conic slice | Slice impossible (proof). One-exception amplitude extension UNSAT (Z3). | [P]/[E] |
| 1753 | Common-flag obstruction (PR825) extended to **nonlinear truth-table gates** | s ≥ Wm for common-flag rational frames, any deterministic pointwise gates (PR1757). **Non-common-flag geometry open.** Next experiment: a five-role mixed nonlinear circuit with a non-routable endpoint and a 2-D frame invoice ≤ 9. | [P]+[F] |
| 1381, 1467 | S3 regular-workspace / faithful 2-D S3 output transport | Dirty-echo instruction savings (372→240, 524→404). Boundary cost 36 is minimal. Scalar savings only. | [P]+[F] |
| 1396, 1476, 1503 | Projected cleanup ranges, helper swap/3-cycle costs | Joint range GL(k+q,2) × {[A B;0 I]}. Swap costs 7, 3-cycle costs 13 for all k (Lean row certificates PR1598/1676). | [P]+[L] partial |
| 1544, 1290 | Target feedback in dirty shears (3×3, 4×3, 4×4 K) | **No feedback saving** for all 512 / 4,096 / 65,536 K. | [E] |
| 1507 | J3 shear gate count vs positive growth | Frontier (7,5,5) and (8,4,4). | [E] |
| 1660 | Bidirectional root shears | Four passes needed. Three are impossible for any coefficients. | [P]+[E] |
| 1486, 1412, 1352, 1403, 1504, 1501, 1489, 1539, 1540, 1579, 1694, 1505, 1493 | Connector alphabets (one-way transfers, DUO, TRIO, broadcast readout, mutable sources, sixth-root phases, dyadic outputs) | Five-source universal batch needs exactly 8 transfers (6 excluded over 242M skeletons). DUO: 74→72 root queries at equal adds. TRIO: no gain. Sixth-root phases keep the 14-call minimum. Broadcast common-A: 64→10 A-evaluations, but no supplier exposes it. Mutable-source borrowing gives echo savings. All are local and not admitted. | [E]/[P] |
| 1418, 1565, 1743, 1695, 1687 | Helper-star scalar rewrites, deferred restorations | Coupled shears save 2 ADDs. Deferred restoration cannot be repaired cheaper than keeping it (w+1 / w+3 vs keep). Five-helper cyclic basis saves 12 ADDs. Two-copy scatter saves 120 ADDs. **No paid-profile change** (H2/K still false). | [E]/[P] |
| 1279, 1357, 1462, 1463, 1409, 1634, 1233, 1588, 1202, 1542 | Precision, truncation, carry, Fourier-layout audits | Interval growth is quadratic in log n. Truncation commutes only with phased coordinate selections. Phase-weighted layouts need all phases 1. Three reciprocal guards suffice. And so on. | [P]/[F] |
| 1427 | Nine-stage stage recipes for PR589 idle hosting (K=4, single ±1 bridges) | 2,070,720 recipes, 1,064 idle structures. **None beats #589.** Multi-bridge gaps open. | [E] |

### 1d. Claims with no reported result (as of fetch)
#1674 (nested helper ends + frames), #1730 (#1094 certificate binding), #1635/#1394/#1548/#1527/#1502/#1593/#1585/#1545/#1547/#1448/#1472/#1561/#1515/#1336/#1355/#1356/#1291/#1283/#1260 are audit, verification or Lean bookkeeping. Each is listed with DONE or RELEASED status on the board but is not mechanism work.

---------------------------------------------------------------------------------------------------------------------

## 2. Strongest NEGATIVE results (by reach)

1. **Format ceiling** κ ≤ 5.16e-3 for all B_K / star-copy / whole-residual-hosting words on realised E8 units
   (`research/format-limits-corrected`, [P]+checked). Rank-k scaling invariance means label rank alone cannot help.
2. **Coverage-law ceilings** (#1240, #1328, #1606, #1723). Inside the current local word and coverage law the headroom
   is < 0.87%. Reaching 1/99 needs ≥ 2.8 unpaid coordinates per family, or V ≥ 1328 ports per unit, or ≥ 8 of 12 late
   interfaces outside PR1429's class.
3. **Flag theorem / Theorem G₀ / common-flag** (PR #288, PR825, #1753). W·m − s ≤ Σ(m/2 − rank A), so m=2 never saves,
   also in the non-abelian commutator model and with nonlinear gates. Complex m=2 never saves in GL₄(C). Common-frame
   networks with s ≤ 8 never save. Unitary scalar mixers cannot reduce paid rank (PR836).
4. **Rank-two labels on triples, restricted models** (`docs/research/block-label-feasibility.md`,
   `additive-label-obstruction.md`, `small-block-control.md`, `research/kappa-nine/*`):
   - intersection-only Gram blocks: rank ≥ 2h (48 at h=24)
   - positive-definite ambient: r/k ≥ (z+s)/s (≥ 667/37 at h=24); the whole PD family is below 2^-67 in the old ledger
   - point-additive labels: r ≥ kh (k(h−1) at h=9)
   - coordinate-local planes: impossible
   - char-2 block fitting: rank ≥ vk/h (≥ 169 at h=24, k=2)
   - **any pairwise-commuting label projections: vk ≤ hr** (no gain; noncommuting projections are required)
   - dimension 7l impossible on the full triple graph for h ≥ 9 (Fano clique ⇒ P_T = I/7)
   - S_h-covariant rank-two fails in dimensions 15 and 16
   - S8-covariant standard^k ⊕ trivial^r, 7k+r ≤ 15, impossible
   - unrestricted dimension 15 at h=9: 43 of 146 branch representatives excluded, **103 open**
   - one-regular-block diagnostic: no 18-label partial extends
   - small control: h=8, r=14 exists (7-colouring), but v=56 < 6h(r/k)=336
5. **E8 complex labels with k=2** need r ≥ 18 (PR446 §6.2, SAT), so planes give no gain on the full E8 in-cap graph.
   The h=9 k=1 labelling is unique (= Sussman's J + (G mod 2)).
6. **Lattice/unit screens**. ADE: only E8 is useful (E7 X* ≈ 1.84e-3; A_n, D_n, E6 give x ≥ 1).
   - Leech: Turyn = 64 copies of E8; full shell has centre bill 65,000; 25-bit fit.
   - Niemeier: D24+, E8³, E8² factors; E8² Pauli rank 816, decoder rank 815; native E8 lift κ ≈ 0.00087.
   - BW16 (#895): window c ≥ 72, ceiling 0.649× E8, loses entirely on copy charge.
   - K12 / Coxeter–Todd: 126 lines, w=6, x ≥ 0.714, loses.
   - Gaussian/Eisenstein/Hurwitz E8: minrank = v/w, so x_K = 1 (no gain).
   - Quadratic-affine (stabilizer-state) real and Gaussian labels: 12 full-support centres rejected.
   - Leech 98,280 / 196,560 offset variants rejected.
   - E8 + extra/isotropic vectors dominated by the quotient (Lemma Q).
7. **E8 decoder floors**.
   - 8-term all-pairs: max(72−p, 56) for p ≤ 24, real and complex (PR968/1077/seed44).
   - Rank-8 rigidity on P104–P120 (8 costly terms only).
   - Nine-term families: A8 simplex 72/71, co-star fixed candidate impossible, single-entry completion ≥ 64,
     free rectangles ≥ 64, row-mask switch ≥ 64, nine-mixed 71.
   - Batch coding = 64·rank(C). P112 minrank exactly 9 in char 2.
   - P111 bit decoder: 9-total unique, 8 UNSAT. Theorem C floor = star floor on P120/P111/P112.
8. **Non-abelian register models** (F2[AGL], GL2, GL3, UT3, UT4, S3, S4, D8): every resolved minimum equals the
   direct (separate-label) bill. Rational / ternary / quarter-integral rank-one alphabets keep 9 calls for 3 I3 targets.
9. **Cross-call and boundary fusions**. R480 has no read-free terminal or entrance (#1618). Centre-free side shear
   fails cover routing (#1636). Centre hosting is blocked by the cut-rank bound (#1516). Deferred restorations are
   unrepairable cheaply (#1565/#1743).
10. **Polynomial-method subset families** (`docs/research/subset-core-family.md`, `prime-subset-limits.md`,
    `single-intersection.md` 5,257 cases, `cube-core-family.md`, `signed-sparse-core.md`, kappa-nine geometry screen):
    - all fail positive-deficit or ceiling screens (best kappa-nine subset-core score 1.0000153 at q=4, h=24)
    - five-port quadratic decoder: γ < 125/76433 for every p ≥ 5
    - zeta/Boolean-lattice family (PR172): negative deficit h=3..8
    - PG(2,9) code (PR288): unbalanced

---------------------------------------------------------------------------------------------------------------------

## 3. Answers to the eight questions

### Q1. Rank-k labels (k ≥ 3) on triples; any k ≥ 2; d/k below the split; "PR #928 / kappa-nine rank-two"
- **k = 2 on triples: heavily tried, not closed.** See §2 item 4 (`research/kappa-nine/{ASSESSMENT,
  LOCAL-ELIMINATION,LOCAL-RANK-TEST,MIXED-RANK-TEST,PAIRED-COPY-TEST,ONE-REGULAR-DIAGNOSTIC,NONCOVARIANT-FOLLOWUP}.md`,
  `docs/research/block-label-feasibility.md`, `additive-label-obstruction.md`, `small-block-control.md`).
  - Hypothetical ledger: d=14,15,16 rank-two labels for 560 triples on 16 points give an optimistic moment < 1 at
    a = 1/511 (old PR82 ledger).
  - d=14 is excluded (Fano). Covariant labels are excluded.
  - **Unrestricted d=15 on 9 points is open** (103 branch cases; a Z3 run on 2,436 unknowns / 13,076 equations timed out).
  - d/k = 7 < h is achieved only at h=8 (r=14), which is too small to matter.
  - Arbitrary indefinite rational rank-two at h=24, d=24 is unresolved.
- **k ≥ 3 on triples: no construction or search found** in the repo or discussions. Some general-k formulas exist:
  PD bound r/k ≥ x(h); point-additive r ≥ kh; char-2 rank ≥ vk/h; clique bound k·ω(H) ≤ r (PR446 §5).
  The commuting-projection obstruction (vk ≤ hr) applies for all k.
- **Other k ≥ 2 families tried.**
  - E8 complex planes need r ≥ 18 (no gain).
  - Quadratic-affine Gaussian labels (rank-2 rational from complex lines) are rejected.
  - Plane ports (#1587): naive 224 vs break-even 163.6/call, with no good plane decoder found and no lower bound.
  - Gaussian/Eisenstein/Hurwitz E8 views (k = [K:Q]) give no gain.
  - **Paired cube bit side: ω(H) = p = h/2, so the clique bound allows k=2 at r=h. PR446 explicitly says
    "it says nothing against k = 2 there". Not tested.**
- Coverage-law link (#1328): u=3 unpaid coordinates per family (rank-3 ports) at the current centre charge c=64
  would pass 1/99 in the relaxation (a* ≈ 0.0110). Nobody has priced a rank-3-port decoder.
- "Projective rank" or orthogonal-rank / Lovász-theta language does not appear anywhere. The PD dual certificate in
  block-label-feasibility is effectively a theta-type bound.

### Q2. Generalising E8's J + (Gram mod 2) to larger "zero-or-odd" systems; BW, Leech, K12, Niemeier
- **Tried.**
  - ADE root systems (`e8-decoder-floors-and-cold14-notes/ade_screen.py`): only E8 useful; E7 X* ≈ 1.84e-3.
  - Deeper punctures, sub-root-system units (D8, E7+A1, A8) and mixed units with non-root ports (≥ 14 lines must go,
    best x ≥ 0.67) are all worse (annealing, not exhaustive).
  - Leech (`research/leech-lattice`, PR598).
  - Niemeier (`research/niemeier-lattices`, PR606): 23 rooted systems; D24+, E8³, E8², D16+ with 30,960 ports,
    decoder rank 815; **21 glue-dependent Niemeier constructions still open**.
  - BW16 (PR895): c ∈ [72, 191] (exact c_min open); rank ≤ 14 sub-units not covered.
  - K12 (G34): loses.
  - E8 over Q(i), Q(ω), H: Hurwitz asymmetric decoder open.
  - D12/D16 spinor packets (#1667): open, not admitted.
  - Turyn port labels: arbitrary full-port binary labels open.
- **The specific family "integer vectors, even norms, inner products in {0} ∪ odd" in dims 10/12/16 was not searched
  as such.** With norm 2 this family is just root systems (already screened). Higher-norm odd-inner-product line
  systems (e.g. norm 4 with inner products {0, ±1, ±3}, norm 6 with {0, ±1, ±3, ±5}) and odd unimodular lattices
  (e.g. min vectors of odd lattices in dims 12–16) have no trace in the repo or discussions.
- Binding constraint learnt from BW16/K12/Gaussian:
  - window c must exceed the largest pairwise non-orthogonal clique;
  - x = c·h/v must be about ≤ 0.6;
  - under the coverage law, V ≥ 1328 ports per unit (#1606).
  - Any candidate has to have small non-orthogonal cliques (≈ dimension) and many lines.

### Q3. Smaller corrector span (Theorem B rank < h−1); sparse / non-star decoders of rank ≥ 10 on E8
- Theorem B (PR446): k_a + Σ_j rank C_j ≤ m. The corrector span equals h−1 in **every** family measured (complex
  p=10, 11; paired cube; E8 bit; E8 complex; #425). PR446 states: "a family with a smaller rank and a cheap decoder
  would change the width bound". **No one has constructed or searched for a family with corrector rank < h−1.**
- Non-star decoders on E8: PR717 random walks (cst 63 on P111, 56 on P104) and PR968 theory (7/13 ratio). Ten-term
  structure is #1622. Copy cost below 64 is excluded in many nine-term subfamilies (§2 item 7).
  `e8-decoder-floors` explicitly says decoders differing from B0 off-pattern with **rank ≥ 10 are not covered**.
  The README of format-limits names "a non-star decoder" as open problem 2 (x = 54/102 or 56/104 would give
  X* = 8.25e-3 / 6.80e-3).
- **Open windows:**
  - masked mixed-β trimmed stars in [60.31, 64] (#1210)
  - unrestricted 10-term search (#1622)
  - 17-term outside-code two-call batch decoders (#1691)
  - arbitrary four-ray sources (#1737)
  - nine or more costly terms in the rigidity chain
  - **repeated-label (vector-linear) decoders, which Lemma Q explicitly does not close**

### Q4. Non-abelian (GL / flag / building) frames; mixed characteristic
- **Tried, all negative.**
  - Theorem G₀ (PR288): the flag bound survives the non-abelian commutator model (Sylvester rank functions on
    solvable quotients).
  - Common-flag s ≥ Wm, also for nonlinear gates (PR825, #1753).
  - Unitary mixers excluded (PR836); nonunitary mixers open, needing accumulated negative mass ≥ 1/2.
  - F2[G] register models for AGL_d, GL2, GL3, UT3, UT4, S3, S4 and D8 never beat the direct bill (§1c).
  - Complex m=2 in GL₄(C): never saves.
  - Lemma λ: phase butterflies need √−1 and 2 invertible. A Fermat-ring change gives an identical network.
- **Stated open** (PR288 §3): the full non-abelian bit model at m=2, complex m=3 at W=2 with ≥ 2 insertions and at
  W=3, bit m=3 at small W, non-smooth nonlinear frames. #1753 adds non-common-flag geometry.
- **Not found anywhere:** frames valued in flag varieties or buildings as such, and **mixed-characteristic frames**
  (e.g. Z_2-adic or Z/4 frames mixing the bit and complex sides). Lemma λ and the Gaussian mod (1+i) argument are
  the nearest work.

### Q5. Idle-cost-free schedules; alternatives to B_K; new skeletons
- The B_K family itself was tried: B2 (5-stage), B3 (7-stage, +6.45%, PR373), and B4/9-stage words (#384/#425).
- Nine-stage recipes for idle hosting: 2.07M recipes, no gain (#1427). Cross-call fusion rejected (#1618).
  Two-panel fanout is conditional (+3.45% cap, #1516).
- format-limits A.7: free B_K idle changes would be worth ×1.67–2.15. It calls the schedule/ρ family **"the only
  untested spec freedom with a ceiling term ≥ ×1.15"**, and notes "one bank pair per invocation is a convention".
  `complex-frame-pair-decoders/CLAIM.md` passed over non-B_K schedules because legality "is not modelable without new
  spec work".
- Design-free helper floors certify only 48% (bit 212/439) and 22% (complex 107/496) of helper counts, so "new
  skeletons" is open problem 4.
- **No discussion attempts a non-B_K schedule** (several active bank pairs per stage, or a different ρ).

### Q6. Polynomial-method families other than triples
- **Tried:**
  - k-subsets with k=2q−1, j=q−1, Lucas central factor (subset cores, q ∈ {2..32}, h ≤ 64)
  - prime-power version over F_p (`prime-subset-limits.md`: centre cannot shrink, partial-output roles too many)
  - all k-subsets with single intersection j (5,257 cases)
  - binary cube with Hamming distance q
  - signed q-sparse vectors (dot product ≡ 0 mod q via the (1+z) polynomial factor)
  - quadratic-phase affine (stabilizer) vectors, real and Gaussian
  - Reed–Muller-type enlarged quadratic polynomial codes
  - Leech cubic kernel (t³−4t)/48, which uses a cubic polynomial in the inner product instead of mod 2
  - five-port quadratic Gram 2(j−1)(j−3)
  - Wilson rank formula for global proper stars (`research/paired-star-rank`)
  - zeta / Boolean lattice
  - PG(2,9)
- **Not found:**
  - **q-analog / Grassmann families** (k-subspaces of F_q^n with dim-intersection conditions, polynomial in q-binomials)
  - **labels that are vectors over F_q for odd q** with an F_q-valued centre and a rational fitting form
    (the prime-subset screen is the closest but stays with subsets)
  - higher-degree polynomial kernels f(⟨x,y⟩) for lattice shells other than the Leech cubic

### Q7. Complex-side (F2-label) units with k ≥ 2, or isotropic / degenerate structures
- **Tried:**
  - E8 complex k=2: r ≥ 18 (UNSAT for r ≤ 17), so no gain.
  - Lemma Q: degenerate (radical) units are dominated by the quotient. Checked on E8 + weight-2 isotropic
    decorations (ρ = 1, 2, 3: worse) and the paired-cube p=3 toy, which is the only one gain (cst 18 → 16) and needs
    a degenerate span.
  - F4-Hermitian / Eisenstein labels: the trace form is alternating, so there are no odd-norm residuals and the
    phase calculus fails.
  - Gaussian labels reduce to F2, so nothing is gained.
  - Complex-compression: alternating binary residuals lack an orthonormal basis.
  - Kappa-nine: mod-2 reduction of even-weight signed vectors is isotropic.
  - Complex parity frames (seed35): 720 rectangles need dimension 2 or 4, not 3.
  - Lemma λ consequences.
- **Not found:**
  - complex-side k ≥ 2 on families other than E8, e.g. the paired cube complex side, where ω = 8, 8, 12, 12 for
    p = 4..7 against h = 2p
  - a modified phase calculus that tolerates alternating residuals (e.g. using F4 with a different kernel interface)
  - Lemma Q's out-of-scope repeated-label class

### Q8. Explicitly open / "next experiment" items with no taker (as of the fetch)
- Unrestricted rational rank-two triple labels, d=15 on 9 points: 103 branch cases (kappa-nine). d=15, 16 on 16 points.
- Paired cube bit side, k=2 at r=h (PR446 §5).
- Plane-port decoder below 163.6/call, and any lower bound for it (#1587). Rank-3 ports (#1328 u=3).
- Corrector rank < h−1 family (PR446 §10). Repeated-label vector-linear decoders (Lemma Q scope).
- Unrestricted 10-term E8 decoders (#1622). 17-term outside-code batch decoders (#1691). Masked trimmed stars in
  [60.31, 64] (#1210, eight leads in RESULTS.json). Nine or more costly terms in the rigidity chain. Four-ray sources
  (#1737). Three or more P104 shears (#1728). Other cost-6 pairs at the 26-line puncture (#1570).
- 21 glue-dependent Niemeier lattices. BW16 exact c_min ∈ [72, 191] and rank ≤ 14 sub-units. Hurwitz asymmetric
  decoder. Arbitrary full-port Turyn labels. Open lead on #617 integer packing (+1.1e-7 κ).
- D12 and D16 spinor cross-packet compensation (#1667).
- Non-B_K schedules and the ρ freedom (format-limits). Per-word enablers (descents or gauges hoisted out of the local
  word, worth 1/72 of the per-call price). New skeletons (52% / 78% of helpers unexplained).
- Non-common-flag nonlinear five-role circuit with invoice ≤ 9 (#1753). Full non-abelian bit model at m=2. Complex m=3
  W=2 with ≥ 2 insertions, and W=3 (PR288). Nonunitary mixers with negative mass ≥ 1/2 (PR836).
- Shared-centre two-panel fanout needing eligible invocation pairs (#1516). Broadcast readout interface (#1694).
- A different global geometry or paid intertwiner for the centre-free spectral word (#1636).
- Balanced ten-call four-SWAP (#1715/#1755). UT4 two-target 15 vs 16 (#1647). AGL2 q=8, 9 (#1727).
  916 unresolved GL3 pairs (#1567).
- At least 8 of 12 late interfaces must change class for 1/99 (#1723): no admitted replacement.

---------------------------------------------------------------------------------------------------------------------

## 4. Ranked list of promising directions that appear UNTRIED

Ranking criterion: escapes a proved ceiling's hypotheses, has an explicit favourable budget somewhere in the record,
and has no prior attempt.

1. **Rank-3 (or rank-k) port labels with a decoder cost that does not scale with k.**
   - #1328 shows u=3 unpaid coordinates per family at c=64 passes 1/99 in the relaxation.
   - #1587 tested only plane ports, naively.
   - Q1-type triple labels with k ≥ 3, or paired-cube k=2 at r=h, are the natural first geometry.
   - The format ceiling's k-invariance means the decoder/window per unit k must shrink. So the decisive first test
     is a clique/minrank bound for the chosen in-cap graph (k·ω ≤ r) before any circuit work.
2. **Corrector rank < h−1 (Theorem B escape).** Every measured family sits exactly at h−1. A port family whose
   drop-free correctors span a proper subspace of q^⊥ directly lowers the width m ≥ 1 + s·rank(C). No one has searched
   for one. Small exact search over line systems in dims 8–12 is feasible.
3. **Non-B_K schedules and the ρ freedom.** These are the only untested spec freedom worth ≥ ×1.15. Free idle changes
   are worth ×1.67–2.15. Needs a spec model of legality first: several active bank pairs per stage, or a different ρ.
4. **Repeated-label (vector-linear) decoders.** Lemma Q explicitly leaves these out. All the E8 decoder floors assume
   scalar-linear decoding.
5. **Zero-or-odd line systems beyond root systems** (norm ≥ 4, odd inner products), and odd unimodular lattices in
   dims 10–16 as units. Screen with the format ceiling: need the largest non-orthogonal clique to be about the
   dimension, x = c·h/v ≲ 0.6, and (coverage law) V ≫ 120.
6. **Grassmann / q-analog and odd-q vector label families** (polynomial method over F_q), never screened. The subset
   and prime-subset analogues fail mainly on role counts. q-analogs change the intersection spectrum and the
   centre factor.
7. **Mixed-characteristic frames** (Z/4, 2-adic or Fermat-ring frames shared by the bit and complex sides). Lemma λ
   shows a ring change alone is neutral. A frame model that lets one paid change serve both sides has not been
   formulated.
8. **Per-word enablers.** A descent or gauge hoisted out of the 72/288 replicated local words, priced at 1/72 of the
   per-call cost. Named as open problem 1 in format-limits, with no attempt in the discussions.
9. Lower-priority but explicitly open and cheap:
   - unrestricted d=15 rank-two triples (103 cases; a well-specified exact search)
   - masked trimmed-star window [60.31, 64] (#1210 leads)
   - 21 glue-dependent Niemeier lattices
   - BW16 rank ≤ 14 sub-units
   - Hurwitz asymmetric decoder
