/*
Create a Java program that allows the user to manage their to-do list. The program will present 
the user with a menu of options to manage their to-do list, including adding new tasks, displaying a list of 
tasks, editing tasks, and deleting tasks from the list. We'll use an ArrayList for storing the tasks and implement methods for each
of the menu options to give functionality to the program.
 */

 import java.util.ArrayList;
 import java.util.Scanner;
 
 public class p7_1 
{
     public static ArrayList<String> todoList = new ArrayList<>();
     public static Scanner scanner = new Scanner(System.in);
 
     public static void main(String[] args) 
     {
        while (true) 
        {
             displayMenu();
             int choice = getChoice();
             performAction(choice);
        }
     }
 
     public static void displayMenu() 
     {
         System.out.println("TO-DO LIST MANAGER");
         System.out.println("1. ADD NEW TASK");
         System.out.println("2. DISPLAY TASKS");
         System.out.println("3. EDIT TASK");
         System.out.println("4. DELETE TASK");
         System.out.println("5. EXIT");
     }
 
     public static int getChoice() 
     {
         System.out.print("ENTER YOUR CHOICE: ");
         return scanner.nextInt();
     }
 
     public static void performAction(int choice) 
     {
         switch (choice) 
         {
             case 1 -> addTask();
             case 2 -> displayTasks();
             case 3 -> editTask();
             case 4 -> deleteTask();
             case 5 -> System.exit(0);
             default -> System.out.println("INVALID CHOICE. PLEASE TRY AGAIN.");
         }
     }
 
     public static void addTask() 
     {
         System.out.print("ENTER NEW TASK: ");
         String task = scanner.next();
         todoList.add(task);
         System.out.println("TASK ADDED SUCCESSFULLY!");
     }
 
     public static void displayTasks() 
     {
         System.out.println("TO-DO LIST:");
         for (int i = 0; i < todoList.size(); i++) 
         {
             System.out.println((i + 1) + ". " + todoList.get(i));
         }
     }
 
     public static void editTask() 
     {
         System.out.print("ENTER TASK NUMBER TO EDIT: ");
         int taskNumber = scanner.nextInt();
         if (taskNumber > 0 && taskNumber <= todoList.size()) 
         {
             System.out.print("ENTER NEW TASK: ");
             String newTask = scanner.next();
             todoList.set(taskNumber - 1, newTask);
             System.out.println("TASK EDITED SUCCESSFULLY!");
         } 
         else 
         {
             System.out.println("INVALID TASK NUMBER.");
         }
     }
 
     public static void deleteTask() 
     {
         System.out.print("ENTER TASK NUMBER TO DELETE: ");
         int taskNumber = scanner.nextInt();
         if (taskNumber > 0 && taskNumber <= todoList.size()) 
         {
             todoList.remove(taskNumber - 1);
             System.out.println("TASK DELETED SUCCESSFULLY!");
         } 
         else 
         {
             System.out.println("INVALID TASK NUMBER.");
         }
     }
 }