from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from decimal import Decimal

from .forms import SignUpForm, GroupForm, JoinGroupForm, ExpenseForm
from .models import UserProfile, Group, Expense

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'expenses/signup.html', {'form': form})

@login_required
def dashboard(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if not profile.group:
            return redirect('select_group')
        
        # Get group members
        members = UserProfile.objects.filter(group=profile.group)
        member_ids = [m.user.id for m in members]
        
        # Get recent expenses
        recent_expenses = Expense.objects.filter(group=profile.group).order_by('-date')[:10]
        
        # Calculate balances
        balances = {}
        for member in members:
            # Amount paid by user
            paid = Expense.objects.filter(
                group=profile.group, 
                paid_by=member.user
            ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
            
            # Amount shared by user
            owed = Decimal('0.00')
            expenses_shared = Expense.objects.filter(
                group=profile.group,
                shared_among=member.user
            )
            
            for expense in expenses_shared:
                split = expense.amount / expense.shared_among.count()
                owed += split
            
            # Calculate net balance
            balances[member.user.username] = {
                'paid': paid,
                'owed': owed,
                'net': paid - owed
            }
        
        return render(request, 'expenses/dashboard.html', {
            'profile': profile,
            'expenses': recent_expenses,
            'balances': balances,
            'members': members
        })
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user)
        return redirect('dashboard')

@login_required
def select_group(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    # Create group form
    if request.method == 'POST' and 'create_group' in request.POST:
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            group = group_form.save()
            profile.group = group
            profile.save()
            messages.success(request, f'Group "{group.name}" created successfully! Your invite code is: {group.code}')
            return redirect('dashboard')
    else:
        group_form = GroupForm()
    
    # Join group form
    if request.method == 'POST' and 'join_group' in request.POST:
        join_form = JoinGroupForm(request.POST)
        if join_form.is_valid():
            code = join_form.cleaned_data['code']
            try:
                group = Group.objects.get(code=code)
                profile.group = group
                profile.save()
                messages.success(request, f'Successfully joined group "{group.name}"!')
                return redirect('dashboard')
            except Group.DoesNotExist:
                messages.error(request, 'Invalid group code. Please try again.')
    else:
        join_form = JoinGroupForm()
    
    return render(request, 'expenses/select_group.html', {
        'group_form': group_form,
        'join_form': join_form
    })

@login_required
def add_expense(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.group:
        return redirect('select_group')
    
    if request.method == 'POST':
        form = ExpenseForm(profile.group, request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.group = profile.group
            expense.save()

            # Many-to-many relationships must be saved after the main object
            form.save_m2m()
            
            messages.success(request, 'Expense added successfully!')
            return redirect('dashboard')
    else:
        form = ExpenseForm(profile.group, initial={'paid_by': request.user})
    
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def expense_list(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.group:
        return redirect('select_group')
    
    expenses = Expense.objects.filter(group=profile.group).order_by('-date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def expense_detail(request, expense_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.group:
        return redirect('select_group')
    
    expense = get_object_or_404(Expense, id=expense_id, group=profile.group)
    split_amount = expense.get_split_amount()
    
    return render(request, 'expenses/expense_detail.html', {
        'expense': expense,
        'split_amount': split_amount
    })

@login_required
def delete_expense(request, expense_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    expense = get_object_or_404(Expense, id=expense_id)
    
    # Check if user is authorized (only the one who added it can delete)

    if expense.paid_by != request.user:
        messages.error(request, "You don't have permission to delete this expense.")
        return redirect('expense_list')
    
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expense_list')
    
    return render(request, 'expenses/delete_expense.html', {'expense': expense})

@login_required
def group_members(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.group:
        return redirect('select_group')
    
    members = UserProfile.objects.filter(group=profile.group)
    return render(request, 'expenses/group_members.html', {'members': members})