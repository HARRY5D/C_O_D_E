%{
#include <stdio.h>
int count=0;
%}
%%
[A-Z] {count++;}      
.     ;               
\n    {printf("Uppercase Letters: %d\n",count);}  
%%
int main(){yylex();}
int yywrap(){return 1;}