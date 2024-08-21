/*import java.util.Scanner;

public class SortSwappedElements {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the size of the array: ");
        int size = scanner.nextInt();
        int[] arr = new int[size];
        System.out.println("Enter the elements of the array:");
        for (int i = 0; i < size; i++) {
            arr[i] = scanner.nextInt();
        }

        sortSwappedElements(arr);

        System.out.println("Sorted array: ");
        for (int i = 0; i < size; i++) {
            System.out.print(arr[i] + " ");
        }
    }

    public static void sortSwappedElements(int[] arr) {
        int n = arr.length;
        int first = -1, second = -1;

        // Find the two swapped elements
        for (int i = 0; i < n - 1; i++) {
            if (arr[i] > arr[i + 1]) {
                if (first == -1) {
                    first = i;
                } else {
                    second = i + 1;
                }
            }
        }

        // Swap the two elements
        if (second != -1) {
            swap(arr, first, second);
        }
    }

    public static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
    */
