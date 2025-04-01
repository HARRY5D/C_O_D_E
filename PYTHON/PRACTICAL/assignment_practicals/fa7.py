class Student:
    school_name = "Charotar High School"
    total_students = 0
    
    def __init__(self, name, grade):
        
        self.name = name
        self.grade = grade
        
        Student.total_students += 1
    
    @classmethod
    def display_school_info(cls):
        print(f"School Name: {cls.school_name}")
        print(f"Total Students: {cls.total_students}")
    
    def display_student_info(self):
        print(f"Student: {self.name}, Grade: {self.grade}")

student1 = Student("Alice", 10)
student2 = Student("Bob", 11)
student3 = Student("Charlie", 9)

Student.display_school_info()
print("\nStudent Details:")
student1.display_student_info()
student2.display_student_info()
student3.display_student_info()