# AIM: Create a Student class with attributes for name, age, and grades, and methods to calculate the average grade and display student information.
class Student:
    def __init__(self, name, age, grades=None):
        self.name = name
        self.age = age
        self.grades = grades if grades is not None else []

    def add_grade(self, grade):
        self.grades.append(grade)

    def calculate_average(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def display_info(self):
        print("Student Information:")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Grades: {self.grades}")
        print(f"Average Grade: {self.calculate_average():.2f}")

if __name__ == "__main__":
    # First program
    print("\n===== STUDENT CLASS DEMO =====")
    student = Student("Alice", 20, [85, 80, 78, 92])
    student.add_grade(88)
    student.display_info()

    # AIM: Create a BankAccount class with attributes for account number, balance, and account type, and methods to deposit, withdraw, and display account information.
    class BankAccount:
        def __init__(self, account_number, balance=0, account_type="Savings"):
            self.account_number = account_number
            self.balance = balance
            self.account_type = account_type

        def deposit(self, amount):
            if amount > 0:
                self.balance += amount
                print(f"Deposited ${amount}. New balance: ${self.balance}")
            else:
                print("Deposit amount must be positive")

        def withdraw(self, amount):
            if amount > 0:
                if amount <= self.balance:
                    self.balance -= amount
                    print(f"Withdrew ${amount}. New balance: ${self.balance}")
                else:
                    print("Insufficient funds")
            else:
                print("Withdrawal amount must be positive")

        def display_info(self):
            print("Account Information:")
            print(f"Account Number: {self.account_number}")
            print(f"Account Type: {self.account_type}")
            print(f"Balance: ${self.balance:.2f}")

    # Second program
    print("\n===== BANK ACCOUNT CLASS DEMO =====")
    account = BankAccount("12345678", 1000, "Checking")
    account.display_info()
    account.deposit(500)
    account.withdraw(200)
    account.display_info()

    # AIM: Create a Person superclass with attributes for name and age, and a Student subclass that inherits from Person and adds an attribute for student ID and a method to display student information.
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def display_info(self):
            print("Name:", self.name)
            print("Age:", self.age)

    class Student(Person):
        def __init__(self, name, age, student_id):
            super().__init__(name, age)
            self.student_id = student_id

        def display_info(self):
            super().display_info()
            print("Student ID:", self.student_id)

    # Third program
    print("\n===== INHERITANCE DEMO =====")
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    student_id = input("Enter student ID: ")
    student = Student(name, age, student_id)
    student.display_info()