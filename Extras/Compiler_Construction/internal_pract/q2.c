#include <stdio.h>

char expr[100];
int idx = 0;

void parse() 
{
    if(expr[idx] == '(' ) //accepts only open bracket
    {
        idx++; // move to the next character
        parse();          
        
        if(expr[idx] == ')') // accepts only closed bracket at that specific index 
        {
            idx++; // move to the next character
        } 
        else 
        {
            printf("Invalid\n");
            return;
        }
        parse();          
    }
}

int main() 
{
    printf("Enter string: ");
    scanf("%s", expr);
    
    parse();    

    if(expr[idx] == '\0') //null character
    {
        printf("Valid\n");
    } 
    else 
    {
        printf("Invalid\n");
    }
    return 0;
}

