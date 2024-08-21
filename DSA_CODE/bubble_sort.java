/*
Implement Sorting Algorithm(s).
A. Bubble Sort
 B. Selection Sort
C. Insertion Sort* 
 
 */


/*
import iava.lang.reflect.Array;
 import iava.util.Scanner;
import iava.util.Arrays;

public class bubble_sort

{
       public static void main(String[] args) 
       {
        Scanner sc=new Scanner(System.in);
        System.out.print("ENTER NO OF ELEMENTS TO ENTER : ");
        int l=sc.nextInt();
        System.out.println("ENTER ELEMENTS : ");
        int [] ar=new int[l];
        for (int i=0;i<l;i++)
        {
        ar[i]=sc.nextInt();    
        }
        for (int i=0;i<l;i++)
        {   
            for (int j=0;j<1;j++)
            {
        
                 if(ar[j]>ar[j+1])
                 {
                    int temp=ar[j];
                    ar[j]=ar[j+1];
                    ar[j+1]=temp;         
                 }
            }  
        }
         System.out.println("BUBBLE SORTED ARRAY :");
         System.out.print("[");  
      //   for (int i=0;i<l;i++)
        // {
          // System.out.print(" "+ar[i]) ;
        //}
        Arrays.sort(ar);
        System.out.print("]");    
        System.out.println(" "+Array.toString() );
    }
}

*/

//2.2
/*Sort an array in linear time if all of its items are in ascending order except for two swapped elements.
Example:
Input: A [] = [3, 8, 6, 7, 5, 9] or [3, 5, 6, 9, 8, 7] or [3, 5, 7, 6, 8, 9]
Output: A [] = [3, 5, 6, 7, 8, 9]
Note: You must solve this problem without using the library's sort function.
Glossary:
Linear Time definition: The time complexity, denoted O(n), of an algorithm whose running time increases at most 
linearly with the size of the input. i.e. do not use nested loops.


*/
//2.1 B
/*
import java.util.Arrays;
import java.util.Scanner;

public class bubble_sort
 {
    public static void main(String[] args)
     {
        
        Scanner sc=new Scanner(System.in);
      
        System.out.print("ENTER NO OF ELEMENTS TO ENTER : ");
       
       int l=sc.nextInt();
       
       System.out.println("ENTER ELEMENTS : ");
       
       int [] ar=new int[l];
       
       for (int i=0;i<l;i++)
         {
          ar[i]=sc.nextInt();    
         }

        insertionSort(ar);
        
       
        System.out.println(Arrays.toString(ar));

    }

    public static void insertionSort(int[] array)
    
    {
        int n = array.length;
        for (int i = 1; i < n; ++i) 
        {
            int key = array[i];
            int j = i - 1;

            while (j >= 0 && array[j] > key) 
            {
                array[j + 1] = array[j];
                j = j - 1;
            }
            array[j + 1] = key;
        }
    

        int first = 0;
        int second = 0;

        for (int i = 0; i < n - 1; i++) 
        {
            if (array[i] > array[i + 1]) 
            {
                first = i;
                break;
            }
        }

        for (int i = n - 1; i > first; i--) 
        {
            if (array[i] < array[i - 1]) 
            {
                second = i;
                break;
            }
        }

        int temp = array[first];
        array[first] = array[second];
        array[second] = temp;
    }
}
    */
    //selection sort
//2.1 C

/*
    import java.util.Scanner;

    public class bubble_sort 
    {
    public static void bubble_sort(int[] arr) 
    {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) 
        {
            int minIndex = i;
            
            for (int j = i + 1; j < n; j++) 
            {
                if (arr[j] < arr[minIndex]) 
                {
                    minIndex = j;
                }
            }
            // Swap the found minimum element with the first element of the unsorted portion
            int temp = arr[minIndex];
            arr[minIndex] = arr[i];
            arr[i] = temp;
        }
    }

    public static void printArray(int[] arr) 
    {
        for (int i = 0; i < arr.length; i++) 
        {
            System.out.print(arr[i] + " ");
        }

        System.out.println();
    }

    public static void main(String[] args) 
    {
        Scanner sc = new Scanner(System.in);

        System.out.println("ENTER NO OF ELEMENTS TO ENTER : ");
    int x=sc.nextInt();
       // int[] arr = {64, 25, 12, 22, 11};
       int[] arr = new int[x];
       for (int i = 0; i < x; i++) 
       {
        System.out.print("ENTER ELEMENT "+(i+1)+" : ");
        arr[i] = sc.nextInt();
        
       } 
       
       System.out.println("ORIGINAL ARRAY:");
        printArray(arr);
        bubble_sort(arr);
        System.out.println("SORTED ARRAY:");
        printArray(arr);
    }
}

*/

