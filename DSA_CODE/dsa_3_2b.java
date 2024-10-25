
import java.util.Scanner;
class ListNode 
{
    int val;
    ListNode next;

    ListNode(int x) 
    {
        val = x;
    }
}

class set 
{
    public ListNode endOfFirstHalf(ListNode head) 
    {
        ListNode start = head, end = head;
        while (end.next != null && end.next.next != null) 
        {
            start = start.next;
            end = end.next.next;
        }
        return start;
    }

    public ListNode reverseList(ListNode head) 
    {
        ListNode prev = null, curr = head;
        while (curr != null) 
        {
            ListNode next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }
        return prev;
    }

    public boolean isPalindrome(ListNode head) 
    {
        if (head == null) return true;
        
        ListNode firstHalfEnd = endOfFirstHalf(head);
        ListNode secondHalfStart = reverseList(firstHalfEnd.next);

        ListNode firstPosition = head;
        ListNode secondPosition = secondHalfStart;

        while (secondPosition != null) 
        {
            if (firstPosition.val != secondPosition.val) return false;
           
            firstPosition = firstPosition.next;
            secondPosition = secondPosition.next;
        }

        firstHalfEnd.next = reverseList(secondHalfStart);
        return true;
    }
}

public class dsa_3_2b 
{
    public static void main(String[] args) 
    {
        Scanner sc = new Scanner(System.in);
        System.out.println("ENTER TOTAL No. OF NODES IN LINKED LIST :");
        int n = sc.nextInt();
        ListNode head = null;
        ListNode current = null;
        for (int i = 0; i < n; i++) 
        {
            System.out.print("ENTER VALUE OF NODE " + (i + 1) + " : ");
            int val = sc.nextInt();
            if (head == null) 
            {
                head = new ListNode(val);
                current = head;
            } 
            else 
            {
                current.next = new ListNode(val);
                current = current.next;
            }
        }
        sc.close();
        
        set s = new set();

        boolean isPalindrome = s.isPalindrome(head);
    
        
         System.out.println(isPalindrome);
    }
}