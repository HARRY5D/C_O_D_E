
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int is_valid_email(const char *email) {
    int at_count = 0;
    int dot_count = 0;
    int i = 0;
    
    if (strlen(email) < 5) return 0;
    
    for (i = 0; i < strlen(email); i++) {
        if (email[i] == '@') at_count++;
        if (email[i] == '.') dot_count++;
    }

    if (at_count != 1 || dot_count < 1) return 0;
    
    int at_pos = strchr(email, '@') - email;
    int last_dot = strrchr(email, '.') - email;
    
    if (at_pos == 0 || at_pos == strlen(email) - 1) return 0;
    if (last_dot <= at_pos + 1 || last_dot == strlen(email) - 1) return 0;
    
    return 1;
}

int main() {
    char email[100];

    printf("Enter email: ");
    scanf("%99s", email);
    
    if (is_valid_email(email))
        printf("Valid Email\n");
    else
        printf("Invalid Email\n");

    return 0;
}