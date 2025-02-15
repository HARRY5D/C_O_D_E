'''
(b) Given an infix expression, the task is to convert it to a postfix expression.
Infix Expression: The expression of type a ‘operator’ b (a+b, where + is an operator) i.e., when the operator is between two operands.
Postfix Expression: The expression of the form “a b operator” (ab+) i.e., When every pair of operands is followed by an operator.
Examples:
Input: A + B * C + D
Output: ABC*+D+
Input: ((A + B)-C * (D / E)) + F
Output: AB+CDE/*-F+

'''
def infix_to_postfix(infix):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack = []
    postfix = ''



    for char in infix:
        if char == ' ':  
            continue
        elif char.isalpha():  
            postfix += char + ' '
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop() + ' '
            stack.pop()  
        else:
            while stack and stack[-1] != '(' and precedence[char] <= precedence.get(stack[-1], 0):
                postfix += stack.pop() + ' '
            stack.append(char)

    while stack:
        postfix += stack.pop() + ' '
    return postfix.strip() 


print("INPUT : A + B * C + D ")
print("OUTPUT : ",(infix_to_postfix('A + B * C + D')))


print("INPUT : ((A + B)-C * (D / E)) + ")
print("OUTPUT : ",(infix_to_postfix('((A + B)-C * (D / E)) +')))

