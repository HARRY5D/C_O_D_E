%{
char ops[100];
int idx = 0;
%}

%%
[+\-*/]  { if (idx > 0) ops[idx++] = ' '; ops[idx++] = yytext[0]; }
.|\n     ;
%%

int main() {
    yylex();
    ops[idx] = '\0';
    printf("Operators: %s\n", ops);
    return 0;
}

int yywrap() { return 1; }



