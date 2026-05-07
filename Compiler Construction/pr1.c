#include <stdio.h>
#include <string.h>

void checkString(char *s) {
    int i = 0;

    if (s[i] != 'a') {
        printf("Invalid String\n");
        return;
    }

    i++;

    while (s[i] == 'b') {
        i++;
    }

    if (s[i] == 'c' && s[i + 1] == '\0') {
        printf("Valid String\n");
    } else {
        printf("Invalid String\n");
    }
}

int main() {
    printf("Input: ac\n");
    char test1[] = "ac";
    checkString(test1);
    printf("\n");

    printf("Input: abbbbbc\n");
    char test2[] = "abbbbbc";
    checkString(test2);
    printf("\n");

    printf("Input: bac\n");
    char test3[] = "bac";
    checkString(test3);
    printf("\n");

    printf("Input: ab\n");
    char test4[] = "ab";
    checkString(test4);
    printf("\n");

    printf("Input: abbbbbac\n");
    char test5[] = "abbbbbac";
    checkString(test5);
    printf("\n");

    printf("Input: Abc\n");
    char test6[] = "Abc";
    checkString(test6);

    return 0;
}
