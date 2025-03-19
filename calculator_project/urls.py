from django.urls import path
from . import views

urlpatterns = [
    path('calculator/', views.calculator_view, name='calculator'),
]
