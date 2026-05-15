%{
#include <stdio.h>
#include <string.h>
#include <ctype.h>

static int is_alpha_space_only(const char *text)
{
    int length = (int)strlen(text);
    if (length < 3 || !isalpha((unsigned char)text[0])) 
    {
        return 0;
    }

    for (int index = 0; index < length; index++) 
    {
        if (!isalpha((unsigned char)text[index]) && text[index] != ' ') 
        {
            return 0;
        }
    }

    return 1;
}

static int is_valid_username(const char *text)
{
    int length = (int)strlen(text);
    if (length < 5 || length > 15 || !isalpha((unsigned char)text[0])) 
    {
        return 0;
    }  

    for (int index = 0; index < length; index++) {
        if (!(isalnum((unsigned char)text[index]) || text[index] == '_')) 
        {
           return 0;
        }

        if (text[index] == '_' && index > 0 && text[index - 1] == '_') 
        {
            return 0;   {/* no consecutive underscores */ }
        }
    }

    return 1;
}

static int is_valid_email(const char *text)
{
    const char *at = strchr(text, '@');
    if (!at || strchr(at + 1, '@') != NULL || strchr(text, ' ') != NULL) 
    {
        return 0;
    }

    if (at == text || at[1] == '\0') 
    {
        return 0;
    }

    const char *dot = strrchr(at + 1, '.');
    if (!dot || dot == at + 1 || dot[1] == '\0') 
    {
        return 0;
    }

    return 1;
}

static int is_valid_mobile(const char *text)
{
    if (strlen(text) != 10 || text[0] < '6' || text[0] > '9') 
    {
        return 0;
    }

    for (int index = 0; index < 10; index++) 
    {
        if (!isdigit((unsigned char)text[index])) 
        {
            return 0;
        }
    }

    return 1;
}

static int is_valid_password(const char *text)
{
    int length = (int)strlen(text);
    int has_upper = 0;
    int has_lower = 0;
    int has_digit = 0;
    int has_special = 0;

    if (length < 8) {
        return 0;
    }

    for (int index = 0; index < length; index++) 
    {
        unsigned char ch = (unsigned char)text[index];
        if (isspace(ch)) {
            return 0;
        }
        if (isupper(ch)) {
            has_upper = 1;
        } else if (islower(ch)) {
            has_lower = 1;
        } else if (isdigit(ch)) {
            has_digit = 1;
        } else {
            has_special = 1;
        }
    }

    return has_upper && has_lower && has_digit && has_special;
}

static int is_valid_dob(const char *text)
{
    int day = 0;
    int month = 0;
    int year = 0;

    if (sscanf(text, "%2d-%2d-%4d", &day, &month, &year) != 3) 
    {
        return 0;
    }

    if (strlen(text) != 10 || text[2] != '-' || text[5] != '-') 
    {
        return 0;
    }

    if (day < 1 || day > 31 || month < 1 || month > 12) 
    {
        return 0;
    }

    if (year < 1900 || year > 9999) {
        return 0;
    }

    return 1;
}


static int is_valid_pincode(const char *text)
{
    if (strlen(text) != 6 || text[0] == '0') {
        return 0;
    }

    for (int index = 0; index < 6; index++) {
        if (!isdigit((unsigned char)text[index])) {
            return 0;
        }
    }

    return 1;
}

static int is_valid_pan(const char *text)
{
    if (strlen(text) != 10) {
        return 0;
    }

    for (int index = 0; index < 5; index++) {
        if (!isupper((unsigned char)text[index])) {
            return 0;
        }
    }

    for (int index = 5; index < 9; index++) {
        if (!isdigit((unsigned char)text[index])) {
            return 0;
        }
    }

    return isupper((unsigned char)text[9]);
}

static int is_valid_url(const char *text)
{
    const char *prefix_http = "http://";
    const char *prefix_https = "https://";
    const char *start = NULL;

    if (strncmp(text, prefix_http, strlen(prefix_http)) == 0) {
        start = text + strlen(prefix_http);
    } else if (strncmp(text, prefix_https, strlen(prefix_https)) == 0) {
        start = text + strlen(prefix_https);
    } else {
        return 0;
    }

    if (*start == '\0' || strchr(start, ' ') != NULL) {
        return 0;
    }

    const char *dot = strrchr(start, '.');
    if (!dot || dot == start || dot[1] == '\0') {
        return 0;
    }

    return 1;
}

static char *trim_value(char *text)
{
    while (*text == ' ' || *text == '\t') {
        text++;
    }

    char *end = text + strlen(text);
    while (end > text && (end[-1] == ' ' || end[-1] == '\t' || end[-1] == '\r')) {
        end--;
    }

    *end = '\0';
    return text;
}

static void print_result(const char *label, int valid)
{
    printf("%s: %s\n", label, valid ? "Valid" : "Invalid");
}
%}

%%

Name:[ \t]*[^\n]+           {
    char *value = trim_value(yytext + 5);
    print_result("Name", is_alpha_space_only(value));
}

Username:[ \t]*[^\n]+       {
    char *value = trim_value(yytext + 9);
    print_result("Username", is_valid_username(value));
}

Email:[ \t]*[^\n]+          {
    char *value = trim_value(yytext + 6);
    print_result("Email", is_valid_email(value));
}

Mobile:[ \t]*[^\n]+         {
    char *value = trim_value(yytext + 7);
    print_result("Mobile", is_valid_mobile(value));
}

Password:[ \t]*[^\n]+       {
    char *value = trim_value(yytext + 9);
    print_result("Password", is_valid_password(value));
}

DateOfBirth:[ \t]*[^\n]+    {
    char *value = trim_value(yytext + 12);
    print_result("DateOfBirth", is_valid_dob(value));
}

Pincode:[ \t]*[^\n]+        {
    char *value = trim_value(yytext + 8);
    print_result("Pincode", is_valid_pincode(value));
}

PAN:[ \t]*[^\n]+            {
    char *value = trim_value(yytext + 4);
    print_result("PAN", is_valid_pan(value));
}

URL:[ \t]*[^\n]+            {
    char *value = trim_value(yytext + 4);
    print_result("URL", is_valid_url(value));
}

[ \t\r\n]+                  { /* skip whitespace */ }

.                            { /* ignore any unexpected characters */ }

%%

int yywrap(void)
{
    return 1;
}

int main(void)
{    printf("Enter line by line:\n");
    yylex();
    return 0;
}

