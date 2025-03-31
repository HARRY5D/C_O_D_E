class Shape:
    def calculate_area(self):
        pass
    def display_area(self):
        print(f"The area is: {self.calculate_area()}")

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def calculate_area(self):
        return 3.14159 * self.radius**2

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def calculate_area(self):
        return self.length * self.width

if __name__ == "__main__":
    circle = Circle(5)
    rectangle = Rectangle(4, 6)
    print(f"Circle area: {circle.calculate_area()}")
    print(f"Rectangle area: {rectangle.calculate_area()}")
    shapes = [Circle(3), Rectangle(5, 4), Circle(7)]
    for i, shape in enumerate(shapes, 1):
        print(f"Shape {i}:", end=" ")
        shape.display_area()



class Book:
    def __init__(self, title, author, isbn):
        self.__title = title
        self.__author = author
        self.__isbn = isbn

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_isbn(self):
        return self.__isbn

    def set_title(self, title):
        self.__title = title

    def set_author(self, author):
        self.__author = author

    def set_isbn(self, isbn):
        if isinstance(isbn, str) and len(isbn) > 0:
            self.__isbn = isbn
        else:
            print("Invalid ISBN format")

    def display_info(self):
        print("Book Information:")
        print(f"Title: {self.__title}")
        print(f"Author: {self.__author}")
        print(f"ISBN: {self.__isbn}")

if __name__ == "__main__":
    book = Book("Python Programming", "John Smith", "978-1234567890")
    book.display_info()
    print("\nAccessing with getters:")
    print(f"Title: {book.get_title()}")
    print(f"Author: {book.get_author()}")
    print("\nModifying book information...")
    book.set_title("Advanced Python Programming")
    book.set_author("Jane Doe")
    print("\nAfter modifications:")
    book.display_info()
    print("\nDemonstrating encapsulation:")
    book.__title = "Invalid Title"
    print(f"Title: {book.get_title()}")

