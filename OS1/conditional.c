#include <stdio.h>
#include <stdbool.h>

void main(void)
{
    float exam;
    char letterGrade;
    bool pass = false;

    printf("Exam Score: ");
    scanf("%f",&exam);


    if (exam >= 90.0) {
        letterGrade = 'A';
        pass = true;
    } else if (exam >= 80) {
        letterGrade = 'B';
        pass = true;
    } else if (exam >= 70) {
        letterGrade = 'C';
        pass = true;
    } else if (exam >= 60) {
        letterGrade = 'D';
    } else {
        letterGrade = 'F';
    }

    printf("Your grade is %c.\n", letterGrade);

    switch (letterGrade) {
        case 'A':
            printf("very good.\n");
            break;
        case 'B':
            printf("good.\n");
            break;
        case 'C':
            printf("mid.\n");
            break;
        case 'D':
            printf("dookie.\n");
            break;
        default: 
            printf("Good god.\n");
    }

    if (pass) {
        printf("You passed.\n");
    } else {
        printf("no pass.\n");
    }
}