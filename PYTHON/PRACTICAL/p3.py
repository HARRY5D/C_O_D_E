# """
# Python Functions and Loops Assignment
# This module demonstrates various function concepts and loop operations
# as specified in the assignment.
# """
# from typing import List, Dict, Tuple, Any, Callable, Optional
# import functools

# # ---------- FUNCTION BASICS ----------

# # Simple function with inputs and output
# def add(a: float, b: float) -> float:
#     """Add two numbers and return the result."""
#     return a + b

# # Function with different argument types
# def greet(name: str, 
#           greeting: str = "Hello", 
#           *additional_msgs: str, 
#           caps: bool = False, 
#           **custom_params: Any) -> str:
#     """
#     Greet someone with customizable parameters.
    
#     Args:
#         name: The name of the person to greet
#         greeting: The greeting to use (default: "Hello")
#         *additional_msgs: Any additional messages
#         caps: Whether to capitalize the output (default: False)
#         **custom_params: Any additional keyword arguments
    
#     Returns:
#         A formatted greeting string
#     """
#     result = f"{greeting}, {name}!"
    
#     if additional_msgs:
#         result += " " + " ".join(additional_msgs)
    
#     if custom_params:
#         for key, value in custom_params.items():
#             result += f"\n{key}: {value}"
            
#     if caps:
#         return result.upper()
        
#     return result

# # Function returning multiple values
# def calculate_stats(numbers: List[float]) -> Tuple[float, float, float, float]:
#     """
#     Calculate statistics for a list of numbers.
    
#     Args:
#         numbers: List of numbers
        
#     Returns:
#         Tuple containing (minimum, maximum, sum, average)
#     """
#     total = sum(numbers)
#     avg = total / len(numbers) if numbers else 0
#     min_val = min(numbers) if numbers else 0
#     max_val = max(numbers) if numbers else 0
    
#     return min_val, max_val, total, avg

# # Lambda function example
# square = lambda x: x * x

# # Function inside another function
# def create_multiplier(factor: float) -> Callable:
#     """
#     Create a function that multiplies its argument by a specified factor.
    
#     Args:
#         factor: The multiplication factor
        
#     Returns:
#         A function that multiplies its argument by the factor
#     """
#     def multiplier(x: float) -> float:
#         """Multiply x by the factor."""
#         return x * factor
    
#     return multiplier

# # Decorator example
# def log_execution(func: Callable) -> Callable:
#     """
#     Decorator that logs the execution of a function.
    
#     Args:
#         func: The function to decorate
        
#     Returns:
#         Decorated function
#     """
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         print(f"Executing {func.__name__} with args: {args}, kwargs: {kwargs}")
#         result = func(*args, **kwargs)
#         print(f"{func.__name__} returned: {result}")
#         return result
    
#     return wrapper

# # Recursive function
# def factorial(n: int) -> int:
#     """
#     Calculate the factorial of n recursively.
    
#     Args:
#         n: The number to calculate factorial for
        
#     Returns:
#         The factorial of n
#     """
#     if n <= 1:
#         return 1
#     return n * factorial(n - 1)

# # ---------- LOOPS BASICS ----------

# def demonstrate_loops() -> None:
#     """Demonstrate various loop techniques."""
#     # Simple for loop with range
#     for i in range(5):
#         print(f"Count: {i}")
    
#     # Loop with enumerate
#     fruits = ["apple", "banana", "cherry"]
#     for index, fruit in enumerate(fruits):
#         print(f"Fruit {index}: {fruit}")
    
#     # While loop
#     counter = 0
#     while counter < 5:
#         print(f"While count: {counter}")
#         counter += 1
    
#     # Loop control statements
#     for i in range(10):
#         if i == 3:
#             continue  # Skip 3
#         if i == 7:
#             break     # Stop at 7
#         print(f"Controlled loop: {i}")
    
#     # Nested loops
#     for i in range(3):
#         for j in range(2):
#             print(f"Nested: ({i}, {j})")
    
#     # Dictionary loop
#     person = {"name": "John", "age": 30, "city": "New York"}
#     for key, value in person.items():
#         print(f"{key}: {value}")
    
#     # List comprehension
#     squares = [x*x for x in range(1, 6)]
#     print(f"Squares using comprehension: {squares}")

# # ---------- ASSIGNMENT TASKS ----------

# # 1. Basic Calculator
# class Calculator:
#     """A basic calculator with addition, subtraction, multiplication, and division."""
    
#     @staticmethod
#     def add(a: float, b: float) -> float:
#         """Add two numbers."""
#         return a + b
    
#     @staticmethod
#     def subtract(a: float, b: float) -> float:
#         """Subtract b from a."""
#         return a - b
    
#     @staticmethod
#     def multiply(a: float, b: float) -> float:
#         """Multiply two numbers."""
#         return a * b
    
#     @staticmethod
#     def divide(a: float, b: float) -> Optional[float]:
#         """Divide a by b. Returns None if b is zero."""
#         if b == 0:
#             print("Error: Division by zero")
#             return None
#         return a / b

# # 2. Fibonacci sequence
# def fibonacci(n: int) -> List[int]:
#     """
#     Generate Fibonacci sequence up to n terms.
    
#     Args:
#         n: Number of terms to generate
        
#     Returns:
#         List containing the Fibonacci sequence
#     """
#     if n <= 0:
#         return []
#     if n == 1:
#         return [0]
    
#     sequence = [0, 1]
#     for i in range(2, n):
#         sequence.append(sequence[i-1] + sequence[i-2])
    
#     return sequence

# # 3. List operations
# def find_max(numbers: List[float]) -> float:
#     """Find the maximum value in a list without using max()."""
#     if not numbers:
#         return float('-inf')
    
#     max_val = numbers[0]
#     for num in numbers[1:]:
#         if num > max_val:
#             max_val = num
    
#     return max_val

# def find_min(numbers: List[float]) -> float:
#     """Find the minimum value in a list without using min()."""
#     if not numbers:
#         return float('inf')
    
#     min_val = numbers[0]
#     for num in numbers[1:]:
#         if num < min_val:
#             min_val = num
    
#     return min_val

# # 4. Dictionary operations
# def dict_operations() -> Dict:
#     """Demonstrate dictionary operations."""
#     # Create a dictionary
#     student = {"name": "Alice", "age": 20}
    
#     # Add a key-value pair
#     student["grade"] = "A"
    
#     # Update a value
#     student["age"] = 21
    
#     # Merge with another dictionary
#     additional_info = {"major": "Computer Science", "year": 2}
#     student.update(additional_info)
    
#     # Delete a key-value pair
#     if "year" in student:
#         del student["year"]
    
#     # Display dictionary contents
#     for key, value in student.items():
#         print(f"{key}: {value}")
    
#     return student

# # 5. To-do list application
# class TodoList:
#     """A simple to-do list application."""
    
#     def __init__(self):
#         """Initialize an empty to-do list."""
#         self.tasks = []
    
#     def add_task(self, task: str) -> None:
#         """Add a task to the list."""
#         self.tasks.append(task)
#         print(f"Task added: {task}")
    
#     def remove_task(self, task: str) -> bool:
#         """
#         Remove a task from the list.
        
#         Returns:
#             True if the task was removed, False otherwise
#         """
#         if task in self.tasks:
#             self.tasks.remove(task)
#             print(f"Task removed: {task}")
#             return True
#         else:
#             print(f"Task not found: {task}")
#             return False
    
#     def view_tasks(self) -> None:
#         """Display all tasks in the list."""
#         if not self.tasks:
#             print("No tasks available.")
#             return
        
#         print("\n===== TO-DO LIST =====")
#         for index, task in enumerate(self.tasks, 1):
#             print(f"{index}. {task}")
#         print("=====================\n")

# # 6. Filter even numbers
# def filter_even_numbers(numbers: List[int]) -> List[int]:
#     """
#     Filter a list to contain only even numbers.
    
#     Args:
#         numbers: List of integers
        
#     Returns:
#         List containing only the even integers
#     """
#     return [num for num in numbers if num % 2 == 0]

# # ---------- MAIN EXECUTION ----------

# def main():
#     """Main function to demonstrate all functionality."""
#     print("\n===== FUNCTION DEMONSTRATIONS =====")
    
#     # Demonstrate basic function
#     print(f"Addition: 5 + 3 = {add(5, 3)}")
    
#     # Demonstrate different argument types
#     print("\nGreeting examples:")
#     print(greet("Alice"))
#     print(greet("Bob", "Hi", caps=True))
#     print(greet("Charlie", "Welcome", "Nice to see you", "Have a great day", role="Student", status="Active"))
    
#     # Demonstrate multiple return values
#     numbers = [1, 2, 3, 4, 5]
#     min_val, max_val, total, avg = calculate_stats(numbers)
#     print(f"\nStatistics for {numbers}:")
#     print(f"Min: {min_val}, Max: {max_val}, Sum: {total}, Average: {avg}")
    
#     # Demonstrate lambda function
#     print(f"\nSquare of 7: {square(7)}")
    
#     # Demonstrate function factory
#     double = create_multiplier(2)
#     triple = create_multiplier(3)
#     print(f"Double 5: {double(5)}")
#     print(f"Triple 5: {triple(5)}")
    
#     # Demonstrate decorator
#     @log_execution
#     def add_decorated(a, b):
#         return a + b
    
#     print("\nDecorator example:")
#     add_decorated(3, 4)
    
#     # Demonstrate recursion
#     print(f"\nFactorial of 5: {factorial(5)}")
    
#     # Demonstrate loops
#     print("\n===== LOOP DEMONSTRATIONS =====")
#     demonstrate_loops()
    
#     # Demonstrate calculator
#     print("\n===== CALCULATOR DEMONSTRATION =====")
#     calc = Calculator()
#     print(f"Addition: 10 + 5 = {calc.add(10, 5)}")
#     print(f"Subtraction: 10 - 5 = {calc.subtract(10, 5)}")
#     print(f"Multiplication: 10 * 5 = {calc.multiply(10, 5)}")
#     print(f"Division: 10 / 5 = {calc.divide(10, 5)}")
#     print(f"Division by zero: {calc.divide(10, 0)}")
    
#     # Demonstrate Fibonacci
#     print("\n===== FIBONACCI DEMONSTRATION =====")
#     fib_sequence = fibonacci(10)
#     print(f"First 10 Fibonacci numbers: {fib_sequence}")
    
#     # Demonstrate list operations
#     print("\n===== LIST OPERATIONS DEMONSTRATION =====")
#     sample_list = [23, 45, 12, 67, 9, 34]
#     print(f"List: {sample_list}")
#     print(f"Max value (custom): {find_max(sample_list)}")
#     print(f"Min value (custom): {find_min(sample_list)}")
    
#     # Demonstrate dictionary operations
#     print("\n===== DICTIONARY OPERATIONS DEMONSTRATION =====")
#     student_dict = dict_operations()
    
#     # Demonstrate to-do list
#     print("\n===== TO-DO LIST DEMONSTRATION =====")
#     todo = TodoList()
#     todo.add_task("Complete Python assignment")
#     todo.add_task("Study for exam")
#     todo.add_task("Go grocery shopping")
#     todo.view_tasks()
#     todo.remove_task("Study for exam")
#     todo.view_tasks()
    
#     # Demonstrate even number filter
#     print("\n===== FILTER EVEN NUMBERS DEMONSTRATION =====")
#     num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#     even_nums = filter_even_numbers(num_list)
#     print(f"Original list: {num_list}")
#     print(f"Even numbers: {even_nums}")

# if __name__ == "__main__":
#     main()

"""
Python Functions and Loops Assignment
Simplified implementation covering all requirements
"""

# ---------- FUNCTION BASICS ----------

# Simple function
def add(a, b):
    """Add two numbers and return the result."""
    return a + b

# Function with different argument types
def greet(name, greeting="Hello", *extra_msgs, caps=False, **other_params):
    """Customizable greeting function."""
    result = f"{greeting}, {name}!"
    
    if extra_msgs:
        result += " " + " ".join(extra_msgs)
    
    if other_params:
        for key, value in other_params.items():
            result += f"\n{key}: {value}"
            
    return result.upper() if caps else result

# Multiple return values
def calculate_stats(numbers):
    """Return min, max, sum and average of numbers."""
    if not numbers:
        return 0, 0, 0, 0
    total = sum(numbers)
    return min(numbers), max(numbers), total, total/len(numbers)

# Lambda function
square = lambda x: x * x

# Function inside function
def create_multiplier(factor):
    """Return a function that multiplies by factor."""
    def multiply(x):
        return x * factor
    return multiply

# Decorator
def log_execution(func):
    """Log function execution details."""
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Result: {result}")
        return result
    return wrapper

# Recursive function
def factorial(n):
    """Calculate factorial recursively."""
    return 1 if n <= 1 else n * factorial(n-1)

# ---------- LOOPS BASICS ----------

def demonstrate_loops():
    """Show various loop techniques."""
    # For loop
    print("\nFor loop:")
    for i in range(3):
        print(f"Count: {i}")
    
    # With enumerate
    print("\nEnumerate:")
    fruits = ["apple", "banana", "cherry"]
    for i, fruit in enumerate(fruits):
        print(f"Fruit {i}: {fruit}")
    
    # While loop
    print("\nWhile loop:")
    i = 0
    while i < 3:
        print(f"While: {i}")
        i += 1
    
    # Break and continue
    print("\nBreak and continue:")
    for i in range(5):
        if i == 1: continue
        if i == 4: break
        print(f"Value: {i}")
    
    # Dictionary loop
    print("\nDictionary loop:")
    person = {"name": "John", "age": 30}
    for k, v in person.items():
        print(f"{k}: {v}")
    
    # List comprehension
    print("\nList comprehension:")
    squares = [x**2 for x in range(1, 5)]
    print(f"Squares: {squares}")

# ---------- ASSIGNMENT TASKS ----------

# Basic calculator
class Calculator:
    """Simple calculator with basic operations."""
    
    @staticmethod
    def add(a, b):
        return a + b
    
    @staticmethod
    def subtract(a, b):
        return a - b
    
    @staticmethod
    def multiply(a, b):
        return a * b
    
    @staticmethod
    def divide(a, b):
        if b == 0:
            print("Error: Division by zero")
            return None
        return a / b

# Fibonacci sequence
def fibonacci(n):
    """Generate Fibonacci sequence up to n terms."""
    if n <= 0: return []
    if n == 1: return [0]
    
    seq = [0, 1]
    for i in range(2, n):
        seq.append(seq[i-1] + seq[i-2])
    return seq

# List operations without built-ins
def find_max(numbers):
    """Find maximum without using max()."""
    if not numbers: return None
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

def find_min(numbers):
    """Find minimum without using min()."""
    if not numbers: return None
    min_val = numbers[0]
    for num in numbers:
        if num < min_val:
            min_val = num
    return min_val

# Dictionary operations
def dict_operations():
    """Demonstrate dictionary operations."""
    # Create and manipulate
    student = {"name": "Alice", "age": 20}
    student["grade"] = "A"  # Add
    student["age"] = 21     # Update
    
    # Merge dictionaries
    more_info = {"major": "Computer Science"}
    student.update(more_info)
    
    # Display
    for k, v in student.items():
        print(f"{k}: {v}")
    
    return student

# To-do list
class TodoList:
    """Simple to-do list application."""
    
    def __init__(self):
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)
        print(f"Added: {task}")
    
    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            print(f"Removed: {task}")
            return True
        print(f"Not found: {task}")
        return False
    
    def view_tasks(self):
        if not self.tasks:
            print("No tasks.")
            return
        print("\n--- TASKS ---")
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task}")
        print("------------\n")

# Filter even numbers
def filter_even_numbers(numbers):
    """Return only even numbers from a list."""
    return [n for n in numbers if n % 2 == 0]

# ---------- MAIN EXECUTION ----------

def main():
    # Basic function demo
    print(f"Addition: 5 + 3 = {add(5, 3)}")
    
    # Greet function demo
    print("\nGreeting examples:")
    print(greet("Alice"))
    print(greet("Bob", "Hi", caps=True))
    print(greet("Charlie", "Welcome", "Nice day", role="Student"))
    
    # Return multiple values
    numbers = [1, 2, 3, 4, 5]
    min_val, max_val, total, avg = calculate_stats(numbers)
    print(f"\nStats: Min={min_val}, Max={max_val}, Sum={total}, Avg={avg}")
    
    # Lambda and nested function
    print(f"Square of 7: {square(7)}")
    double = create_multiplier(2)
    print(f"Double 5: {double(5)}")
    
    # Decorator
    @log_execution
    def test_func(a, b):
        return a + b
    
    print("\nDecorator test:")
    test_func(10, 20)
    
    # Recursion
    print(f"\nFactorial of 5: {factorial(5)}")
    
    # Loops demo
    demonstrate_loops()
    
    # Calculator
    calc = Calculator()
    print(f"\nCalculator: 10 + 5 = {calc.add(10, 5)}")
    print(f"Calculator: 10 / 0 = {calc.divide(10, 0)}")
    
    # Fibonacci
    print(f"\nFibonacci(8): {fibonacci(8)}")
    
    # List operations
    data = [23, 45, 12, 67, 9]
    print(f"\nMax of {data}: {find_max(data)}")
    print(f"Min of {data}: {find_min(data)}")
    
    # Dictionary operations
    print("\nDictionary operations:")
    dict_operations()
    
    # Todo list
    print("\nTodo list:")
    todo = TodoList()
    todo.add_task("Do homework")
    todo.add_task("Buy groceries")
    todo.view_tasks()
    todo.remove_task("Do homework")
    todo.view_tasks()
    
    # Filter even numbers
    nums = [1, 2, 3, 4, 5, 6]
    print(f"\nEven numbers in {nums}: {filter_even_numbers(nums)}")

if __name__ == "__main__":
    main()