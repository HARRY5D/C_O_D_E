"""
Practical 7: File Operations in Python
This program demonstrates various file operations including reading, writing, and manipulating files.
"""
import os

def demo_file_basics():
    """Demonstrates basic file operations - creating, writing, and reading."""
    print("\n===== Basic File Operations =====")
    
    # Write to a file
    with open("sample.txt", "w") as file:
        file.write("Hello, World!\n")
        file.write("This is a demonstration of file operations in Python.\n")
        file.write("File handling is an essential skill for any programmer.")
    print("File 'sample.txt' created and written successfully.")
    
    # Read from the file
    with open("sample.txt", "r") as file:
        content = file.read()
    print("\nReading entire file at once:")
    print(content)
    
    # Read line by line
    print("\nReading file line by line:")
    with open("sample.txt", "r") as file:
        line_num = 1
        for line in file:
            print(f"Line {line_num}: {line.strip()}")
            line_num += 1

def process_numbers(numbers):
    """Separates odd and even numbers into different files."""
    print("\n===== Processing Numbers =====")
    
    # Open files for writing
    with open("odd_numbers.txt", "w") as odd_file, open("even_numbers.txt", "w") as even_file:
        for num in numbers:
            if num % 2 == 0:
                even_file.write(f"{num}\n")
            else:
                odd_file.write(f"{num}\n")
    
    print("Numbers have been separated into odd_numbers.txt and even_numbers.txt")
    
    # Read and display the results
    print("\nOdd numbers:")
    with open("odd_numbers.txt", "r") as file:
        print(file.read())
    
    print("\nEven numbers:")
    with open("even_numbers.txt", "r") as file:
        print(file.read())

def demonstrate_file_methods():
    """Demonstrates various file methods like tell, seek, etc."""
    print("\n===== File Methods Demonstration =====")
    
    with open("demo_methods.txt", "w") as file:
        file.write("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    with open("demo_methods.txt", "r") as file:
        # Read first 5 characters
        print(f"First 5 characters: {file.read(5)}")
        
        # Show current position
        position = file.tell()
        print(f"Current position: {position}")
        
        # Move to position 10
        file.seek(10)
        print(f"After seek(10), next 5 characters: {file.read(5)}")
        
        # Move to beginning and read everything
        file.seek(0)
        print(f"After seek(0), all content: {file.read()}")
    
    # Check if file exists
    if os.path.exists("demo_methods.txt"):
        print("File exists!")
        
        # Rename file
        os.rename("demo_methods.txt", "renamed_file.txt")
        print("File renamed to 'renamed_file.txt'")
        
        # Get file path
        path = os.path.abspath("renamed_file.txt")
        print(f"Absolute path: {path}")
        
        # Remove file
        os.remove("renamed_file.txt")
        print("File has been removed")

def read_5_words():
    """Reads and displays any 5 words from a text file."""
    print("\n===== Reading 5 Words =====")
    
    # Create a file with sample text
    with open("words_sample.txt", "w") as file:
        file.write("The quick brown fox jumps over the lazy dog. ")
        file.write("Programming in Python is fun and rewarding. ")
        file.write("File operations are essential for data processing.")
    
    # Read 5 words from the file
    with open("words_sample.txt", "r") as file:
        content = file.read()
        words = content.split()
        selected_words = words[:5]  # Get first 5 words
    
    print(f"5 words from the file: {' '.join(selected_words)}")

def create_triangle():
    """Generates a triangle pattern and saves it to a file."""
    print("\n===== Creating Triangle Pattern =====")
    
    # Create triangle pattern
    triangle = []
    for i in range(1, 6):
        line = '*' * i
        triangle.append(line)
    
    # Write to file
    with open("triangle.txt", "w") as file:
        for line in triangle:
            file.write(line + "\n")
    
    print("Triangle pattern saved to 'triangle.txt'")
    
    # Display the triangle
    print("\nTriangle Pattern:")
    with open("triangle.txt", "r") as file:
        print(file.read())

def appendix_operations():
    """Additional file operations for demonstration."""
    print("\n===== Appending to Files =====")
    
    # Create a file
    with open("append_demo.txt", "w") as file:
        file.write("Initial content.\n")
    
    # Append to the file
    with open("append_demo.txt", "a") as file:
        file.write("This line is appended.\n")
        file.write("This is another appended line.\n")
    
    # Read the file
    with open("append_demo.txt", "r") as file:
        content = file.read()
    
    print("File after appending:")
    print(content)

def main():
    print("===== File Operations in Python =====")
    
    # Demonstrate basic file operations
    demo_file_basics()
    
    # Process odd and even numbers
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    process_numbers(numbers)
    
    # Demonstrate various file methods
    demonstrate_file_methods()
    
    # Read 5 words from a file
    read_5_words()
    
    # Create a triangle pattern
    create_triangle()
    
    # Demonstrate appending to files
    appendix_operations()
    
    print("\n===== Program Complete =====")

if __name__ == "__main__":
    main()