'''
(c) Given a postfix expression, the task is to evaluate the postfix expression.
Postfix expression: The expression of the form “a b operator” (ab+) i.e., when a pair of operands is followed by an operator.
Examples:
Input: str = “2 3 1 * + 9 -“
Output: -4
Explanation: If the expression is converted into an infix expression, it will be 2 + (3 * 1) – 9 = 5 – 9 = -4.

'''
def evaluate_postfix(expression):
   
    stack = []

    tokens = expression.split()

    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        elif token in "+-*/":
            if len(stack) < 2:
                raise ValueError("INVALID EXPRESSION.")

            operand2 = stack.pop()
            operand1 = stack.pop()

            if token == "+":
                result = operand1 + operand2
            elif token == "-":
                result = operand1 - operand2
            elif token == "*":
                result = operand1 * operand2
            elif token == "/":
                if operand2 == 0:
                    raise ZeroDivisionError("DIVISION BY ZERO.")
                result = operand1 / operand2
            stack.append(result)

    if len(stack) != 1:
        raise ValueError("INVALID EXPRESSION")

    return stack[0]
expression = "2 3 1 * + 9 -"
print("INPUT : ",expression)
result = evaluate_postfix(expression)
print("OUTPUT :",result) 