from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Group, Expense

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one number.")
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("Password must contain at least one letter.")
        return password

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class JoinGroupForm(forms.Form):
    code = forms.CharField(max_length=20, required=True)

class ExpenseForm(forms.ModelForm):
    shared_among = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'paid_by', 'shared_among']
    
    def __init__(self, group=None, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        if group:
            from .models import UserProfile
            user_ids = UserProfile.objects.filter(group=group).values_list('user_id', flat=True)
            self.fields['paid_by'].queryset = User.objects.filter(id__in=user_ids)
            self.fields['shared_among'].queryset = User.objects.filter(id__in=user_ids)