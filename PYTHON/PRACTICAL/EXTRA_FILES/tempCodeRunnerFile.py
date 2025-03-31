
# class BookstoreItem:
#     """Base class for items sold in bookstore"""
#     def __init__(self, title, author, price, item_id):
#         self.title = title
#         self.author = author
#         self.price = price
#         self.item_id = item_id
    
#     def get_details(self):
#         """Return item details"""
#         return f"{self.title} by {self.author} - ${self.price}"
    
#     def calculate_price(self, quantity=1):
#         """Calculate price based on quantity"""
#         return self.price * quantity

# class PrintedBook(BookstoreItem):
#     """Class for physical books"""
#     def __init__(self, title, author, price, item_id, shipping_weight):
#         super().__init__(title, author, price, item_id)
#         self.shipping_weight = shipping_weight
#         self.format = "Printed"
    
#     def calculate_price(self, quantity=1):
#         """Override to include shipping cost based on weight"""
#         base_price = super().calculate_price(quantity)
#         shipping_cost = self.shipping_weight * 2 * quantity
#         return base_price + shipping_cost
    
#     def get_details(self):
#         """Override to include format"""
#         return f"{super().get_details()} (Printed, Weight: {self.shipping_weight}kg)"

# class EBook(BookstoreItem):
#     """Class for digital books"""
#     def __init__(self, title, author, price, item_id, file_size):
#         super().__init__(title, author, price, item_id)
#         self.file_size = file_size
#         self.format = "Digital"
    
#     def calculate_price(self, quantity=1):
#         """Override for digital pricing (no shipping but adds tax)"""
#         base_price = super().calculate_price(quantity)
#         digital_tax = base_price * 0.05  # 5% digital tax
#         return base_price + digital_tax
    
#     def get_details(self):
#         """Override to include format"""
#         return f"{super().get_details()} (E-Book, Size: {self.file_size}MB)"

# class Customer:
#     """Class to manage customer information"""
#     def __init__(self, customer_id, name, email):
#         self.customer_id = customer_id
#         self.name = name
#         self.__email = email  # Private attribute
#         self.__payment_info = None  # Private attribute
#         self.order_history = []
    
#     def add_payment_info(self, payment_info):
#         """Set payment information securely"""
#         self.__payment_info = payment_info
    
#     def get_email(self):
#         """Getter for email"""
#         return self.__email

# class Order:
#     """Class to manage customer orders"""
#     order_count = 0  # Class variable to track total orders
    
#     def __init__(self, customer):
#         Order.order_count += 1
#         self.order_id = f"ORD-{Order.order_count}"
#         self.customer = customer
#         self.items = []
#         self.status = "Pending"
    
#     def add_item(self, book, quantity=1):
#         """Add book to order"""
#         self.items.append({"book": book, "quantity": quantity})
    
#     def calculate_total(self):
#         """Calculate total price of order"""
#         total = 0
#         for item in self.items:
#             total += item["book"].calculate_price(item["quantity"])
#         return total
    
#     def complete_order(self):
#         """Mark order as complete and add to customer history"""
#         self.status = "Complete"
#         self.customer.order_history.append(self)
#         return f"Order {self.order_id} completed. Total: ${self.calculate_total():.2f}"
    
#     @classmethod
#     def get_total_orders(cls):
#         """Class method to return total number of orders"""
#         return cls.order_count

# class Bookstore:
#     """Main class to manage the bookstore"""
#     def __init__(self, name):
#         self.name = name
#         self.inventory = []
#         self.customers = []
#         self.orders = []
    
#     def add_book(self, book):
#         """Add a book to inventory"""
#         self.inventory.append(book)
    
#     def add_customer(self, customer):
#         """Register a customer"""
#         self.customers.append(customer)
    
#     def place_order(self, order):
#         """Process a new order"""
#         self.orders.append(order)
#         return order.complete_order()
    
#     def get_total_revenue(self):
#         """Calculate total revenue from all completed orders"""
#         total = 0
#         for order in self.orders:
#             if order.status == "Complete":
#                 total += order.calculate_total()
#         return total
    
#     def search_books(self, keyword):
#         """Search inventory by title or author"""
#         results = []
#         for book in self.inventory:
#             if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower():
#                 results.append(book)
#         return results

# # Demo function to test all the classes
# def run_demo():
#     print("\n===== OOP CONCEPTS DEMONSTRATION =====\n")
    
#     # Demonstrate polymorphism with shapes
#     circle = Circle(5)
#     rectangle = Rectangle(4, 6)
    
#     shapes = [circle, rectangle]
#     for shape in shapes:
#         print(f"{shape.name} area: {shape.calculate_area()}")
    
#     # Demonstrate encapsulation with Book class
#     book = Book("Python Programming", "John Smith", "1234567890123")
#     print(f"\nBook details: {book.get_title()} by {book.get_author()}")
#     book.set_author("Jane Doe")  # Change the author
#     print(f"Updated author: {book.get_author()}")
    
#     # Demonstrate method overloading
#     calc = Calculator()
#     print(f"\nCalculator.add(5): {calc.add(5)}")
#     print(f"Calculator.add(5, 3): {calc.add(5, 3)}")
#     print(f"Calculator.add(5, 3, 2): {calc.add(5, 3, 2)}")
    
#     # Demonstrate class and static methods
#     print(f"\nDefault Pi: {MathOperations.pi}")
#     MathOperations.change_pi(3.14159)
#     print(f"Updated Pi: {MathOperations.pi}")
#     print(f"Is 7 prime? {MathOperations.is_prime(7)}")
    
#     # Demonstrate property decorator
#     temp = Temperature(25)
#     print(f"\nTemperature in Celsius: {temp.celsius}°C")
#     print(f"Temperature in Fahrenheit: {temp.fahrenheit}°F")
#     temp.fahrenheit = 104
#     print(f"Updated Celsius: {temp.celsius}°C")
    
#     print("\n===== BOOKSTORE SYSTEM DEMONSTRATION =====\n")
    
#     # Create bookstore
#     store = Bookstore("Python Bookstore")
    
#     # Add books to inventory
#     book1 = PrintedBook("Python Basics", "John Smith", 29.99, "B001", 0.5)
#     book2 = EBook("Advanced Python", "Jane Doe", 19.99, "E001", 15)
#     store.add_book(book1)
#     store.add_book(book2)
    
#     # Register customer
#     customer1 = Customer(1, "Alice", "alice@example.com")
#     store.add_customer(customer1)
    
#     # Place an order
#     order1 = Order(customer1)
#     order1.add_item(book1, 2)
#     order1.add_item(book2, 1)
    
#     # Complete the order
#     result = store.place_order(order1)
#     print(result)
    
#     # Check inventory
#     print("\nBookstore Inventory:")
#     for book in store.inventory:
#         print(f"- {book.get_details()}")
    
#     # Search for books
#     print("\nSearch results for 'Python':")
#     for book in store.search_books("Python"):
#         print(f"- {book.get_details()}")
    
#     # Check revenue
#     print(f"\nTotal bookstore revenue: ${store.get_total_revenue():.2f}")
#     print(f"Total orders processed: {Order.get_total_orders()}")

# # Run the demo
# if __name__ == "__main__":
#     run_demo()