
import os

def demo_file_basics():
    
    with open("sample.txt", "w") as file:
        file.write("Hello, World!\n")
     
    with open("sample.txt", "r") as file:
        content = file.read()
    print(content)
    
    with open("sample.txt", "r") as file:
        line_num = 1
        for line in file:
            print(f"Line {line_num}: {line.strip()}")
            line_num += 1

def odd_even(numbers):
    
    with open("odd_numbers.txt", "w") as odd_file, open("even_numbers.txt", "w") as even_file:
        for num in numbers:
            if num % 2 == 0:
                even_file.write(f"{num}\n")
            else:
                odd_file.write(f"{num}\n")
    
    
    print("\nOdd numbers:")
    with open("odd_numbers.txt", "r") as file:
        print(file.read())
    
    print("\nEven numbers:")
    with open("even_numbers.txt", "r") as file:
        print(file.read())

def demonstrate_file_methods():

    with open("demo_methods.txt", "w") as file:
        file.write("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    with open("demo_methods.txt", "r") as file:
        print(f"First 5 characters: {file.read(5)}")
        
        position = file.tell()
        print(f"Current position: {position}")
        
        file.seek(10)
        print(f"After seek(10): {file.read(5)}")
        file.seek(0)
        print(f"After seek(0): {file.read()}")
    
    if os.path.exists("demo_methods.txt"):
        print("File exists!")
        
        os.rename("demo_methods.txt", "renamed_file.txt")
        print("File renamed to 'renamed_file.txt")
        
        p = os.path.abspath("renamed_file.txt")
        print(f"Absolute path: {p}")
        
        os.remove("renamed_file.txt")
        print("File has been removed")

def read_5_words():
    """Reads and displays any 5 words from a text file."""
    print("\n===== Reading 5 Words =====")
    
    with open("words_sample.txt", "w") as file:
        file.write("This is a sample text file for demonstration.")
    
    with open("words_sample.txt", "r") as file:
        content = file.read()
        words = content.split()
        selected_words = words[:5]  # Get first 5 words
    
    print(f"5 words from the file: {' '.join(selected_words)}")

def create_triangle():
    """Generates a triangle pattern and saves it to a file."""
    print("\n===== Creating Triangle Pattern =====")
    
    triangle = []
    for i in range(1, 6):
        for j in range(0,6):
          line = 'j' * i
        triangle.append(line)
    
    with open("triangle.txt", "w") as file:
        for line in triangle:
            file.write(line + "\n")
    
    print("Triangle pattern saved to 'triangle.txt'")
    
    print("\nTriangle Pattern:")
    with open("triangle.txt", "r") as file:
        print(file.read())

def appendix_operations():
    """Additional file operations for demonstration."""
    print("\n===== Appending to Files =====")
    
    with open("append_demo.txt", "w") as file:
        file.write("Initial content.\n")
    
    with open("append_demo.txt", "a") as file:
        file.write("This line is appended.\n")
        file.write("This is another appended line.\n")
    
    with open("append_demo.txt", "r") as file:
        content = file.read()
    
    print("File after appending:")
    print(content)

def main():
    
    demo_file_basics()
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    odd_even(numbers)
    
    demonstrate_file_methods()
    
    read_5_words()
    
    create_triangle()
    
    appendix_operations()
    

if __name__ == "__main__":
    main()