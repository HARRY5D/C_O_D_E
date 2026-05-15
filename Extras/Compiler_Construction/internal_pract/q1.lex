%{
#include <stdio.h>
int a=0, b=0, c=0, op=0;
%}

%%
a       { a++; }
b       { b++; }
c       { c++; }
"+"     { op++; }
\n      {  if(a>=1 && b>=1 && c>=1 && op>=2) printf("Valid\n"); else printf("Invalid\n"); a=b=c=op=0; }
.       ;
%%

int main() 
{
    yylex();
    return 0;
}

int yywrap() 
{
    return 1;
}