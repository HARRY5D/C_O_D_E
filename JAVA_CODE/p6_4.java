//AIM : Write a program to solve producer-consumer problem using thread Synchronization.
/*

public class p6_4 {
    private static final int MAX_SIZE = 5;
    private final int[] s = new int[MAX_SIZE];
    private int count = 0;
    private int in = 0; 
    private int out = 0;

    public synchronized void produce(int item) throws InterruptedException 
    {
        while (count == MAX_SIZE) 
        {
            wait();
        }
        s[in] = item;
        in = (in + 1) % MAX_SIZE;
        count++;
        System.out.println("Produced: " + item);
        notify();
    }

    public synchronized int consume() throws InterruptedException 
    {
        while (count == 0) 
        {
            wait();
        }
        int item = s[out];
        out = (out + 1) % MAX_SIZE;
        count--;
        System.out.println("Consumed: " + item);
        notify();
        return item;
    }

    static class Producer extends Thread 
    {
        private final p6_4 s;

        public Producer(p6_4 s) 
        {
            this.s = s;
        }

        @Override
        public void run() 
        {
            try 
            {
                int item = 0;
                while (true) 
                {
                    s.produce(item++);
                    Thread.sleep(1000);
                }
            } 
            catch (InterruptedException e) 
            {
                Thread.currentThread().interrupt();
            }
        }
    }

    static class Consumer extends Thread 
    {
        private final p6_4 s;

        public Consumer(p6_4 s) 
        {
            this.s = s;
        }

        @Override
        public void run() 
        {
            try 
            {
                while (true) 
                {
                    s.consume();
                    Thread.sleep(1500);
                }
            } 
            catch (InterruptedException e) 
            {
                Thread.currentThread().interrupt();
            }
        }
    }

    public static void main(String[] args) 
    {
        p6_4 s = new p6_4();
        Producer producer = new Producer(s);
        Consumer consumer = new Consumer(s);
        producer.start();
        consumer.start();
    }
}
*/

class Buffer 
{
    private int[] buffer;
    private int count;
    private int in;
    private int out;

    public Buffer(int size) 
    {
        buffer = new int[size];
        count = 0;
        in = 0;
        out = 0;
    }

    public synchronized void produce(int item) throws InterruptedException {
        while (count == buffer.length) 
        {
            wait();
        }
        buffer[in] = item;
        in = (in + 1) % buffer.length;
        count++;
        System.out.println("Produced: " + item);
        notify();
    }

    public synchronized int consume() throws InterruptedException 
    {
        while (count == 0) 
        {
            wait();
        }
        int item = buffer[out];
        out = (out + 1) % buffer.length;
        count--;
        System.out.println("Consumed: " + item);
        notify();
        return item;
    }
}

class Producer extends Thread 
{
    private Buffer buffer;
    private int item;

    public Producer(Buffer buffer) {
        this.buffer = buffer;
    }

    @Override
    public void run() 
    {
        try 
        {
            while (true) {
                buffer.produce(item++);
                Thread.sleep(1000);
            }
        } 
        catch (InterruptedException e) 
        {
            Thread.currentThread().interrupt();
        }
    }
}

class Consumer extends Thread 
{
    private Buffer buffer;

    public Consumer(Buffer buffer) 
    {
        this.buffer = buffer;
    }

    @Override
    public void run() 
    {
        try 
        {
            while (true) 
            {
                buffer.consume();
                Thread.sleep(1500);
            }
        } 
        catch (InterruptedException e) 
        {
            Thread.currentThread().interrupt();
        }
    }
}

 class ProducerConsumer 
 {
    public static void main(String[] args) 
    {
        Buffer buffer = new Buffer(5);
        Producer producer = new Producer(buffer);
        Consumer consumer = new Consumer(buffer);
        producer.start();
        consumer.start();
    }
}

