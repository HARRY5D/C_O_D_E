
class THREAD extends Thread 
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
        System.out.println("PRINTED BY RUNNABLE INTERFACE.");
    }
}

 class Threading 
 {
    public static void main(String[] args) 
    {
        THREAD t1 = new THREAD();
        t1.start();
        MyRunnable r = new MyRunnable();
        Thread t2 = new Thread(r);
        t2.start();
    }
}