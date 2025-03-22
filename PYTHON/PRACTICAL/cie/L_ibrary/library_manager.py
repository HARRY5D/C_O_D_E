from books import Book

class LibraryManager:
    def __init__(self):
        self.books = {}
    
    def add_book(self, title, author):
        book = Book(title, author)
        self.books[title] = book
    
    def borrow_book(self, title):
        if title not in self.books:
            return f"Book '{title}' not found!"
        
        book = self.books[title]
        if not book.is_available():
            return "Book not available!"
        
        book.available = False
        return f"{title} borrowed!"
    
    def return_book(self, title):
        if title not in self.books:
            return f"Book '{title}' not found!"
        
        book = self.books[title]
        book.available = True
        return "Book returned!"
    
    def show_books(self):
        available_books = [book for book in self.books.values() if book.is_available()]
        if not available_books:
            return "No books available!"
        
        result = "Available books:\n"
        for book in available_books:
            result += f"{book}\n"
        return result.strip()