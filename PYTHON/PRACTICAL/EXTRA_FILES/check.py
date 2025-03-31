def segregate_numbers(numbers):
    with open("odd_numbers.txt", "w") as odd_file, open(
        "even_numbers.txt", "w"
    ) as even_file:
        for num in numbers:
            if num % 2 == 0:
                even_file.write(f"{num}\n")
            else:
                odd_file.write(f"{num}\n")

    print("Numbers have been segregated:")
    print("- Odd numbers saved to 'odd_numbers.txt'")
    print("- Even numbers saved to 'even_numbers.txt'")
    print("\nContent of odd_numbers.txt:")
    with open("odd_numbers.txt", "r") as odd_file:
        print(odd_file.read())

    print("Content of even_numbers.txt:")
    with open("even_numbers.txt", "r") as even_file:
        print(even_file.read())

if __name__ == "__main__":
    input_str = input("Enter a list of numbers separated by spaces: ")
    numbers = [int(num) for num in input_str.split()]
    segregate_numbers(numbers)
