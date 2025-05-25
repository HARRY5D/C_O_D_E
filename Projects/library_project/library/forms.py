from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Borrower

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    is_admin = forms.BooleanField(required=False, label="Register as library staff")
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_admin')
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one number.")
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("Password must contain at least one letter.")
        return password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if self.cleaned_data.get('is_admin'):
            user.is_staff = True
        if commit:
            user.save()
        return user

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'ISBN', 'genre']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BorrowForm(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput())
    
class ReturnForm(forms.Form):
    borrower_id = forms.IntegerField(widget=forms.HiddenInput())