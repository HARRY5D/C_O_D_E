/*
import java.util.Scanner;

 class leet {
  public int specialArray(int[] nums) 
  {
     for (int x = 0; x <= 1000; x++)
     {
      int count = 0;
      for (int num : nums)
       {
        if (num >= x)
         {
          count++;
        }
      }
      if (count == x)
      
      {
        return x;
      }
    }
    return -1;
  }

  public static void main(String[] args) 
  {
    Scanner sc = new Scanner(System.in);
    System.out.print("ENTER NO. OF ELEMENTS IN ARRAY : ");
    int n = sc.nextInt();
    int[] nums = new int[n];
    System.out.println("INPUT : ");
    for (int i = 0; i < n; i++)
     {
      nums[i] = sc.nextInt();
    }
    sc.close();
    leet ans = new leet();
    int result = ans.specialArray(nums);
    System.out.println(" OUTPUT : " + result);

    
  }
}*/



import java.util.Scanner;

public class leet {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

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
                            break; // Exit the inner loop after finding a match
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

