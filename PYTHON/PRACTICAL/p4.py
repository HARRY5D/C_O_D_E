class Parent:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Student(Parent):
    def __init__(self, name, age, score):
        super().__init__(name, age)
        self.score = score

    def ave(self):
        return sum(self.score) / len(self.score)
    
    def student(self):
        return self.name, self.age, self.score

name = input("Enter Student Name : ")    
age = int(input("Enter Student Age : "))
score = int(input("Enter Student Score : "))

s = Student(name, age, score)

print(s.student())
# print("Average Score : ", s.ave())

