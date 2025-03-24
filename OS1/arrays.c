#include <stdio.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    int myArray[] = {20, 30, 40, 50, 60};

    for (int i=0; i<5; i++)
    {
        printf("Array[%d] = %d\n", i, myArray[i]);
    }
    return 0;
}