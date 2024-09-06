

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

class LinkedList 
{
    Node head;

    public
     void insertAtFront(int data) 
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
        }
         else 
        {
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
                System.out.println("N IS LARGER THEN LIST'S LENGTH.");
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
        LinkedList l = new LinkedList();
        Scanner scanner = new Scanner(System.in);

        while (true) 
        {
            System.out.println("CHOOSE FROM BELOW : ");
            System.out.println("1. INSERT A NODE AT FRONT.");
            System.out.println("2. DELTE A NODE FROM LAST.");
            System.out.println("3. DELETE n'th NODE FROM END.");
            System.out.println("4. DELETE ALL THE NODES.");
            System.out.println("5. EXIT.");

            int choice = scanner.nextInt();

            switch (choice) 
            {
                case 1 -> {
                    System.out.println("ENTER DATA TO INSERT AT FRONT : ");
                    int data = scanner.nextInt();
                    l.insertAtFront(data);
                }
                case 2 -> l.deleteLast();

                case 3 -> {
                    System.out.println("ENTER N TO DELETE NODE FROM END(N=1,2..) : ");
                    int n = scanner.nextInt();
                    l.deleteNthFromEnd(n);
                }
                case 4 -> l.deleteAll();
                case 5 -> {
                    scanner.close();
                    return;
                }
                default -> System.out.println("INVALID INPUT.");
            }
        }
    }
}
//*/