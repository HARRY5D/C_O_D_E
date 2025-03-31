"""
Database Operations with SQLite
Demonstrates basic database operations and implements a student management system
"""
import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_file):
        """Initialize database connection"""
        self.db_file = db_file
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to the database"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def execute_query(self, query, params=None):
        """Execute a query and commit changes"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return False
    
    def fetch_all(self, query, params=None):
        """Execute a query and fetch all results"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return []
    
    def fetch_one(self, query, params=None):
        """Execute a query and fetch one result"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return None

class StudentManagementSystem:
    def __init__(self):
        """Initialize the student management system"""
        self.db = DatabaseManager("students.db")
        if not self.db.connect():
            print("Failed to connect to database. Exiting...")
            return
        
        # Create students table if it doesn't exist
        self.db.execute_query('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            grade TEXT,
            email TEXT UNIQUE
        )
        ''')
    
    def add_student(self, name, age, grade, email):
        """Add a new student to the database"""
        try:
            query = "INSERT INTO students (name, age, grade, email) VALUES (?, ?, ?, ?)"
            params = (name, age, grade, email)
            if self.db.execute_query(query, params):
                print(f"Student '{name}' added successfully")
                return True
            return False
        except sqlite3.IntegrityError:
            print(f"Error: Email '{email}' already exists")
            return False
    
    def update_student(self, student_id, name=None, age=None, grade=None, email=None):
        """Update a student's details"""
        # Build the update query dynamically based on provided parameters
        updates = []
        params = []
        
        if name:
            updates.append("name = ?")
            params.append(name)
        if age:
            updates.append("age = ?")
            params.append(age)
        if grade:
            updates.append("grade = ?")
            params.append(grade)
        if email:
            updates.append("email = ?")
            params.append(email)
            
        if not updates:
            print("No updates provided")
            return False
            
        params.append(student_id)  # For the WHERE clause
        
        query = f"UPDATE students SET {', '.join(updates)} WHERE id = ?"
        
        if self.db.execute_query(query, params):
            print(f"Student with ID {student_id} updated successfully")
            return True
        return False
    
    def delete_student(self, student_id):
        """Delete a student from the database"""
        query = "DELETE FROM students WHERE id = ?"
        if self.db.execute_query(query, (student_id,)):
            print(f"Student with ID {student_id} deleted successfully")
            return True
        return False
    
    def display_all_students(self):
        """Display all students in the database"""
        query = "SELECT * FROM students ORDER BY name"
        students = self.db.fetch_all(query)
        
        if not students:
            print("No students found")
            return
            
        print("\n--- All Students ---")
        print("ID | Name | Age | Grade | Email")
        print("-" * 50)
        for student in students:
            print(f"{student[0]} | {student[1]} | {student[2]} | {student[3]} | {student[4]}")
        print("-" * 50)
    
    def search_students(self, search_term):
        """Search for students by name, grade, or email"""
        query = """
        SELECT * FROM students 
        WHERE name LIKE ? OR grade LIKE ? OR email LIKE ?
        ORDER BY name
        """
        params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
        students = self.db.fetch_all(query, params)
        
        if not students:
            print(f"No students found matching '{search_term}'")
            return
            
        print(f"\n--- Search Results for '{search_term}' ---")
        print("ID | Name | Age | Grade | Email")
        print("-" * 50)
        for student in students:
            print(f"{student[0]} | {student[1]} | {student[2]} | {student[3]} | {student[4]}")
        print("-" * 50)
    
    def close(self):
        """Close the database connection"""
        self.db.close()

# Online Bookstore System with DB Integration

class Book:
    def __init__(self, id=None, title=None, author=None, price=0.0, quantity=0):
        self.id = id
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity
    
    def __str__(self):
        return f"{self.title} by {self.author} - ${self.price:.2f}"

class Customer:
    def __init__(self, id=None, name=None, email=None):
        self.id = id
        self.name = name
        self.email = email
        self.order_history = []
    
    def __str__(self):
        return f"{self.name} ({self.email})"

class BookstoreSystem:
    def __init__(self):
        """Initialize the bookstore system"""
        self.db = DatabaseManager("bookstore.db")
        if not self.db.connect():
            print("Failed to connect to database. Exiting...")
            return
        
        # Create necessary tables
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        # Books table
        self.db.execute_query('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
        ''')
        
        # Customers table
        self.db.execute_query('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
        ''')
        
        # Orders table
        self.db.execute_query('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
        ''')
        
        # Order Items table
        self.db.execute_query('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
        ''')
    
    def add_book(self, title, author, price, quantity):
        """Add a new book to inventory"""
        try:
            query = "INSERT INTO books (title, author, price, quantity) VALUES (?, ?, ?, ?)"
            params = (title, author, price, quantity)
            if self.db.execute_query(query, params):
                print(f"Book '{title}' added successfully")
                return True
            return False
        except sqlite3.Error as e:
            print(f"Error adding book: {e}")
            return False
    
    def search_books(self, search_term):
        """Search for books by title or author"""
        query = """
        SELECT * FROM books
        WHERE title LIKE ? OR author LIKE ?
        ORDER BY title
        """
        params = (f"%{search_term}%", f"%{search_term}%")
        books = self.db.fetch_all(query, params)
        
        result = []
        for book_data in books:
            book = Book(
                id=book_data[0],
                title=book_data[1],
                author=book_data[2],
                price=book_data[3],
                quantity=book_data[4]
            )
            result.append(book)
        
        return result
    
    def display_all_books(self):
        """Display all books in inventory"""
        query = "SELECT * FROM books ORDER BY title"
        books = self.db.fetch_all(query)
        
        if not books:
            print("No books found in inventory")
            return
            
        print("\n--- Book Inventory ---")
        print("ID | Title | Author | Price | Quantity")
        print("-" * 60)
        for book in books:
            print(f"{book[0]} | {book[1]} | {book[2]} | ${book[3]:.2f} | {book[4]}")
        print("-" * 60)
    
    def add_customer(self, name, email):
        """Add a new customer"""
        try:
            query = "INSERT INTO customers (name, email) VALUES (?, ?)"
            params = (name, email)
            if self.db.execute_query(query, params):
                print(f"Customer '{name}' added successfully")
                return True
            return False
        except sqlite3.IntegrityError:
            print(f"Error: Email '{email}' already exists")
            return False
    
    def find_customer(self, email):
        """Find customer by email"""
        query = "SELECT * FROM customers WHERE email = ?"
        result = self.db.fetch_one(query, (email,))
        
        if result:
            customer = Customer(
                id=result[0],
                name=result[1],
                email=result[2]
            )
            return customer
        return None
    
    def place_order(self, customer_id, book_items):
        """Place an order
        
        Args:
            customer_id: Customer ID
            book_items: List of tuples (book_id, quantity)
        """
        try:
            # Calculate total amount and verify inventory
            total_amount = 0
            for book_id, qty in book_items:
                book_data = self.db.fetch_one(
                    "SELECT price, quantity FROM books WHERE id = ?", 
                    (book_id,)
                )
                
                if not book_data:
                    print(f"Book with ID {book_id} not found")
                    return False
                
                price, available = book_data
                
                if available < qty:
                    print(f"Not enough copies available for book ID {book_id}")
                    return False
                
                total_amount += price * qty
            
            # Create the order
            self.db.execute_query(
                "INSERT INTO orders (customer_id, total_amount) VALUES (?, ?)",
                (customer_id, total_amount)
            )
            
            # Get the last inserted order ID
            order_id = self.db.fetch_one("SELECT last_insert_rowid()")[0]
            
            # Add order items and update inventory
            for book_id, qty in book_items:
                book_data = self.db.fetch_one(
                    "SELECT price FROM books WHERE id = ?", 
                    (book_id,)
                )
                price = book_data[0]
                
                # Add order item
                self.db.execute_query(
                    "INSERT INTO order_items (order_id, book_id, quantity, price) VALUES (?, ?, ?, ?)",
                    (order_id, book_id, qty, price)
                )
                
                # Update inventory
                self.db.execute_query(
                    "UPDATE books SET quantity = quantity - ? WHERE id = ?",
                    (qty, book_id)
                )
            
            print(f"Order placed successfully. Order ID: {order_id}, Total: ${total_amount:.2f}")
            return True
            
        except sqlite3.Error as e:
            print(f"Error placing order: {e}")
            return False
    
    def get_customer_orders(self, customer_id):
        """Get all orders for a customer"""
        query = "SELECT * FROM orders WHERE customer_id = ? ORDER BY order_date DESC"
        orders = self.db.fetch_all(query, (customer_id,))
        
        if not orders:
            print("No orders found for this customer")
            return []
            
        result = []
        for order in orders:
            order_id = order[0]
            order_date = order[2]
            total = order[3]
            
            # Get order items
            items_query = """
            SELECT oi.book_id, b.title, oi.quantity, oi.price
            FROM order_items oi
            JOIN books b ON oi.book_id = b.id
            WHERE oi.order_id = ?
            """
            items = self.db.fetch_all(items_query, (order_id,))
            
            result.append({
                'order_id': order_id,
                'date': order_date,
                'total': total,
                'items': items
            })
        
        return result
    
    def export_inventory(self, filename):
        """Export book inventory to a text file"""
        try:
            books = self.db.fetch_all("SELECT * FROM books")
            
            with open(filename, 'w') as f:
                f.write("ID|Title|Author|Price|Quantity\n")
                for book in books:
                    f.write(f"{book[0]}|{book[1]}|{book[2]}|{book[3]}|{book[4]}\n")
            
            print(f"Inventory exported to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting inventory: {e}")
            return False
    
    def import_inventory(self, filename):
        """Import book inventory from a text file"""
        try:
            if not os.path.exists(filename):
                print(f"File {filename} not found")
                return False
                
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            # Skip header line
            for i, line in enumerate(lines[1:], 1):
                try:
                    data = line.strip().split('|')
                    if len(data) != 5:
                        print(f"Invalid data format on line {i+1}")
                        continue
                        
                    # Check if book ID already exists
                    book_id = int(data[0])
                    existing = self.db.fetch_one(
                        "SELECT id FROM books WHERE id = ?", 
                        (book_id,)
                    )
                    
                    if existing:
                        # Update existing book
                        self.db.execute_query(
                            "UPDATE books SET title=?, author=?, price=?, quantity=? WHERE id=?",
                            (data[1], data[2], float(data[3]), int(data[4]), book_id)
                        )
                    else:
                        # Insert new book
                        self.db.execute_query(
                            "INSERT INTO books (id, title, author, price, quantity) VALUES (?, ?, ?, ?, ?)",
                            (book_id, data[1], data[2], float(data[3]), int(data[4]))
                        )
                    
                except Exception as e:
                    print(f"Error processing line {i+1}: {e}")
            
            print(f"Inventory imported from {filename}")
            return True
        except Exception as e:
            print(f"Error importing inventory: {e}")
            return False
    
    def close(self):
        """Close the database connection"""
        self.db.close()

def run_student_system():
    """Run the student management system"""
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    sms = StudentManagementSystem()
    
    # Add sample students
    sms.add_student("John Doe", 20, "A", "john@example.com")
    sms.add_student("Jane Smith", 19, "B", "jane@example.com")
    sms.add_student("Bob Johnson", 21, "A", "bob@example.com")
    
    # Display all students
    sms.display_all_students()
    
    # Update a student
    sms.update_student(1, grade="A+")
    
    # Search for students
    sms.search_students("John")
    
    # Delete a student
    sms.delete_student(3)
    
    # Display all students again
    sms.display_all_students()
    
    sms.close()

def run_bookstore_system():
    """Run the bookstore system"""
    print("\n===== ONLINE BOOKSTORE SYSTEM =====")
    bookstore = BookstoreSystem()
    
    # Add sample books
    bookstore.add_book("Python Programming", "John Smith", 29.99, 10)
    bookstore.add_book("Database Systems", "Alice Johnson", 39.99, 5)
    bookstore.add_book("Web Development", "Bob Brown", 24.99, 8)
    
    # Display all books
    bookstore.display_all_books()
    
    # Search for books
    print("\nSearching for 'Python':")
    python_books = bookstore.search_books("Python")
    for book in python_books:
        print(book)
    
    # Add a customer
    bookstore.add_customer("Mary Williams", "mary@example.com")
    
    # Place an order
    print("\nPlacing an order:")
    # Order: 2 copies of "Python Programming" and 1 copy of "Web Development"
    bookstore.place_order(1, [(1, 2), (3, 1)])
    
    # Export inventory
    bookstore.export_inventory("inventory.txt")
    
    # Display customer orders
    print("\nCustomer order history:")
    orders = bookstore.get_customer_orders(1)
    for order in orders:
        print(f"Order #{order['order_id']} - Date: {order['date']}, Total: ${order['total']:.2f}")
        print("Items:")
        for item in order['items']:
            print(f"  - {item[1]}: {item[2]} x ${item[3]:.2f}")
    
    bookstore.close()

def main():
    print("===== DATABASE OPERATIONS DEMO =====")
    
    # Run student management system
    run_student_system()
    
    # Run bookstore system
    run_bookstore_system()
    
    print("\nDemonstration complete.")

if __name__ == "__main__":
    main()