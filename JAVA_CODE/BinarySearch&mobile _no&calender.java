
import java.util.Scanner;

class BinarySearch 

{
    public static void main(String[] args) 

    {
        String number;
        try (Scanner scan = new Scanner(System.in)) {
            System.out.println("ENTER A MOBILE NUMBER IN THE GIVEN FORMAT :  +91-AA-BBB-CCCCC ");
            number = scan.nextLine();
        }
            String op_Code = number.substring(4, 6);
            String msc = number.substring(7, 10);
            String subs_Code = number.substring(11,16);

            System.out.println(" MOBILE SYSTEM OPERATOR CODE IS :  " + op_Code);
            System.out.println(" MSC IS :  " + msc);
            System.out.println(" UNIQUE CODE IS :  " + subs_Code);
        
    }
}

/* 
import java.util.Scanner;
public class FIRST
{
     public static void main(String[] args) 

     {
        Scanner sc = new Scanner(System.in);
        System.out.println("ENTER A NO IN FORMAT +91-AA-BBB-CCCCC : ");
        String number=sc.nextLine();
        String[]  sp= number.split("-",6);
        System.out.println(" OPERATOR CODE : "+sp[1]);
        System.out.println(" MSC CODE : "+sp[2]);        
        System.out.println(" UNIQUE CODE : "+sp[3]);

    }

}

*/
/* 
import java.time.DayOfWeek;
import java.time.Month;
import java.time.Year;
import java.util.Scanner;
import java.util.Calendar;

public class First
{
public static void main(String[] args)
{
        {

         System.out.println("MONTH : "+DayOfWeek);
         System.out.println("MONTH : "+Month );
         System.out.println("MONTH : "+Year);


        }

}

}  */
/* 
 
import java.util.Arrays;
import java.util.Scanner;
public class First(2nd)

{

     public static void main(String[] args) 

     {
        Scanner sc = new Scanner(System.in);

       
                int s;
                System.out.print("Enter size of the array: ");
                s = sc.nextInt();
                int[] arr = new int[s];
        
                for (int b = 0; b < s; b++) 
                
                {
                    System.out.print("Enter the element " + (b + 1) + " : ");
                    arr[b] = sc.nextInt();
                }
                for (int i = 0; i < arr.length; i++) 
                {
                    System.out.print(arr[i] + " ");
                }


                linear.close();
                
            
    

    }

}
*/
/* 
import java.util.Arrays;
import java.util.Scanner;

public class BinarySearch 

{
    public int search(int[] nums, int target) 
    {
        int x = 0;
        int y = nums.length - 1;

        while (x <= y) 
        {
            int mid = (x + y)  / 2; 
            if (nums[mid] == target) 
            {
                return mid; 
            }
             else if (nums[mid] < target) 
             {
                x = mid + 1; 
            } 
            else 
            {
                y = mid - 1; 
            }
        }
        return -1; 
    }

    public static void main(String[] args) 
    {
        BinarySearch binarySearch = new BinarySearch();
        Scanner sc = new Scanner(System.in);
        System.out.print("ENTER SIZE OF ARRAY : ");
        int size = sc.nextInt();
        sc.nextLine(); // Consume newline

        int[] nums = new int[size];
        System.out.print("ENTER ELEMENTS OF ARRAY : ");
        for (int i = 0; i < size; i++) 
        {
            nums[i] = sc.nextInt();
        }

        System.out.print("ENTER THE  ELEMENT TO FIND  : ");
        int target = sc.nextInt();

        
        Arrays.sort(nums);

        int result = binarySearch.search(nums, target);

        if (result != -1) 
        {
            System.out.println("ELEMENT FOUND AT INDEX VALUE :  " + result);
        } else 
        {
            System.out.println("ELEMENT NOT FOUND IN ARRAY.");
        }
    }
}
*/