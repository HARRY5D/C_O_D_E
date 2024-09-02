
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