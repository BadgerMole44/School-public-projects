#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#define MAXSIZE 1001

int main (int argc, char *argv[])
{
    char *fileIn = "infile2.txt";
    int fd;                                                             // file descriptor
    

    /*trying to open sequential input file*/                                                 
    if ( (fd = open(fileIn, O_RDONLY)) == -1)                 // syscall
    {
        printf("ERROR: Error opening %s.\n", fileIn);
        return -1;
    }

    if (fchmod(fd, S_IROTH | S_IWOTH | S_IXOTH) == -1)
    {
        printf("There is an error changing permissions of output file %s.\n", fileIn);
        return -1;
    }

    /*trying to close sequential output file*/
    if (close(fd) == -1)
    {
        printf("There is an error at closing %s.\n", fileIn);
        return -1;
    }

    // change permissions without opening:
    if (fchmod(fd, S_IRGRP | S_IWGRP | S_IXGRP) == -1)
    {
        printf("There is an error changing permissions of output file %s.\n", fileIn);
        return -1;
    }    
    

    
    
    return 0;
}