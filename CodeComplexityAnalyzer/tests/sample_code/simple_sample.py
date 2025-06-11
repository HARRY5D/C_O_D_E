"""
Simple Python code with low complexity for testing.
"""


def add_numbers(a, b):
    """Add two numbers together."""
    return a + b


def multiply_numbers(a, b):
    """Multiply two numbers."""
    return a * b


def greet_user(name):
    """Greet a user by name."""
    return f"Hello, {name}!"


def calculate_area(length, width):
    """Calculate the area of a rectangle."""
    return length * width


def is_even(number):
    """Check if a number is even."""
    return number % 2 == 0


class SimpleCalculator:
    """A simple calculator class."""
    
    def __init__(self):
        """Initialize the calculator."""
        self.result = 0
    
    def add(self, value):
        """Add a value to the result."""
        self.result += value
        return self.result
    
    def subtract(self, value):
        """Subtract a value from the result."""
        self.result -= value
        return self.result
    
    def multiply(self, value):
        """Multiply the result by a value."""
        self.result *= value
        return self.result
    
    def divide(self, value):
        """Divide the result by a value."""
        if value != 0:
            self.result /= value
        return self.result
    
    def clear(self):
        """Clear the result."""
        self.result = 0
        return self.result


def format_currency(amount):
    """Format a number as currency."""
    return f"${amount:.2f}"


def get_file_extension(filename):
    """Get the extension of a filename."""
    return filename.split('.')[-1] if '.' in filename else ''


def reverse_string(text):
    """Reverse a string."""
    return text[::-1]


def count_words(text):
    """Count the number of words in a text."""
    return len(text.split())
