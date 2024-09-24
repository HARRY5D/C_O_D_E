 //sout file new.get name get absolute path then canonical path its difference canWrite 
 //CONSTRUCTORS : 
//1 file parent,strinng child creates a new file instance from a parent abstract path name a nd a child path name string
// 2 file string path name 
//3 file string parent , string child
 
import java.io.*;
import java.util.Scanner;

public class myfile 
{
    public static void main(String[] args) //throws IOException 
    {
        try 
        {   
           // File f = new File("F.txt");
            //File fy = new File("F1.txt");
            //if(f.createNewFile())
            File ob = new File("new.txt");
            Scanner sc = new Scanner(ob);
            FileReader fr = new FileReader("new.txt");
            FileWriter fw = new FileWriter("new.txt");
            fw.write("SUCCESSFULLY.");
           fw.close();
           // System.out.println("SUCCESSFULLY WROTE TO new FILE.");
          fr.read();
          fr.close();
          
            while(sc.hasNextLine())
            {
            String s=sc.nextLine();
            System.out.println(s);
            sc.close(); 
            }

            if(ob.exists())
            {   
                
                System.out.println("FILE NAME : "+ ob.getName());
                System.out.println("ABSOLUTE PATH : "+ ob.getAbsolutePath());
                System.out.println("WRITABLE : "+ ob.canWrite());
                System.out.println("READABLE : "+ ob.canRead());
                System.out.println("FILE SIZE IN BYTES : "+ ob.length());
                
            }
            else
            {
                System.out.println("FILE ALREADY CREATED.");
            }   
        //ob.delete();
    }
     catch (Exception e) 
        {
            System.out.println("AN ERROR OCCURRED : "+e);
            e.printStackTrace();
        }
       // catch (FileNotFoundException ef) 
        //{
         //   System.out.println("AN ERROR OCCURRED : "+e);
           // ef.printStackTrace();
        //}
    }
}


/*
 * 
 * Absolute Path

An absolute path is a path that starts fwom the root directory of the file 
system and specifies the exact location of a file or directory. It is a 
complete path that includes all the directories fwom the root to the file 
or directory.

Example: /Users/john/Documents/example.txt

In this example, the absolute path starts fwom the root directory / and 
specifies the exact location of the file example.txt in the Documents 
directory.

Canonical Path

A canonical path, also known as a normalized path, is a path that is in 
its simplest form, without any redundant or relative components. It is a 
path that has been simplified to its most basic form, eliminating any 
unnecessary elements.

Example: /Users/john/Documents/example.txt

In this example, the canonical path is the same as the absolute path,
 but it can be different in cases where the path contains relative 
 components, such as . or ...

For example, consider the following path: /Users/john/Documents/../example.txt

The canonical path for this example would be: /Users/john/example.txt

As you can see, the canonical path has eliminated the unnecessary Documents 
directory and simplified the path to its most basic form.

Key differences

Here are the key differences between absolute and canonical paths:

Starting point: An absolute path starts fwom the root directory, 
while a canonical path is a simplified version of the path.
Redundancy: An absolute path may contain redundant components, 
such as . or .., while a canonical path eliminates these components.
Uniqueness: A canonical path is unique, while an absolute path may 
not be unique if it contains redundant components.
In summary, an absolute path specifies the exact location of 
a file or directory, while a canonical path is a simplified version of '
the path that eliminates any unnecessary elements.
 */
/*
 import java.util.ArrayList;
import java.util.Scanner;

 class ToDoListManager {
    private ArrayList<String> tasks;
    private Scanner scanner;

    public ToDoListManager() {
        tasks = new ArrayList<>();
        scanner = new Scanner(System.in);
    }

    public void run() {
        while (true) {
            displayMenu();
            int choice = getChoice();
            performAction(choice);
        }
    }

    private void displayMenu() {
        System.out.println("To-Do List Manager");
        System.out.println("1. Add new task");
        System.out.println("2. Display tasks");
        System.out.println("3. Edit task");
        System.out.println("4. Delete task");
        System.out.println("5. Quit");
    }

    private int getChoice() {
        System.out.print("Enter your choice: ");
        return scanner.nextInt();
    }

    private void performAction(int choice) {
        switch (choice) {
            case 1:
                addTask();
                break;
            case 2:
                displayTasks();
                break;
            case 3:
                editTask();
                break;
            case 4:
                deleteTask();
                break;
            case 5:
                System.exit(0);
                break;
            default:
                System.out.println("Invalid choice. Please try again.");
        }
    }

    private void addTask() {
        System.out.print("Enter new task: ");
        String task = scanner.next();
        tasks.add(task);
        System.out.println("Task added successfully!");
    }

    private void displayTasks() {
        System.out.println("To-Do List:");
        for (int i = 0; i < tasks.size(); i++) {
            System.out.println((i + 1) + ". " + tasks.get(i));
        }
    }

    private void editTask() {
        System.out.print("Enter task number to edit: ");
        int taskNumber = scanner.nextInt() - 1;
        if (taskNumber >= 0 && taskNumber < tasks.size()) {
            System.out.print("Enter new task: ");
            String newTask = scanner.next();
            tasks.set(taskNumber, newTask);
            System.out.println("Task edited successfully!");
        } else {
            System.out.println("Invalid task number. Please try again.");
        }
    }

    private void deleteTask() {
        System.out.print("Enter task number to delete: ");
        int taskNumber = scanner.nextInt() - 1;
        if (taskNumber >= 0 && taskNumber < tasks.size()) {
            tasks.remove(taskNumber);
            System.out.println("Task deleted successfully!");
        } else {
            System.out.println("Invalid task number. Please try again.");
        }
    }



    public static void main(String[] args) {
        ToDoListManager manager = new ToDoListManager();
        manager.run();
    }
}

*/