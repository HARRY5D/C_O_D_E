import java.util.Scanner;

public class Node {
    int data;
    Node next;

    Node(int data) {
        this.data = data;
        this.next = null;
    }
}

class List 

{
    Node head;

    public List() {
        head = null;
    }

    // (a) Insert a node at front
    public void insertAtFront(int data) {
        Node newNode = new Node(data);
        newNode.next = head;
        head = newNode;
        System.out.println("NODE INSERTED AT FRONT: " + data);
        display();
    }

    // (b) Delete a node at last
    public void deleteLast() {
        if (head == null) {
            System.out.println("LINKED LIST IS EMPTY. CANNOT DELETE.");
            return;
        }
        if (head.next == null) {
            System.out.println("NODE DELETED: " + head.data);
            head = null;
            display();
            return;
        }

        Node current = head;
        while (current.next.next != null) {
            current = current.next;
        }

        System.out.println("NODE DELETED: " + current.next.data);
        current.next = null;
        display();
    }

    // (c) Delete Nth Node from End of List
    public void deleteNthFromEnd(int n) {
        if (head == null) {
            System.out.println("LINKED LIST IS EMPTY. CANNOT DELETE.");
            return;
        }

        if (n <= 0) {
            System.out.println("INVALID NTH VALUE. PLEASE ENTER A POSITIVE NUMBER.");
            return;
        }

        Node fast = head;
        Node slow = head;

        // Move fast pointer n nodes ahead
        for (int i = 0; i < n; i++) {
            if (fast == null) {
                System.out.println("NTH NODE DOES NOT EXIST. INVALID NTH VALUE.");
                return;
            }
            fast = fast.next;
        }

        // Now move both pointers until fast reaches the end
        if (fast == null) {
            System.out.println("NODE DELETED: " + slow.data);
            head = head.next;
            display();
            return;
        }

        while (fast.next != null) {
            fast = fast.next;
            slow = slow.next;
        }

        // slow pointer now points to the node before the Nth node from the end
        if (slow.next != null) {
            System.out.println("NODE DELETED: " + slow.next.data);
            slow.next = slow.next.next;
        }
        display();
    }

    // (d) Delete all nodes of linked list
    public void deleteAll() {
        if (head == null) {
            System.out.println("LINKED LIST IS ALREADY EMPTY.");
            return;
        }
        while (head != null) {
            Node temp = head;
            head = head.next;
            temp = null; // Release the reference to the deleted node
        }
        System.out.println("ALL NODES DELETED.");
        display(); // Display an empty list
    }

    public void display() {
        if (head== null) {
            System.out.println("LINKED LIST IS EMPTY.");
            return;
        }
        Node current = head;
        System.out.print("LINKED LIST: ");
        while (current!= null) {
            System.out.print(current.data + " ");
            current = current.next;
        }
        System.out.println();
    }
}

    public static void main(String[] args) 
    {
        Scanner scanner = new Scanner(System.in);
        List list = new List(); // Create an instance of the List class

        while (true) {
            System.out.println("ENTER 1 TO INSERT A NODE AT FRONT.");
            System.out.println("ENTER 2 TO DELETE A NODE AT LAST.");
            System.out.println("ENTER 3 TO DELETE NTH NODE FROM END OF LIST.");
            System.out.println("ENTER 4 TO DELETE ALL NODES.");
            System.out.println("ENTER 5 TO EXIT.");
            System.out.print("ENTER YOUR CHOICE: ");
            int choice = scanner.nextInt();
            scanner.nextLine(); // Consume the leftover newline character

            if (choice == 1) {
                System.out.print("ENTER DATA FOR NEW NODE: ");
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
