#include <stdio.h>
#include <string.h>

int main() {

    char code[100][200];
    int n = 0;
    int i;

    printf("Enter C code line by line (type END to finish):\n\n");

    while (1) {
        fgets(code[n], 200, stdin);

        if (strncmp(code[n], "END", 3) == 0)
            break;

        n++;
    }

    printf("\n--- Basic Blocks ---\n");

    int block = 1;

    for (i = 0; i < n; i++) {

        if (strstr(code[i], "if")) {
            printf("B%d : %s", block++, code[i]);
        }
        else if (strstr(code[i], "else")) {
            printf("B%d : %s", block++, code[i]);
        }
        else if (strstr(code[i], "while")) {
            printf("B%d : %s", block++, code[i]);
        }
        else if (strstr(code[i], "break")) {
            printf("B%d : %s", block++, code[i]);
        }
        else if (strstr(code[i], "return")) {
            printf("B%d : %s", block++, code[i]);
        }
        else {
            printf("B%d : %s", block++, code[i]);
        }
    }

    printf("\n--- Possible CFG Flow (Sequential) ---\n");

    for (i = 1; i < block - 1; i++) {
        printf("B%d -> B%d\n", i, i + 1);
    }

    printf("\nCFG Generation Complete\n");

    return 0;
}
