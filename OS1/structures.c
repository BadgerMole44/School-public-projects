#include<stdio.h>
#include<string.h>
#include<stdlib.h>

int main(int argc, char *argv[])
{
    struct PatientData {
        char name[20];
        int age;
        float weight;
    };

    typedef struct PatientData patient;                                         // alaias

    patient tim = { "Tim", 35, 150.0 };                                         // init
    patient class[3];
    patient *p;
    patient *pa;

    printf("Name: %s age: %d weight: %.2f\n", tim.name, tim.age, tim.weight);

    strcpy(tim.name, "Timothy");

    tim.age = 36;
    tim.weight = 180.0;

    printf("Single struct\n");
    printf("Name: %s age: %d weight: %.2f\n\n", tim.name, tim.age, tim.weight);

    strcpy(class[0].name, "John");
    strcpy(class[1].name, "Jill");
    strcpy(class[2].name, "Jack");

    for (int i=0; i<3; i++) {
        class[i].age = 10*i + 10;
        class[i].weight = 180 - 10*i;
    }

    printf("Traditional array of structs\n");
    for (int i=0; i<3; i++) {
         printf("Name: %s age: %d weight: %.2f\n", class[i].name, class[i].age, class[i].weight);
    }

    p = (patient*)calloc(3, sizeof(*p));

    pa = p;

    strcpy(pa->name, "Mary");
    strcpy((pa+1)->name, "Mark");
    strcpy((pa+2)->name, "Milly");

    for (int i=0; i<3; i++) {
        (pa+i)->age = 10*i + 15;
        (pa+i)->weight = 180 - 20*i;
    }

    printf("\nPointer array of structs\n");

    for (int i=0; i<3; i++) {
         printf("Name: %s age: %d weight: %.2f\n", (pa+i)->name, (pa+i)->age, (pa+i)->weight);
    }

    free(p);

    return 0;
}