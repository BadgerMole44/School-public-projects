#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#define SIZE 11

int main (int argc, char *argv[])
{
    char *filename = "infile.txt1";
    int fd;                                                             // file descriptor
    char c;
    char buffer[(SIZE) + 1];                                            // space for end of string
    int r;

    /*1) open*/                                                 
    if ( (fd = open(filename, O_RDWR | O_CREAT)) == -1)                 // syscall
    {
        printf("ERROR: Error opening file.\n");
        return 1;
    }
    
    /*2) do somthing: read*/
    while( ( r = read(fd, buffer, SIZE) ) > 0)   // syscall: what you want to read, where to dump it, how long is the buffer. returns how many were read
    {   
        buffer[(SIZE) + 1]='\0';
        printf("%s", buffer);
    }

    /*2) do somthing: write to the end. writing to the end does not require us to change the position if we've read to the end.*/
    strcpy(buffer, "\nFffffffffF");
    write(fd, buffer, 11);                                      // syscall

    /*2) do somthing: write to the middle. must adjust position.*/
    lseek(fd, 22, SEEK_SET);                                    //syscall: move to position 22 starting from the beginning.
    strcpy(buffer, "FffffffffF\n");
    write(fd, buffer, 11);                                      // syscall

    /*3) close*/
    if(close(fd) == -1) 
    {
        printf("ERROR: Error closing file.\n");                 // syscall
        return 1;
    }

    return 0;
}