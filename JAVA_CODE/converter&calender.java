 //import java.util.Scanner;

//public class converter 
//{
  //  public static void main(String[] args) 
    /* 
        long decimal;
        int source1;
        try (Scanner sc = new Scanner(System.in)) {
            System.out.print("ENTER THE NUMBER TO CONVERT : ");
            int number = sc.nextInt();
            System.out.print("ENTER THE BASE OF ABOVE NUMBER (IN No.): ");
            int source = sc.nextInt();
            sc.nextLine();
            System.out.print("ENTER THE  BASE(In No.) TO CONVERT INTO : ");
            int target = sc.nextInt();
            decimal = convertToDecimal(number, source);
            String convertedNumber = convertToBase(decimal, target);
            System.out.println("CONVERTED NUMBER: " + convertedNumber);
            System.out.print("ENTER THE  BASE(In No.) THAT YOU WANT : ");
            source1 = sc.nextInt();
        
          sc.close();
        }
              String originalNumber = convertToBase(decimal, source1);
            System.out.println("CONVERTED NUMBER: " + originalNumber);
        
        
    }

    public static long convertToDecimal(int number, int source) 
    {
        long decimal = 0;
        int power = 0;
        while (number > 0) 
        {
            int remainder = number % source;
            decimal += remainder * Math.pow(source, power);
            number /= source;
            power++;
        }
        return decimal;
    }

    public static String convertToBase(long decimal, int base) 
    {
        StringBuilder convertedNumber = new StringBuilder();
        while (decimal > 0) 
        {
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

*/        //return convertedNumber.toString();
/* 
        Scanner scan = new Scanner(System.in);
        int i = scan.nextInt();

double d=scan.nextDouble();
String s=scan.nextLine();
        // Write your code here.
scan.close();
        System.out.println("String: " + s);
        System.out.println("Double: " + d);
        System.out.println("Int: " + i);
    }
}*/
  //  }
//}

/* 
import java.util.Scanner;

public class CalendarApp {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the month (1-12): ");
        int month = scanner.nextInt();

        System.out.print("Enter the year: ");
        int year = scanner.nextInt();

        displayCalendar(month, year);
    }

    public static void displayCalendar(int month, int year) {
        // Array to store days in each month (including leap years)
        int[] daysInMonth = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

        // Adjust for leap years
        if (isLeapYear(year)) {
            daysInMonth[2] = 29;
        }

        // Calculate the day of the week for the 1st of the month (0 = Sunday, 1 = Monday, etc.)
        int dayOfWeek = getDayOfWeek(1, month, year);

        // Print the calendar header
        System.out.println("\n      " + getMonthName(month) + " " + year);
        System.out.println("-----------------------------");
        System.out.println("Sun Mon Tue Wed Thu Fri Sat");

        // Print empty spaces before the first day of the month
        for (int i = 0; i < dayOfWeek; i++) {
            System.out.print("    ");
        }

        // Print the days of the month
        for (int i = 1; i <= daysInMonth[month]; i++) {
            System.out.printf("%3d ", i);
            if ((i + dayOfWeek) % 7 == 0) {
                System.out.println();
            }
        }

        System.out.println("\n");
    }

    // Function to check if a year is a leap year
    public static boolean isLeapYear(int year) {
        return ((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0);
    }

    // Function to calculate the day of the week (0 = Sunday, 1 = Monday, etc.)
    public static int getDayOfWeek(int day, int month, int year) {
        int y = year - (month < 3 ? 1 : 0);
        return ((day + ((13 * (month + (month < 3 ? 12 : 0)) - 1) / 5) + y + (y / 4) - (y / 100) + (y / 400)) % 7);
    }

    // Function to get the month name
    public static String getMonthName(int month) {
        String[] monthNames = {"", "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"};
        return monthNames[month];
    }
}
*/
/*
Scanner sc = new Scanner(System.in);


String str = new String();

str.nextLine(); 
//char c={  }


    }

}
*/

