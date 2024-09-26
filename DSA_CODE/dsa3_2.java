/*
 * (a) Reverse Linked List
Given the head of a singly linked list, reverse the list, and return the reversed list.
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]
 */

// Definition for singly-linked list.
/*
 This code snippet is responsible for creating a linked list from user input. It takes the number of elements (n) from the user and then prompts them to enter each element's value. Here's a detailed explanation:

1. for (int i = 0; i < n; i++):

This is a for loop that iterates n times, where n is the number of elements the user wants to enter.
int i = 0: The loop counter i is initialized to 0.
i < n: The loop continues as long as i is less than n.
i++: After each iteration, the value of i is incremented by 1.
2. System.out.print("ENTER ELEMENT" + (i + 1) + ": ");:

This line prints a message to the console, prompting the user to enter the next element.
It uses (i + 1) to display the element number (e.g., "ENTER ELEMENT 1:", "ENTER ELEMENT 2:", etc.) in a user-friendly way.
3. int val = sc.nextInt();:

This line reads an integer value from the user using the Scanner object sc.
The input value is stored in the variable val.
4. dsa3_2 node = new dsa3_2(val);:

This line creates a new node of the dsa3_2 class.
The new dsa3_2(val) constructor initializes the node with the value read from the user (val).
5. if (head == null):

This if statement checks if the head of the linked list is null. If it is, it means the list is currently empty.

head = node;: If the list is empty, the new node is assigned as the head of the list.

tail = node;: Since the list is empty, the new node is also the tail of the list.

6. else:

This else block is executed if the linked list is not empty (i.e., head is not null).

tail.next = node;: This line links the new node to the end of the existing list. It sets the next pointer of the current tail node to the newly created node.

tail = node;: The tail pointer is updated to point to the newly added node, making it the new tail of the list.

In Summary:

This for loop iterates through the number of elements specified by the user, reading each element value from the console, creating a new node with that value, and then adding that node to the end of the linked list. It handles both the case of creating a new linked list (when head is null) and the case of appending to an existing list.

 */

import java.util.Scanner;

class set 
{
    public dsa3_2 reverseList(dsa3_2 head)
    {
        dsa3_2 prev = null;
        dsa3_2 curr = head;
        while (curr != null) 
        {
            dsa3_2 nextTemp = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nextTemp;
        }
        return prev;
    }
}

public class dsa3_2 
{
    int val;
    dsa3_2 next;
    

    dsa3_2(int val) { this.val = val; }

    dsa3_2(int val, dsa3_2 next)

    { 
        this.val = val; 
        this.next = next; 
    }

    public static void main(String[] args) 
    {
        set s = new set();
        Scanner sc = new Scanner(System.in);

        System.out.print("ENTER TOTAL No. OF ELEMENTS : ");
        int n = sc.nextInt();

        dsa3_2 head = null;
        dsa3_2 tail = null;

        for (int i = 0; i < n; i++) 
        {
            System.out.print("ENTER ELEMENT No. " + (i + 1) + " : ");
            int val = sc.nextInt();

            dsa3_2 node = new dsa3_2(val);

            if (head == null) 
            {
                head = node;
                tail = node;
            }
            else
            {
                tail.next = node;
                tail = node;
            }
        }

        dsa3_2 rev = s.reverseList(head);

        System.out.print("REVERSED LINKED LIST : ");
        
        while (rev != null) 
        {
            System.out.print(rev.val + " ");
            rev = rev.next;
        }
        sc.close();
    }
}


