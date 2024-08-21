import java.util.Arrays;
import java.util.Scanner;

public class bubble_sort
 {
    public static void main(String[] args)
     {
        
        Scanner sc=new Scanner(System.in);
       // int[] ar = {3, 8, 6, 7, 5, 9};
       System.out.print("ENTER NO OF ELEMENTS TO ENTER : ");
       
       int l=sc.nextInt();
       
       System.out.println("ENTER ELEMENTS : ");
       
       int [] ar=new int[l];
       
       for (int i=0;i<l;i++)
       {
       ar[i]=sc.nextInt();    
       }

        insertionSort(ar);
        
       // System.out.println("ARRAY : {3, 8, 6, 7, 5, 9}");
       
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
