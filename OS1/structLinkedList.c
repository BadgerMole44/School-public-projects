#include<stdio.h>
#include<string.h>
#include<stdlib.h>

int main(int argc, char *argv[])
{
    char s[100] = "";

    struct PatientData {
        char name[20];
        int age;
        float weight;
        struct PatientData *next;
    };

    typedef struct PatientData Patient;

    Patient *head = (Patient*)calloc(1, sizeof(*head));
    Patient *pa = head;
    Patient *pb;

    strcpy(head->name, "Person 1");
    head->age = 35;
    head->weight = 150.0;
    head->next = NULL;

    for (int i=0; i<3; i++)
    {
        pb = (Patient*)calloc(1, sizeof(*pb));
        sprintf(s, "Person %d", i + 2);
        strcpy(pb->name, s);
        pb->age = 10*i + 15;
        pb->weight = 180 - 22.5*i;
        pb->next = NULL;
        pa->next = pb;
        pa = pb;
    }
    
    for(pa=head; pa!=NULL; pa=pa->next)
    {
        printf("Name: %s age: %d weight: %.2f\n", pa->name, pa->age, pa->weight);
    }
    
}