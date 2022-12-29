#include "stdio.h"


int main () {
    int x[*];
    int y;
    x[y = 20] = 0;
    printf("%d. %d", y, x[y]);
    return 0;
}
