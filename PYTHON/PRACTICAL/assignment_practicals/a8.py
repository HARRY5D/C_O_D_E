def basic_exception_demo():
    print("\n -----Basic Exception Handling-----")
    
    try:
        x = 10 / 0
    except ZeroDivisionError:
        print("x = 10/0 : Cannot divide by zero")
    
    try:
        num = int("abc")
    except ValueError:
        print("int(abc) : Invalid conversion")
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


class AgeRestrictionError(Exception):
    def __init__(self, age, min_age):
        self.age = age
        self.min_age = min_age
        self.message = f"Age {age} is below the minimum required age of {min_age}."
        super().__init__(self.message)

def verify_age(age, min_age=18):
    if age < min_age:
        raise AgeRestrictionError(age, min_age)
    return f"Age verification successful. Access granted."

def custom_exception_demo():
    print("\n-----Custom Exception Demo-----")
    
    try:
        age = int(input("Enter your age: "))
        result = verify_age(age)
        print(result)
    except AgeRestrictionError as e:
        print(f"Error: {e}")
    except ValueError:
        print("Error: Please enter a valid number for age.")


def access_list_element(my_list):
    print("\n IndexError Handling ")
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