#include "manyfunctions.h"

int main(int argc, char *argv[])
{
    int x = 15;
    int y = 35;
    int z = 40;
    float res;
    char msg[100] = "";
    int arr[SIZE] = { 15, 35, 40, 20, 40, 30 };
    int arr_len = sizeof(arr) / sizeof(arr[0]);


    printf("Function returns float: The average of %d, %d, and %d is %.2f\n", x, y, z, average(x, y, z));
    printf("Function returns string: %s\n", averageWMsg(x, y, z, msg));
    printf("Function passed an array: { ");
    for (int i = 0; i < arr_len; i++)
    {
        printf("%d", arr[i]);
        if (i != (arr_len - 1))
        {
            printf(", ");
        }
    }
    printf(" }\n    The average of the array is %.2f\nThe args provided to the program are: ", averageArr(arr));

    for (int i = 0; i<argc; i++)
    {
        printf("%s", argv[i]);

        if (i ==(argc-1))
        {
            printf("\n");
        } else {
            printf(", ");
        }
    }

    return 0;
}
