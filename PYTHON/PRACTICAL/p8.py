
def basic_exception_demo():
    print("\n===== Basic Exception Handling =====")
    
    try:
        x = 10 / 0
    except ZeroDivisionError:
        print("Cannot divide by zero")
    
    try:
        num = int("abc")
    except ValueError:
        print("Invalid conversion")
    except ZeroDivisionError:
        print("Division by zero")
    
    try:
        num = int("123")
    except ValueError:
        print("Not a valid number")
    else:
        print(f"Conversion successful: {num}")
    
    try:
        file = open("nonexistent.txt", "r")
    except FileNotFoundError:
        print("File not found")
    finally:
        print("This always executes")


class InsufficientFundsError(Exception):
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


def main():
    basic_exception_demo()
    
    custom_exception_demo()
    
    my_list = [10, 20, 30, 40, 50]
    access_list_element(my_list)
    
    convert_to_integer()

if __name__ == "__main__":
    main()