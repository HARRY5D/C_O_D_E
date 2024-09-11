/*Write a Java program to take the salary of five different employees in an array.
Salary must be incremented by 5% through the thread. After every increment thread 
should be sleeping for around 2000 milliseconds. */
import java.util.Scanner;

class incrementor extends Thread 
{
    public double[] salaries;
    public int num;

    public incrementor(double[] salaries, int num) 
    {
        this.salaries = salaries;
        this.num = num;
    }

    @Override
    public void run() 
    {
        try 
        {
            for (int i = 0; i < 10; i++) 
            { 
                Thread.sleep(2000);
                synchronized (salaries) 
                {
                    salaries[num] = salaries[num] * 1.05;
                    System.out.println("SALARY OF EMPLOYEE " + (num + 1) + " IS INCREMENTED TO : " + salaries[num]);
                }
            }
        } 
        catch (InterruptedException e) 
        {
            Thread.currentThread().interrupt();
            System.out.println("THREAD INTERUPTED.");
        }
    }
}

public class p6_2 
{
    public static void main(String[] args) 
    {
        double[] salaries = new double[5];
        try (Scanner sc = new Scanner(System.in)) 
        {
            for (int i = 0; i < 5; i++) 
            {
                System.out.print("ENTER SALARY OF EMPLOYEE No." + (i + 1) + ": ");
                salaries[i] = sc.nextDouble();
            }
            for (int i = 0; i < 5; i++) 
            {
                incrementor inc = new incrementor(salaries, i);
                inc.start();
            }
        }
    }
}
