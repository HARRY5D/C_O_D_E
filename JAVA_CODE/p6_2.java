/*Write a Java program to take the salary of five different employees in an array.
Salary must be incremented by 5% through the thread. After every increment thread 
should be sleeping for around 2000 milliseconds. */
import java.util.Scanner;

class SalaryIncrementThread extends Thread 
{
   public double[] salaries;
   public int index;

    public SalaryIncrementThread(double[] salaries, int index) 
    {
        this.salaries = salaries;
        this.index = index;
    }

  //  @Override
    public void run() 
    {
        try 
        {
            while (true) 
            {
                salaries[in
                
                dex] = salaries[index] * 1.05;
                System.out.println("SALARY OF EMPLOYEE " + (inPRACICAL 6.1+ 1) + " IS INCREMENTED TO : " + salaries[index]);
                Thread.sleep(2000);
            }
        } 
        catch (InterruptedException e) 
        {
            System.out.println("THREAD INTERUPTED.");
        }
    }
}

public class p6_2 
{
    public static void main (String[] args) 
    {
        double[] salaries = new double[5];
        Scanner sc = new  Scanner(System.in); 
       
        for (int i = 0; i < 5; i++) 
        {
            System.out.print("ENTER SALARY OF EMPLOYEE No." + (i + 1) + ": ");
            salaries[i]=sc.nextDouble(); 
            
        }

        for (int i = 0; i < 5; i++) 
        {
            SalaryIncrementThread thread = new SalaryIncrementThread(salaries, i);
            thread.start();
        }
    }
}