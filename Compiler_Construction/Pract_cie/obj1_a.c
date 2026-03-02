#include <stdio.h>
#include <string.h>
int main()
{
    char s[100]; 
    
    printf("Enter a string: ");
    scanf("%s",s);
    
    int a=0;
    for(int i=0;s[i];i++) if(s[i]=='a') a++;
    int n = strlen(s); 
   
    if(n == 1) { printf("Invalid\n"); } 
    
    else if (a>=2) printf("Valid\n"); 
    else printf("Invalid\n");
}

