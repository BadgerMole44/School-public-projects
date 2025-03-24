#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>

int main(int argc, char *argv[])
{
    pid_t myPID;
    pid_t childOutPID;
    int nForks;
    int childrenExiting;
    int time=0;
    int i;
    
    if ( argc != 2 || ( ( nForks = atoi(argv[1]) ) < 1 ) )
    {
        printf("Invalid use. Should be:\ncyclefork #_of_forks\n#_of_forks should be a integer > 0\n");
        exit(1);
    }

    setbuf(stdout, NULL);                       // Disable buffer for stdout

    for ( i = 0; i < nForks; i++ ) {            // create a child with decreasign wait time for each loop.
        switch (fork()) {
            case -1:                            
                printf("There is a problem with fork.\n");
                exit(1);
            case 0:                             // child prints, sleeps, exits
                myPID = getpid();
                printf("Process %d created. Waiting %d seconds.\n", myPID, nForks-i);
                sleep(nForks-i);
                _exit(EXIT_SUCCESS);
            default:                            // parent keeps going.
                break;
        }
    }

    childrenExiting = 0;
    while (childrenExiting < nForks) {
        childOutPID = wait(NULL);
        if ( childOutPID < 1 ) {
            printf("Unexpected Error.");
            exit(1);
        }
        childrenExiting++;;
        printf("Children # %d (Pid=%d) exit acknowleged\n", childrenExiting, childOutPID);
    }

    printf("All children are back.\n");
    printf("Bye!\n");
    exit(EXIT_SUCCESS);
}