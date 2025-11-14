from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Transaction(models.Model):
    TYPE_CHOICES = (('income', 'Income'), ('expense', 'Expense'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(choices=TYPE_CHOICES, max_length=7)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.type}: {self.amount} ({self.user.username})"

class Budget(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='budget')
    month = models.CharField(max_length=7)  # 'YYYY-MM'
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.user.username} - {self.month}"
