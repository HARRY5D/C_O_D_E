# ===== Basic Exception Handling =====

def basic_exception_demo():
    print("\n===== Basic Exception Handling =====")
    
    # Simple try-except
    try:
        x = 10 / 0
    except ZeroDivisionError:
        print("Cannot divide by zero")
    
    # Multiple except blocks
    try:
        num = int("abc")
    except ValueError:
        print("Invalid conversion")
    except ZeroDivisionError:
        print("Division by zero")
    
    # Try-except-else
    try:
        num = int("123")
    except ValueError:
        print("Not a valid number")
    else:
        print(f"Conversion successful: {num}")
    
    # Try-except-finally
    try:
        file = open("nonexistent.txt", "r")
    except FileNotFoundError:
        print("File not found")
    finally:
        print("This always executes")

# ===== Custom Exception =====

class InsufficientFundsError(Exception):
    """Exception raised when withdrawing more money than available."""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        self.message = f"Cannot withdraw ${amount}. Balance is ${balance}."
        super().__init__(self.message)

def bank_withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount

def custom_exception_demo():
    print("\n===== Custom Exception Demo =====")
    
    balance = 500
    try:
        balance = bank_withdraw(balance, 700)
        print(f"Withdrawal successful. New balance: ${balance}")
    except InsufficientFundsError as e:
        print(f"Error: {e}")

# ===== IndexError Handling =====

def access_list_element(my_list):
    print("\n===== IndexError Handling =====")
    print(f"List: {my_list}")
    
    while True:
        try:
            index = int(input("Enter an index: "))
            element = my_list[index]
            print(f"Element at index {index}: {element}")
            break
        except IndexError:
            print(f"Error: Index out of range. Please enter an index between 0 and {len(my_list)-1}.")
        except ValueError:
            print("Error: Please enter a valid integer.")

# ===== ValueError Handling =====

def convert_to_integer():
    print("\n===== ValueError Handling =====")
    
    while True:
        try:
            user_input = input("Enter a number: ")
            number = int(user_input)
            print(f"Successfully converted to integer: {number}")
            return number
        except ValueError:
            print(f"Error: '{user_input}' is not a valid integer. Please try again.")

# ===== Main Function =====

def main():
    # Demonstrate basic exception handling
    basic_exception_demo()
    
    # Demonstrate custom exception
    custom_exception_demo()
    
    # Demonstrate IndexError handling
    my_list = [10, 20, 30, 40, 50]
    access_list_element(my_list)
    
    # Demonstrate ValueError handling
    convert_to_integer()

if __name__ == "__main__":
    main()