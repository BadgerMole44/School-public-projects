#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define SIZE 100

int* createArray(int n);
void printArr(int *arr, int n);
int prodArr(int *arr, int n);

int main(int argc, char *argv[])
{
    printf("Pointer Example:\n");
    char c = 123;
    printf("   Variable c:\n      Address: %p\n      Value: %d\n", &c, c);
    char *pC = &c;
    printf("   Variable pC:\n      Address: %p\n      Value: %p\n      Dereferenced: %d\n", &pC, pC, *pC);

    int *arr;
    int n;
    int prod;
    char msg[200];

    sprintf(msg,"How many elements in the array(1-%d)? ", SIZE);
    printf("%s",msg);
    scanf("%d", &n);
    if ( (n<=0) || (n>SIZE)) {
        printf("Number of elements (%d) is invalid.\n", n);
        return 1;
    }

    arr = createArray(n);
    if (arr != NULL)
    {
        printArr(arr, n);

        prod = prodArr(arr, n);

        printf("The product of all elements in arr is %d\n", prod);

        free(arr);

        return 0; 
    } else {
        printf("Error allocating memory.\n");
    }
}

int* createArray(int n)
{
    int *arr = (int*)malloc(sizeof(*arr)*n);
    if (arr != NULL) 
    {
        int *p = arr;
        for (int i=0; i<n; i++)
        {
            printf("Enter element %d of arr: ", i);
            if (scanf("%d", p) != 1){
                printf("Error reading number.\n");
                free(arr);
                return NULL;
            }
            p++;
        }
    }
    return arr;
}

void printArr(int *p, int n)
{
    for (int i=0; i<n; i++) 
    {
        printf("arr[%d] = %d\n", i, *p);
        p++;
    }
}

int prodArr(int *p, int n)
{
    int prod = 1;
    for (int i=0; i<n; i++)
    {
        prod *= (*p);
        p++;
    }
    return prod;
} 
