/*Create a Recyclable Interface with the default method with the message “Give proper
input”. Create three different classes (Fabric, Bottle & Paper), which implement a
Recyclable interface. Class requires toString methods which return the name of the recyclable materials. The toString method of the Fabric class returns the text “Febric” etc.
Expected output:
What do you want to recycle? Choose a number.
1 - Clothes
2 - Bottles
3 – Newspapers
4 – Exit
Choose a Number: 2 Fabric RECYCLED...
Chose a number: 5 Give proper input
Choose another number: 4 Thanks for coming...
 */


 
// Recyclable interface with default method

import java.util.*;

interface Recyclable 
{
    default void recycle() 
    {
        System.out.println(this.toString() + " RECYCLED...");
    }
}

// Fabric class implementing Recyclable interface
class Fabric implements Recyclable 
{
    @Override
    public String toString() 
    {
        return "FABRIC";
    }
}

// Bottle class implementing Recyclable interface
class Bottle implements Recyclable 
{
    @Override
    public String toString() 
    {
        return "BOTTLE";
    }
}

// Paper class implementing Recyclable interface
class Paper implements Recyclable 
{
    @Override
    public String toString() 
    {
        return "PAPER";
    }
}

public class p3_2 
{
    public static void main(String[] args) 
    {
        Scanner sc = new Scanner(System.in);

        while (true) 
        {
            System.out.println("WHAT DO YOU WANT TO RECYCLE? ");
            System.out.println("1 - CLOTHES");
            System.out.println("2 - BOTTLES");
            System.out.println("3 - NEWSPAPER");
            System.out.println("4 - EXIT");
            System.out.print("CHOOSE A No. : ");

            int x = sc.nextInt();
            sc.close();
            switch (x) 
            {
                case 1:
                    Fabric fabric = new Fabric();
                    fabric.recycle();
                    break;
                case 2:
                    Bottle Bottle = new Bottle();
                    Bottle.recycle();
                    break;
                case 3:
                    Paper paper = new Paper();
                    paper.recycle();
                    break;
                case 4:
                    System.out.println("THANKS FOR COMING...");
                    return;
                default:
                    System.out.println("GIVE PROPER INPUT.");
            }
        }
    }
}