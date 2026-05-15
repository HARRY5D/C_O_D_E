%{
#include <stdio.h>
#include <string.h>

void validate_username(char *s);
void validate_password(char *s);
%}

%%

Name:.* 
{
    if (yytext[6] >= 'A' && yytext[6] <= 'Z')
        printf("Name: Valid\n");
    else
        printf("Name: Invalid\n");
}

Username:.* 
{
    validate_username(yytext+10);
}

Email:.* 
{
    if (strchr(yytext, '@') && strchr(yytext, '.'))
        printf("Email: Valid\n");
    else
        printf("Email: Invalid\n");
}

Mobile:.* {
    if (yytext[8] >= '6' && yytext[8] <= '9')
        printf("Mobile: Valid\n");
    else
        printf("Mobile: Invalid\n");
}

Password:.* {
    validate_password(yytext+10);
}

DateOfBirth:.* 
{
    
    int day = 0;
    int month = 0;
    int year = 0;

    if (sscanf(text, "%2d-%2d-%4d", &day, &month, &year) != 3) 
    {
        printf("DateOfBirth: Invalid\n");
    }

    if (strlen(text) != 10 || text[2] != '-' || text[5] != '-') 
    {
        printf("DateOfBirth: Invalid\n");
    }

    if (day < 1 || day > 31 || month < 1 || month > 12) 
    {
        printf("DateOfBirth: Invalid\n");
    }

    printf("DateOfBirth: Valid\n");  
}

Pincode:.* 
{
    if (strlen(text) != 6 || text[0] == '0') 
    {
        printf("Pincode: Invalid\n");
    }

    for (int index = 0; index < 6; index++) 
    {
        if (!isdigit((unsigned char)text[index])) 
        {
            printf("Pincode: Invalid\n");
        }
    }


    if (yytext[9] != '0')
        printf("Pincode: Valid\n");
    else
        printf("Pincode: Invalid\n");
}

PAN:.* {
    if (strlen(text) != 10) 
    {
        printf("PAN: Invalid\n"); 
    }

    for (int index = 0; index < 5; index++) 
    {
        if (!isupper((unsigned char)text[index])) 
        {
            printf("PAN: Invalid\n"); 
        }
    }

    for (int index = 5; index < 9; index++) 
    {
        if (!isdigit((unsigned char)text[index])) 
        {
            printf("PAN: Invalid\n"); 
        }
    }

    //return isupper((unsigned char)text[9]);

    printf("PAN: Valid\n"); 
}

URL:.* {
    if (strstr(yytext, "http://") || strstr(yytext, "https://"))
        printf("URL: Valid\n");
    else
        printf("URL: Invalid\n");
}

%%

void validate_username(char *s) 
{
    int len = strlen(s);
    int i;
    for(i=0;i<len-1;i++){
        if(s[i]=='_' && s[i+1]=='_')
        {
            printf("Username: Invalid\n");
            return;
        }
    }
    printf("Username: Valid\n");
}

void validate_password(char *s) 
{
    int u=0,l=0,d=0,spl=0,i;
    for(i=0;s[i];i++)
    {
        if(s[i]>='A'&&s[i]<='Z') u=1;
        else if(s[i]>='a'&&s[i]<='z') l=1;
        else if(s[i]>='0'&&s[i]<='9') d=1;
        else spl=1;
    }

    if(u&&l&&d&&spl)
        printf("Password: Valid\n");
    else
        printf("Password: Invalid\n");
}

int main() 
{   printf("Enter line by line:\n");
    yylex();
    return 0;
}
