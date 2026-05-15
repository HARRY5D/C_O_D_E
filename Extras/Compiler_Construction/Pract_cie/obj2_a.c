//2.	String over {0,1} that must start and end with same symbol.

#include <stdio.h>
#include <string.h> 
int main()
{
    char s[100]; 
    
    printf("Enter a string: ");
    scanf("%s",s);
    
    int n = strlen(s); 
    
    if(s[0]==s[n-1]) printf("Valid\n"); 
    
    else printf("Invalid\n");
}