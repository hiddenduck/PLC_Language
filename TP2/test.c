#include "stdio.h"


int main () {
    int x[30];
    int y;
    x[y = 20] = 0;
    printf("%d. %d", y, x[y]);
    return 0;
}
