# Expression & Conditional Parser - LEX/YACC Implementation

## Overview
A comprehensive parser built using LEX (lexical analyzer) and YACC (parser generator) to validate and parse:
- Arithmetic expressions with proper operator precedence
- Conditional statements (if-else, nested if-else)
- Logical and relational operators
- Error detection and recovery

## Problem Statement
Design and develop a unified LEX + YACC + C-based parser capable of:
- ✓ Parsing arithmetic expressions with proper operator precedence
- ✓ Parsing conditional constructs (if–else, nested conditions)
- ✓ Handling parentheses, associativity, and mixed operators
- ✓ Validating syntax and detecting malformed inputs
- ✓ Resolving ambiguous constructs such as dangling else
- ✓ Reporting syntactic errors with informative messages

## Files Included

### 1. `lexer.l` - Lexical Analyzer (LEX)
**Purpose**: Tokenize input into meaningful units
- Keywords: `if`, `else`
- Identifiers: Variable names
- Numbers: Integer constants
- Operators: Arithmetic, Relational, Logical
- Delimiters: Parentheses, braces, semicolons

### 2. `parser.y` - Parser (YACC)
**Purpose**: Define grammar rules and build parse tree
- Expression grammar with precedence
- Conditional statement rules
- Dangling else resolution
- Error recovery mechanisms

### 3. Test Files
- `test.txt` - Valid test cases
- `test_invalid.txt` - Invalid test cases for error detection
- `test_extended.txt` - Extended features (logical operators, ternary)

## Compilation and Execution

### Step 1: Generate Parser Code
```bash
# Generate lexer
flex lexer.l

# Generate parser
yacc -d parser.y
# OR with bison (more common):
bison -d parser.y

# This creates:
# - lex.yy.c (from flex)
# - parser.tab.c and parser.tab.h (from yacc/bison)
```

### Step 2: Compile
```bash
# Compile all together
gcc lex.yy.c parser.tab.c -o parser -lfl

# OR if lfl not found:
gcc lex.yy.c parser.tab.c -o parser
```

### Step 3: Run
```bash
# From file
./parser test.txt

# Interactive mode
./parser
# Then type expressions and press Ctrl+D when done
```

## Complete Build Commands

### Using Makefile (recommended):
```bash
make clean
make
make run          # Run with test.txt
make test-valid   # Test valid cases
make test-invalid # Test invalid cases
```

### Manual commands:
```bash
# Full build
flex lexer.l
bison -d parser.y
gcc lex.yy.c parser.tab.c -o parser -lfl

# Run tests
./parser test.txt
./parser test_invalid.txt
```

## Grammar Specifications

### Operator Precedence (Low to High)
```
Assignment      =           (right associative)
Logical OR      ||          (left associative)
Logical AND     &&          (left associative)
Equality        == !=       (left associative)
Relational      < > <= >=   (left associative)
Addition        + -         (left associative)
Multiplication  * / %       (left associative)
Unary           - !         (right associative)
Parentheses     ( )
```

### Grammar Rules

#### Program Structure:
```
program → stmt_list
stmt_list → stmt | stmt_list stmt
```

#### Statements:
```
stmt → assignment_stmt
     | if_stmt
     | compound_stmt
     
assignment_stmt → ID = expr ;

if_stmt → IF ( cond ) stmt
        | IF ( cond ) stmt ELSE stmt
        
compound_stmt → { stmt_list }
              | { }
```

#### Expressions:
```
expr → expr + expr
     | expr - expr
     | expr * expr
     | expr / expr
     | expr % expr
     | - expr
     | ( expr )
     | ID
     | NUM
```

#### Conditions:
```
cond → expr relop expr
     | cond && cond
     | cond || cond
     | ! cond
     | ( cond )
     
relop → > | < | >= | <= | == | !=
```

## Test Cases

### Valid Expressions:
```c
a = (m + n*3) / (x - y);                    // Arithmetic with precedence
b = x + y - z;                               // Left associativity
result = (a + b) * (c - d);                 // Parentheses
```

### Valid Conditionals:
```c
if(a > b) x = a + 2; else x = b - 1;       // Basic if-else
if(x < y) z = x;                            // If without else
if(a > b) if(c < d) y = c; else y = d;     // Nested if-else
```

### Valid Logical Operations:
```c
if(a > b && c < d) x = 1;                   // Logical AND
if(x == y || m != n) result = 0;           // Logical OR
if(!(a > b)) x = b;                         // Logical NOT
```

### Invalid Cases (Should Produce Errors):
```c
a = (m + n;              // Missing closing parenthesis
if(a > b) x = a + b      // Missing semicolon
a = m + * n;             // Invalid operator sequence
if() x = 5;              // Empty condition
```

## Key Concepts Explained

### 1. Operator Precedence Resolution
**Q: How does YACC resolve operator precedence?**

YACC uses `%left`, `%right`, and `%nonassoc` declarations:
```yacc
%left '+' '-'       // Lower precedence
%left '*' '/'       // Higher precedence
```
- Operators declared later have **higher precedence**
- `%left` means left-associative: `a-b-c` = `(a-b)-c`
- `%right` means right-associative: `a=b=c` = `a=(b=c)`

### 2. Dangling Else Problem
**Q: What causes shift-reduce conflicts in nested if-else?**

Example:
```c
if(a) if(b) x=1; else y=2;
```

Ambiguous: Does `else` belong to first or second `if`?

**Solution** - Use precedence:
```yacc
%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

if_stmt: IF '(' cond ')' stmt %prec LOWER_THAN_ELSE
       | IF '(' cond ')' stmt ELSE stmt
```

This makes `else` bind to the **nearest if**.

### 3. Error Recovery
**Q: How can error recovery be incorporated?**

Using the `error` token:
```yacc
stmt: error ';' { 
    yyerrok;              // Resume parsing
    printf("Skipping to semicolon\n");
}
```

This allows parser to continue after syntax errors.

## Applications

1. **Compiler Front-End**: Validates source code syntax
2. **Static Analysis Tools**: Detects code issues without execution
3. **Syntax Validators**: IDE syntax highlighting
4. **DSL Parsers**: Custom language interpreters
5. **Code Evaluation**: Automated grading systems

## Learning Outcomes

After completing this practical, students can:
1. ✓ Write LEX rules for tokenization
2. ✓ Write YACC rules for parsing expressions and conditionals
3. ✓ Understand and resolve shift-reduce conflicts
4. ✓ Implement operator precedence and associativity
5. ✓ Integrate LEX and YACC with C code
6. ✓ Apply error-handling strategies
7. ✓ Extend grammar for complex syntax

## Troubleshooting

### Error: "undefined reference to yywrap"
**Solution**: Add `-lfl` flag or define yywrap in lexer.l:
```c
int yywrap() { return 1; }
```

### Error: "parser.tab.h not found"
**Solution**: Generate with `-d` flag:
```bash
bison -d parser.y
```

### Shift-Reduce Conflicts
**Check**: Run yacc with verbose output:
```bash
bison -d -v parser.y
# Creates parser.output with conflict details
```

### Compilation Warnings
**Solution**: Use modern flags:
```bash
gcc -Wall -Wno-unused-function lex.yy.c parser.tab.c -o parser
```

## Extended Features (Bonus)

### Ternary Operator:
```c
result = (a > b) ? a : b;
```

### Else-If Ladder:
```c
if(x > 0) y = 1;
else if(x < 0) y = -1;
else y = 0;
```

### Compound Statements:
```c
if(a > b) {
    x = a;
    y = b;
}
```

## Tools/Technology

- **LEX/Flex**: Lexical analyzer generator
- **YACC/Bison**: Parser generator
- **GCC**: GNU C Compiler
- **Linux/WSL**: Development environment

## Time Investment
- **Implementation**: 3 hours
- **Testing & Debugging**: 1 hour
- **Total Engagement**: 4 hours

---
**Course**: Compiler Construction  
**Topic**: Parser Design using LEX/YACC  
**Learning Outcomes**: CO2/CO3  
**Date**: January 16, 2026
