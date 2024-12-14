/*
Task Management System
Task Management System that allows users to add tasks, mark tasks as complete, and view
a list of pending tasks. Note: The system does not use a database and should store data in
memory.
1. Task Module
 Objective: To allow users to add new tasks with relevant details.
Functional Requirements:
1. Add Task:
- Input: Task Description, Due Date, and Priority Level (High, Medium, Low).
- Validation:
- Task Description should not be empty.
- Due Date should be in the future.
- Priority Level should be one of the predefined values (High, Medium, Low).
- Output: Confirmation message that the task has been added successfully.
2. View Tasks:
- Output: Display the list of all tasks with details (description, due date, priority, and status -
pending or completed).
3. Task Search:
- Input: Task Description or Due Date.
- Output: Display matching tasks with their details or a message if no task is found.
2. Task Status Module
 Objective: To manage the status of tasks and allow users to mark tasks as complete.
Functional Requirements:
4. Mark Task as Complete:
- Input: Task ID or Task Description.
- Validation: Ensure that the input refers to an existing task.
- Output: Update the task status to 'Completed' and provide a confirmation message.
5. View Pending Tasks:
- Output: Display a list of all tasks that are still pending, along with their details (description,
due date, and priority).

3. User Interface Module
 Objective: To create a simple, console-based interface for interaction.
Functional Requirements:
Main Menu:
- Options to navigate:
- Add Task
- Mark Task as Complete
- View All Tasks
- View Pending Tasks

Notes for Students:
 Use collections such as ArrayList, HashMap, or Set for storing and managing tasks.
 Divide the code into logical packages (e.g., task, status, main). Demonstrate clear
usage of import statements to manage inter-package dependencies.
 Proper use of try-catch blocks to handle input errors (e.g., incorrect date formats,
empty task descriptions, invalid options)
Evaluation Criteria
Use of Collections (20 Points)
 Excellent (16-20 Points): Uses appropriate collections (ArrayList, HashMap, Set)
effectively; demonstrates efficient data management and retrieval.
 Good (11-15 Points): Uses collections appropriately but with minor inefficiencies in
data handling.
 Fair (6-10 Points): Uses collections but lacks efficiency or makes inappropriate
choices for the given use cases.
 Needs Improvement (0-5 Points): Fails to use collections effectively or
demonstrates incorrect usage.
Exception Handling (10 Points)
 Excellent (8-10 Points): Implements try-catch blocks effectively for all input errors;
error messages are clear and user-friendly.
 Good (5-7 Points): Uses try-catch blocks appropriately with minor errors or unclear
messages.
 Fair (3-4 Points): Handles some errors using try-catch blocks but misses important
cases or provides vague messages.
 Needs Improvement (0-2 Points): Fails to implement exception handling correctly
or provides no meaningful error messages.
Package Organization (10 Points)

 Excellent (8-10 Points): Code is divided into well-defined packages; imports are
correctly used to manage dependencies.

 Good (5-7 Points): Code is organized into packages with minor issues in inter-
package dependencies.

 Fair (3-4 Points): Packages are used but lack logical organization or have
dependency issues.
 Needs Improvement (0-2 Points): Code lacks proper package organization and fails
to use imports effectively.  using arrays or hashmap


 */
//package task_manager;


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

 public class Main
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


