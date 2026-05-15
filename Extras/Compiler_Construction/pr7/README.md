# LR(0) Parser - Practical 7

## Overview
This program implements a complete LR(0) parser that constructs canonical LR(0) item sets, builds ACTION & GOTO tables, and performs shift-reduce parsing to validate input strings.

## Grammar Used

The program uses the following grammar (conflict-free for LR(0)):

```
0. S' -> S     (Augmented start production)
1. S  -> A A
2. A  -> a A
3. A  -> b
```

**Language**: Strings containing exactly 2 occurrences of 'b', with any number of 'a's before each 'b'.

## Features

1. **LR(0) Automata Construction**
   - Closure computation
   - GOTO function implementation
   - Canonical collection of LR(0) items

2. **Parsing Table Generation**
   - ACTION table (shift/reduce/accept)
   - GOTO table for non-terminals
   - Conflict detection (shift-reduce, reduce-reduce)

3. **Shift-Reduce Parsing**
   - Step-by-step trace
   - Stack visualization
   - Accept/Reject decisions

## Compilation

```bash
gcc pr7.c -o pr7
```

Or use the provided Makefile:
```bash
make
```

## Usage

```bash
./pr7
```

The program will:
1. Display the grammar
2. Construct LR(0) automata
3. Show all states with items
4. Build and display the ACTION & GOTO table
5. Prompt for input strings to parse

## Test Cases

### Valid Strings (Should be ACCEPTED)

1. **`ab$`** - Simplest valid string (a before first b, nothing before second b)
2. **`aab$`** - Two a's before first b, nothing before second b  
3. **`abb$`** - One a before first b, nothing before second b
4. **`aabb$`** - Two a's before first b, one a before second b
5. **`aaab$`** - Three a's before first b, nothing before second b
6. **`aaaabb$`** - Four a's before first b, one a before second b
7. **`aaaaabb$`** - Five a's before first b, one a before second b

### Invalid Strings (Should be REJECTED)

1. **`a$`** - Only one 'a', no 'b's
2. **`b$`** - Only one 'b' (needs 2)
3. **`aa$`** - Two a's, no 'b's
4. **`bbb$`** - Three b's (too many)
5. **`abab$`** - Alternating pattern (not matching grammar)
6. **`ba$`** - Wrong order
7. **`aabbb$`** - Three b's instead of two

## Understanding the Output

### LR(0) States
Each state shows items with dot (•) positions:
```
State I0
│ Z -> •S
│ S -> •A A
│ A -> •a A
│ A -> •b
```

### ACTION Table Entries
- **sN**: Shift to state N
- **rN**: Reduce by production N
- **acc**: Accept the string

### GOTO Table Entries
- Shows state transitions for non-terminals after reductions

### Parsing Trace
Example for input `aab$`:
```
Step Stack              Input       Action
──────────────────────────────────────────
1    [0]                aab$        Shift 2
2    [0 2a]             ab$         Shift 2
3    [0 2a 2a]          b$          Shift 4
4    [0 2a 2a 4b]       $           Reduce by 3: A -> b
5    [0 2a 2a 3A]       $           Reduce by 2: A -> a A
6    [0 2a 3A]          $           Reduce by 2: A -> a A
7    [0 3A]             $           ...continues until accept
```

## Key Concepts Demonstrated

### 1. Closure Computation
When an item has a dot before a non-terminal, all productions of that non-terminal are added to the closure with dot at the beginning.

### 2. GOTO Function
GOTO(state, symbol) computes the next state by:
- Taking all items with dot before 'symbol'
- Moving the dot past the symbol
- Computing closure of the result

### 3. Shift-Reduce Decisions
- **Shift**: When dot is before a terminal in an item
- **Reduce**: When dot is at the end of an item
- **Accept**: When we reduce by S' -> S and input is $

### 4. Conflict Detection
This grammar is LR(0) compatible (no conflicts). A conflict occurs when:
- **Shift-Reduce**: Same state has both shift and reduce actions
- **Reduce-Reduce**: Same state has multiple reduce actions

## Modifying the Grammar

To test with different grammars, modify the `initialize_grammar()` function:

```c
void initialize_grammar() {
    // Production 0: S' -> S (always augmented)
    grammar[0].left = 'Z';  // Z represents S'
    strcpy(grammar[0].right, "S");
    
    // Add your productions here
    grammar[1].left = 'S';
    strcpy(grammar[1].right, "YourRHS");
    
    // ...
    
    prod_count = X; // Total productions including S' -> S
    start_symbol = 'Z';
}
```

## Extensions for Post-Lab Work

1. **Test with longer strings**: Try `aaaaaabb$`, `aaaaaaaaaabb$`
2. **Identify conflicts**: Modify grammar to create shift-reduce conflicts
3. **Error recovery**: Extend the parser to suggest corrections for invalid strings
4. **Grammar transformation**: Convert conflicting grammars to LR(0) compatible form

## Learning Outcomes

After completing this practical, you will understand:

1. How LR(0) automata are constructed through closure and GOTO
2. The role of ACTION and GOTO tables in bottom-up parsing
3. The shift-reduce parsing mechanism
4. How conflicts arise and affect parser determinism
5. Why LR(0) can handle more grammars than LL(1)

## References

- Compilers: Principles, Techniques, and Tools (Dragon Book)
- Engineering a Compiler
- Compiler Design in C

---

**Author**: Compiler Construction Lab  
**Practical**: 7 - LR(0) Parser Implementation  
**Hours Required**: 4
