import sqlite3
from datetime import datetime

class StudentDB:
    def __init__(self, db_name="students.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_table()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Successfully connected to {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll_number TEXT UNIQUE,
                    name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    created_at TEXT
                )
            ''')
            self.connection.commit()
            print("Table 'students' is ready")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def add_student(self, roll_number, name, age, gender):
        try:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute('''
                INSERT INTO students 
                (roll_number, name, age, gender, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (roll_number, name, age, gender, created_at))
            self.connection.commit()
            print(f"Student {name} added successfully with Roll No: {roll_number}")
            return True
        except sqlite3.IntegrityError:
            print(f"Error: Roll number {roll_number} already exists")
            return False
        except sqlite3.Error as e:
            print(f"Error adding student: {e}")
            return False

    def update_student(self, roll_number, **kwargs):
        try:
            self.cursor.execute("SELECT id FROM students WHERE roll_number = ?", (roll_number,))
            if not self.cursor.fetchone():
                print(f"Student with roll number {roll_number} not found")
                return False

            if not kwargs:
                print("No fields provided for update")
                return False

            set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
            query = f"UPDATE students SET {set_clause} WHERE roll_number = ?"
            
            values = list(kwargs.values())
            values.append(roll_number)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"Student with roll number {roll_number} updated successfully")
                return True
            else:
                print(f"No changes made to student with roll number {roll_number}")
                return False
                
        except sqlite3.Error as e:
            print(f"Error updating student: {e}")
            return False

    def delete_student(self, roll_number):
        try:
            self.cursor.execute("DELETE FROM students WHERE roll_number = ?", (roll_number,))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"Student with roll number {roll_number} deleted successfully")
                return True
            else:
                print(f"Student with roll number {roll_number} not found")
                return False
                
        except sqlite3.Error as e:
            print(f"Error deleting student: {e}")
            return False

    def get_all_students(self):
        try:
            self.cursor.execute("SELECT * FROM students ORDER BY name")
            students = self.cursor.fetchall()
            return students
        except sqlite3.Error as e:
            print(f"Error retrieving students: {e}")
            return []

    def search_students(self, field, value):
        try:
            valid_fields = ["roll_number", "name", "age", "gender"]
            if field not in valid_fields:
                print(f"Invalid search field: {field}")
                return []
                
            query = f"SELECT * FROM students WHERE {field} LIKE ?"
            self.cursor.execute(query, (f"%{value}%",))
            students = self.cursor.fetchall()
            return students
        except sqlite3.Error as e:
            print(f"Error searching students: {e}")
            return []

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed")


def display_students(students):
    if not students:
        print("No students found")
        return
        
    print("\nRoll No  Name  Age  Gender")
    print("________________________________")
    for student in students:
        roll_number, name, age, gender = student[1:5]
        
        print(f"{roll_number:<8} {name:<15} {age:<5} {gender:<6}")

def main_menu():
    db = StudentDB()
    
    while True:
        print("\n==== STUDENT MANAGEMENT SYSTEM ====")
        print("1. Add New Student")
        print("2. Update Student Record")
        print("3. Delete Student Record")
        print("4. Display All Students")
        print("5. Search Students")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            add_student_menu(db)
        elif choice == '2':
            update_student_menu(db)
        elif choice == '3':
            delete_student_menu(db)
        elif choice == '4':
            students = db.get_all_students()
            display_students(students)
        elif choice == '5':
            search_students_menu(db)
        elif choice == '6':
            db.close()
            print("Thank you for using Student Management System!")
            break
        else:
            print("Invalid choice. Please try again.")


def add_student_menu(db):
    print("\n--- Add New Student ---")
    
    roll_number = input("Enter Roll Number: ")
    name = input("Enter Name: ")
    
    while True:
        try:
            age = int(input("Enter Age: "))
            if 0 <= age <= 120:
                break
            else:
                print("Please enter a valid age between 0 and 120")
        except ValueError:
            print("Please enter a valid number for age")
    
    gender = input("Enter Gender (M/F/Other): ").upper()
    
    db.add_student(roll_number, name, age, gender)


def update_student_menu(db):
    print("\n--- Update Student Record ---")
    
    roll_number = input("Enter Roll Number of student to update: ")
    
    print("Leave field empty if you don't want to update it")
    name = input("Enter New Name (or press Enter to skip): ")
    
    age = None
    age_input = input("Enter New Age (or press Enter to skip): ")
    if age_input:
        try:
            age = int(age_input)
        except ValueError:
            print("Invalid age, this field will not be updated")
    
    gender = input("Enter New Gender (or press Enter to skip): ")
    
    updates = {}
    if name:
        updates["name"] = name
    if age is not None:
        updates["age"] = age
    if gender:
        updates["gender"] = gender
    
    db.update_student(roll_number, **updates)


def delete_student_menu(db):
    print("\n--- Delete Student Record ---")
    
    roll_number = input("Enter Roll Number of student to delete: ")
    confirm = input(f"Are you sure you want to delete student with roll number {roll_number}? (y/n): ")
    
    if confirm.lower() == 'y':
        db.delete_student(roll_number)
    else:
        print("Deletion cancelled")


def search_students_menu(db):
    print("\n--- Search Students ---")
    print("1. Search by Roll Number")
    print("2. Search by Name")
    print("3. Search by Gender")
    print("4. Return to Main Menu")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == '4':
        return
    
    field_mapping = {
        '1': 'roll_number',
        '2': 'name',
        '3': 'gender'
    }
    
    if choice in field_mapping:
        field = field_mapping[choice]
        value = input(f"Enter {field.replace('_', ' ')} to search for: ")
        students = db.search_students(field, value)
        display_students(students)
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main_menu()