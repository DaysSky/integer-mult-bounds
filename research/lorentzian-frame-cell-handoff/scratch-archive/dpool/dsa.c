// SA over decoder piece sets drawn from a pool of low-rank supports. Target t is served iff its membership vector
// m_t (bit j = t in piece j) is not in span{m_s : s in N(t)}.  Minimise unserved + lambda*max(0, cost-budget).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define MAXV 400
#define MAXP 20000
#define MAXK 24
int V, n; int lab[MAXV]; int nN[MAXV], nR[MAXV]; int Nl[MAXV][MAXV], Rl[MAXV][MAXV];
int P; int prank[MAXP]; int pnl[MAXP]; unsigned char pbit[MAXP][MAXV];
int K, budget; int sel[MAXK];
static int served(int t, unsigned *m){
    unsigned b[MAXK]; memset(b, 0, sizeof(b));
    for (int i = 0; i < nN[t]; i++){ unsigned x = m[Nl[t][i]];
        for (int bit = K-1; bit >= 0 && x; bit--) if (x >> bit & 1){ if (b[bit]) x ^= b[bit]; else { b[bit] = x; break; } } }
    unsigned x = m[t];
    for (int bit = K-1; bit >= 0 && x; bit--) if ((x >> bit & 1) && b[bit]) x ^= b[bit];
    return x != 0;
}
int eval(int *unserved_list){
    unsigned m[MAXV]; memset(m, 0, sizeof(m));
    for (int j = 0; j < K; j++) for (int s = 0; s < V; s++) if (pbit[sel[j]][s]) m[s] |= 1u << j;
    int u = 0; for (int t = 0; t < V; t++) if (!served(t, m)){ if (unserved_list) unserved_list[u] = t; u++; }
    return u;
}
int cost(){ int c = 0; for (int j = 0; j < K; j++) c += prank[sel[j]]; return c; }
int main(int argc, char **argv){
    FILE *f = fopen(argv[1], "r"); FILE *fp = fopen(argv[2], "r");
    K = atoi(argv[3]); budget = atoi(argv[4]); long iters = atol(argv[5]); double T0 = atof(argv[6]); srand(atoi(argv[7]));
    int maxrank = argc > 8 ? atoi(argv[8]) : 10;
    if (fscanf(f, "%d %d", &V, &n) != 2) return 1;
    for (int t = 0; t < V; t++) if (fscanf(f, "%d", &lab[t]) != 1) return 1;
    for (int t = 0; t < V; t++){ if (fscanf(f, "%d", &nN[t]) != 1) return 1; for (int i = 0; i < nN[t]; i++) if (fscanf(f, "%d", &Nl[t][i]) != 1) return 1;
        if (fscanf(f, "%d", &nR[t]) != 1) return 1; for (int i = 0; i < nR[t]; i++) if (fscanf(f, "%d", &Rl[t][i]) != 1) return 1; }
    P = 0; char buf[1000]; int r, nl;
    while (fscanf(fp, "%d %d %s", &r, &nl, buf) == 3){ if (r > maxrank) continue; prank[P] = r; pnl[P] = nl; for (int s = 0; s < V; s++) pbit[P][s] = buf[s] == '1'; P++; }
    fprintf(stderr, "pool %d (rank <= %d)\n", P, maxrank);
    for (int j = 0; j < K; j++) sel[j] = rand() % P;
    if (argc > 9 && !strcmp(argv[9], "b0")){ int j = 0; for (int p = 0; p < P && j < K; p++) if (prank[p] == 10 && pnl[p] == 90) sel[j++] = p; fprintf(stderr, "b0 init %d pieces\n", j); }
    double lam = 3.0;
    int cu = eval(NULL); int cc = cost(); double cur = cu + lam * fmax(0, cc - budget); double best = cur; int bestsel[MAXK]; memcpy(bestsel, sel, sizeof(sel));
    for (long it = 0; it < iters; it++){
        double T = T0 * (1.0 - (double)it / iters) + 0.05;
        int j = rand() % K; int old = sel[j]; sel[j] = rand() % P;
        int u = eval(NULL); int c = cost(); double nv = u + lam * fmax(0, c - budget);
        if (nv <= cur || exp(-(nv - cur) / T) > (double)rand() / RAND_MAX){ cur = nv; cu = u; cc = c; if (cur < best){ best = cur; memcpy(bestsel, sel, sizeof(sel)); } }
        else sel[j] = old;
        if (it % 5000 == 0) fprintf(stderr, "it %ld T %.2f cur %.1f (unserved %d cost %d) best %.1f\n", it, T, cur, cu, cc, best);
    }
    memcpy(sel, bestsel, sizeof(sel)); int ul[MAXV]; int u = eval(ul);
    printf("best unserved %d cost %d pieces:", u, cost()); for (int j = 0; j < K; j++) printf(" %d(r%d)", sel[j], prank[sel[j]]); printf("\n");
    return 0;
}
