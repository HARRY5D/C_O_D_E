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

Question 1 The correct answers are: (a) In Java, the extends clause is used to specify the inheritance relationship. (b) The subclass of a non-abstract class can be declared abstract.

Question 2 The correct answers are: (a) A class can only be extended by one class. (e) A non-final class can be extended by any number of classes is false, so this option is correct.

Question 3 The correct answers are: (a) The Bar class is a subclass of Foo. (b) The statement b.f(); is legal. (d) The statement a.g(); is legal.

Question 4 The correct answer is: (a) Private methods cannot be overridden in subclasses.

Question 5 The correct answer is: (f) ((A) this).doIt();

Question 6 The correct answer is: (d) The code will compile and print 23, when run.

Question 7 The correct answer is: (e) super.msg.text

Question 8 The correct answers are: (a) public int step1(int i) { return 1; } (e) private static String step2(String str) { return str; }

Question 9 The correct answer is: (e) MySub(int count) { this(count, count); }

Question 10 The correct answer is: (b) If both a subclass and its superclass do not have any declared constructors, the implicit default constructor of the subclass will call super() when run.

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
       */