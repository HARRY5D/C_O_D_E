# Email Validator - Quick Start Guide

## What's Been Created

Your pr3 directory now contains:

### 1. Email Validation Program (Problem Requirement)
- `email_validator.c` - Main email validation program using POSIX regex
- `EMAIL_VALIDATOR_README.md` - Complete documentation
- `POST_LAB_WORK.md` - Post-laboratory analysis and reflection

### 2. Lexical Analyzer (Separate Practical)
- `lexer.l` - Flex lexical analyzer for C-like language
- `main.c` - Driver program for lexer
- `test.c` - Test input file

### 3. Build System
- `Makefile` - Automated build and run commands

---

## Quick Start - Email Validator

### Step 1: Compile (in Linux/WSL)
```bash
cd /mnt/d/JAVA/CODE/Compiler_Construction/pr3
gcc email_validator.c -o email_validator
```

### Step 2: Run
```bash
./email_validator
```

### Step 3: Choose Mode
- Option 1: Interactive (type emails manually)
- Option 2: Test Mode (runs all test cases automatically)

---

## Using Makefile (Recommended)

```bash
# Build email validator
make email_validator

# Run email validator
make run-email

# Build lexer
make lexer

# Run lexer
make run-lexer

# Clean all builds
make clean

# Rebuild everything
make rebuild
```

---

## Test Cases Summary

### Should Print "Valid Email":
✓ abc@gmail.com
✓ student123@charusat.edu
✓ User.name-90@domain.co.in
✓ test_user@example.org
✓ john.doe+tag@company.com

### Should Print "Invalid Email":
✗ abc@@gmail.com (double @)
✗ abc@.com (domain starts with dot)
✗ abc@domain (no extension)
✗ @domain.com (no username)
✗ user@ (no domain)

---

## Key Files for Submission

For your lab report, focus on these files:

1. **email_validator.c** - Main implementation (117 lines)
2. **EMAIL_VALIDATOR_README.md** - Technical documentation
3. **POST_LAB_WORK.md** - Analysis, extended tests, and reflection
4. **Screenshot/Output** - Capture program execution

---

## Program Features

### 1. Interactive Mode
- Enter emails one by one
- Real-time validation
- Type 'quit' to exit

### 2. Test Mode
- Automatically runs 20+ test cases
- Categorized: Valid, Invalid, Edge Cases
- Clear output formatting

### 3. Code Quality
- ✓ Well-commented code
- ✓ Modular design (separate validation function)
- ✓ Comprehensive error handling
- ✓ Memory management (regfree)
- ✓ POSIX standard compliance

---

## Understanding the Regex Pattern

```regex
^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$
```

| Part | Meaning |
|------|---------|
| `^` | Start of string |
| `[A-Za-z0-9._%+-]+` | Username (1+ chars) |
| `@` | Literal @ |
| `[A-Za-z0-9.-]+` | Domain (1+ chars) |
| `\.` | Literal dot |
| `[A-Za-z]{2,}` | Extension (2+ letters) |
| `$` | End of string |

---

## Answers to Key Questions

### 1. Role of Regular Expressions
- Formal pattern specification
- Structural validation beyond simple comparison
- Reusable pattern matching engine

### 2. POSIX Regex in C
- `regcomp()`: Compile pattern
- `regexec()`: Match pattern
- `regfree()`: Free resources

### 3. Email Components
- Local part (username)
- @ symbol
- Domain name
- Domain extension (.com, .edu, etc.)

### 4. Regex vs String Comparison
- Regex: Pattern-based, flexible, structural
- String: Character-by-character, exact match

### 5. Real-World Usage
- User registration
- Form validation
- Database integrity
- Email marketing platforms
- Authentication systems

---

## Troubleshooting

### Error: "undefined reference to regcomp"
**Solution**: You're on Windows. Use WSL or Linux.

### Error: "regex.h not found"
**Solution**: Install build-essential: `sudo apt install build-essential`

### Lexer errors
**Note**: The lexer.l file is for a different practical (lexical analysis).
Don't mix it with the email validator.

---

## Next Steps

1. ✓ Compile and run the program
2. ✓ Test with various email inputs
3. ✓ Review the documentation files
4. ✓ Complete the reflection questions
5. ✓ Prepare lab report with screenshots

---

## Contact/Questions

If the program doesn't work:
1. Ensure you're in Linux/WSL environment
2. Check gcc is installed: `gcc --version`
3. Verify file permissions: `chmod +x email_validator`
4. Review compilation errors carefully

---

**Implementation Time**: 1:30 hours  
**Status**: ✓ Complete  
**Date**: January 16, 2026
