/*
 * (a) Implement dsa5_1 using array
Implement a program to implement a dsa5_1 using Array. Your task is to use the class as shown in the comments in the code editor and complete the functions push () and pop () to implement a dsa5_1.
Example 1:
Input:
push(2)
push(3)
pop()
push(4)
pop()
Output: 3, 4
 * 
 */


public class dsa5_1 {
    private int maxSize;
    private int top;
    private int[] dsa5_1Array;

    public dsa5_1(int size) {
        maxSize = size;
        dsa5_1Array = new int[maxSize];
        top = -1;
    }

    public void push(int value) {
        if (top >= maxSize - 1) {
            System.out.println("dsa5_1 is full. Can't push " + value);
            return;
        }
        dsa5_1Array[++top] = value;
    }

    public int pop() {
        if (top < 0) {
            System.out.println("dsa5_1 is empty. Can't pop.");
            return -1;
        }
        return dsa5_1Array[top--];
    }

    public static void main(String[] args) {
        dsa5_1 dsa5_1 = new dsa5_1(5);
        dsa5_1.push(2);
        dsa5_1.push(3);
        System.out.println(dsa5_1.pop()); // Output: 3
        dsa5_1.push(4);
        System.out.println(dsa5_1.pop()); // Output: 4
    }
}