    /*Create a Java program the object class Point. An instance of a Point class depicts a point in two dimensional area where the smallest and biggest values for axis x and y are zero and 100 respectively. Coordinate values are integers. Class needs declarations to two private int type instance variables, one for each axis. Name the variables as you see fit.
In addition to two instance variables, the class also requires a constructor and two instance methods according to the following descriptions.
Constructor has two parameters, one for each axis. Values of these parameters are assigned to be the values of corresponding instance variables. Constructor must make sure that the coordinate value stays inside valid scope. If the value is lower than zero, value is zero and similarly if the value is higher than 100, value is to be 100.

A toString() method is declared for the class. Method returns a character string where the coordinate values are enclosed with parenthesis separated with commas. ((e.g.) “(86,34)”). Value of the x coordinate is presented first.
Another method declared for the class is move Method receivestwo parameters which are used to change the coordinate value. Parameters present the difference in the original coordinate value, not the new value directly. Method must make sure that neither of the coordinate values are smaller than

zero nor higher than 100. If the change makes either of the values too low or too high, value is set to be zero or 100 respectively.Following are some examples of the method functionality:

if the old value of the coordinate is 12 and the difference is 34, new value is 46
if the old value of the coordinate is 53 and the difference is -60, new value is 0
if the old value of the coordinate is 63 and the difference is 82, new value is 100 Point class can be tested with PointTest class which has only the main method. */
    

    
    
    import java.util.Scanner;

class Point
 {
    private int x;
    private int y;

    public Point(int x, int y) 
    {
        this.x = Math.max(0, Math.min(x, 100)); 
        this.y = Math.max(0, Math.min(y, 100)); 
    }

  

    public String toString()
     {
        return "(" + x + "," + y + ")";
    }

    public void move(int xDiff, int yDiff) 
    {
        this.x = Math.max(0, Math.min(this.x + xDiff, 100));
        this.y = Math.max(0, Math.min(this.y + yDiff, 100));
    }
}

public class PointTest 
{
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("ENTER THE X-COORDINATE : ");
        int x = sc.nextInt();
        System.out.print("ENTER THE Y-COORDINATE :  ");
        int y = sc.nextInt();

        Point point = new Point(x, y);

        System.out.println("POINT : " + point);

        System.out.print("ENTER THE DIFFERNECE OF X-COORDINATE: ");
        int xDiff = sc.nextInt();
        System.out.print("ENTER THE DIFFERNECE OF Y-COORDINATE :  ");
        int yDiff = sc.nextInt();

        point.move(xDiff, yDiff);

        System.out.println("NEW POINT : " + point);
        sc.close();
    }
}
    



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



//jdk 7,12,14,16 ma switch case na syntax changes









/*

import java.util.Scanner;

class GasMeter
 {
    private double totalFuel;
    private double fuel95;
    private double fuel98;
    private double diesel;

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

    public static void printTotalFuel(GasMeter gasMeter) {
        System.out.println("TOTAL FUEL USED : " + gasMeter.totalFuel);
    }

    public static void printFuel95(GasMeter gasMeter) {
        System.out.println("TOTAL 95 OCTANE FUEL USED : " + gasMeter.fuel95);
    }

    public static void printFuel98(GasMeter gasMeter) {
        System.out.println("TOTAL 98 OCTANE FUEL USED : " + gasMeter.fuel98);
    }

    public static void printDiesel(GasMeter gasMeter) {
        System.out.println("TOTAL DIESAL FUEL USED : " + gasMeter.diesel);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        GasMeter gasMeter = new GasMeter();

        while (true) {
            System.out.print("ENTER YOUR CHOICE :  \n 1=95 \n2=98 \n3=DIESEL[TYPE ANY OTHER NO. TO QUIT ] ");
            int choice = scanner.nextInt();
            scanner.nextLine(); // Consume the leftover newline character

            if (choice < 1 || choice > 3) {
                break;
            }

            System.out.print("ENTER AMOUNT OF REFUEL : ");
            double amount = scanner.nextDouble();
            scanner.nextLine(); // Consume the leftover newline character

            switch (choice) {
                case 1:
                    gasMeter.refuel("95", amount);
                    break;
                case 2:
                    gasMeter.refuel("98", amount);
                    break;
                case 3:
                    gasMeter.refuel("DIESEL ", amount);
                    break;
            }
        }

        printTotalFuel(gasMeter);
        printFuel95(gasMeter);
        printFuel98(gasMeter);
        printDiesel(gasMeter);

        scanner.close();
    }
}
    */