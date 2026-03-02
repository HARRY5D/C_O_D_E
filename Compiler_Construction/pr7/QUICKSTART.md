# LR(0) Parser - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Compile
```bash
cd "d:\JAVA\CODE\Compiler_Construction\pr7\"
gcc pr7.c -o pr7
```

### Step 2: Run
```bash
./pr7
```

### Step 3: Test
When prompted, enter test strings:

**✓ Valid Inputs (will be accepted):**
- `ab$`
- `aab$`
- `bb$`
- `aabb$`
- `aaaabb$`

**✗ Invalid Inputs (will be rejected):**
- `a$`
- `b$`
- `abab$`
- `bbb$`

---

## 📋 What You'll See

### 1. Grammar Display
```
0. Z -> S
1. S -> A A
2. A -> a A
3. A -> b
```

### 2. LR(0) States
All canonical item sets with closure

### 3. ACTION & GOTO Table
```
STATE │ ACTION (a, b, $) │ GOTO (S, A)
──────┼──────────────────┼─────────────
  0   │ s2  s4           │ 1   3
  1   │         acc      │
  ...
```

### 4. Parsing Trace
```
Step  Stack         Input    Action
1     [0]           aab$     Shift 2
2     [0 2a]        ab$      Shift 2
3     [0 2a 2a]     b$       Shift 4
...
```

---

## 📝 Sample Test Session

```bash
$ ./pr7

╔═══════════════════════════════════════╗
║  LR(0) PARSER - COMPILER CONSTRUCTION ║
╚═══════════════════════════════════════╝

➤ Grammar Loaded:
   0. Z -> S
   1. S -> A A
   2. A -> a A
   3. A -> b

➤ Constructing LR(0) Automata...
✓ LR(0) Automata Construction Complete!
  Total States: 8

[States displayed...]

╔═══════════════════════════════════════╗
║            PARSE MENU                 ║
╠═══════════════════════════════════════╣
║  1. Parse a string                    ║
║  2. Exit                              ║
╚═══════════════════════════════════════╝
Enter choice: 1

Enter input string (use $ at end): aab$

[Parsing trace shown...]

✓ STRING ACCEPTED! Input belongs to the grammar.
```

---

## 🎯 Quick Reference

### Grammar Language
**Pattern:** `a*b a*b`  
**Description:** Exactly 2 'b' characters, each optionally preceded by 'a's

### Test Examples
| Input     | Result | Reason                          |
|-----------|--------|---------------------------------|
| `ab$`     | ✓      | Valid: a,b then b               |
| `bb$`     | ✓      | Valid: b then b                 |
| `aabb$`   | ✓      | Valid: aa,b then b              |
| `a$`      | ✗      | Invalid: No b's                 |
| `b$`      | ✗      | Invalid: Only 1 b               |
| `bbb$`    | ✗      | Invalid: 3 b's                  |
| `abab$`   | ✗      | Invalid: Wrong structure        |

---

## 🔧 Troubleshooting

**Error: "gcc not found"**
- Install MinGW or GCC compiler
- Add to PATH environment variable

**Error: "permission denied"**
```bash
chmod +x pr7
./pr7
```

**Program crashes on input**
- Ensure input ends with `$`
- Use only characters 'a', 'b', and '$'

---

## 📚 Understanding the Output

### LR(0) Item Notation
- `A -> a•b` means: dot is between 'a' and 'b'
- `A -> ab•` means: dot at end (reduce point)
- `A -> •ab` means: dot at start (just entered this production)

### ACTION Table Codes
- **sN**: Shift input symbol and go to state N
- **rN**: Reduce by production number N
- **acc**: Accept the input string
- **(blank)**: Error - invalid input

### GOTO Table
- Shows state transitions for non-terminals after reductions
- Used when popping symbols during reduce operations

---

## 🎓 Learning Objectives Checklist

- [ ] Understand closure computation for LR(0) items
- [ ] Trace GOTO function for state transitions
- [ ] Read ACTION & GOTO tables
- [ ] Follow shift-reduce parsing trace
- [ ] Identify valid vs invalid strings
- [ ] Recognize conflict-free grammar characteristics

---

## 📖 Additional Resources

- **Full Documentation**: See `README.md`
- **Test Cases**: See `TEST_CASES.md`
- **Modify Grammar**: Edit `initialize_grammar()` function in `pr7.c`

---

## ⚡ Power User Tips

**Modify the Grammar:**
```c
// In initialize_grammar() function
grammar[1].left = 'S';
strcpy(grammar[1].right, "YourProduction");
```

**Test Multiple Strings:**
```bash
# Prepare a test file
echo "1
aab$
1
bb$
2" > test_input.txt

# Run with input redirection
./pr7 < test_input.txt
```

---

**Need Help?** Check the full README.md or refer to TEST_CASES.md for detailed examples.

Happy Parsing! 🎉
