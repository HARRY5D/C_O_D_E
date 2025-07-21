/*
  
 You will be given a zero-indexed array A. You need to rearrange its elements in such a way that the following conditions are satisfied:
A[i] ≤ A[i+1] if i is even.
A[i] ≥ A[i+1] if i is odd.
In other words, the following inequality should hold:
A [0] ≤ A [1] ≥ A [2] ≤ A [3] ≥ A [4], and so on.
Operations ≤ and ≥ should alter.
Input
The first line contains a single integer T denoting the number of test cases.
The first line of each test case contains an integer N, that is the size of the array A.
The second line of each test case contains the elements of array A.
output : 
For each test case, output a single line containing N space separated integers, which are the elements of A arranged in the required order. If there are more than one valid arrangements, you can output any of them.
Example:
2
2
3 2
3
10 5 2
Output:
2 3
2 10 5

 */
/*
import java.util.*;

public class dsa2_3 

{

 public static void main(String[] args) 
 
 {
 
    Scanner sc = new Scanner(System.in);
    
    System.out.println("ENTER NO OF TEST CASES :  ");

    int t = sc.nextInt();
    System.out.println("ENTER NO OF ELEMENTS :  ");

    int s = sc.nextInt();

    int [][]x = new int[t][s]; 

    for (int i = 0; i < s; i++) 
    {
        
    if (exp instanceof Object) {
        Object obj = (Object)exp;
        
    }[i]x=sc.nextInt();
    }

}   


}
*/
//even = smaall and vice versa

import java.util.Arrays;
import java.util.Scanner;

public class dsa2_3 
{
    public static void main(String[] args)
     {
        
        System.out.println("ENTER No. OF TEST CASES : ");

        Scanner sc = new Scanner(System.in);
        int t = sc.nextInt();
        while (t-- > 0) 
        {
            System.out.print("ENTER TOTAL No. OF ELEMENTS : ");
            int n = sc.nextInt();

            int[] arr = new int[n];
            for (int i = 0; i < n; i++) 
            {
                System.out.print("ENTER ELEMENT No. "+ (i+1) +" : ");
                arr[i] = sc.nextInt();
            }
            sc.close();
            rearrangeArray(n, arr);
            for (int i = 0; i < n; i++) 
            {
                
                System.out.print(arr[i] + " ");
            }
            System.out.println();
        }
    }

    public static void rearrangeArray(int n, int[] arr) 
    {
        Arrays.sort(arr);
        int[] result = new int[n];
        int small = 0, large = n - 1;
        for (int i = 0; i < n; i++) 
        {
            if (i % 2 == 0) 
            {
                result[i] = arr[small];
                small++;
            } 
            else if(i%2 !=0 )
            {
                result[i] = arr[large];
                large--;
            }
        }
        System.arraycopy(result, 0, arr, 0, n);
    }
}
