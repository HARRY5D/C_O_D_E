class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def __add__(self, other):
        """Overload the + operator to add quantities of same product"""
        if self.name == other.name and self.price == other.price:
            return Product(self.name, self.price, self.quantity + other.quantity)
        else:
            raise ValueError("Can only add products with the same name and price")
    
    def __str__(self):
        return f"Product: {self.name}, Price: ${self.price}, Quantity: {self.quantity}"


product1 = Product("Watch", 999.99, 5)
product2 = Product("Watch", 999.99, 3)
product3 = Product("Smartphone", 599.99, 10)

combined_product = product1 + product2
print(product1)
print(product2)
print(combined_product)

try:
    # This should raise an error
    invalid_combination = product1 + product3
except ValueError as e:
    print(f"Error: {e}")