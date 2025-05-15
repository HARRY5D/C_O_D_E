from django.db import models
from django.contrib.auth.models import User
import uuid

class Group(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4()).split('-')[0]
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.user.username

class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_paid')
    date = models.DateField(auto_now_add=True)
    shared_among = models.ManyToManyField(User, related_name='shared_expenses')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} - {self.amount}"
    
    def get_split_amount(self):
        return self.amount / self.shared_among.count() if self.shared_among.count() > 0 else 0