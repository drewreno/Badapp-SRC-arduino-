#include <stdio.h>
#include <stdlib.h>

int findMaxEarnings(int lengths[], int n, int m, int c) {
    int maxProfit = 0;

    //maximum length of rod
    int maxLength = 0;
    for (int i = 0; i < n; i++) {
        if (lengths[i] > maxLength) {
            maxLength = lengths[i];
        }
    }

    //cutting rods to every possible length
    for (int len = 1; len <= maxLength; len++) {
        int profit = 0;

        for (int i = 0; i < n; i++) {
            if (lengths[i] < len) {
                //if the rod is shorter than the current length, skip it
                continue;
            }

            int numCuts = lengths[i] / len - 1;
            if (lengths[i] % len > 0) {
                numCuts++;
            }

            int totalValue = (lengths[i] / len) * len * m;
            int totalCost = numCuts * c;

            if (totalValue - totalCost > 0) {
                profit += totalValue - totalCost;
            }
        }

        if (profit > maxProfit) {
            maxProfit = profit;
        }
    }

    return maxProfit;
}

int main() {
    int t, n, m, c;

    scanf("%d", &t);
    int out[t];

    for (int i = 0; i < t; i++) {
        scanf("%d %d %d", &n, &m, &c);

        int lengths[n];
        for (int j = 0; j < n; j++) {
            scanf("%d", &lengths[j]);
        }

        out[i] = findMaxEarnings(lengths, n, m, c);
    }

    for (int i = 0; i < t; i++) {
        printf("%d\n", out[i]);
    }

    return 0;
}
