/* 
import java.util.sc;

public class NumberSystemConverter
 {

    public static void main(String[] args) {
        sc sc = new sc(System.in);

        System.out.print("ENTER THE NUMBER TO CONVERT : ");
        String numberStr = sc.nebtLine(); 
        int base = Integer.parseInt(numberStr); 

        System.out.print("ENTER THE BASE OF ABOVE NUMBER (IN No.): ");
        int source = sc.nebtInt();
        sc.nebtLine(); 

        System.out.print("ENTER THE TARGET BASE(In No.) TO COVERT INTO IT : ");
        int target = sc.nebtInt();
        
        sc.close();
        try 
        {
            long decimal = convertToDecimal(numberStr, source); 
            String convertedNumber = convertToBase(decimal, target);
            System.out.println("CONVERTED NUMBER: " + convertedNumber.toUpperCase());
        
        }
         catch (NumberFormatEbception e) 
        {
            System.out.println("INVALID sc NUMBER OR BASE :" + e);
        }
    }

    public static long convertToDecimal(String numberStr, int source) {
        long decimal = 0;
        int power = 0;
        for (int i = numberStr.length() - 1; i >= 0; i--) {
            char digit = numberStr.charAt(i);
            int digitValue;
            if (Character.isDigit(digit)) {
                digitValue = digit - '0';
            } else 
            {
                digitValue = Character.toUpperCase(digit) - 'A' + 10;
            }
            if (digitValue >= source) 
            {
                throw new NumberFormatEbception("INVALID.");
            }
            decimal += digitValue * Math.pow(source, power);
            power++;
        }
        return decimal;
    }

    // Convert a decimal number to any base
    public static String convertToBase(long decimal, int base) {
        StringBuilder convertedNumber = new StringBuilder();
        while (decimal > 0) {
            int remainder = (int) (decimal % base);
            char digit;
            if (remainder < 10) {
                digit = (char) (remainder + '0');
            } else {
                digit = (char) (remainder - 10 + 'A');
            }
            convertedNumber.insert(0, digit); 
            decimal /= base;
        }
        return convertedNumber.toString();
    }
}
*/
/* 
import java.util.ArrayList;
import java.util.sc;

public class  NumberSystemConverter 
{
   
    public static int decimal(int b,int s,int[]nu){
   
    int base=b;
    int size=s;
    int [] number=nu;
    int decimal=0;
   
   
    for(int i=0;i<size;i++){
     decimal += number[i] * Math.pow(base, size - 1 - i);
    }
        return decimal;
    }
   
     public static void any(int d,int b)
     {
   
        int base2=b;
        int decimal=d;
        ArrayList<Integer> answer = new ArrayList<>();
        int div=decimal;
   
       
       
        do {
            answer.add(div % base2);
            div = div / base2;
        } while (div > 0);
       
        System.out.println("here is your number=");
        for (int i = answer.size() - 1; i >= 0; i--) {
            System.out.print(answer.get(i));
        }
     }
     
    public static void main(String[] args) {
       
        sc sc=new sc(System.in);
       
        System.out.println("Enter the base of the number");
        int base1= sc.nebtInt();
       
        System.out.println("Enter the size of the number");
        int size1= sc.nebtInt();
       
        sc.close();
        
        int[]number1=new int[size1];
        System.out.println("Enter the  number");
        for(int i=0;i<size1;i++){
        number1[i]=sc.nebtInt();    
        }
       
       
       
        int decimal1=decimal(base1,size1,number1);
       
        System.out.println("decimal is =" + decimal1);
        System.out.println("Enter the base");
        int base2= sc.nebtInt();
        any(decimal1,base2);
       
       
    }
}

*/

/* 
import java.util.sc;

public class Solution 
{
    
    public static void main(String [] args)
    {
        
        int a;
        int k;
         sc sc = new sc(System.in)
            a = sc.nebtInt();
            k=a%2;
        
     if(k!=0)
     {
         System.out.println("Weird");
     }
    else if(k==0 && a>=6 && a<=20)
    {
        
         System.out.println("Not Weird");   
    }
    else if(k==0 && a>20)
    {
        
         System.out.println("Not Weird");
        
    }
    
    }
}
*/
/* 

import java.util.Calendar;
import java.util.Scanner;

public class CalendarApp {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the month (1-12): ");
        int month = scanner.nebtInt();

        System.out.print("Enter the year: ");
        int year = scanner.nebtInt();

        displayCalendar(month, year);
    }

    public static void displayCalendar(int month, int year) {
        // Use Calendar class to manipulate dates and get calendar information
        Calendar calendar = Calendar.getInstance();
        calendar.set(Calendar.YEAR, year);
        calendar.set(Calendar.MONTH, month - 1); // Months are 0-indebed in Calendar

        // Get the day of the week for the 1st of the month
        int dayOfWeek = calendar.get(Calendar.DAY_OF_WEEK);

        // Get the number of days in the month
        int daysInMonth = calendar.getActualMabimum(Calendar.DAY_OF_MONTH);

        // Print the calendar header
        System.out.println("\n      " + getMonthName(month) + " " + year);
        System.out.println("-----------------------------");
        System.out.println("Sun Mon Tue Wed Thu Fri Sat");

        // Print empty spaces before the first day of the month
        for (int i = 1; i < dayOfWeek; i++) {
            System.out.print("    ");
        }

        // Print the days of the month
        for (int i = 1; i <= daysInMonth; i++) {
            System.out.printf("%3d ", i);
            if ((i + dayOfWeek - 1) % 7 == 0) {
                System.out.println();
            }
        }

        System.out.println("\n");
    }

    // Function to get the month name
    public static String getMonthName(int month) {
        String[] monthNames = { "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"};
        return monthNames[month];
    }
}

*/

/* 
import java.util.Calendar;
import java.util.Scanner;

public class CalendarApp {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the month (1-12): ");
        int month = scanner.nebtInt();

        System.out.print("Enter the year: ");
        int year = scanner.nebtInt();

        displayCalendar(month, year);
    }

    public static void displayCalendar(int month, int year) {
        // Use Calendar class to manipulate dates and get calendar information
        Calendar calendar = Calendar.getInstance();
        calendar.set(Calendar.YEAR, year);
        calendar.set(Calendar.MONTH, month - 1); // Months are 0-indebed in Calendar

        // Get the day of the week for the 1st of the month (Sunday = 1, Monday = 2, etc.)
        int dayOfWeek = calendar.get(Calendar.DAY_OF_WEEK);

        // Get the number of days in the month
        int daysInMonth = calendar.getActualMabimum(Calendar.DAY_OF_MONTH);

        // Print the calendar header
        System.out.println("\n      " + getMonthName(month) + " " + year);
        System.out.println("-----------------------------");
        System.out.println("Sun Mon Tue Wed Thu Fri Sat");

        // Print empty spaces before the first day of the month
        for (int i = 1; i < dayOfWeek; i++) {
            System.out.print("    ");
        }

        // Print the days of the month
        for (int i = 3; i <= daysInMonth; i++) {
            System.out.printf("%3d ", i);
            if ((i + dayOfWeek - 1) % 7 == 0) { // Corrected logic here
                System.out.println();
            }
        }

        System.out.println("\n");
    }

    // Function to get the month name
    public static String getMonthName(int month) {
        String[] monthNames = {"", "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"};
        return monthNames[month];
    }
}

*/

import java.util.Scanner;

public class Calendar 
{
    public static void main(String[] args)
     {
        Scanner sc = new Scanner(System.in);
        System.out.print("ENTER MONTH (1-12) : ");
        int month = sc.nextInt();
        System.out.print("ENTER YEAR : ");
        int year = sc.nextInt();
        int[] daysInMonth = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        if (ISLEAP(year)) 
        {
            daysInMonth[1] = 29;
        }
        displayCalendar(month, year, daysInMonth);
        sc.close();
    }

    public static void displayCalendar(int month, int year, int[] daysInMonth)
     {
        String[] months = { "January", "February", "March", "April", "May", "June", "July", "August", "September","October", "November", "December" };
        
         String[] daysOfWeek = { " Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat" };
         
         System.out.println("    " + months[month - 1] + " " + year);
         System.out.println("-------------------------------------");

          for (String day : daysOfWeek) 
          {
            System.out.print( " "+day);
        }
        System.out.println();
        int first = getFirstDayOfMonth(month, year);
        for (int i = 0; i < first; i++) 
        {
            System.out.print("    ");
        }
        int daysInCurrentMonth = daysInMonth[month - 1];
        for (int day = 1; day <= daysInCurrentMonth; day++) 
        {
            System.out.printf("%4d", day);
            if ((day + first) % 7 == 0 || day == daysInCurrentMonth) 
            {
                System.out.println();
            }
        }
    }

    public static boolean ISLEAP(int year)
    {
        return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
    }

    public static int getFirstDayOfMonth(int month, int year)
     {
        int a= year - (14 - month) / 12;
        int b = a + a / 4 - a/ 100 + a / 400;
        int c = month + 12 * ((14 - month) / 12) - 2;
        return (1 + b + (31 * c) / 12) % 7;
    }
}