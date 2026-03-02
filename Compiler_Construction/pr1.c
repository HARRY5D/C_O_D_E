#include <stdio.h>

int main() {
    char s[100];
    int i = 0;

    scanf("%s", s);

    if (s[i] != 'a') {
        printf("Invalid String");
        return 0;
    }

    i++;

    while (s[i] == 'b') {
        i++;
    }

    if (s[i] == 'c' && s[i + 1] == '\0') {
        printf("Valid String");
    } else {
        printf("Invalid String");
    }

    return 0;
}
