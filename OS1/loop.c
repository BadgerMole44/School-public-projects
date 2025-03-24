#include <stdio.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    int i = 1, j=1;
    for (;(i+j) <= 5;)
    {
        printf("%d %s\n", i, "For Go Beavers!!!");
        i++, j++;
    }

    i=1, j=1;
    while ((i+j) <= 5)
    {
        printf("%d %s\n", i, "While Go Beavers!!!");
        i++, j++;
    }

    i=1, j=1;
    do {
        printf("%d %s\n", i, "Do Go Beavers!!!");
        i++, j++;
    } while ((i+j) <= 5);

    return 0;
}