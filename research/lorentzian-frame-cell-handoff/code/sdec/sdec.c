// Simulated annealing for sparse binary decoders: points U[u] in F2^k (k<=16). For each target t, the valid
// functionals W satisfy <W,U[u]>=0 for u in N(t) and <W,U[t]>=1. Row weight = 1 + #{u in R(t): <W,U[u]>=1}, minimised
// over valid W. Infeasible target (U[t] in span U[N(t)]) costs PEN. Objective = sum over targets.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define MAXV 400
int V, n, K;
int lab[MAXV];
int nN[MAXV], nR[MAXV];
int Nl[MAXV][MAXV], Rl[MAXV][MAXV];
unsigned U[MAXV];
int PEN = 400;
static inline int par(unsigned x){ return __builtin_parity(x); }
// returns row weight (>=1) or PEN if infeasible; also writes best W
int target_cost(int t, unsigned *bestW){
    // basis of span U[N(t)] in reduced echelon (pivot = highest bit)
    unsigned basis[16]; int piv[16]; int d = 0;
    unsigned b[16]; memset(b, 0, sizeof(b)); // b[bit] = vector with pivot bit
    for (int i = 0; i < nN[t]; i++){
        unsigned x = U[Nl[t][i]];
        for (int bit = K-1; bit >= 0 && x; bit--) if (x >> bit & 1){ if (b[bit]) x ^= b[bit]; else { b[bit] = x; d++; break; } }
    }
    unsigned x = U[t];
    for (int bit = K-1; bit >= 0 && x; bit--) if ((x >> bit & 1) && b[bit]) x ^= b[bit];
    if (!x) return PEN;
    // enumerate W: valid W = functionals vanishing on span(b) with <W,U[t]>=1. Enumerate all 2^K W? K<=13 -> 8192;
    // cheaper: find complement basis of annihilator. Do brute force over annihilator via Gaussian on dual.
    // Build matrix rows = basis vectors; solve <W,row>=0. Free variables = non-pivot bits.
    // Reduce b to fully reduced form
    for (int bit = K-1; bit >= 0; bit--) if (b[bit]) for (int b2 = K-1; b2 >= 0; b2--) if (b2 != bit && b[b2] && (b[b2] >> bit & 1)) b[b2] ^= b[bit];
    int freeb[16], nf = 0; for (int bit = 0; bit < K; bit++) if (!b[bit]) freeb[nf++] = bit;
    int best = 1 << 30; unsigned bw = 0;
    for (unsigned m = 0; m < (1u << nf); m++){
        unsigned W = 0;
        for (int i = 0; i < nf; i++) if (m >> i & 1) W |= 1u << freeb[i];
        // pivot bits determined: for each pivot row r (pivot p): <W,r>=0 -> W_p = parity(W & r & ~(1<<p))
        for (int bit = 0; bit < K; bit++) if (b[bit]){ unsigned r = b[bit]; if (par(W & r & ~(1u<<bit))) W |= 1u << bit; }
        if (!par(W & U[t])) continue;
        int w = 1;
        for (int i = 0; i < nR[t]; i++) w += par(W & U[Rl[t][i]]);
        if (w < best){ best = w; bw = W; }
    }
    if (bestW) *bestW = bw;
    return best;
}
int cost[MAXV];
long total(){ long s = 0; for (int t = 0; t < V; t++){ cost[t] = target_cost(t, NULL); s += cost[t]; } return s; }
int main(int argc, char **argv){
    FILE *f = fopen(argv[1], "r"); K = atoi(argv[2]); long iters = atol(argv[3]); double T0 = atof(argv[4]); int seed = atoi(argv[5]);
    int init = argc > 6 ? atoi(argv[6]) : 0;   // 0: B0 labels + random extra bits; 1: random
    srand(seed);
    if (fscanf(f, "%d %d", &V, &n) != 2) return 1;
    for (int t = 0; t < V; t++) if (fscanf(f, "%d", &lab[t]) != 1) return 1;
    for (int t = 0; t < V; t++){
        if (fscanf(f, "%d", &nN[t]) != 1) return 1; for (int i = 0; i < nN[t]; i++) if (fscanf(f, "%d", &Nl[t][i]) != 1) return 1;
        if (fscanf(f, "%d", &nR[t]) != 1) return 1; for (int i = 0; i < nR[t]; i++) if (fscanf(f, "%d", &Rl[t][i]) != 1) return 1;
    }
    for (int u = 0; u < V; u++){
        if (init == 0){ U[u] = lab[u]; for (int b = n; b < K; b++) if (rand() & 1) U[u] |= 1u << b; }
        else U[u] = rand() & ((1u << K) - 1);
    }
    long cur = total(), best = cur;
    unsigned bestU[MAXV]; memcpy(bestU, U, sizeof(U));
    fprintf(stderr, "init total %ld\n", cur);
    for (long it = 0; it < iters; it++){
        double T = T0 * (1.0 - (double)it / iters) + 1e-3;
        int u = rand() % V; int bit = rand() % K;
        U[u] ^= 1u << bit;
        long nt = 0; int nc[MAXV];
        for (int t = 0; t < V; t++){ nc[t] = target_cost(t, NULL); nt += nc[t]; }
        long delta = nt - cur;
        if (delta <= 0 || exp(-delta / T) > (double)rand() / RAND_MAX){ cur = nt; memcpy(cost, nc, sizeof(int)*V); if (cur < best){ best = cur; memcpy(bestU, U, sizeof(U)); } }
        else U[u] ^= 1u << bit;
        if (it % 2000 == 0){ int inf = 0; for (int t = 0; t < V; t++) inf += cost[t] >= PEN; fprintf(stderr, "it %ld T %.2f cur %ld best %ld infeasible %d\n", it, T, cur, best, inf); }
    }
    memcpy(U, bestU, sizeof(U)); total();
    printf("best %ld\n", best);
    for (int u = 0; u < V; u++) printf("%u %d\n", U[u], cost[u]);
    return 0;
}
