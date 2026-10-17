/* Exhaustive F_2 schedule search with splits, K <= 6 pairs, S <= 15 stages.
   usage: [PERTIME=p] [ALLOWMASKS=file] splitk K S maxsplits seq... [nallowed r t r t ...]
   Rows 2i = X_i, 2i+1 = Y_i as 16-bit words; bit 2i = x_i, 2i+1 = y_i.  Prints feasible split sets. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned long long u64;
typedef unsigned __int128 u128;
static int K, S, MAXS, PERTIME = 2, seq[32];
typedef struct { uint16_t r[12]; } Mat;
static int rank16(unsigned v[], int n) {
    unsigned a[12]; int r = 0; for (int i = 0; i < n; i++) a[i] = v[i];
    for (int bit = 0; bit < 16 && r < n; bit++) {
        int p = -1; for (int i = r; i < n; i++) if (a[i] >> bit & 1) { p = i; break; }
        if (p < 0) continue; unsigned t = a[p]; a[p] = a[r]; a[r] = t;
        for (int i = 0; i < n; i++) if (i != r && (a[i] >> bit & 1)) a[i] ^= a[r];
        r++;
    }
    return r;
}
static int potX(const Mat *M) { unsigned v[6]; for (int i = 0; i < K; i++) v[i] = M->r[2 * i] & 0x5555; return rank16(v, K); }
static int potY(const Mat *M) { unsigned v[6]; for (int i = 0; i < K; i++) v[i] = M->r[2 * i + 1] & 0xaaaa; return rank16(v, K); }
static int ngl[5]; static unsigned char gl[5][20200][4]; static int byrow[5][4][16][1400], nbyrow[5][4][16];
static void mkgl(int k) {
    int n = 0;
    for (int code = 0; code < (1 << (k * k)); code++) {
        unsigned v[4]; for (int i = 0; i < k; i++) v[i] = (code >> (k * i)) & ((1 << k) - 1);
        if (rank16(v, k) == k) { for (int i = 0; i < k; i++) { gl[k][n][i] = v[i]; byrow[k][i][v[i]][nbyrow[k][i][v[i]]++] = n; } n++; }
    }
    ngl[k] = n;
}
static void tr(Mat *R, const Mat *M, int *ps, int k, unsigned char *A, unsigned char *B) {
    *R = *M;
    for (int i = 0; i < k; i++) {
        unsigned nx = 0, ny = 0;
        for (int j = 0; j < k; j++) { if (A[i] >> j & 1) nx ^= M->r[2 * ps[j]]; if (B[i] >> j & 1) ny ^= M->r[2 * ps[j] + 1]; }
        R->r[2 * ps[i]] = nx; R->r[2 * ps[i] + 1] = ny;
    }
}
static void loc(Mat *M, int q, int rev) { if (rev) M->r[2 * q] ^= M->r[2 * q + 1]; else M->r[2 * q + 1] ^= M->r[2 * q]; }
/* hash set */
typedef struct { Mat m; u128 k; } ent;
typedef struct { ent *t; size_t cap, n; } hset;
static void hinit(hset *h, size_t cap) { h->cap = cap; h->n = 0; h->t = calloc(cap, sizeof(ent)); }
static size_t hh(const Mat *m, u128 k) {
    u64 x = 0x9E3779B97F4A7C15ULL;
    for (int i = 0; i < 12; i++) { x ^= m->r[i] + 0x632BE59BD9B4E019ULL + (x << 6) + (x >> 2); }
    x ^= (u64)k * 0xBF58476D1CE4E5B9ULL; x ^= (u64)(k >> 64) * 0x94D049BB133111EBULL; x ^= x >> 31; return x;
}
static int eqm(const Mat *a, const Mat *b) { return memcmp(a, b, sizeof(Mat)) == 0; }
static int hadd(hset *h, const Mat *m, u128 k) {
    if (h->n * 2 > h->cap) {
        hset g; hinit(&g, h->cap * 2);
        for (size_t i = 0; i < h->cap; i++) if (h->t[i].k) { size_t j = hh(&h->t[i].m, h->t[i].k) % g.cap; while (g.t[j].k) j = (j + 1) % g.cap; g.t[j] = h->t[i]; g.n++; }
        free(h->t); *h = g;
    }
    u128 kk = k + 1; size_t j = hh(m, kk) % h->cap;
    while (h->t[j].k) { if (h->t[j].k == kk && eqm(&h->t[j].m, m)) return 0; j = (j + 1) % h->cap; }
    h->t[j].m = *m; h->t[j].k = kk; h->n++; return 1;
}
static int act[8][32], nact[8], lastact[8];
static u128 allowed; static u128 amask[50000]; static int namask = 0;
static int subset_ok(u128 m) { if (!namask) return 1; for (int i = 0; i < namask; i++) if ((m & ~amask[i]) == 0) return 1; return 0; }
static int interior(int r, int b) {
    int last = -1, nxt = S;
    for (int i = 0; i < nact[r]; i++) { int j = act[r][i]; if (j < b && j > last) last = j; if (j >= b && j < nxt) nxt = j; }
    return (last + 1) < b && b < nxt;
}
static void rref2(unsigned *v) {
    int r = 0;
    for (int bit = 15; bit >= 0 && r < 2; bit--) {
        int p = -1; for (int i = r; i < 2; i++) if (v[i] >> bit & 1) { p = i; break; }
        if (p < 0) continue; unsigned t = v[p]; v[p] = v[r]; v[r] = t;
        for (int i = 0; i < 2; i++) if (i != r && (v[i] >> bit & 1)) v[i] ^= v[r];
        r++;
    }
}
static void canon(Mat *M, int b, int used) {
    if (b + 1 < S && seq[b] != seq[b + 1]) {
        int p = seq[b], q = seq[b + 1];
        unsigned xs[2] = { M->r[2 * p], M->r[2 * q] }, ys[2] = { M->r[2 * p + 1], M->r[2 * q + 1] };
        rref2(xs); rref2(ys);
        M->r[2 * p] = xs[0]; M->r[2 * q] = xs[1]; M->r[2 * p + 1] = ys[0]; M->r[2 * q + 1] = ys[1];
    }
    if (used >= MAXS) {
        for (int r = 0; r < K; r++) {
            if (lastact[r] > b) continue;
            if (b + 1 < S && seq[b + 1] == r) continue;
            if (b + 1 < S && seq[b] == r && seq[b + 1] != r) continue;
            M->r[2 * r] &= 0x5555; M->r[2 * r + 1] &= 0xaaaa;
        }
    }
}
static int popc128(u128 x) { return __builtin_popcountll((u64)x) + __builtin_popcountll((u64)(x >> 64)); }
int main(int argc, char **argv) {
    K = atoi(argv[1]); S = atoi(argv[2]); MAXS = atoi(argv[3]); if (getenv("PERTIME")) PERTIME = atoi(getenv("PERTIME"));
    for (int i = 0; i < S; i++) seq[i] = atoi(argv[4 + i]);
    allowed = ~(u128)0;
    if (argc > 4 + S) { int na = atoi(argv[4 + S]); allowed = 0;
        for (int i = 0; i < na; i++) { int r = atoi(argv[5 + S + 2 * i]), t = atoi(argv[6 + S + 2 * i]); allowed |= (u128)1 << (r * S + t); } }
    for (int k = 1; k <= 4; k++) mkgl(k);
    if (getenv("ALLOWMASKS")) { FILE *f = fopen(getenv("ALLOWMASKS"), "r"); char buf[128];
        while (fscanf(f, "%127s", buf) == 1) { u128 x = 0; for (char *c = buf; *c; c++) x = x * 10 + (*c - '0'); amask[namask++] = x; } fclose(f); }
    for (int r = 0; r < K; r++) { nact[r] = 0; lastact[r] = -1; for (int j = 0; j < S; j++) if (seq[j] == r) { act[r][nact[r]++] = j; lastact[r] = j; } }
    Mat I; memset(&I, 0, sizeof I); for (int i = 0; i < 2 * K; i++) I.r[i] = 1u << i;
    hset cur; hinit(&cur, 1 << 10); { Mat M0 = I; loc(&M0, seq[0], 0); canon(&M0, 0, 0); hadd(&cur, &M0, 0); }
    int P = 2 * K;
    for (int b = 1; b < S; b++) {
        hset nx; hinit(&nx, 1 << 12);
        int a = seq[b - 1], c = seq[b];
        int base[2], nb = 0; base[nb++] = a; if (c != a) base[nb++] = c;
        int idle[8], ni = 0; for (int r = 0; r < K; r++) if (r != a && r != c && interior(r, b) && ((allowed >> (r * S + b)) & 1)) idle[ni++] = r;
        for (size_t e = 0; e < cur.cap; e++) {
            if (!cur.t[e].k) continue;
            Mat M = cur.t[e].m; u128 mask = cur.t[e].k - 1;
            int used = popc128(mask);
            for (int zc = 0; zc < (1 << ni); zc++) {
                int nz = __builtin_popcount(zc);
                if (nz > PERTIME || used + nz > MAXS || nb + nz > 4) continue;
                int ps[4], k = 0; for (int i = 0; i < nb; i++) ps[k++] = base[i];
                u128 m2 = mask;
                for (int zi = 0; zi < ni; zi++) if (zc >> zi & 1) { ps[k++] = idle[zi]; m2 |= (u128)1 << (idle[zi] * S + b); }
                if (!subset_ok(m2)) continue;
                int u2 = popc128(m2);
                if (k == 1) {
                    for (int rev = 0; rev < 2; rev++) { Mat M2 = M; loc(&M2, c, rev); if (potX(&M2) + potY(&M2) == P - 1) { canon(&M2, b, u2); hadd(&nx, &M2, m2); } }
                    continue;
                }
                int ci = 0; while (ps[ci] != c) ci++;
                unsigned xs[4], ys[4];
                for (int i = 0; i < k; i++) { xs[i] = M.r[2 * ps[i]]; ys[i] = M.r[2 * ps[i] + 1]; }
                int rXX = potX(&M), rYY = potY(&M);
                for (int rev = 0; rev < 2; rev++) {
                    for (int io = 0; io < ngl[k]; io++) {
                        unsigned char *O = gl[k][io];
                        unsigned newrows[4];
                        for (int i = 0; i < k; i++) { unsigned v_ = 0; for (int j = 0; j < k; j++) if (O[i] >> j & 1) v_ ^= (rev ? xs[j] : ys[j]); newrows[i] = v_; }
                        for (int rc = 1; rc < (1 << k); rc++) {
                            unsigned oth = 0; for (int j = 0; j < k; j++) if (rc >> j & 1) oth ^= (rev ? ys[j] : xs[j]);
                            unsigned blk[6]; int cnt = 0;
                            for (int i = 0; i < K; i++) {
                                int pos = -1; for (int t = 0; t < k; t++) if (ps[t] == i) pos = t;
                                unsigned rv = pos >= 0 ? newrows[pos] : M.r[rev ? 2 * i : 2 * i + 1];
                                if (i == c) rv ^= oth;
                                blk[cnt++] = rev ? (rv & 0x5555) : (rv & 0xaaaa);
                            }
                            int r2 = rank16(blk, K);
                            if ((rev ? r2 + rYY : rXX + r2) != P - 1) continue;
                            for (int jq = 0; jq < nbyrow[k][ci][rc]; jq++) {
                                unsigned char *Q = gl[k][byrow[k][ci][rc][jq]];
                                Mat M1; if (rev) tr(&M1, &M, ps, k, O, Q); else tr(&M1, &M, ps, k, Q, O);
                                loc(&M1, c, rev); canon(&M1, b, u2); hadd(&nx, &M1, m2);
                            }
                        }
                    }
                }
            }
        }
        free(cur.t); cur = nx; P--;
        fprintf(stderr, "b=%d states=%zu\n", b, cur.n);
        if (!cur.n) { printf("INFEASIBLE\n"); return 0; }
    }
    u128 masks[4096]; int nm = 0;
    for (size_t e = 0; e < cur.cap; e++) if (cur.t[e].k) {
        u128 mk = cur.t[e].k - 1; int f = 0; for (int i = 0; i < nm; i++) if (masks[i] == mk) { f = 1; break; }
        if (!f && nm < 4096) masks[nm++] = mk;
    }
    printf("FEASIBLE %d", nm);
    for (int i = 0; i < nm; i++) { printf(" ["); for (int r = 0; r < K; r++) for (int b = 0; b < S; b++) if ((masks[i] >> (r * S + b)) & 1) printf("(%d,%d)", r, b); printf("]"); }
    printf("\n");
    return 0;
}
