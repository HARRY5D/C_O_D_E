
import java.util.Scanner;


/*
import java.util.sc;

public class morse_decode
{
    public static void main(String[] args) 
    {
        sc sc = new sc(System.in);

        String s[] = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x"," ","y", "z","  "};
        String morse[] = {".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".---.", "--.-", ".-.","...", "-", "..-", "...-", ".--", "-..-", "-.--", "--..","____"};

      
        System.out.println("ENTER 1 FOR STRING TO MORSE CONVERSION. \n" + "ENTER 2 FOR MORSE CODE TO STRING CONVERSION.  \n" +"ENTER 3 TO EXIT.");
        int a = sc.nextInt();

        while(a!=3)
        {
        if (a == 1) 
        {
            sc.nextLine();
    
            String  s2 = sc.nextLine().toLowerCase();
            
           // s2.split(" ");
            
            String s1[] = new String[s2.length()];

            for (int i = 0; i < s2.length(); i++) 
            {
                for (int j = 0; j <s.length; j++) 
                {
                   // if (s1[i].equals(morse[j]))
                    if (s2.charAt(i)== s[j].charAt(0))
                     {
                        s1[i] = s[j];
                         morse[j]=s[j];
                        System.out.print(morse[j]);
                       // System.out.print(morse[i]);
                   
                    }
                }

            }

        }
       else  if (a == 2) 
       {
            sc.nextLine();
            String  s2 = sc.nextLine();
            String s1[] = s2.split(" ");
            
            for (int i = 0; i <s1.length; i++)
               {
                for (int j = 0; j < morse.length; j++) 
                       { 
                          if (s1[i].equals(morse[j]))
                          {
                             System.out.print(s[j]);
                            break;}
                          }
                   }
               }
         }
    }
}
*/
/*
import java.util.sc;

public class morse_decode 
{
    public static void main(String[] args) 
    {
        sc sc = new sc(System.in);

        String s[] = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", " ", "y", "z", "  "};
        String morse[] = {".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".---.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--..", "_____"};

        System.out.println("ENTER 1 FOR STRING TO MORSE CONVERSION. \n" + "ENTER 2 FOR MORSE CODE TO STRING CONVERSION.  \n" +"ENTER 3 TO EXIT.");
        int a = sc.nextInt();

        while (a != 3) 
        {
            if (a == 1) 
            {
                sc.nextLine(); 
                String s2 = sc.nextLine().toLowerCase(); 

                for (int i = 0; i < s2.length(); i++) 
                {
                    for (int j = 0; j < s.length; j++) 
                    {
                        if (s2.charAt(i) == s[j].charAt(0)) 
                        {
                            System.out.print(morse[j] + " ");
                            break;
                        }
                    }
                }
                System.out.println(); 

            }
             else if (a == 2) 
            {
                sc.nextLine(); 
                String s2 = sc.nextLine();
                String s1[] = s2.split(" ");

                for (int i = 0; i < s1.length; i++) 
                {
                    for (int j = 0; j < morse.length; j++)
                     {
                        if (s1[i].equals(morse[j])) 
                        {
                            System.out.print(s[j]);
                            break;
                        }
                    }
                }
            }
            System.out.println("\nENTER 1 FOR STRING TO MORSE CONVERSION. \n" + "ENTER 2 FOR MORSE CODE TO STRING CONVERSION.  \n" +"ENTER 3 TO EXIT.");
            a = sc.nextInt(); 
        }
        sc.close();
    }
}
    


    /*
    import java.util.sc;

public class morse_decode {
    public static void main(String[] args) {
        sc sc = new sc(System.in);

        String s[] = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", " ", "y", "z", "  "};
        String morse[] = {".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".---.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--..", "_____"};

        System.out.println("ENTER 1 FOR STRING TO MORSE CONVERSION. \n" + "ENTER 2 FOR MORSE CODE TO STRING CONVERSION.  \n" +"ENTER 3 TO EXIT.");
        int a = sc.nextInt();

        while (a != 3) {
            if (a == 1) {
                sc.nextLine(); // Consume the leftover newline character
                String s2 = sc.nextLine().toLowerCase(); 

                for (int i = 0; i < s2.length(); i++) {
                    for (int j = 0; j < s.length; j++) {
                        if (s2.charAt(i) == s[j].charAt(0)) {
                            System.out.print(morse[j] + " "); // Print morse code
                            // Don't break here - we want to process the whole string
                        }
                    }
                }
                System.out.println(); // Print a newline after conversion

            } else if (a == 2) {
                sc.nextLine(); // Consume the leftover newline character
                String s2 = sc.nextLine();
                String s1[] = s2.split(" ");

                for (int i = 0; i < s1.length; i++) {
                    for (int j = 0; j < morse.length; j++) {
                        if (s1[i].equals(morse[j])) {
                            System.out.print(s[j]);
                            break; // Exit the inner loop after finding a match
                        }
                    }
                }
            }
            System.out.println("\nENTER 1 FOR STRING TO MORSE CONVERSION. \n" + "ENTER 2 FOR MORSE CODE TO STRING CONVERSION.  \n" +"ENTER 3 TO EXIT.");
            a = sc.nextInt(); 
        }
        sc.close();
    }
}
*/


public class morse_decode
{
       public static void main(String[] args)
     {
        Scanner sc = new Scanner(System.in);

        System.out.print("ENTER NO. OF STUDENTS : ");
        int n = sc.nextInt();

        sc.nextLine(); 
        
        String[] name = new String[n];
        int[] AGE = new int[n];
        int[] roll = new int[n];

        for (int i = 0; i < n; i++) 
        {
            System.out.println("\nENTER DETAIL FOR STUDENT :  " + (i + 1) + ":");
            System.out.print("NAME : ");
            name[i]=sc.nextLine();
            System.out.print("AGE : ");
            AGE[i]=sc.nextInt();

            sc.nextLine();            
            
            System.out.print("ROLL NO. : ");
            roll[i] = sc.nextInt();
        }

        System.out.println("\nSTUDENT DETAILS :");

        for (int i = 0; i < n; i++) {
            System.out.println("NAME: " + name[i] + ", AGE: " + AGE[i] + ", ROLL NO.  : " + roll[i]);
        
        sc.close();
    }
  }
}