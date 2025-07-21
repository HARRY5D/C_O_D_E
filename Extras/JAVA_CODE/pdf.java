class pdf {
    public static void classMethod() {
    System.out.println("classMethod() in pdf");
    }
    public void instanceMethod() {
    System.out.println("instanceMethod() in pdf");
    }
    }
    class Bar extends pdf {
    public static void classMethod() {
    System.out.println("classMethod() in Bar");
    }
    public void instanceMethod() {
    System.out.println("instanceMethod() in Bar");
    //return b;
    }
    class Test { }
    public static void main(String[] args) 
    {
    pdf f = new Bar();
    f.instanceMethod();
    f.classMethod();
    }
    }

    /*
     multi threading :

     1. Which is the correct way to start a new thread?
Select the one correct answer.
(a) Just create a new Thread object. The thread will start automatically.
(b) Create a new Thread object and call the method begin().
(c) Create a new Thread object and call the method start().
(d) Create a new Thread object and call the method run().
(e) Create a new Thread object and call the method resume().
ANSWER : (c)
Create a new Thread object and call the method start(). The call to the start()
method will return immediately and the thread will start executing the run()
method asynchronously.
2. When extending the Thread class to implement the code executed by a
thread, which method should be overridden?
Select the one correct answer.
(a) begin()
(b) start()
(c) run()
(d) resume()
(e) behavior()
ANSWER : (c)
When extending the Thread class, the run() method should be overridden to
provide the code executed by the thread. This is analogous to implementing the
run()method of the Runnable interface
3. Which statements are true?
Select the two correct answers.
(a) The class Thread is abstract.
(b) The class Thread implements Runnable.
(c) The Runnable interface has a single method named start.
(d) Calling the method run() on an object implementing Runnable will create a
new thread.
(e) A program terminates when the last user thread finishes.
ANSWER : (b) and (e)
The Thread class implements the Runnable interface and is not abstract. A
program terminates when the last user thread finishes. The Runnable interface
has a single method named run. Calling the run() method on a Runnable object
does not necessarily create a new thread; the run() method is executed by a
thread. Instances of the Thread class must be created to spawn new threads.
4. What will be the result of attempting to compile and run
the following program?
public class MyClass extends Thread {
public MyClass(String s) { msg = s; }
String msg;
public void run() {
System.out.println(msg);
}
public static void main(String[] args) {
new MyClass("Hello");
new MyClass("World");
}
Select the one correct answer.
(a) The program will fail to compile.
(b) The program will compile without errors and
will print Hello and World, in
that order, every time the program is run.
(c) The program will compile without errors and
will print a never-ending
stream of Hello and World.
(d) The program will compile without errors and
will print Hello and World when
run, but the order is unpredictable.
(e) The program will compile without errors and
will simply terminate without
any output when run.
ANSWER : (e)
The program will compile without errors and will simply terminate without any
output when run. Two thread objects will be created, but they will never be
started. The start() method must be called on the thread objects to make the
threads execute the run() method asynchronously.
5. What will be the result of attempting to compile and run the following program?
class Extender extends Thread {
public Extender() { }
public Extender(Runnable runnable) {super(runnable);}
public void run() {System.out.print("|Extender|");}
}
public class Implementer implements Runnable {
public void run() {System.out.print("|Implementer|");}
public static void main(String[] args) {
new Extender(new Implementer()).start(); // (1)
new Extender().start(); // (2)
new Thread(new Implementer()).start(); // (3)}}
Select the one correct answer.
(a) The program will fail to compile.
(b) The program will compile without errors and will print |Extender| twice and | Implementer
| once, in some order, every time the program is run.
(c) The program will compile without errors and will print|Extender| once and|Implementer|
twice, in some order, every time the program is run.
(d) The program will compile without errors and will print |Extender| once and | Implementer
| once, in some order, every time the program is run
(e) The program will compile without errors and will simply terminate without any output
when run.
(f) The program will compile without errors, and will print |Extender| once and Implementer|
once, in some order, and terminate because of an runtime error.
ANSWER : (b)
(1) results in the run() method of the Extender class being called, which
overrides the method from the Thread class, as does (2). (3) results in the run()
method of the Implementer class being called.
Invoking the start() method on a subclass of the Thread class always results in
the overridden run() method being called, regardless of whether a Runnable is
passed in a constructor of the subclass.
6. What will be the result of attempting to compile and run the following program?
class R1 implements Runnable {
public void run() {
System.out.print(Thread.currentThread().getName());
}}
public class R2 implements Runnable {
public void run() {
new Thread(new R1(),"|R1a|").run();
new Thread(new R1(),"|R1b|").start();
System.out.print(Thread.currentThread().getName());
}
public static void main(String[] args) {
new Thread(new R2(),"|R2|").start();
}}
Select the one correct answer.
(a) The program will fail to compile.
(b) The program will compile without errors and will print |R1a| twice and |R2|once, in some
order, every time the program is run.
(c) The program will compile without errors and will print|R1b| twice and |R2|once, in some
order, every time the program is run.
(d) The program will compile without errors and will print |R1b| once and |R2|twice, in some
order, every time the program is run.
(e) The program will compile without errors and will print |R1a| once, |R1b|once, and |R2|
once, in some order, every time the program is run.
ANSWER : (d)
Note that calling the run() method on a Thread object does not start a thread.
However, the run() method of the Thread class will invoke the run() method of
the Runnable object that is passed as argument in the constructor call. In other
words, the run() method of the R1 class is executed in the R2 thread, i.e., the
thread that called the run() method of the Thread class.
7. What will be the result of attempting to compile and run the following program?
public class Threader extends Thread {
Threader(String name) {
super(name); }
public void run() throws IllegalStateException {
System.out.println(Thread.currentThread().getName());
throw new IllegalStateException();
}
public static void main(String[] args) {
new Threader("|T1|").start();
}}
Select the one correct answer.
(a) The program will fail to compile.
(b) The program will compile without errors, will print |T1|, and terminate normally every
time the program is run.
(c) The program will compile without errors, will print|T1|, and throw an
IllegalStateException,
every time the program is run.
(d) None of the above.
ANSWER : (c)
Note that the complete signature of the run() method does not specify a throws
clause, meaning it does not throw any checked exceptions. However, it can
always be implemented with a throws clause containing unchecked exceptions,
as is the case in the code above.
8. What will be the result of attempting to compile and run the following
program?
public class Worker extends Thread {
public void run() {
System.out.print("|work|");
}
public static void main(String[] args) {
Worker worker = new Worker();
worker.start();
worker.run();
worker.start();
}
}
Select the one correct answer.
(a) The program will fail to compile.
(b) The program will compile without errors, will print |work| twice, and terminate normally
every time the program is run.
(c) The program will compile without errors, will print|work| three times, and terminate
normally every time the program is run.
(d) The program will compile without errors, will print|work| twice, and throw an
IllegalStateException, every time the program is run.
(e) None of the above.
ANSWER : (d)
The call to the run() method just executes the method in the main thread. Once
a thread has terminated, it cannot be started by calling the start() method as
shown above. A new thread must be created and started.
9. Given the following program, which statements are guaranteed to be
true?
public class ThreadedPrint {
static Thread makeThread(final String id, boolean daemon) {
Thread t = new Thread(id) {
public void run() { System.out.println(id);
}
};
t.setDaemon(daemon);
t.start();
return t;
}
public static void main(String[] args) {
Thread a = makeThread("A", false);
Thread b = makeThread("B", true);
System.out.print("End\n");
}
}
Select the two correct answers.
(a) The letter A is always printed.
(b) The letter B is always printed.
(c) The letter A is never printed after End.
(d) The letter B is never printed after End.
(e) The program might print B, End, and A, in that order.
ANSWER : (a) and (e)
Because the exact behavior of the scheduler is undefined, the text A, B, and End
can be printed in any order. The thread printing B is a daemon thread, which
means that the program may terminate before the thread manages to print the
letter. Thread A is not a daemon thread, so the letter A will always be printed
10.Given the following program, which alternatives would make good choices to synchronize
on at (1)?
public class Preference {
private int account1;
private Integer account2;
public void doIt() {
final Double account3 = new Double(10e10);
synchronized(/* ___(1)___ *//*) {
System.out.print("doIt");
}}}
Select the two correct answers.
(a) Synchronize on account1.
(b) Synchronize on account2.
(c) Synchronize on account3.
(d) Synchronize on this.
ANSWER : (b) and (d)
We cannot synchronize on a primitive value. Synchronizing on a local object is
useless, as each thread will create its own local object and it will not be a shared
resource.
11.Which statements are not true about the synchronized block?
Select the three correct answers.
(a) If the expression in a synchronized block evaluates to null, a NullPointer-
Exception will be thrown.
(b) The lock is only released if the execution of the block terminates normally.
(c) A thread cannot hold more than one lock at a time.
(d) Synchronized statements cannot be nested.
(e) The braces cannot be omitted even if there is only a single statement to
execute in the block.
ANSWER : (b) , (c) and (d)
The lock is also released when an uncaught exception occurs in the block.
12.Which statement is true?
Select the one correct answer.
(a) No two threads can concurrently execute synchronized methods on the same
object.
(b) Methods declared synchronized should not be recursive, since the object lock
will not allow new invocations of the method.
(c) Synchronized methods can only call other synchronized methods directly.
(d) Inside a synchronized method, one can assume that no other threads are
currently executing any other methods in the same class.
ANSWER : (a)
No two threads can concurrently execute synchronized methods on the same
object. This does not prevent one thread from executing a non-synchronized
method while another thread executes a synchronized method on the same
object. The synchronization mechanism in Java acts like recursive semaphores,
which means that during the time a thread owns the lock, it may enter and
re-enter any region of code associated with the lock, so there is nothing wrong
with recursive synchronized calls. Synchronized methods can call other
synchronized and nonsynchronized methods directly
13.Given the following program, which statement is true?
public class MyClass extends Thread {
static Object lock1 = new Object();
static Object lock2 = new Object();
static volatile int i1, i2, j1, j2, k1, k2;
public void run() { while (true) { doIt(); check(); } }
void doIt() {
synchronized(lock1) { i1++; }
j1++;
synchronized(lock2) { k1++; k2++; }
j2++;
synchronized(lock1) { i2++; } }
void check() {
if (i1 != i2) System.out.println("i");
if (j1 != j2) System.out.println("j");
if (k1 != k2) System.out.println("k");
}
public static void main(String[] args) {
new MyClass().start();
new MyClass().start();
}}
Select the one correct answer.
(a) The program will fail to compile.
(b) One cannot be certain whether any of the letters i, j, and k will be printed during
execution.
(c) One can be certain that none of the letters i, j, and k will ever be printed during execution.
(d) One can be certain that the letters i and k will never be printed during execution.
(e) One can be certain that the letter k will never be printed during execution.
ANSWER : (b)
One cannot be certain whether any of the letters i, j, and k will be printed
during execution. For each invocation of the doIt() method, each variable pair is
incremented and their values are always equal when the method returns. The
only way a letter could be printed would be if the method check() was executed
between the time the first and the second variable were incremented. Since the
check() method does not depend on owning any lock, it can be executed at any
time, and the method doIt() cannot protect the atomic nature of its operations
by acquiring locks.
14. Given the following program, which code
modifications will result in both threads
being able to participate in printing one smiley
(:-)) per line continuously?
public class Smiley extends Thread {
pulic void run() { // (1)
while(true) { // (2)
try { // (3)
System.out.print(":"); // (4)
sleep(100); // (5)
System.out.print("-"); // (6)
sleep(100); // (7)
System.out.println(")"); // (8)
sleep(100); // (9)
} catch (InterruptedException e) {
e.printStackTrace();
} } }
public static void main(String[] args) {
new Smiley().start();
new Smiley().start();
}
}
Select the two correct answers.
(a) Synchronize the run() method with the keyword synchronized, (1).
(b) Synchronize the while loop with a synchronized(Smiley.class) block, (2).
(c) Synchronize the try-catch construct with a synchronized(Smiley.class) block,(3).
(d) Synchronize the statements (4) to (9) with one synchronized(Smiley.class) block.
(e) Synchronize each statement (4), (6), and (8) individually with a synchronized
(Smiley.class) block.
(f) None of the above will give the desired result.
ANSWER : (c) and (d)
First note that a call to sleep() does not release the lock on the Smiley.class
object once a thread has acquired this lock. Even if a thread sleeps, it does not
release any locks it might possess.
(a) does not work, as run() is not called directly by the client code.
(b) does not work, as the infinite while loop becomes the critical region and the
lock will never be released. Once a thread has the lock, other threads cannot
participatein printing smileys.
(c) works, as the lock will be released between each iteration, giving other
threads the chance to acquire the lock and print smileys.
(d) works for the same reason as (c), since the three print statements will be
executed as one atomic operation.
(e) may not work, as the three print statements may not be executed as one
atomic operation, since the lock will be released after each print statement.
Synchronizing on this does not help, as the printout from each of the three print
statements executed by each thread can be interspersed.
15. Given:
public static synchronized void main(String[] args) throws
InterruptedException {
Thread t = new Thread();
t.start();
System.out.print("X");
t.wait(10000);
System.out.print("Y");
}
What is the result of this code?
A. It prints X and exits
B. It prints X and never exits
C. It prints XY and exits almost immediately
D. It prints XY with a 10-second delay between X and Y
E. It prints XY with a 10,000-second delay between X and Y
F. The code does not compile
G. An exception is thrown at runtime
ANSWER : (G)
The code does not acquire a lock on t before calling t.wait(), so it throws an
IllegalMonitorStateException. The method is synchronized, but it's not
synchronized on t so the exception will be thrown. If the wait were placed
inside a synchronized(t) block, then D would be correct.
16. Which are true? (Choose all that apply.)
A. The notifyAll() method must be called from a synchronized context
B. To call wait(), an object must own the lock on the thread
C. The notify() method is defined in class java.lang.Thread
D. When a thread is waiting as a result of wait(), it releases its lock
E. The notify() method causes a thread to immediately release its lock
F. The difference between notify() and notifyAll() is that notifyAll() notifies all
waiting threads, regardless of the object they're waiting on
ANSWER :
A is correct because notifyAll() (and wait() and notify()) must be called from
within a synchronized context. D is a correct statement.
B is incorrect because to call wait(), the thread must own the lock on the object
that wait() is being invoked on, not the other way around. C is incorrect because
notify() is defined in java.lang.Object. E is incorrect because notify() will not
cause a thread to release its locks. The thread can only release its locks by
exiting the synchronized code. F is incorrect because notifyAll() notifies all the
threads waiting on a particular locked object, not all threads waiting on any
object.
17. Given
class MyThread extends Thread {
MyThread() {
System.out.print("MyThread ");
}
public void run() {
System.out.print("bar ");
}
public void run(String s) {
System.out.print("baz ");
}
}
public class TestThreads {
public static void main (String [] args) {
Thread t = new MyThread() {
public void run() {
System.out.print("foo ");
}
};
t.start();
} }
What is the result?
A. foo
B. MyThread foo
C. MyThread bar
D. foo bar
E. foo bar baz
F. bar foo
G. Compilation fails
H. An exception is thrown at runtime
ANSWER : (B)
B is correct. In the first line of main we're constructing an instance of an
anonymous inner class extending from MyThread. So the MyThread constructor
runs and prints MyThread. Next, main() invokes start() on the new thread
instance, which causes the overridden run() method (the run() method in the
anonymous inner class) to be invoked.
18. public class Leader implements Runnable {
public static void main(String[] args) {
Thread t = new Thread(new Leader());
t.start();
System.out.print("m1 ");
t.join();
System.out.print("m2 ");
}
public void run() {
System.out.print("r1 ");
System.out.print("r2 ");
} }
Which are true? (Choose all that apply.)
A. Compilation fails
B. The output could be r1 r2 m1 m2
C. The output could be m1 m2 r1 r2
D. The output could be m1 r1 r2 m2
E. The output could be m1 r1 m2 r2
F. An exception is thrown at runtime
ANSWER : (A)
The join() must be placed in a try/catch block. If it were, answers B and D would
be correct. The join() causes the main thread to pause and join the end of the
other thread, meaning "m2" must come last.
Programming Exercises
1. Declare an interface called Function that has a method named evaluate
that takes an int parameter and returns an int value. Create a class called Half
that implements the Function interface. The implementation of the method
evaluate() should return the value obtained by dividing the int argument by
2. In a client, create a method that takes an arbitrary array of int values as a
parameter, and returns an array that has the same length, but the value of an
element in the new array is half that of the value in the corresponding
element in the array passed as the parameter. Let the implementation of this
method create an instance of Half, and use this instance to calculate values
for the array that is returned.
1. Implement three classes: Storage, Counter, and Printer. The Storage class
should store an integer. The Counter class should create a thread that starts
counting from 0 (0, 1, 2, 3, ...) and stores each value in the Storage class. The
Printer class should create a thread that keeps reading the value in the
Storage class and printing it.
Write a program that creates an instance of the Storage class and sets up a
Counter and a Printer object to operate on it.
2. Modify the program from the previous exercise to ensure that each number is
printed exactly once, by adding suitable synchronization.


    multi threading code :  https://www.blackbox.ai/share/35ddca1d-5e87-4c87-bd68-8a5e2f714bbc 
or see on date 9/11/24


        Which statements are true?
Select the two correct answers.
(a) In Java, the extends clause is used to specify the inheritance relationship. -true
(b) The subclass of a non-abstract class can be declared abstract.- true
(c) All members of the superclass are inherited by the subclass. – false
(d) A final class can be abstract. – false
(e) A class in which all the members are declared private, cannot be declared public.- false
Which statements are true?
Select the two correct answers.
(a) A class can only be extended by one class. -True
(b) Every Java object has a public method named equals.
(c) Every Java object has a public method named length.
(d) A class can extend any number of classes.-True
(e) A non-final class can be extended by any number of classes.-false
Which statements are true?
Select the two correct answers.
(a) A subclass must define all the methods from the superclass.
(b) It is possible for a subclass to define a method with the same name and parameters as a
method defined by the superclass.
(c) It is possible for a subclass to define a field with the same name as a field defined by the
superclass.
(d) It is possible for two classes to be the superclass of each other.
Given the following classes and declarations, which statements are
true?
// Classes
class Foo {
private int i;
public void f() { /* ... */ 
/*
public void g() { /* ... */ 
/*
class Bar extends Foo {
public int j;
public void g() { /* ... */ //}


// Declarations:
/*
Foo a = new Foo();
Bar b = new Bar();
Select the three correct answers.
(a) The Bar class is a subclass of Foo.
(b) The statement b.f(); is legal.
(c) The statement a.j = 5; is legal.
(d) The statement a.g(); is legal.
(e) The statement b.i = 3; is legal.
Which statement is true?
Select the one correct answer.
(a) Private methods cannot be overridden in subclasses.
(b) A subclass can override any method in a superclass.
(c) An overriding method can declare that it throws checked exceptions that are not thrown
by the method it is overriding.
(d) The parameter list of an overriding method can be a subset of the parameter list of the
method that it is overriding.
(e) The overriding method must have the same return type as the overridden method.
Given classes A, B, and C, where B extends A, and C extends B, and where all classes
implement the instance method void doIt(). How can the doIt() method in A be called from
an instance method in C?
Select the one correct answer.
(a) doIt();
(b) super.doIt();
(c) super.super.doIt();
(d) this.super.doIt();
(e) A.this.doIt();
(f) ((A) this).doIt();
(g) It is not possible.
What would be the result of compiling and running the following program?
// Filename: MyClass.java
public class MyClass {
public static void main(String[] args) {
C c = new C();
System.out.println(c.max(13, 29));
} }
class A {
int max(int x, int y) { if (x>y) return x; else return y; }
}
class B extends A{
int max(int x, int y) { return super.max(y, x) - 10; }
}
class C extends B {
int max(int x, int y) { return super.max(x+10, y+10); }
}
Select the one correct answer.
(a) The code will fail to compile because the max()
method in B passes the arguments in the call
super.max(y, x) in the wrong order.
(b) The code will fail to compile because a call to a max()
method is ambiguous.
(c) The code will compile and print 13, when run.
(d) The code will compile and print 23, when run.
(e) The code will compile and print 29, when run.
(f) The code will compile and print 39, when run.
Which is the simplest expression that can be inserted at (1), so that
the program prints the value of the text field from the Message class?
class Message {
// The message that should be printed:
String text = "Hello, world!"; }
class MySuperclass {
Message msg = new Message(); }
public class MyClass extends MySuperclass {
public static void main(String[] args) {
MyClass object = new MyClass();
object.print(); }
public void print() {
System.out.println(
/* (1) INSERT THE SIMPLEST EXPRESSION HERE );
/*
} }
Select the one correct answer.
(a) text
(b) Message.text
(c) msg.text
(d) object.msg.text
(e) super.msg.text
(f) object.super.msg.text
Which method declarations, when inserted at (7), will not result in a
compile-time error?
class MySuperclass {
public Integer step1(int i)
{ return 1; } // (1)
protected String step2
(String str1, String str2) { return str1; } // (2)
public String step2(String str1)
{ return str1; } // (3)
public static String step2() { return "Hi"; } // (4)
public MyClass makeIt() { return new MyClass(); } // (5)
public MySuperclass makeIt2() { return new MyClass(); } // (6)
}
public class MyClass extends MySuperclass {
// (7) INSERT METHOD DECLARATION HERE
}
Select the two correct answers.
(a) public int step1(int i) { return 1; }
(b) public String step2(String str2, String str1) {
return str1; }
(c) private void step2() { }
(d) private static void step2() { }
(e) private static String step2(String str) { return str; }
(f) public MySuperclass makeIt() {
return new MySuperclass(); }
(g) public MyClass makeIt2() { return new MyClass(); }
Which constructors can be inserted at (1) in MySub without causing a compile-time
error?
class MySuper {
int number;
MySuper(int i) { number = i; }
}
class MySub extends MySuper {
int count;
MySub(int count, int num) {
super(num);
this.count = count;
}
// (1) INSERT CONSTRUCTOR HERE }
Select the one correct answer.
(a) MySub() {}
(b) MySub(int count) { this.count = count; }
(c) MySub(int count) { super(); this.count = count; }
(d) MySub(int count) { this.count = count;
super(count); }
(e) MySub(int count) { this(count, count); }
(f) MySub(int count) { super(count); this(count, 0); }
Which statement is true?
Select the one correct answer.
(a) A super() or this() call must always be provided explicitly as the first statement in the body
of a constructor.
(b) If both a subclass and its superclass do not have any declared constructors, the implicit
default constructor of the subclass will call super() when run.
(c) If neither super() nor this() is declared as the first statement in the body of a constructor,
this() will implicitly be inserted as the first statement.
(d) If super() is the first statement in the body of a constructor, this() can be declared as the
second statement.
(e) Calling super() as the first statement in the body of a constructor of a subclass will always
work, since all superclasses have a default constructor.
(The Person, Student, Employee, Faculty, and Staff classes)
• Design a class named Person and its two subclasses named Student and
Employee. Make Faculty and Staff subclasses of Employee.
• A person has a name, address, phone number, and email address.
• A student has a class status (freshman, junior, or senior). Define the status
as a constant.
• An employee has an office, salary, and date hired.
• A faculty member has office hours and a rank. A staff member has a title.
Override the toString method in each class to display the class name and
the person’s name.
Consider an example of declaring the examination result. Design three classes: Student,
Exam, and Result. The Student class has data members such as those representing
rollNumber, Name, etc. Create the class Exam by inheriting Student class. The Exam class
adds fields representing the marks scored in six subjects. Derive Result from the Exam class,
and it has its own fields such as total_marks. Write an interactive program to model this
relationship.
     */


     /*
      I'll help you with each question.

Question 1 The correct answers are: (a) In Java, the extends clause is used to specify the inheritance relationship. 
(b) The subclass of a non-abstract class can be declared abstract.

Question 2 The correct answers are: (a) A class can only be extended by one class. 
(e) A non-final class can be extended by any number of classes is false, so this option is correct.

Question 3 The correct answers are: (a) The Bar class is a subclass of Foo.
 (b) The statement b.f(); is legal. (d) The statement a.g(); is legal.

Question 4 The correct answer is: (a) Private methods cannot be overridden in subclasses.

Question 5 The correct answer is: (f) ((A) this).doIt();

Question 6 The correct answer is: (d) The code will compile and print 23, when run.

Question 7 The correct answer is: (e) super.msg.text

Question 8 The correct answers are: (a) public int step1(int i) { return 1; } (e) private static String step2(String str) { return str; }

Question 9 The correct answer is: (e) MySub(int count) { this(count, count); }

Question 10 The correct answer is: (b) If both a subclass and its superclass do not have any declared constructors, 
the implicit default constructor of the subclass will call super() when run.

Question 11 Here is the design for the classes:

public class Person {
    private String name;
    private String address;
    private String phoneNumber;
    private String email;

    public Person(String name, String address, String phoneNumber, String email) {
        this.name = name;
        this.address = address;
        this.phoneNumber = phoneNumber;
        this.email = email;
    }

    @Override
    public String toString() {
        return "Person: " + name;
    }
}

public class Student extends Person {
    private String classStatus;

    public Student(String name, String address, String phoneNumber, String email, String classStatus) {
        super(name, address, phoneNumber, email);
        this.classStatus = classStatus;
    }

    @Override
    public String toString() {
        return "Student: " + super.toString() + ", Class Status: " + classStatus;
    }
}

public class Employee extends Person {
    private String office;
    private double salary;
    private Date dateHired;

    public Employee(String name, String address, String phoneNumber, String email, String office, double salary, Date dateHired) {
        super(name, address, phoneNumber, email);
        this.office = office;
        this.salary = salary;
        this.dateHired = dateHired;
    }

    @Override
    public String toString() {
        return "Employee: " + super.toString() + ", Office: " + office + ", Salary: " + salary + ", Date Hired: " + dateHired;
    }
}

public class Faculty extends Employee {
    private String officeHours;
    private String rank;

    public Faculty(String name, String address, String phoneNumber, String email, String office, double salary, Date dateHired, String officeHours, String rank) {
        super(name, address, phoneNumber, email, office, salary, dateHired);
        this.officeHours = officeHours;
        this.rank = rank;
    }

    @Override
    public String toString() {
        return "Faculty: " + super.toString() + ", Office Hours: " + officeHours + ", Rank: " + rank;
    }
}

public class Staff extends Employee {
    private String title;

    public Staff(String name, String address, String phoneNumber, String email, String office, double salary, Date dateHired, String title) {
        super(name, address, phoneNumber, email, office, salary, dateHired);
        this.title = title;
    }

    @Override
    public String toString() {
        return "Staff: " + super.toString() + ", Title: " + title;
    }
}

quest : 12 : 

public class Student {
    private int rollNumber;
    private String name;

    public Student(int rollNumber, String name) {
        this.rollNumber = rollNumber;
        this.name = name;
    }

    @Override
    public String toString() {
        return "Student: " + name + ", Roll Number: " + rollNumber;
    }
}

public class Exam extends Student {
    private int marks1;
    private int marks2;
    private int marks3;
    private int marks4;
    private int marks5;
    private int marks6;

    public Exam(int rollNumber, String name, int marks1, int marks2, int marks3, int marks4, int marks5
      */



      //exception handling : 
      /*
      What is the output of this program?
1.class exception_handling
2.{
3.public static void main(String args[])
4.{
5.try
6.{
7.System.out.print("Hello" + " " + 1 / 0);
8.}
9.catch(ArithmeticException e)
10.{
11.System.out.print("World");
12.}
13.}
14.}
JAVA Exception Handling
Q-02
Given:
try { int x = Integer.parseInt("two"); }
Which could be used to create an appropriate
catch block? (Choose all that apply.)
Options are-
A. ClassCastException
B. IllegalStateException
C. NumberFormatException
D. IllegalArgumentException
E. ExceptionInInitializerError
F. ArrayIndexOutOfBoundsException
JAVA Exception Handling
3
Which of these keywords is used to
manually throw an exception?
a) try
b) finally
c) throw
d) catch
JAVA Exception Handling
4 What is the output of this program?
1.class exception_handling
2.{
3.public static void main(String args[])
4.{
5.try
6.{
7.int a, b;
8.b = 0;
9.a = 5 / b;
10.System.out.print("A");
11.}
12.catch(ArithmeticException e)
13.{
14.System.out.print("B");
15.}
16.}
17.}
JAVA Exception Handling
5. What is the output here
1.class exception_handling
2.{
3.public static void main(String args[])
4.{
5.try
6.{
7.int a, b;
8.b = 0;
9.a = 5 / b;
10.System.out.print("A");
11.}
12.catch(ArithmeticException e)
13.{
14.System.out.print("B");
15.}
16.finally
17.{
18.System.out.print("C");
19.}
20.}
21.} JAVA Exception Handling
Q-06
try
{
int x = 0;
int y = 5 / x;
}
catch (Exception e)
{
System.out.println("Exception");
}
catch (ArithmeticException ae)
{
System.out.println(" Arithmetic Exception");
}
System.out.println("finished");
A.Finished
B. Exception
C. Compilation fails.
D. Arithmetic Exception
JAVA Exception Handling
public class X
{
public static void main(String [] args)
{
try
{
badMethod();
System.out.print("A");
}
catch (Exception ex)
{
System.out.print("B");
}
finally
{
System.out.print("C");
}
System.out.print("D");
}
public static void badMethod()
{
throw new Error(); /* Line 22 
}
}
JAVA Exception Handling
• ABCD
• Compilation fails.
• C is printed before exiting with an error
message.
• BC is printed before exiting with an error
message.
JAVA Exception Handling
public class X {
public static void main(String [] args)
{ try
{ badMethod();
System.out.print("A");
}
catch (RuntimeException ex) /* Line 10 
{ System.out.print("B");
}
catch (Exception ex1)
{
System.out.print("C");
}
finally {
System.out.print("D");
}
System.out.print("E");
}
public static void badMethod()
{
throw new RuntimeException();
} }
JAVA Exception Handling
• BD
• BCD
• BDE
• BCDE
JAVA Exception Handling

Let's analyze each of your questions one by one:

Q-01: Output of the program
java
Insert Code
Edit
Copy code
class exception_handling {
    public static void main(String args[]) {
        try {
            System.out.print("Hello" + " " + 1 / 0);
        } catch (ArithmeticException e) {
            System.out.print("World");
        }
    }
}
Output: Hello followed by an ArithmeticException will occur due to division by zero. The catch block will handle this exception, so the output will be:

Insert Code
Edit
Copy code
Hello World
Q-02: Appropriate catch block for Integer.parseInt("two")
The Integer.parseInt("two") will throw a NumberFormatException because "two" is not a valid integer. The appropriate catch blocks are:

C. NumberFormatException
D. IllegalArgumentException (since NumberFormatException is a subclass of IllegalArgumentException)
Correct Options: C, D

Q-03: Keyword to manually throw an exception
The keyword used to manually throw an exception in Java is:

c) throw
Q-04: Output of the program
java
Insert Code
Edit
Copy code
class exception_handling {
    public static void main(String args[]) {
        try {
            int a, b;
            b = 0;
            a = 5 / b;
            System.out.print("A");
        } catch (ArithmeticException e) {
            System.out.print("B");
        }
    }
}
Output: The program will throw an ArithmeticException due to division by zero, and the catch block will handle it. Therefore, the output will be:

Insert Code
Edit
Copy code
B
Q-05: Output of the program with finally block
java
Insert Code
Edit
Copy code
class exception_handling {
    public static void main(String args[]) {
        try {
            int a, b;
            b = 0;
            a = 5 / b;
            System.out.print("A");
        } catch (ArithmeticException e) {
            System.out.print("B");
        } finally {
            System.out.print("C");
        }
    }
}
Output: Similar to the previous case, the ArithmeticException will be caught, and "B" will be printed. The finally block will execute regardless of whether an exception occurred or not, so "C" will also be printed. Thus, the output will be:

Insert Code
Edit
Copy code
BC
Q-06: Output of the program
java
Insert Code
Edit
Copy code
try {
    int x = 0;
    int y = 5 / x;
} catch (Exception e) {
    System.out.println("Exception");
} catch (ArithmeticException ae) {
    System.out.println("Arithmetic Exception");
}
System.out.println("finished");
Output: The catch (Exception e) block will catch the ArithmeticException, as Exception is the superclass of ArithmeticException. Therefore, "Exception" will be printed, followed by "finished":

Insert Code
Edit
Copy code
compilation fails 

Q-07: Output of the program with Error
java
Insert Code
Edit
Copy code
public class X {
    public static void main(String [] args) {
        try {
            badMethod();
            System.out.print("A");
        } catch (Exception ex) {
            System.out.print("B");
        } finally {
            System.out.print("C");
        }
        System.out.print("D");
    }
    
    public static void badMethod() {
        throw new Error(); // Line 22
    }
}
Output: An Error is thrown which is not caught by the catch (Exception ex) block. The finally block will execute, printing "C", but the program will terminate with an error before printing "D". Therefore, the output will be:

Insert Code
Edit
Copy code
C
(Note: "D" is not printed because the error causes the program to terminate.)

Q-08: Output of the program with RuntimeException
java
Insert Code
Edit
Copy code
public class X {
    public static void main(String [] args) {
        try {
            badMethod();
            System.out.print("A");
        } catch (RuntimeException ex) { // Line 10
            System.out.print("B");
        } catch (Exception ex1) {
            System.out.print("C");
        } finally {
            System.out.print("D");
        }
        System.out.print("E");
    }
    
    public static void badMethod() {
        throw new RuntimeException();
    }
}
Output: The badMethod throws a RuntimeException, which will be caught by the catch (RuntimeException ex) block, printing "B". The finally block will execute, printing "D", and then "E" will be printed. Therefore, the output will be:

Insert Code
Edit
Copy code
BDE
Feel free to ask if you

*/