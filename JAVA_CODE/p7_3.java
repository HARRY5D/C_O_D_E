/*Create a Java program that simulates a simple online bookstore. 
The program should allow the user to browse books, add books to their cart, 
and checkout. We'll use HashMaps to store the items and implement methods for
browsing books, adding books to the cart, and checking out. This project will 
cover the concepts of HashMaps, loops, conditional statements, and methods in Java.
In the main method, create a HashMap of books, with each book mapped 
to a unique ID.
In another method, loop over the HashMap to print out the list of books.
Use the Scanner class to get user input to add a book to the cart.
Create an ArrayList to store the items in the cart.
Create a method for checking out and iterating over the cart item to 
calculate the total cost

 */

 import java.util.ArrayList;
 import java.util.HashMap;
 import java.util.Scanner;
 
 class p7_3 
 {
     private static HashMap<String, Integer> books = new HashMap<>();
     private static ArrayList<String> cart = new ArrayList<>();
 
     public static void main(String[] args) 
     {
        books.put("BOOK1", 1099);
        books.put("BOOK2", 1299);
        books.put("BOOK3", 999);
         Scanner scanner = new Scanner(System.in);
 
         while (true) 
         {
             displayMenu();
             
           System.out.println("ENTER YOUR CHOICE : ");
             int choice = scanner.nextInt();
 
             switch (choice) 
             {
                 case 1 -> browseBooks();
                 case 2 -> addBookToCart(scanner);
                 case 3 -> checkout();
                 case 4 -> System.exit(0);
                 default -> System.out.println("INVALID CHOICE. PLEASE TRY AGAIN.");
             }
         }
     }
 
     private static void displayMenu() 
    {
         System.out.println("WELCOME TO ONLINE BOOKSTORE:");
         System.out.println("1. BROWSE BOOKS");
         System.out.println("2. ADD BOOK TO CART");
         System.out.println("3. CHECKOUT");
         System.out.println("4. EXIT");
    }
 
     private static void browseBooks() 
    {
         System.out.println("AVAILABLE BOOKS:");
         
         
         for (String book : books.keySet()) 
        {
             System.out.println(book + " - " + books.get(book)+" Rs");
        }
    }
 
     private static void addBookToCart(Scanner scanner) 
    {
         System.out.print("ENTER BOOK ID TO ADD TO CART: ");
         String bookId = scanner.next();
         if (books.containsKey(bookId)) 
        {
             cart.add(bookId);
             System.out.println("BOOK ADDED TO CART SUCCESSFULLY!");
        } 
        else 
        {
             System.out.println("BOOK NOT FOUND.");
        }
    }
 
    private static void checkout() 
    {
         double totalCost = 0;
         System.out.println("YOUR CART:");
         for (String bookId : cart) 
         {
            System.out.println(bookId + " - " + books.get(bookId)+" Rs");
           totalCost += books.get(bookId);
         }
         System.out.println("TOTAL COST:" + totalCost+" Rs");
         System.out.println("THANK YOU FOR SHOPPING!");
     }
 }