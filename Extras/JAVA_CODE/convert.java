
/* Create a Java program to demonstrate the concept of method overloading using String.
 Take the input as String through Scanner Class.
 If String without having space, then the character ‘A’ replace by the ‘Z’ also displays length of the string.
 If String has space, replace the second half of the string thought “CHARUSAT”.
 If String Length Is more than 10 with space, then convert String in lowercase.

 */
/* 
 import java.util.Scanner;

 public class convert
 
 { 
       
    String s;
    int l;
    
    public void replace(String s)
    {
         int x= s.length();

         if (x>10) 
         {
             
      if(s.contains(" " ))
         {
            
            s=s.toLowerCase();
            System.out.println(s);
         }
         
      
      } 
       if(s.contains(" "))
      {
        // l=s.length();
         //if(l>10)
         //{
           // s=s.toLowerCase();
            //System.out.println(s);
            s.replace(" ", "charusat");
            //s.replace(oldChar, newChar);
            }
            else 
            {
               s=s.replace('A', 'Z');

               System.out.println(" " + s);

               System.out.println(" LENGTH : " + s.length());

            }
         }
      }

      public static void convert(String []args)
      
      {
         convert rep = new convert();

         Scanner sc=new Scanner(System.in);
         System.out.println("ENTER A STRING : ");
         //sc.hasNextLine();
         String s=sc.nextLine();
         

      }  

      */


/*
      import java.util.Scanner;

      public class convert 
      {
            
           public static String processString(String str) 
         {
               int mid = str.length() / 2;

             return str.substring(0, mid-1) + "CHARUSAT";
      
         }

         public static String processString(String str, boolean convertToLowercase) 
      {
        if (convertToLowercase) 
        {
           // return str.toLowerCase();
            str = str.toLowerCase().replace('A', 'Z') + " LENGTH : " + str.length();
           
        }
        return str.toLowerCase();
           
        
      }

         public static void convert(String[] args) 
         {
            Scanner sc = new Scanner(System.in);
            System.out.println("ENTER A STRING :");
            String input = sc.nextLine();
            sc.close();

            if (input.contains(" ")) 
            {
               if (input.length() > 10) 
               {
                System.out.println(processString(input, true));
               }   
               else 
               {  
                System.out.println(processString(input));
               }
           } 
            else
            {
            System.out.println(processString(input, false));
            }

    }
}
   
 
*/
import java.util.Scanner;

public class convert {
    public static void main (String[] args) 
    {
        Scanner sc = new Scanner(System.in);
        System.out.println("ENTER A STRING :");
        String input = sc.nextLine();
        overloadMethod(input);
        sc.close();
    }

    public static void overloadMethod(String str) 
    {
        if (!str.contains(" "))
         { 
            str = str.replace("A", "Z");
            System.out.println("MODIFIED STRING : " + str);
            System.out.println("STRING LENGTH : " + str.length());
        } 
        else if (str.contains(" "))
         
         {
             overloadMethod(str, str.length());
         }
    }

    public static void overloadMethod(String str, int length) 
     {
        if (length > 10)
         {
            str = str.toLowerCase();
        }
        int mid = str.length() / 2;

        String secondHalf = str.substring(mid-1);

        str = str.substring(0, mid-1) + "CHARUSAT";
        
        System.out.println("MODIFIED STRING : " + str);
    }
}
