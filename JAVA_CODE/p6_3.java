/*Write a Java program with three different Thread names “Dhoni”,
“Kohli”, “Hardik”. Give “Dhoni” the highest priority and “Hardik” 
the lowest priority and check the execution of the Thread from highest
to lowest place every thread in the loop of 5 iterations. After every print,
there is sleep of thread around 1000 millisecond. If the execution of the thread does not 
go in the given order then find the alternate way and create 
another program through join() method. */
/*
public class p6_3 
{
    
}*/

class p6_3 extends Thread 
{
    public p6_3(String name) 
    {
    super(name);
    }
    public void run() 
    {
        for (int i = 1; i <= 5; i++) 
        {
        try 
        {
        Thread.sleep(1000);
        } 
        catch (InterruptedException e) 
        {
        System.out.println(e);
        }
        System.out.println(getName() + " ITERATION : " + i);
        }
    }
        public static void main(String[] args) 
        {
        
        p6_3 d = new p6_3("DHONI");
        p6_3 k = new p6_3("KOHLI");
        p6_3 h = new p6_3("HARDIK");
        
        d.setPriority(Thread.MAX_PRIORITY);
        k.setPriority(Thread.NORM_PRIORITY);
        h.setPriority(Thread.MIN_PRIORITY);
        
        d.start();
        k.start();
        h.start();
        }
        }