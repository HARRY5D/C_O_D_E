
import java.util.Stack;

class p5_3c 
{
    public static int evaluatePostfix(String expression) 
    {
        Stack<Integer> stack = new Stack<>();
        
    String[] tokens = expression.split("\\s+");
    
    for (String token : tokens) {
        if (token.matches("\\d+")) {
            stack.push(Integer.parseInt(token));
        } else if ("+-*/".contains(token)) {
            if (stack.size() < 2) {
                throw new IllegalArgumentException("INVALID EXPRESSION.");
            }
            
            int operand2 = stack.pop();
            int operand1 = stack.pop();
            int result;
            
            switch (token) {
                case "+":
                    result = operand1 + operand2;
                    break;
                case "-":
                    result = operand1 - operand2;
                    break;
                case "*":
                    result = operand1 * operand2;
                    break;
                case "/":
                    if (operand2 == 0) {
                        throw new ArithmeticException("DIVISION BY ZERO.");
                    }
                    result = operand1 / operand2;
                    break;
                default:
                    throw new IllegalArgumentException("Invalid operator: " + token);
            }
            stack.push(result);
        }
    }
    
    if (stack.size() != 1) {
        throw new IllegalArgumentException("INVALID EXPRESSION");
    }
    
    return stack.pop();
    }


    public static void main(String[] args) 
    {
    String expression = "2 3 1 * + 9 -";
    System.out.println("INPUT : " + expression);
    int result = evaluatePostfix(expression);
    System.out.println("OUTPUT : " + result);
}

}