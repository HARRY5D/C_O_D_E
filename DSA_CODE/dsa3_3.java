import java.util.Scanner;

class ListNode 
{
    int val;
    ListNode next;
    ListNode(int val) 
    { this.val = val; }
    ListNode(int val, ListNode next) 
    { this.val = val; 
        this.next = next; }
}

class MERGE 
{
    
    public ListNode merge(ListNode list1, ListNode list2) 
    {
        ListNode dummy = new ListNode(0);
        ListNode current = dummy;
        while (list1 != null && list2 != null) 
        {
            if (list1.val < list2.val) 
            {
                current.next = list1;
                list1 = list1.next;
            } 
            else 
            {
                current.next = list2;
                list2 = list2.next;
            }
            current = current.next;
        }
        if (list1 != null) 
        {
            current.next = list1;
        } 
        else 
        {  current.next = list2;  }
            return dummy.next;
    }
}

public class dsa3_3 
{
    public static void main(String[] args) 
    {
        Scanner sc = new Scanner(System.in);
        MERGE mg = new MERGE();

        System.out.print("ENTER TOTAL No. OF NODES FOR 1st LIST : ");
        int n1 = sc.nextInt();
        ListNode list1 = null;
        ListNode current1 = null;
        for (int i = 0; i < n1; i++) 
        {
            System.out.print("ENTER VALUE FOR NODE " + (i + 1) +" : ");
            int val = sc.nextInt();
            if (list1 == null) 
            {
                list1 = new ListNode(val);
                current1 = list1;
            } 
            else 
            {
                current1.next = new ListNode(val);
                current1 = current1.next;
            }
        }

        System.out.print("ENTER TOTAL No. OF NODES FOR 2nd LIST :  ");
        int n2 = sc.nextInt();
        ListNode list2 = null;
        ListNode current2 = null;
        for (int i = 0; i < n2; i++) 
        {
            System.out.print("ENTER VALUE FOR NODE " + (i + 1) +" : ");
            int val = sc.nextInt();
            if (list2 == null) 
            {
                list2 = new ListNode(val);
                current2 = list2;
            } 
            else 
            {
                current2.next = new ListNode(val);
                current2 = current2.next;
            }
        }

        ListNode MERGER = mg.merge(list1, list2);
        System.out.println("Merged list:");
        while (MERGER != null) 
        {
            System.out.print(MERGER.val + " ");
            MERGER = MERGER.next;
        }
    }
}