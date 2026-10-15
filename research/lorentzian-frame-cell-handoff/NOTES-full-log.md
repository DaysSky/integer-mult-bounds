# Low-helper complex word — notes (session 2026-10-14)

## Environment
- Repo: /home/user/integer-mult-bounds, local `main` = upstream/main bce54fb3 (fork main was stale). Not pushed.
- All 1340 upstream PR heads fetched as refs/upstream-pr/N. Corpus + search: scratchpad/prs/{corpus.json,own.json,search.py}
  (own.json = first-occurrence dedup; `python3 search.py -c 'regex' -w 400 'regex2' -m 590`).
- api.github.com blocked (403); PR bodies not available, but PR research READMEs are in the corpus.

## Prior art checked (no duplicate found)
- #717 format-limits-2: F4 twin substitution 0/73 helpers deletable; F2 tight-frames wall; F6 no reuse; S1 in-place dead;
  P4: cutting k helpers (width back to 48-bins) b9: k=234 2.41e-3, 300 2.78e-3, 480 4.79e-3; B3R SSS 8-helper word
  (frame-ILLEGAL: all regs end FULL, ignores target end frame perp(port)).
- #1240/#1272 (Colkitt): packing ceiling tool `ceiling(local,73,896,9,64)`; levers centre-free 2.80x, rank-16 2.31x, etc.
- No upstream frame-legal low-helper complex construction; no numerical helper deletion on complex words.

## Ceiling screen (#1240 model, ideal packing)
| profile | x vs selected | kappa cap |
| selected (492 h) | 1.00 | 0.001687 |
| 224 h unit | 1.18 | 0.001998 |
| 168 h unit | 1.33 | 0.002249 |
| 112 h unit | 1.53 | 0.002572 |
| 112 h rank-2 | 1.77 | 0.002975 |
| 0 h unit | 2.14 | 0.003608 |

## Algebra (verified numerically)
- Use FULL-WORD ports/root_lines (gauge44-frames-x/evidence/local/FULL-WORD.json.gz); U U^T = J+G mod 2.
- Drop-free demand N = I - G/2 = I - R R^T/4 ; G/2 = 14 P (rank 8). Support = 5824 legal pairs (p_s.p_t=0) = root-odd pairs.
- Each source: 52 readers = 6 pencils x 8 cross + 4 within-tetrad.
- PENCIL pi=(pair {i,j}, sign sigma): 12 lines = 3 tetrads x 4 (class) = 6 HALVES of 2 lines. Pencil = K_{2^6}, legal iff
  different halves, N constant after orientation. Halves of pencil: lines z_a, z_a+w; w = f_i+f_j (7 distinct w's, each
  shared by 8 pencils); z's orthonormal, w isotropic & orthogonal to all. Any k halves span k+1 dims.
- Half = root-orthogonal pair in a tetrad (2 sign flips); 168 halves, each in 2 pencils; each line has 3 halves.
  Common readers of a half = 20 (10 per pencil). Cross-tetrad legal pairs in exactly 1 pencil; within-tetrad in 3.
- F = span(f_m) 4-dim isotropic; tetrads = 14 cosets of F; f_m = (1,v_m), tetrads = affine planes of AG(3,2).

## Crossing lemma per level d (events = register climbs crossing dim d-1 -> d)
- N = sum_e alpha_e beta_e^T, supp beta spans <= d-1 dims, supp alpha spans <= 9-d dims (legal automatic).
- Per-pencil min constant blocks (cross exact, within optional): L3=6, L4=3 (class->co-class), L5=5 (<=4 INFEASIBLE,
  proven), L6=3, ... pencil-aligned counts L3 336, L4 168, L5 280, L6 168, L7 336.
- Level 2: each source needs 2 events (best hyperplane sections 32+20; 3 complement dirs give 32, 3 half dirs give 20).
- Level 3: singles max 20 readers; PAIR blocks (legal pairs s,s') up to 16 common readers rank-1 (area 32 = cap).
  Exact partition with only 16-pairs + 20-singles: INFEASIBLE. Min level-3 count between ~224 and 336.
- Max rank-1 blocks at level 5: 6x6 (= 3 halves | 3 halves inside one pencil).
- Handoff's bottom (Y-pairs + X_s + H_s at complement frame) is an exact level-3 decomposition: 56*40+112*32 = 5824.
- "Rank-7 meeting" blocker reproduced: forced only if L4 uses the tight 3-block class->co-class shape; L4 has slack.

## Structural constraints found
- Once frame chains are fixed, content/responsibility supports are automatic; design = chains + same-frame mixing.
- Level-synchronous ordering is WLOG (gates sharing a register ordered by frame dim).
- Centres: tau_{T,k} needs all 8 lines of a tetrad -> frame span(T) (dead for drop-free: no target legal to all of T).
  Cheapest factory guess ~4 receivers/tetrad (~56 helpers) + 8 carriers. Canonical word: 42 sources at dim 8 after A,
  B carried by helpers (Y<-H 786, Y<-X 126), Y<-Y 112 gates all at dim 7.
- Bottom needs y->y fan-out (targets as distributors), top needs x->x fan-in, if helpers are few.

## Tools (scratchpad/hf)
- geo.py (F2 helpers, load canonical word), e8.py (P, Rr, N, LEG, TET, PEN, halves_of), sym.py (symmetry group:
  1344 perms x 2^8 signs, linear on labels, N-equivariant), framenet.py (level-synchronous net + matrix-free CG ALS),
  pencil5.py / pencil5b.py (per-pencil ILPs), lev3.py / lev3ilp.py, portspans.pkl (port-spanned subspaces dims 1-5).
- canon_fn.py: ALS validation on canonical word chains (slow; residual 7.0 -> 2.5 after 6 sweeps from random).

## Session findings (cont.)
- Level 5: exact 4 general rank-1 terms per pencil (shapes A0+C|A1+B, A1+C|A0+B, A0+B|A1+C, A1+B|A0+C).
  Cross-exact forces designated-class within = (1/u+1/v, 1/(1-u)+1/(1-v)); both =1 iff u^2-u+1=0 (6th root of unity).
  Real symmetric within contributions c achievable iff c<=0 or c>=4. 4-shape covers of a pencil: 18.
- Pencil radical V_pi^perp = {0, w, x_i, x_j}: x_m = label of deleted frame line 2e_m; p_t.x_m = [m not in T_t];
  centre frames cf_m = x_m^perp. Pencil-aligned level-2 frame <p_s,x_m> covers 28 readers (3 pencils).
- Level 3: every legal source pair has 3 maximal 16-target rank-1 blocks (pencils through pivot coord avoiding flip coord);
  b-frame forced = <p_s,p_u,x_pivot>. Within-tetrad legal pairs: K_{4,4} per tetrad, 168 pair events cover all cross
  (pivot 3-cycle scheme), +112 within singles = 280.
- Halves: 16 cross common readers span 6 but N rank 2 (two pencils orient oppositely).
- COUPLING/DUPLICATION: x-directions entering frames at level 3/4 cap level-5 S-side to 3 dims; x-free bottom needs
  half/2-half/3-half frames. Invertible mixing preserves content rank -> duplicated contents need fresh registers.
  Non-targets may not read targets -> all duplication feeding the middle is by sources/helpers.
  Estimate for pencil-pipeline designs: ~224 source copies + ~168-224 pencil duplications ~ 400-450 helpers (~canonical).
- Centre via target levels: dead (reading graph connected; B101/B106 in #717). Decoder D1 hole (mixed beta, n>=9, P112)
  still open upstream; #968 frame-pair decoders + #1071/#1125 delivery obstructions on punctures.
- Unit screens all lose to E8: ADE #620, Leech #598, Niemeier #606, BW16 #895, extension rings #620.

## Session (cont., 2026-10-14 late): framework-level scan
- Format ceiling X(s,h,k=1,x) best-s (skel.X): h=9 x=.57 5.2e-3; h=4 x=.3 4.75e-2; h=3 x=.3 6.7e-2; h=2 x=0 0.21.
  Small windows would be huge but x<1 needs mixed fields; single-field units have x>=1 (Hadamard; known: #634/Jain).
- "J+B mod 2" units (even norms, pairwise products 0 or odd): v <= h(2^h-1)/(2^{h/2}-1) (Lagrangian count);
  h=8 bound 136 (E8 has 120), h=10 330, h=12 780. Hub: Lorentzian I_{11,1}/I_{13,1} (#620/#634) lose after helpers.
- Eisenstein E8 (40 K-lines, k=2, w=4): F2 minrank 10 (my SAT; matches #620). #620 CP-SAT best decoder 40.
  My cost-pattern SAT (3x10, 3x12, 4+2x10) and budget SAT (r=12, <=39) found nothing in ~30 min; symmetric
  (N(Syl5), order 20) flat-pair linear model optimum = 40. Linear F2 ansatz J + sum u^perp x w^perp: inconsistent.
  Symmetry group of the 40 lines: order 25920 (PSp4(3)); generated by order-3 complex reflections (eis/eisgroup.py).
- Twins for E8 complex ports (same root, new F2 label sharing the 8 totals): none (perp spans all of F2^9).
- Network coding: the saving IS a coding/flow gap (#634 note 2, known). Li-Li refuted Oct 2026 (dysfunctor 33-vertex
  gap 150/149; Braverman-He F9 PG(2,9) flow<=147/157; Zhang-Li-Li reversible circuits). arXiv blocked here.
  New observation: frames give LP dual certificate F* <= s/m. With all-rank-1 edges at frame dim m = demand hop
  distance, bill = (1/g) m^a => a < ln g / ln m. dysfunctor would give 0.0042 IF it were a reversible all-roles wire
  circuit with exact frames -- but it is a general network code (unbalanced vertices H, G, C absorb info), and
  converting to a reversible circuit adds scratch roles (carriers = helpers). Fresh zero temporaries don't help:
  scratch roles break even in the s-vs-Wm ledger, temporaries are pure cost.
- Topology test (exact undirected fractional MCF, scratchpad/flow): 3-stage swap with direct reads + J+B centres:
  D4 (W=39) and D5 (W=58) routable (F*=W) -> no frames can save. Paper triple motif h=5 routable (both groupings).
- Schedules: with bridges confined to worlds (X-world/Y-world) and decoder calls = rank-1 cross-world updates,
  a swap of 2K families needs >= 2K decoder calls (off-diagonal rank K each way); B_K's 2K+1 is near-optimal.
  Fan-out calls (one combo -> several target banks) are still rank 1: no escape from ~1 centre charge per family.
- E8 over O = Z[(1+sqrt-7)/2] (A = (I+C)/2, C = Paley skew conference matrix of order 8; preserves E8): 120 K-lines
  (only +-r per line), k=2, w=4, 21 K-orthogonal lines per line. Max non-orth clique >= 24, F2 fitting minrank >= 26
  (v/w = 30): extension-view pattern "minrank ~ v/w" (#620) holds again -> dead. (scratchpad/k7)
- Duality: a rational "0-or-odd" configuration (v vectors, Q-rank d, F2 fitting minrank mr) gives the bit unit
  (window d, mr totals of cost <= d) and the complex unit (labels (r mod 2, 1), window mr, d totals of cost <= mr).
  Both have x ~ d*mr/v. E8: 120/(8*9). Lagrangian bound v <= p(2^h-1)/(2^{h/2}-1) (p = positive index).
  II_{9,1} local search (small/medium vectors): 152-160 lines at d=10 (worse than E8). Hub: I_{11,1}, I_{13,1}.
- Subset-minrank LP (generalizing #798's clique LP) and symmetric budget SAT runs: in progress (eis/lpb.py,
  eis/symbudget.py). Symmetric (cyclic) decoders found so far: none below 40.

## Session (2026-10-14, after "keep looking for architectural breakthroughs")
- Re-read #288 (paradigm negative results), #907, #446 (Thms A/B/C), #928 kappa-nine (rank-two on triple graph),
  #1240/#1348 (coverage law: D = u*w - c per call; thresholds u>=2.80 or F>=3093 for 1/99), PR386 nine-stage geometry.
- Lattice-cut fact: in subspace-label frames, per X/Y session saving <= distance - |grade change| = 2k; helpers are
  0->F monotone (no saving). So saving/pair is capped by label rank k; everything else is overhead (helpers, drops).
- Format ceiling with label rank k (skel.X, R-free): (h=8,k=2,x=0.6) 0.0475; (8,2,1.0) 0.0214; (8,2,1.2) 0.0115;
  (8,2,1.5) 0.0045; (8,3,1.0) 0.070; (12,3,1.0) 0.043; E8 refs 0.00516/0.00519. k=2 at h=8 beats E8 iff x <~ 1.45.
- k=2 E8 2-frames (pairs of orthogonal roots; 3780 frames; mod-2 lines are isotropic lines of O+(8,2) through
  2 nonsingular + 1 singular point; class of rho=a+b <-> one of 135 norm-4 frames, 28 coordinate planes each):
  * symmetric sum-vector decoder J + Omega(rho): v <= 36 (spread of 135 singular pts into 9 t.s. solids, <=4
    orthogonal frames per solid) -> x >= 72/36 = 2 = k: zero saving. Local search hits 36 exactly.
  * asymmetric pointer decoders B = J + omega(psi_T, phi_S), psi,phi in the frame (rank <= 9): local search (34020
    vertices) also stuck at 36.
  * product/split families die on shared components (same-line ports need B=0).
  * whole family with J+Omega(rho): ~1793 pattern violations per frame. Dead.
  -> consistent with #288 "k-dim labels need degree>=3 indicators". Scripts: scratchpad/k2/.

## Full non-abelian flag model (bit primitive) — #288 open item 3, no follow-ups in corpus
- Model: free = lower Borel B- of GL_2m (controlled shifts D+=KH, lower-tri Levi), paid = upper unipotents
  (H+=MD, cost rank). Frames up to free moves = chambers of the spherical building X = B-\GL_2m(F_q)
  (q = address radix, free odd prime). Cost of a move = c(delta(x,y)), delta = Weyl distance in S_2m; rank-1
  upper unipotents have delta = a transposition; c(w) = reflection length = 2m - #cycles(w) (conjectured, fits).
  Session condition (free entry/exit ops included): delta(src, snk) = w_T = (1,m+1)(2,m+2)...(m,2m) (block swap).
  Abelian shear model = big cell. Minimal factorizations of w_T = orderings of its m transpositions.
- Local compatibility (neighbours of a chamber pairwise at Weyl distance w_T), m=2: q=2 -> 2, q=3 -> 3 (both match
  #288), q=5 -> 5 (new). Abelian cap is m. So the "<= m compatible directions" obstruction to isometric
  Tanner-code embeddings disappears for large radix q. Scripts: scratchpad/flag/{bld,compat,compat2}.py.
- Payload field is free for the bit primitive (any field; algebraic solutions reduce mod p at constant volume
  overhead), so F_9-linear codes (Braverman-He) are admissible payloads. BH's graph G (PG(2,9) minus 175
  edges, sessions at distance 5, 735 vs 785) would need an isometric embedding into the m=5 flag building
  (GL_10(F_q)) with edges at reflection length 1 and sessions at Weyl distance w_T; if it existed and the 9
  zero-in/garbage-out temporaries are charged, bill ~ 735 (1/5)^{1-a}/157 -> a ~ 0.041 (24x today).
  #288 1.4(d) only excluded the ABELIAN M_5(Q) embedding.
- Small-m register searches (this session): complex abelian m=3 W=3 s=8 random sequences (238 det-passing)
  -> residual stuck at sqrt(3); bit configs with "any 6 frames span I" filter: none generated. Not conclusive.
- q=7 confirms compat(q)=q (2,3,5,7). The q-cliques consist of neighbours of the longest transposition type
  (H1<->D2), pairwise at w_T: thickness realises "(14)+(14)=w_T", impossible in an apartment/abelian chart.
- BH graph at m=2 in the flag model (any chamber assignment is a valid common-frame network for BH's F9 code
  + 9 zero-in/garbage-out temporaries; cost = sum of reflection lengths, sessions need delta=w_T):
  * metric LP bound = 294 exactly (uniform 0.4/edge; lambda* = 147/157); bar to save = W*m = 314.
  * m=1 analogue = integral multicut: heuristic min 166 = 157 data + 9 temporaries (>= 157, consistent with
    the abelian flag theorem). Product (two GL2 blocks) optimum = 2*166 = 332.
  * GL4(F3) building annealing (4 runs, 8e6 steps, cluster moves): best 332 every time.
  * Gr(2,4)(F3) relaxation (provable lower bound: building cost >= Grassmann projection cost, sessions
    transversal): best 332 every time (4 seeds).
  -> no evidence the building beats the product on BH's graph at m=2; this route looks dead at m=2.
    m=5 isometric embedding (735 vs 785) remains untested (hard CSP in GL10 building).
  Scripts: scratchpad/bh/{bhgraph,sa,sa2,lp,multicut,mc_sa,gr24}.py, scratchpad/flag/{table,actions}.py.

## Representation (p-integral) obstruction, any frame group (incl. full flag model)
- Map the formal identity through the natural 2m-dim rep rho over a field K containing the payload F.
  Free ops (B-, mixing) preserve the subspace F^W (x) D; a rank-r paid op moves it by <= r; the target
  diag(T)Pi moves it by W*m.  Hence: if every frame is defined over (a ring reducing to) the payload field,
  s >= W*m — abelian or not.  Savings REQUIRE frames non-integral at char(payload) (E8: 1/4 vs F2; triples 1/2).
  (Known in hub as the "p-integral theorem" per #288 credits.)  Consequence: same-characteristic flag SATs
  (F2 frames, F2 payload) are vacuous; the meaningful relaxation is frames over F_q (radix q odd), payload F2.
- Every hub lower-bound tool for the bit side goes through abelian/solvable quotients (characters, Sylvester
  rank on solvable group rings). The full flag model generates SL_4 (perfect): those tools vanish. Open.
- Mixed-char SAT (frames F3 = 2080 flags, 16 free gens, 68 paid transvections; payload F2):
  controls W=1 S=1 UNSAT, W=1 S=2 SAT, W=2 S=4 L=2 SAT (169 s). Running W=2 S=3 (L=2; and swap/any-register L=3).
  (Same-char F2/F2: W=2 S=3 rounds=1 UNSAT — vacuous by the obstruction.)
- Idea (untested): quantitative 2-adic-depth bound on savings; would say whether deeper denominators help.
- Gr(2,4) relaxation (free = parabolic P, target = transversal planes; valid necessary condition):
  F3 frames / F2 payload: W=2 S=3 L=2 UNSAT (43 s); L=3 timed out at 900 s (rerun 6000 s in progress), L=4 running.
  F2 frames / F3 payload (also mixed char): controls pass; W=2 S=3 L=3 running.
  (Earlier I misread an interleaved "SAT 0.7" from a control as a positive — it was NOT.)
- Flag-level F3/F2: W=2 S=3 L=2 UNSAT (54 s); deeper runs killed (Gr relaxation subsumes them).
- Agent C (k>=2 families): none beat E8; unfolding lemma (k-dim unit = k=1 unit on kv lines with decoder
  B (x) J_k, same window & cost, x1=x/k); clique bound h/k >= omega(supp B) kills E8 k-folds; Lovasz-theta bound
  (definite forms) h/k >= theta(Z(B)) ~ 0.75n for triples -> #928's n=16 rank-two case needs d>=25 unless the form
  is indefinite.  Remaining k=2 target: #928 triples n=16, d in [15,24], indefinite (ideal X* 1.3e-2..2.9e-2),
  but triples' helper load (z=234 at n=16) is the real obstacle.  Scripts: scratchpad/agentC/.
- Building + q-clique centre idea: all ports one step from a common chamber => single-gate network => routing,
  no saving; the decoder/coding structure is still required.

## Decoder row sparsity / corrector span (this session, continued)
- Row-sparsity SAT (k2/sparsedec.py, E8 P120, rank c, per-row off-diagonal cap k): c=9: k<=62 UNSAT (k=63 SAT) —
  consistent with the corpus uniqueness of the rank-9 decoder (J+Gbar, every orthogonal pair a corrector).
- Why it matters: #446 Theorem B gives m >= k + sum_j rk C_j (C_j = span of drop-free correctors = orthogonal
  lines with B_TS=1). The format premise (Win) sets the climb a = corrector rank = h-1 = 7 for every known family;
  #446 flags "a family with smaller corrector rank and a cheap decoder" as open. corr/ceil_a.py (float skel with a
  decoupled): at x=0.6, a=7 -> 5.16e-3, a=6 6.06e-3, a=5 7.32e-3, a=4 9.21e-3, a=3 1.36e-2, a=2 2.37e-2; but x=0.8
  kills it (a=7: 1.32e-3).  So the target is small corrector span AND star cost x <= ~0.6.
- corr/corrsat.py: E8 decoder with each target's correctors inside one chosen subspace W_T from a menu
  (E6-type: 28 per line, d=6; D5: 378, d=5; D4: 315, d=4; A3: 1260, d=3).  E6, rank 10: UNSAT (193 s).
  Constructive attempts B0 + Delta (Delta kills correctors outside W_T) need rank ~9+10r (r = #classes of normals),
  i.e. x >> 1: corrector restriction multiplies rank.  Expectation: costly; SAT ranks 12/14 running.
- PRUNED (user request) with these states: flag-model Gr(2,4)(F3) W=2 S=3 L=3 and L=4 undecided after ~30 CPU-min
  each; E6-menu corrector SAT rank 12/14 undecided; row-cap c=12 k=36 undecided; agents B/D/E stopped
  (D: AGL(4,2)-equivariant d=24 rank-two triples, best orbit residual 9.67, not converged).
- Complex P112 frame decoder: corrector candidates 52 per target, span dim 8, F2 form rank 8 (cxcorr.py).
- Isotropic corrector spans do not shrink the window: C_j ∩ W_j' = 0 and C_j ⊥ W_j' for later stages (W_j'
  nondegenerate), so the target frame accumulates ~sum dim C_j; the lever is corrector DIMENSION, not form rank.
- Idle-free ceiling (E8 bit, x=63/111): 1.004e-2 at s=7 vs 6.0e-3 — idle removal is worth only 1.67x; active
  climbs (a = h-k) dominate.  Big gains need small w = h/k with x/k < 1, i.e. new k>=2 units.
- Ceiling landscape (corr/land.py, k-scaled skel, best s): beat E8 (6.0e-3) needs w=h/k=4 with x/k<=0.7, w=2 with
  x/k<=0.8; 10x needs w=2,x/k~0.45 or w=3,x/k~0.3.
- Complex P112 as a k=2 unit (pair F2-orthogonal lines into ports): the complex frame decoder is the signed Gram
  (B = 2G on live lines, 8 signed totals), rows never constant on a pair, so no B(x)J_2 form; a port-level decoder
  needs B_PQ=0 unless all 4 line pairs are Q-non-orthogonal (~3 of 56 ports per port) -> near-diagonal, x/k ~ 1. Dead,
  same mechanism as agent C's theta bound: full orthogonality of k-dim labels is too rare in E8 geometry.

## Odd-or-zero line systems (J+Gbar decoder of rank <= w+1) — this session
- Clique LP bound: v <= w(2^{w/2}+1) for classes over symplectic F2^w; x >= (w+1)/(2^{w/2}+1) (w=8: 0.53, E8 0.60).
- Search (oddz/clique.py, {0,+-1,+-2} vectors, norms 4/8): w=8 finds E8 (120, x=0.6) only; w=10 best 122 lines
  (F2 rank 8, x 0.74); w=12 best 132 (x 1.0). E8^2 norm-4 lines avoiding +-2 (oddz/e8sq.py): only ~74 lines (x~3.7).
  -> realizability, not the F2 counting, caps the family at E8.  (Niemeier pkg: full E8^2 needs mod-4 decoder rank 815.)
- Rank-k triple labels: VM bundle (scratchpad/vm-bundle.tar.gz) runs rank-2/3 continuation from split, AGL(1,16)/AGL(4,2)
  equivariant b=2,3,4, odd-or-zero w=10/12.  Local equivariant runs stopped by user (VM covers them).
- Local rank-2 AGL(4,2) gap run before stop: d=25..29 no convergence (best orbit-res 1.0).
- kappa-nine's recommended (never executed) experiment, n=9 rank-two labels at d=15: 853 random restarts of ALS(400)+LM(80)
  (n9d15/restarts.py, 2 seeds x 600 s): no hit, best residual 3.685, every restart floors near 3.7-3.8 -> strong
  numerical evidence of infeasibility (plus agent D's PSL(2,8)/AGL(2,3) equivariant failures at 15). Not a proof.
- Extension rings (Gauss/Eisenstein/Hurwitz E8, K12): closed by #620 (minrank = v/w in every view -> x_K = 1).

## Discussion digest (agent, scratchpad/discussions_digest.md) -> untried leads; tested this session
- Paired-cube bit family (transversal triples of p pairs, h=2p, v=8C(p,3), parity decoder c=2p): PR446 §5 says the clique
  bound allows rank-two labels at r=h ("says nothing against k=2"); untested in the hub.  pcube/pc.py, pc_cont.py:
  * p=4: rank-two at r=8=h found instantly (res 1.7e-15) — but there Q=I-J/9 is definite and x/k = 8*8/64 = 1 (no value).
  * p=5 (r=10..18 random restarts: best 8.9/7.2/1.1/0.67) and p=6,7 at r=h: no solution.  Descent from split
    (r=4p) stalls at once: p=5 20->19 res 2.5 (drop and reduce modes), p=6 24->23 res 4.0.
  * Value if it had worked (hub skel, w=r/2, x/k=c r/(2v)): p=11 r=42 7.0e-3, r=36 9.5e-3, r=22 2.1e-2; p=10 r=30 1.1e-2.
  -> NOT CONCLUDED (user: test all cases). Only a few cells were tried locally. Full grid in VM bundle 2
     (scratchpad/vm-bundle2.tar.gz): p=5..11, b=2,3,4, every r in [bp, 2bp-1], random + descent + B_p-equivariant.
     B_p-equivariant control: p=4 split d=16 found (5 configs); p=4 d=8 non-equivariant solution is not B_4-symmetric.

## Network-coding lens (this session, late)
- Every hub word with s < Wm is an undirected multiple-unicast network with coding gap Wm/s (frame ranks = routing
  lower bound by the triangle inequality).  dysfunctor's 33-vertex Li-Li counterexample (149 vs 150) was extracted
  from the upstream XOR-swap bit network (cells + row/column parities; saving = cells - rows - cols; carriers = helpers).
- Zhang-Li-Li arXiv 2610.09367 (7 Oct 2026): reversible circuit, all registers demands, bank exchange up to sign,
  workspace restored, temporal metric sum = N(M+1) (= hub's s=Wm break-even); gap via +2 control-port penalties;
  BGS tensor amplification -> polylog gaps.  Afshani-Freksen-Kamma-Larsen (ICALP'19) Omega(n log n) for multiplication
  circuits was CONDITIONAL on Li-Li -> premise now false.  Hub corpus cites neither.
- Exponent of a seed: a ~ ln(gap)/ln(m) (all rank-1 edges) -- same form as BGS amplification exponent.
- Braverman-He (gap 785/735 at distance 5 -> a~0.04 if frame-realizable): abelian real embedding fails (residual 11.5),
  real Grassmann m=3,4,5 edge/session conflict, F2 Grassmann anneal 2141 edges (need <785), causal greedy fails.
  Garbage: its 9 C/J temporaries end dirty (PR288 "unbalanced").  Garbage-free variant would need |B| = dim W >= 166.
- ZLL metric as frames: time = common flag (break-even); penalty block reduces to an m=2 problem -> flag theorem kills
  the block-diagonal realisation.  Non-block open.
- Room: flag theorem with rank-1 edges allows s >= 2W (savings up to 1-2/m); cut bound in Bil_2(3x3) with translation
  sessions allows 1024 vs routing 1536.  So no known bound blocks big per-level gains; the barrier is constructive.
- Translation-invariant abelian model (frames F_3^{3x3}, payload F_2, r register types, block moves): exact
  character-identity search (galg/mitm.py): r=1 control recovers routing; r=2 with 4 or 5 moves (d=3 offsets): NO
  solution (routing 6 is optimal there).  d=4 running.  Consistent with hub's "F2[G] register models never beat direct bill".
- Translation-invariant model, r=2, d=4 basis offsets, 5 moves: no solution (routing optimal for r=2, d<=4).
- E8^2 bit decoder (Niemeier pkg: mod-4 decoder rank 815, x=0.42, ceiling 7.18e-3 > E8 6.0e-3):
  lower bound: greedy pairwise non-orthogonal set 273 lines.  Ceiling if rank were 450: 1.27e-2, 273: 1.54e-2.
  All 8 W(E8)xW(E8)-invariant decoders on the 28800 root-pair lines (e8sq/bbrank.py, exact F2 rank via vec-trick
  images): (1,1,1)=mod-4 decoder rank 782; (1,0,1) 1998; the other six >= 4000.  -> no better symmetric decoder;
  non-invariant decoders in [273, 782] remain open (hard minrank).
- Grid-swap count (dysfunctor): n x n grid gap ~ 1 + 1/(10n); carriers (side info) cost ~n per cell vs O(1) saving;
  3-direction bulk variant also ~1 + 2/(15n).  Same trade-off as decoder rank c >= v/(2z+1) vs helper load z.
- 33-vertex dysfunctor network (my transcription, dysemb/net33.py: 33 v, 91 e, cap 149, 30 msgs, need 150): abelian frame
  embedding m=5 fails (best residual 2.75 over 200 restarts; m=4 2.04; m=3 0.48 but m=3 cannot save since Wm=90<149);
  real Grassmann m=5: edges satisfiable only with degenerate sessions (min sv 1e-7) -> not frame-realizable (numerical).
  Conclusion: coding-gap networks built without frames do not embed; need frame-NATIVE designs.
- Frame-native candidate: dual polar graph DSp(6,2) (Lagrangians of F_2^6; isometric in Grassmann J_2(6,3); m=3;
  135 v, deg 14, 945 e).  Flow vs cut (dualpolar/dp.py): all opposite pairs flow 0.0729 exact, best cut 0.125 (ratio
  <=1.71); random opposite matchings (67 sessions) flow ~4.5, best cut ~6.1-6.3 (ratio <=1.34-1.39).  Cut > flow, so
  coding gains are not excluded by cuts on a frame-native graph.  Next: construct codes (BH-style global algebraic codes).

## Unit screens beyond lattices / Lorentzian odd-or-zero (this session, after compaction)
- Framing: a unit is (labels: char-0 Gram, window h) x (decoder: F2, rank c) with B_TS != 0 => labels orthogonal;
  same pair gives a complex unit with roles swapped (labels = F2 Gram, decoder = char-0 Gram).  x = cst/v, cst = sum of
  gathered spans (<= c*h).  Hub helper model (#620 est_model.py, calibrated): even LP-level x at h=10..16 gives only
  a ~ 2.5-3.4e-3 at rho = 3-4 helpers/port (1.4-1.9x E8); small h + small x would be worth more (h=4 x=.5 rho 4: 5.7e-3).
- Small configurations, exact SAT minrank (smallh/screen.py): {0,+-1}^3 (13 lines), {0,+-1}^4 (40), {0,+-1,+-2}^3 (49),
  indefinite {0,+-1}^3 (1,1,-1), {0,+-1}^4 (1,1,1,-1) and (1,1,-1,-1), F4 (24), B4, B3: every one has minrank >= v/h
  (x_proxy >= 1).  No small-window unit found.
- Lorentzian II_{9,1} = E8+U odd-or-zero sets (lor2/): LP bound 330 lines (h=10, c<=11).  Tabu/greedy max-clique over
  23,882 norm+-2 lines finds 165 = the I_{10,1} triples+pairs family (inner products 0,+-1 only), x = 110/165; larger
  pool (88,686 lines incl. norm +-6) found less (search weakness, not a bound).
- Exact S_n-invariant odd-or-zero systems in w^perp of I_{n,1} (lor3/orbits.py, entries |x_i|<=2, |y|<=3, norms
  +-2,+-4,+-6): n=10: 165; n=11: 220; n=12: 298 = 220 triples + 66 pairs + 12 norm-6 vectors (-1^11,2;-3) [window 12,
  c<=13, x ~ 0.48-0.52]; n=13: 364; n=14: 455.  These are the hub's I_{n,1} family (+12 at n=12), x ~ 6/(n+1).
  Gap to the LP bound x >= (h+1)/(2^{h/2}+1) grows with h; closing it is worth <= ~1.3-1.5x in the helper model.
- Decoupled "abstract class" units (quad/): S subset of F2^{2m} with symplectic w, decoder P = J + w|_S (rank <= 2m+1),
  labels = any char-0 orthogonal representation of {w(a,b)=0}.  LP: |S| <= h(2^m+1).  Numerical (LM, quad/orthrep.py):
  O+(8,2) nonsingular (120) at h=8 = E8 (control, instant); O-(6,2) (36) and O+(6,2) (28) at h=6 realizable (x>1);
  O-(8,2) nonsingular (136): best residual^2 = 114 - 6h for h=8..12 (4 seeds each) -> needs h ~ 19, x ~ 1.26. Not useful.
- Rigid extension of the I_{10,1} 165-system by abstract classes (lor2/extend.py): 176 lines in R^{9,1} (rational),
  window 10, rank_F2(P) = 11, 0 violations (independent check): x_proxy 0.625 (vs 0.667).  Flexible LM growth from 176
  (quad/flexgrow2.py) found no further class in ~25 min.  Greedy growth from scratch at m=4,h=8 stalls at 65 (E8=120): weak.
- Symmetric single-invocation F2 swap (x += x+y, y += x+y is one transvection over F2): analysed as a non-B_K schedule
  (the #595 census's only untested >=x1.15 freedom).  It decomposes into two simultaneous standard invocations (U-unit,
  V-unit, U perp V) plus self-terms; per register saving k, copy x, but each register's frame must absorb both its
  cross correctors and its self correctors -> climb ~ (h_U - 1) + (h_V - 1) per register in one stage, the same as B_K's
  two active stages of a.  No gain found at the accounting level (not a proof; centre restoration from the swapped bank
  works because y' = x_orig).
- Port-subset SAT for h=3 (smallh/subsat.py) was stopped at its time limit with no result recorded (output lost to a
  buffered pipe); not concluded.
- Exact subgroup-invariant odd-or-zero search in w^perp of I_{n,1} (lor3/orbits2.py; Young subgroups; entries |x|<=2,
  |y|<=3, norms +-2..+-6; networkx exact max-weight clique on orbits): n=10 -> 165 under S10, S9xS1, S8xS2, S7xS3,
  S6xS4, S5xS5 (several distinct 165-systems); n=11 -> 220 (S10xS1, S9xS2, S6xS5); n=12 -> 298 (5 subgroups).
  => with small coordinates the lattice optimum is the hub's I_{n,1} family (+12 at n=12).
- Abstract (non-lattice) rigid extension (lor3/extend2.py, verify_ext.py, 0 violations): n=10: 165 -> 176 (every base),
  n=11: 220 -> 231 (window 11, decoder rank 11, x = 110/231 = 0.476, skel 8.20e-3 > hub I_{11,1} 7.17e-3),
  n=12: 298 -> 299.  Helper model (#620 est_model, rho=4): 231-unit 1.57e-3 bit / 1.78e-3 cx vs E8 1.79e-3 / 2.03e-3:
  still loses at equal helpers per port.  Only near the h=10 LP bound (330, x=1/3) would Lorentzian clearly win (2.46e-3).
- 4-subsets of an 11-set (330 = LP bound, F2^10 = even subsets, w = |A cap B| mod 2): not representable at h=10
  (LM residual 15.6, 2 seeds).
- n=10 exact symmetric search with larger coordinates (|x|<=3, |y|<=5, norms to +-10) under S10, S9xS1, S8xS2, S5xS5:
  165.  Smaller groups (|x|<=2,|y|<=3): S4xS3xS3, S3^3xS1, S2^5 (650 self-compatible orbits), S4xS4xS2: 165.
- Two negative directions, w = (1^n; t,t) in I_{n,2} (lor3/orbits3.py, self-compat fixed for indefinite y-part):
  S_n-invariant maxima 46-73 lines at windows 10-12.  Dead.
- I_{n,1} family skel ceiling (cst = n(n-1)): peaks 9.18e-3 at n=16 (x=0.353); with the +n abstract extension 9.43e-3
  at n=15.  i.e. <= ~1.57x E8's 6.0e-3 helper-free, and the hub's helper model (window-penalised) puts all of them
  at or below E8.  Lorentzian lattice units are therefore helper-limited, not unit-limited.
- Near-exhaustive n=10 run: S2^4xS1^2 (5190 orbits, 1396 self-compatible, 621,897 edges, exact clique 291 s): 165.
  S2^3xS1^4 and S2^2xS1^6 hit their 3400 s per-case limit (no result); the |x|<=3,|y|<=5 S2^5 case was cut off by the
  2-hour background limit before finishing.  Not concluded for those three; not restarted (limit already maximal).

## Helper floors at the top level (this session; scratchpad/helpers/, hf/cxtop.py)
- CORRECTION: exact label/functional decoder costs (lor3/costs.py) show the abstract extensions do NOT improve x:
  n=10 165->176: bit x .600->.625; n=11 220->231: bit .500->.524 (complex .550->.571, binary window 12);
  n=12 298->299: .520->.522.  Earlier "231 at x=0.476" used an invalid proxy.  Best Lorentzian bit unit = hub I_{11,1}.
- Helper model (#620 est_model): Lorentzian needs fewer helpers than E8 to tie: I_{11,1} bit <= 2.66-3.34/port,
  complex (exact window 12, x .55) <= 2.40-2.98/port, vs E8 shipped 3.95 (bit) / 4.43 (complex).
  At E8's own x: rho 3.95->2 is +39% bit; climbing in rank-4 pieces instead of rank 1-2 is +19%.
- E8 bit top structure (classes.py): the 180 needed top contents K_{ax} (one per cell) are 16-line sums = 8 cells
  (one per block outside a's pair), each split 4+4 over exactly 2 quads; each cell lies in 8 K's; F2 rank of the
  180 K's is 38.  Hyperplane sections of t^perp: 8821 (5040/2016/1008/666/63/28 of 10/13/16/21/30/36 lines);
  shareable only D6 (2 targets) and E6 (3 targets).  No 2 sections cover E7 minus an E6 (27 lines).
- LEVEL-6 REGISTER FLOOR (argued): a register whose content spans a full 6-dim section needs a merge partner at that
  flat; every register crosses level 6 once.  Enumerating all covers (topcover.py): with one shared level-6 read the
  only valid cover is the D6 triple -> per target >= 1 (needer+partner shared by 2) + 2 x 1.5 (2 dedicated + partner
  per cross D6) = 4 registers -> >= 480 registers -> E8 bit helpers >= 360 (shipped 439).  Option B (level-6 read
  inside a 5-dim flat, no partner): no 2-section cover exists (topcover5.py, 3000 largest 5-flats).
  => E8 bit is within ~20% of its top floor: helper lever on the bit side <= ~+15-20% (model).
- Complex P112 analogue (hf/cxtop.py): readers 52, sections 255 per target; best cover: F7 shared by 2 + 1 dedicated
  shared by 2 -> 2.5 registers/target -> >= 280 at level 7 -> helpers >= ~168 (shipped 496).  Big slack, but kappa =
  min(bit, complex) and complex is only 3.5% below bit, so complex helper savings are bit-capped.
- Why: bit labels are char-0 and E8's reader sets (E7) are indecomposable -> cover 3 at both ends; complex labels are
  binary (cover 2).  For root-type units cover 2 <=> s^perp cap L decomposable (D_n: A1+D_{n-2}, x=1).  Low x with
  cover 2 in char 0 is the open question that decides whether the helper lever can exceed ~+20% kappa.

## Lorentzian re-check: cover numbers and break-even helper density (this session; scratchpad/lorcov, lor4, lor5)
- topcover5 (E8 bit, option B, level-6 read inside a 5-flat): EXHAUSTIVE over all 36,435 5-dim flats: no cover. (closes
  the "3000 largest" caveat.)
- Lorentzian I_{n,1} (w=(1^n;3)) lines = A_{n-1} roots e_i-e_j + triples e_i+e_j+e_k+f; n=9 is E8 (control).
- Cover numbers, exact (lorcov/cover2q.py: quadratic-form kernel K over Q, rank mod 2 primes; lorcov/linecover.py: bitset
  exhaustive over line pairs/triples), all 19 saved lattice systems (n=10: 11 Young-group variants, n=11: 3, n=12: 5):
    any-frame model (hub #595 D1: b = <u_s, w>, w arbitrary): n=10,11 roots cover 2 (dim K = 1), triples >= 3 (K = 0);
      n=12 (298, with norm-6 lines): all >= 3.  E8 control: all K = 0 (cover 3), matches #595 D1.
    closed (port-spanned) frames, source end (b = <s,u>, u a line): cover 3 for EVERY line at n=10,11 (like E8);
      n=12 norm-6 lines > 3.
    abstract extensions 176/231/299: all >= 3 (the extra classes break the roots' decomposition).
  => #595 D1 sink floor (c-1)v - v/leftover: Lorentzian any-frame ~1.75/port (n=11) vs E8 1.91/port; closed frames ~2/port
     both.  No structural helper advantage; floors do not bind anyway (E8 shipped 3.5-3.95/port).
- Odd-or-zero planes: lines in the same mod-2 class are pairwise orthogonal, so a plane holds <= 8 lines even when
  indefinite (definite: <= 4, B2).  Section sharing stays O(1); no Lorentzian-only sharing lever.
- Other w = (1^n; t), t = 0,1,2,4 (lor4/sweep.sh, S_n and S_{n-1}xS_1, |x|<=2, |y|<=3, norms +-2,4,6): max systems are
  D_n-sized (t=1: n(n-1); t=0,2: <= 272 at n=18; t=4 n=17,18: 136/153).  Evaluated in lor4/eval.log.

## Exact bit pricer, generic in (h, v, R, local histogram) (scratchpad/price/pricer.py)
- Reproduces the published nine-stage bit prices EXACTLY (all printed digits): P111 0.001733052823330162099157,
  R420 0.001653826988146798944268, from their local histograms: global profile = 288 x local + idle remainders;
  idle slots per port copy = skel.idle_slots(K, a=h-1) x 2 copies; width-h helper residuals hosted whole (greedy by
  per-residual saving == exact DP on both controls); root of sum z r/(mW)(m/r)^q + 32 m (sum z) m^q/(1e16 W) = 1.
- Exact ideal-profile bound (one move per register): I11,1 at rho 3.95 = 2.21e-3, E8 2.61e-3; every ideal row beats
  P111 up to the hosting wall R = 4v -> the bound excludes nothing; fragmentation decides.
- Exact scenario prices (each register's climb split in k even moves; E8 control: k=4 scenario 1.7266e-3 vs real
  P111 1.7331e-3):  I11,1 beats P111 iff R <= 730 (k=3, 3.32/port), 633 (k=4, 2.88), 565 (k=5), 523 (k=6);
  I13,1: 1179 (k=3, 3.24/port), 1020 (k=4, 2.80), 920 (k=5), 838 (k=6).
  Hub #620 s4 sketch (unbuilt middle): 732-787 helpers -> a built word with <= 3 moves/register at <= 730 would beat
  P111 exactly.  The question is constructive.
- Construction facts (lword/): decoder U U^T = J + G mod 2 (centres), totals at {x_i = y} flats, 90 lines rank 10
  each, cst 110 exact.  20,790 good 4-frames (hub count reproduced).  d-line corrections cannot all be folded into
  cell needers (per frame: triangle parity system, no solution) -> >= 1 d-line read per target.  Cell needers:
  each can be read in-chain by one target and consumed by the other -> >= 2 needer registers per port (440) in the
  cell architecture.  Needer flats = sums of blocks over the frame's outside set (A(Out), Trip(Out), cones over a
  support point, fans), all blocks in rank-6 flats.
- Exact I11,1 price grid (x1e-3; P111 1.733053): R=451: k2 2.352 k3 2.133 k4 2.001 k5 1.904 k6 1.844 k7 1.796;
  R=633: 2.057/1.854/1.734/1.646; R=732: 1.925/1.731/1.616/1.533; R=787: 1.859/1.669/1.557/1.477.
  Argued top floor (same model as E8's >= 480 registers): Lorentzian >= 880 registers -> R >= 660 -> needs about
  <= 3-3.5 moves per register to beat P111 (P111 itself makes 4.40 per register).

## ARCHITECTURAL: general nondegenerate frames give the paper's Lorentzian triple family cover 2 (exact)
- upstream/build/sections/03-motifs.tex: "A label is a nondegenerate subspace of a fixed bilinear space"; the paper's
  own bit network is the triple family T_100 with form I - J/9 (eigenvalue -91/9: Lorentzian), and its gate labels are
  non-port-spanned subspaces ((B (x) F) perp (P (x) t^perp)).  The hub's bitE8 format restricts frames to closed
  port masks (xcheck: "every frame closed in the live labels") -- a format convention, not a theory requirement.
  NEW CONSTRAINT for indefinite forms: every frame must be NONDEGENERATE (automatic for E8, not for Lorentzian).
- Exact covers of T_h readers (|T cap T'| = 1):  port-spanned (line) cover 3 for h = 10, 11, 12 (linecover.py);
  any-hyperplane cover 2 (quadratic kernel dim K = h, h = 10, 11).  trip/ndcover.py, exact rational: two
  NONDEGENERATE hyperplanes of s^perp cover R(s) for h = 10, 12, 13, 14, 15, 16 (H1 = s^perp cap {x_a=0}, complement
  det 1 + 2/(9-h); H2 >= span(G_a), complement det 4).  h = 11: H1 degenerate (det 0) for this split.
  E8: no quadric vanishes on E7 (K = 0) -> cover 3 under ANY frames; general frames do nothing for E8.
- So with paper-legal general frames, T_h (h != 11) has cover 2 at both ends: design-free carrier floor ~1/port
  (hub #595 D1 sink formula (c-1)v - v/leftover) instead of ~2/port.
- Exact break-even vs P111 (validated pricer; k even moves per register):  T_14 (v364, x .5): k3 R<=647 (1.78/port),
  k4 525 (1.44);  T_15 (v455, x .462): k3 859 (1.89), k4 708 (1.56);  T_16 (v560, x .429): k3 1077 (1.92), k4 888
  (1.59);  T_18: k3 1.85, k4 1.52.  At 1 helper/port, k4: T_15 1.936e-3, T_16 1.947e-3 (+12% over P111).
  => potential bit-supplier improvement IF a T_h word with general frames lands within ~0.6-0.9/port of its floor.
- Total frames C_i = span{t_T : T ∋ i}: rank h-1, Gram det 4 (nondegenerate) for h = 12..16 (exact) -> x = 6/(h-2)
  stands with legal frames.
- Exact price at the cover-2 sink-only floor R = v - floor(v/C(h-3,2)) (~0.99/port), vs P111:
  T_15: k3 2.0548e-3 (+18.6%), k4 1.9417e-3 (+12.0%), k5 (+7.3%);  T_16: k3 2.0670e-3 (+19.3%), k4 (+12.7%), k5 (+7.9%).
- Paper's original T_h network: one side wire per (source, reader) pair (z_b = 3 C(97,2) per port at h = 100):
  helper-bound by design.  The open problem: a T_h word with general frames within ~0.6-0.9/port of its floor.

## Building a T_h word (session 2026-10-15; scratchpad/tword/)
- Kit: space.py (exact rational subspaces, form I - J/9, nondegeneracy, perp), tfam.py, gword.py (general-frame word
  builder: nested climbs, nondegenerate frames, D/A/scatter/B/C, histogram), gcheck.py (independent exact checker:
  own rational algebra; nondegeneracy of every frame, nesting, content-in-frame for z registers and for every register
  read by a target, F2 replay of all columns, H1-H5, rank-mass identity, exact price via price/pricer.py).
- Pipeline validation: naive.py T_10 (centre totals at C_i, one copy per (target, reader) = the paper's side wires):
  PASS, R = 7930 (66/port), cst 90, x .75, 24,020 moves; beyond the hosting wall (unpriceable), as expected.
- Exact top-level facts for T_h (T_10, T_12; top3.py): every cover of R(S) by line-perp sections uses 3 sections each
  shared by exactly 2 targets (no A2 planes: <S,S'> = 1 gives S - S' = e_c - e_d, not a line); no parity covers.
- STRUCTURAL: content reaches two targets only through a frame inside both perps, i.e. inside a line-perp section.
  A target's in-chain reads all lie in ONE section (its chain is nested).  With line-perp cover 3, every target needs
  >= 2 further registers entering its dedicated zone (rigorous given the cover).  So the general-frame cover 2 helps
  only the SOURCE end (2 branches instead of 3); the TOP stays E8-like.  Rigorous floor still R >= v; realistic
  merge accounting (2 registers per section that must deliver a section-spanning sum, 1.5 v sections) gives ~3v
  non-target registers, R ~ 2v.  Exact price T_16 at R = 2v + h: E8-like paths 1.6925e-3 (-2.3%), coarse +9.1%,
  fine -5.6%.  => borderline: needs asymmetric section pieces (no wasted merge partners) AND a middle that is almost
  free (time-multiplexed onto the 2v top registers) AND paths at least E8-coarse.  Not excluded, not shown.

## CORRECTION + exact room (session 2026-10-15)
- The general-frame "cover 2" for T_h does NOT lower the register floor.  Frame-independent line-mixing cut: along any
  path carrying x_s to a target, frames are nested; the first frame holding a second line t_s' confines all later
  targets to R(s) cap R(s'); exit registers carry x_s alone (one source each); a target reads at most one source at a
  single-line frame.  => non-target registers >= 3v - floor(v/leftover) when the line cover is 3 (floor/leftover.py;
  E8 control reproduces the hub's 52/63, leftover 11, sink floor exactly).
- Exact floors: T_10 220 (1.83v), T_12 413, T_14 692 (1.90v), T_16 1074 (1.92v), I_{11,1} 426 (1.94v, leftover 15),
  I_{13,1} 706 (1.94v, leftover 16), E8 230 (v=120).
- Room = exact break-even (vs P111, even-split k moves) - floor: I_{10,1} +.18/-.15v; I_{11,1} +1.38v (k3) / +0.94v (k4);
  I_{12,1} +.77/+.38; I_{13,1} +1.30/+.86; I_{14,1} +.80/+.41; I_{15,1} ~+1.05/+.64; I_{16,1} +.61/+.24; I_{17,1} +.70/+.32;
  T_14 < 0; T_16 ~ 0 under the even-split k>=3 model (NOT ruled out: words with fewer moves per register, or a different pricing shape, are untested).  E8 best words: 1.58v (R420), 2.05v (P111) above floor.
- 4-subsets of [11] (LP-bound 330): 14 pairwise-orthogonal AG(3,2) planes on 8 points => window >= 14 (clique bound; scoped to that unit family).
- Remaining Lorentzian path: an I_{11,1} (or I_{13,1}) word with middle <= 0.9-1.3v (E8 R420 middle = 1 empty
  register per cell = 1.5v), i.e. R <= 633 (k4) / 730 (k3).  Note: coordinate flats on 9 points are degenerate
  (null w_S) -> not legal frames.
- SCOPE RULE (user, 2026-10-15): nothing above is "ruled out" unless every case is excluded.  Break-even rows use the
  even-split k-move scenario model; floors are exact lower bounds; neither excludes a family by itself.

## Top-level (section) bound and the E8 vs I11,1 comparison (session 2026-10-15; scratchpad/lean, price/arr.py)
- Every 3-section cover of an I11,1 reader set is a good 4-frame (P targets: 252 PPTT; T targets: 336 TTTT + 84 PPTT)
  or, for T targets only, a PPP triple (420).  Mutual partner graphs cannot use PPP: each P has exactly one
  inside-T and one disjoint-T partner, so the 55 PPT-type T targets use all 55 disjoint edges (counting).  55 P's
  (odd) => at least one non-mutual section.
- Private sets (lines of a section in no other section of the target) span the section's line flat for every PPTT
  and TTTT section except PPTT's TT section (24 lines, rank 8 of 9; its flat W has W-perp lines = {T,T'} only, so it
  is section-specific anyway).  Both targets of a frame section have the same private set.
- Lemma (forced projection): at a flat, outputs = invertible image of inputs; inputs come from proper sub-flats.
  If two outputs must carry the same spanning forced set, the flat needs an extra register.  Consequence per section:
  2 arrivals give ONE shared register (pre-read by one target, terminal for the other; the other arrival dead), two
  distinct tops need 3 arrivals.  With one pre-read per target: registers >= 3S - v (S sections).
  I11,1: S = 330 -> non-target registers >= 770, R >= 550 (2.5v).  E8: S = 180 -> R >= 300 (= hub #493 bound).
- Exact scenario prices vs arrivals/section a (R = S a - v): at equal a and k, E8 beats I11,1 by ~5-6 points:
  a=2.33 (top bound): E8 k4 ~ +12%, I11,1 k4 ~ +6.6% over P111.  a=3 (R420-type middle): E8 k4 -4.4% (real R420 -4.6%),
  I11,1 k4 -9.1%.  Middle waste allowed above the top bound to tie P111 at k4: E8 ~0.7v, I11,1 ~0.38v; R420 wastes
  1.0v (cell layer: 3 registers per cell, hub bound for 3 branches/source on the D4 partition).
- => no Lorentzian pricing advantage at equal architecture (scoped: even-split scenario model, frame-type tops).
  The open lever for BOTH families is the middle network (cell layer).  Not ruled out: an I11,1 word with middle
  waste <= 0.38v (k4) / <= 0.82v (k3).

## E8 middle-network structure (session 2026-10-15; scratchpad/e8lean)
- R420 partition, one D6 in coordinates: d-cell = pair (2,5), B-perp = D4 on {0,1,3,4}, E-set = {0,1,3,4}x{2,5}
  (16 lines); the 8 E-cells pair a j=2 line with a j=5 line of a different i (e.g. (0,2)+ with (1,5)+).
- Intrinsic 2-flat covers of E(H): 3 of type (D4,D4) [one = R420's quads, max sharing 6 = proven max: a quad's perp
  D4 holds at most 6 design cells], (D5,D5) through B-perp (each D5 in exactly 3 design D6s, ALL needing the same 8
  forced E-lines -> forced coincidence), (D4,D5), (A3,D5) and private ones.  (D5,D5) feeding needs single lines
  instead of cell sums but its coincidence waste brings the count back to 540 (360 arrivals + 120 D5 leftovers + 60
  flex-only diagonal thirds).
- Transposition asymmetry: transpose maps sources<->targets, frames<->perps, keeps R and the histogram, but the
  interface allows mutable SOURCES (sources can arrive at D6s as needers) while targets may never feed z registers.
  Source-side (cell) bound: helpers >= 3*#cells - v when every cell sends its sum to two quads (rank 2 -> third
  register).  R420 meets it exactly (14 helpers per 4-frame = 8 carriers + 6 empties).  The top bound (3S - v
  non-target registers, R >= 300) is slack in R420 only by the source registers it reuses.  => R < 420 needs a
  source side without cells feeding two quads (and, by the transpose picture, a matching top).
- E8 4-covers of R(t) by rank-5 flats exist (no 3-covers); ALL are (D5,D5,D5,A5): perps = three A3s through t
  meeting pairwise only in t, plus Z = t x A2 (t is always the A1 factor => the A5 is single-user).  Multiplicity
  57 lines x1, 6 lines x3.  No 4-cover by D5s alone.  5040 covers per target.
- Cost model (needer flats): registers >= sum over flats of max(#terminal users, dim span(needers)) + assembly
  leftovers (a single spanning needer needs 2 arrivals).  Sections: 2 per section with one pre-reader, 3 with none.
  4-cover design: about 4 registers per target (R ~ 360) only if the 6-user D5 nodes have needer dependencies that
  let pre-readers ride free; otherwise 5 (R ~ 480).  Hypothetical rank-3 -> rank-5 direct design at R = 360 with
  branch moves {1,2,2,2,1}: exact price 1.86135e-3 (+7.4% over P111, +12.6% over R420) -- the payoff if realizable.
- EXHAUSTIVE (E8, t-perp): every 3-cover of R(t) by flats of rank <= 6 is a D6 frame triple (315 covers); no E6 or
  single-user flat appears.  4-covers by rank-5 flats are only (D5,D5,D5,A5), A5 single-user.  No 4-cover by D5s.
- Cost model per cover organisation: helpers >= sum_t k_t - v + L (k_t = cover size, L = assembly leftovers at
  single-user / identical-content flats; pre-reads and free source participations limited to one per port).
  Frames: 3v - v + 1.5v = 3.5v.  E8 4-covers: 4v - v + v = 4v.  => among single-level cover organisations frames are
  cheapest; the source side (transpose, no help from targets: H1) gives R >= 3.5v = 420 for E8 (R420 tight) and
  R >= 770 for I11,1 (frames, 330 cells).
- Exact scenario prices I11,1 vs P111: R=550 k3 +13.8% k4 +6.5% k5 +1.3%; R=660 k3 +4.9% k4 -1.9%; R=770 k3 -2.6%
  k4 -9.1%.  So frame-organised I11,1 words lose to P111 at >= 3 even moves per register (scoped: section/cell
  organisation, scenario pricing).  Remaining in-framework avenue: 4-section covers with leftover-free shared flats
  (best case 3v = 660, borderline: needs <= ~3.5 moves).  NOT ruled out outside this framework.
- Side observation: P111 (punctured, v=111, R=439) sits ~28-37 helpers above a punctured-frame estimate (153 cells
  x3 + 27 punctured cells x2 - 111 sources (+9 totals) = 402-411): a punctured-native skeleton could be worth ~+2%
  bit c (estimate, unbuilt).
- 4-SECTION COVERS (both families, exhaustive): E8 has 382,089 4-covers of R(t) by line-perp sections; the most common
  types use E6 sections (A2 partner, 3 users) and D6 sections, with ALL private sets small (1-8 lines) and PROPER
  (non-spanning), e.g. (D6:3, E6:4, E6:4, E6:4).  I11,1: T(012) 1,892,286 and P(01) 1,287,436 4-covers by sections,
  the common types all-proper with 71/85-line A2 sections (3 users) and private sets of 3-16 lines.
  => proper private sets remove the forced section-level leftover; A2 cells on the source side (3 sources, rank 3)
  can fan out without empties.  Cost of a leftover-free 4-section organisation: helpers >= 4v - v = 3v
  (E8 360, I11,1 660), vs frames 3.5v.  Scenario prices at 3v: E8 R=360 k4 ~ +3.5% (k5 ~ 0%), I11,1 R=660 k3 +4.9%,
  k4 -1.9%.  E8 still prices better at equal architecture.  Unbuilt; rank/consistency conditions not yet checked.

## E8 4-section word build (session 2026-10-15, scratchpad/sec4)
- design2.py: Z15-invariant self-dual 4-plane design WITH cross-orthogonality (every (t,s), s in R(t), has design planes
  P ∋ s, Q ∋ t, P ⊥ Q, and a D4 between): FOUND (design.json; v1 kept as design_v1.json).  quadstat: all 120 covers valid,
  private sizes pair 3 / A2 4.  Structure (blocks.py, secblocks.py): the 10 'full' D4s form a D4 partition (5 complementary
  pairs); all 120 A2 planes lie inside blocks (12 of 16 A2s per block, each line in 3); the 60 pair planes join t in B to
  u in B'.  A2 section Q ⊂ B: Q-perp = B' (12) + one design A2 cell in each of the 8 other blocks (960/960).  Pair section
  {t,u}: t's 3 frame-mates (private) + u's 3 mates + an A2 plane in each other block (6 design cells, 2 not).
- Register accounting (corrected): mutable sources (relaxed checker) => 480 registers = x_s + 3 copies per line; R = 360
  with zero middle waste; route.py's model (|P| out per cell, |Q| in per section) is that architecture.
- route.py (Z15, D4 quads only, one hop, distinct quads, exact counts): INFEASIBLE.  route2.py soft coverage: proven
  bound <= 482 of 504 rep (t,s) pairs; with slack the optimum needs 240 extra register slots.  => D4-only single-hop middle
  is excluded for this design (in-model, rigorous via solver bound).
- route3.py (generalized: lines -> cells -> any multi-section flats of rank 3..5, nested -> sections, Z15, 480 registers):
  full coverage 504/504 (and 408/408 with an in-chain block-total read of B') -- coverage is NOT the obstacle.
- stageS.py (section-level GF(2) content, upstream dropped; each arrival supported in one legal flat; lam invertible):
  FEASIBLE (excl=1).  All arrivals end up in rank-5 D5 nodes.  d5struct.py (exact): for each block-A3 A (120; 3 design A2
  sections each) G_A = A-perp is a D5 = B' + exactly one line of each of the 8 other blocks; each A2 section Q gets its
  other-block content exactly through its 3 A3s: Q-perp ∩ C = U_{A∋Q} (G_A ∩ C) (960/960).  Upstream consequence: no
  non-complement design cell lies in any G_A, and no pair cell lies in any G_A, so D5-node content must enter as raw line
  registers or through transversal non-cell flats.
- Rigor caveat: route.py / route2 bound / stageS cg runs used Z15-canonical variables => they exclude Z15-INVARIANT
  realisations only.  stageS_ns.py (no symmetry, 120 targets, 180 sections, 72,120 vars): cell-generated arrivals (support
  = union of design cells inside the arrival's node; WLOG multi-section nodes, since single-section pre-mixers can be
  removed), |Q| arrivals per section, B' block total read in-chain: INFEASIBLE (unconditional for this design/model).
  Z15 with one in-chain node read per target (support in cells of a node inside t's section perps): INFEASIBLE.
  depth2.py (Z15; raw line registers allowed; nodes fed by raw lines + cells; #in = #out at nodes/cells; 4 registers per
  line; B' in-chain): INFEASIBLE.  stageS cg=0 (raw content, no capacity) feasible -> the register budget is what fails.
- USER NOTE (2026-10-15): helper trimming is already confirmed not to work -> do not pursue punctured-native trimming or
  complex helper deletion.

## Chain-length (move) lever, exact (scratchpad/moves, price/movegrid.py)
- Replay of P111-tuned chains reproduces its local profile and price exactly (0.00173342703959).  Helpers avg 4.92 moves
  (top chain 0-1-2-4-6-7-8 x95), sources 4.86, targets 1.92.
- What-if reprices at R=439: helpers skip rank-1 copy stop +2.36%; skip rank-7 stops +2.51%; both +4.99%; also skip
  cells +12.0%; helpers 0->6->8 +22%.  Scenario grid (v=111, R<=444 wall): helpers 3 moves (src 2-3, tgt 2) c~0.00188-0.00191.
- FORCED (any E8 word, from cover number 3, exhaustive): >= 2 fresh helpers per source stop at <s> (x_s content leaves <s>
  only in registers at <s>; reach after next frame F is F-perp; covering s-perp needs >= 3), and >= 2 registers per
  target stop at t-perp then pay 7->8.  P111 has ~279 / ~370 such stops vs forced 222 / 222 -> realistic headroom from
  these two step types ~1.5%, needing a top with 2 t-perp reads per target.

## 4-section architecture: exact chain pricing and waste allowance (price/lor4sec.py, e84sec.py, e84waste.py)
- Forced chains (copies stop at <s>: each line in 4 cells -> 3 copies made at <s>; deliveries read at t-perp; one
  section read in-chain; targets 0 -> section -> t-perp), zero waste, vs P111-tuned 0.0017334:
  I_{11,1} R=660: no middle +9.1% (upper bound), one middle level rank 3/8 +3.3%, rank 4/7 +0.9%, rank 5/6 -0.2%,
  two levels -3.5..-4.9%.  E8 v=120 R=369: +2.7% (rank 3), +1.35% (rank 4).  E8 punctured v=111 R=342: +14.1% (rank 3),
  +12.6% (rank 4), two levels +8.9%.  Unbalanced moves (one big jump) price better than balanced.
- Waste allowance, punctured E8 (wasted helper = copy chain ending at FULL): rank-3 middle beats P111t up to R=444 (the
  hosting wall; +0.9% there), rank-4 up to ~438, two levels up to ~404.  => ~90-100 helpers of middle waste allowed.
- Correction: stageS/depth2 models required nonzero arrivals (excluded empty fresh helpers 0 -> section).  stageS2.py
  (maximal supports Q-perp ∩ Q'-perp, Z15) re-checked: cg=1 INFEASIBLE with and without empty arrivals.
- I_{11,1} all-proper 4-section covers (lsec/covers.py, H55 reps): P(0,1) 326,028 of 422,320; T reps 704,392 of 948,292
  (all three T reps identical counts).  Many A2-type planes have only 2 lines (4620 of 6765).
- Killed (unrun): E8 non-symmetric cell-routed test with general in-chain reads (stageS_ns ex0 cg1 ic1).
- I_{11,1} design A (lsec/ldesign_A.json; H55; 440 two-line planes; all covers proper; 52 rep (t,s) fail
  cross-orthogonality): raw section-level content INFEASIBLE (H55, nonzero arrivals), and INFEASIBLE with empty arrivals
  both H55 and NON-SYMMETRIC (55,990 vars).  Explanation (lprivcover.py, exact set cover): 3 of 8 section orbits need
  3 node supports (Q-perp ∩ Q'-perp) to hold their 2 users' private lines but have 2 arrivals.  Patching = +165
  registers -> R ~825 > 730 break-even.  ldesign4.py searches designs with lazy cross-orth + private-screen cuts.
- E8: 3 more Z15 designs (design_enum.py, witness relaxed to P ⊂ Q-perp; all 1 pair + 3 A2 per line) pass the
  private-line screen (design_0 with slack) but cell-routed content is INFEASIBLE (Z15, empties) for all 4 designs.
- MODEL CORRECTION: the in-chain user of a section reads any combination of its arrivals; only DELIVERED users' rows must
  be independent (earlier models forced all rows invertible).  Re-run with the correct rule (stageS2.py IC2=1): all 4 E8
  designs still INFEASIBLE cell-routed (Z15, empties).  depth2/depth2s re-run pending with the rule.
- stageS3 (min extra arrivals, cell-routed, original E8 design): stopped at 1 h limit, no solution, no bound (unknown).
- In-chain section reads cut the top to 3v arrivals -> zero-waste R = 2v.  Exact chain prices (price/inch2v.py) vs
  P111t: punctured E8 R=231 +36%, beats P111t for ANY R <= 444 (wall); E8 v=120 R=249 +22.6%, break-even R<=393-408;
  I_{11,1} R=440 +19.7..+23.4%, break-even R<=682-743.  (Scenario histograms of the forced chain shape, not words.)
- E8 original design, depth2 (raw lines, zero waste, corrected in-chain rule, Z15): INFEASIBLE.  depth2s (min registers,
  absent slots allowed) running.
- I_{11,1} design R (ldesign5.py raw mode, lazy private-screen cuts, 26 iterations; 440 two-line planes; passes the
  screen): raw section-level content INFEASIBLE (H55, empties, corrected in-chain rule).  Screen is necessary, not
  sufficient.  ldesign6.py: same with >= 2 three-line planes per line.
- Not modelled anywhere yet: nondegeneracy of Lorentzian node flats (extra restriction, does not affect INFEASIBLE).
- I_{11,1} designs (ldesign6.py): H55 with >= 2 three-line planes per line: INFEASIBLE (no such invariant design);
  >= 1: design R3 (275 two-line + 110 three-line planes; proper; passes private screen).
- R3 raw section-level content (empties, corrected in-chain rule): INFEASIBLE under H55, Z11 AND NON-SYMMETRIC (59,840
  vars) -> unconditional for that model.  Adding ONE free in-chain node read per target:
    unnested relaxation (any Q'-perp ∩ t-perp): FEASIBLE;  NESTED (X = Q*-perp ∩ Q'-perp inside the target's in-chain
    section Q*, chain 0 -> X -> Q*-perp -> t-perp): FEASIBLE (H55).  => first positive section-level result for the
    Lorentzian 4-section architecture; mechanism = targets read content passing through a middle node.
  Next: ldepth2s.py (depth-2 register capacity, nested in-chain node reads supported on available lines) on R3; also to do:
  nondegeneracy of node flats (Q+Q')-perp in R^{11,1}; add in-chain node reads to E8 depth2s.
- R3 with NONDEGENERATE nodes only (116/2688 rep node flats degenerate, excluded): nested in-chain section-level still
  FEASIBLE (H55).
- E8 depth2s (raw, min registers, corrected in-chain, absent slots, no node reads): solver found N=2475 only, bound 480
  -> inconclusive (model too big for CP-SAT to optimise).
- CAPACITY ARGUMENT (depth-2): a node with n inputs emits arrivals supported on <= n lines (raw) / ~3n (cells), and feeds
  only sections orthogonal to it.  R3: best nodes feed 6 sections (15 outputs, 15 lines); 88% feed 2.  => depth-2
  zero-waste cannot carry ~|R(t)|/4 lines per delivery; aggregation depth >= 3 needed (as in R420: cell -> quad -> D6).
  E8 designs: the only big nodes are the 10 block D4s, which carry only complement content.
- Deeper-middle pricing (price/inch2v_deep.py), in-chain architecture, zero waste R=2v: punctured E8 +28..+34% (2-3
  levels), beats P111t at any R <= 444; I_{11,1} +12..+17%, break-even R <= 632..711.
- Idea (not built, flagged to user as possibly 'trimming'): R420 top with partner-D6 in-chain reads + B' block-total
  in-chain reads instead of cell keepers -> partner D6s need 2 registers not 3 -> cells need 4 empties per frame not 6
  -> R ~ 360 + totals, IF the frame-triangle parity system becomes solvable with dependent in-chain rows.
- R3 depth-2 min-register (ldepth2s, 6000 s): UNKNOWN (no solution, no proof).  Counting check: producible incidences
  <= ~33,000 vs required 26,070 -> counting alone does not exclude depth-2 on R3.  ldepth2f.py: feasibility with
  N <= 959 (R <= 739, break-even) running.
- I_{11,1} hub pairs (lsec/hubs.py): Y = D4 (6 P + 6 T, rank 4, nondegenerate) with X = Y-perp 30 lines (rank 6);
  rank-3 Y (A3, 6 lines) with X 56 lines (rank 7).  A D4 hub lets its 12 targets read a 30-line X-total in-chain
  (E8 analogue: B' block total, 12 of 63).  Candidate backbone for a shallow Lorentzian middle (unbuilt).
- I_{11,1} APEX STRUCTURE (exact, by hand + lsec checks): for apex p, D10(p) = {P(ij), T(ijp) : i,j != p} (90 lines,
  rank 10; = the decoder-total frames).  D(S,p) ⊥ D(S^c,p) for S ⊂ [11]\{p}; D4|D6 hubs found by search are D(A,p) ⊕
  D(B,p) with |A|=4, |B|=6.  Readers x lines of a hub peak at a 5|5 split (20 targets read a 20-line total).
  Reader sets: R(T(abc)) = F2-sum over p in {a,b,c} of the FULL flats D10(p) ∩ t-perp (= D8(p; others) ⊕ A1, 57 lines,
  rank 9, single user) -- a parity 3-cover by full-flat totals (outside pairs counted 3x).  R(P(ab)) = sum over the 9
  apexes p ∉ {a,b}.  Identity: σ_p(T(pbc)) = τ_p + μ_p(b) + μ_p(c) + x_t (τ = apex total, μ_p(b) = 18 lines of D10(p)
  through b).  Not frame-legal to read τ, μ directly (D10(p) ⊄ t-perp); dedicated-σ deliveries cost ~990 registers.

## E8 frame-D6 parity identity and an R420-top variant (sec4/r420cells.json, stageS2/4)
- EXACT (all 120 lines): R(t) = tot(D6_1)+tot(D6_2)+tot(D6_3) + (x_e1+x_e2+x_e3) for t's 4-frame {t,e1,e2,e3}, D6_i =
  {t,e_i}-perp (a line ⊥ t meets an even number of the e_i non-orthogonally since the frame sums into 2E8; mates lie in 2).
  Both users of a D6 need the same full total -> one user in-chain removes that D6's forced third register.
- Mate corrections alone = triangle system with no solution (R420's d-line obstruction).  With in-chain reads of the
  2-mate cell Φ\{t,x(t)} ⊂ D6_{t,x(t)} (nested chain 0 -> cell -> D6 -> t-perp) the system is solvable iff every mate is
  excluded by an even number of targets, e.g. x(1)=x(2)=3, x(3)=x(4)=1.  Count: per frame 3 D6s with an in-chain user
  (2 registers) + 3 both-delivered (3) = 15 vs R420's 18; keeper-sums at 3 cells per frame (vs 6 empties) -> ~11 helpers
  per frame -> R ~ 330 + totals (R420: 420).  Possibly 'trimming' in the user's sense -- feasibility test only.
- Section-level on R420 geometry (Z15, raw, empties, dependent in-chain rows): 2 slots per D6: INFEASIBLE (ic=0 and
  nested ic=2); unnested node read: FEASIBLE.  stageS4 (one optional extra slot per D6, minimise) running.
- RESULT: R420 geometry, nested in-chain reads + dependent in-chain rows, one optional extra slot per D6 (stageS4.py):
  minimum extra slots = 4 orbits = 60 registers, PROVEN OPTIMAL within Z15 (R420 uses 180 thirds).  D6 level 420
  arrivals instead of 540.  Section-level relaxation only (supports, no capacity/phases/B'-routing); possibly 'trimming'.
- Faithful R420-skeleton model (scratchpad/r420v/r420top2.py): cells (2 sums each, optional keeper = 3rd register;
  keeper cells may send equal sums like R420), quads = R420's 60 D4s with span-preserving 6x6 transforms, block nodes =
  span of keepers, D6 thirds from the complementary block node (<= #keepers), in-chain node read (quad / keeper cell /
  block ⊂ t-perp, nested in the in-chain D6 if any), <= 1 in-chain D6 per target, delivered rows independent.
  Must admit R420 (180 keepers).  First version wrongly forced exactly one in-chain D6 and distinct cell sums (R420
  not representable) -> INFEASIBLE was a modelling artefact; corrected run in progress.
- R420 plan: qhost == partner for 28/120 targets; each target hosts at a distinct D6.
- Price per removed helper (P111-tuned chains, whole helpers removed, exact mass): ~+0.135% c each; with targets on
  0->4->6->7 (-1.6%): drop 60 -> +6.5%, 90 -> +11.2%, 120 -> +16.1% vs P111-tuned (estimates, not words).
- Faithful R420-skeleton model r420top2 (admits R420; cells may send equal sums only with a keeper/3rd register):
  OPTIMAL keepers = 180, PROVEN >= 180 (no symmetry assumed) for every top in the modelled class (in-chain D6 reads,
  nested quad/keeper/block in-chain reads, thirds from the complementary block node).  => R420's skeleton is locked at
  R = 420 by its SOURCE side (each cell must feed both its quads its full sum -> 3rd register per cell), not by the top;
  consistent with the hub family bound and the user's note.  r420top3 (adds d-cell keeper thirds, exclusive keeper
  roles) running; expected 180 for the same reason.
- My hand 60-keeper design had a frame-nesting error (a keeper in the block node sits at the block D4 frame, which is not
  inside the own-frame D6s) -- discarded.
- Mate-correction system per frame (r420v/mates.py, exhaustive): minimum 2 asymmetric D6s per frame; minimal sets are
  exactly complementary owner pairs {01,23},{02,13},{03,12}.
- R420 generator anatomy (gen_l3.py): cell = keeper branch + summed branch + empty; quad outputs ex_part = S^D^Qc (+ext);
  D6: o1 += o2; thirds = free keepers (zz D6s) or phase-B Q-deliveries (block node, rank 12).
- E8: all 4 designs, cell-routed + nested in-chain node read (stageS2 cg=1 ic=2, Z15): INFEASIBLE.
- R3 section solution (lstageS_dump) realisation cost (lsec/realize_cost.py): 880 nonzero arrivals, 1100 distinct
  nodes (one vector each), support sum 17,655 -> depth-2 cost N >= 1100 (R >= 880) even optimistically; raw ~17,655.
  The section solver does not share nodes -> need capacity-aware models.
- Apex hubs in R3: D4(S,p) (12 lines) feed up to 9 sections (23 slots); D5 (20) up to 4; D6 (30) up to 2.
  Pure 3-fold apex-D4 cover impossible (each hub 6 P + 6 T lines -> P over-, T under-covered; T lines would get 2
  registers, below the source cover bound).
- lhub.py: capacity-EXACT hub model (active hub = all its lines as raw inputs, any output vectors on its lines, <= |X|
  outputs; slots from hubs / raw lines / empties / absent; nested in-chain read at an active hub).  Running on R3.
- r420top5.py prepared: up to 2 nested in-chain node reads (cell ⊂ quad ⊂ D6 etc.).
- lhub.py on R3 (apex hubs |S|=3,4,5 + raw lines + empties; capacity-exact): INFEASIBLE at any register count (H55).
  R3's section-feasible solution needs big rank-7 nodes Q-perp ∩ Q'-perp, which feed only ~2 sections (poor capacity):
  squeezed between small nodes (insufficient content) and big nodes (unshareable).  Not a proof for every middle.
- Why R420 cells need 2 quads (hence an empty each): every cell is an E-cell for 8 D6s (4 per quad); one quad feeds only
  6 D6s.  Only escape inside the skeleton: targets reading quad content in-chain (r420top5 tests 2 nested reads).
- ehub.py (E8 capacity-exact hub model, 32,110 candidate hubs) running on the original design.
- Prior art (#620, research/e8-decoder-floors-and-cold14-notes/s4-lorentzian-helpers): E8 cell architecture transferred
  to I_{11,1}: 787 helpers (3.58/port) or 732 (3.33/port, pair sources with 2 non-cell branches); notes <= 3/port needs
  <= 0.63 empties per cell vs E8's 1.  Consistent with my frame-class bound R >= 770 (1 empty/cell) and break-even 730
  (k3).  Corpus search found no sub-420 E8 bit word attempts beyond R420 itself.

## Session (cont.): Lorentzian hub->mid, move what-if, R420 cells under a 4-section top
- USER (again): helper trimming is proven not to work -> r420top3 killed, r420top4/5 not run; task closed with the
  proven r420top2 result (keepers >= 180) only.
- lhub3.py (I11,1, design R3, H55-canonical): lines -> apex hubs D(S,p) (fully raw, <= |X| outputs) -> mid nodes
  Y = Q-perp ∩ Q'-perp (nondegenerate, containing a hub; inputs = hub registers; outputs <= inputs; content = union of
  feeding hubs) -> section slots (mid / hub / raw / empty / absent, <= |Q| slots) + one nested in-chain read (active hub
  or fed mid inside the in-chain section).  Bug fixed first (support clause omitted mid sources).
  HS = {3,4}: INFEASIBLE;  HS = {3,4,5}: INFEASIBLE.  Sanity run with free mids (FREEMID=1) pending.
  SCOPE: H55-symmetric only; <= |Q| arrivals per section; <= 1 nested node read per target; mids only from fully-raw
  apex hubs; mids only design-pair intersections.  NOT an exclusion of Lorentzian, nor of hub->mid in general.
- Move what-if (moves/inchain_whatif.py, exact pricer on P111-tuned's replayed profile): k targets read one needer
  in-chain at its D6 (needer 6->7->8 becomes 6->8, target 0->2->7 becomes 0->2->6->7; net -{1,5} +{2,4}):
  k=28 -0.15%, 56 -0.30%, 111 -0.60%.  Exact consequence of that histogram change: this restructure loses.
  Exact marginals (moves/marginal.py): every jump merge (a,b)->a+b gains +0.007..+0.013% per event; balanced splits lose.
  The +1.5% lever needs targets 0->6->7 with the d-line folded into a D6 needer (merge (1,5)->6 per target), which
  meets the mate system (>= 2 asymmetric D6s per frame) -> extra registers (~0.135% each) outweigh 0.013% per target
  unless the asymmetry is free.  Not built.
- lhub3 sanity (FREEMID=1: mids = all nondegenerate design-pair intersections, free content/capacity): pending.
- Punctured Lorentzian break-even (price/punct_be.py, scenario model): lowering v LOWERS the break-even R
  (I11,1 k3: v=220 730, 215 669, 209 597; k4: 633, 579, 514) -> puncturing gives no scenario-level allowance; P111's
  gain over R420 is in its real histogram, not in v.  (E8 v=120 rows hit the hosting wall 479.)
- R420 cells under the existing 4-section designs (sec4/stageS2c.py, CELLS=r420cells.json): INFEASIBLE for all 4
  designs -- trivially: sec4/cellcover.py shows 2880-5760 of 7560 (t,s) pairs have NO R420 cell of s inside any of t's
  design section perps (A2 sections meet other blocks in A2s, which hold no orthogonal pair).  Designs were built for
  self-dual planes, not for frame cells.

## CELL BOTTLENECK LEMMA (E8 frame architecture, ANY middle) -- cellb/forced.py, forced2.py, noroute.py
- Setting: (A1) every source has exactly 3 branch registers (x_s alone until first mixing) first-mixing at the 3 cells
  {s,e} of its frame; (A2) every register a target reads comes from inside one of t's 3 frame-D6s {t,f}-perp (in-chain
  reads at frames inside such a D6; deliveries at t-perp of registers whose previous frame is inside such a D6);
  closed frames, monotone chains.  R420 and P111's skeleton satisfy (A1)-(A2).
- Argument: if a cell C={s,e} is occupied only by its 2 branch registers, x_s and x_e leave C only in its 2 output
  streams (contents an invertible image of (x_s,x_e): at most one carries s+e), and every register later carrying
  their influence sits at frames ⊇ N_k (stream k's next frame, N_k ⊋ C).  A target whose every route for s AND for e
  passes through C ("doubly forced") needs either the s+e stream or both s and e streams, so some N_k must lie inside
  a C-containing D6 of every doubly forced target.  Minimal candidates N = closure(C + one line) suffice (any N ⊋ C
  contains one).
- EXACT (R420 D4 partition, source frames = top frames): every one of the 180 cells has 16 doubly forced targets and
  NO admissible common node -> every cell needs a 3rd register (empty or extra copy) -> N >= 540, R >= 420 for EVERY
  word in this class, whatever the middle (nodes, depth, in-chain reads inside the D6s).  This upgrades r420top2
  (R420's quad middle only) to any middle.  R420 is optimal in its class.
- Mismatched source/top partitions (top = g(source), random g in W(E8)): 2460-3056 (t,u) pairs have no route at all
  (infeasible outright); bad cells would be 148-168.
- Escapes NOT covered by the lemma: sources with >= 4 branches; targets reading outside their 3 frame-D6s (other
  sections, 4-section tops, chain frames not inside a D6); frame systems that are not D4 partitions (3-regular frame
  graphs; screening in cellb/framegraph.py).
- REFINEMENT (cell reads): a target may read cell C in-chain (frame C on its chain; a chain holds at most ONE rank-2
  frame).  k_C = doubly-forced targets that must then read C = 16 - max_N served.  R420 partition, frame top:
  k_C = 8 for all 180 cells (best node rank 3 serves 8) -> at most 120/8 = 15 cells keep 2 registers ->
  sum j_C >= 165 -> R >= 405 (rigorous, any middle).  Route-level CP-SAT (cellb/routemodel.py, frame top, Z15):
  min sum j_C = 180 PROVEN OPTIMAL (Z15-invariant solutions); non-symmetric run pending.
- FREE TOP (targets may read anywhere in t-perp; only (A1) assumed: 3 branches per source at the R420 cells):
  doubly forced T_C still 16 per cell, span rank 6 (no node serves all), best node serves 12 -> k_C = 4 -> at most
  30 cells keep 2 registers -> sum j_C >= 150 -> R >= 390 for EVERY word with R420-cell sources, any top, any middle.
  So R420-type sources leave at most 30 helpers (~4%) of room, and only via non-frame tops with every target spending
  its single rank-2 read on a cell; R420 itself is optimal for the frame top under Z15.
- Frame graphs that are not D4 partitions (3-regular, closed neighbourhoods = frames): with the FRAME top they lose
  routes (~3000 no-route pairs for triangle-free examples); with a FREE top every (t,u) has a route (parity identity:
  t ⊥ u meets 1 or 3 of u's frame mates orthogonally).  Doubly forced sets shrink there (t must avoid 4 mates instead
  of 2) -> screening Z15-invariant non-partition frame graphs (cellb/kfree_graph.py).
- CORRECTION: the parity identity (t ⊥ u meets 1 or 3 of u's mates orthogonally) holds only for D4-FRAMES (4
  orthogonal lines whose closure is a D4; 315 per line, 9450 in all) -- generic orthogonal 4-tuples (closure A1^4)
  fail it.  The triangle-free 'frame graphs' screened first (cellb/kfree_graph.py, k_C = 0) used mostly A1^4 frames
  (105 of 120) -> invalid: lines with no route (cellb/topcover.py INFEASIBLE; routemodel2 INFEASIBLE).  Redone with
  D4-frame graphs (cellb/fg_d4.py: each line picks a D4 frame ∋ it, symmetric adjacency, Z15).
- VALID D4-frame graphs (cellb/fg_d4.py, Z15, no partition-like line): free top -> |T_C| = 8 for every cell and
  k_C = 0 (one node serves all 8) in 3 of 4 graphs (4th: k_C <= 1) -> the doubly-forced bottleneck that locks every
  partition-frame word (R >= 390 free top / 405 frame top) DISAPPEARS for non-partition frame systems.  Top cost
  (cellb/topcover.py, fgd4_1_0): 2 delivered rank-6 flats + 1 in-chain section per target, i.e. 240 delivered (same as
  the in-chain frame top).  => the cell-level obstructions leave only the trivial R >= 240 for this class.  Next layers
  (route-level with singly forced targets, content parity, node capacity) pending.
- ehub.py (E8 capacity-exact raw-hub model, design.json, Z15): stopped by me after ~85 CPU-min with no solution and no bound (unknown); deprioritised (design.json is incompatible with frame cells; superseded by the cell-bottleneck line).

## Lorentzian cell-bottleneck port (session cont., scratchpad/lcell)
- lbase.py: 20,790 good 4-frames (pairwise orthogonal, sum in 2L; 252 per P line, 420 per T line), all nondegenerate.
  Parity identity holds for good frames (inner products of distinct lines are 0/±1; sum in 2L) -> with a FREE top
  every (t,u) has a route for every good-frame graph.
- H55-invariant symmetric good-frame graphs: NONE exist (CP-SAT INFEASIBLE, both partition and non-partition modes) ->
  H55 is too restrictive here; rerunning with Z11 (GRP=11).  (#620's partition used no such symmetry.)
- EXACT: good 4-frames are only TTTT (13,860) or PPTT (6,930) -> every good frame holds an EVEN number of P lines;
  55 P lines is odd -> NO partition of the I11,1 lines into good 4-frames exists (also confirmed: no H55- or
  Z11-invariant partition).  => every Lorentzian frame-cell source system with good frames is NON-partition (or mixes
  in PPP triples for T lines).  #620's E8-style transfer must break the partition somewhere.
- EXACT (stronger): no SYMMETRIC good-frame cell system exists at all on I11,1: a P line's 3-cover is only a PPTT
  good frame (1 P mate + 2 T mates), so symmetric cells would perfectly match the 55 P lines (odd).  T lines also have
  PPP covers (57 per T line: 3 P lines ⊥ T, pairwise non-orthogonal, sections {T,P}-perp cover R(T) oddly off the
  mates; T has 31 P lines ⊥ it).  => any 3-branch frame-cell source system on I11,1 has >= 1 asymmetric cell
  ("defect": the partner's content must come from an extra branch, +1 register).  lgraph2.py minimises defects
  (Z11 forces multiples of 11) and screens k_C.
- KEY CANDIDATE (E8): graph cellb/fgd4_1_0.json (Z15, non-partition D4-frame graph: 120 distinct frames, neighbouring
  frames share exactly 2 lines, frames lie in 70 D4s = 35 orthogonal pairs, each line in 7; no neighbour shares the D4).
  With the R420-type FRAME TOP (t's sections = perps of its own 3 cells, each D6 shared by its 2 cell users; frame-D6
  parity identity applies): 0 no-route pairs, doubly forced 8 per cell, k_C = 0 for all 180 cells, 16 singly forced
  per cell.  (Other graphs: fgd4_1_1 has 1920 no-route pairs under its own-frame top; fgd4_1_3 k_C 2-4.)
  => R420's top on a non-partition cell system passes the cell bottleneck screen.  Route-level frame-mode run pending.
- routemodel2.py (R420 cells, free top with rank-6 delivery flats, Z15): stopped by me (CPU); the kfree counting bound R >= 390 stands.
- routefree.py (route level, unrestricted top, R420 cells, Z15): solution with sum j_C = 150 = the kfree counting
  bound -> the route-level relaxation cannot exceed 390 for R420 cells (the true value may be higher).
- Section level (sec4/stageS2c.py, sections = perps of the graph's cells, cell-routed supports, nested in-chain,
  dependent in-chain rows, empties, EXACTLY 2 slots per D6): fgd4_1_0 INFEASIBLE; R420 INFEASIBLE (control).
  stageS4 (one optional extra slot per D6, minimise; cg=1) running on both.
- stageS4 (section level, cell-routed, KX=1, Z15): fgd4_1_0 min extra = 4 orbits = 60 (PROVEN OPTIMAL); R420 also 60.
  So both need 420 arrivals at the D6 sections; R420's cells additionally need 540 registers (cell lemma), the new
  graph's cells need none extra at cell level => combined relaxation bound N >= 420, R >= 300 for the new system vs
  R >= 420 for R420 cells (Z15).  Potential, not a construction.  Capacity model sec4/fcap.py (cells -> nodes ->
  slots with exact GF(2) stream spans, node counts; depth 2 only) running on both (R420 = control, expect >= 180).
- Target value (price/r420scale.py, exact pricer, R420 histogram minus whole empty helpers with jumps 2,2,2,2):
  v=120 frame-cell word beats P111-tuned iff R <= ~382 (R=380 +0.31%, 360 +2.95%, 340 +5.7%, 300 +11.8%).
  Estimate of chain shape only; a real word's histogram decides.
- lhub3 FREEMID sanity rerun: stopped by me (CPU priority to the cell-architecture runs) -> lhub3 INFEASIBLE results remain UNVALIDATED by a positive control; treat them as unconfirmed.
- routemodel.py frame top, R420 cells, NO symmetry: killed at the 30-min background limit before a result (unconditional frame-top bound stays at the counting value R >= 405).
- CORRECTION: stageS4's objective counts only slots BEYOND 2 per section (base slots free, possibly unused), so
  "420 arrivals / R >= 300" for fgd4_1_0 is NOT a valid bound.  Valid: 60 sections need a 3rd arrival (Z15); cells
  give N >= 360 (R >= 240).  Rerun minimising total used arrivals pending.
- stageS5 (= stageS4 counting EVERY used slot): fgd4_1_0 min total arrivals = 28 slot-orbits = 420, PROVEN OPTIMAL
  (Z15, <= 3 slots per section).  So N >= 420 / R >= 300 does hold within that scope; KX=2 rerun to drop the 3-slot cap.
- stageS5 KX=2 (<= 4 slots per section): still 420 arrivals, PROVEN OPTIMAL (Z15) -> section+cell relaxation bound for fgd4_1_0: N >= 420, R >= 300 (Z15 scope; section-level relaxation, cell-routed maximal supports).
- Structure note (frame top, any frame-cell system): S = #cells = #sections = 1.5v, cells give exactly 2S = 3v
  registers; sections need ~2 arrivals each because the two users' mate corrections differ (in a NON-partition
  system user t's correction in {t,f}-perp lies in t's other mates, user f's in f's other mates -- disjoint sets), so
  arrivals >= ~2S = 3v, i.e. R >= 2v + X (X = sections needing a 3rd arrival).  E8 fgd4_1_0: X = 60 = 0.5v -> R >= 300.
  If I11,1 behaves alike (X ~ 0.5v = 110) its floor in this class would be ~550 vs break-even 633 (k4) / 730 (k3).
  Room: E8 ~0.68v (to ~382), I11,1 ~0.38v (k4) / ~0.82v (k3).  To be measured (lcell/lstage5.py).
- Lorentzian symmetric-system parity, second obstruction: with all P lines in PPTT frames, P-T edges = 110 force
  55 T lines into PPTT frames and 110 into TTTT; T-T degree sum = 55*1 + 110*3 = 385 is ODD -> a second defect is
  forced (besides the P-matching one).  PPP covers are incompatible with the frame top (PPP mates are pairwise
  non-orthogonal, so each mate lies in NO section of the target; 3 mates cannot all come from one rank-2 read).
  Z11-invariant systems: defects come in multiples of 11 (>= 11 from the P orbits; likely >= 22).
  lgraph3 first solution: 66 defects (not optimal; 11 PPP covers).  Rerun with NOPPP=1.
- RETRACTION (frame top): route-level model with ALL forced targets (cellb/routemodel.py frame, GRAPH=fgd4_1_0, Z15):
  min sum j_C = 225, PROVEN OPTIMAL (vs 180 for R420 cells).  The doubly-forced screen (k_C = 0) was too weak:
  16 singly forced targets per cell cannot be served by a 2-register cell's streams.  => fgd4_1_0 with the frame
  top needs N >= 585, R >= 465 (Z15 scope) -- WORSE than R420.  The "escape" holds only for the doubly-forced screen.
  Free-top route-level for fgd4 graphs to be rerun (routefree/routepar).
- fcap.py (frame-top capacity, fgd4_1_0 then R420): stopped by me -- superseded by the frame-top route bound (225 > 180).
- PPP covers are invalid on the SOURCE side too: a mate P_i of a PPP-cover line u needs x_u (P_i ⊥ u) but no cell
  {u,P_j} lies in P_i-perp (the P's are pairwise non-orthogonal) -> no route (routepar free top on lsys3_1_0, which
  had 11 PPP covers: INFEASIBLE).  Good frames only (NOPPP=1).
- (User: Lorentzian only.)  E8 runs stopped.  lgraph3 NOPPP (Z11, good frames only, 150 s): system lcell/lsys3np_3_0.json
  with 44 defects (55 P + 165 T good frames; not proven minimal).  Cells 352; registers 2*352 = 704 = 660 + 44.
  Route models running on it: TOP=choose (any good frame through t as top), TOP=sec4 (<= 4 plane sections),
  plus lsys_screen (own-frame no-route, k_C).
- lsys_screen(lsys3np_3_0): own-cover frame top: 8074 no-route pairs (infeasible as matched frame top).  Free top:
  doubly forced up to 38/cell; k_C: 0 (154 cells), 2 (33), 4 (143), 12 (22) -> counting with <= 220 cell readers:
  sum j_C >= 127 -> R >= 440 + 44 + 127 = 611 for THIS system (free top, doubly-forced counting only; real value higher).
- lcell/lsa.py (local search over Z11 good-frame systems, objective = free-top doubly-forced counting bound
  R_lb = 440 + defects + sum_j_lb): from 611 (44 defects + 127) to 592 (132 defects + 20) and 594 (154 + 0).
  Defects and cell bottleneck trade off; heuristic minima ~590 (NOT a proof over all systems; counting bound only).
- I11,1 scenario prices near the class bound (vs P111t): R=592 k3 +10.2% k4 +3.1% k5 -2.0%; R=611 +8.7/+1.7/-3.4;
  R=633 +6.9/0.0/-5.0; R=660 +4.9/-1.9/-6.9.  Real words make ~4.4 moves/register -> even AT the heuristic bound ~592
  a frame-cell Lorentzian word is only about break-even, and real words sit above their lower bounds.
- lsys3np_4_0 (seed 4): R_lb 638 (44 defects + 154).
- REFINED per-cell screen lcell/lscore2.py (free top; doubly + singly forced; 2-register cell streams (s+a,s),
  (s+a,a), (s,a) to rank-3 closure nodes INCLUDING degenerate ones -- valid relaxation even with general frames,
  since a general frame F ⊋ C meeting other content has line span ⊇ some closure(C+x)); unserved forced targets need
  the target's single rank-2 read; counting with <= 220 readers.  R_lb2 = 440 + defects + sum_j_lb2:
  lsys3np_3_0 633; lsys3np_5_0 622; lsa_best_1 616; lsa_best_2 594 (132 defects + 22).  lsa2.py searches on R_lb2.
  NOTE: lsa.py's doubly-forced score used nondegenerate nodes only (not a valid bound under general frames);
  lscore2 numbers supersede it.
- lcell/ltopcheck.py: for lsys3np_3_0 and lsa_best_2, EVERY target misses 13-24 lines of R(t) under EVERY good-frame
  top (no frame triple through t has a source cell of each u inside its sections) -> minimal-delivery tops
  (in-chain + 2 delivered) are impossible for these systems; targets need >= 3 delivered registers (4-section-type
  tops), i.e. >= 3v = 660 deliveries.  TOP=choose route run killed (moot).  (A system designed for frame-top routes,
  like E8's fgd4_1_0, is not excluded -- not searched.)

## Session 09:32-11:32 UTC (user: 2 h or breakthrough), Lorentzian
- More Z11 systems (lgraph3 NOPPP, seeds 4-9) doubly-forced score: 638, 603, 677, 611, 581, 572 (seed 9: 132 defects,
  0 doubly-forced extras).  Refined (lscore2): lsys3np_8_0 605, lsys3np_9_0 611, lsa2_best_11 583 (132 + 11).
- REALISTIC CHAIN PRICING (price/lor_framecell_price.py, exact pricer, v=220, h=11): R420-like chains (sources
  1-2-m-9-10-11, carriers 0-1-2-m-9-10-11, extras 0-m-9-.., targets 0-2-9-10, 660 deliveries, 11 totals at rank 10):
  node rank 5: R=550 +7.6%, 583 +5.1%, 620 +2.5%, 660 -0.2%, 700 -2.8% vs P111t; ranks 4/6/7 similar (break-even
  R ~ 655-665).  => a Lorentzian frame-cell word AT its cell-level floor (~583) would beat P111-tuned by ~5%;
  room above the floor ~75 registers.  Precedent: R420 sits exactly on its class's cell-level bound (240 + 180).
  This is POTENTIAL (lower bound + chain-shape estimate), not a word.
- Bottleneck anatomy (lcell/lcellstats.py): cells of FULLY shared frames have doubly-forced sets of 4..38 and r up
  to 12 (lsys3np_3_0: D29 r4 x99 cells, D38 r12 x22); extra branches (defects) add routes and relieve them.  MIXED
  cells (frames differ) have small doubly-forced sets.
- NOFULL search (lgraph3 NOFULL=1: no two lines of a cell choose the same frame): lsys3npnf_31_0: 176 defects (300 s,
  solver bound 11) but sum_j_lb2 = 6 -> R_lb2 = 622.  => if a non-partition Z11 system with ~22-44 defects exists,
  the cell-level floor would be ~470-490 (vs break-even ~655).  Searching for low-defect NOFULL systems.
- Stopped: sec4 route model on lsys3np_3_0 (no result within budget), lsa2 seeds 21/22 (superseded family).
- NOFULL defect sketch (hand argument, to be verified by the CP-SAT bound): if P(ab)'s frame is {P(ab),P(cd),T(abx),
  T(cdx)} and a T-neighbour's frame differs, either that arc is a defect or the T's frame is forced to
  {P(ab),P(ef),T(abx),T(efx)} (resp. {P(ab),P(cx),T(abd),T(cdx)}) whose P(ef) (P(cx)) frame is forced to contain
  P(ab), giving an unreciprocated P->P(ab) arc (P(ab) has one P-neighbour).  Each such defect is charged <= 2 times
  over the 110 P-T arcs -> NOFULL systems need >= ~55 defects (R_lb >= ~500).  Not yet rigorous.
- lcell/lsa3.py: fast cached Z11 local search (0.006 s per unchanged rescore); lsa4.py: NON-symmetric local search.
- Two middle levels (price/lor_framecell_price2.py; cell -> m1 -> m2 -> section 9): R=520 +5.9%, 550 +3.8%,
  583 +1.6%, 620 -0.8%, 660 -3.2% vs P111t (break-even ~612).  One level: break-even ~655-665.  So the margin above
  the best cell-level floor (~583) is ~30 (two levels) to ~75 (one level) registers.
- lsa3 (Z11, fast cached): 583 -> 578 (132 defects + 6) [lcell/lsa3_best_a.json].  lsa4 (non-symmetric) and lsa5
  (search for own-frame-top-admitting systems: stuck at >2000 no-route pairs, 660 defects) stopped.
- Running: parity-level free-top route model on lsa2_best_11 (global coupling); sec4 route model (<=4 plane sections,
  ALLNODES) on lsa3_best_a; lgraph3 NOFULL defect minimisation (bound from the solver).
- lsa3 seed 43: 572 = 440 + 132 defects + 0 cell extras [lcell/lsa3_best_f.json] -- cell bottleneck fully relieved; floor = 2v + defects.
- Faithful-er chain pricing (price/lor_fc_price3.py: every helper a carrier/extra branch 0-1-2-mid-9-.., sources
  1-2-mid-9-.., 660 deliveries, targets 0-2-9-10): one middle level R=572 +4.5% (break-even ~630); TWO middle levels
  R=572 -0.1% (break-even ~572).  => even a word exactly at the best cell floor (572) only TIES P111-tuned if its
  middle needs two aggregation levels (likely: cells rank 2 -> sections rank 9); +4.5% needs a one-level middle.
  Lorentzian frame-cell potential: between ~0% and ~+4.5% at the floor; real words above the floor do worse.
- Stream-node anatomy (lcell/lnodes.py, lsa3_best_f): every cell's sum stream goes to its own private rank-3 node
  (396 distinct, none shared) -> all sharing/aggregation must happen above rank 3.
- Puncture check (lor_fc_price3 shape): v=209 R=564 -> -4.2% (one level) / -8.5% (two levels): puncturing does not help in shape models (P111's E8 gain is histogram-specific).
- One-level-middle feasibility (thinking, not proven): in a one-level middle each stream visits one node N, whose
  k_N outputs each serve <= 2-3 targets (delivered user + in-chain users of its section), and only targets in
  perp(N).  Global count: sum over lines of reach >= 26,070 needs nodes with k_N >= ~6 registers and >= ~18 lines in
  perp -> not excluded by counting.  Per-target view: t needs content from >= ~60 cells through <= ~9 outputs ->
  nodes of rank ~6-7 inside t-perp, whose perps hold few targets -> tension.  Undecided; decides 0% vs +4.5%.
- Non-symmetric low-T search (lsa4, from lsa3_best_f): 570 = 440 + 130 defects + 0 [lcell/lsa4_best_g.json].
- Node-family observation: for a 6-set B, N_B = P lines on B (15 lines, rank 5) has perp L(A) (A = complement,
  20 lines: P and T on A) -> a quad-like node: holds the P-P cells inside B and serves the 20 targets of L(A).  Each
  P-P cell lies in 21 such N_B.  T-T cells inside L(A) (|A| >= 5) serve only P targets on B (<= 15).  Candidate
  building blocks for an R420-style Lorentzian middle; not developed.
- In-chain NODE reads (target chain 0-2-m-9-10: read a big shared node on the chain for free) relieve the per-target
  output limit that makes one-level middles hard.  Prices at R=568 (current best floor): one-level registers +
  simple targets +4.8%; one-level + targets with a node stop +2.6..2.8%; two-level registers +0.2%.  R=600: +2.3/+0.1/
  -2.4%.  => potential at the floor ~0..+5%, typical ~+2.5%; break-even ~600 for the node-read design.
- Non-symmetric search: 568 = 440 + 128 + 0 (lcell/lsa4_best_g.json).
- lgraph3 NOFULL (1500 s): 132 defects, solver lower bound 22 (= parity minimum under Z11); its j = 47 -> R_lb2 619.
- Defect-repair search (lcell/lsa6.py, non-symmetric): 566 -> 555 (114 defects + 1); independent recheck with
  lscore2 (all closures): lsa6_best_i.json = 554 (114 + 0).  At R=554: two-level middle ~+1.3%, node-read design
  ~+4%, one-level ~+6% vs P111t (interpolated from the exact price grids).  Continuing (seeds 93, 94).
- Exact prices at R=554 (price grids): one-level +6.02%, one-level+node read +3.68%, two-level +1.34%, two-level+node read -0.81% vs P111t.  R=520: +9.0/+6.5/+4.3/+2.0.
- sec4 route model on lsa3_best_a stopped (memory 6 GB, older system, no result); parity-level free-top model restarted NON-symmetric on the 554 system (lsa6_best_i).
- 554 system anatomy (lsa6_best_i): 35 fully shared frames (140 lines: 92 in PPTT, 48 in TTTT), 74 lines with their
  own frame, 3 frames shared by 2; extra branches: 102 lines x1, 6 lines x2.  Pattern: a partition-like core whose
  cell bottlenecks are relieved by extra branches coming from 'satellite' lines whose frames point into the core.
- FRAGILITY: in the 554 system the cells that would need in-chain readers demand 228 reads (40 cells x2, 34 x4, 1 x12) against 220 targets with one rank-2 read each -> the floor relies on nearly every target spending its single cell read on a specific cell (and on nesting that read under its chain); real words will likely pay more.
- Pessimistic variant (no in-chain cell reads): every cell with r_C > 0 needs a 3rd register -> 554 system: 440 + 114 + 75 = 629.  So the cell floor lies in [554 (optimistic reads), 629 (no reads)] for this system; prices: one-level +6.0% .. ~0%, two-level +1.3% .. ~-4.5%.
- Validation: the refined screen on E8 R420 cells gives r_C = 4 for all 180 cells and sum j >= 150 (= kfree bound; R420 realises 180) -- consistent.
- Optimistic-best systems saturate cell reads (demand 224-228 vs 220) and have no-read floors 628-629; the no-read-optimised search is at 611.  Range of the cell floor: [553 optimistic, ~611 no reads].
- Exact prices: R=553: one-level +6.11%, +node read +3.76%, two-level +1.42%, two-level+node read -0.73%.  R=608 (no-read floor): +1.62 / -0.54 / -2.98 / -4.95%.
- Forced cells per target (lsa6_best_l): 33-63, mean 49 -- each target needs content routed from ~49 specific cells.
  In a one-level middle each such cell reaches t only through one of its 2 stream nodes, and t has ~19 channels
  (4 sections x ~3 arrivals + <= 7 nested in-chain node reads), so nodes must hold ~2.6 of t's forced cells each
  while also serving each cell's ~25-40 forced targets -> one-level middles look infeasible (counting heuristic, not
  proven) -> two-level middle -> break-even ~555-572 ~ the floor itself.  Best estimate: Lorentzian frame-cell words
  are at best about break-even with P111-tuned.  NOT a proof.
- CORRECTION to the one-level heuristic: rank-4 good-frame spans hold all 6 cells of the frame (like R420's quads)
  and have rank-7 perps with many lines -> nodes with ~6 cells serving many targets exist, so one-level middles are
  NOT implausible.  One- vs two-level remains undecided (=> potential at the floor 553: between ~-0.7% and ~+6%).
- BUG NOTE: lcell/lscore2.py memoises r_C per Z11 orbit of the cell -> WRONG for non-symmetric systems (its "554"
  recheck of lsa6_best_i was not a valid independent check).  New independent scorer lcell/lscore_ind.py (no
  cross-cell memo): lsa6_best_k 552 (112 defects, reader demand 218 <= 220, j 0; no-read 624), lsa6_best_l 553,
  lsa3_best_f (Z11) 572 -- the search scorers (context-keyed cache) are confirmed.
- No-read-optimised system (lsa6_best_nr, independent check): 601 = 440 + 152 + 9, reader demand only 50 (robust).  Search at 600.  At R=600: one-level +2.3%, one-level+node read ~0%, two-level -2.4%.
- One-level probe (lcell/lmulti.py, lsa6_best_k, every 3rd cell): a node closure(C u C') holding >= 3 system cells
  covers typically 40-60% of C's forced targets (max 100%); any 2-cell closure 50-80%.  With 2 streams per cell,
  coverage is not the obstacle; capacity (outputs/fan-out) undecided.  One- vs two-level stays open.
- 552 system anatomy (lsa6_best_k): 23 full PPTT frames (46 P + 46 T) + 12 full TTTT frames (48 T) = 140 lines in 35 full frames; 9 P + 21 T with own PPTT frames, 42 T with own TTTT, 8 T in TTTT frames shared by 2; extra branches: 101 lines x1, 4 x2, 1 x3.
- 10:33: floors optimistic 552 (lsa6_best_k/l), no-read 599 (lsa6_nr).
- 10:40: lsa6 seed 97 (from Z11 lsys3np_5_0, 66 defects) reached 550 = 440 + 110 defects + 0 extras
  [lcell/lsa6_n550_snapshot.json].  Independent rescore (lscore_ind.py): cells 385, reader demand 216 <= 220, j 0,
  R_lb 550; NOREADS 617.  Exact prices at R=550: one-level +6.37%, one-level+node read +4.00%, two-level +1.67%,
  two-level+node read -0.49% vs P111t.  Different start basins matter (k/l from lsa6_best_i stalled at 552).
  Running: lsa6_o (from the 550 system), lsa6_p (from lsys3np_8_0), lsa6_n (continuing), lsa6_nr (no-read).
- 10:44: lsa6 seed 97 -> 548 = 440 + 108 + 0 [lcell/lsa6_n548_snapshot.json]; independent rescore: reader demand
  220 = V exactly (pool fully saturated), no-read 615.  No-read search finished at 596 = 440 + 144 + 12
  [lcell/lsa6_nr596_snapshot.json] (independent: reader demand 80).
- EXACT READ ASSIGNMENT (lcell/lexact.py): the pool count lets 220 reads be spread arbitrarily; exactly, each
  target reads ONE cell, and each bottleneck cell must pick one minimal unserved set U (over all stream patterns and
  rank-3 closure-node pairs, degenerate included) whose targets all read it, or take a 3rd register.  CP-SAT set
  packing.  j=0 test (J0=1; options restricted to |U| <= r_min + slack, valid since chosen sets are disjoint):
  548 system INFEASIBLE (slack 0) -> R >= 549;  550 system INFEASIBLE (slack 4) -> R >= 551.  (lmand.py: no target
  is mandatory for any cell -- the conflict is global, not local.)  Full minimisation running.
- Margin search (lsa6.py POOL=205: pool counting with 15 reads held back, a search proxy only): 550 = 440 + 110 + 0
  with reader demand 204 (slack 16) [lcell/lsa6_q550_snapshot.json] -> exact j=0 test STILL INFEASIBLE (12,012
  options) -> R >= 551.  The 550-system with slack 3 [lsa6_q551_snapshot.json]: INFEASIBLE -> >= 551.
  lconf.py: NO pairwise conflicts (every pair of bottleneck cells has disjoint option pairs) -> the obstruction is
  global (higher-order set-packing), not local.
- Sanity control: lsa6_nr596 (12 bottleneck cells, demand 80): exact j=0 FEASIBLE (OPTIMAL) -> its exact-read floor
  is 584 = 440 + 144 + 0 (an explicit read assignment exists).  So the infeasibility results are not a model artefact.
- Independent pure-Python backtracking verifier (lcell/lxc.py, no CP-SAT) launched on 548 (slack 0) + control.
- lxc.py (independent backtracking, no CP-SAT): 548 (n) j=0 DOES NOT EXIST (4 nodes); control nr596 EXISTS (17 nodes)
  -> agrees with CP-SAT on both.  Margin 548 [lsa6_q548_snapshot.json, demand 205, slack 15]: exact j=0 INFEASIBLE.
- MAJOR: full exact minimisation on lsa6_n550 (pool count 550, demand 216; 110 defects): CP-SAT proven bound
  sum j >= 18 (incumbent 23) -> R >= 568 for that system (not 550).  [corrected attribution: first noted as best_k]  The pool count is far too optimistic for read-saturated
  systems: reads cannot be distributed freely.  => the "optimistic floor ~548-552" is NOT valid as an exact-read
  floor; exact-read floors so far: nr596 system 584 (exact, j=0 feasible), lsa6_n550 >= 568 (<= 573).
  Searches switched to reduced pools (POOL=100, 140) from the nr596 system; winners to be exact-checked.
- Certificate (lxc.py VERB=1, 548 system, slack 0 => every bottleneck cell must use a minimum-size unserved set):
  cells {4,53}, {35,60}, {59,71} have unique minimum sets {111,156}, {0,6,116,190}, {14,26,101,193}; the unique
  minimum set of cell {10,84} meets their union -> no j=0 assignment (4 search nodes).  lsa3_best_f (572, Z11,
  demand 220): j=0 does not exist (2 nodes) -> >= 573.  lsa4_best_g file now scores 564 (122 + 2, demand 236 > 220).
- Exact prices: R=568 +4.84/+2.55/+0.18/-1.92%; 575 +4.27/+2.00/-0.38/-2.46%; 584 +3.53/+1.29/-1.11/-3.15%;
  596 +2.57/+0.37/-2.05/-4.06% (one-level / +node read / two-level / two-level+node read) vs P111t.
- Full exact minimisation, 548 system (lsa6_n548, 108 defects): sum j in [16, 20] (CP-SAT bound 16, incumbent 20 =
  explicit read assignment) -> exact-read floor of that system in [564, 568].  550 system: [568, 573].
  => BEST EXACT-READ FLOOR FOUND: <= 568 (lsa6_n548 with an explicit assignment), >= 564 for that system.  Low-defect
  read-saturated systems still beat read-light ones (584) after exact assignment.  Rerunning 548 with the knapsack cut.
- r140 search system (lsa6_r140_a.json, 136 defects, demand 167): exact sum j in [1, 9] (400 s) -> [577, 585].
- Exact prices R=564: +5.18 / +2.87 / +0.51 / -1.60% (one-level / +node read / two-level / two-level+node read).
- Open next questions (Lorentzian frame-cell class):
  1. Search directly on the EXACT read-assignment score (pool counting misleads); candidate objective: LP relaxation
     of the set packing (GLOP) inside lsa6, exact CP-SAT on improvements.
  2. Close the [564, 568] gap for lsa6_n548 (longer CP-SAT run / better cuts).
  3. Middle construction (R420 analogue) and the one- vs two-level question decide the sign of the potential.
- Margin 550 system (lsa6_q550, 110 defects, demand 204): exact sum j in [10, 18] (800 s) -> [560, 568].
- Margin 548 system (lsa6_q548, 108 defects, demand 205): exact sum j in [11, 20] (500 s) -> [559, 568].
  All low-defect systems' explicit assignments land at 568; proven lower ends 559-564 (CP-SAT gaps open).
- Parity-level route model (routepar.py PAR=1 TOP=free ALLNODES NOSYM) on lsa6_best_i: timed out at 3200 s with bound 0
  (incumbent 726) -> INCONCLUSIVE (model too large); no information beyond the per-cell screens.
- 548 rerun with knapsack cut (600 s, loaded CPU): bound 13 / incumbent 21 -- weaker than the first run; combined
  (proven bound 16 from run 1, assignment j=20 from run 1): lsa6_n548 exact floor in [564, 568] unchanged.
- Mid-pool search (lsa6.py POOL=185 from the 548 system): 554 = 440 + 114 + 0, demand 184 [lcell/lsa6_s185_a.json];
  exact sum j in [8, 15] (420 s) -> [562, 569].
- Long run (840 s), lsa6_q548: incumbent j = 19 -> explicit exact-read floor 567 (best found), bound 11 -> [559, 567].
- Final long run lsa6_n548 (780 s): bound 13 / incumbent 20 (no change; [564, 568] from run 1 stands).
- 11:28 SESSION END.  Verdict unchanged: Lorentzian frame-cell words NOT proven worse, NOT shown better.  Best
  exact-read cell floor 567 (explicit), per-system lower ends 559-564; window at the floor -1.9%..+4.8% vs P111t by
  middle depth (no-read floor 596: -4.1%..+2.6%).  The earlier 548-552 "optimistic" floors were pool-count artefacts.
  No background jobs left running.

## Middle-layer construction session (user: "continue building the middle layer"), scratchpad/lmid, system lsa6_q548
- Top coverage (lmid/ltop4.py, exact per-target CP-SAT): R(t) (|R| = 129 for P, 115 for T) covered by plane sections
  using ONLY routable lines (some system cell of u inside the section) + one in-chain cell read: 213 targets need 4
  sections, 7 T targets need 5, none fewer -> >= 3 delivered registers per target, >= 667 deliveries (rigorous for this
  system: every delivered register's content lies in a rank-<=9 flat inside t-perp, i.e. inside a plane section).
- FRAME-TOP PARITY IDENTITY (exact, all 220 targets, lmid/lftop.py): for any good frame {t,e1,e2,e3},
  R(t) = sum_i tot({t,e_i}-perp) + x_e1 + x_e2 + x_e3 (lines have |<u,e>| <= 1, frame sum in 2L).  But on this system the
  unroutable part forces a private correction c(t): own frames |c| 23-58, best frame over ALL good frames through t
  |c| 16-28, and for NO target and NO frame does c(t) fit routably in one extra plane section (lftop2.py) -> a
  shared-total frame top costs >= 4 deliveries per target (>= 880 registers, R >= 660) on this system.
- Node census (lnodes2/3): pair-closure nodes are rank 3-4 with <= 8 covered lines; apex hubs D(A,p): |A|=5 (rank 5,
  20 lines, perp 20) up to 13 covered lines; |A|=6 (rank 6, 30 lines, perp 12) up to 22.
- ONE-LEVEL REACH BOUND (rigorous for strict one-level: every register visits <= 1 frame strictly between rank 2 and 9;
  lmid/lreach2.py + lgmax.py): content entering node N reaches only users of the sections visited by N's registers
  (<= 3 each, perp of a rank-9 flat is a plane) and only targets in perp(N); lines fed <= 2 per cell register; so
  incidences through N <= min(a_N, 2k)*min(b_N, 3k) <= k*min(3a_N, 2b_N).  Exhaustive over ALL flats containing each
  cell (WLOG N = perp(perp(cells)), DFS with b-pruning): per-cell best 30 (288 cells), 33 (20), 36 (57), 39 (19);
  over all flats G* = 40 (D5 hub: 20 lines, perp 20).  Cell registers give <= 24,186 < 25,630 = sum|R(t)| - 440
  -> >= 37 extra registers -> ONE-LEVEL R >= 585 for this system (vs exact-read cell floor 559-567).  Loose: assumes
  every register at its node's maximum, all sections with 3 using users (A2 planes), no double coverage.
- A2-only tops (lmid/ltop4a.py): with only 3-user (A2-plane) sections EVERY target needs 5 sections -> any 4-section top
  uses >= 1 two-user section; lines forced through 2-user sections sum to >= 1801 (lmt.py: 3 best A2 sections + cell
  read cover all but m_t = 6-10 lines per target).  Small effect.  (A per-register v2/v3 split is NOT valid for mixed
  nodes -- brute force found violations of k3*min(3a,2b)+k2*min(2a,2b) >= min(a,2k)min(b,3k3+2k2); not used.)
- Refined reach with A2 packing (lreach3.py, running): a register reaches the lines of ONE plane in perp(N); k registers
  reach <= min(b, 2k + min(k, alpha)), alpha = max disjoint A2 planes in perp(N).
- Refined one-level reach (lreach3.py, exhaustive, A2-packing reach limit): per-cell values 28 (77), 30 (211),
  31.2 (20), 34 (57), 35.3 (19); X = 23,436 < 25,630 -> >= 55 extra registers -> ONE-LEVEL R >= 603 (this system).
- FIRST LORENTZIAN FRAME-CELL WORD BUILT (lmid/lw.py builder + lmid/build3.py design): word3.json.gz, system
  lsa6_q548, one-level middle (line -> system cell -> pp-closed node inside the section -> plane section -> t-perp),
  per-target min plane-section tops (887 private parts), exact F2 frame algebra, decoder totals tot_i = sum D10(i)
  hosted at FULL on dead registers (no feeders needed).  Independent checker tword/gcheck.py: PASS (nondegenerate
  frames, nesting, content-in-frame, exact F2 semantics, H1-H5, rank mass).  R = 11,494 (greedy small nodes: 7,861
  node outputs, 7,885 cell empties, 3,050 node empties) -> beyond the hosting wall, unpriced.  Pipeline validated.
- Middle variants on the same private 4-section top (887 parts): build5 capacity-aware greedy R = 11,819; build6
  max-coverage (every part taken straight from its section: 15,574 cell links) R = 15,533; build7 annealing over
  per-part node covers: cost 10,876 -> 10,728 (R 11,637).  Structural: with transform-at-node middles every private
  part costs one register per node arrival; R ~ 1e4.  Paired top (ltopP.py, CP-SAT 900 s): only 956 deliveries found
  (bound 126) -- not usable as formulated.
- Parity covers by ROUTABLE section totals exist for every target (lparspan.py: 1[R(t)] in the F2 span of {rt(S)}, span
  dim 86-120); min weight not found in 60 s (CP-SAT bound 5).
- New paradigm being built (R420 mechanism): pure BROADCASTERS (branch registers carrying one line, climbing nested
  frames, never modified) + COLLECTORS (delivery registers and targets in-chain reading whatever is present along one
  nested chain inside t-perp; one register per delivery regardless of how many lines).  bc1.py = support-level
  coverage prototype.
- bc1.py (random broadcaster chains, depth 4): even 12 reading chains per target leave ~68 of 115 lines unread ->
  broadcaster chains must be coordinated with readers.  bc2.py (demand-driven broadcaster/collector word, emitted):
  R = 22,846 (21,959 carriers + 887 collectors): collectors read at big section-local nodes, which no other section
  can share (a broadcaster serves only a NESTED family of read frames) -> almost every read spawns a broadcaster.
- STATUS of the build: a valid Lorentzian frame-cell word exists (word3, gcheck PASS, R = 11,494).  Every middle
  construction tried (transform-at-node greedy x3, annealing, broadcaster/collector) lands at R ~ 1.1e4 - 2.3e4,
  20x the exact-read cell floor (559-567) and far beyond break-even (~600-630).  An efficient middle needs a laminar
  system of PUBLIC frames (small flats inside many sections, each a meeting point for broadcasters and collectors,
  arranged so that every collector's reads lie on one nested chain) -- the analogue of R420's quads/D4 blocks; no
  such structure is known for I_{11,1} (no frame partition; apex hub lattices fail the nesting).  Open.

## 9-hour session (start 13:12 UTC; user: do not stop, do not dismiss anything until verifiably bad)
- frs.py: own-frame-top routability search (U = unroutable (section,line) pairs + lam*defects); lsa6_q548 starts U=8115.
- E8 calibration: R420's 180 cells give U = 0 (every D6 section = cell perp is covered by cells inside it) -> full
  own-frame routability is R420's defining property.
- I_{11,1}: no plane section of lsa6_q548 is fully routable (deficits 5-30, typical 20; lfullrt.py).  frs.py (local
  search on U + 2*defects): from lsa6_q548 U 8115 -> ~1850 but defects 108 -> ~590 (symmetry destroyed); from random
  similar.  Block-structured random systems (blocks.py: apex D4 blocks D(A,x) = 3 PPTT frames, cube blocks = 2 TTTT
  frames + 3 P) give U ~ 8000 with 64-82 defects -- blocks alone do not create routability.
- Good-frame closures: PPTT frame -> apex D4 block D({abcd},x) (12 lines, 3 frames); TTTT frame -> cube block on a
  pairing {ab,cd,ef}: 8 transversal T lines (2 TTTT frames) + 3 matching P lines (11 lines).
- Hand analysis (PPTT-framed P(ij), partner pair {k,l}, apex y): P(ij) is unroutable into the section of a PT cell
  {P(ab),T(abx)} iff x not in {k,l,y} and {a,b} meets {k,l} (with {a,b,x} disjoint from {i,j}) -> full routability
  forces every PPTT-framed P line touching k or l to have its apex in {i,j,l,y}: very strong apex coherence.
- fru0.py: exact CP-SAT for fully routable (U = 0) good-frame systems, defects free: running Z11 and no-symmetry.
- PRICE GRID (price/price_2lvl.py, price_0lvl.py; exact pricer, v=220, h=11, 660 deliveries, model of lor_fc_price3):
  uneven jumps are cheaper.  Break-even R vs P111-tuned: zero-level (cell -> section) ~755; one-level mid rank 3/8 ~677,
  4/7 ~642, 5/6 ~632; one-level + target node read rank 3/8 ~656, 4/7 ~616, 5/6 ~603; two-level (3,4),(3,8),(7,8) ~611,
  (3,5),(3,7),(4,5),(4,8),(6,7),(6,8) ~587, (3,6),(5,6),(5,8) ~580, (4,6),(4,7),(5,7) ~570.
- lreach4 (per-rank one-level reach, q548), first cell: rank-3 nodes <= 12 per register, rank 4 <= 18, rank 5 <= 31,
  rank 8 <= 12 -> rank-3/8 one-level designs need ~2x the registers of rank-5 ones; their price advantage cannot
  compensate (full run pending).
- llp/: S11-symmetric LP lower bound for STRICT ONE-LEVEL words over ALL good-frame systems (lp_model.md).
  313 node orbits (closed line sets, rank <= 8, |perp| >= 2); 7 plane-section orbits (2|70 PP, 3|85 PPP, 2|66 PT-disj,
  2|56 PT-inc, 2|61 TT non-orth (2-line plane), 2|56 TT, 3|71 PTT); 1.3M concrete closed sets inside sections.
- RESULT (llp/lpsolve.py, all systems, strict one-level, union coverage): LP optimum = 660 registers exactly (the
  branch-register floor) -> R >= 440 only.  Union-coverage counting cannot separate one-level words from the floor; the
  q548 reach bound (603) comes from that system's cells, not from geometry.  Whatever kills (or allows) one-level words is
  EXACT mod-2 assembly (spans), not coverage.  LP optimum structure (fractional): rank-7 nodes with 21-26 lines and
  7-10-line perps; T targets read TT-nonorthogonal sections ({T(abc),T(def)}, disjoint triples, 61 lines) in-chain,
  P targets PT-disjoint sections (66 lines); ~1.4 deliveries per target from 66/56/70-line sections.
- fru0 (exact CP-SAT, fully routable own-frame systems): Z11 UNKNOWN after 3600 s (no solution; defect bound 4),
  no-symmetry UNKNOWN after 3600 s (no solution; bound 0).  Own-frame U=0 routability remains undecided (not ruled out).
- NEW (llp/lparity3.py, exhaustive per target): PARITY TRIPLES of plane sections with defect ONE line:
  section totals of 3 plane sections through t XOR to 1_{R(t)} + 1_{d} (d in R(t), in none of the 3 sections).
  I_{11,1} P(ab): {ab,ac,bc}+{ab,ad,bd}+{ab,cd} (PPP,PPP,PP; d = P(cd); 36 per target), PPP+PT(inc)+PTT (324),
  PP+PTT+PTT (252).  T(bcd): PT(disj)+PTT+PTT (108), PT+TT*+TT* (700), PTT+PTT+TT (168), PTT+TT+TT* (504)
  (TT* = non-orthogonal disjoint-triple pair, 61-line section).  E8 (I_{9,1} lines): (E6, E6, D6) with defect 1,
  378 per line (vs the frame top (D6,D6,D6) + 3 mates).  A2 sections have 3 users -> fewer sections than frame tops
  (ideal: E8 140 vs 180; I_{11,1} ~257 vs 330).  Earlier E6/A2 work used 4-section UNION covers; the 3-section parity
  version is new.  Caveat: d lies in none of t's sections, so with an in-chain section read (cell read nested inside
  it) d needs a private register; with 3 deliveries (R420-style targets 0 -> cell -> t-perp) the cell read supplies d.
- A3 STRUCTURE (llp/la3.py, exact): the defect-1 parity triples are exactly the A3 subsystems.  For an A3 (6 lines =
  edges of K4; 4 A2 triangles; 3 orthogonal opposite pairs) and a line t in it: tot(Q1-perp) + tot(Q2-perp) +
  tot({t,opp(t)}-perp) = 1_{R(t)} + x_{opp(t)}, Q1, Q2 = the two triangles through t.  E8: 7560 A3s, 378 per line;
  identity verified.  An A3 PARTITION would share every section fully: per block 4 A2 sections (3 users) + 3 cell
  sections (2 users) = 7 sections for 6 targets (frame top: 1.5 per target).  Transposed source side: each line
  branches at its 2 triangles (A2 cells, 3 registers) + its opposite-pair cell -> 3 registers per line, 18 per block.
  The defect target opp(t) reads x_t at the rank-1 frame <t> (keeper read); then no in-chain section read is
  possible (opp(t) lies in none of t's sections), so targets take 3 deliveries (R420-like 0 -> <d> -> t-perp).
  E8 max disjoint A3s: >= 18 found (108 of 120 lines), bound 20 (300 s) - partition existence open; longer run going.
- A3 COMPATIBILITY (llp/la3compat.py, la3clique.py, exact DFS): a block system whose sections meet other blocks only in
  whole cells needs pairwise "compatible" A3s.  E8: 1200 compatible partners per A3; NO compatible A3 partition
  (exhaustive, 1 s); largest compatible packing found 8 blocks.  I_{11,1}: 13,200 A3s (4 orbits), compatible packing
  found 8 blocks (600 s, not proven max).  Random E8 A3 packings: ~37% unroutable (section,line) pairs.
- E8 A3 DESIGN ON R420's D4 PARTITION (llp/e8a3.py, CP-SAT OPTIMAL 3 s): every line takes 2 triangle cells (A2 in its
  block) + 1 pair cell (an R420 cell) forming an A3 (120 distinct A3s, not a partition); self-dual top.  Result:
  0 unroutable incidences, 140 sections (80 E6 + 60 D6) vs R420's 180.  Anatomy (e8a3anat.py): E6 = B' (12) + one chosen
  triangle cell from each of the 8 other blocks; D6 = B' + d-cell + 8 chosen pair cells (= R420's D6).  Each cell is a
  piece of 8 sections.  Per target: B' + 8 more lines lie in all 3 sections, 42 lines in one, d in none.
- Middle for that design (e8a3quad.py, e8a3tri.py): D6 pieces sit in R420's D4 quads (2 per D6, 6 sections per quad);
  E6 pieces: any 4 of them span the whole E6 (rank 6); best shared nodes are rank-4 D4s with 3 pieces serving 4 E6s
  (160 such).  => each E6 needs >= 3 piece arrivals.  R420-style accounting (arrivals = pieces + copies, one delivered
  register per user carrying the full piece sum): E6 5, D6 3 -> 580 registers, R ~ 460 > 420.  The 22% section saving
  is eaten by harder E6 assembly + 3-way copies.  Escape not excluded: cross-section corrections through the 8
  triple-overlap lines (not modelled).
- Same accounting for I_{11,1}: sections of 56-85 lines need kappa >= 3 pieces from shareable nodes (<= ~30 lines);
  registers per target ~ sum over its sections (kappa + users - 1)/users >= 5.3 (A3 top) / 6 (frame top) vs ~3.9 at
  break-even (852-897 registers).  Heuristic accounting, NOT a proof (union-coverage LP allows 660).
- PARITY-TOP LANDSCAPE (llp/lparity_a3s.py, lparity_a3s_e8.py; meet-in-the-middle, exhaustive for the representative
  targets): with sections = plane sections + A3-perp sections (rank-8 frames, 6 users; E8 D5 20 lines, I_{11,1}
  42-56 lines), combinations of <= 4 sections with defect <= 1 are ONLY the A3 triples (E8 378, I11 P 612, T 276) and,
  for I11 T lines, the 1204 triples through non-orthogonal TT pairs.  No 4-section defect-<=1 tops exist, and no
  top uses an A3-perp section.  => tops are frame triples (defect 3) or these triples; sections have <= 3 users.
- TRIPLE-OVERLAP STRUCTURE of I_{11,1} tops (exhaustive over each representative's tops): the 3 sections of a top
  share 25-56 lines (A3 tops 36-56, frame tops 25-30) -- needed once (mod 2), like B' in R420; exclusive parts are
  14-32 lines per section.  For an A3 top the triple part is the A3-perp (42-56 lines, 6 users).
- K4 block analysis (P targets, A3 = K4 on {a,b,c,d}): section {ab,ac,bc}-perp (85) = lines on Q=[11]-abcd (56,
  triple) + 'touching d' (29, exclusive, common to its 3 users).  The closure of the touching-d part is the WHOLE
  section (85 lines, rank 9): no proper node contains it, so kappa_ex >= 2 at any depth.  Per block (6 targets):
  arrivals >= 7 kappa_ex + 11 (6 Q-deliveries + 5 copies as differentiators) -> >= 4.17 registers per target,
  R >~ 697 (one- or two-level) > every break-even (611-677).  The triple part (56 lines) also cannot be assembled
  one-level without ~22 dead registers per block (cell registers carry <= 3 lines; 6 useful outputs).
- kappa (union cover of a whole section by proper closed nodes, llp/lkappa.py): PP section (70 lines) 3 (optimal);
  with shareable nodes (>= |N|/2 sink planes) 4 found.
- EXCLUSIVE-PART CLOSURES (llp/lexcl.py, exhaustive over all 3-section tops of both representatives): for EVERY frame
  triple and EVERY defect-1 triple, each section's exclusive lines (14-43 lines) have closure = the whole section line
  set -> no proper node contains an exclusive part -> every delivery of an exclusive part needs >= 2 node arrivals
  (any depth).  (E8 R420 also has kappa = 2; for I11 this combines with 1.5 cells/target and 25-56-line triple parts.)
- Break-even ratios across I_{n,1} (price/price_i13.py): I10,1 2.56-3.18 v, I11,1 2.78-3.43 v, I13,1 2.90-3.54 v
  (two-level ... zero-level).  An exact R420 analogue (3.5 v) loses in every size, as in E8 (R420 -4.6%).  I13,1 has
  no good-frame parity obstruction (78 P lines, T-T degree sum even) but that only buys R420-type 3.5 v.
- 4-SECTION TOPS (llp/lexcl4.py, 3000 sampled union 4-covers per representative, <= 3 lines left to the rank<=2 read):
  exclusive parts shrink to mostly 5-14 lines and ~85% have PROPER closures -> one node output per delivery
  (kappa_ex = 1) is geometrically possible.  This is the remaining loophole: a zero-waste 4-section design needs every
  node's outputs to be exactly a basis of its input span (users' needed vectors), every cell register used once.
  Earlier exact section-level models of 4-section Lorentzian designs (lsec/lstageS, lhub) hit the node squeeze
  (R >= 880 for design R3; hub-only middle INFEASIBLE) -- not a proof for jointly optimised designs.
- PRICING CORRECTION / NEW: the pricer is extremely sensitive to local rank mass at fixed R (deficit ~0.5% of mW);
  histograms MUST be mass-consistent (sources climb 10, helpers 11, targets 10, totals 10 for I11).  With exact
  counts (price/price_a3exact.py; control: standard one-level rank 5 breaks even at R = 629 as before) the
  A3-PARITY ARCHITECTURE SHAPE prices much better: targets 0 -> <d> -> t-perp (2 moves), copies/differentiators
  without middle node (empties 0-9-10-11, carrier copies 0-1-2-9-10-11), merged-away pieces die without the t-perp
  stop.  Break-even R ~ 777 (rank-5 nodes) / ~811 (rank 3 or 8) vs 629/675 for the standard shapes.
  E8 version (price/price_e8a3.py; R420 control reproduced -4.59%): E8 A3 shape at R = 460 is -5.1..-6.0% -> no E8 gain.
- kappa of EXCLUSIVE parts (llp/lkex.py, exact CP-SAT over maximal proper nodes S & x-perp): EXACTLY 2 for every
  section of every 3-section top (both target types); pieces 12-35 lines.  Full sections need 3 (optimal).
- Shareability of the 2-piece covers (llp/lkex2.py; sinks of pp(piece) vs ceil(|piece|/2) inputs): OK (ratio >= 1)
  for PT-inc 56, PT-disj 66 (|E| 19), PP 70 (|E| 14), PTT 71 (|E| 24), TT 56; NOT for big A2 exclusive parts
  (PPP 85 |E| 29-43, PTT 71 |E| 29-34: ratio 0.54-0.78) and TT* 61 (0.75).  No P-target top is fully shareable;
  T-target (PTT,PTT,TT) tops may be.
- IDEALISED A3 ACCOUNTING (I11): per 6 targets 7 sections x kappa_ex 2 + 11 differentiators (6 Q + 5 copies) = 25
  registers -> R ~ 697 -> +4.3% (rank 5) .. +6.5% (rank 3/8) over P111-tuned IF all pieces shareable.  With the
  measured shareability (A2 sections effectively ~2.7 arrivals) -> R ~ 800 ~ break-even (777-811).  Not yet counted:
  defects, leftover lines outside A3/TT* tops, routability, node-capacity mismatch, keeper-read conflicts.
  STATUS: closest Lorentzian candidate so far -- at break-even in idealised accounting, not a gain.
- PER-TARGET A3 ACCOUNTING with measured shareability (per user of a section: kappa_eff/u + (u-1)/u,
  kappa_eff = 2/min(1, ratio)): best P tops ~4.45-4.54 registers/target (PP+PTT+PTT / PP+PPP+PPP), best T tops
  ~4.17 ((PTT,PTT,TT) with 71|24 sections) -> ~933 registers, R ~ 713 vs A3-shape break-even 777-811 -> +3..5%
  IF realisable.  Caveats: (i) the 6 Q-delivery registers per block need a second middle level (cell -> mid ->
  A3-perp node) to carry the 42-56-line triple part; (ii) users of a shared section have different exclusive parts
  (union larger -> more arrivals) unless they share an A3 block; (iii) block designs: <= 27 disjoint A3s (2+ P lines
  each) -> 58 lines need TT*/frame tops (~5.2/target) -> R ~ 777 ~ break-even; (iv) defects, routability, keeper
  reads, totals not counted.  => ARCHITECTURAL POTENTIAL at break-even +- a few %, not a realised gain.
- CORRECTED A3 PRICING (price/price_a3exact2.py): the 6 Q-delivery registers per block need two middle levels
  (cell -> mid -> A3-perp node (rank 7/8) -> section).  Break-even then R ~ 712 (mid rank 5) .. ~756 (mid rank 3,
  Q-node 8); ideal accounting R = 696 -> only +0.85..+3.4%.  A fully consistent all-A3 design is impossible
  (T lines need 165 PTT triangles but P lines offer only 110 triangle slots) -> >= ~55 T lines on TT*-tops
  (~+1 register each) -> realistic estimate exceeds break-even.  => A3 architecture: break-even at best, loses
  realistically (not proven).
- FRAME-TOP shape with cheap differentiators (price/price_frame.py), I11, R = 770 (330 sections x (2 pieces + 1)):
  -3.5..-5.6% with two-level Q-deliveries (needed: triple parts 25-30 lines); +0.6% only if Q were plain empties
  (impossible).  Frame tops lose; A3-parity tops are the better Lorentzian shape (ideal +0.85..3.4%).
- PRICING CEILING (price/price_ceiling.py): all chains single jumps (sources 1->11, helpers 0->11, targets 0->10)
  give +40% at R = 700 and +27% at R = 875 (hosting wall ~880) -> the loss is in the intermediate stops (chain
  entropy), not in R.  Marginal value of single stops in the A3 shape at R = 696 (price/price_stops.py): source
  section stop 2.2%, target <d> stop 1.6%, piece node/section stops 1.6% each, others 0.1-0.9%.
- A3 SHAPE WITH SEPARATE RANKS (price/price_a3exact3.py): exclusive-part pieces live in S & x-perp nodes (rank 8);
  with pieces at rank 8 the break-even is R ~ 749-757 for every Q-mid rank 3-6 (Q-node 8), ~747 with Q-node 7;
  pieces at rank 7 -> 731, rank 6 -> 719.  => realistic A3 break-even ~750 (rank-8 pieces are the natural ones).
- DESIGN COST MODEL LOWER BOUND (per-line min over defect-1 triples, ignores consistency): 937.4 registers ->
  R >= 717.4 in the e11design2 cost model (P best 4.54 = PPP,PPP,PP; T best 4.17 = PTT 71,PTT 71,PT-disj 66, 84 of
  1480 options).  Room to the ~750 break-even: ~33 registers.
- DEFECT-LINE POSITION in defect-1 triples (exhaustive, both representatives): for every P-line triple and every T-line
  A3 triple the defect line d lies in NONE of the 3 sections (so the target must read x_d at <d> and cannot read a
  section in-chain).  EXCEPTION: 280 of the 700 (61,61,66) TT*-triples per T line have d in 2 sections -> such T
  targets can run 0 -> <d> -> S -> t-perp with an in-chain read of one section (R420-type).  Not yet priced.
- CONSISTENT Z11 DESIGN (llp/e11design2.py; every line a defect-1 triple (A3 or TT*), used planes used by all their
  lines, Z11; cost = per (user, section) kappa_eff/u + (u-1)/u with the MEASURED lkex2 shareability ratios -- all 9
  option signatures are in the table, no defaults): CP-SAT 900 s, 4 workers: UNKNOWN (no feasible design found),
  proven objective bound 1014.42 registers -> R >= 794 for EVERY consistent Z11 design in this cost model, above the
  A3-shape break-even (~757 with rank-8 pieces).  Option costs: P 4.54 (PP70,PPP85|29 x2), 4.73 (PT-disj66,PTT71|24,
  PPP85|38), 4.82 (PP70|28, PTT71|29 x2), 4.92 (PT-inc56, PTT71|29, PPP85|43); T 4.17 (PT-disj66|19, PTT71|24 x2),
  4.54 (TT56|14, PTT71|29 x2), 4.85 (TT56|19, TT*61, PTT71|34), 5.17 (TT*61 x2, PT-disj66|29), 6.44 (TT*61 x2,
  PT-disj66|30).  Scope: consistent + Z11 + this cost model (shareability penalty heuristic).  Running: LP bounds
  without symmetry and without consistency (llp/e11lpdesign.py).
- REACH LEMMA (rigorous, from the checker rules: every gate operand climbs to the gate frame; frames nested).
  Along any content path s_u -> r1 -> r2 -> ... -> target t the gate frames are nested, so t lies in F-perp for every
  frame F on the path.  Let A run over the registers that carry x_u at a frame of rank <= 2 (sources, carriers, cell
  registers of cells containing u, targets reading at rank <= 2), and F_A = A's first frame of rank >= 3.  Then
  R(u) is contained in the union of lines(F_A-perp) (plus targets that read x_u themselves at rank <= 2).
  Max reach |lines(F-perp)| by rank of F (exhaustive over node orbits, llp/nodes.pkl): rank 1: 129, 2: 85, 3: 56,
  4: 36, 5: 25, 6: 17, 7: 11, 8: 6.  E8 control: D4 quads reach 12, R420 9 x 12 = 108 >= 63.
  => I_{11,1} with 3 branches per line and cells of <= 3 lines (<= 8-9 cell-stage registers carry x_u): direct
  cell -> rank-8 node chains reach <= 54 < 115..129 targets: IMPOSSIBLE.  Several cell registers per line need a low
  first stop (rank <= 4..6).  The A3-shape break-even ~757 (price_a3exact3, pieces cell -> 8) was for an infeasible
  shape.
- Self-dual A3 designs, sharper: targets that need x_u only through cell c (u's exclusive targets for that cell,
  14-43) must be covered by the perps of c's registers' first frames F (F-perp <= c-perp & y-perp, a rank-8 node):
  this is exactly the kappa_ex cover, so >= 2 registers per cell take a low first stop (rank 3 = span(c, y)):
  phi >= 2/3 (triangle cells) .. 1 (pair cells).  Prices (price/price_a3mix.py, price_a3reach.py): low stop rank 3,
  phi = 1/4: break-even 755; 1/3: 749; 1/2: 739; phi = 1 (all pieces two-level): 705.  So phi ~ 0.75 -> ~720-725.
- AGGREGATED COUNTING LP for defect-1-triple designs (llp/e11agglp.py; plane-type balance, exact option classes):
  kappa = 2 everywhere (rigorous arrivals model): registers >= 935 -> R >= 715 (consistent or not).  Shareability
  per-option costs, consistent designs: >= 1048.3 -> R >= 828.  (Type-min shareability: 715 / 751.7.)
  => A3/TT* class: rigorous-model floor R >= 715 vs reach-compliant break-even ~720-725 (shape model): at most
  ~1% of room, needing a perfect zero-waste consistent design (none found: e11design2 Z11 UNKNOWN, no solution).
- 4-SECTION / 4-PART kappa=1 SHAPES (price/price_4sec.py, price_4sec2.py): with pieces cell -> 8 -> t-perp (no section
  stop) the ideal R = 660 would give +9.8%, but that shape violates the reach lemma; reach-compliant
  (cell -> m1 -> 8 -> t-perp): +2.2..4.3% at R = 660, break-even ~700-735.
- REACH LEMMA, level k (same proof): R(u) is covered by lines(G_A-perp) over registers A carrying x_u at rank <= k,
  G_A = A's first frame of rank > k.  Rank-8 frames reach <= 6 -> every line needs >= 22 (P) / 20 (T) registers
  carrying it when stepping up to rank >= 8.  With <= 9 cell registers per line, cell registers must MIX at a
  low frame (k_F inputs -> k_F outputs all carrying the group's lines) before rank 8: with groups of ~6, >= 3 low-stop
  registers per line (phi >= 1/3); the level-2 exclusive-target cover gives phi >= 2/3..1 (the binding one).
  Lines x reach Pareto (nodes.pkl): rank 3 (6, 56); 4 (12, 30); 5 (20, 20) [D5 _|_ D5']; 6 (35, 10), (15, 17);
  7 (56, 6), (25, 11); 8 (47, 6).  Best product at rank 5 (D5: 400) vs E8 D4 144.
- IN-CHAIN TT* OPTION (llp/e11agglp2.py): 280 of each T line's (PT-disj, TT*, TT*) tops have d (a P line) in BOTH
  TT* sections, and the other user of each TT* section is also _|_ d -> 0 -> <d> -> S -> t-perp with S read in-chain
  (by both users: 2 arrivals, no differentiator, if their needs coincide).  Aggregated LP (model A + this option,
  optimistic): registers >= 925.83 -> R >= 705.8 (P: all (PPP, PT-disj, PTT); T: 110 (PTT, TT*, TT) + 55 in-chain
  (PT-disj, TT*, TT*_in)).  Window vs reach-compliant break-even (~720-725): <= ~2% under optimistic assumptions.
- PARITY TOPS WITH 4 SECTIONS ARE IMPOSSIBLE (llp/lpar4_min.py, exhaustive numpy pair-xor matching; validated by
  recounting the 3-section defect-1 tops: 612 P / 1480 T): the minimum defect |S1^S2^S3^S4^R(t)| over 4 distinct plane
  sections through t is 42 (both P and T).  3-section tops with defect 2-3 that are in-chain capable (all defect
  lines in one section): NONE (llp/lpar_inchain.py).  => in-chain parity reads exist only via the TT* defect-1 tops
  of T lines.
- EXACT UNION COVERS (llp/lunion_min.py): R(t) = S1 u S2 u S3 exactly for P: 252 (PP, PT-disj, PT-inc) = frame tops;
  T: 1120 ((PTd)^3 420, (PTd, PTi, TT) 84, (PTd, TT*, TT*) 280, (TT)^3 336).  4-section exact union covers: many.
  These are the frame tops of the old main line (union reads with in-chain section, mate corrections).
- The union-coverage LP (R >= 440) is reach-compatible (arrivals from node N go only to sections containing N; nodes
  fan out by mixing), so its gap to realistic words is mod-2 exactness + independence, not reach.
- FRAME UNION TOPS + IN-CHAIN, re-priced with the cheap-chain rules (price/price_frameinchain.py, price_general.py):
  model-A counts (330 pair sections: 220 with an in-chain user cost 2, 110 with two delivered users cost 3) give
  R = 550 (= 3S - v).  Shape: pieces two-level (cell -> low stop m1 -> rank-8 node -> S), dead pieces skip t-perp,
  copies 0-9-10-11, targets 0 -> S0 -> t-perp (exact union covers need no defect read).  At R = 550: +11.25%
  (m1 = 3, phi = 1), +8.9% (m1 = 5); break-even ~739 / ~703.  Break-even map (D deliveries, X extra cell registers):
  targets 0-9-10, m1 3: D 440 X 0 -> 740, X 50 -> 716, X 108 -> 692, X 220 loses; targets 0-2-9-10 about -40.
  (Matches the earlier inch2v estimate: zero-waste in-chain R = 2v = 440 -> +20%, break-even 682-743.)  On the old
  systems (lsa6_q548: >= 667 deliveries, 108 defects) the same rules give -1..+2% at R = 660.  The handoff's
  'R <= 600' target was for a stop-heavy shape; in-chain union shapes allow R up to ~690-740.
- KAPPA = 2 SHARED PARTS: frame-top exclusive parts have full closure (proven earlier), so both users of a pair
  section must receive IDENTICAL parts (only P1 + P2 has full closure in span{P1, P2}).  Then for every line u the
  targets in R(u) are paired by the sections delivering u -> needs a perfect matching of R(u); |R(u)| = 129 / 115 is
  ODD -> >= 1 non-shared delivery per line (>= 220 private incidences; cheap if concentrated in 1-user sections).
- WEAK ROUTABILITY (the real union-top requirement, symmetric): orthogonal pair (t,u) is routable iff some e in M(t),
  f in M(u) have e _|_ u, f _|_ t, e _|_ f (cell {u,f} inside section {t,e}-perp).  Only ONE routable section per
  (t,u) is needed (fru0 demanded every line of every section).  Stored systems (llp/lmatch.py): lsa6_q548 8014
  unroutable (t,u) of 26070, sharing deficiency 12112; nr596 7688; lsa3_best_f 7436.  Annealer llp/lroute_sa.py
  (10k moves/s): random start 4491 unroutable unordered pairs (of 13035) -> 2321 in 20k moves; long runs going.
- A3/TT* full LP (llp/e11lpdesign.py, no symmetry, no consistency): killed at the 50-min limit, no result (the
  aggregated LPs already give the class floors 715 / 705.8).
- WEAK-ROUTABILITY ANNEAL (llp/lroute_sa.py, good frames, LAM 1): unroutable unordered pairs 4491 (random) -> 2 with
  100 non-reciprocal mate incidences after 5.5M moves (still cooling).  LAM 4 got stuck at ~690; 'all covers'
  (lroute_sa2.py, incl. (PTd)^3 and TT* covers) at LAM 2: 233 / 430 mid-run.  => near-complete weak routability IS
  reachable (contrast: fru0's strong condition undecided; stored systems ~7400-8000).
- Top-level evaluator llp/lmatch3.py (per-line sharing matchings with free private deliveries through single-user
  sections, parts, 2-node kappa test, in-chain orientation, model-A count).  lsa6_q548: R ~ 1093.  First-frame layer
  llp/lframe1.py (each cell register picks one rank-3 first frame span(cell, y); a delivery needs a frame inside the
  section): lsa6_q548 covers 15108 / 18056 incidences in 60 s (not optimal).
- WEAK ROUTABILITY U = 0 REACHED (llp/lroute_sa.py seed 11, good frames, LAM 1): every one of the 13,035 orthogonal
  pairs has a routable (cell, section) pair, with 98 non-reciprocal mate incidences.  Z11-symmetric version
  (llp/lroute_z11.py, 20 orbit choices): stuck at U ~ 1750 (symmetric good-frame systems far from routable).
- MIDDLE CAPACITY SCREEN (llp/lmidcap.py): reach forces first frames of rank <= ~5 (inputs carry <= 6 lines at rank
  3, <= 20 at rank 5); pieces sharing a node through a common user are DISJOINT (a target's parts partition R(t));
  a node with k inputs has k outputs (zero waste needs k useful pieces = k sink sections).  lsa6_q548: 702 pieces on
  688 distinct nodes (no sharing), 607 nodes need more inputs than pieces -> ~1880 cell-stage registers vs 660.
  => the frame union line's binding obstacle is node sharing with overlapping content (R420's D4 quads), which needs
  partition-like frame structure (cell lemma, R ~ 770 > break-even ~690-740).
- NO R420-STYLE BLOCK PARTITION (node orbits, nodes.pkl): rank-5 20-line nodes (D5 type, perp 20 or 15) all have 10 P
  lines, so no Z11-transversal D5 (needs 5 P) and no D5 partition (55 P lines); D4 (12 lines, 6 P), A4-type (10 lines,
  4/6/10 P) blocks have even P counts vs 55 P lines (odd); frames impossible (P matching); A3s <= 27 disjoint.  The
  odd number of P lines blocks every balanced self-dual block partition that gives E8 its D4 quads.
- MIDDLE DEPTH vs PRICE for frame union in-chain tops (model-A counts, R = 550 ideal): piece chain middle stops
  (8): +15.9% / BE 808 [reach-infeasible]; (3,8): +11.3% / 740 [needs rank-8 inputs of >= ~17 lines: rank-3 frames
  carry <= 6 -> infeasible with node sharing <= 3]; (5,8): +8.9% / 704 [reach at level 2: 6 x 25 >= 129 ok only with
  max-reach rank-5 frames]; (3,5,8): +5.9% / 656; (4,6,8), (3,5,7): +5.2% / 640.  Register conservation per level
  (k in -> k out; outputs may overlap; identical outputs need empties) + content caps (rank 3: 6, rank 5: 20 lines) +
  reach (>= 22 registers carrying u at rank <= 5 before rank-8 nodes) are consistent with a three-level zero-waste
  middle (6 -> ~24 -> ~72 registers carrying u), which prices at break-even ~656.
- U = 0 SYSTEM EVALUATED (llp/lroute_best_11.json, lfull_eval.sh): 281 reciprocal + 98 single-user sections;
  shared 22,492 / free private 3,374 / differing 204 incidences, unroutable 0; parts kappa: 107 sections need 3
  nodes; top-level model-A R ~ 870 (matching not optimised for kappa).  Middle screen: 544 pieces on 481 nodes
  (423 nodes with 1 piece), 107 parts without 2-node decomposition, ~1,449 cell-stage registers needed vs 660.
  First-frame layer: >= 25,296 / 26,070 incidences covered (240 s, not optimal).  => weak routability alone does not
  help: unstructured systems fail at kappa / node sharing.  Next: structured frames {t, opp_X(t), a, opp_Y(a)} from
  the 27-block A3 packing (A3-perp node shared by the block's 3 opposite-pair sections) - llp/lroute_a3.py running.
- STRUCTURED A3-OPPOSITE FRAMES (llp/lroute_a3.py: block lines of the 27-block A3 packing must take a frame containing
  their A3-opposite, so A3-perp nodes are shared by the block's 3 opposite-pair sections): only 3-13 frame options per
  block line; weak routability stuck at U ~ 1,700-2,150 (good / all covers).  Structure vs routability tension (as Z11).
- CELL-FREE SOURCES (first mixing at rank-3 frames, chain 1 -> 3 -> 5 -> 8): break-even ~688 vs 656 with cells, but
  reach needs R(u) covered by the perps of u's first frames: min cover of R(u) by perps of rank-3 frames through u is
  4 for P and T (CP-SAT found 4; proof of 'no 3-cover' running, llp/lr3cover.py).  Argument: each such perp lies in a
  plane section through u, so 3 of them must refine a 3-section union cover whose exclusive parts have full closure
  (no rank-8 node holds them) - proven for frame/defect-1 triples, CP-SAT check pending for the other covers.
- RANK-8 FRAME SECTIONS (new top class): sections F-perp for rank-3 frames F through t (users = lines of F, 3-6);
  R(t) union-covered by 4 such perps (exists); 1 in-chain (target chain 0 -> F0-perp (8) -> t-perp), 3 delivered
  with DISTINCT parts; in-chain parts read as combinations of the section's delivered outputs -> every cell-stage
  register is a delivery, no copies: R = 440 in counting.  Prices (price/price_r8sec.py), R = 440: cells + middle
  stops (3,5): +13.5%, break-even 662; cells (5): +16.9% / 710; cells (3): +19.7% / 746; no cell (3,5): +16.0% / 698.
  (Matches the earlier inch2v +19.7..23.4% at R = 2v.)  All-A3 version impossible by counting (each A3 has >= 2 P
  lines: 147 A3s need >= 294 P-incidences > 220).  Z11 design CP-SAT (llp/lr8design.py, 84,205 frame orbits:
  sizes 3: 59,360, 4: 21,755, 5: 1,890, 6: 1,200) running: each line in exactly 4 used frames + every orthogonal pair
  covered.
- RANK-8 SECTIONS, refined requirement: full consistency is NOT needed.  Delivered parts are per-target registers
  (free subsets of their section perps, partitioning R(t) with the in-chain part); only each target's single in-chain
  part must be a combination of delivered co-users' parts on that section (simplest: identical to one co-user b's
  delivered part, A_in(t) = A_F(b) within F-perp, F containing t and b).  Registers = 660 deliveries -> R = 440.
  Middle (the crux): each section node F-perp with k delivered users needs k inputs (zero waste) whose span contains
  the k parts; inputs from rank-5 mids carry <= 20 lines; per line u >= ~97 delivered parts contain u, reachable by
  fan-out 6 cell registers -> ~24 at rank 3 -> ~50 at rank 5 -> ~150 parts (counting OK); exact GF(2) content with
  every target's 4 parts summing to R(t) is the open problem (needs algebraic structure, as R420's D4 quads).
- EXCLUSIVE PARTS OF ALL EXACT UNION COVERS (llp/lexcl_union.py): P: all 252 covers (= good frames) have NO section
  whose exclusive part fits a proper rank-8 node -> P lines cannot be covered by 3 perps of rank-3 frames (rigorous:
  such a 3-cover refines an exact 3-section union cover {t,a_i}-perp and needs each exclusive part inside one rank-8
  node).  T: the 420 (PT-disj)^3 covers (not good frames: {T, 3 disjoint P lines}) have ALL THREE exclusive parts
  inside proper rank-8 nodes (kappa_ex = 1!); the 420 good frames and 280 TT* covers have none.  So T lines may admit
  3-covers by rank-8 nodes (3 sections, kappa = 1, 2 deliveries per T target) - CP-SAT check running.
- PROVEN (llp/lr3cover_exact.py, exhaustive): NO line has R(t) covered by 3 perps of rank-3 frames through t
  (= 3 rank-8 nodes).  Reduction: every rank-3 frame F through t contains a line a with {t,a} a 2-line plane, so
  F-perp lies in the pair section {t,a}-perp; a 3-cover refines an exact 3-section pair cover (covers3.pkl: P 252,
  T 1120) with nodes N_i = S_i & x-perp containing the exclusive parts.  P: no cover has any exclusive part inside a
  node; T: 11,340 node triples from the 420 (PT-disj)^3 covers, none covers R(t).  Consequences: rank-8-section tops
  need >= 4 sections per target; sources whose first mixing is at rank >= 3 (no cells) need >= 4 branches (unless
  targets read x_u at rank <= 2).  (lr3cover.py CP-SAT: P case UNKNOWN at 600 s - superseded.)
- RANK-8 SECTIONS, overhead sensitivity (cells, stops 3,5): extra dead empties: R 480 +10.9%, 520 +8.3%, 560 +5.8%,
  600 +3.5%, 640 +1.3%, 660 +0.2%.  In-chain parts NOT spanned by co-users' delivered parts need their own full piece
  (dies at the node): 55 -> +8.1%, 110 -> +3.2%, 220 -> -5.4%.  Matching-based symmetric T frames {T, P_x, P_y}
  (perfect matching of the other 8 points) never cover R(T) (32 lines always missed).  Zero waste needs, at every
  section node F-perp, exactly (#delivered users of F) <= 6 inputs (registers that reach F-perp can only be delivered
  to users of F), each carrying <= 20 lines (rank-5 mids).
- RANK-8 MIDDLE MODEL (spec for the exact layer, not yet built).  Given: top (4 section frames per target, in-chain
  choice), delivered parts A_b(F) per (delivered user, section) and in-chain parts in their span; source cells =
  3 pair cells per line from an exact union cover (reach rank 2: pair sections cover R(u)).
  Registers: 660 = one per (line, cell) branch.  Path of register r: cell c(r) (2) -> first frame F'(r) = span(c, y)
  (rank 3) -> mid M(r) (rank 5, F' inside M) -> section node N(r) = F-perp (rank 8, M inside F-perp) -> delivered to a
  user b of F with b's part.  Nesting needs c(r) inside F-perp, i.e. both lines of the cell _|_ every line of F.
  Mixing: at every node (cell, F', M, F-perp) the registers present undergo an invertible GF(2) map; content-in-frame
  at each level.  Zero waste: at section node F-perp, #registers = #delivered users of F, outputs = their parts.
  Necessary checks first: per section node, span{A_b} has a basis of rank-<=5-supported vectors (lr8midcheck.py);
  per mid, its outputs (one per section node it feeds) must be supported in M (<= 20 lines); per line u, its <= 6
  cell registers must fan out to every delivered part containing u (reach, fan-out counts OK on average).
- I11 strict rank-8 design (llp/lr8design.py, Z11, every line in exactly 4 used frames): 1500 s FEASIBLE but only
  1804 / 2370 rep (t,u) pairs covered (264 frames: 231 x 3-line, 22 x A3, 11 x 5-line); not a design; undecided.
- E8 4-COVER ARCHITECTURE (earlier this session, e8lean notes): all 4-covers of R(t) by rank-5 flats are
  (D5, D5, D5, A5) = perps of three A3s through t (pairwise meeting only in t) + Z = t x A2 (A5 single-user ->
  1 assembly leftover per target).  5,040 covers per target (re-derived: e8r5/e8cov2.py, mapped by reflections).
  Registers 3 deliveries + 1 leftover per target = 480 -> R = 360 IF every in-chain (pre-reader) part rides free
  on co-users' delivered parts; otherwise R ~ 480.  Price at R = 360 (cells -> 3 -> D5 node -> t-perp): +7.4%
  (also the earlier exact 1.86135e-3).  The free-riding question was never resolved -> decisive test now.
- E8 FREE-RIDING TEST (scratchpad e8r5/): locally every pair of users of an A3 can get identical parts on X-perp
  (791 achievable parts per user, sizes 15-20).  Globally: a cover selection with a potential host for all 120
  targets exists (annealer e8host_sa.py), but the EXACT parts layer (e8parts.py: multiply-covered lines assigned once
  per target, host delivered with identical part) hosts only 53-58 of 120 (OPTIMAL for those selections); exact-
  objective annealing running.  Exclusive parts: D5 parts 15 lines, A5 part 12 lines, all of closure rank 5
  (span their sections) -> A5 single-user leftover is unavoidable.  Realistic E8 price (deliveries 360 + U,
  120 A5 leftovers, rank-3 middle stop, unhosted targets fully delivered): U = 0 -> R 360 +1.5%; U 30 -> -2.1%;
  U 60 -> -5.4% (no-middle shape +6.5% at U = 0 is reach-infeasible).  => E8 4-cover potential <= ~1.5%.
- E8 hosting structure (best selection, 58 hosted): host relations 58; hosts are NOT A3-opposites mostly (8 orthogonal,
  50 not); hosts serving 1 / 2 / 3 riders: 49 / 3 / 1; NO host is itself hosted.  If general, hosted <= v - #hosts
  ~ v/2 (one rider per host) -> E8 4-cover U >= ~60 -> loses.  Same mechanism may cap I11 rank-8 hosting at ~v/2
  (U ~ 110 -> R ~ 550, ~+3% before other overheads).  To test on I11 (lr8host_sa.py on frame-seeded covers).
- I11 RANK-8 COVER POOL (llp/lr8covers.py, vectorised greedy seeded from every frame with perp >= 40): ~1,640 covers per
  P line, ~630 per T line (Z11 rotations of the 20 orbit reps).  Exact hosting annealer (llp/lr8host_sa.py, targeted
  'co-user adopts the shared frame' moves, CP-SAT exact hosting per step ~0.2 s): started 17:38.
- I11 hosting structure at 75 hosted (llp/lr8host_anal.py): riders per host 1/2/3 = 44/14/1; 4 hosts are themselves
  hosted (E8: 0); host _|_ rider 26, not 49; hosting frames mostly A3 (62 of 75; 6-user sections).  The E8 v/2 cap
  mechanism does not hold strictly in I11.
- I11 rank-8 LEFTOVER PROBLEM (lr8host_anal.py on the 82-hosted OPTIMAL selection): 794 used sections, 414 of them have
  exactly one delivered user (each +1 assembly leftover, conservative) -> R ~ 440 + U + L ~ 990.  Hosting-only
  objective is the wrong target.  New objective cost = U + L (lr8host_sa2.py, exact hosting layer): SA from random
  covers ~1000 -> ~930 in 3 min (slow; single-target moves cannot create shared frames).
- Z11-symmetric pool CP-SAT relaxation (llp/lr8poolmip.py: choose cover + in-chain frame per orbit rep; hosted = in-
  chain frame delivered by some co-user; single = frame orbit with exactly one delivered user; no exact part identity):
  U + L = 506 at 52 s, 484 at 97 s (still improving).  Break-even needs U + L <= ~222 (R <= 662).
- EXHAUSTIVE 4-covers (llp/lr8allcovers.py): frames through t: P 11,515 in 24 Stab(t)-orbits, T 14,945 in 29 orbits;
  exact enumeration of covers per orbit representative running.
- Conservative Z11 pool MIP (all single-delivered sections cost 1): U+L 429 at 165 s (stopped; superseded).
- LEFTOVER RULE CORRECTED (cost model above: "a single spanning needer needs 2 arrivals"): a section costs an assembly
  leftover only if its ONLY delivered user's part spans the rank-8 node.  Exclusive parts of pool covers: P rank 5-7
  (never 8), T rank 5-8 (rank 8 in ~13%).  A rank-7 exclusive part stays non-spanning iff every multiply-covered line
  assigned to it lies in span(ex) (exact).
- SPANNING-AWARE Z11 pool MIP (llp/lr8poolmip2.py, relaxation: hosting = co-user delivers the in-chain frame, no part
  identity; leftover only for forced rank-8 exclusive parts): OPTIMAL 0 in 228 s (every rep hosted, no leftover).
- EXACT checks of MIP2 designs:
  - non-equivariant exact layer (llp/lr8exact2.py, 300 s FEASIBLE) on an early MIP2 snapshot: hosted 119, U 101,
    spanning leftovers L 4 -> U + L = 105, R ~ 545.
  - Z11-equivariant exact layer (llp/lr8z11.py, OPTIMAL) on the final MIP2 design: 9 of 20 rep orbits hosted, L 0 ->
    U + L = 121, R ~ 561.
- Price with the extras as full delivered pieces (realistic; dead-empty pricing is optimistic): U+L = 0 +13.5%,
  50 +8.4%, 105 +3.2%, 150 -0.7%, 200 -4.7% (cells, mids 3,5); cell-free 3,5: 105 +5.6%, 150 +1.6%.
  Break-even U + L ~ 140 (cells) / ~170 (cell-free).  => rank-8 sections now have a COUNTING-MODEL margin of ~+3%
  (exact hosting/leftovers; middle layer, reach and word NOT yet built).
- EXHAUSTIVE 4-covers per P line (llp/lr8allcovers.py): 65,170 (greedy pool had ~1,640).  Frame orbits that occur in
  covers (Stab(t)-orbit size: covers containing rep): A3 36:2520, 84:925, 252:70, 252:10, 280:19, 378:25, 378:25,
  504:10, 756:10, 1260:3, 1260:25; the other 13 frame orbits occur in NO 4-cover.
