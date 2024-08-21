/*
Create program by writing two classes (Bottle and SodaBottle). Bottle class has one double type attribute: volume, which tells the
 volume of the bottle. This class also has one method: returnVolume, which returns the bottle volume. SodaBottle is derived from 
 Bottle class and it implements the Recyclable interface class. SodaBottle also includes the name of the soda as attribute.
 A toString method is needed in SodaBottle class. toString returns the name of the soda and the volume of the bottle. 
 Check example print for more precise printing needs. Recycle method should print the text “Bottle returned for recycling”. 
 Create object of SodaBottel Class only in main class.
  Expected output
Type in the name of the soda: 
Pepsi 
Type in the volume of the bottle: 1 Pepsi, 1.0 litres
Bottle returned for recycling.
 */

 /*
public class p3_3
{


    
}
interface Recyclable 
{
    default void recycle() 
    {
        System.out.println(this.toString() + "returned for recycling. ");
    }
}
class Bottle

{
    public double volume;
  
    public Bottle(double volume)
    {
    this.volume = volume;
    }
}

    /*
class Bottle implements Recyclable 
{
    @Override
    public String toString() 
    {
        return "BOTTLE";
    }
}
    
class SodaBottle extends Bottle implements Recyclable
{
    public  String name;
    public  double volume = 0;
    
    public SodaBottle(String name, double volume)
    {
        this.name = name;
        this.volume = volume;
    }

    
        @Override
        public String toString()
        {
            return name + ", " + volume + " litres";
        }
    
        @Override
        public void recycle()
        {
                System.out.println(this.toString() + " returned for recycling");
        }
}

*/
 
import java.util.Scanner;

interface Recyclable 
{
    void recycle();
}

class Bottle 
{
    protected double volume;

    public Bottle(double volume) 
    {
        this.volume = volume;
    }

    public double returnVolume() 
    {
        return volume;
    }
}

class SodaBottle extends Bottle implements Recyclable 
{
    private String name;


    public SodaBottle(String name, double volume)
    {
        super(volume);
        this.name = name;
    }

    @Override
    public void recycle() 
    {
        System.out.println("Bottle returned for recycling.");
    }

    @Override
    public String toString() 
    {
        return name + ", " + returnVolume() + " litres";
    }
}

public class p3_3 

{
    public static void main(String[] args) 
    {
        Scanner sc = new Scanner(System.in);

        System.out.print("Type in the name of the soda: ");
        String name = sc.nextLine();

        System.out.print("Type in the volume of the bottle: ");
        double volume = sc.nextDouble();

        SodaBottle sb = new SodaBottle(name, volume);

        System.out.println(sb.toString());
        sb.recycle();
    }
}