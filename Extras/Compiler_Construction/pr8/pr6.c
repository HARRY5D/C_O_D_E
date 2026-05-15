#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX 20

typedef struct {
    char op;
    char arg1[20];
    char arg2[20];
    char res[20];
} Quad;

typedef struct {
    char name[20];
    float value;
} Symbol;

Symbol table[MAX];
int symCount = 0;

int isNumber(char *s){
    return (s[0]>='0' && s[0]<='9') || s[0]=='.';
}

float getValue(char *name){
    if(isNumber(name))
        return atof(name);

    for(int i=0;i<symCount;i++)
        if(strcmp(table[i].name,name)==0)
            return table[i].value;

    printf("Error: undefined symbol %s\n",name);
    return 0;
}

void setValue(char *name,float v){
    for(int i=0;i<symCount;i++){
        if(strcmp(table[i].name,name)==0){
            table[i].value=v;
            return;
        }
    }
    strcpy(table[symCount].name,name);
    table[symCount].value=v;
    symCount++;
}

int main(){

    Quad q[]={
        {'+',"quiz1","quiz2","t1"},
        {'/',"t1","2","t2"},
        {'*',"t2","0.2","t3"},
        {'*',"assignment2","2","t4"},
        {'+',"assignment1","t4","t5"},
        {'/',"t5","3","t6"},
        {'*',"t6","0.4","t7"},
        {'+',"t3","t7","t8"},
        {'+',"t8","attendance","final"}
    };

    int qCount=9;

    setValue("quiz1",8.0);
    setValue("quiz2",9.0);
    setValue("assignment1",15.0);
    setValue("assignment2",20.0);
    setValue("attendance",5.0);

    for(int i=0;i<qCount;i++){
        float a=getValue(q[i].arg1);
        float b=getValue(q[i].arg2);
        float r=0;

        switch(q[i].op){
            case '+': r=a+b; break;
            case '-': r=a-b; break;
            case '*': r=a*b; break;
            case '/': r=a/b; break;
        }
        setValue(q[i].res,r);
    }

    printf("Final Marks = %.2f\n",getValue("final"));
}