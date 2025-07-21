

/*
import java.util.Scanner;


class list {
    int data;
    list next;

    list(int data) {
        this.data = data;
        this.next = null;
    }
}

class List {
    list head;

    public List() {
        head = null;
    }

    // (a) Insert a list at front
    public void insertAtFront(int data) {
        list newlist = new list(data);
        newlist.next = head;
        head = newlist;
        System.out.println("list INSERTED AT FRONT: " + data);
        display();
    }

    // (b) Delete a list at last
    public void deleteLast() {
        if (head == null) {
            System.out.println("LINKED LIST IS EMPTY. CANNOT DELETE.");
            return;
        }
        if (head.next == null) {
            System.out.println("list DELETED: " + head.data);
            head = null;
            display();
            return;
        }

        list current = head;
        while (current.next.next != null) {
            current = current.next;
        }

        System.out.println("list DELETED: " + current.next.data);
        current.next = null;
        display();
    }

    // (c) Delete Nth list from End of List
    public void deleteNthFromEnd(int n) {
        if (head == null) {
            System.out.println("LINKED LIST IS EMPTY. CANNOT DELETE.");
            return;
        }

        if (n <= 0) {
            System.out.println("INVALID NTH VALUE. PLEASE ENTER A POSITIVE NUMBER.");
            return;
        }

        list fast = head;
        list slow = head;

        // Move fast pointer n lists ahead
        for (int i = 0; i < n; i++) {
            if (fast == null) {
                System.out.println("NTH list DOES NOT EXIST. INVALID NTH VALUE.");
                return;
            }
            fast = fast.next;
        }

        // Now move both pointers until fast reaches the end
        while (fast != null) {
            fast = fast.next;
            slow = slow.next;
        }

        // slow pointer now points to the list before the Nth list from the end
        if (slow.next != null) { 
            System.out.println("list DELETED: " + slow.next.data);
            slow.next = slow.next.next;
        } else {
            System.out.println("list DELETED: " + slow.data);
            slow = null; // If slow is the last list, set it to null
        }
        display();
    }

    // (d) Delete all lists of linked list
    public void deleteAll() {
        if (head == null) {
            System.out.println("LINKED LIST IS ALREADY EMPTY.");
            return;
        }
        while (head != null) {
            list temp = head;
            head = head.next;
            temp = null; // Release the reference to the deleted list
        }
        System.out.println("ALL listS DELETED.");
        display(); // Display an empty list
    }

    public void display() {
        if (head == null) {
            System.out.println("LINKED LIST IS EMPTY.");
            return;
        }
        list current = head;
        System.out.print("LINKED LIST: ");
        while (current != null) {
            System.out.print(current.data + " ");
            current = current.next;
        }
        System.out.println();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        List list = new List(); // Create an instance of the List class

        while (true) {
            System.out.println("ENTER 1 TO INSERT A list AT FRONT.");
            System.out.println("ENTER 2 TO DELETE A list AT LAST.");
            System.out.println("ENTER 3 TO DELETE NTH list FROM END OF LIST.");
            System.out.println("ENTER 4 TO DELETE ALL listS.");
            System.out.println("ENTER 5 TO EXIT.");
            System.out.print("ENTER YOUR CHOICE: ");
            int choice = scanner.nextInt();
            scanner.nextLine(); // Consume the leftover newline character

            if (choice == 1) {
                System.out.print("ENTER DATA FOR NEW list: ");
                int data = scanner.nextInt();
                list.insertAtFront(data);
            } else if (choice == 2) {
                list.deleteLast();
            } else if (choice == 3) {
                System.out.print("ENTER NTH VALUE: ");
                int n = scanner.nextInt();
                list.deleteNthFromEnd(n);
            } else if (choice == 4) {
                list.deleteAll();
            } else if (choice == 5) {
                System.out.println("EXITING.");
                break;
            } else {
                System.out.println("INVALID CHOICE. PLEASE ENTER A NUMBER BETWEEN 1 AND 5.");
            }
        }
        scanner.close();
    }
}

*/
/* 
import java.util.Scanner;
/*
class list 
{
    int data;
    list next;
    list(int data)
     {
        this.data = data;
        this.next = null;
    }
//}

class list
 {
    int data;
    list next;

    list (int data)
     {
        this.data = data;
        this.next = null;
    }
   // list head;
        list head;
    // Method to insert a list at the front
    public void insertAtFront(int data) {
        list newlist = new list(data);
        newlist.next = head;
        head = newlist;
        display();
    }

    // Method to delete the last list
    public void deleteLast() {
        if (head == null) {
            System.out.println("List is empty");
            return;
        }
        if (head.next == null) {
            head = null;
        } else {
            list temp = head;
            while (temp.next.next != null) {
                temp = temp.next;
            }
            temp.next = null;
        }
        display();
    }

    // Method to delete the Nth list from the end
    public void deleteNthFromEnd(int n) {
        list dummy = new list(0);
        dummy.next = head;
        list first = dummy;
        list second = dummy;
        
        for (int i = 0; i <= n; i++) {
            if (first == null) {
                System.out.println("N is larger than the length of the list");
                return;
            }
            first = first.next;
        }
        while (first != null) {
            first = first.next;
            second = second.next;
        }
        second.next = second.next.next;
        head = dummy.next;
        display();
    }

    // Method to delete all lists
    public void deleteAll() {
        head = null;
        display();
    }

    // Method to display the content of the linked list
    public void display() {
        if (head == null) {
            System.out.println("List is empty");
            return;
        }
        list temp = head;
        while (temp != null) {
            System.out.print(temp.data + " ");
            temp = temp.next;
        }
        System.out.println();
    }

    public static void main(String[] args) {
        list l = new list();
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("Choose an operation: ");
            System.out.println("1. Insert a list at front");
            System.out.println("2. Delete a list at last");
            System.out.println("3. Delete Nth list from End of List");
            System.out.println("4. Delete all lists");
            System.out.println("5. Exit");

            int choice = scanner.nextInt();

            switch (choice) {
                case 1 -> {
                    System.out.println("Enter data to insert at front: ");
                    int data = scanner.nextInt();
                    l.insertAtFront(data);
                }
                case 2 -> l.deleteLast();
                case 3 -> {
                    System.out.println("Enter N to delete Nth list from end: ");
                    int n = scanner.nextInt();
                    l.deleteNthFromEnd(n);
                }
                case 4 -> l.deleteAll();
                case 5 -> {
                    scanner.close();
                    return;
                }
                default -> System.out.println("Invalid choice! Please try again.");
            }
        }
    }
}
*/

import java.util.Scanner;

class Node 
{
    int data;
    Node next;

    Node(int data) 
    {
        this.data = data;
        this.next = null;
    }
}

class list 
{
    Node head;

    public void insertAtFront(int data) 
    {
        Node newNode = new Node(data);
        newNode.next = head;
        head = newNode;
        display();
    }

    public void deleteLast() 
    {
        if (head == null) 
        {
            System.out.println("THE LIST IS EMPTY.");
            return;
        }
        if (head.next == null) 
        {
            head = null;
        } else {
            Node temp = head;
            while (temp.next.next != null) 
            {
                temp = temp.next;
            }
            temp.next = null;
        }
        display();
    }

    public void deleteNthFromEnd(int n) 
    {
        Node dummy = new Node(0);
        dummy.next = head;
        Node first = dummy;
        Node second = dummy;

        for (int i = 0; i <= n; i++) 
        {
            if (first == null) 
            {
                System.out.println("N IS LARGER THAN LIST'S LENGTH.");
                return;
            }
            first = first.next;
        }

        while (first != null) 
        {
            first = first.next;
            second = second.next;
        }

        second.next = second.next.next;
        head = dummy.next;
        display();
    }


    public void deleteAll() 
    {
        head = null;
        display();
    }

    public void display() 
    {
        if (head == null) 
        {
            System.out.println("NO ELEMENTS PRESENT.");
            return;
        }
        Node temp = head;
        while (temp != null) 
        {
            System.out.print(temp.data + " ");
            temp = temp.next;
        }
        System.out.println();
    }

    public static void main(String[] args) 
    {
        list l = new list();
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("CHOOSE FROM BELOW : ");
            System.out.println("1. INSERT A NODE AT FRONT.");
            System.out.println("2. DELETE A NODE FROM LAST.");
           // System.out.println("3. DELETE N'th NODE FROM END.");
            System.out.println("3. DELETE ALL THE NODES.");
            System.out.println("4. EXIT.");

            int choice = scanner.nextInt();

            switch (choice) 
            {
                case 1 -> {
                    System.out.println("ENTER DATA TO INSERT AT FRONT : ");
                    int data = scanner.nextInt();
                    l.insertAtFront(data);
                }
                case 2 -> l.deleteLast();
                /*
                case 3 -> {
                    System.out.println("ENTER N TO DELETE NODE FROM END(N=1,2..) : ");
                    int n = scanner.nextInt();
                    l.deleteNthFromEnd(n);
                }

                */
                case 3 -> l.deleteAll();
                case 4 -> {
                    scanner.close();
                    return;
                }
                default -> System.out.println("INVALID INPUT.");
            }
        }
    }
}
