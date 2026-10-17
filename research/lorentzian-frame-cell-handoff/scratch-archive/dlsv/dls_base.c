// Dynamic local search for max clique (Pullan-Hoos DLS-MC style, simplified). usage: dls graph.txt seconds seed pd
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>
int n, W; uint64_t *adj; int *deg;
#define ADJ(i,j) ((adj[(size_t)(i)*W + ((j)>>6)] >> ((j)&63)) & 1)
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "r"); double secs = atof(argv[2]); srand(atoi(argv[3])); int pd = argc > 4 ? atoi(argv[4]) : 2;
  fscanf(f, "%d", &n); W = (n + 63) / 64; adj = calloc((size_t)n * W, 8);
  char *line = malloc(1 << 20); fgets(line, 1 << 20, f);
  for (int i = 0; i < n; i++) { fgets(line, 1 << 20, f); char *p = line; int j, c;
    while (sscanf(p, "%d%n", &j, &c) == 1) { adj[(size_t)i*W + (j>>6)] |= 1ULL << (j & 63); p += c; } }
  int *inC = calloc(n, 4), *C = malloc(n * 4), csz = 0, *miss = calloc(n, 4), *pen = calloc(n, 4), *tabu = calloc(n, 4);
  int best = 0, *bestC = malloc(n * 4); long it = 0; clock_t t0 = clock(); int *cand = malloc(n * 4);
  // miss[v] = number of clique vertices not adjacent to v (v not in C)
  while ((double)(clock() - t0) / CLOCKS_PER_SEC < secs) {
    it++;
    int nc = 0, minp = 1 << 30;
    for (int v = 0; v < n; v++) if (!inC[v] && miss[v] == 0) { if (pen[v] < minp) { minp = pen[v]; nc = 0; } if (pen[v] == minp) cand[nc++] = v; }
    if (nc) { int v = cand[rand() % nc]; inC[v] = 1; C[csz++] = v; for (int u = 0; u < n; u++) if (u != v && !ADJ(u, v)) miss[u]++;
      if (csz > best) { best = csz; memcpy(bestC, C, csz * 4); printf("best %d it %ld t %.1f\n", best, it, (double)(clock()-t0)/CLOCKS_PER_SEC); fflush(stdout);} continue; }
    nc = 0; minp = 1 << 30;
    for (int v = 0; v < n; v++) if (!inC[v] && miss[v] == 1 && tabu[v] < it) { if (pen[v] < minp) { minp = pen[v]; nc = 0; } if (pen[v] == minp) cand[nc++] = v; }
    if (nc) { int v = cand[rand() % nc]; int w = -1; for (int i = 0; i < csz; i++) if (!ADJ(v, C[i])) { w = i; break; }
      int out = C[w]; C[w] = v; inC[out] = 0; inC[v] = 1; tabu[out] = it + 7;
      for (int u = 0; u < n; u++) { if (u != out && !ADJ(u, out)) miss[u]--; if (u != v && !ADJ(u, v)) miss[u]++; }
      continue; }
    // perturb: increase penalties of clique vertices, restart from a random vertex keeping its neighbours
    for (int i = 0; i < csz; i++) pen[C[i]]++;
    if (it % pd == 0) for (int v = 0; v < n; v++) if (pen[v]) pen[v]--;
    int v = rand() % n; int ncsz = 0;
    for (int i = 0; i < csz; i++) if (ADJ(v, C[i])) C[ncsz++] = C[i]; else inC[C[i]] = 0;
    csz = ncsz; if (!inC[v]) { inC[v] = 1; C[csz++] = v; }
    memset(miss, 0, n * 4); for (int i = 0; i < csz; i++) for (int u = 0; u < n; u++) if (u != C[i] && !ADJ(u, C[i])) miss[u]++;
  }
  printf("final best %d\n", best); for (int i = 0; i < best; i++) printf("%d ", bestC[i]); printf("\n");
}
