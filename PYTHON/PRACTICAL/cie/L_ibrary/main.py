
from cie.L_ibrary.library_manager import LibraryManager

def main():
    manager = LibraryManager()
    
    print.upper("Enter the number of books to add:")
    
    n = int(input())
    print.upper("Enter the name of books and author to add:")
    #print("Enter the number of books to add:")
    
    
    for _ in range(n):
        book_info = input().split(' ', 1)
        if len(book_info) >= 2:
            title = book_info[0]
            author = book_info[1]
            for i in range(2, len(book_info)):
                title += " " + book_info[i-1]
                author = book_info[i]
        else:
            title = book_info[0]
            author = "Unknown"
        manager.add_book(title, author)
    
    while True:
        try:
            print.upper("Enter the transaction (Borrow:B / Return : R) and book title:")
            transaction = input()
            if not transaction:
                break
                
            action, title = transaction.split(' ', 1)
            
            if action == 'B':
                result = manager.borrow_book(title)
                print(result)
            elif action == 'R':
                result = manager.return_book(title)
                print(result)
        except EOFError:
            break
    
    print(manager.show_books())

if __name__ == "__main__":
    main()