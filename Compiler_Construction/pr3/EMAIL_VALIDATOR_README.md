# Email Validation Using POSIX Regular Expressions

## Problem Statement
Design and implement a C program that employs the regular expression engine to validate email syntax according to formal specifications. The solution translates email pattern specifications into an intelligent validation mechanism.

## Components of a Valid Email Address

1. **Local Part (Username)**: 
   - Alphanumeric characters (A-Z, a-z, 0-9)
   - Special characters: dot (.), underscore (_), percent (%), plus (+), hyphen (-)
   - Must have at least one character

2. **@ Symbol**: Mandatory separator between local and domain parts

3. **Domain Name**:
   - Alphanumeric characters
   - Can contain dots and hyphens
   - Must have at least one character

4. **Domain Extension**:
   - Must start with a dot
   - At least 2 alphabetic characters (e.g., .com, .edu, .co.in)

## Regular Expression Pattern
```regex
^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$
```

### Pattern Breakdown:
- `^` - Start of string anchor
- `[A-Za-z0-9._%+-]+` - Local part: one or more valid characters
- `@` - Literal @ symbol
- `[A-Za-z0-9.-]+` - Domain: one or more valid domain characters
- `\.` - Escaped dot (literal period)
- `[A-Za-z]{2,}` - Extension: minimum 2 alphabetic characters
- `$` - End of string anchor

## Compilation and Execution

### In Linux (WSL/Ubuntu):
```bash
# Compile the program
gcc email_validator.c -o email_validator

# Run the program
./email_validator
```

### Expected Workflow:
1. Choose mode (Interactive or Test)
2. For Interactive: Enter emails one by one
3. For Test: Automatically validates predefined test cases
4. Program outputs "Valid Email" or "Invalid Email"

## Test Cases

### Valid Emails:
- `abc@gmail.com` ✓
- `student123@charusat.edu` ✓
- `User.name-90@domain.co.in` ✓
- `test_user@example.org` ✓
- `john.doe+tag@company.com` ✓

### Invalid Emails:
- `123@company.org` ✗ (starts with number - actually valid in our pattern)
- `abc@@gmail.com` ✗ (double @)
- `abc@.com` ✗ (domain starts with dot)
- `abc@domain` ✗ (missing extension)
- `@domain.com` ✗ (missing local part)
- `user@` ✗ (missing domain)
- `user name@domain.com` ✗ (space in local part)

## Key Concepts

### 1. Regular Expressions Role
Regular expressions provide a formal grammar for pattern matching, enabling:
- Declarative pattern specification
- Efficient string validation
- Complex structural verification

### 2. POSIX Regex Functions
- `regcomp()`: Compiles regex pattern into executable form
- `regexec()`: Executes pattern matching against input string
- `regfree()`: Releases compiled regex resources

### 3. Regex vs String Comparison
| Aspect | Regex | String Comparison |
|--------|-------|-------------------|
| Flexibility | Highly flexible patterns | Exact match only |
| Validation | Structural validation | Character-by-character |
| Scalability | Single pattern for variations | Multiple conditions |
| Performance | Compiled pattern reuse | Simple iteration |

## Real-World Applications

1. **E-Commerce Platforms**: Customer account registration
2. **Email Services**: Prevent invalid address submission
3. **Authentication Systems**: User identity verification
4. **Form Validation**: Web and mobile applications
5. **Database Integrity**: Ensure valid email storage
6. **Compiler Design**: Token pattern recognition

## Skills Demonstrated

1. ✓ Regex-based input validation
2. ✓ Interpretation of formal grammar rules
3. ✓ Algorithmic reasoning and problem decomposition
4. ✓ Secure and reliable input handling
5. ✓ Debugging and boundary-case testing

## Learning Outcomes Achieved

1. Successfully translated formal regex syntax into executable validation logic
2. Applied POSIX regex functions (`regcomp`, `regexec`, `regfree`) for pattern verification
3. Evaluated structural correctness of user input in real-time
4. Implemented comprehensive test coverage including edge cases

## Time Investment
Total Implementation Time: **1:30 hours**

---
*Course: Compiler Construction*  
*Topic: Pattern Recognition and Lexical Analysis*  
*Date: January 16, 2026*
