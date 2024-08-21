/*
    Create GasMeter class that keeps track of amount of refuelled gas. Class needs an instance method that receives the refuelled substance as 
    parameter and the refuelled amount in litres. Class also needs four class methods which can print how much each substance has been used and 
    the total amount of refuelled gas. 
Example output: 
what do you want: 1=95, 2=98, 3=Diesel (type any other number to quit): 1 How much do you want to refuel: 6,5 
what do you want: 1=95, 2=98, 3=Diesel (type any other number to quit): 2 How much do you want to refuel: 5,5 
what do you want: 1=95, 2=98, 3=Diesel (type any other number to quit): 0 Total used fuel: 12.0 
Total used 95 octane fuel: 6.5 
Total used 98 octane fuel: 5.5 Total used diesel fuel: 0.0 */


/*
import java.util.Scanner;

class GasMeter
 {
    public 

     float  totalFuel;
     double fuel95;
     double fuel98;
     double diesel;

    public GasMeter() 
    {
        totalFuel = 0;
        fuel95 = 0;
        fuel98 = 0;
        diesel = 0;
    }

    public void refuel(String substance, double amount) 
    {
        totalFuel += amount;
     
        switch (substance.toLowerCase()) 

        {
            case "95":
                fuel95 += amount;
                break;
            case "98":
                fuel98 += amount;
                break;
            case "diesel":
                diesel += amount;
                break;
        }
    }

    public static void printTotalFuel(GasMeter p4) 
    {
        System.out.println("TOTAL FUEL USED :  "+p4.totalFuel+" LITRES"  );
    }

    public static void printFuel95(GasMeter p4) 
    {
        System.out.println("TOTAL 95 OCTANE FUEL USED : " + p4.fuel95+" LITRES");
    }

    public static void printFuel98(GasMeter p4) 
    {
        System.out.println("TOTAL 98 OCTANE FUEL USED : " + p4.fuel98+" LITRES");
    }

    public static void printDiesel(GasMeter p4) 
    {
        System.out.println("TOTAL DIESEL FUEL USED : " + p4.diesel+" LITRES");
    }

    public static void main(String[] args) 
    {
        Scanner sc = new Scanner(System.in);
        GasMeter Gas = new GasMeter();

        while (true)
        {
            System.out.print("WHAT DO YOU WANT : \n 1. FUEL 95 \n 2.FUEL 98 \n 3. DIESEL[TYPE ANY OTHER NO. TO QUIT ] \n");
            int choice = sc.nextInt();
            sc.nextLine(); 

            if (choice < 1 || choice > 3)
            {
                break;
            }

            System.out.print("ENTER AMOUNT OF REFUEL : ");
            double amount = sc.nextDouble();
            sc.nextLine(); 
            
            switch (choice) 
            {
                case 1:
                    Gas.refuel("95", amount);
                    break;
                case 2:
                    Gas.refuel("98", amount);
                    break;
                case 3:
                    Gas.refuel("DIESEL", amount);
                    break;
            }
        }

        printTotalFuel(Gas);
        printFuel95(Gas);
        printFuel98(Gas);
        printDiesel(Gas);

        sc.close();
    }
}
*/
import java.util.Scanner;

class GasMeter {
    public double totalFuel;
    public double fuel95;
    public double fuel98;
    public double diesel;

    public GasMeter() {
        totalFuel = 0;
        fuel95 = 0;
        fuel98 = 0;
        diesel = 0;
    }

    public void refuel(String substance, double amount) {
        totalFuel += amount;

        switch (substance.toLowerCase()) {
            case "95":
                fuel95 += amount;
                break;
            case "98":
                fuel98 += amount;
                break;
            case "diesel":
                diesel += amount;
                break;
        }
    }

    public static void printTotalFuel(GasMeter p4) {
        System.out.println("TOTAL FUEL USED :  " + p4.totalFuel + " LITRES");
    }

    public static void printFuel95(GasMeter p4) {
        System.out.println("TOTAL 95 OCTANE FUEL USED : " + p4.fuel95 + " LITRES");
    }

    public static void printFuel98(GasMeter p4) {
        System.out.println("TOTAL 98 OCTANE FUEL USED : " + p4.fuel98 + " LITRES");
    }

    public static void printDiesel(GasMeter p4) {
        System.out.println("TOTAL DIESEL FUEL USED : " + p4.diesel + " LITRES");
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        GasMeter Gas = new GasMeter();

        while (true) {
            System.out.print("WHAT DO YOU WANT : \n 1. FUEL 95 \n 2.FUEL 98 \n 3. DIESEL[TYPE ANY OTHER NO. TO QUIT ] \n");
            int choice = sc.nextInt();
            sc.nextLine();

            if (choice < 1 || choice > 3) {
                break;
            }

            System.out.print("ENTER AMOUNT OF REFUEL : ");
            double amount = sc.nextDouble();
            sc.nextLine();

            switch (choice) {
                case 1:
                    Gas.refuel("95", amount);
                    break;
                case 2:
                    Gas.refuel("98", amount);
                    break;
                case 3:
                    Gas.refuel("diesel", amount); // Changed "DIESEL" to "diesel"
                    break;
            }
        }

        printTotalFuel(Gas);
        printFuel95(Gas);
        printFuel98(Gas);
        printDiesel(Gas);

        sc.close();
    }
}