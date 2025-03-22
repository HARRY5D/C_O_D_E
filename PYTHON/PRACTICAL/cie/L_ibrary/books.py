
class Book:
    def __init__(self, title, author, available=True):
        self.title = title
        self.author = author
        self.available = available
    
    def is_available(self):
        return self.available
    
    def __str__(self):
        return f"{self.title} BY {self.author}"