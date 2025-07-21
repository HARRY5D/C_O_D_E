/*
  Write a program to create thread which display “HELLO WORLD BY ” message.
A. by extending Thread class
B. by using Runnable interface.
 */
//import java.util.*;

public class p6_1 
{
    static class HELLO extends Thread 
    {
        @Override
        public void run() 
        {
            System.out.println("HELLO WORLD BY EXTENDING THREAD.");
        }
    }

    static class runner implements Runnable 
    {
        @Override
        public void run() 
        {
            System.out.println("HELLO WORLD BY USING RUNNABLE INTERFACE.");
        }
    }

    public static void main(String[] args) 
    {
        HELLO print = new HELLO();
        print.start();

        runner run = new runner();
        
        Thread r = new Thread(run);
        r.start();
    }
}