class Parent:
    school_name = "XYZ School"
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def info(self):
        return f"{self.name} is {self.age} years old."

class Student(Parent):
    grade_scale = {"A": 90, "B": 80, "C": 70, "D": 60, "F": 0}
    
    def __init__(self, name, age, scores):
        super().__init__(name, age)
        self.scores = [scores] if isinstance(scores, int) else scores
        self._grade = None
    
    def ave(self):
        return sum(self.scores) / len(self.scores)
    
    def info(self):
        basic_info = super().info()
        return f"{basic_info} Average score: {self.ave()}"
    
    def student(self):
        return self.name, self.age, self.scores
    
    def get_grade(self):
        return self._grade
        
    def set_grade(self, grade):
        if grade in self.grade_scale:
            self._grade = grade
        else:
            print("Invalid grade")

class TA(Student, Parent):
    def __init__(self, name, age, scores, department):
        Student.__init__(self, name, age, scores)
        self.department = department
    
    def get_role(self):
        return f"Teaching Assistant in {self.department}"

name = input("Enter Student Name: ")    
age = int(input("Enter Student Age: "))
score = int(input("Enter Student Score: "))

s = Student(name, age, score)

print("Student Name:", s.name)
s.name = s.name.upper()
print("Modified Name:", s.name)

print("Student Details:", s.student())
print("Average Score:", s.ave())
print("Student Info:", s.info())

s.set_grade("A")
print("Assigned Grade:", s.get_grade())

print("School:", Parent.school_name)
print("Grade Scale:", Student.grade_scale)

print("Method Resolution Order:", TA.__mro__)

ta = TA("Alex", 28, [95, 90], "Computer Science")
print(ta.info())
print(ta.get_role())


class Person:
    species = "Homo sapiens"
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def introduce(self):
        return f"My name is {self.name} and I am {self.age} years old."

class Student(Person):
    school = "University"
    
    def __init__(self, name, age):
        super().__init__(name, age)
        self._grade = None
        
    def get_info(self):
        basic_info = super().introduce()
        return f"{basic_info} I am a student at {self.school}."
        
    def get_grade(self):
        return self._grade
        
    def set_grade(self, grade):
        if grade in ['A', 'B', 'C', 'D', 'F']:
            self._grade = grade
        else:
            print("Invalid grade")
            
    def __str__(self):
        return f"Student: {self.name}, Age: {self.age}"

class TeachingAssistant(Student, Person):
    def __init__(self, name, age, department=None):
        Student.__init__(self, name, age)
        self.department = department
        
    def get_role(self):
        return f"TA in {self.department} department"


name = input("Enter Student Name: ")    
age = int(input("Enter Student Age: "))

s = Student(name, age)

print(s.get_info())
print(f"Species: {s.species}")
print(f"School: {s.school}")

grade_letter = input("Enter grade (A-F): ")
s.set_grade(grade_letter)
print(f"Assigned Grade: {s.get_grade()}")

ta = TeachingAssistant("Alex", 28, "Computer Science")
print(ta.get_info())
print(ta.get_role())

print(f"MRO for TeachingAssistant: {TeachingAssistant.__mro__}")


class Main:
    def __init__(self):
        print("Main class initialized.")

    def run(self):
        print("This is the main class running.")


class Sub(Main):
    def __init__(self):
        print("Sub class initialized")
        super().__init__()
        print(TeachingAssistant.__mro__)


class A:
    def greet(self):
        return "Hello from A"

class B(A):
    def greet(self):
        return super().greet() + " and B"

class C(B):
    def greet(self):
        return super().greet() + " and C"

class D(C):
    def greet(self):
        return super().greet() + " and D"

d = D()
print(d.greet())