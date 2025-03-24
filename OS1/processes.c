#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

void showEnvVars(char *envp[], char *prefix);

extern char **environ;

int main(int argc, char *argv[])                              // run bash set | more to see environment variable names. PATH HOME etc
{
    char *myEnvVar;
    char *prefix = "H";
    char **envp = environ;

    printf("\nOriginal Global Environment Variable with prefix %s...\n", prefix);
    showEnvVars(envp, "H");

    if (setenv("HELLO", "hello", 0) == -1) {                                 // setenv: name , value, overwrite. set HELLO to hello.
        printf("\nHELLO environment variable could not be added.\n");
        exit(1);
    } else {
        printf("\nEnvironment variable HELLO was added to global environment.\n");
    }
    if ( ( myEnvVar = getenv("HELLO") ) == NULL) {
        myEnvVar = "Not Available";
    }

    envp = environ;
    
    printf("Recovered Environment Variable HELLO ==> %s from the global environment\n", myEnvVar);
    printf("\nGlobal Environment Variables After adding HELLO...\n");
    showEnvVars(envp, "H");
}

/* Print all environment variables that start with the prefix*/
void showEnvVars(char *envp[], char *prefix) {
    for (char **p = &envp[0]; *p != 0; p++) {
        if ( ( *prefix == 0 ) || ( strncmp(*p, prefix, strlen(prefix) ) == 0 ) ) {
            printf("%s\n", *p);
        }
    }
}