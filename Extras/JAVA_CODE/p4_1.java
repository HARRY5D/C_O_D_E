/*
 Write a Java Program which should ask for two integers and then add them together and print the result.
  Your task is to write the code which asks for the numbers and uses exception handling to check if the given numbers are integers. 
  If the user inputs something else than an integer, “You did not type an integer!” is printed on screen. 
  Program also includes the variable inputCorrect which value needs to be set to false if the given numbers are not integers.
 */

import java.util.*;

 public class p4_1

{ 
     public static void main(String[] args) 
    {
      Scanner sc = new Scanner(System.in);
      boolean inputCorrect = true;
     
      int n1 = 0, n2 = 0;    
          
      while (true) 
       {
         try 
         { 
             System.out.print("ENTER THE 1st INTEGER : ");
            n1 = sc.nextInt();
            break;
           } 
           catch (InputMismatchException e) 
           {
                System.out.println("YOU DID NOT TYPE AN INTEGER!");
                sc.next(); 
            }
         }
    
        while (true) 
        {
            try 
             {
                System.out.print("ENTER THE 2nd INTEGER : ");
                n2 = sc.nextInt();
                break;
            } 
            catch (InputMismatchException e) 
            {
                System.out.println("YOU DID NOT TYPE AN INTEGER!");
                sc.next(); 
            }
        }
        if (inputCorrect=true) 
        {
            int sum = n1 + n2;
            System.out.println("THE SUM OF TWO INTEGERS IS : " + sum);            
        } 
        sc.close();
        
    }

}
