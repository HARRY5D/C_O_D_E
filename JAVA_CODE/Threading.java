/*Write a program to create thread which display “Hello World” message.
A. by extending Thread class
B. by using Runnable interface. */
class MyThread extends Thread 
{
    public void run() 
    {
        System.out.println("PRINTED BY EXTENDING THREAD CLASS.");
    }
}

class MyRunnable implements Runnable 
{
    public void run() 
    {
        System.out.println("PRINTED BY USING RUNNABLE INTERFACE.");
        System.out.println("Hello World");
    }
}

class Threading 
{
    public static void main(String[] args) 
    {
        MyThread t1 = new MyThread();
        t1.start();
        MyRunnable r = new MyRunnable();
        Thread t2 = new Thread(r);
        t2.start();
    }
}