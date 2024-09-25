import java.util.Stack;

public class p5_3b 
{
    private int precedence(char ch) 
    {
        switch (ch) 
        {
            case '+':
            case '-':
                return 1;
            case '*':
            case '/':
                return 2;
            case '^':
                return 3;
        }
        return -1;
    }

    public String convertToPostfix(String infix) 
    {
        StringBuilder postfix = new StringBuilder();
        Stack<Character> stack = new Stack<>();

        for (int i = 0; i < infix.length(); i++) 
        {
            char ch = infix.charAt(i);

            if (Character.isLetterOrDigit(ch)) 
            {
                postfix.append(ch);
            } 
            else if (ch == '(') 
            {
                stack.push(ch);
            } 
            else if (ch == ')') 
            {
                while (!stack.isEmpty() && stack.peek() != '(') 
                {
                    postfix.append(stack.pop());
                }
                if (!stack.isEmpty() && stack.peek() == '(') 
                {
                    stack.pop();
                }
            } 
            else 
            {
                while (!stack.isEmpty() && precedence(ch) <= precedence(stack.peek())) 
                {
                    postfix.append(stack.pop());
                }
                stack.push(ch);
            }
        }

        while (!stack.isEmpty()) 
        {
            postfix.append(stack.pop());
        }

        return postfix.toString();
    }

    public static void main(String[] args) 
    {
        p5_3b converter = new p5_3b();
        String infix1 = "A + B * C + D";
        String infix2 = "((A + B) - C * (D / E)) + F";

        System.out.println("INFIX : " + infix1);
        System.out.println("POSTFIX : " + converter.convertToPostfix(infix1));

        System.out.println("INFIX : " + infix2);
        System.out.println("POSTFIX : " + converter.convertToPostfix(infix2));
    }
}