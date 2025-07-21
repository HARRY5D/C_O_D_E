
import java.util.*;

class Vehicle
{
   
    String type;
    int cost;
    String model;
    boolean available;
    int days;
    int id = 0;
   
    List<String> lt = new ArrayList<>();
    List<String> rented = new ArrayList<>();
   
    Vehicle(String type, String model, int cost, int days)
    {
        this.type = type;
        this.cost = cost;
        this.model = model;
        this.available = true;
        this.days = days;
    }

    public void rent(Scanner sc)
    {
        System.out.println("Enter details of vehicle:");
        System.out.print("Enter type of vehicle: ");
        type = sc.nextLine();
       
        System.out.print("Enter model of vehicle: ");
        model = sc.nextLine();
       
        rented.add(model);
       
        System.out.print("ENTER NO. OF DAYS TO RENT: ");
        days = sc.nextInt();
       
        System.out.print("Enter rent of vehicle: ");
        cost = sc.nextInt();
       
        System.out.println("TOTAL RENT: " + (cost * days));
        System.out.println("Details of vehicle added successfully");
    }
   
    public void dispAll()
    {
        for (String model : lt)
        {
            System.out.println("Model: " + model);
        }
    }

    public void disp(String model)
    {
        if (model.equals(this.model))
        {
            System.out.println("Details of vehicle:");
            System.out.println("Type: " + type + "\nModel: " + model + "\nRent: " + cost + "\nAvailable: " + available);
        }
    }

    public void update(String model, boolean available)
    {
        try{
        System.out.println("ENTER NEW MODEL: ");
        Scanner sc = new Scanner(System.in);
        model = sc.nextLine();
        lt.add(model);
        this.available = available;
        System.out.println("STATUS UPDATED");
        }catch(Exception e){e.getMessage();}
    }

    public void ret(String model)
    {
        System.out.println("ENTER VEHICLE MODEL: ");
        Scanner sc = new Scanner(System.in);
        String mod = sc.nextLine();

        if (mod.equals(this.model) && available)
        {
            System.out.println("VEHICLE RETURNED.");
            available = true;
        }
        else
        {

            System.out.println("NO SUCH MODEL");
        }
     }
   
}

  class Main
 {
   

    public static void main (String[] args)
    {  
        int choice;
        Scanner sc = new Scanner(System.in);
        Vehicle v= new Vehicle("", "", 0, 0);

        while (true) {
            System.out.println("ENTER YOUR CHOICE:");
            System.out.println("1. ADD VEHICLE");
            System.out.println("2. SHOW ALL AVAILABLE VEHICLES");
            System.out.println("3. RETURN A VEHICLE");
            System.out.println("4. UPDATE A VEHICLE STATUS");
            System.out.println("5. EXIT");

            choice = sc.nextInt();
            sc.nextLine();
            switch (choice)
            {
                case 1:
                    v.rent(sc);
                    break;
                case 2:
                    v.dispAll();
                    break;
                case 3:
                    v.ret(v.model);
                    break;
                case 4:
                    System.out.print("Enter model to update: ");
                    String modelToUpdate = sc.nextLine();
                    v.update(modelToUpdate, true);
                    break;
                case 5:
                    System.exit(0);
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }
}
