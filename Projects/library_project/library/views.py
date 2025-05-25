from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .forms import SignUpForm, BookForm, BorrowForm, ReturnForm
from .models import Book, Borrower

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'library/signup.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('client_dashboard')

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    books = Book.objects.all()
    borrowers = Borrower.objects.all()
    return render(request, 'library/admin_dashboard.html', {
        'books': books,
        'borrowers': borrowers
    })

@login_required
def client_dashboard(request):
    # Get available books for borrowing
    available_books = Book.objects.filter(is_available=True)
    
    # Get user's borrowed books
    borrowed_books = Borrower.objects.filter(
        user=request.user,
        borrowed_book__isnull=False,
        return_date__isnull=True
    )
    
    return render(request, 'library/client_dashboard.html', {
        'available_books': available_books,
        'borrowed_books': borrowed_books
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = BookForm(instance=book)
    return render(request, 'library/edit_book.html', {'form': form, 'book': book})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('admin_dashboard')
    return render(request, 'library/delete_book.html', {'book': book})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Check if book is available
    if not book.is_available:
        return redirect('client_dashboard')
    
    if request.method == 'POST':
        # Create borrower record
        borrower = Borrower(
            user=request.user,
            name=request.user.username,
            email=request.user.email,
            borrowed_book=book
        )
        borrower.save()
        
        # Update book availability
        book.is_available = False
        book.save()
        
        return redirect('client_dashboard')
    
    return render(request, 'library/borrow_book.html', {'book': book})

@login_required
def return_book(request, borrower_id):
    borrower = get_object_or_404(Borrower, id=borrower_id, user=request.user)
    
    if request.method == 'POST':
        # Update return date
        borrower.return_date = timezone.now()
        borrower.save()
        
        # Update book availability
        book = borrower.borrowed_book
        book.is_available = True
        book.save()
        
        return redirect('client_dashboard')
    
    return render(request, 'library/return_book.html', {'borrower': borrower})