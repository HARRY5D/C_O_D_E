def add(a, b):
    return a + b
def subtract(a, b):
    return a - b
def multiply(a, b):
    return a * b
def divide(a, b):
    if b == 0:
        return "Error! Division by zero is not allowed."
    return a / b
def calculator():
    print("Simple Calculator")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    choice = input("Enter choice (1-4): ")
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    if choice == "1":
        print(f"{num1} + {num2} = {add(num1, num2)}")
    elif choice == "2":
        print(f"{num1} - {num2} = {subtract(num1, num2)}")
    elif choice == "3":
        print(f"{num1} * {num2} = {multiply(num1, num2)}")
    elif choice == "4":
        print(f"{num1} / {num2} = {divide(num1, num2)}")
    else:
        print("Invalid input")
if __name__ == "__main__":
    calculator()


def factorial(n):
    if n < 0:
        return "-ive number"
    elif n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def main():
    try:
        num = int(input("Enter a non-negative integer: "))
        result = factorial(num)
        print(f"The factorial of {num} is: {result}")
    except ValueError:
        print("Please enter a valid integer.")

if __name__ == "__main__":
    main()


def find_maximum(numbers):
    if not numbers:
        return None
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val
def find_minimum(numbers):
    if not numbers:
        return None
    min_val = numbers[0]
    for num in numbers:
        if num < min_val:
            min_val = num
    return min_val
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
def calculate_average(numbers):
    if not numbers:
        return None
    return calculate_sum(numbers) / len(numbers)
def main():
    try:
        input_str = input("Enter numbers: ")
        numbers = [float(x) for x in input_str.split()]
        print(f"List: {numbers}")
        print(f"Maximum: {find_maximum(numbers)}")
        print(f"Minimum: {find_minimum(numbers)}")
        print(f"Sum: {calculate_sum(numbers)}")
        print(f"Average: {calculate_average(numbers)}")
    except ValueError:
        print("Please enter valid numbers.")
if __name__ == "__main__":
    main()


def generate_fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    fibonacci = [0, 1]
    for i in range(2, n):
        fibonacci.append(fibonacci[i - 1] + fibonacci[i - 2])
    return fibonacci
def main():
    try:
        n = int(input("Enter the number: "))
        if n <= 0:
            print("Please enter a positive integer.")
        else:
            sequence = generate_fibonacci(n)
            print(f"Fibonacci sequence with {n} terms: {sequence}")
    except ValueError:
        print("Please enter a valid integer.")
if __name__ == "__main__":
    main()


def add_to_dict(dictionary, key, value):
    dictionary[key] = value
    return dictionary
def update_dict(dictionary, key, value):
    if key in dictionary:
        dictionary[key] = value
        return True
    return False
def delete_from_dict(dictionary, key):
    if key in dictionary:
        del dictionary[key]
        return True
    return False
def merge_dicts(dict1, dict2):
    merged_dict = dict1.copy()
    merged_dict.update(dict2)
    return merged_dict
def display_dict(dictionary):
    if not dictionary:
        print("Dictionary is empty.")
    else:
        print("Dictionary contents:")
        for key, value in dictionary.items():
            print(f"{key}: {value}")
def main():
    my_dict = {}
    my_dict = add_to_dict(my_dict, "name", "John")
    my_dict = add_to_dict(my_dict, "age", 30)
    my_dict = add_to_dict(my_dict, "city", "New York")
    print("After adding key-value pairs:")
    display_dict(my_dict)
    update_dict(my_dict, "age", 31)
    print("\nAfter updating age:")
    display_dict(my_dict)
    delete_from_dict(my_dict, "city")
    print("\nAfter deleting city:")
    display_dict(my_dict)
    other_dict = {"country": "USA", "job": "Developer"}
    merged = merge_dicts(my_dict, other_dict)
    print("\nAfter merging with another dictionary:")
    display_dict(merged)
if __name__ == "__main__":
    main()



def add_task(todo_list, task):
    todo_list.append(task)
    return f"Task '{task}' added successfully."

def remove_task(todo_list, index):
    if 0 <= index < len(todo_list):
        task = todo_list.pop(index)
        return f"Task '{task}' removed successfully."
    return "Invalid task index."

def view_tasks(todo_list):
    if not todo_list:
        return "Your to-do list is empty."

    result = "To-Do List:\n"
    for i, task in enumerate(todo_list):
        result += f"{i+1}. {task}\n"
    return result

def main():
    todo_list = []
    while True:
        print("1. Add Task")
        print("2. Remove Task")
        print("3. View Tasks")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            task = input("Enter the task: ")
            print(add_task(todo_list, task))
        elif choice == "2":
            print(view_tasks(todo_list))
            if todo_list:
                try:
                    index = int(input("Enter the task number to remove: ")) - 1
                    print(remove_task(todo_list, index))
                except ValueError:
                    print("Please enter a valid number.")
        elif choice == "3":
            print(view_tasks(todo_list))
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()


def filter_even_numbers(numbers):
    even_numbers = []
    for num in numbers:
        if num % 2 == 0:
            even_numbers.append(num)
    return even_numbers

def main():
    try:
        input_str = input("Enter a list of numbers: ")
        numbers = [int(num) for num in input_str.split()]

        even_numbers = filter_even_numbers(numbers)

        print(f"Original list: {numbers}")
        print(f"Even numbers: {even_numbers}")
    except ValueError:
        print("Please enter valid integers separated by spaces.")

if __name__ == "__main__":
    main()


def find_largest_smallest(numbers):
    if not numbers:
        return None, None

    largest = smallest = numbers[0]
    for num in numbers:
        if num > largest:
            largest = num
        if num < smallest:
            smallest = num

    return largest, smallest

def main():
    try:
        input_str = input("Enter a list of numbers: ")
        numbers = [float(num) for num in input_str.split()]
        if not numbers:
            print("The list is empty.")
        else:
            largest, smallest = find_largest_smallest(numbers)
            print(f"List: {numbers}")
            print(f"Largest number: {largest}")
            print(f"Smallest number: {smallest}")
    except ValueError:
        print("Please enter valid numbers separated by spaces.")

if __name__ == "__main__":
    main()
