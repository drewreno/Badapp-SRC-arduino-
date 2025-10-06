#include <stdio.h>
#include <stdlib.h>

int compare(const void * a, const void * b) {
   return ( *(int*)a - *(int*)b );
}

long long distance(int *stor, int N) {
    qsort(stor, N, sizeof(int), compare); // Sort the array for efficient computation

    long long holder = 0; //trying long long 
    for (int i = 0; i < N; i++) {
        holder += (long long)stor[i] * i - (long long)stor[i] * (N - i - 1);
    }
    return holder;
}

int main() {
    int T, N;
    scanf("%d", &T);
    long long *out = malloc(T * sizeof(long long));

    for(int i = 0; i < T; i++) {
        scanf("%d", &N);

        int *storage = malloc(N * sizeof(int));
        for (int j = 0; j < N; j++) {
            scanf("%d", &storage[j]);
        }

        out[i] = distance(storage, N);
        free(storage);
    }

    for(int k = 0; k < T; k++) {
        printf("%lld\n", out[k]);
    }

    free(out);
    return 0;
}
