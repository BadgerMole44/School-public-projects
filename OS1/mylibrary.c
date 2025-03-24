#include "manyfunctions.h"

float average(int a, int b, int c)
{
    float avg = ( (float)(a + b + c) ) / 3;
    return avg;
}

char * averageWMsg(int a, int b, int c, char s[])
{
    float avg = ( (float)(a + b + c) ) / 3;

    sprintf(s, "The average of %d, %d, and %d is %.2f", a, b, c, avg);

    return s;
}

float averageArr(int *arr)
{
    float avg = 0;
    int arr_len = sizeof(arr) / sizeof(arr[0]);

    for (int i = 0; i < arr_len ; i++)
    {
        avg += arr[i];
    }

    avg /= arr_len;

    return avg;
}