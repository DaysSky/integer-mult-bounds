# One-level LP lower bound (I_{11,1}, all good-frame systems)

Class (strict one-level frame-cell words):
- every source has exactly 3 branch registers whose first mixing is at the 3 cells of a good frame
  (forced for 3 branches; extra branches or empties are "extra registers");
- every register visits at most ONE frame of rank 3..8 ("middle frame"), then at most one rank-9 frame, t-perp, FULL;
- targets visit no middle frame (chain 0 -> rank<=2 -> rank 9 -> t-perp).

Relaxation (each step only enlarges the feasible set, so the LP optimum is a valid lower bound):
1. Union coverage: every u in R(t) lies in the support of some register t reads (mod-2 exactness dropped).
2. Node of a register = pp(lines of its middle frame) (or of its last rank<=2 frame): more lines, no fewer sinks.
3. Lines available at a node <= 2 * (#registers entering it) + (#registers entering from A2 planes); a register entering
   from an A2 plane is an extra register (not one of the 660 branch registers): T >= 660 + #(3-line registers).
4. Sinks: plane sections pm(pi) (users = lines of pi).  Direct node -> t-perp deliveries are dominated by routing
   through a plane section {t, e}-perp with e in pm(N) (same cost, same coverage).  Nodes with pm(N) = {t} (private) and
   private rank-9 frames give <= 3 lines per register to one target ("PRIV").
5. A target reads: one rank<=2 chain (<= 3 lines, plus PRIV), ONE plane section in-chain (union of all arrivals'
   supports), and delivered registers (each is one arrival of a section it is a user of; union of arrivals' supports).
6. An arrival from node N to section S covers every line available at N (w <= min(y, z)).
7. S11 symmetry: the LP is S11-invariant; an invariant optimum exists, so variables are orbit values.

R >= T_LP - 220 (T counts all registers, v = 220 sources included).
