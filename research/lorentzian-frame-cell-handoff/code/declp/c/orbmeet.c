/* For a line set Y of I_{11,1} (lines = 2- or 3-subsets of 11 points, indexed 0..219) and a list of flats
   (220-bit masks), count for every flat the number of permutations sigma in S11 with sigma(Y) meeting the flat,
   and the number of sigma with sigma(Y) == Y (stabiliser order).  Exhaustive over all 11! permutations (Heap).
   input (stdin): nY, then nY lines "k p1 .. pk"; then a 220-entry table "k p1 .. pk" giving each line index's
   points; then nF, then nF lines of 4 uint64 masks.  output: stab, then nF counts. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static int lidx[11][11][12];   /* lidx[a][b][c] for sorted a<b<c (c=11 means P line {a,b}) */
int main(void) {
    int nY; if (scanf("%d", &nY) != 1) return 1;
    int yk[64], yp[64][3];
    for (int i = 0; i < nY; i++) { scanf("%d", &yk[i]); for (int j = 0; j < yk[i]; j++) scanf("%d", &yp[i][j]); }
    memset(lidx, -1, sizeof lidx);
    for (int l = 0; l < 220; l++) {
        int k, p[3]; scanf("%d", &k); for (int j = 0; j < k; j++) scanf("%d", &p[j]);
        if (k == 2) lidx[p[0]][p[1]][11] = l; else lidx[p[0]][p[1]][p[2]] = l;
    }
    int nF; scanf("%d", &nF);
    uint64_t (*F)[4] = malloc(sizeof(uint64_t[4]) * nF);
    for (int f = 0; f < nF; f++) for (int w = 0; w < 4; w++) scanf("%llu", (unsigned long long *)&F[f][w]);
    long long *cnt = calloc(nF, sizeof(long long)); long long stab = 0;
    uint64_t Ym[4] = {0, 0, 0, 0};
    /* own mask of Y */
    for (int i = 0; i < nY; i++) {
        int a = yp[i][0], b = yp[i][1], c = yk[i] == 3 ? yp[i][2] : 11;
        int l = lidx[a][b][c]; Ym[l >> 6] |= 1ULL << (l & 63);
    }
    int s[11], c[11]; for (int i = 0; i < 11; i++) { s[i] = i; c[i] = 0; }
    long long nperm = 0;
    for (;;) {
        uint64_t m[4] = {0, 0, 0, 0};
        for (int i = 0; i < nY; i++) {
            int q[3]; for (int j = 0; j < yk[i]; j++) q[j] = s[yp[i][j]];
            /* sort */
            if (yk[i] == 2) { if (q[0] > q[1]) { int t = q[0]; q[0] = q[1]; q[1] = t; } q[2] = 11; }
            else { if (q[0] > q[1]) { int t = q[0]; q[0] = q[1]; q[1] = t; } if (q[1] > q[2]) { int t = q[1]; q[1] = q[2]; q[2] = t; }
                   if (q[0] > q[1]) { int t = q[0]; q[0] = q[1]; q[1] = t; } }
            int l = lidx[q[0]][q[1]][q[2]]; m[l >> 6] |= 1ULL << (l & 63);
        }
        if (m[0] == Ym[0] && m[1] == Ym[1] && m[2] == Ym[2] && m[3] == Ym[3]) stab++;
        for (int f = 0; f < nF; f++)
            if ((m[0] & F[f][0]) | (m[1] & F[f][1]) | (m[2] & F[f][2]) | (m[3] & F[f][3])) cnt[f]++;
        nperm++;
        /* Heap's algorithm, iterative */
        int i = 1;
        while (i < 11 && c[i] >= i) { c[i] = 0; i++; }
        if (i >= 11) break;
        if (i % 2 == 0) { int t = s[0]; s[0] = s[i]; s[i] = t; } else { int t = s[c[i]]; s[c[i]] = s[i]; s[i] = t; }
        c[i]++;
    }
    printf("%lld %lld\n", nperm, stab);
    for (int f = 0; f < nF; f++) printf("%lld\n", cnt[f]);
    return 0;
}
