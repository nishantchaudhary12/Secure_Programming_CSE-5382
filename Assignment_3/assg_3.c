#include <stdio.h>
#include <string.h>

int main(){

    char first_string[20];
    char second_string[10];
    int x,y,p,q;

    printf("Enter the first string kid! \n");

    gets(first_string);
    printf("The First String Entered was: %s\n", first_string);
    strcpy(second_string, first_string);
    printf("The Second String is: %s\n", second_string);

    p = strlen(first_string);
    q = strlen(first_string);
    printf("\n\n%d : %d\n", p, q);

    return 0;
}
