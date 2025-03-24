#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>



int main(int argc, char *argv[], char *envp[])                              // run bash set | more to see environment variable names. PATH HOME etc
{
    int i = 0;
    char *mayEnvVar;

    printf("\nInside the child process ...\nArguments in argv:\n");
    for ( char **p = &argv[0]; ( *p != 0 ) && ( i < 5 ); p++, i++ ) {
        printf("argv[%d] = %s\n", i, *p);
    }

    printf("\nArguments in environment variables:\n");
    i = 0;
    for ( char **p = &envp[0]; ( *p != 0 ) && ( i < 5 ); p++, i++ ) {
        printf("envp[%d] = %s\n", i, *p);
    }

    return 0;
}