// input, assignment, variables, output.

#include <stdio.h>
int main (void)
{
    int days;
    float weeks;

    printf("How many days till christmas? ");
    scanf("%d", &days);

    weeks = (float)days / 7;
    
    printf("%d days is %.2f weeks.\n", days, weeks);
    return 0;
}