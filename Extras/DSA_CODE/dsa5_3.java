public class dsa5_3
{
    public static int searchMatrix(int[][] matrix, int target) 
    {
        int rows = matrix.length;
        int cols = matrix[0].length;
        int low = 0;
        int high = rows * cols - 1;

        while (low <= high) 
        {
            int mid = low + (high - low) / 2;
            int midVal = matrix[mid / cols][mid % cols];

            if (midVal == target) 
            {
                return mid;
            } 
            else if (midVal < target) 
            {
                low = mid + 1;
            } 
            else 
            {
                high = mid - 1;
            }
        }

        return -1; 
    }

    public static void main(String[] args) 
    {
        int[][] matrix = 
        {
            {1, 3, 5, 7},
            {10, 11, 16, 20},
            {23, 30, 34, 50}
        };

        int target = 11;
        int result = searchMatrix(matrix, target);

        if (result != -1) 
        {
            System.out.println("Target found at index " + result);
        } 
        else 
        {
            System.out.println("Target not found");
        }
    }
}