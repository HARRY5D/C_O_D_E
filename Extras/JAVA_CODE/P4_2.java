/*Write a java program with two classes (SmallException and BigException)
 and two methods to the p4_2 class (printErrorReport and testValue).
  SmallException and BigException are individual exception classes deriving from Exception class.
   Both classes require a constructor that receives a String object as parameter.
    Parameter is used to relay an informative message with the exception.
     Parameter is relayed to the superclass constructor. printErrorReport method receives the exception as 
     a parameter and prints the error report of the exception using getMessage method. testValue method receives 
     the tested number as a parameter. If the number is lower than five, method throws the SmallException
      and parameter is the message: VALUE IS lower than 5. If the
number is higher than 10, method throws the BigException and 
parameter is the message: VALUE IS higher than 10.
 */
// Define the SmallException class

import java.util.Scanner;

class SmallException extends Exception 
{
    public SmallException(String  message) 
    {
        super(message);
    }
}

class BigException extends Exception 
{
    public BigException(String message) 
    {
        super(message);
    }
}

class P4_2 
 {
    public void printErrorReport(Exception e) 
    {
        System.out.println("ERROR REPORT : " + e.getMessage());
    }

    public void testValue(int value) throws SmallException, BigException 
    {
        if (value < 5) 
        {
            throw new SmallException("VALUE IS LOWER than 5");
        } 
        else if (value > 10) 
        {
            throw new BigException("VALUE IS HIGHER THAN 10");
        } 
        else 
        {
            System.out.println("VALUE IS WITHIN RANGE OF [5, 10]");
        }
    }
    
    public static void main(String[] args) 
    {
        P4_2 obj = new P4_2();
        Scanner sc = new Scanner(System.in);
    
        while (true) 
        {
            try 
            {
                System.out.print("ENTER A No. (OR) TYPE EXIT TO QUIT : ");
                String input = sc.next();
    
                if (input.equalsIgnoreCase("exit")) 
                {
                    break;
                }
                int value = Integer.parseInt(input);
                obj.testValue(value);
    
            } 
          catch (NumberFormatException e) 
         {    System.out.println("INVALID INPUT.ENTER A VALID INTEGER..");          } 
            
            catch (SmallException | BigException e)
            {
                obj.printErrorReport(e);
            }
        }
        sc.close();
    }
}