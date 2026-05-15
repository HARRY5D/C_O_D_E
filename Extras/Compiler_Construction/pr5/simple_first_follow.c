#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX 20

char grammar[MAX][MAX];
char first[MAX][MAX];
char follow[MAX][MAX];
int n;

// Check if character exists in set
int contains(char *set, char c) {
    for (int i = 0; set[i]; i++) 
        if (set[i] == c) return 1;
    return 0;
}

// Add character to set (no duplicates)
void add(char *set, char c) {
    if (!contains(set, c)) {
        int l = strlen(set);
        set[l] = c;
        set[l+1] = '\0';
    }
}

// Check if character is a non-terminal (uppercase)
int isNonTerminal(char c) {
    return isupper(c);
}

void FIRST(char c);

// Compute FIRST of a string
void FIRST_string(char *str, char *res) {
    if (str[0] == '\0') {
        add(res, '#');  // Empty string
        return;
    }
    
    for (int i = 0; str[i]; i++) {
        if (!isNonTerminal(str[i])) {
            // Terminal symbol
            add(res, str[i]);
            return;
        } else {
            // Non-terminal: add its FIRST (except epsilon)
            FIRST(str[i]);
            int idx = str[i] - 'A';
            for (int j = 0; first[idx][j]; j++) {
                if (first[idx][j] != '#') 
                    add(res, first[idx][j]);
            }
            // If no epsilon, stop here
            if (!contains(first[idx], '#')) 
                return;
        }
    }
    // All symbols can derive epsilon
    add(res, '#');
}

// Compute FIRST set for non-terminal c
void FIRST(char c) {
    int idx = c - 'A';
    if (strlen(first[idx]) != 0) return;  // Already computed

    for (int i = 0; i < n; i++) {
        if (grammar[i][0] == c) {
            if (grammar[i][2] == '#') {
                // Production: c -> epsilon
                add(first[idx], '#');
            } else if (!isNonTerminal(grammar[i][2])) {
                // Production: c -> terminal...
                add(first[idx], grammar[i][2]);
            } else {
                // Production: c -> Non-terminal...
                char res[MAX] = "";
                FIRST_string(&grammar[i][2], res);
                for (int k = 0; res[k]; k++) 
                    add(first[idx], res[k]);
            }
        }
    }
}

// Compute FOLLOW set for non-terminal c
void FOLLOW(char c) {
    int idx = c - 'A';
    if (strlen(follow[idx]) != 0) return;  // Already computed

    // Rule 1: $ in FOLLOW(Start Symbol)
    if (c == grammar[0][0]) 
        add(follow[idx], '$');

    for (int i = 0; i < n; i++) {
        for (int j = 2; grammar[i][j]; j++) {
            if (grammar[i][j] == c) {
                if (grammar[i][j+1] != '\0') {
                    // Rule 2: Something after c
                    if (!isNonTerminal(grammar[i][j+1])) {
                        // Terminal follows
                        add(follow[idx], grammar[i][j+1]);
                    } else {
                        // Non-terminal follows: add FIRST(beta) - {epsilon}
                        char temp[MAX] = "";
                        FIRST_string(&grammar[i][j+1], temp);
                        for (int k = 0; temp[k]; k++) {
                            if (temp[k] != '#') 
                                add(follow[idx], temp[k]);
                        }
                        // If epsilon in FIRST(beta), add FOLLOW(A)
                        if (contains(temp, '#')) {
                            FOLLOW(grammar[i][0]);
                            int p = grammar[i][0] - 'A';
                            for (int k = 0; follow[p][k]; k++) 
                                add(follow[idx], follow[p][k]);
                        }
                    }
                } else {
                    // Rule 3: c is at the end, add FOLLOW(A)
                    FOLLOW(grammar[i][0]);
                    int p = grammar[i][0] - 'A';
                    for (int k = 0; follow[p][k]; k++) 
                        add(follow[idx], follow[p][k]);
                }
            }
        }
    }
}

int main() {
    /*
     * Simple Grammar:
     * S -> AB      (Start with A then B)
     * A -> a       (A produces 'a')
     * A -> #       (A can be epsilon/empty)
     * B -> b       (B produces 'b')
     * 
     * Expected Results:
     * FIRST(S) = {a, b}  (can start with 'a' from A, or if A is empty, 'b' from B)
     * FIRST(A) = {a, #}  (can be 'a' or epsilon)
     * FIRST(B) = {b}     (only 'b')
     * 
     * FOLLOW(S) = {$}    (S is start symbol, followed by end-of-input)
     * FOLLOW(A) = {b}    (A is followed by B which produces 'b')
     * FOLLOW(B) = {$}    (B is at end of S, so FOLLOW(S))
     */
    
    n = 4;
    strcpy(grammar[0], "S=AB");   // S -> AB
    strcpy(grammar[1], "A=a");    // A -> a
    strcpy(grammar[2], "A=#");    // A -> epsilon
    strcpy(grammar[3], "B=b");    // B -> b

    // Initialize sets
    for (int i = 0; i < MAX; i++) {
        first[i][0] = '\0';
        follow[i][0] = '\0';
    }

    // Compute FIRST sets
    printf("Computing FIRST sets...\n");
    for (int i = 0; i < n; i++) {
        FIRST(grammar[i][0]);
    }

    // Compute FOLLOW sets
    printf("Computing FOLLOW sets...\n");
    for (int i = 0; i < n; i++) {
        FOLLOW(grammar[i][0]);
    }

    // Display Grammar
    printf("\n=== GRAMMAR ===\n");
    for (int i = 0; i < n; i++) {
        printf("%c -> %s\n", grammar[i][0], 
               strcmp(&grammar[i][2], "#") == 0 ? "ε (epsilon)" : &grammar[i][2]);
    }

    // Display FIRST sets
    printf("\n=== FIRST SETS ===\n");
    for (int i = 0; i < 26; i++) {
        if (strlen(first[i])) {
            printf("FIRST(%c) = { ", i + 'A');
            for (int j = 0; first[i][j]; j++) {
                if (first[i][j] == '#')
                    printf("ε");
                else
                    printf("%c", first[i][j]);
                if (first[i][j+1]) printf(", ");
            }
            printf(" }\n");
        }
    }

    // Display FOLLOW sets
    printf("\n=== FOLLOW SETS ===\n");
    for (int i = 0; i < 26; i++) {
        if (strlen(follow[i])) {
            printf("FOLLOW(%c) = { ", i + 'A');
            for (int j = 0; follow[i][j]; j++) {
                printf("%c", follow[i][j]);
                if (follow[i][j+1]) printf(", ");
            }
            printf(" }\n");
        }
    }

    return 0;
}
