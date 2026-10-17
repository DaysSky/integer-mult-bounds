/* Exhaustive F_2 schedule search with splits.  usage: splitc K s maxsplits seq...   (seq of s pair indices)
   Prints every feasible split set (as list of (pair,time)) found at the end.
   Rows: 2i = X_i, 2i+1 = Y_i; row bits: coordinate 2i = x_i, 2i+1 = y_i.  One split (idle pair joining the transform
   at the junction level) per time at most.  Potential pruning: every local after the first lowers
   rank(XX)+rank(YY) by exactly one. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned long long u64;
static int K, S, MAXS, seq[32];
static int rank8(unsigned v[], int n) {   /* rank over F2 of n bytes */
    unsigned a[8]; int r = 0; for (int i = 0; i < n; i++) a[i] = v[i];
    for (int bit = 0; bit < 8 && r < n; bit++) {
        int p = -1; for (int i = r; i < n; i++) if (a[i] >> bit & 1) { p = i; break; }
        if (p < 0) continue; unsigned t = a[p]; a[p] = a[r]; a[r] = t;
        for (int i = 0; i < n; i++) if (i != r && (a[i] >> bit & 1)) a[i] ^= a[r];
        r++;
    }
    return r;
}
static inline unsigned row(u64 M, int i) { return (M >> (8 * i)) & 0xff; }
static inline u64 setrow(u64 M, int i, unsigned v) { return (M & ~(0xffULL << (8 * i))) | ((u64)v << (8 * i)); }
static int pot(u64 M) {
    unsigned xx[4], yy[4];
    for (int i = 0; i < K; i++) { xx[i] = row(M, 2 * i) & 0x55; yy[i] = row(M, 2 * i + 1) & 0xaa; }
    return rank8(xx, K) + rank8(yy, K);
}
static u64 loc(u64 M, int q, int rev) {
    if (rev) return setrow(M, 2 * q, row(M, 2 * q) ^ row(M, 2 * q + 1));
    return setrow(M, 2 * q + 1, row(M, 2 * q + 1) ^ row(M, 2 * q));
}
/* GL_k(F2) matrices as arrays of k row-masks */
static int ngl[4]; static unsigned char gl[4][200][3];
static void mkgl(int k) {
    int n = 0;
    for (int code = 0; code < (1 << (k * k)); code++) {
        unsigned v[3]; for (int i = 0; i < k; i++) v[i] = (code >> (k * i)) & ((1 << k) - 1);
        if (rank8(v, k) == k) { for (int i = 0; i < k; i++) gl[k][n][i] = v[i]; n++; }
    }
    ngl[k] = n;
}
static u64 tr(u64 M, int *ps, int k, unsigned char *A, unsigned char *B) {
    unsigned xs[3], ys[3]; u64 R = M;
    for (int i = 0; i < k; i++) { xs[i] = row(M, 2 * ps[i]); ys[i] = row(M, 2 * ps[i] + 1); }
    for (int i = 0; i < k; i++) {
        unsigned nx = 0, ny = 0;
        for (int j = 0; j < k; j++) { if (A[i] >> j & 1) nx ^= xs[j]; if (B[i] >> j & 1) ny ^= ys[j]; }
        R = setrow(R, 2 * ps[i], nx); R = setrow(R, 2 * ps[i] + 1, ny);
    }
    return R;
}
/* hash set of (M, mask) */
typedef struct { u64 m, k; } ent;
typedef struct { ent *t; size_t cap, n; } hset;
static void hinit(hset *h, size_t cap) { h->cap = cap; h->n = 0; h->t = calloc(cap, sizeof(ent)); }
static inline size_t hh(u64 m, u64 k) { u64 x = m * 0x9E3779B97F4A7C15ULL ^ (k + 0x632BE59BD9B4E019ULL) * 0xBF58476D1CE4E5B9ULL; x ^= x >> 31; return x; }
static int hadd(hset *h, u64 m, u64 k) {   /* key k stored +1 so 0 = empty */
    if (h->n * 2 > h->cap) {
        hset g; hinit(&g, h->cap * 2);
        for (size_t i = 0; i < h->cap; i++) if (h->t[i].k) { size_t j = hh(h->t[i].m, h->t[i].k) % g.cap; while (g.t[j].k) j = (j + 1) % g.cap; g.t[j] = h->t[i]; g.n++; }
        free(h->t); *h = g;
    }
    size_t j = hh(m, k + 1) % h->cap;
    while (h->t[j].k) { if (h->t[j].m == m && h->t[j].k == k + 1) return 0; j = (j + 1) % h->cap; }
    h->t[j].m = m; h->t[j].k = k + 1; h->n++; return 1;
}
static int act[8][32], nact[8]; static u64 allowed = ~0ULL;
static int interior(int r, int b) {
    int last = -1, nxt = S;
    for (int i = 0; i < nact[r]; i++) { int j = act[r][i]; if (j < b && j > last) last = j; if (j >= b && j < nxt) nxt = j; }
    return (last + 1) < b && b < nxt;
}

/* RREF basis of a set of k bytes (k <= 2 here), returned sorted descending in out[0..k-1] (zeros last). */
static void rref_bytes(unsigned *v, int k) {
    int r = 0;
    for (int bit = 7; bit >= 0 && r < k; bit--) {
        int p = -1; for (int i = r; i < k; i++) if (v[i] >> bit & 1) { p = i; break; }
        if (p < 0) continue; unsigned t = v[p]; v[p] = v[r]; v[r] = t;
        for (int i = 0; i < k; i++) if (i != r && (v[i] >> bit & 1)) v[i] ^= v[r];
        r++;
    }
}
static int lastact[8];
/* canonical form for the boundary b+1 (next transform includes GL on pairs base = {p_b, p_{b+1}} if distinct);
   frozen pairs (no later activity, no split budget left) keep only x-part of X row and y-part of Y row. */
static u64 canon(u64 M, int b, int used) {
    if (b + 1 < S && seq[b] != seq[b + 1]) {
        int p = seq[b], q = seq[b + 1];
        unsigned xs[2] = { row(M, 2 * p), row(M, 2 * q) }, ys[2] = { row(M, 2 * p + 1), row(M, 2 * q + 1) };
        rref_bytes(xs, 2); rref_bytes(ys, 2);
        M = setrow(M, 2 * p, xs[0]); M = setrow(M, 2 * q, xs[1]);
        M = setrow(M, 2 * p + 1, ys[0]); M = setrow(M, 2 * q + 1, ys[1]);
    }
    if (used >= MAXS) {
        for (int r = 0; r < K; r++) {
            if (lastact[r] > b) continue;                        /* active later */
            if (b + 1 < S && (seq[b + 1] == r)) continue;
            if (b + 1 < S && seq[b] == r && seq[b + 1] != r) continue;   /* in next junction base */
            M = setrow(M, 2 * r, row(M, 2 * r) & 0x55); M = setrow(M, 2 * r + 1, row(M, 2 * r + 1) & 0xaa);
        }
    }
    return M;
}
int main(int argc, char **argv) {
    K = atoi(argv[1]); S = atoi(argv[2]); MAXS = atoi(argv[3]);
    for (int i = 0; i < S; i++) seq[i] = atoi(argv[4 + i]);
    if (argc > 4 + S) { int na = atoi(argv[4 + S]); allowed = 0;
        for (int i = 0; i < na; i++) { int r = atoi(argv[5 + S + 2 * i]), t = atoi(argv[6 + S + 2 * i]); allowed |= 1ULL << (r * S + t); } }
    for (int k = 1; k <= 3; k++) mkgl(k);
    for (int r = 0; r < K; r++) { nact[r] = 0; lastact[r] = -1; for (int j = 0; j < S; j++) if (seq[j] == r) { act[r][nact[r]++] = j; lastact[r] = j; } }
    u64 I = 0; for (int i = 0; i < 2 * K; i++) I = setrow(I, i, 1u << i);
    hset cur; hinit(&cur, 1 << 10); hadd(&cur, canon(loc(I, seq[0], 0), 0, 0), 0);
    int P = 2 * K;
    for (int b = 1; b < S; b++) {
        hset nx; hinit(&nx, 1 << 12);
        int a = seq[b - 1], c = seq[b];
        int base[2], nb = 0; base[nb++] = a; if (c != a) base[nb++] = c;
        int idle[8], ni = 0; for (int r = 0; r < K; r++) if (r != a && r != c && interior(r, b) && (allowed >> (r * S + b) & 1)) idle[ni++] = r;
        for (size_t e = 0; e < cur.cap; e++) {
            if (!cur.t[e].k) continue;
            u64 M = cur.t[e].m, mask = cur.t[e].k - 1;
            int used = __builtin_popcountll(mask);
            for (int zi = -1; zi < ni; zi++) {
                if (zi >= 0 && used >= MAXS) break;
                int ps[3], k = 0; for (int i = 0; i < nb; i++) ps[k++] = base[i];
                u64 m2 = mask;
                if (zi >= 0) { ps[k++] = idle[zi]; m2 |= 1ULL << (idle[zi] * S + b); }
                if (k == 1) {
                    for (int rev = 0; rev < 2; rev++) { u64 M2 = loc(M, c, rev); if (pot(M2) == P - 1) hadd(&nx, canon(M2, b, __builtin_popcountll(m2)), m2); }
                    continue;
                }
                for (int ia = 0; ia < ngl[k]; ia++) for (int ib = 0; ib < ngl[k]; ib++) {
                    u64 M1 = tr(M, ps, k, gl[k][ia], gl[k][ib]);
                    for (int rev = 0; rev < 2; rev++) { u64 M2 = loc(M1, c, rev); if (pot(M2) == P - 1) hadd(&nx, canon(M2, b, __builtin_popcountll(m2)), m2); }
                }
            }
        }
        free(cur.t); cur = nx; P--;
        fprintf(stderr, "b=%d states=%zu\n", b, cur.n);
        if (!cur.n) { printf("INFEASIBLE\n"); return 0; }
    }
    /* collect distinct split masks */
    u64 masks[4096]; int nm = 0;
    for (size_t e = 0; e < cur.cap; e++) if (cur.t[e].k) {
        u64 mk = cur.t[e].k - 1; int f = 0; for (int i = 0; i < nm; i++) if (masks[i] == mk) { f = 1; break; }
        if (!f && nm < 4096) masks[nm++] = mk;
    }
    printf("FEASIBLE %d", nm);
    for (int i = 0; i < nm; i++) { printf(" ["); for (int r = 0; r < K; r++) for (int b = 0; b < S; b++) if (masks[i] >> (r * S + b) & 1) printf("(%d,%d)", r, b); printf("]"); }
    printf("\n");
    return 0;
}
