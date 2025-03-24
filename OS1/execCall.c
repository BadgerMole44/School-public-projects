#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>


int main(int argc, char *argv[], char *envp[])
{
    char *otherProg = "otherProg";                                                  // program to be called
    char *my_argv[] = { "A1", "A2", (char*) NULL };                                 // argv must be 0 terminated like a string.
    char *my_envp[] = { "E1", "E2", (char*) NULL };

    printf("forking with execv().\n");
    switch (fork()) {
        case -1: 
            printf("There is a problem with fork.\n");
            exit(1);
        case 0:                                                                     // child
            printf("On child process ... Calling process %s.\n", otherProg);
            if ( execv(otherProg, my_argv) != 0) {
                printf("Child process could not call process %s.\n", otherProg);
                _exit(1);
            }
        default:                                                                   // parent
            break;
    }
    sleep(1);
    
    printf("\n#------------------------------------------------------#\nforking with execve()\n");
    switch (fork()) {
    case -1: 
        printf("There is a problem with fork.\n");
        exit(1);
    case 0:                                                                     // child
        printf("On child process ... Calling process %s.\n", otherProg);
        if ( execve(otherProg, my_argv, my_envp) != 0) {
            printf("Child process could not call process %s.\n", otherProg);
            _exit(1);
        }
    default:                                                                    // parent
        break;
    }
}  