#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>

static void myHandler(int sig);

int main (int argc, char *argv[])
{
    char msg[100];
    setbuf(stdout, NULL);       // disable buffering for stdout

    if (signal(SIGINT, myHandler) == SIG_ERR) {                             // set myHandler as the handler for SIGINT signal
        printf("Could not initilizr handler for Ctrl-C (SIGINT.\n)");
        exit(1);
    }

    if (signal(SIGQUIT, myHandler) == SIG_ERR) {
        printf("Could not initilizr handler for Ctrl-\\ (SIGQUIT.\n)");
        exit(1);
    }

    if (signal(SIGTERM, SIG_IGN) == SIG_ERR) {                                       // ignore kill               
        printf("Could not initilizr handler SIGTERM.\n");
        exit(1);
    }

    /*    if (signal(SIGKILL, SIG_IGN) == SIG_ERR) {                                       // ignore kill               
        printf("Could not initilizr handler SIGKILL.\n");
        exit(1);
    }
    */
    strcpy(msg, "Hello ");
    if (argc > 1) {
        strcat(msg, argv[1]);
    }
    strcat(msg, "!");

    while (1) {
        printf("%s\n", msg);
        sleep(1);
    }
}

static void myHandler(int sig) 
{
    printf("\nSignal Recieved: (%d) ==> %s\n", sig, strsignal(sig));
    close(1);
    exit(1);
}
