/*

 */

import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

class Storage 
{
    private int value;
    private final Lock lock = new ReentrantLock();

    public void setValue(int value) 
    {
        lock.lock();
        try 
        {
            this.value = value;
        } 
        finally 
        {
            lock.unlock();
        }
    }

    public int getValue() 
    {
        lock.lock();
        try 
        {
            return value;
        } 
        finally 
        {
            lock.unlock();
        }
    }
}

class Counter implements Runnable 
{
    private final Storage storage;
    private volatile boolean running = true;

    public Counter(Storage storage) 
    {
        this.storage = storage;
    }

    @Override
    public void run() 
    {
        int count = 0;
        while (running) 
        {
            storage.setValue(count);
            count++;
         
            try 
            {
                Thread.sleep(1000); // Sleep for 1 second
            } 
            catch (InterruptedException e) 
            {
                Thread.currentThread().interrupt();
            }
        }
    }

    public void stop() 
    {
        running = false;
    }
}

class Printer implements Runnable 
{
    private final Storage storage;
    private volatile boolean running = true;

    public Printer(Storage storage) 
    {
        this.storage = storage;
    }

    @Override
    public void run() 
    {
        while (running) 
        {
            int value = storage.getValue();
            System.out.println("Current value: " + value);
            try 
            {
                Thread.sleep(1000); // Sleep for 1 second
            } 
            catch (InterruptedException e) 
            {
                Thread.currentThread().interrupt();
            }
        }
    }

    public void stop() 
    {
        running = false;
    }
}

 class multi_threading 
 {
    public static void main(String[] args) 
    {
        Storage storage = new Storage();
        Counter counter = new Counter(storage);
        Printer printer = new Printer(storage);

        Thread counterThread = new Thread(counter);
        Thread printerThread = new Thread(printer);

        counterThread.start();
        printerThread.start();

        try 
        {
            Thread.sleep(10000); // Let the program run for 10 seconds
        } 
        catch (InterruptedException e) 
        {

            e.printStackTrace();
        }

        counter.stop();
        printer.stop();

        try 
        {
            counterThread.join();
            printerThread.join();
        } 
        catch (InterruptedException e) 
        {
            e.printStackTrace();
        }

        System.out.println("Program finished.");
    }
}
