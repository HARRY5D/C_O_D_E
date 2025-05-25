from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='expenses/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('accounts/signup/', views.signup_view, name='signup'),
    
    # Dashboard and group management
    path('dashboard/', views.dashboard, name='dashboard'),
    path('select-group/', views.select_group, name='select_group'),
    path('group-members/', views.group_members, name='group_members'),
    
    # Expense management
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/<int:expense_id>/', views.expense_detail, name='expense_detail'),
    path('expenses/<int:expense_id>/delete/', views.delete_expense, name='delete_expense'),
]