public class assignment {
    
}
/*1
 class Counter {
    private int count = 0;
    public synchronized void increment() { count++; }
    public int getCount() { return count; }
}

public class ThreadCounter {
    public static void main(String[] args) throws InterruptedException {
        Counter c = new Counter();
        Thread t1 = new Thread(() -> { for(int i=0; i<1000; i++) c.increment(); });
        Thread t2 = new Thread(() -> { for(int i=0; i<1000; i++) c.increment(); });
        t1.start(); t2.start();
        t1.join(); t2.join();
        System.out.println("Count: " + c.getCount());
    }
}
2
class NumberPrinter {
    boolean isOdd = true;
    
    synchronized void printOdd(int num) {
        if(!isOdd) wait();
        System.out.println(num);
        isOdd = false;
        notify();
    }
    
    synchronized void printEven(int num) {
        if(isOdd) wait();
        System.out.println(num);
        isOdd = true;
        notify();
    }
}

public class EvenOddPrinter {
    public static void main(String[] args) {
        NumberPrinter np = new NumberPrinter();
        Thread odd = new Thread(() -> {
            for(int i=1; i<=10; i+=2) np.printOdd(i);
        });
        Thread even = new Thread(() -> {
            for(int i=2; i<=10; i+=2) np.printEven(i);
        });
        odd.start(); even.start();
    }
}
3
public class NamedThreads {
    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(() -> {
            for(int i=1; i<=5; i++) {
                System.out.println(Thread.currentThread().getName() + ": " + i);
                try { Thread.sleep(1000); } catch(InterruptedException e) {}
            }
        }, "Worker-1");
        
        Thread t2 = new Thread(() -> {
            System.out.println(Thread.currentThread().getName() + " started");
        }, "Worker-2");
        
        t1.start();
        t1.join();
        t2.start();
    }
}
4
import java.util.*;

public class WordChecker {
    public static void main(String[] args) {
        Set<String> unique = new HashSet<>();
        Set<String> duplicates = new HashSet<>();
        
        for(String word : args) {
            if(!unique.add(word)) duplicates.add(word);
        }
        unique.removeAll(duplicates);
        
        System.out.println("Unique: " + unique);
        System.out.println("Duplicates: " + duplicates);
    }
}
5
import java.util.*;

public class StudentManager {
    public static void main(String[] args) {
        ArrayList<String> students = new ArrayList<>();
        Scanner sc = new Scanner(System.in);
        
        while(true) {
            System.out.println("\n1.Add 2.Remove 3.Display 4.Check 5.Exit");
            switch(sc.nextInt()) {
                case 1: students.add(sc.next()); break;
                case 2: students.remove(sc.next()); break;
                case 3: System.out.println(students); break;
                case 4: System.out.println(students.contains(sc.next())); break;
                case 5: return;
            }
        }
    }
}
6
import java.util.*;

public class IntegerSorter {
    public static void main(String[] args) {
        ArrayList<Integer> nums = new ArrayList<>();
        Scanner sc = new Scanner(System.in);
        
        while(sc.hasNextInt()) nums.add(sc.nextInt());
        
        Collections.sort(nums);
        System.out.println("Ascending: " + nums);
        Collections.reverse(nums);
        System.out.println("Descending: " + nums);
    }
}
7
import java.util.*;

public class WordFrequency {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        HashMap<String, Integer> freq = new HashMap<>();
        
        String[] words = sc.nextLine().split(" ");
        for(String word : words) {
            freq.put(word, freq.getOrDefault(word, 0) + 1);
        }
        
        freq.forEach((word, count) -> System.out.println(word + ": " + count));
    }
}
8
import java.io.*;

public class FileCopy {
    public static void main(String[] args) {
        try (BufferedReader reader = new BufferedReader(new FileReader("source.txt"));
             BufferedWriter writer = new BufferedWriter(new FileWriter("dest.txt"))) {
            
            String line;
            while ((line = reader.readLine()) != null) {
                writer.write(line);
                writer.newLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
9
import java.io.*;

public class FileStats {
    public static void main(String[] args) {
        try (BufferedReader br = new BufferedReader(new FileReader("input.txt"))) {
            int lines = 0, words = 0, chars = 0;
            String line;
            
            while ((line = br.readLine()) != null) {
                lines++;
                chars += line.length();
                words += line.split("\\s+").length;
            }
            
            System.out.printf("Lines: %d\nWords: %d\nChars: %d", lines, words, chars);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
10
import java.io.*;

public class BinaryCopy {
    public static void main(String[] args) {
        try (BufferedInputStream in = new BufferedInputStream(new FileInputStream("input.bin"));
             BufferedOutputStream out = new BufferedOutputStream(new FileOutputStream("output.bin"))) {
            
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = in.read(buffer)) != -1) {
                out.write(buffer, 0, bytesRead);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
11
public class WordSearch {
    public static void main(String[] args) {
        try (BufferedReader br = new BufferedReader(new FileReader("input.txt"))) {
            String searchWord = "target";
            String line;
            int lineNum = 0;
            
            while ((line = br.readLine()) != null) {
                lineNum++;
                if (line.contains(searchWord)) {
                    System.out.println("Line " + lineNum + ": " + line);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
12
public class ReverseFileContent {
    public static void main(String[] args) {
        List<String> lines = new ArrayList<>();
        
        try (BufferedReader reader = new BufferedReader(new FileReader("input.txt"));
             BufferedWriter writer = new BufferedWriter(new FileWriter("output.txt"))) {
            
            String line;
            while ((line = reader.readLine()) != null) {
                lines.add(line);
            }
            
            for (int i = lines.size() - 1; i >= 0; i--) {
                writer.write(lines.get(i));
                writer.newLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
13
// mathoperations/Addition.java
package mathoperations;
public class Addition {
    public int add(int a, int b) { return a + b; }
}

// geometry/Rectangle.java
package geometry;
import mathoperations.Addition;
public class Rectangle {
    private int length, width;
    public int getPerimeter() {
        Addition add = new Addition();
        return 2 * add.add(length, width);
    }
}
14
// utilities/MathUtils.java
package utilities;
public class MathUtils {
    public static int square(int x) { return x * x; }
    public static int cube(int x) { return x * x * x; }
}

// Main.java
import static utilities.MathUtils.*;
public class Main {
    public static void main(String[] args) {
        System.out.println(square(5));
        System.out.println(cube(3));
    }
}
15
interface Payment {
    void processPayment(double amount);
}

class CreditCardPayment implements Payment {
    public void processPayment(double amount) {
        System.out.println("Processing " + amount + " via Credit Card");
    }
}

class PayPalPayment implements Payment {
    public void processPayment(double amount) {
        System.out.println("Processing " + amount + " via PayPal");
    }
}

public class PaymentProcessor {
    public static void main(String[] args) {
        Payment payment = new CreditCardPayment();
        payment.processPayment(100.0);
    }
}
16
@FunctionalInterface
interface Calculable { double calculate(double a, double b); }
@FunctionalInterface
interface Displayable { void display(String message); }

class Calculator {
    public static void main(String[] args) {
        Calculable add = (a, b) -> a + b;
        Displayable print = System.out::println;
        print.display("Result: " + add.calculate(5, 3));
    }
}
17
interface Student {
    String getName();
    String getID();
    double getGrade();
}

class UndergraduateStudent implements Student {
    private String name, id;
    private double grade;
    
    public String getName() { return name; }
    public String getID() { return id; }
    public double getGrade() { return grade; }
}
18-19
interface Course {
    String getName();
    void enroll(Student student);
}

class OnlineCourse implements Course {
    private String name;
    private List<Student> students = new ArrayList<>();
    
    public String getName() { return name; }
    public void enroll(Student student) { 
        students.add(student); 
    }
}
20-23
class ExceptionDemo {
    public static void main(String[] args) {
        try {
            int age = Integer.parseInt(new Scanner(System.in).nextLine());
            if(age < 18 || age > 100) 
                throw new IllegalArgumentException("Invalid age");
            
            double[] results = new double[5];
            results[age % 5] = 100 / age;
            
        } catch(NumberFormatException e) {
            System.out.println("Invalid number");
        } catch(ArithmeticException e) {
            System.out.println("Cannot divide by zero");
        } catch(ArrayIndexOutOfBoundsException e) {
            System.out.println("Invalid array index");
        } catch(IllegalArgumentException e) {
            System.out.println(e.getMessage());
        }
    }
}


  
 */