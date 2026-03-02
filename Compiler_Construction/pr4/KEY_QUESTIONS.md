# Key Questions - Detailed Answers

## Course: Compiler Construction - Practical 4
## Topic: Expression & Conditional Parser Using LEX/YACC + C

---

## Question 1: How does YACC resolve operator precedence and associativity in arithmetic expressions?

### Answer:

YACC (Yet Another Compiler-Compiler) resolves operator precedence and associativity using **declarative precedence directives** and **grammar rule annotations**. This eliminates ambiguity in expression parsing without explicit tree construction.

### Mechanism:

#### 1. **Precedence Declarations**

YACC provides three directives to declare precedence:

```yacc
%left  '+'  '-'      // Left-associative, lower precedence
%left  '*'  '/'      // Left-associative, higher precedence
%right '='           // Right-associative
%nonassoc '<' '>'    // Non-associative (no chaining)
```

**Key Principle**: 
- Operators listed **later** have **higher precedence**
- Operators on the **same line** have **equal precedence**

#### 2. **Associativity Types**

| Directive | Meaning | Example | Parsed As |
|-----------|---------|---------|-----------|
| `%left` | Left-to-right | `a - b - c` | `(a - b) - c` |
| `%right` | Right-to-left | `a = b = c` | `a = (b = c)` |
| `%nonassoc` | No chaining | `a < b < c` | **Error!** |

#### 3. **Conflict Resolution**

**Shift-Reduce Conflict Example:**
```
Input: a + b * c
State: a + b • * c

Options:
  SHIFT  *  → Read * (makes b*c)
  REDUCE +  → Complete a+b first
```

**YACC Decision:**
- Compare precedence of `+` (left side) and `*` (right side)
- Since `*` has **higher precedence**, YACC **shifts**
- Result: `a + (b * c)` ✓

**Reduce-Reduce Conflict Example:**
```
Equal precedence: a - b - c

Options when seeing second '-':
  Reduce (a-b) first → left-associative
  Shift - to make (b-c) → right-associative
```

**YACC Decision:**
- `%left` directive → **REDUCE** immediately
- Result: `(a - b) - c` ✓

### Implementation Example:

#### Grammar Without Precedence (Ambiguous):
```yacc
expr: expr '+' expr
    | expr '*' expr
    | NUM
    ;
```

**Problem**: Input `2 + 3 * 4` has multiple parse trees:
```
Tree 1: (2 + 3) * 4 = 20   // Wrong!
Tree 2: 2 + (3 * 4) = 14   // Correct!
```

#### Grammar With Precedence (Unambiguous):
```yacc
%left '+'
%left '*'

%%
expr: expr '+' expr
    | expr '*' expr
    | NUM
    ;
```

**Result**: YACC automatically chooses Tree 2 (multiplication first).

### Advanced: Precedence Overriding

Sometimes you need different precedence for same operator:

```yacc
%left '+' '-'
%left '*' '/'
%right UMINUS      // Unary minus

%%
expr: expr '+' expr
    | expr '*' expr
    | '-' expr %prec UMINUS    // Override precedence
    | NUM
    ;
```

**Example**: `-2 * 3`
- Without `%prec`: Might parse as `-(2*3)` or `(-2)*3`
- With `%prec UMINUS`: Parses as `(-2) * 3` (unary minus has highest precedence)

### Precedence Table (Our Parser):

| Precedence | Operators | Associativity | Description |
|------------|-----------|---------------|-------------|
| 1 (Lowest) | `=` | Right | Assignment |
| 2 | `||` | Left | Logical OR |
| 3 | `&&` | Left | Logical AND |
| 4 | `==` `!=` | Left | Equality |
| 5 | `<` `>` `<=` `>=` | Left | Relational |
| 6 | `+` `-` | Left | Additive |
| 7 | `*` `/` `%` | Left | Multiplicative |
| 8 | `!` `-` (unary) | Right | Unary |
| 9 (Highest) | `(` `)` | - | Parentheses |

### Algorithm Behind the Scenes:

YACC generates a **LR (Left-to-Right, Rightmost derivation) parser** with a **precedence/associativity table**:

```
ACTION Table:
State | +    | *    | NUM  | $
------|------|------|------|----
0     | s3   | s4   | s1   | accept
1     | r2   | s4   | r2   | r2
2     | r1   | r1   | r1   | r1

r1 = reduce by: expr → expr * expr
r2 = reduce by: expr → expr + expr
s3 = shift and go to state 3
```

When conflict occurs, consult precedence table instead of guessing.

### Why This Matters:

1. **No Grammar Rewriting**: Don't need separate rules for each precedence level
2. **Clear Declaration**: Precedence is explicit, not hidden in grammar structure
3. **Easy Modification**: Changing precedence is one line change
4. **Efficient**: LR parser with precedence is faster than trying all parse trees

### Comparison: With vs Without Precedence

**Without Precedence (Multiple Grammar Rules):**
```yacc
expr: term
    ;
term: term '+' factor
    | factor
    ;
factor: factor '*' atom
      | atom
      ;
atom: NUM
    | '(' expr ')'
    ;
```
*Grammar is verbose and hard to modify*

**With Precedence (Single Rule):**
```yacc
%left '+'
%left '*'
%%
expr: expr '+' expr
    | expr '*' expr
    | '(' expr ')'
    | NUM
    ;
```
*Grammar is concise and clear*

### Conclusion:

YACC's precedence mechanism provides:
- ✓ **Declarative** syntax (what, not how)
- ✓ **Automatic** conflict resolution
- ✓ **Efficient** LR parsing
- ✓ **Maintainable** grammar specifications

This is superior to manually encoding precedence in grammar structure.

---

## Question 2: What causes shift–reduce or reduce–reduce conflicts in nested if–else constructs?

### Answer:

Conflicts in nested if-else constructs arise from **grammar ambiguity**, where the parser cannot deterministically decide which action to take. The most famous case is the **Dangling Else Problem**.

### Understanding the Dangling Else Problem

#### Ambiguous Input:
```c
if(a > b) if(c < d) x = 1; else y = 2;
```

#### Two Possible Interpretations:

**Interpretation 1** (else belongs to outer if):
```c
if(a > b) {
    if(c < d) {
        x = 1;
    }
} 
else {
    y = 2;  // ← else matches outer if
}
```

**Interpretation 2** (else belongs to inner if):
```c
if(a > b) {
    if(c < d) {
        x = 1;
    } 
    else {
        y = 2;  // ← else matches inner if
    }
}
```

### Why Conflict Occurs:

#### Grammar (Without Resolution):
```yacc
stmt: IF '(' cond ')' stmt
    | IF '(' cond ')' stmt ELSE stmt
    | ID '=' expr ';'
    ;
```

#### Parsing State When Conflict Happens:
```
Input: if(a>b) if(c<d) x=1; • else y=2;
                           ↑
                    Parser is here

Stack: [ if(a>b) if(c<d) x=1; ]

Options:
  1. REDUCE: Complete inner if-stmt without else
     → if(a>b) [if(c<d) x=1;]  (now outer if can take else)
     
  2. SHIFT: Read 'else' token
     → if(a>b) if(c<d) x=1; else  (else for inner if)
```

### Types of Conflicts:

#### 1. **Shift-Reduce Conflict**

**Definition**: Parser can either:
- **Shift**: Read the next token
- **Reduce**: Apply a grammar rule to what's already on stack

**Dangling Else Example:**
```
State 42:
  if_stmt → IF ( cond ) stmt •              [reduce possible]
  if_stmt → IF ( cond ) stmt • ELSE stmt    [shift possible]
  
Looking at: ELSE

Conflict:
  - Reduce using first rule (complete if without else)
  - Shift ELSE token (continue to if-else rule)
```

**Why It's a Problem:**
- Both actions are **grammatically valid**
- Different actions lead to **different parse trees**
- Parser must **choose one** deterministically

#### 2. **Reduce-Reduce Conflict**

**Definition**: Parser can reduce using multiple different rules

**Example (Different Context):**
```yacc
stmt: expr ';'
    ;
expr: ID
    ;
call: ID
    ;

// When seeing "x", reduce to expr or call?
```

**In If-Else Context (Rare):**
```yacc
stmt: simple_stmt
    | if_stmt
    ;
simple_stmt: IF '(' cond ')' stmt
    ;
if_stmt: IF '(' cond ')' stmt
    ;

// Both rules match same pattern - conflict!
```

### Conflict Analysis in YACC:

#### Checking for Conflicts:
```bash
bison -d -v parser.y
# Creates parser.output with detailed state information
```

#### Example parser.output:
```
State 24:

    6 stmt: IF '(' cond ')' stmt .
    7     | IF '(' cond ')' stmt . ELSE stmt

    ELSE  shift, and go to state 25

    ELSE      [reduce using rule 6 (stmt)]
    $default  reduce using rule 6 (stmt)

Conflict: 1 shift/reduce conflict
```

### Resolution Strategies:

#### Strategy 1: **Precedence/Associativity**

```yacc
%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%%
stmt: IF '(' cond ')' stmt %prec LOWER_THAN_ELSE
    | IF '(' cond ')' stmt ELSE stmt
    ;
```

**How it works:**
- Give `ELSE` token higher precedence
- When conflict occurs, **shift** (prefer ELSE)
- Result: `else` binds to **nearest** (innermost) `if`

**Conflict Resolution:**
```
Rule: if-without-else has precedence LOWER_THAN_ELSE
Token: ELSE has precedence ELSE

Since ELSE > LOWER_THAN_ELSE:
  → SHIFT ELSE (don't reduce yet)
  → else matches inner if
```

#### Strategy 2: **Grammar Rewriting**

**Original Ambiguous Grammar:**
```yacc
stmt: IF '(' cond ')' stmt
    | IF '(' cond ')' stmt ELSE stmt
    ;
```

**Rewritten Unambiguous Grammar:**
```yacc
stmt: matched_stmt
    | unmatched_stmt
    ;

matched_stmt:
    IF '(' cond ')' matched_stmt ELSE matched_stmt
    | other_stmt
    ;

unmatched_stmt:
    IF '(' cond ')' stmt
    | IF '(' cond ')' matched_stmt ELSE unmatched_stmt
    ;
```

**Idea**: Separate matched (with else) and unmatched (without else) statements.

**Drawback**: Grammar becomes much more complex.

#### Strategy 3: **Require Explicit Delimiters**

**Force Braces:**
```yacc
stmt: IF '(' cond ')' '{' stmt '}'
    | IF '(' cond ')' '{' stmt '}' ELSE '{' stmt '}'
    ;
```

**Example:**
```c
if(a > b) {
    if(c < d) {
        x = 1;
    }
} else {        // Unambiguous: clearly for outer if
    y = 2;
}
```

**Drawback**: Less flexible, forces specific style.

### Why Most Languages Choose Nearest Binding:

1. **Intuitive**: Matches how programmers think
2. **Simple**: Easy precedence rule
3. **Consistent**: With other nesting (loops, functions)
4. **Minimal**: No extra syntax required

### Common Programming Language Solutions:

| Language | Solution |
|----------|----------|
| C, Java, JavaScript | Nearest `if` (via shift preference) |
| Python | Indentation-based (no ambiguity) |
| Algol 60, Ada | Explicit `end if` or `fi` keyword |
| Shell scripts | `fi` keyword to close `if` |
| Visual Basic | `End If` keyword |

### Testing for Conflicts:

```bash
# Generate parser with verbose output
bison -d -v parser.y

# Check for conflicts
grep "conflict" parser.output

# Output:
# State 24 conflicts: 1 shift/reduce
```

**Types of Output:**
- `X shift/reduce`: X shift-reduce conflicts
- `Y reduce/reduce`: Y reduce-reduce conflicts
- No message: Grammar is conflict-free ✓

### Real-World Impact:

**Without Proper Resolution:**
```c
// Programmer writes:
if(debug)
    if(verbose)
        log("debug");
else
    log("error");

// Might be interpreted as:
if(debug) {
    if(verbose)
        log("debug");
    else
        log("error");  // ✗ Wrong! Error logged when debug=true, verbose=false
}
```

**With Proper Resolution:**
```c
// Correctly interpreted as:
if(debug) {
    if(verbose) {
        log("debug");
    } else {
        log("error");
    }
}
```

### Summary:

**Shift-Reduce Conflicts in If-Else occur because:**
1. ✗ Grammar has multiple valid derivations
2. ✗ Parser can't decide: reduce now or read more tokens
3. ✗ Different choices lead to different meanings

**Solution:**
1. ✓ Use precedence declarations (`%prec`, `%nonassoc`)
2. ✓ Prefer SHIFT over REDUCE when seeing `else`
3. ✓ Bind `else` to nearest unmatched `if`

This resolves the ambiguity deterministically and matches programmer expectations.

---

## Question 3: How can error recovery be incorporated to allow continued parsing despite syntactic errors?

### Answer:

Error recovery enables parsers to **detect errors**, **report them**, and **continue parsing** to find additional errors in a single run. This is crucial for development tools (compilers, IDEs) that need to report multiple errors at once.

### Why Error Recovery Matters:

**Without Error Recovery:**
```
File: program.c (1000 lines)
Line 10: Missing semicolon
Parser: "Syntax error"
→ Stops immediately
→ Fix line 10, recompile
→ Find error at line 50
→ Fix line 50, recompile
→ Repeat...
```

**With Error Recovery:**
```
File: program.c (1000 lines)
Parser: 
  Line 10: Missing semicolon
  Line 50: Unmatched parenthesis
  Line 203: Invalid operator
→ Fix all 3 errors at once
→ Recompile
```

### Error Recovery Strategies in YACC:

#### 1. **The `error` Token**

YACC provides a special token called `error` that matches syntax errors.

**Basic Usage:**
```yacc
stmt: assignment_stmt
    | if_stmt
    | error ';'     { 
        yyerrok;    // Resume normal parsing
        printf("Error recovered at semicolon\n");
      }
    ;
```

**How it works:**
1. Parser detects syntax error
2. Enters error recovery mode
3. Discards tokens until it finds `;`
4. Reduces using `error ';'` rule
5. Calls `yyerrok` to resume normal parsing

**Example:**
```c
Input: a = b +* c;    // Invalid: +*
       x = y + z;     // Valid

Without recovery: Stops at line 1
With recovery:
  → "Error in line 1"
  → Skips to semicolon
  → Continues to parse line 2 successfully
```

#### 2. **Error Recovery Points**

Place `error` at strategic locations:

```yacc
/* Statement-level recovery */
stmt: ID '=' expr ';'
    | if_stmt
    | error ';'              { yyerrok; }
    ;

/* Expression-level recovery */
expr: expr '+' expr
    | expr '*' expr
    | '(' expr ')'
    | '(' error ')'          { yyerrok; }
    | ID
    | NUM
    ;

/* Block-level recovery */
block: '{' stmt_list '}'
     | '{' error '}'         { yyerrok; }
     ;
```

**Strategy**: Recover at **synchronization points** (`;`, `}`, `end`, etc.)

#### 3. **Multi-Level Recovery**

```yacc
program: decl_list stmt_list
       | error stmt_list     { yyerrok; /* Skip bad declarations */ }
       ;

stmt_list: stmt
         | stmt_list stmt
         | stmt_list error stmt { yyerrok; /* Skip bad statement */ }
         ;

stmt: assignment
    | if_stmt
    | error ';'              { yyerrok; /* Recover at semicolon */ }
    ;
```

**Effect**: Errors in one part don't prevent parsing other parts.

### YACC Error Recovery Functions:

#### 1. **`yyerrok`**
```c
yyerrok;  // Resume normal parsing
```
- Tells parser: "Error handled, continue normally"
- Usually called in error recovery actions

#### 2. **`yyclearin`**
```c
yyclearin;  // Discard current lookahead token
```
- Discards the token that caused the error
- Useful when error token itself is problematic

#### 3. **`yyerror()`**
```c
void yyerror(const char *msg) {
    fprintf(stderr, "Error at line %d: %s\n", line_num, msg);
}
```
- Called automatically when syntax error detected
- Customize to provide better error messages

### Advanced Error Recovery Techniques:

#### 1. **Panic Mode Recovery**

Discard tokens until a synchronizing token is found:

```yacc
stmt_list: stmt
         | stmt_list stmt
         | error sync_token { yyerrok; }
         ;

sync_token: ';' | '}' | END_OF_STATEMENT
          ;
```

**Algorithm:**
1. On error, enter panic mode
2. Pop symbols from stack
3. Discard input tokens
4. Until a synchronizing token is found
5. Resume parsing

#### 2. **Phrase-Level Recovery**

Perform local corrections:

```yacc
if_stmt: IF '(' cond ')' stmt
       | IF '(' cond error stmt {
           yyerror("Missing closing parenthesis");
           yyerrok;
         }
       | IF error '(' cond ')' stmt {
           yyerror("Missing opening parenthesis");
           yyerrok;
         }
       ;
```

**Strategy**: Anticipate common errors and provide specific fixes.

#### 3. **Error Production Rules**

Add rules specifically for common errors:

```yacc
assignment: ID '=' expr ';'
          | ID '=' expr error {
              yyerror("Missing semicolon");
              yyerrok;
            }
          | ID expr ';' {
              yyerror("Missing assignment operator");
              yyerrok;
            }
          ;
```

### Practical Implementation Example:

```yacc
%{
#include <stdio.h>
int line_num = 1;
int error_count = 0;

void yyerror(const char *s);
%}

%%

program: stmt_list {
           if(error_count == 0)
               printf("✓ No errors found\n");
           else
               printf("✗ Total errors: %d\n", error_count);
         }
       ;

stmt_list: /* empty */
         | stmt_list stmt
         | stmt_list error ';' {
             error_count++;
             yyerrok;
             printf("→ Recovered at semicolon\n");
           }
         ;

stmt: assignment
    | if_stmt
    | compound_stmt
    ;

assignment: ID '=' expr ';' {
              printf("✓ Valid assignment\n");
            }
          ;

if_stmt: IF '(' cond ')' stmt {
           printf("✓ Valid if statement\n");
         }
       | IF '(' cond ')' stmt ELSE stmt {
           printf("✓ Valid if-else statement\n");
         }
       | IF '(' error ')' stmt {
           error_count++;
           yyerrok;
           yyerror("Invalid condition in if statement");
         }
       | IF error stmt {
           error_count++;
           yyerrok;
           yyerror("Missing parentheses in if statement");
         }
       ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "✗ Line %d: %s\n", line_num, s);
    error_count++;
}
```

### Error Message Enhancement:

#### Basic Error Message:
```
Syntax error
```

#### Enhanced Error Message:
```c
void yyerror(const char *s) {
    extern char *yytext;
    fprintf(stderr, "Error at line %d, column %d\n", 
            line_num, col_num);
    fprintf(stderr, "Near token: '%s'\n", yytext);
    fprintf(stderr, "Message: %s\n", s);
    fprintf(stderr, "Expected: semicolon, closing brace, or statement\n");
}
```

**Output:**
```
Error at line 15, column 23
Near token: '*'
Message: syntax error
Expected: semicolon, closing brace, or statement
```

### Testing Error Recovery:

**Input (test_errors.txt):**
```c
a = b + c;          // OK
x = y +* z;         // Error: +*
m = n - p;          // OK after recovery
if(a > b x = 1;     // Error: missing )
result = 42;        // OK after recovery
```

**Output:**
```
✓ Valid assignment
✗ Line 2: syntax error near '*'
→ Recovered at semicolon
✓ Valid assignment
✗ Line 4: Invalid condition in if statement
→ Recovered at semicolon
✓ Valid assignment
✗ Total errors: 2
```

### Best Practices:

1. **Synchronization Points**: Use natural delimiters (`;`, `}`, `end`)
2. **Local Recovery**: Handle errors close to where they occur
3. **Informative Messages**: Tell user what went wrong and where
4. **Limit Cascading**: Prevent one error from triggering many messages
5. **Count Errors**: Report total at end

### Trade-offs:

| Aspect | With Recovery | Without Recovery |
|--------|---------------|------------------|
| Errors Found | Multiple per run | One per run |
| Parse Time | Slower (recovery overhead) | Faster |
| Complexity | Higher | Lower |
| User Experience | Better (batch errors) | Worse (iterative) |
| False Positives | Possible (cascading) | Rare |

### Summary:

**Error recovery is implemented through:**
1. ✓ Special `error` token in grammar rules
2. ✓ `yyerrok` to resume parsing
3. ✓ Strategic synchronization points (`;`, `}`)
4. ✓ Custom `yyerror()` for informative messages
5. ✓ Error production rules for common mistakes

**Benefits:**
- Find **multiple errors** in one compilation
- Improve **developer productivity**
- Provide **better diagnostics**
- Enable **IDE error highlighting**

This makes the parser **robust** and **user-friendly**, essential for production compilers and development tools.

---

## Conclusion

These three questions cover the core concepts of parser implementation:

1. **Precedence/Associativity**: How to parse expressions correctly
2. **Conflict Resolution**: How to handle ambiguous grammars
3. **Error Recovery**: How to make parsers robust and helpful

Together, they form the foundation of practical compiler construction using LEX and YACC.

---
*Document prepared for Practical 4 - Compiler Construction*  
*Expression & Conditional Parser Implementation*  
*Date: January 16, 2026*
