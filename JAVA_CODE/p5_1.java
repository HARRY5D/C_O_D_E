/*
 
Write a Java program which have readInfo method called in Person class. 
readInfo method is written to ClientsInFile class. The purpose of the program is
 to read the client information from clients.txt, make an object out of every client 
 and finally print the information of every client on screen. Every client has their 
 individual row in the file. File has every client’s name and ID. Person class has one 
 String type attribute where the information of the person (name and ID) is stored in. 
 A toString method is required for Person class as well. toString returns the information of 
 the person. readInfo method receives an array as parameter. This array will be used 
 to store the created people. Method should create an object from each client in the file 
 and store it in the array. Method returns the number of persons in the file.

 Expected Output:
David 121279-2251
Matt 190970-1691
Homer 230369-2512
 */

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
 
class Person 
{
    public String info;   
    public Person(String info) 
    {
     this.info = info;
    }
    @Override
    public String toString() 
    {
      return info;
    }
}
 
class ClientsInFile 
{
    public int readInfo(Person[] people) 
    {
        try 
        {
            File file = new File("clients.txt");
            Scanner sc = new Scanner(file);
            int count = 0;
            while (sc.hasNextLine()) 
            {
                String line = sc.nextLine();
                String[] parts = line.split(" ");
                String name = parts[0];
                String id = parts[1];
                Person person = new Person(name + " " + id);
                people[count] = person;
                count++;
            }
            sc.close();
            return count;
        } 
        catch (FileNotFoundException e) 
        {
         System.out.println("File not found!");
          return 0;
        }
    }
}
class p5_1
{
     public static void main(String[] args) 
    {
        ClientsInFile cF = new ClientsInFile();
        Person[] p = new Person[4]; 
        int count = cF.readInfo(p);
        for (int i = 0; i < count; i++) 
        {
         System.out.println(p[i].toString());
        }
    }
}    

